import os
import discord
from discord.ext import commands
from discord import app_commands, Embed, ButtonStyle, TextStyle
from discord.ui import View, Button, Modal, TextInput, Select

# ================= Configuration =================
TOKEN = os.getenv("DISCORD_TOKEN")

# Category IDs
BOOST_CATEGORY_ID = 1534328814707151151
CARRY_CATEGORY_ID = 1534328768611618846

# Role ID allowed to write 'done'
STAFF_ROLE_ID = 1534345538080870480

# Payment Infos
MY_RIB_INFO = "Bank: CIH BANK\nRIB: 0644507960825345253\nName: Omar"
MY_PAYPAL_INFO = "PayPal Email: Omarjr"

# Image URLs (Put direct image links here or host them permanently)
IMAGE_PRICES_1 = "https://cdn.discordapp.com/attachments/1254112291096363150/1534346676989464587/image.png"
IMAGE_PRICES_2 = "https://cdn.discordapp.com/attachments/1254112291096363150/1534347605138739250/image.png"

# Prices Matrix for Ranks
RANK_PRICES = {
    "Bronze I": 0, "Bronze II": 1, "Bronze III": 1,
    "Silver I": 1, "Silver II": 1.5, "Silver III": 1.5,
    "Gold I": 2, "Gold II": 2, "Gold III": 2,
    "Diamond I": 2, "Diamond II": 2, "Diamond III": 3,
    "Mythic I": 4, "Mythic II": 5, "Mythic III": 6,
    "Legendary I": 9, "Legendary II": 12, "Legendary III": 15,
    "Masters I": 30, "Masters II": 60, "Pro": 105
}

RANKS_ORDER = list(RANK_PRICES.keys())

def calculate_price(current_rank: str, desired_rank: str, order_type: str) -> float:
    try:
        start_idx = RANKS_ORDER.index(current_rank)
        end_idx = RANKS_ORDER.index(desired_rank)
        if start_idx >= end_idx:
            return 0.0
        base_total = sum(RANK_PRICES[RANKS_ORDER[i]] for i in range(start_idx + 1, end_idx + 1))
        multiplier = 2.0 if order_type == "Carry" else 1.0
        return round(base_total * multiplier, 2)
    except ValueError:
        return 0.0

# ================= Discord Bot Setup =================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Confirmation View for Closing
class ConfirmCloseView(View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="Yes, Close", style=ButtonStyle.danger, emoji="✅", custom_id="confirm_close_btn")
    async def confirm(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🔒 Closing channel in 5 seconds...")
        await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.datetime.timedelta(seconds=5))
        await interaction.channel.delete()

    @discord.ui.button(label="Cancel", style=ButtonStyle.secondary, emoji="❌", custom_id="cancel_close_btn")
    async def cancel(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Closing cancelled.", ephemeral=True)
        await interaction.message.delete()

# Modal for Close with Reason
class CloseReasonModal(Modal):
    def __init__(self):
        super().__init__(title="Close Ticket With Reason")
        self.reason = TextInput(
            label="Reason for closing",
            style=TextStyle.paragraph,
            placeholder="Write the reason here...",
            required=True
        )
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        reason_text = self.reason.value
        await interaction.response.send_message(f"🔒 Ticket closing. Reason: **{reason_text}**\nDeleting in 5 seconds...")
        await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.datetime.timedelta(seconds=5))
        await interaction.channel.delete()

# Ticket Controls View
class TicketControlsView(View):
    def __init__(self, payment_method: str = "Bank Transfer / RIB", payment_enabled: bool = False):
        super().__init__(timeout=None)
        self.payment_method = payment_method

        self.close_btn = Button(label="Close", style=ButtonStyle.danger, emoji="🔒", custom_id="ticket_close_btn")
        self.close_btn.callback = self.close_callback

        self.close_reason_btn = Button(label="Close With Reason", style=ButtonStyle.secondary, emoji="📝", custom_id="ticket_close_reason_btn")
        self.close_reason_btn.callback = self.close_reason_callback

        self.sent_payment_btn = Button(
            label="I Sent Payment",
            style=ButtonStyle.success,
            emoji="💳",
            disabled=not payment_enabled,
            custom_id="ticket_sent_payment_btn"
        )
        self.sent_payment_btn.callback = self.sent_payment_callback

        self.add_item(self.close_btn)
        self.add_item(self.close_reason_btn)
        self.add_item(self.sent_payment_btn)

    async def close_callback(self, interaction: discord.Interaction):
        embed = Embed(
            title="Confirm Action",
            description="Are you sure you want to close this ticket?",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed, view=ConfirmCloseView(), ephemeral=True)

    async def close_reason_callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CloseReasonModal())

    async def sent_payment_callback(self, interaction: discord.Interaction):
        pm_lower = self.payment_method.lower()
        if "bank" in pm_lower or "rib" in pm_lower:
            pay_details = f"🏦 **Bank Transfer Details (RIB):**\n```\n{MY_RIB_INFO}\n```"
        else:
            pay_details = f"🅿️ **PayPal Details:**\n```\n{MY_PAYPAL_INFO}\n```"

        embed = Embed(
            title="Payment Instructions",
            description=f"{pay_details}\n\nPlease send a screenshot of the payment in this channel for verification!",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)

# Step-by-Step Dropdown Flow (Prevents mistyping)
class OrderDropdownFlowView(View):
    def __init__(self, order_type: str):
        super().__init__(timeout=180)
        self.order_type = order_type
        self.current_rank = None
        self.desired_rank = None
        self.power_11_count = None

        # Step 1: Select Current Rank
        self.current_select = Select(
            placeholder="Select your current rank...",
            options=[discord.SelectOption(label=rank, value=rank) for rank in RANKS_ORDER[:-1]]
        )
        self.current_select.callback = self.current_callback
        self.add_item(self.current_select)

    async def current_callback(self, interaction: discord.Interaction):
        self.current_rank = self.current_select.values[0]
        start_idx = RANKS_ORDER.index(self.current_rank)
        valid_desired = RANKS_ORDER[start_idx + 1:]

        self.clear_items()
        # Step 2: Select Desired Rank
        self.desired_select = Select(
            placeholder=f"Current: {self.current_rank} -> Select desired rank...",
            options=[discord.SelectOption(label=rank, value=rank) for rank in valid_desired[:25]]
        )
        self.desired_select.callback = self.desired_callback
        self.add_item(self.desired_select)

        await interaction.response.edit_message(
            content=f"✅ Current Rank: **{self.current_rank}**\nNow select your **Desired Rank**:",
            view=self
        )

    async def desired_callback(self, interaction: discord.Interaction):
        self.desired_rank = self.desired_select.values[0]

        self.clear_items()
        # Step 3: Select Power 11 Brawlers Count
        self.power_select = Select(
            placeholder="How many Power 11 brawlers do you have?",
            options=[
                discord.SelectOption(label="1 - 5 Brawlers", value="1-5"),
                discord.SelectOption(label="6 - 10 Brawlers", value="6-10"),
                discord.SelectOption(label="11 - 15 Brawlers", value="11-15"),
                discord.SelectOption(label="16 - 20 Brawlers", value="16-20"),
                discord.SelectOption(label="20+ Brawlers", value="20+")
            ]
        )
        self.power_select.callback = self.power_callback
        self.add_item(self.power_select)

        await interaction.response.edit_message(
            content=f"✅ Current: **{self.current_rank}** | Desired: **{self.desired_rank}**\nSelect **Power 11 Count**:",
            view=self
        )

    async def power_callback(self, interaction: discord.Interaction):
        self.power_11_count = self.power_select.values[0]

        self.clear_items()
        # Step 4: Select Payment Method
        self.payment_select = Select(
            placeholder="Select Payment Method...",
            options=[
                discord.SelectOption(label="Bank Transfer / RIB", emoji="🏦"),
                discord.SelectOption(label="PayPal", emoji="🅿️")
            ]
        )
        self.payment_select.callback = self.payment_callback
        self.add_item(self.payment_select)

        await interaction.response.edit_message(
            content=f"✅ Current: **{self.current_rank}** | Desired: **{self.desired_rank}** | Power 11: **{self.power_11_count}**\nSelect **Payment Method**:",
            view=self
        )

    async def payment_callback(self, interaction: discord.Interaction):
        pay_m = self.payment_select.values[0]
        category_id = CARRY_CATEGORY_ID if self.order_type == "Carry" else BOOST_CATEGORY_ID
        category = interaction.guild.get_channel(category_id)

        # Check for single ticket limit per user
        if category:
            for channel in category.text_channels:
                if channel.name == f"order-{interaction.user.name}".lower():
                    await interaction.response.edit_message(
                        content=f"❌ You already have an open ticket: {channel.mention}. Close it first!",
                        view=None
                    )
                    return

        await interaction.response.defer(ephemeral=True)

        total_price = calculate_price(self.current_rank, self.desired_rank, self.order_type)
        price_str = f"${total_price} USD" if total_price > 0 else "Custom Pricing"

        ticket_name = f"order-{interaction.user.name}".lower()

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        ticket_channel = await interaction.guild.create_text_channel(
            name=ticket_name,
            category=category if isinstance(category, discord.CategoryChannel) else None,
            overwrites=overwrites
        )

        header_embed = Embed(
            title="Ranked Boost Order Ticket",
            description=f"Your Ranked **{self.order_type}** order ticket is open 👊",
            color=0x8A2BE2
        )
        header_embed.set_footer(text="Powered by Iceyz BrawlMart™")

        details_embed = Embed(
            title="Your Ranked Boost Order Details",
            color=0x8A2BE2
        )
        details_embed.add_field(name="Current Rank 🛡️", value=f"└ `{self.current_rank}`", inline=False)
        details_embed.add_field(name="Desired Rank 🏆", value=f"└ `{self.desired_rank}`", inline=False)
        details_embed.add_field(name="Power 11 Brawlers ⚡", value=f"└ `{self.power_11_count}`", inline=False)
        details_embed.add_field(name="Order Type 🚀", value=f"└ `{self.order_type}`", inline=False)
        details_embed.add_field(name="Total Price 💰", value=f"└ `{price_str}`", inline=False)
        details_embed.add_field(name="Payment Method 💳", value=f"└ `{pay_m}`", inline=False)
        details_embed.set_footer(text=f"Powered by Iceyz BrawlMart™ • {interaction.user.id}")

        view = TicketControlsView(payment_method=pay_m, payment_enabled=False)

        msg = await ticket_channel.send(content=f"{interaction.user.mention}", embeds=[header_embed, details_embed], view=view)

        bot.ticket_data[ticket_channel.id] = {
            "payment_method": pay_m,
            "message_id": msg.id
        }

        await interaction.followup.send(f"Ticket created successfully! {ticket_channel.mention}", ephemeral=True)

# Service Select View
class ServiceTypeView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=ButtonStyle.success, emoji="🚀", custom_id="srv_boosted_btn")
    async def boosted_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Please select your order parameters using the menus below:", view=OrderDropdownFlowView("Boost"), ephemeral=True)

    @discord.ui.button(label="Get Carried (2x Price)", style=ButtonStyle.blurple, emoji="🤝", custom_id="srv_carried_btn")
    async def carried_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Please select your order parameters using the menus below:", view=OrderDropdownFlowView("Carry"), ephemeral=True)

# Main Ticket Panel View
class MainTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get Your Rank Upgraded", style=ButtonStyle.primary, emoji="👊", custom_id="get_rank_upgraded")
    async def upgrade_button(self, interaction: discord.Interaction, button: Button):
        embed = Embed(
            title="Choose your service type:",
            description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)",
            color=0x8A2BE2
        )
        await interaction.response.send_message(embed=embed, view=ServiceTypeView(), ephemeral=True)

# Command to Setup Main Panel
@bot.tree.command(name="setup_panel", description="Setup Ranked Boost Panel")
@app_commands.default_permissions(administrator=True)
async def setup_panel(interaction: discord.Interaction):
    # Single clean embed with image to remove the empty bottom line box
    embed1 = Embed(
        title="Ranked B00st Service",
        description="**What We Offer**\n• Climb the ranks with professional boosting service\n• Fast, secure, and reliable rank progression\n• Experienced boosters with proven track records",
        color=0x8A2BE2
    )
    embed1.set_image(url=IMAGE_PRICES_1)

    await interaction.channel.send(embed=embed1, view=MainTicketView())
    await interaction.response.send_message("Panel created successfully!", ephemeral=True)

@bot.event
async def on_ready():
    bot.ticket_data = getattr(bot, 'ticket_data', {})
    bot.add_view(MainTicketView())
    bot.add_view(ServiceTypeView())
    bot.add_view(TicketControlsView())
    await bot.tree.sync()
    print(f"Bot logged in as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.channel.id in bot.ticket_data:
        if message.content.strip().lower() == "done":
            has_staff_role = any(role.id == STAFF_ROLE_ID for role in message.author.roles)
            if not has_staff_role and not message.author.guild_permissions.administrator:
                await message.channel.send("❌ Only Staff members can use the `done` command!")
                return

            data = bot.ticket_data[message.channel.id]
            pm_method = data["payment_method"]
            msg_id = data["message_id"]

            try:
                msg = await message.channel.fetch_message(msg_id)
                new_view = TicketControlsView(payment_method=pm_method, payment_enabled=True)
                await msg.edit(view=new_view)
                await message.channel.send("✅ Payment button activated! Click **'I Sent Payment'** below to receive payment details.")
            except Exception as e:
                print(f"Error updating payment button: {e}")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)

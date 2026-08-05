import os
import discord
from discord.ext import commands
from discord import app_commands, Embed, ButtonStyle, TextStyle
from discord.ui import View, Button, Modal, TextInput, Select

# ================= Configuration =================
TOKEN = os.getenv("DISCORD_TOKEN")

BOOST_CATEGORY_ID = 1534328814707151151
CARRY_CATEGORY_ID = 1534328768611618846
STAFF_ROLE_ID = 1534345538080870480

MY_RIB_INFO = "Bank: CIH BANK\nRIB: 0644507960825345253\nName: Omar"
MY_PAYPAL_INFO = "PayPal Email: Omarjr"

# Dynamic payment details dictionary
PAYMENT_DETAILS = {
    "PayPal": f"🅿️ **PayPal Details:**\n```\n{MY_PAYPAL_INFO}\n```",
    "Bank Transfer Portal / RIB": f"🏦 **Bank Transfer Details (RIB):**\n```\n{MY_RIB_INFO}\n```",
    "Venmo": "💸 **Venmo Details:**\n```\nVenmo ID: @Omarjr\n```",
    "Cash App": "💵 **Cash App Details:**\n```\nCash Tag: $Omarjr\n```",
    "Wise": "🌍 **Wise Details:**\n```\nWise Email: Omarjr@wise.com\n```",
    "Apple Pay": "🍎 **Apple Pay Details:**\n```\nPhone / Email: Omarjr\n```",
    "Zelle": "⚡ **Zelle Details:**\n```\nZelle Email/Phone: Omarjr\n```",
    "Binance": "🟡 **Binance Details:**\n```\nBinance Pay ID: 123456789\n```",
    "Revolut": "💳 **Revolut Details:**\n```\nRevolut Tag: @Omarjr\n```",
    "Chime": "🟢 **Chime Details:**\n```\nChime Sign: $Omarjr\n```",
    "Skrill": "🟣 **Skrill Details:**\n```\nSkrill Email: Omarjr\n```",
    "Bitcoin": "🪙 **Bitcoin Wallet:**\n```\nBTC Address Here\n```",
    "Litecoin": "🥈 **Litecoin Wallet:**\n```\nLTC Address Here\n```",
    "Ethereum": "💎 **Ethereum Wallet:**\n```\nETH Address Here\n```",
    "Solana": "☀️ **Solana Wallet:**\n```\nSOL Address Here\n```",
    "Tether (USDT)": "💵 **Tether (USDT TRC20) Wallet:**\n```\nUSDT Address Here\n```"
}

IMAGE_PRICES_1 = "https://cdn.discordapp.com/attachments/1254112291096363150/1534346676989464587/image.png"
IMAGE_PRICES_2 = "https://cdn.discordapp.com/attachments/1254112291096363150/1534347605138739250/image.png"

# ================= CUSTOM EMOJIS CONFIGURATION =================
# حط الـ name والـ id ديال الإيموجي اللي هزيتي من السيرفر ديالك هنايا.
# إلا خليتي الـ id = None غايخدم بالإيموجي العادي (Default) تلقائياً.

CUSTOM_EMOJIS = {
    "PayPal": {"name": "paypal", "id": None, "animated": False},
    "Bank Transfer Portal / RIB": {"name": "bank", "id": None, "animated": False},
    "Venmo": {"name": "venmo", "id": None, "animated": False},
    "Cash App": {"name": "cashapp", "id": None, "animated": False},
    "Wise": {"name": "wise", "id": None, "animated": False},
    "Apple Pay": {"name": "applepay", "id": None, "animated": False},
    "Zelle": {"name": "zelle", "id": None, "animated": False},
    "Binance": {"name": "binance", "id": None, "animated": False},
    "Revolut": {"name": "revolut", "id": None, "animated": False},
    "Chime": {"name": "chime", "id": None, "animated": False},
    "Skrill": {"name": "skrill", "id": None, "animated": False},
    "Bitcoin": {"name": "bitcoin", "id": None, "animated": False},
    "Litecoin": {"name": "litecoin", "id": None, "animated": False},
    "Ethereum": {"name": "ethereum", "id": None, "animated": False},
    "Solana": {"name": "solana", "id": 1534559022730969160, "animated": False},
    "Tether (USDT)": {"name": "usdt", "id": None, "animated": False},
}

DEFAULT_EMOJIS = {
    "PayPal": "🅿️",
    "Bank Transfer Portal / RIB": "🏦",
    "Venmo": "🔹",
    "Cash App": "💵",
    "Wise": "🌐",
    "Apple Pay": "🍎",
    "Zelle": "⚡",
    "Binance": "🟡",
    "Revolut": "💳",
    "Chime": "🟢",
    "Skrill": "🟣",
    "Bitcoin": "🪙",
    "Litecoin": "🥈",
    "Ethereum": "💎",
    "Solana": "☀️",
    "Tether (USDT)": "💵"
}

# ----------------- RANKS EMOJIS -----------------
CUSTOM_RANK_EMOJIS = {
    "Bronze I": {"name": "bronze1", "id": None, "animated": False},
    "Bronze II": {"name": "bronze2", "id": None, "animated": False},
    "Bronze III": {"name": "bronze3", "id": None, "animated": False},
    "Silver I": {"name": "silver1", "id": None, "animated": False},
    "Silver II": {"name": "silver2", "id": None, "animated": False},
    "Silver III": {"name": "silver3", "id": None, "animated": False},
    "Gold I": {"name": "gold1", "id": None, "animated": False},
    "Gold II": {"name": "gold2", "id": None, "animated": False},
    "Gold III": {"name": "gold3", "id": None, "animated": False},
    "Diamond I": {"name": "diamond1", "id": None, "animated": False},
    "Diamond II": {"name": "diamond2", "id": None, "animated": False},
    "Diamond III": {"name": "diamond3", "id": None, "animated": False},
    "Mythic I": {"name": "mythic", "id": 1534572012658495629, "animated": False},
    "Mythic II": {"name": "mythic", "id": 1534572012658495629, "animated": False},
    "Mythic III": {"name": "mythic", "id": 1534572012658495629, "animated": False},
    "Legendary I": {"name": "legendary1", "id": None, "animated": False},
    "Legendary II": {"name": "legendary2", "id": None, "animated": False},
    "Legendary III": {"name": "legendary3", "id": None, "animated": False},
    "Masters I": {"name": "masters1", "id": None, "animated": False},
    "Masters II": {"name": "masters2", "id": None, "animated": False},
    "Pro": {"name": "pro", "id": None, "animated": False}
}

DEFAULT_RANK_EMOJIS = {
    "Bronze I": "🥉", "Bronze II": "🥉", "Bronze III": "🥉",
    "Silver I": "🥈", "Silver II": "🥈", "Silver III": "🥈",
    "Gold I": "🥇", "Gold II": "🥇", "Gold III": "🥇",
    "Diamond I": "💎", "Diamond II": "💎", "Diamond III": "💎",
    "Mythic I": "🔮", "Mythic II": "🔮", "Mythic III": "🔮",
    "Legendary I": "👑", "Legendary II": "👑", "Legendary III": "👑",
    "Masters I": "🔥", "Masters II": "🔥", "Pro": "⚡"
}

# ----------------- POWER 11 EMOJIS -----------------
CUSTOM_POWER11_EMOJIS = {
    "0": {"name": "power_0", "id": None, "animated": False},
    "1": {"name": "power_1", "id": None, "animated": False},
    "2": {"name": "power_2", "id": None, "animated": False},
    "3": {"name": "power_3", "id": None, "animated": False},
    "4": {"name": "power_4", "id": None, "animated": False},
    "5": {"name": "power_5", "id": None, "animated": False},
    "6-10": {"name": "power_6_10", "id": None, "animated": False},
    "11-15": {"name": "power_11_15", "id": None, "animated": False},
    "16-20": {"name": "power_16_20", "id": None, "animated": False},
    "20+": {"name": "power_20plus", "id": None, "animated": False}
}

DEFAULT_POWER11_EMOJIS = {
    "0": "❌", "1": "⚡", "2": "⚡", "3": "⚡", "4": "⚡", "5": "⚡",
    "6-10": "🔥", "11-15": "🔥", "16-20": "🌟", "20+": "👑"
}

def get_custom_or_default_emoji(label: str, custom_dict: dict, default_dict: dict, fallback="⭐"):
    custom = custom_dict.get(label)
    if custom and custom.get("id"):
        return discord.PartialEmoji(
            name=custom["name"],
            id=custom["id"],
            animated=custom.get("animated", False)
        )
    return default_dict.get(label, fallback)

PAYMENT_OPTIONS = [
    discord.SelectOption(label=label, emoji=get_custom_or_default_emoji(label, CUSTOM_EMOJIS, DEFAULT_EMOJIS, "💳"))
    for label in DEFAULT_EMOJIS.keys()
]

# ================= RANK CONFIGURATION =================
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

# Power 11 Brawlers options (0 to 20+)
POWER_11_OPTIONS = [
    discord.SelectOption(label="0 Brawlers", value="0", emoji=get_custom_or_default_emoji("0", CUSTOM_POWER11_EMOJIS, DEFAULT_POWER11_EMOJIS)),
    discord.SelectOption(label="1 Brawler", value="1", emoji=get_custom_or_default_emoji("1", CUSTOM_POWER11_EMOJIS, DEFAULT_POWER11_EMOJIS)),
    discord.SelectOption(label="2 Brawlers", value="2", emoji=get_custom_or_default_emoji("2", CUSTOM_POWER11_EMOJIS, DEFAULT_POWER11_EMOJIS)),
    discord.SelectOption(label="3 Brawlers", value="3", emoji=get_custom_or_default_emoji("3", CUSTOM_POWER11_EMOJIS, DEFAULT_POWER11_EMOJIS)),
    discord.SelectOption(label="4 Brawlers", value="4", emoji=get_custom_or_default_emoji("4", CUSTOM_POWER11_EMOJIS, DEFAULT_POWER11_EMOJIS)),
    discord.SelectOption(label="5 Brawlers", value="5", emoji=get_custom_or_default_emoji("5", CUSTOM_POWER11_EMOJIS, DEFAULT_POWER11_EMOJIS)),
    discord.SelectOption(label="6 - 10 Brawlers", value="6-10", emoji=get_custom_or_default_emoji("6-10", CUSTOM_POWER11_EMOJIS, DEFAULT_POWER11_EMOJIS)),
    discord.SelectOption(label="11 - 15 Brawlers", value="11-15", emoji=get_custom_or_default_emoji("11-15", CUSTOM_POWER11_EMOJIS, DEFAULT_POWER11_EMOJIS)),
    discord.SelectOption(label="16 - 20 Brawlers", value="16-20", emoji=get_custom_or_default_emoji("16-20", CUSTOM_POWER11_EMOJIS, DEFAULT_POWER11_EMOJIS)),
    discord.SelectOption(label="20+ Brawlers", value="20+", emoji=get_custom_or_default_emoji("20+", CUSTOM_POWER11_EMOJIS, DEFAULT_POWER11_EMOJIS))
]

def calculate_price(current_rank: str, desired_rank: str, order_type: str) -> float:
    try:
        start_idx = RANKS_ORDER.index(current_rank)
        end_idx = RANKS_ORDER.index(desired_rank)
        if start_idx >= end_idx:
            return 0.0
        base_total = sum(RANK_PRICES[RANKS_ORDER[i]] for i in range(start_idx + 1, end_idx + 1))
        multiplier = 2.0 if order_type == "Carry" else 1.0
        return round(base_total * multiplier, 2)
    except Exception:
        return 0.0

def is_staff_or_admin(user: discord.Member) -> bool:
    has_staff_role = any(role.id == STAFF_ROLE_ID for role in user.roles)
    return has_staff_role or user.guild_permissions.administrator

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Confirmation View for Closing
class ConfirmCloseView(View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="Yes, Close", style=ButtonStyle.danger, emoji="✅", custom_id="confirm_close_btn")
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if not is_staff_or_admin(interaction.user):
            await interaction.response.send_message("❌ Only Staff members can confirm closing this ticket!", ephemeral=True)
            return
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

# Modal for Renaming Ticket
class RenameTicketModal(Modal):
    def __init__(self):
        super().__init__(title="Rename Ticket")
        self.new_name = TextInput(
            label="New Channel Name",
            style=TextStyle.short,
            placeholder="e.g. order-john-done",
            required=True,
            max_length=100
        )
        self.add_item(self.new_name)

    async def on_submit(self, interaction: discord.Interaction):
        new_channel_name = self.new_name.value.strip().lower().replace(" ", "-")
        await interaction.channel.edit(name=new_channel_name)
        await interaction.response.send_message(f"✏️ Channel renamed to `{new_channel_name}`", ephemeral=False)

# Ticket Controls View
class TicketControlsView(View):
    def __init__(self, payment_method: str = "Bank Transfer Portal / RIB", payment_enabled: bool = False):
        super().__init__(timeout=None)
        self.payment_method = payment_method

        self.close_btn = Button(label="Close", style=ButtonStyle.danger, emoji="🔒", custom_id="ticket_close_btn")
        self.close_btn.callback = self.close_callback

        self.close_reason_btn = Button(label="Close With Reason", style=ButtonStyle.secondary, emoji="📝", custom_id="ticket_close_reason_btn")
        self.close_reason_btn.callback = self.close_reason_callback

        self.rename_btn = Button(label="Rename", style=ButtonStyle.secondary, emoji="✏️", custom_id="ticket_rename_btn")
        self.rename_btn.callback = self.rename_callback

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
        self.add_item(self.rename_btn)
        self.add_item(self.sent_payment_btn)

    async def close_callback(self, interaction: discord.Interaction):
        if not is_staff_or_admin(interaction.user):
            await interaction.response.send_message("❌ Only Staff members can close this ticket!", ephemeral=True)
            return

        embed = Embed(
            title="Confirm Action",
            description="Are you sure you want to close this ticket?",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed, view=ConfirmCloseView(), ephemeral=True)

    async def close_reason_callback(self, interaction: discord.Interaction):
        if not is_staff_or_admin(interaction.user):
            await interaction.response.send_message("❌ Only Staff members can close this ticket!", ephemeral=True)
            return

        await interaction.response.send_modal(CloseReasonModal())

    async def rename_callback(self, interaction: discord.Interaction):
        if not is_staff_or_admin(interaction.user):
            await interaction.response.send_message("❌ Only Staff members can rename this ticket!", ephemeral=True)
            return

        await interaction.response.send_modal(RenameTicketModal())

    async def sent_payment_callback(self, interaction: discord.Interaction):
        default_fallback = f"💳 **Payment Details ({self.payment_method}):**\n```\nContact staff for details.\n```"
        pay_details = PAYMENT_DETAILS.get(self.payment_method, default_fallback)

        embed = Embed(
            title="Payment Instructions",
            description=f"{pay_details}\n\nPlease send a screenshot of the payment in this channel for verification!",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)

# Final Modal (Only Additional Notes)
class FinalDetailsModal(Modal):
    def __init__(self, order_type: str, current_rank: str, desired_rank: str, power_11_count: str, payment_method: str):
        super().__init__(title=f"Ranked Boost ({order_type})")
        self.order_type = order_type
        self.current_rank = current_rank
        self.desired_rank = desired_rank
        self.power_11_count = power_11_count
        self.payment_method = payment_method

        self.additional_notes = TextInput(
            label="Additional Notes (Optional)",
            style=TextStyle.paragraph,
            placeholder="Any special requests or details...",
            required=False
        )

        self.add_item(self.additional_notes)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        notes = self.additional_notes.value.strip() or "None"

        category_id = CARRY_CATEGORY_ID if self.order_type == "Carry" else BOOST_CATEGORY_ID
        category = interaction.guild.get_channel(category_id)

        if category:
            for channel in category.text_channels:
                if channel.name == f"order-{interaction.user.name}".lower():
                    await interaction.followup.send(
                        content=f"❌ You already have an open ticket: {channel.mention}. Close it first!",
                        ephemeral=True
                    )
                    return

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
        details_embed.add_field(name="Payment Method 💳", value=f"└ `{self.payment_method}`", inline=False)
        details_embed.add_field(name="Notes 📝", value=f"└ `{notes}`", inline=False)
        details_embed.set_footer(text=f"Powered by Iceyz BrawlMart™ • {interaction.user.id}")

        view = TicketControlsView(payment_method=self.payment_method, payment_enabled=False)

        msg = await ticket_channel.send(content=f"{interaction.user.mention}", embeds=[header_embed, details_embed], view=view)

        bot.ticket_data[ticket_channel.id] = {
            "payment_method": self.payment_method,
            "message_id": msg.id
        }

        await interaction.followup.send(f"Ticket created successfully! {ticket_channel.mention}", ephemeral=True)


class OpenModalView(View):
    def __init__(self, order_type, current_rank, desired_rank, power_11_count, payment_method):
        super().__init__(timeout=180)
        self.order_type = order_type
        self.current_rank = current_rank
        self.desired_rank = desired_rank
        self.power_11_count = power_11_count
        self.payment_method = payment_method

    @discord.ui.button(label="Click to Complete Order", style=ButtonStyle.success, emoji="📝")
    async def open_modal_btn(self, interaction: discord.Interaction, button: Button):
        modal = FinalDetailsModal(
            order_type=self.order_type,
            current_rank=self.current_rank,
            desired_rank=self.desired_rank,
            power_11_count=self.power_11_count,
            payment_method=self.payment_method
        )
        await interaction.response.send_modal(modal)

class OrderSelectionView(View):
    def __init__(self, order_type: str):
        super().__init__(timeout=300)
        self.order_type = order_type
        self.selected_current_rank = None
        self.selected_desired_rank = None
        self.selected_power_11 = None
        self.selected_payment_method = None

        rank_options_1 = [
            discord.SelectOption(
                label=r, 
                emoji=get_custom_or_default_emoji(r, CUSTOM_RANK_EMOJIS, DEFAULT_RANK_EMOJIS)
            ) for r in RANKS_ORDER
        ]
        self.current_select = Select(placeholder="Select your current rank...", options=rank_options_1[:25], custom_id="sel_curr_rank")
        self.current_select.callback = self.current_rank_callback
        self.add_item(self.current_select)

    async def current_rank_callback(self, interaction: discord.Interaction):
        self.selected_current_rank = self.current_select.values[0]
        
        self.clear_items()
        
        start_idx = RANKS_ORDER.index(self.selected_current_rank)
        available_desired_ranks = RANKS_ORDER[start_idx + 1:]

        if not available_desired_ranks:
            await interaction.response.send_message("❌ You are already at the highest rank!", ephemeral=True)
            return

        rank_options_2 = [
            discord.SelectOption(
                label=r, 
                emoji=get_custom_or_default_emoji(r, CUSTOM_RANK_EMOJIS, DEFAULT_RANK_EMOJIS)
            ) for r in available_desired_ranks
        ]
        desired_select = Select(
            placeholder=f"Current: {self.selected_current_rank} ➔ Select desired rank...", 
            options=rank_options_2[:25], 
            custom_id="sel_des_rank"
        )
        desired_select.callback = self.desired_rank_callback
        self.add_item(desired_select)
        
        await interaction.response.edit_message(content=f"✅ Current Rank: **{self.selected_current_rank}**\nNow pick your desired rank:", view=self)

    async def desired_rank_callback(self, interaction: discord.Interaction):
        self.selected_desired_rank = interaction.data["values"][0]

        self.clear_items()
        power11_select = Select(placeholder="Select number of Power 11 Brawlers...", options=POWER_11_OPTIONS, custom_id="sel_power_11")
        power11_select.callback = self.power_11_callback
        self.add_item(power11_select)

        await interaction.response.edit_message(
            content=f"✅ Current: **{self.selected_current_rank}** ➔ Desired: **{self.selected_desired_rank}**\nNow select how many **Power 11 Brawlers** you have:",
            view=self
        )

    async def power_11_callback(self, interaction: discord.Interaction):
        self.selected_power_11 = interaction.data["values"][0]

        self.clear_items()
        payment_select = Select(placeholder="Select your payment method...", options=PAYMENT_OPTIONS[:25], custom_id="sel_pay_method")
        payment_select.callback = self.payment_method_callback
        self.add_item(payment_select)

        await interaction.response.edit_message(
            content=f"✅ Current: **{self.selected_current_rank}** ➔ Desired: **{self.selected_desired_rank}** ➔ Power 11: **{self.selected_power_11}**\nNow choose payment method:",
            view=self
        )

    async def payment_method_callback(self, interaction: discord.Interaction):
        self.selected_payment_method = interaction.data["values"][0]

        view = OpenModalView(
            order_type=self.order_type,
            current_rank=self.selected_current_rank,
            desired_rank=self.selected_desired_rank,
            power_11_count=self.selected_power_11,
            payment_method=self.selected_payment_method
        )
        await interaction.response.edit_message(
            content=f"✅ Setup Completed!\n**Current**: `{self.selected_current_rank}` | **Desired**: `{self.selected_desired_rank}`\n**Power 11**: `{self.selected_power_11}` | **Payment**: `{self.selected_payment_method}`\n\n👇 Click button below to finalize ticket:",
            view=view
        )

class ServiceTypeView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=ButtonStyle.success, emoji="🚀", custom_id="srv_boosted_btn")
    async def boosted_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Please select your order parameters:", view=OrderSelectionView("Boost"), ephemeral=True)

    @discord.ui.button(label="Get Carried (2x Price)", style=ButtonStyle.blurple, emoji="🤝", custom_id="srv_carried_btn")
    async def carried_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Please select your order parameters:", view=OrderSelectionView("Carry"), ephemeral=True)

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

@bot.tree.command(name="setup_panel", description="Setup Ranked Boost Panel")
@app_commands.default_permissions(administrator=True)
async def setup_panel(interaction: discord.Interaction):
    embed1 = Embed(
        title="Ranked B00st Service",
        description="**What We Offer**\n• Climb the ranks with professional boosting service\n• Fast, secure, and reliable rank progression\n• Experienced boosters with proven track records",
        color=0x8A2BE2
    )
    embed1.set_image(url=IMAGE_PRICES_1)

    embed2 = Embed(color=0x8A2BE2)
    embed2.set_image(url=IMAGE_PRICES_2)

    await interaction.channel.send(embeds=[embed1, embed2], view=MainTicketView())
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
            if not is_staff_or_admin(message.author):
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

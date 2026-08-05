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
    "Venmo": "🔹 **Venmo Details:**\n```\nVenmo ID: @Omarjr\n```",
    "Cash App": "💵 **Cash App Details:**\n```\nCash Tag: $Omarjr\n```",
    "Wise": "🌐 **Wise Details:**\n```\nWise Email: Omarjr@wise.com\n```",
    "Apple Pay": "🍎 **Apple Pay Details:**\n```\nPhone / Email: Omarjr\n```",
    "Zelle": "⚡ **Zelle Details:**\n```\nZelle Email/Phone: Omarjr\n```",
    "Binance": "🟡 **Binance Details:**\n```\nBinance Pay ID: 123456789\n```",
    "Revolut": "💳 **Revolut Details:**\n```\nRevolut Tag: @Omarjr\n```",
    "Chime": "🟢 **Chime Details:**\n```\nChime Sign: $Omarjr\n```",
    "Skrill": "🟣 **Skrill Details:**\n```\nSkrill Email: Omarjr\n```",
    "Bitcoin": "🪙 **Bitcoin Wallet:**\n```\nBTC Address Here\n```",
    "Litecoin": "🪙 **Litecoin Wallet:**\n```\nLTC Address Here\n```",
    "Ethereum": "🪙 **Ethereum Wallet:**\n```\nETH Address Here\n```",
    "Solana": "🪙 **Solana Wallet:**\n```\nSOL Address Here\n```",
    "Tether (USDT)": "🪙 **Tether (USDT TRC20) Wallet:**\n```\nUSDT Address Here\n```"
}

IMAGE_PRICES_1 = "https://cdn.discordapp.com/attachments/1254112291096363150/1534346676989464587/image.png"
IMAGE_PRICES_2 = "https://cdn.discordapp.com/attachments/1254112291096363150/1534347605138739250/image.png"

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

# Payment options
PAYMENT_OPTIONS = [
    discord.SelectOption(label="PayPal", emoji="🅿️"),
    discord.SelectOption(label="Bank Transfer Portal / RIB", emoji="🏦"),
    discord.SelectOption(label="Venmo", emoji="🔹"),
    discord.SelectOption(label="Cash App", emoji="💵"),
    discord.SelectOption(label="Wise", emoji="🌐"),
    discord.SelectOption(label="Apple Pay", emoji="🍎"),
    discord.SelectOption(label="Zelle", emoji="⚡"),
    discord.SelectOption(label="Binance", emoji="🟡"),
    discord.SelectOption(label="Revolut", emoji="💳"),
    discord.SelectOption(label="Chime", emoji="🟢"),
    discord.SelectOption(label="Skrill", emoji="🟣"),
    discord.SelectOption(label="Bitcoin", emoji="🪙"),
    discord.SelectOption(label="Litecoin", emoji="🪙"),
    discord.SelectOption(label="Ethereum", emoji="🪙"),
    discord.SelectOption(label="Solana", emoji="🪙"),
    discord.SelectOption(label="Tether (USDT)", emoji="🪙")
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
    def __init__(self, payment_method: str = "Bank Transfer Portal / RIB", payment_enabled: bool = False):
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
        pay_details = PAYMENT_DETAILS.get(
            self.payment_method, 
            f"💳 **Payment Details ({self.payment_method}):**\n```\nContact staff for details.\n

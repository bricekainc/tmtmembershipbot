from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from config import BOT_TOKEN, ADMIN_TELEGRAM_ID
from db_manager import check_admin_status
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Command Handlers ---

def start(update: Update, context: CallbackContext):
    """Handles the /start command (Initiates the platform onboarding flow)."""
    user_id = update.effective_user.id
    # NOTE: This is where you would check if the user has paid the master fee.
    
    if user_id == ADMIN_TELEGRAM_ID:
        # Acknowledge the admin, but guide them to the proper command
        update.message.reply_text("Welcome! Send /kariuki for the Admin Panel.")
    
    # Placeholder for regular user flow
    update.message.reply_text(
        "👋 Welcome to TMTmembershipBot! The Master Subscription Platform.\n\n"
        "To start monetizing your channel, you need to first pay the platform usage fee."
        "\n\n(Implement: Master fee check and payment link here)"
    )

def kariuki_command(update: Update, context: CallbackContext):
    """Handles the /kariuki admin login command."""
    user_id = update.effective_user.id

    if user_id != ADMIN_TELEGRAM_ID:
        update.message.reply_text("🚫 Access Denied. Only the Master Admin can use this command.")
        return

    # Secondary check against the database for robustness
    if not check_admin_status(user_id):
        # This case is for the specified admin ID not being set up in the DB yet
        update.message.reply_text("❌ Admin ID is authorized but not configured in the master_admin table.")
        return

    # --- Admin Menu ---
    admin_menu = (
        "👑 **TMTmembershipBot Admin Panel**\n\n"
        "Select an action:\n"
        "1. /setup_master_payments - Configure platform's M-Pesa/Paystack/PayPal.\n"
        "2. /view_platform_stats - See total revenue and connected bots.\n"
        "3. /manage_bot_users - List and manage users of the master bot."
    )
    update.message.reply_text(admin_menu, parse_mode='Markdown')

# --- Main Bot Initialization ---

def main():
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is missing in the environment variables.")
        return

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("kariuki", kariuki_command))
    
    # TODO: Add handlers for the subsequent steps:
    # - setup_master_payments
    # - connect_bot_token (takes the user's bot key)
    # - setup_channel_id
    # - setup_plan
    # - setup_gateway_credentials

    # Start the Bot using long polling (simplest for deployment on Render/Koyeb)
    logger.info("TMTmembershipBot is starting using polling...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

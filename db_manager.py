import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    """Establishes and returns a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def check_admin_status(telegram_id):
    """Checks if a user is the authorized master admin."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        # Ensure your master_admin table is set up with:
        # CREATE TABLE master_admin (telegram_id BIGINT PRIMARY KEY);
        query = "SELECT COUNT(*) FROM master_admin WHERE telegram_id = %s"
        cursor.execute(query, (telegram_id,))
        is_admin = cursor.fetchone()[0] > 0
        cursor.close()
        return is_admin
    except mysql.connector.Error as err:
        print(f"Error checking admin status: {err}")
        return False
    finally:
        if conn and conn.is_connected():
            conn.close()

# --- Example function to save connected bot data ---
def save_connected_bot(owner_id, bot_token_encrypted, bot_username):
    """Saves a new connected bot's data (token must be encrypted)."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO connected_bots (owner_telegram_id, bot_api_key, bot_username, master_fee_paid, status)
        VALUES (%s, %s, %s, TRUE, 'active')
        """
        cursor.execute(query, (owner_id, bot_token_encrypted, bot_username))
        conn.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        # Handle duplicate entry error if bot is already connected
        if err.errno == 1062: # MySQL error code for Duplicate entry
             print("Bot already connected.")
        else:
             print(f"Error saving connected bot: {err}")
        return False
    finally:
        if conn and conn.is_connected():
            conn.close()

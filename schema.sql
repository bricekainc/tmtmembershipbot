-- TMTmembershipBot Database Schema (MySQL)
-- All tables are designed to support a multi-tenant structure where connected_bots is the core tenant.

-- =================================================================
-- 1. MASTER ADMINISTRATION TABLES
-- =================================================================

-- Stores the Telegram ID of the single Master Admin who controls the platform.
CREATE TABLE master_admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    setup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stores global platform settings like currency conversion rates or master fee amounts.
CREATE TABLE platform_settings (
    setting_key VARCHAR(50) PRIMARY KEY,
    setting_value TEXT
);

-- =================================================================
-- 2. TENANT (CONNECTED BOT) TABLES
-- =================================================================

-- Stores data for each channel owner's bot connected to the platform.
CREATE TABLE connected_bots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_telegram_id BIGINT NOT NULL,
    bot_api_key TEXT NOT NULL COMMENT 'Encrypted bot token (for security)',
    bot_username VARCHAR(100) NOT NULL UNIQUE,
    master_fee_paid BOOLEAN DEFAULT FALSE COMMENT 'Tracks payment of the platform fee',
    status ENUM('active', 'inactive', 'banned') DEFAULT 'inactive',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stores the premium channels managed by a specific bot.
CREATE TABLE channels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bot_id INT NOT NULL,
    channel_id BIGINT NOT NULL COMMENT 'Telegram channel ID (e.g., -100... format)',
    channel_title VARCHAR(255),
    invite_link VARCHAR(255) COMMENT 'Base invite link managed by bot',
    FOREIGN KEY (bot_id) REFERENCES connected_bots(id) ON DELETE CASCADE,
    UNIQUE KEY bot_channel_unique (bot_id, channel_id)
);

-- Stores the subscription plans offered by a specific bot.
CREATE TABLE plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bot_id INT NOT NULL,
    plan_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    currency ENUM('KES', 'USD') NOT NULL,
    duration_days INT NOT NULL COMMENT 'Duration of the plan in days (e.g., 30, 90, 365)',
    channel_id INT NOT NULL COMMENT 'Which channel this plan grants access to',
    FOREIGN KEY (bot_id) REFERENCES connected_bots(id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE
);

-- =================================================================
-- 3. PAYMENT & SUBSCRIPTION TABLES
-- =================================================================

-- Stores the encrypted API credentials for each payment gateway configured by the channel owner.
CREATE TABLE payment_configs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bot_id INT NOT NULL,
    gateway ENUM('MPESA', 'PAYSTACK', 'PAYPAL') NOT NULL,
    config_data TEXT NOT NULL COMMENT 'Encrypted JSON blob of sensitive credentials',
    is_active BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (bot_id) REFERENCES connected_bots(id) ON DELETE CASCADE,
    UNIQUE KEY bot_gateway_unique (bot_id, gateway)
);

-- Stores records of individual user subscriptions.
CREATE TABLE subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bot_id INT NOT NULL,
    user_telegram_id BIGINT NOT NULL,
    plan_id INT NOT NULL,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,
    transaction_id VARCHAR(255) UNIQUE COMMENT 'Unique identifier from M-Pesa, Paystack, or PayPal',
    amount_paid DECIMAL(10, 2) NOT NULL,
    currency_paid ENUM('KES', 'USD') NOT NULL,
    status ENUM('active', 'expired', 'pending', 'cancelled') DEFAULT 'pending',
    FOREIGN KEY (bot_id) REFERENCES connected_bots(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES plans(id) ON DELETE RESTRICT
);

-- ============================================================
-- TASK 28 - EDABIP MINI ENTERPRISE ANALYTICS DASHBOARD
-- DATABASE SCHEMA
-- ============================================================

DROP DATABASE IF EXISTS edabip_dashboard;

CREATE DATABASE edabip_dashboard
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE edabip_dashboard;


-- ============================================================
-- USERS TABLE
-- ============================================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    password_hash VARCHAR(255) NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_users_email (email),

    INDEX idx_users_active (is_active)
);


-- ============================================================
-- TRANSACTIONS TABLE
-- ============================================================

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    order_number VARCHAR(50) NOT NULL UNIQUE,

    category VARCHAR(100) NOT NULL,

    amount DECIMAL(12,2) NOT NULL,

    status ENUM(
        'Completed',
        'Pending',
        'Cancelled'
    ) NOT NULL DEFAULT 'Completed',

    transaction_date DATE NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_transactions_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    INDEX idx_transactions_user_id (user_id),

    INDEX idx_transactions_category (category),

    INDEX idx_transactions_status (status),

    INDEX idx_transactions_date (transaction_date)
);


-- ============================================================
-- VERIFY TABLES
-- ============================================================

SHOW TABLES;

DESCRIBE users;

DESCRIBE transactions;
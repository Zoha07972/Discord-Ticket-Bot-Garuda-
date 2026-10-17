CREATE TABLE IF NOT EXISTS ticket_counter (
    guild_id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    last_ticket_number BIGINT UNSIGNED NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS tickets (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    guild_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    channel_id BIGINT UNSIGNED NOT NULL UNIQUE,
    ticket_number BIGINT UNSIGNED NOT NULL,
    category VARCHAR(32) NOT NULL,
    status ENUM('open', 'closed') NOT NULL DEFAULT 'open',
    claimed_by BIGINT UNSIGNED NULL,
    close_reason TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY idx_tickets_guild_user_status (guild_id, user_id, status),
    KEY idx_tickets_guild_number (guild_id, ticket_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

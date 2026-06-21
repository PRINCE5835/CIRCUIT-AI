-- BreadBoard AI - Database Schema (MySQL 8)
-- Engine: InnoDB, Charset: utf8mb4, Collation: utf8mb4_unicode_ci

CREATE DATABASE IF NOT EXISTS breadboard
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE breadboard;

-- ── Users ────────────────────────────────────────────────────
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    avatar_url VARCHAR(500),
    preferred_language VARCHAR(10) DEFAULT 'en',
    is_active TINYINT(1) DEFAULT 1,
    is_verified TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Projects ─────────────────────────────────────────────────
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    circuit_data JSON,
    breadboard_image_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'draft',
    is_public TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_projects_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Circuits ─────────────────────────────────────────────────
CREATE TABLE circuits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    netlist TEXT,
    schematic_data JSON,
    components_json JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_circuits_project_id (project_id),
    INDEX idx_circuits_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Components ───────────────────────────────────────────────
CREATE TABLE components (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    manufacturer VARCHAR(255),
    model_number VARCHAR(255),
    specifications_json JSON,
    datasheet_url VARCHAR(500),
    image_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Marketplace ──────────────────────────────────────────────
CREATE TABLE marketplace_listings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seller_id INT NOT NULL,
    component_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    quantity INT DEFAULT 1,
    `condition` VARCHAR(50) DEFAULT 'new',
    location VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE,
    INDEX idx_marketplace_status (status),
    INDEX idx_marketplace_seller (seller_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Voice Sessions ───────────────────────────────────────────
CREATE TABLE voice_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_type VARCHAR(50) NOT NULL,
    audio_url VARCHAR(500),
    transcript TEXT,
    language VARCHAR(10) DEFAULT 'en',
    duration_ms INT,
    processed_json JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_voice_sessions_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Cost Estimates ──────────────────────────────────────────
CREATE TABLE cost_estimates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    total_cost DECIMAL(12,2),
    currency VARCHAR(10) DEFAULT 'USD',
    breakdown_json JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_cost_estimates_project (project_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ── Safety Reports ──────────────────────────────────────────
CREATE TABLE safety_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    circuit_id INT NOT NULL,
    user_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    issues_json JSON,
    severity VARCHAR(20),
    recommendations TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (circuit_id) REFERENCES circuits(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_safety_reports_circuit (circuit_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ═══════════════════════════════════════════════════════════════
-- CONTENT SOURCING SYSTEM
-- ═══════════════════════════════════════════════════════════════

-- Priority sources for content attribution (Wikipedia, SparkFun, Adafruit, etc.)
CREATE TABLE sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL COMMENT 'Display name of the source',
    url VARCHAR(1000) NOT NULL COMMENT 'Full URL to the source page or API',
    source_type ENUM(
        'wikipedia',
        'electronics_tutorials',
        'arduino_docs',
        'raspberry_pi_docs',
        'sparkfun',
        'adafruit',
        'open_source_circuit',
        'wikipedia_commons',
        'wikimedia_commons',
        'datasheet',
        'academic',
        'other'
    ) NOT NULL COMMENT 'Classification of the source',
    priority TINYINT UNSIGNED DEFAULT 5 COMMENT '1=highest priority, 10=lowest',
    license VARCHAR(255) DEFAULT NULL COMMENT 'Creative Commons, MIT, etc.',
    author VARCHAR(255) DEFAULT NULL,
    description TEXT DEFAULT NULL COMMENT 'Brief description of the source content',
    language VARCHAR(10) DEFAULT 'en',
    is_active TINYINT(1) DEFAULT 1,
    last_validated_at DATETIME DEFAULT NULL COMMENT 'Last time URL was verified working',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_source_url (url(255)),
    INDEX idx_source_type (source_type),
    INDEX idx_source_priority (priority),
    INDEX idx_source_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Junction: which sources were used for a given piece of generated content
CREATE TABLE content_sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_id INT NOT NULL,
    content_type ENUM(
        'circuit',
        'component',
        'lesson',
        'repair_guide',
        'safety_check',
        'cost_estimate',
        'breadboard_layout',
        'tutorial',
        'explanation',
        'image',
        'datasheet',
        'code_example',
        'schematic'
    ) NOT NULL COMMENT 'Type of content this source was used for',
    content_id INT NOT NULL COMMENT 'ID of the content record (polymorphic)',
    usage_context VARCHAR(255) DEFAULT NULL COMMENT 'How the source was used (e.g. "component spec", "wiring diagram")',
    attribution_text TEXT DEFAULT NULL COMMENT 'Human-readable attribution string',
    image_url VARCHAR(1000) DEFAULT NULL COMMENT 'Specific image URL used from this source',
    relevance_score DECIMAL(3,2) DEFAULT NULL COMMENT 'How relevant the source was (0.00 - 1.00)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE,
    INDEX idx_content_type_id (content_type, content_id),
    INDEX idx_content_source (source_id, content_type),
    UNIQUE KEY uk_content_source (source_id, content_type, content_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- BreadBoard AI - Database Schema (PostgreSQL 15+)
-- For Render.com or any PostgreSQL deployment

CREATE DATABASE breadboard;

-- ── Users ────────────────────────────────────────────────────
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    avatar_url VARCHAR(500),
    preferred_language VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Projects ─────────────────────────────────────────────────
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    circuit_data JSONB,
    breadboard_image_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'draft',
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_projects_user_id ON projects(user_id);

-- ── Circuits ─────────────────────────────────────────────────
CREATE TABLE circuits (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    netlist TEXT,
    schematic_data JSONB,
    components_json JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_circuits_project_id ON circuits(project_id);
CREATE INDEX idx_circuits_user_id ON circuits(user_id);

-- ── Components ───────────────────────────────────────────────
CREATE TABLE components (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    manufacturer VARCHAR(255),
    model_number VARCHAR(255),
    specifications_json JSONB,
    datasheet_url VARCHAR(500),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Marketplace ──────────────────────────────────────────────
CREATE TABLE marketplace_listings (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    component_id INTEGER NOT NULL REFERENCES components(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    quantity INTEGER DEFAULT 1,
    condition VARCHAR(50) DEFAULT 'new',
    location VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_marketplace_status ON marketplace_listings(status);
CREATE INDEX idx_marketplace_seller ON marketplace_listings(seller_id);

-- ── Voice Sessions ───────────────────────────────────────────
CREATE TABLE voice_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_type VARCHAR(50) NOT NULL,
    audio_url VARCHAR(500),
    transcript TEXT,
    language VARCHAR(10) DEFAULT 'en',
    duration_ms INTEGER,
    processed_json JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_voice_sessions_user_id ON voice_sessions(user_id);

-- ── Cost Estimates ──────────────────────────────────────────
CREATE TABLE cost_estimates (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total_cost DECIMAL(12,2),
    currency VARCHAR(10) DEFAULT 'USD',
    breakdown_json JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_cost_estimates_project ON cost_estimates(project_id);

-- ── Safety Reports ──────────────────────────────────────────
CREATE TABLE safety_reports (
    id SERIAL PRIMARY KEY,
    circuit_id INTEGER NOT NULL REFERENCES circuits(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending',
    issues_json JSONB,
    severity VARCHAR(20),
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_safety_reports_circuit ON safety_reports(circuit_id);

-- ── Conversations ───────────────────────────────────────────
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) DEFAULT 'New Chat',
    messages JSONB NOT NULL,
    model VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- ── Content Sources ─────────────────────────────────────────
CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL UNIQUE,
    source_type VARCHAR(50) NOT NULL,
    priority INTEGER DEFAULT 5,
    license VARCHAR(255),
    author VARCHAR(255),
    description TEXT,
    language VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    last_validated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_source_type ON sources(source_type);
CREATE INDEX idx_source_priority ON sources(priority);
CREATE INDEX idx_source_active ON sources(is_active);

-- ── Content Sources Junction ─────────────────────────────────
CREATE TABLE content_sources (
    id SERIAL PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    content_type VARCHAR(50) NOT NULL,
    content_id INTEGER NOT NULL,
    usage_context VARCHAR(255),
    attribution_text TEXT,
    image_url VARCHAR(255),
    relevance_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_id, content_type, content_id)
);
CREATE INDEX idx_content_type_id ON content_sources(content_type, content_id);
CREATE INDEX idx_content_source ON content_sources(source_id, content_type);

-- ── Project Components (BOM) ─────────────────────────────────
CREATE TABLE project_components (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    component_id INTEGER NOT NULL REFERENCES components(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1,
    notes VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_project_components_project_id ON project_components(project_id);
CREATE INDEX idx_project_components_component_id ON project_components(component_id);

-- ── Auto-update trigger for updated_at ──────────────────────
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE
    tbl TEXT;
BEGIN
    FOR tbl IN
        SELECT unnest(ARRAY['users', 'projects', 'circuits', 'components',
                           'marketplace_listings', 'voice_sessions',
                           'cost_estimates', 'safety_reports',
                           'conversations', 'sources', 'project_components'])
    LOOP
        EXECUTE format(
            'CREATE TRIGGER trg_%s_updated_at
             BEFORE UPDATE ON %I
             FOR EACH ROW
             WHEN (OLD.* IS DISTINCT FROM NEW.*)
             EXECUTE FUNCTION update_updated_at()',
            tbl, tbl
        );
    END LOOP;
END;
$$;

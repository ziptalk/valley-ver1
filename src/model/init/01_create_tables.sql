CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT 
        PRIMARY KEY,
    username TEXT,
    language TEXT 
        DEFAULT 'ko' 
        CHECK (language IN ('ko', 'en')),
    created_at TIMESTAMP 
        DEFAULT now()
);

CREATE TABLE IF NOT EXISTS groups (
    group_id BIGINT 
        PRIMARY KEY,
    group_name TEXT,
    language TEXT 
        DEFAULT 'ko' 
        CHECK (language IN ('ko', 'en')),
    created_at TIMESTAMP 
        DEFAULT now()
);

CREATE TABLE IF NOT EXISTS points (
    id BIGINT 
        GENERATED ALWAYS AS IDENTITY 
        PRIMARY KEY,
    owner_type TEXT 
        CHECK (owner_type IN ('user', 'group')),
    owner_id BIGINT,
    point INT 
        DEFAULT 0,
    updated_at TIMESTAMP 
        DEFAULT now(),
    UNIQUE(owner_type, owner_id)
);

CREATE TABLE IF NOT EXISTS ads (
    id BIGINT 
        GENERATED ALWAYS AS IDENTITY 
        PRIMARY KEY,
    content TEXT 
        NOT NULL,
    created_at TIMESTAMP 
        DEFAULT now(),
    is_active BOOLEAN 
        DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS ad_view_logs (
    id SERIAL 
        PRIMARY KEY,
    owner_type VARCHAR(10) 
        CHECK (owner_type IN ('user', 'group')),  -- 'user' or 'group'
    owner_id BIGINT 
        NOT NULL,         -- user_id or group_id
    ad_id INTEGER 
        NOT NULL,
    viewed_at DATE 
        DEFAULT CURRENT_DATE,  -- Store only the date
    points_earned INTEGER 
        NOT NULL,
    UNIQUE(owner_type, owner_id, viewed_at)
);

ALTER TABLE ad_view_logs
ADD CONSTRAINT fk_ad_view_logs_ad
FOREIGN KEY (ad_id)
REFERENCES ads(id)
ON DELETE CASCADE;
--users sample data
INSERT INTO users (user_id, username, language)
VALUES 
('123456789', 'alice', 'en'),
('234567890', 'bob', 'ko'),
('345678901', 'charlie', 'en'),
('456789012', 'daisy', 'ko'),
('567890123', 'ethan', 'en');

--groups sample data
INSERT INTO groups (group_id, group_name, language)
VALUES
('123456789', 'dev_group', 'en'),
('987654321', 'study_kor', 'ko'),
('-1001122334455', 'global_chat', 'en'),
('-1005566778899', 'kpop_lovers', 'ko');

--users points sample data
INSERT INTO points (owner_type, owner_id, point)
SELECT 'user', user_id, point
FROM (VALUES
    ('alice', 150),
    ('bob', 200),
    ('charlie', 300)
) AS t(username, point)
JOIN users u ON u.username = t.username;

--groups points sample data
INSERT INTO points (owner_type, owner_id, point)
SELECT 'group', group_id, point
FROM (VALUES
    ('dev_group', 1000),
    ('study_kor', 800)
) AS t(group_name, point)
JOIN groups g ON g.group_name = t.group_name;

--ads sample data
INSERT INTO ads (content, is_active)
VALUES 
('🔥 Get your free credits now! Click here!', TRUE),
('🚀 Upgrade to premium and unlock features!', FALSE),
('📢 New version released – check it out!', TRUE),
('🎁 Invite friends and earn rewards!', FALSE),
('💬 Join our global Telegram bot challenge!', TRUE);
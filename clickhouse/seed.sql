-- Scene 12 Test Data

INSERT INTO cinepilot.scenes VALUES
('SC12', 'movie_001', 'Office Arrival', 'Modern Office', 'Morning', ['Daniel', 'Sarah'], ['Coffee cup', 'Blue jacket', 'Laptop', 'Phone'], now());

INSERT INTO cinepilot.takes VALUES
('SC12_T001', 'SC12', 'movie_001', 1, 'video/scene_12/take_01.mp4', now()),
('SC12_T002', 'SC12', 'movie_001', 2, 'video/scene_12/take_02.mp4', now());

INSERT INTO cinepilot.continuity_issues VALUES
('SC12_ISSUE_001', 'SC12', 'SC12_T002', 'movie_001', 'costume', 'Black jacket instead of blue', 'critical', 0.96, now()),
('SC12_ISSUE_002', 'SC12', 'SC12_T002', 'movie_001', 'prop', 'Coffee cup missing', 'high', 0.91, now());

INSERT INTO cinepilot.production_decisions VALUES
('SC12_DECISION_001', 'SC12', 'movie_001', 'SC12_T001', 'Take 1 has correct costume and props', now(), now());
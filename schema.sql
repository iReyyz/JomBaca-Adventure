-- 1. Jadual users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    level INT DEFAULT 1,
    xp INT DEFAULT 0,
    coins INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Jadual tasks
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    type VARCHAR(50) NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'easy'
);

-- 3. Jadual user_tasks
CREATE TABLE IF NOT EXISTS user_tasks (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    task_id INT REFERENCES tasks(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending',
    score INT DEFAULT 0,
    completed_at TIMESTAMP
);

-- 4. Jadual scores
CREATE TABLE IF NOT EXISTS scores (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    points INT NOT NULL DEFAULT 0,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Jadual battles
CREATE TABLE IF NOT EXISTS battles (
    id SERIAL PRIMARY KEY,
    player1_id INT REFERENCES users(id) ON DELETE CASCADE,
    player2_id INT REFERENCES users(id) ON DELETE CASCADE,
    winner_id INT REFERENCES users(id) ON DELETE SET NULL,
    score_player1 INT DEFAULT 0,
    score_player2 INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

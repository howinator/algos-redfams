CREATE TABLE IF NOT EXISTS users (
  id SERIAL,
  username VARCHAR(100) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS subreddits (
  id SERIAL,
  name VARCHAR(100) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS comments (
  id BIGSERIAL,
  username VARCHAR(100) REFERENCES users (username),
  subreddit VARCHAR(100) REFERENCES subreddits (name),

  PRIMARY KEY (username, subreddit)
);

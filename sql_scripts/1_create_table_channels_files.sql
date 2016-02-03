CREATE SEQUENCE channel_auto_id;
CREATE SEQUENCE files_auto_id;
CREATE TABLE IF NOT EXISTS files(id BIGINT PRIMARY KEY DEFAULT nextval('files_auto_id'), file_link VARCHAR(500));

CREATE TABLE IF NOT EXISTS channels(id BIGINT PRIMARY KEY DEFAULT nextval('channel_auto_id'), name VARCHAR(200) NOT NULL ,
link VARCHAR(500) NOT NULL, icon_id INTEGER REFERENCES files(id), channel_language VARCHAR(2) DEFAULT 'ua');

CREATE SEQUENCE tv_programs_auto_id;
CREATE TABLE tv_programs(id INTEGER PRIMARY KEY DEFAULT nextval('tv_programs_auto_id'),
name VARCHAR(200), genre VARCHAR(50), show_date DATE, show_time TIME, channel_id INTEGER REFERENCES channels(id))

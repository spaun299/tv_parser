CREATE SEQUENCE tv_programs_auto_id;
CREATE TABLE tv_programs(id INTEGER PRIMARY KEY DEFAULT nextval('tv_programs_auto_id'),
name VARCHAR(200), genre VARCHAR(50), show_date DATE, show_time TIME, channel_id INTEGER REFERENCES channels(id),
cr_tm TIMESTAMP WITHOUT TIME ZONE);
CREATE TRIGGER cr_tm_program BEFORE INSERT ON tv_programs FOR EACH ROW EXECUTE PROCEDURE time_before_insert_column();

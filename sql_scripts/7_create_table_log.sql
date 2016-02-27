CREATE SEQUENCE log_auto_id;
CREATE TABLE log(id INTEGER NOT NULL DEFAULT nextval('log_auto_id'), parser_name VARCHAR(20),
  count_new_items INTEGER, cr_tm TIMESTAMP WITHOUT TIME ZONE, success BOOLEAN DEFAULT TRUE,
  total_channels INTEGER , total_programs INTEGER);
CREATE TRIGGER cr_tm_trigger BEFORE INSERT ON log FOR EACH ROW EXECUTE PROCEDURE time_before_insert_column();
CREATE TRIGGER count_channels_programs BEFORE INSERT ON log FOR EACH ROW EXECUTE PROCEDURE count_channels_programs();

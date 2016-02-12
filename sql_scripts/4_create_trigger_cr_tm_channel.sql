CREATE TRIGGER cr_tm_trigger BEFORE INSERT ON channels FOR EACH ROW EXECUTE PROCEDURE  time_before_insert_column();

CREATE OR REPLACE FUNCTION time_before_insert_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.cr_tm = now();
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE OR REPLACE FUNCTION count_objects_for_log(text)
  RETURNS int AS $$
    DECLARE total INT;
  BEGIN
      EXECUTE 'SELECT  INTO total COUNT(' || quote_ident($1) || ') FROM '  || quote_ident($1) || ';';
  RETURN total;
END;
$$ language 'plpgsql';

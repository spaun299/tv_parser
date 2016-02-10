CREATE OR REPLACE FUNCTION time_before_insert_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.cr_tm = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

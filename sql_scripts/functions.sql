CREATE OR REPLACE FUNCTION time_before_insert_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.cr_tm = now();
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE OR REPLACE FUNCTION count_channels_programs()
  RETURNS TRIGGER AS $$
    DECLARE total_channels INT; total_programs INT;
  BEGIN
       SELECT(SELECT COUNT(channels.id) AS c_count FROM channels),
                     COUNT(tv_programs.id) AS t_count INTO total_channels, total_programs
       FROM  tv_programs;
      NEW.total_channels = total_channels;
      NEW.total_programs = total_programs;
      RETURN NEW;
END;
$$ language 'plpgsql';
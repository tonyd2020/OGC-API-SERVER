CREATE OR REPLACE FUNCTION notify_sample_changes()
RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify(
    'sample_changed',
    json_build_object(
      'operation', TG_OP,
      'record', row_to_json(NEW)
    )::text
  );

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

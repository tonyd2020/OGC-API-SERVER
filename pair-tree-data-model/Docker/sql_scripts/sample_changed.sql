CREATE TRIGGER sample_changed
AFTER INSERT OR UPDATE
ON public.sample
FOR EACH ROW
EXECUTE PROCEDURE notify_sample_changes()

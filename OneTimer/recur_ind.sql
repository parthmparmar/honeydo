ALTER TABLE public."Tasks"
ADD recur_ind integer;

ALTER TABLE public."Tasks"
ADD recur_days integer;

ALTER TABLE public."Tasks"
ADD parent_task_id integer;

UPDATE public."Tasks"
SET recur_ind = 0;

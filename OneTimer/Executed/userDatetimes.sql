ALTER TABLE public."Users"
ADD user_created_date timestamp;

UPDATE public."Users"
SET user_created_date = last_login;

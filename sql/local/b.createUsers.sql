\c pdbrd_db
DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'pdbrd_app_rw') THEN

      RAISE NOTICE 'role "pdbrd_app_rw" already exists, skipping';
   ELSE
      BEGIN   -- nested block
         CREATE ROLE pdbrd_app_rw LOGIN PASSWORD 'password';
      EXCEPTION
         WHEN duplicate_object THEN
            RAISE NOTICE 'role "pdbrd_app_rw" was just created by a concurrent transaction, skipping';
      END;
   END IF;
END
$do$;

REVOKE ALL PRIVILEGES ON SCHEMA public FROM PUBLIC;
CREATE SCHEMA IF NOT EXISTS public;
GRANT CONNECT ON DATABASE pdbrd_db to pdbrd_app_rw;
GRANT USAGE ON SCHEMA public TO pdbrd_app_rw;
GRANT CREATE ON SCHEMA public to pdbrd_app_rw;
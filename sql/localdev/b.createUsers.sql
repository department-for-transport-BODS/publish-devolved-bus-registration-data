\c epp
DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'epp_site_ro') THEN

      RAISE NOTICE 'role "epp_site_ro" already exists, skipping';
   ELSE
      BEGIN   -- nested block
         CREATE ROLE epp_site_ro LOGIN PASSWORD 'password';
      EXCEPTION
         WHEN duplicate_object THEN
            RAISE NOTICE 'role "epp_site_ro" was just created by a concurrent transaction, skipping';
      END;
   END IF;
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'epp_site_rw') THEN

      RAISE NOTICE 'role "epp_site_rw" already exists, skipping';
   ELSE
      BEGIN   -- nested block
         CREATE ROLE epp_site_rw LOGIN PASSWORD 'password';
      EXCEPTION
         WHEN duplicate_object THEN
            RAISE NOTICE 'role "epp_site_rw" was just created by a concurrent transaction, skipping';
      END;
   END IF;
END
$do$;

REVOKE ALL PRIVILEGES ON SCHEMA public FROM PUBLIC;
CREATE SCHEMA IF NOT EXISTS public;
GRANT CONNECT ON DATABASE epp to epp_site_ro;
GRANT CONNECT ON DATABASE epp to epp_site_rw;
GRANT USAGE ON SCHEMA public TO epp_site_ro;
GRANT USAGE ON SCHEMA public TO epp_site_rw;
GRANT CREATE ON SCHEMA public to epp_site_rw;
REVOKE CREATE ON SCHEMA public FROM epp_site_ro;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO epp_site_ro;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO epp_site_ro;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO epp_site_ro;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO epp_site_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE,SELECT ON SEQUENCES TO epp_site_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT EXECUTE ON ROUTINES TO epp_site_ro;

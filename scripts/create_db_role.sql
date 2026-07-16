-- NSTP — create the least-privilege application role and its database.
--
-- Run ONCE, as the postgres superuser:
--
--   /Library/PostgreSQL/18/bin/psql -U postgres -h localhost -f scripts/create_db_role.sql
--
-- You'll be asked for the postgres superuser password (set at install), then
-- prompted to choose a NEW password for the `nstp` role. Use that same nstp
-- password in .env as DB_PASSWORD.
--
-- \prompt keeps the password out of shell history and out of this file.
--
-- WHY NOT the postgres superuser for the app?
--   A superuser can read and destroy every database on the server. The app only
--   ever needs its own. If the app is compromised, the blast radius should be
--   nstp_db and nothing else.
--
-- WHY CREATEDB, then?
--   It is the one privilege granted beyond the minimum. Django's test runner
--   (pytest-django) creates and drops a throwaway `test_nstp_db` on every run.
--   Without CREATEDB the entire test suite cannot run. It does NOT grant any
--   access to other existing databases.

\prompt 'Choose a password for the new nstp role: ' nstp_pw

-- 1. The application role. LOGIN + CREATEDB only — explicitly NOT a superuser.
CREATE ROLE nstp WITH LOGIN PASSWORD :'nstp_pw' CREATEDB NOSUPERUSER NOCREATEROLE;

-- 2. The database, owned by nstp. Created only if it does not already exist.
SELECT 'CREATE DATABASE nstp_db OWNER nstp ENCODING ''UTF8'''
 WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'nstp_db')\gexec

-- If nstp_db already existed (e.g. made earlier in pgAdmin), transfer ownership.
ALTER DATABASE nstp_db OWNER TO nstp;

-- 3. Lock down the public schema inside nstp_db so only nstp can use it.
\connect nstp_db
ALTER SCHEMA public OWNER TO nstp;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO nstp;

-- 4. Confirm.
\echo ''
\echo '--- Role privileges (rolsuper must be f) ---'
SELECT rolname, rolsuper, rolcreatedb, rolcanlogin
  FROM pg_roles WHERE rolname = 'nstp';
\echo '--- Database owner (must be nstp) ---'
SELECT datname, pg_catalog.pg_get_userbyid(datdba) AS owner
  FROM pg_database WHERE datname = 'nstp_db';
\echo ''
\echo 'Done. Now put the nstp password into .env as DB_PASSWORD.'

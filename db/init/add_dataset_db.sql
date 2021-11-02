-- get the environment variable for the database and user creation
\set db_user `echo "${DB_USER}"`
\set db_password `echo "${DB_PASSWORD}"`
\set db_db `echo "${DB_DB}"`

ALTER USER :db_user WITH UNENCRYPTED PASSWORD :'db_password';
ALTER USER :db_user WITH LOGIN;
CREATE DATABASE :db_db OWNER :'db_user';

ALTER DATABASE :db_db SET search_path = public, postgis;

\c :db_db;
CREATE EXTENSION IF NOT EXISTS postgis ;

SET TIMEZONE='Europe/Zurich';

-- Types
CREATE TYPE levl AS ENUM ('country', 'NUTS1', 'NUTS2', 'NUTS3', 'LAU', 'geometry');

-- Tables
CREATE TABLE public.datasets
(
    ds_id int PRIMARY KEY,
    metadata jsonb,
    shared_id varchar(200) UNIQUE
);

CREATE TABLE public.spatial
(
    fid varchar(200) PRIMARY KEY,
    name varchar(200),
    name_engl varchar(200),
    cntr_code char(2),
    levl_code levl DEFAULT 'geometry',
    ds_id int,
    geometry geometry(Geometry,3035)
);

CREATE TABLE public.data
(
    index SERIAL PRIMARY KEY,
    start_at timestamp without time zone,
    fields jsonb,
    variable varchar(200),
    unit varchar(200),
    value double precision,
    ds_id int,
    fid varchar(200),
    dt double precision,
    z double precision,
    isRaster boolean,
    vis_id uuid
);

CREATE TABLE public.visualization
(
    vis_id uuid PRIMARY KEY,
    legend jsonb default'{}'::jsonb,
    timestamp timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


-- Foreign keys
ALTER TABLE spatial
    ADD CONSTRAINT fk_ds_id
    FOREIGN KEY(ds_id)
    REFERENCES datasets(ds_id)
    ON DELETE CASCADE
;

ALTER TABLE data
    ADD CONSTRAINT fk_ds_id
    FOREIGN KEY(ds_id)
    REFERENCES datasets(ds_id)
    ON DELETE CASCADE
;

ALTER TABLE data
    ADD CONSTRAINT fk_vis_id
    FOREIGN KEY(vis_id)
    REFERENCES visualization(vis_id)
    ON DELETE CASCADE
;

-- Indices
CREATE INDEX on data(ds_id);
CREATE INDEX on data(israster);
CREATE INDEX on data(vis_id);
CREATE INDEX on data(start_at);
CREATE INDEX on data(vis_id);
CREATE INDEX on spatial(ds_id);
CREATE INDEX on spatial(levl_code);
CREATE INDEX ON spatial USING gist(geometry);

-- Privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO :db_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO :db_user;

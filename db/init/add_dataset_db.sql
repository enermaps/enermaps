-- get the environment variable for the database and user creation
\set db_user `echo "${DB_USER}"`
\set db_password `echo "${DB_PASSWORD}"`
\set db_db `echo "${DB_DB}"`

CREATE USER :db_user WITH UNENCRYPTED PASSWORD :'db_password';
ALTER USER :db_user WITH LOGIN;
CREATE DATABASE :db_db OWNER :'db_user';

ALTER DATABASE :db_db SET search_path = public, postgis;

\c :db_db;
CREATE EXTENSION IF NOT EXISTS postgis ;

CREATE TYPE levl AS ENUM ('country', 'NUTS1', 'NUTS2', 'NUTS3', 'LAU', 'geometry');

CREATE TABLE public.datasets
(
    ds_id int PRIMARY KEY,
    metadata jsonb
);

CREATE TABLE public.spatial
(
    fid varchar(200) PRIMARY KEY,
    name varchar(200),
    name_engl varchar(200),
    cntr_code char(2),
    levl_code levl,
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
    layer jsonb default'{"type": "numerical"}'::jsonb
);


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


GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO :db_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO :db_user;

-- POSTGREST
CREATE ROLE api_anon nologin;
GRANT usage ON schema public TO api_anon;
GRANT api_anon TO test;

CREATE ROLE api_user nologin;
GRANT api_user TO test;

GRANT USAGE ON schema public TO api_user;
GRANT SELECT ON public.spatial TO api_user;
GRANT SELECT ON public.data TO api_user;
GRANT SELECT ON public.datasets TO api_user;


CREATE FUNCTION enermaps_query(ds_id integer)
    RETURNS TABLE(fid char, json_object_agg json, fields jsonb, start_at timestamp without time zone, dt float, z float, ds_id int, geometry text)
    AS 'SELECT data.fid,
            json_object_agg(variable, value),
            fields,
            start_at, dt, z, data.ds_id, st_astext(geometry)
           FROM data
    INNER JOIN spatial ON data.fid = spatial.fid
    WHERE data.ds_id = 2
    GROUP BY data.fid, start_at, dt, z, data.ds_id, fields, geometry
    ORDER BY data.fid;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;

GRANT EXECUTE ON FUNCTION enermaps_query(ds_id integer) to api_user;
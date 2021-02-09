CREATE ROLE dataset WITH UNENCRYPTED PASSWORD 'dataset';
ALTER ROLE dataset WITH LOGIN;
CREATE DATABASE dataset OWNER 'test';
-- REVOKE ALL PRIVILEGES ON DATABASE dataset FROM public;

-- GRANT ALL PRIVILEGES ON DATABASE dataset TO dataset;

ALTER DATABASE dataset SET search_path = public, postgis;
\c dataset

CREATE EXTENSION IF NOT EXISTS postgis ;

CREATE TYPE levl AS ENUM ('country', 'NUTS1', 'NUTS2', 'NUTS3', 'LAU', 'geometry');

CREATE TABLE public.datasets
(
    ds_id int PRIMARY KEY,
    metadata jsonb
);

CREATE TABLE public.spatial
(
    "FID" varchar(200) PRIMARY KEY,
    "NAME" varchar(200),
    "NAME_ENGL" varchar(100),
    "CNTR_CODE" char(2),
    "LEVL_CODE" levl,
    geometry geometry(Geometry,3035)
);

CREATE TABLE public.data
(
    index SERIAL PRIMARY KEY,
    "time" timestamp without time zone,
    fields jsonb,
    variable varchar(100),
    value double precision,
    ds_id int,
    "FID" varchar(200),
    dt double precision,
    z double precision,
    "Raster" boolean
);

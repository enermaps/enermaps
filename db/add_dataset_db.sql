CREATE ROLE dataset WITH UNENCRYPTED PASSWORD 'dataset';
ALTER ROLE dataset WITH LOGIN;
CREATE DATABASE dataset OWNER 'dataset';
REVOKE ALL PRIVILEGES ON DATABASE dataset FROM public;

GRANT ALL PRIVILEGES ON DATABASE dataset TO dataset;

ALTER DATABASE dataset SET search_path = public, postgis;
\c dataset

CREATE EXTENSION IF NOT EXISTS postgis ;

CREATE TABLE public.datasets
(
    ds_id bigint PRIMARY KEY,
    metadata jsonb
);

CREATE TABLE public.spatial
(
    "FID" text PRIMARY KEY,
    "NAME" text,
    "NAME_ENGL" text,
    "CNTR_CODE" text,
    "LEVL_CODE" bigint,
    geometry geometry(Geometry,4326)
);

CREATE TABLE public.data
(
    index bigint PRIMARY KEY,
    "time" timestamp without time zone,
    fields jsonb,
    variable text,
    value double precision,
    ds_id bigint,
    "FID" text,
    dt double precision,
    z double precision,
    "Raster" boolean
);

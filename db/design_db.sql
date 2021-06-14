CREATE ROLE dataset WITH UNENCRYPTED PASSWORD 'dataset';
ALTER ROLE dataset WITH LOGIN;
CREATE DATABASE dataset OWNER 'test';
-- REVOKE ALL PRIVILEGES ON DATABASE dataset FROM public;

-- GRANT ALL PRIVILEGES ON DATABASE dataset TO dataset;

ALTER DATABASE dataset SET search_path = public, postgis;
\c dataset

CREATE EXTENSION IF NOT EXISTS postgis ;

CREATE TABLE public.datasets
(
    dataset_id int,
    metadata jsonb,
    name  varchar(200),
    title varchar(200),
    abstract varchar(200),
    PRIMARY KEY(dataset_id)
);

CREATE TABLE public.layer
(
    layer_id int,
    dataset_id int,
    metadata jsonb,
    name varchar(200),
    title varchar(200),
    abstract varchar(200),
    start_at timestamp,
    PRIMARY KEY(layer_id)
);

CREATE TABLE public.spatial
(
    spatial_id varchar(200),
    layer_id int,
    spatial_geometry geometry(Geometry,3035),
    PRIMARY KEY(spatial_id),
    CONSTRAINT fk_layer FOREIGN KEY(layer_id) REFERENCES layer(layer_id)
);


CREATE TABLE public.feature
(
    feature_id int,
    layer_id int,
    spatial_id varchar(200),
    properties jsonb,
    variable varchar(200),
    value double precision,
    unit varchar(200),
    z double precision,
    time timestamp,
    dt interval,
    PRIMARY KEY(layer_id),
    CONSTRAINT fk_layer FOREIGN KEY(layer_id) REFERENCES layer(layer_id),
    CONSTRAINT fk_spatial FOREIGN KEY(spatial_id) REFERENCES spatial(spatial_id)
);


CREATE TABLE public.bitmap
(
    layer_id int,
    raster_path varchar(200),
    z double precision,
    time timestamp,
    dt interval,
    CONSTRAINT fk_layer FOREIGN KEY(layer_id) REFERENCES layer(layer_id)
);

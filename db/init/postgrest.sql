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

-- Sample query
DROP FUNCTION IF EXISTS enermaps_query(dataset_id integer);
CREATE FUNCTION enermaps_query(dataset_id integer)
    RETURNS TABLE(fid char, variables json, fields json, start_at timestamp without time zone, dt float, z float, ds_id int, geometry text)
    AS 'SELECT data.fid,
            json_object_agg(variable, value) as variables,
            to_json(fields),
            start_at, dt, z, data.ds_id, st_astext(geometry)
           FROM data
    INNER JOIN spatial ON data.fid = spatial.fid
    WHERE data.ds_id = dataset_id
    GROUP BY data.fid, start_at, dt, z, data.ds_id, fields, geometry
    ORDER BY data.fid;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
GRANT EXECUTE ON FUNCTION enermaps_query(dataset_id integer) to api_user;

-- Sample query returning geojson
DROP FUNCTION IF EXISTS enermaps_geojson(dataset_id integer);
CREATE FUNCTION enermaps_geojson(dataset_id integer)
    RETURNS JSONB
    AS $$
    SELECT jsonb_build_object(
    'type',     'FeatureCollection',
    'features', jsonb_agg(features.feature)
)
FROM (
  SELECT jsonb_build_object(
    'type',       'Feature',
    'id',         fid,
    'geometry',   ST_AsGeoJSON(ST_TRANSFORM(geometry, 4326))::jsonb,
    'properties', to_jsonb(inputs) - 'fid' - 'geometry'
  ) AS feature
  FROM (SELECT data.fid,
        jsonb_object_agg(variable, value) as variables,
        fields,
        start_at, dt, z, data.ds_id, geometry
        FROM data
        INNER JOIN spatial ON data.fid = spatial.fid
        WHERE data.ds_id = dataset_id
        GROUP BY data.fid, start_at, dt, z, data.ds_id, fields, geometry
        ORDER BY data.fid) inputs) features;
        $$
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
GRANT EXECUTE ON FUNCTION enermaps_query(dataset_id integer) to api_user;


-- Code to support OPENAIRE gateway
-- Create a new datasets table to be filled in
-- as the original datasets table only contains integrated datasets
CREATE TABLE public.datasets_full
(
    ds_id int PRIMARY KEY,
    shared_id varchar(200),
    metadata json
);
GRANT SELECT ON public.datasets_full TO api_user;
-- Make it public to anynomous users
GRANT SELECT ON public.datasets_full TO api_anon;

-- Example of custom function
DROP FUNCTION IF EXISTS enermaps_get_metadata(shared_id text);
CREATE FUNCTION enermaps_get_metadata(shared_id text)
    RETURNS TABLE(title text, url text, description text)
    AS $$SELECT
        metadata ->> 'Title (with Hyperlink)' as title,
        metadata ->> 'URLs' AS url,
        metadata ->> 'Description (in brief)' as description
        FROM datasets_full
        WHERE metadata ->> 'shared_id' = shared_id;$$
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
GRANT EXECUTE ON FUNCTION enermaps_get_metadata(shared_id text) to api_user;

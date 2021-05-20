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

-- Example of custom function (to be used with POST request and authentication)
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

-- Utility function for making a JSON array out of CSV values (used for authors list)
DROP VIEW IF EXISTS datacite;
DROP FUNCTION IF EXISTS array_to_json_with_key(text[], text);
CREATE FUNCTION array_to_json_with_key(text[],text) RETURNS JSON AS $$
DECLARE
  s text;
  x text;
  counter int;
BEGIN
counter := 0;
s := '[';
  FOREACH x  IN ARRAY $1
  LOOP
    s := s || '{"' || $2 || '":"' || x || '"}';
    counter := counter + 1;
    IF counter < array_length($1,1) THEN
        s := s || ',';
    END IF;
  END LOOP;
s := s  || ']';
  RETURN JSON(s);
END;
$$ LANGUAGE plpgsql;
GRANT EXECUTE ON FUNCTION array_to_json_with_key(text[], text) to api_user;
GRANT EXECUTE ON FUNCTION array_to_json_with_key(text[], text) to api_anon;

CREATE VIEW datacite AS
SELECT json_agg(t) as data from (
SELECT shared_id AS id, row_to_json((
 SELECT x from (SELECT
    json_build_array(json_build_object('title',metadata->>'Title (with Hyperlink)')) as titles,
    json_build_array(
        json_build_object('identifier',metadata->>'Identifier',
        'identifierType', (CASE metadata->>'Identifier Type'
                                            WHEN 'Digital Object Identifier (DOI)' THEN 'DOI'
                                            WHEN 'Uniform Resource Locator (URL)' THEN 'URL'
                                            ELSE '?' END)
                                            )) as identifiers,
    array_to_json_with_key(string_to_array(metadata->>'Creator',','),'name') as creators,
    json_build_array(
        json_build_object('rights', text('OPEN'),
        'rightsUri','info:eu-repo/semantics/openAccess'),
        json_build_object('rights', metadata->>'License',
        'rightsUri','')
                        ) as "rightsList",
    json_build_array(
        json_build_object('lang', text('EN'),
        'description',metadata->>'Description (in brief)',
        'descriptionType', text('Abstract')
                                        )) as descriptions,
    metadata->>'Publisher' as publisher,
    metadata->>'Publication Year' as "publicationYear",
    json_build_array(
            json_build_object('date',metadata->>'Publication Date',
            'dateType', text('Issued'))
                                        ) as dates,
    json_build_array(
            json_build_object('resourceTypeGeneral',('Dataset'))
                                        )as "types",
    text('http://datacite.org/schema/kernel-4') as "schemaVersion",
    text('EnerMaps') as "source",
    bool(true) as "isActive")
    AS x )) AS "attributes" FROM datasets_full)t;
GRANT SELECT ON public.datacite to api_anon;

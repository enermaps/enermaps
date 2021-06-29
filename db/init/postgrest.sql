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


-- Query returning geojson with flexible json input (actually in text format, to be PostgREST-friendly)
-- Utility function to check whether a string is a json object
CREATE OR REPLACE FUNCTION is_json_object(p_json text)
  RETURNS boolean
AS
$$
BEGIN
    IF 0 < count(*) FROM json_object_keys(p_json::json) THEN
    RETURN TRUE;
    ELSE
    RETURN FALSE;
    END IF;
exception
  when others then
     return false;
END
$$
LANGUAGE plpgsql
IMMUTABLE;

-- Utility function to create a where-clause from json arguments
CREATE OR REPLACE FUNCTION create_json_where(_key text, _value json)
  RETURNS text
AS
$$
DECLARE
        _subkey text;
        _subvalue text;
        where_string text := '';
        counter int := 0;
BEGIN
    FOR _subkey, _subvalue IN SELECT * FROM json_each_text(_value)
        LOOP
        where_string := where_string || _key || ' ->> ''' || _subkey ||  ''' = ''' || _subvalue || '''';
        counter := counter + 1;
        IF counter < count(*) FROM json_object_keys(_value) THEN
            where_string := where_string || ' AND ';
        END IF;
        END LOOP;
    RETURN where_string;
END
$$
LANGUAGE plpgsql
IMMUTABLE;

-- Main function
CREATE OR REPLACE FUNCTION enermaps_query_geojson(parameters text,
                                                    row_limit int default 100,
                                                    row_offset int default 0)
    RETURNS JSONB
    AS $$
    DECLARE
        -- where string
        where_string text := 'WHERE ';
        -- variables to loop on the json input
        _key text;
        _value text;
        _subkey text;
        _subvalue text;
        counter int := 0;
        -- output
        out_jsonb jsonb;
    BEGIN
        FOR _key, _value IN
           SELECT * FROM json_each_text(parameters::json)
            LOOP
            IF _key = 'level' THEN
                where_string := where_string || 'spatial.levl_code = ANY(''' || _value || '''::levl[])';
            ELSIF _key = 'intersecting' THEN
                where_string := where_string || 'ST_intersects(spatial.geometry,ST_TRANSFORM(ST_GeometryFromText(''' || _value || ''',4326),3035))';
            ELSIF is_json_object(_value) THEN
                where_string :=  where_string ||  create_json_where(_key, _value::json);
            ELSE
                where_string := where_string || _key || ' = ' || _value;
            END IF;
            counter := counter + 1;
            IF counter < count(*) FROM json_object_keys(parameters::json) THEN
                where_string := where_string || ' AND ';
            END IF;
        END LOOP;
        EXECUTE format('
        SELECT jsonb_build_object(
        ''type'',     ''FeatureCollection'',
        ''features'', jsonb_agg(features.feature)
        )
            FROM (
              SELECT jsonb_build_object(
                ''type'',       ''Feature'',
                ''id'',         fid,
                ''geometry'',   ST_AsGeoJSON(ST_Reverse(ST_ForceRHR(ST_TRANSFORM(geometry, 4326))))::jsonb,
                ''properties'', to_jsonb(inputs) - ''fid'' - ''geometry''
              ) AS feature
                FROM (SELECT data.fid,
                    jsonb_object_agg(variable, value) as variables,
                    fields,
                    start_at, dt, z, data.ds_id, geometry
                    FROM data
                    INNER JOIN spatial ON data.fid = spatial.fid
                    %s
                    GROUP BY data.fid, start_at, dt, z, data.ds_id, fields, geometry
                    ORDER BY data.fid LIMIT %s OFFSET %s)
                inputs)
            features;', where_string, row_limit, row_offset)
        INTO out_jsonb;
        RETURN out_jsonb;
    END;
    $$
    LANGUAGE plpgsql;
GRANT EXECUTE ON FUNCTION enermaps_query_geojson(text, integer, integer) to api_user;

-- Equivalent function returning a table instead of GeoJSON
CREATE OR REPLACE FUNCTION enermaps_query_table(parameters text,
                                                row_limit int default 100,
                                                row_offset int default 0)
    RETURNS  table (
        fid varchar,
        variables jsonb,
        fields jsonb,
        start_at timestamp without time zone,
        dt double precision,
        z double precision,
        ds_id integer,
        geometry geometry(Geometry,3035)
    )
    AS $$
    DECLARE
        -- where string
        where_string text := 'WHERE ';
        -- variables to loop on the json input
        _key text;
        _value text;
        counter int := 0;
    BEGIN
        FOR _key, _value IN
           SELECT * FROM json_each_text(parameters::json)
            LOOP
            IF _key = 'level' THEN
                where_string := where_string || 'spatial.levl_code = ANY(''' || _value || '''::levl[])';
            ELSIF _key = 'intersecting' THEN
                where_string := where_string || 'ST_intersects(spatial.geometry,ST_TRANSFORM(ST_GeometryFromText(''' || _value || ''',4326),3035))';
            ELSIF is_json_object(_value) THEN
                where_string :=  where_string || create_json_where(_key, _value::json);
            ELSE
                where_string := where_string || _key || ' = ' || _value;
            END IF;
            counter := counter + 1;
            IF counter < count(*) FROM json_object_keys(parameters::json) THEN
                where_string := where_string || ' AND ';
            END IF;
        END LOOP;
        RETURN QUERY EXECUTE format('
        SELECT data.fid,
                    jsonb_object_agg(variable, value) as variables,
                    fields,
                    start_at, dt, z, data.ds_id, geometry
                    FROM data
                    INNER JOIN spatial ON data.fid = spatial.fid
                    %s
                    GROUP BY data.fid, start_at, dt, z, data.ds_id, fields, geometry
                    ORDER BY data.fid LIMIT %s OFFSET %s;', where_string, row_limit, row_offset);
    END;
    $$
    LANGUAGE plpgsql;
GRANT EXECUTE ON FUNCTION enermaps_query_table(parameters text, row_limit int, row_offset int) to api_user;


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
        metadata ->> 'Title' as title,
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
    json_build_array(json_build_object('title',metadata->>'Title')) as titles,
    json_build_array(
        json_build_object('identifier',metadata->>'Identifier',
        'identifierType', (CASE metadata->>'Identifier Type'
                                            WHEN 'Digital Object Identifier (DOI)' THEN 'DOI'
                                            WHEN 'Uniform Resource Locator (URL)' THEN 'URL'
                                            ELSE '?' END)
                                            )) as identifiers,
    array_to_json_with_key(string_to_array(metadata->>'Creator','; '),'name') as creators,
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

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
GRANT SELECT ON public.visualization TO api_user;


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
        IF _subvalue is null THEN
        where_string := where_string || _key || ' ->> ''' || _subkey ||  ''' IS NULL ';
        ELSE
        where_string := where_string || _key || ' ->> ''' || _subkey ||  ''' = ''' || _subvalue || '''';
        END IF;
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
                    jsonb_object_agg(variable, unit) as units,
                    fields,
                    legend,
                    start_at, dt, z, data.ds_id, geometry
                    FROM data
                    INNER JOIN spatial ON data.fid = spatial.fid
                    LEFT JOIN visualization ON data.vis_id = visualization.vis_id
                    %s
                    GROUP BY data.fid, start_at, dt, z, data.ds_id, fields, legend, geometry
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
DROP FUNCTION IF EXISTS enermaps_query_table(parameters text, row_limit int, row_offset int);
CREATE OR REPLACE FUNCTION enermaps_query_table(parameters text,
                                                row_limit int default 100,
                                                row_offset int default 0)
    RETURNS  table (
        fid varchar,
        variables jsonb,
        units jsonb,
        fields jsonb,
        legend jsonb,
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
                    jsonb_object_agg(variable, unit) as units,
                    fields,
                    legend,
                    start_at, dt, z, data.ds_id, geometry
                    FROM data
                    INNER JOIN spatial ON data.fid = spatial.fid
                    LEFT JOIN visualization ON data.vis_id = visualization.vis_id
                    %s
                    GROUP BY data.fid, start_at, dt, z, data.ds_id, fields, legend, geometry
                    ORDER BY data.fid LIMIT %s OFFSET %s;', where_string, row_limit, row_offset);
    END;
    $$
    LANGUAGE plpgsql;
GRANT EXECUTE ON FUNCTION enermaps_query_table(parameters text, row_limit int, row_offset int) to api_user;

-- View to provide list of parameters to construct the queries
CREATE OR REPLACE VIEW parameters AS
SELECT ds_id::int as ds_id,
        (metadata ->> 'Title (with Hyperlink)') as title,
        (metadata ->> 'parameters')::jsonb ->> 'variables' as variables,
        TO_TIMESTAMP((metadata ->> 'parameters')::jsonb ->> 'start_at', 'YYYY-MM-DD HH24:MI')::timestamp without time zone as start_at,
        TO_TIMESTAMP((metadata ->> 'parameters')::jsonb ->> 'end_at', 'YYYY-MM-DD HH24:MI')::timestamp without time zone as end_at,
        ((metadata ->> 'parameters')::jsonb ->> 'fields')::jsonb as fields,
        ((metadata ->> 'parameters')::jsonb ->> 'is_raster')::bool as is_raster,
        (metadata ->> 'parameters')::jsonb ->> 'temporal_granularity' as temporal_granularity,
        ((metadata ->> 'parameters')::jsonb ->> 'time_periods')::jsonb as time_periods,
        ((metadata ->> 'parameters')::jsonb ->> 'is_tiled')::bool as is_tiled,
        ((metadata ->> 'parameters')::jsonb ->> 'levels')::jsonb as levels,
        (metadata ->> 'default_parameters')::jsonb as default_parameters
        FROM datasets
        WHERE (metadata ->> 'Title (with Hyperlink)') <> ''
        ORDER BY ds_id;
GRANT SELECT ON public.parameters to api_anon;
GRANT SELECT ON public.parameters to api_user;


-- Code to support OPENAIRE gateway
-- Create a new datasets table to be filled in
-- as the original datasets table only contains integrated datasets
CREATE TABLE IF NOT EXISTS public.datasets_full
(
    ds_id int PRIMARY KEY,
    shared_id varchar(200),
    metadata json
);
GRANT SELECT ON public.datasets_full TO api_user;
-- Make it public to anynomous users
GRANT SELECT ON public.datasets_full TO api_anon;


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

-- Bibliographical metadata in Datacite format
DROP VIEW IF EXISTS datacite;
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
        'rightsUri',metadata->>'License URL')
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

-- EnerMaps-specific metadata
DROP VIEW IF EXISTS metadata;
CREATE VIEW metadata AS
SELECT ds_id, shared_id,
json_build_object(
                  'Title', metadata ->> 'Title',
                  'Link', metadata ->> 'Link',
                  'Description', metadata ->> 'Description (in brief)',
                  'Metadata of source dataset (URL)', metadata ->> 'Metadata URLs',
                  'Methodology (brief description)', metadata ->> 'Methodology (brief description)',
                  'Methodology (URL)', metadata ->> 'Methodology (URL to methodology descriptions)',
                  'Accuracy', metadata ->> 'Accuracy',
                  'Completeness', metadata ->> 'Completeness',
                  'Level', metadata ->> 'Level',
                  'Spatial Granularity', metadata ->> 'Spatial Granularity',
                  'DOI', metadata ->> 'DOI',
                  'Identifier', metadata ->> 'Identifier',
                  'Identifier type', metadata ->> 'Identifier type',
                  'Object', metadata ->> 'Object',
                  'Publisher', metadata ->> 'Publisher',
                  'Publication Date', metadata ->> 'Publication Date',
                  'Publication Year', metadata ->> 'Publication Year',
                  'Temporal Granularity', metadata ->> 'Temporal Granularity',
                  'Time references', metadata ->> 'Time references (time data refers)',
                  'URLs', metadata ->> 'URLs',
                  'Content (keywords)', metadata ->> 'Content (keywords)',
                  'Origin', metadata ->> 'Origin' ,
                  'Geographical extension', metadata ->>'Geographical extension',
                  'Projection system', metadata ->> 'Projection system',
                  'Access conditions', metadata ->> 'Access conditions',
                  'License', metadata ->> 'License',
                  'License URL', metadata ->> 'License URL',
                  'Terms of use', metadata ->> 'Terms of use',
                  'Availability', metadata ->> 'Availability',
                  'Resource type', metadata ->> 'Resource type',
                  'Data format', metadata ->> 'Data format',
                  'Size of file (raw, compressed in parentheses)', metadata ->> 'Size of file (raw, compressed in parentheses)',
                  'Other relevant information', metadata ->> 'Other relevant information'
                 ) as metadata
    from datasets_full
GROUP BY ds_id
ORDER BY ds_id;
GRANT SELECT ON public.metadata to api_anon;

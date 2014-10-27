CREATE OR REPLACE FUNCTION clean_address(address TEXT) RETURNS TEXT AS $$
    SELECT regexp_replace(regexp_replace(regexp_replace(regexp_replace(regexp_replace(regexp_replace(trim(address)
    , ' \#\w+$', '')   -- remove apartment number (ex: " #10" at end of address)
    , ' AV$', ' AVE')  -- format AV as AVE
    , ' BL$', ' BLVD') -- format BL as BLVD
    , ' FY$', ' FWY')   -- format FY as FWY
    , ' WY$', ' WAY')   -- format WY as WAY
    , ' HY$', ' HWY');  -- format HY as HWY
$$ LANGUAGE 'sql';

DROP MATERIALIZED VIEW standardized_fire_incidents;
CREATE MATERIALIZED VIEW standardized_fire_incidents AS
    SELECT *, clean_address(concat_ws(' ',  street_number::varchar, street_prefix::varchar, street_name::varchar, street_type::varchar, street_suffix::varchar)) AS standardized_address FROM fire_incidents;

CREATE INDEX ON standardized_fire_incidents (standardized_address);
CREATE INDEX ON standardized_fire_incidents (alarm_datetime);

DROP MATERIALIZED VIEW standardized_police_incidents;
CREATE MATERIALIZED VIEW standardized_police_incidents AS
    SELECT *, clean_address(concat_ws(' ',  street_number::varchar, street_prefix::varchar, street_name::varchar, street_type::varchar, street_suffix::varchar)) AS standardized_address FROM police_incidents;

CREATE INDEX ON standardized_police_incidents (standardized_address);
CREATE INDEX ON standardized_police_incidents (call_datetime);
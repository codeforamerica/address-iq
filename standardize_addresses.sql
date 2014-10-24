CREATE OR REPLACE FUNCTION clean_address(address TEXT) RETURNS TEXT AS $$
    SELECT regexp_replace(regexp_replace(regexp_replace(regexp_replace(regexp_replace(regexp_replace(address::varchar 
    , ' \#\w+$', '')   -- remove apartment number (ex: " #10" at end of address)
    , ' AV$', ' AVE')  -- format AV as AVE
    , ' BL$', ' BLVD') -- format BL as BLVD
    , ' FY$', ' FWY')   -- format FY as FWY
    , ' WY$', ' WAY')   -- format WY as WAY
    , ' HY$', ' HWY');  -- format HY as HWY
$$ LANGUAGE 'sql';

SELECT DISTINCT clean_address(concat_ws(' ',  street_number::varchar, street_prefix::varchar, street_name::varchar, street_type::varchar, street_suffix::varchar)) FROM fire_incidents;
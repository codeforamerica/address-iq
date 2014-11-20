CREATE EXTENSION pg_trgm;
CREATE INDEX trgm_idx ON address_summaries USING gist (address gist_trgm_ops);
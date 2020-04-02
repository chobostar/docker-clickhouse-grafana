CREATE DATABASE IF NOT EXISTS pg;

CREATE TABLE IF NOT EXISTS pg.pg_stat_statements (
    created_date Date DEFAULT today(),
    created_at DateTime DEFAULT now(),
	cluster_name LowCardinality(String),
	hostname LowCardinality(String),
	datname LowCardinality(String),
    username LowCardinality(String),
	query String,
	calls Float64,
	total_time Float64,
	rows Float64,
	shared_blks_hit Float64,
	shared_blks_read Float64,
	shared_blks_dirtied Float64,
	shared_blks_written Float64,
	local_blks_hit Float64,
	local_blks_read Float64,
	local_blks_dirtied Float64,
	local_blks_written Float64,
	temp_blks_read Float64,
	temp_blks_written Float64,
	blk_read_time Float64,
	blk_write_time Float64
) ENGINE = MergeTree(created_date, (created_at, cluster_name, hostname, datname, username), 8192)
TTL created_date + INTERVAL 10 DAY DELETE;
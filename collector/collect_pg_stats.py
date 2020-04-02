import os
from clickhouse_driver import Client
import psycopg2
import psycopg2.extras
from typing import Dict, List


def fetch_rows() -> List[Dict]:
    with psycopg2.connect("") as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    datname,
                    usename username,
                    left(query, 10000) as query, 
                    sum(calls) as calls, 
                    sum(total_time) as total_time, 
                    sum(rows) as rows,
                    sum(shared_blks_hit) as shared_blks_hit,
                    sum(shared_blks_read) as shared_blks_read,
                    sum(shared_blks_dirtied) as shared_blks_dirtied,
                    sum(shared_blks_written) as shared_blks_written,
                    sum(local_blks_hit) as local_blks_hit,
                    sum(local_blks_read) as local_blks_read,
                    sum(local_blks_dirtied) as local_blks_dirtied,
                    sum(local_blks_written) as local_blks_written,
                    sum(temp_blks_read) as temp_blks_read,
                    sum(temp_blks_written) as temp_blks_written,
                    sum(blk_read_time) as blk_read_time,
                    sum(blk_write_time) as blk_write_time
                FROM pg_stat_statements 
                JOIN pg_database ON pg_stat_statements.dbid = pg_database.oid
                JOIN pg_user ON pg_stat_statements.userid = pg_user.usesysid
                GROUP BY queryid, query, datname, usename
            """)
            return cur.fetchall()


def get_rows(cluster_name:str, hostname:str) -> List[Dict]:
    rows = fetch_rows()
    for row in rows:
        row.update({"cluster_name": cluster_name, "hostname": hostname})
    return rows


def push_to_clickhouse(rows:List[Dict]):
    client = Client('localhost')
    client.execute(
            "INSERT INTO pg.pg_stat_statements("
                "query,"
                "calls,"
                "total_time,"
                "rows,"
                "shared_blks_hit,"
                "shared_blks_read,"
                "shared_blks_dirtied,"
                "shared_blks_written,"
                "local_blks_hit,"
                "local_blks_read,"
                "local_blks_dirtied,"
                "local_blks_written,"
                "temp_blks_read,"
                "temp_blks_written,"
                "blk_read_time,"
                "blk_write_time,"
                "cluster_name,"
                "hostname,"
                "datname,"
                "username) VALUES",
                rows
        )


def configure():
    if not 'PGHOST' in os.environ:
        os.environ['PGHOST'] = 'localhost'
    if not 'PGUSER' in os.environ:
        os.environ['PGUSER'] = 'postgres'


def main():
    configure()
    rows = get_rows(cluster_name="docker", hostname="notebook")
    push_to_clickhouse(rows=rows)


if __name__ == '__main__':
    main()
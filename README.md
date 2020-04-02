# ClickHouse Grafana pg_stat_statements

## demo
![image](img/demo.png)

Custom Docker container + compose providing:
* [Clickhouse](https://github.com/yandex/ClickHouse/) Database _(latest)_
* [Grafana](https://github.com/grafana/grafana) w/ autoprovisioned [Clickhouse Datasource](https://github.com/Vertamedia/clickhouse-grafana) _(latest)_

##### More Examples
Full Examples are available on the project [wiki](https://github.com/lmangani/docker-clickhouse-grafana/wiki)


## Docker Hub Image
```
qxip/clickhouse-grafana
```

## Launch w/ Compose
```
docker-compose up -d
```

## Build Local Image
```
git clone https://github.com/lmangani/docker-clickhouse-grafana
cd docker-clickhouse-grafana

docker build -t qxip/clickhouse-grafana:local .
```

## Usage
Run migrations:
```
cd db/clickhouse
./migrate.sh

cd ../postgres
./migrate.sh
```
run bench:
```
pgbench -i -U postgres -h localhost

pgbench -T 3000
```
run collector:
```
watch -n 30 python3 collector/collector_pg_stats.py
```

query from Grafana
```sql
SELECT
    t,
    groupArray((query, rate)) AS groupArr
FROM
(
    SELECT
        t,
        query,
        if(runningDifference(c) <= 0, nan, runningDifference(c) / runningDifference(t / 1000)) AS rate
    FROM
(
        SELECT
            (intDiv(toUInt32(created_at), $interval) * $interval) * 1000 AS t,
            query,
            max(total_time) AS c
        FROM pg.pg_stat_statements
        WHERE
            ((created_date >= toDate($from)) AND(created_date <= toDate($to)))
            AND((created_at >= toDateTime($from)) AND(created_at <= toDateTime($to)))
            AND cluster_name = 'docker'
            AND hostname = 'notebook'
        GROUP BY
            t,
            query
        ORDER BY
            query ASC,
            t ASC
)
    WHERE rate >= 0
)
GROUP BY t
ORDER BY t ASC
```

##### Credits
This bundle lives thanks to the Vertamedia [clickhouse-grafana](https://github.com/Vertamedia/clickhouse-grafana) datasource plugin

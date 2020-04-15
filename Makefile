up:
	docker-compose up -d --build

down:
	docker-compose down --volumes

migrate:
	docker-compose exec -T clickhouse clickhouse-client -mn < ./db/clickhouse/init.sql
	docker-compose exec -T postgres psql -U postgres  < ./db/postgres/init.sql
	docker-compose exec -T postgres pgbench -U postgres -i

run:
	docker-compose exec -T postgres pgbench -U postgres --time 600 &
	watch -n 5 python3 ./collector/collect_pg_stats.py

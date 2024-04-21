# Migrations

`docker run --rm --network="tracker-network" -v "$(pwd)/migrations":/app liquibase/liquibase:4.19.0 --defaultsFile=/app/liquibase.properties update`

# Docker build

From root

`docker build -t gateway -f gateway/src/Dockerfile .`

# Docker run

`docker run -d --network="tracker-network" -p 8000:8000 gateway`
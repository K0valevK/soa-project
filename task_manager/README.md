# Migrations

`docker run --rm --network="tracker-network" -v "$(pwd)/migrations":/app liquibase/liquibase:4.19.0 --defaultsFile=/app/liquibase.properties update`

# Build docker

From root

`docker build -t task_manager -f task_manager/src/Dockerfile .`

# Run docker

`docker run -d --network="tracker-network" -p 8001:8001 task_manager`

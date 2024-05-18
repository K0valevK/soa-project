# Docker build

From root

`docker build -t statistics -f statistics/src/Dockerfile .`

# Docker run

`docker run -d --network="tracker-network statistics"`

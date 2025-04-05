COMPOSE = docker compose
ARGS = DOCKER_DEFAULT_PLATFORM=linux/amd64 COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 COMPOSE_BAKE=true

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Available targets:"
	@echo "  dev     - Build and start development environment"
	@echo "  down    - Stop and remove all containers"
	@echo "  clean   - Remove all containers, networks, and volumes"

# Development environment
dev:
	${ARGS} $(COMPOSE) --env-file ./.env -f docker-compose.yaml up --build --watch

test:
	$(COMPOSE) exec django python manage.py test shorturls.tests

# Stop and remove containers
down:
	$(COMPOSE) --env-file ./.env -f docker-compose.yaml down

# Clean up everything
clean:
	$(COMPOSE) --env-file ./.env -f docker-compose.yaml down -v --remove-orphans

.PHONY: help dev staging prod down clean

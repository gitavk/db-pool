# Optional if applicable for project
-include .env
export

# ==================================================================================== #
# HELPERS
# ==================================================================================== #

## help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

.PHONY: confirm
confirm:
	@echo -n 'Are you sure? [y/N] ' && read ans && [ $${ans:-N} = y ]

# ==================================================================================== #
# DATABASE INFO
# ==================================================================================== #

## show-db-settings: Display specific PostgreSQL settings from the running container in a table format
.PHONY: show-db-settings
show-db-settings:
	@echo "-- Live PostgreSQL Settings from container (filtered) --"
	@helpers/show_db_settings.sh
	@echo "--------------------------------------------------------"

# ==================================================================================== #
# SCENARIOS
# ==================================================================================== #

## scenario1: Run scenario 1 (Normal Operation) and display results
.PHONY: scenario1
scenario1:
	docker compose down
	docker compose up --abort-on-container-exit app
	docker compose down

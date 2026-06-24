.PHONY: help setup backend ai-engine mobile web admin teacher migrate seed seed-sources lint test docker-up docker-down clean

help:
	@echo "BreadBoard AI - Development Commands"
	@echo "------------------------------------"
	@echo "make setup          - Full project setup (backend + ai-engine)"
	@echo "make backend        - Install backend dependencies"
	@echo "make ai-engine      - Install AI engine dependencies"
	@echo "make mobile         - Install mobile app deps"
	@echo "make web            - Install web app deps"
	@echo "make admin          - Install admin panel deps"
	@echo "make teacher        - Install teacher dashboard deps"
	@echo "make migrate        - Run database migrations"
	@echo "make seed           - Seed database (all)"
	@echo "make seed-sources   - Seed priority content sources"
	@echo "make lint           - Lint all Python code"
	@echo "make test           - Run all tests"
	@echo "make docker-up      - Start all Docker services"
	@echo "make docker-down    - Stop all Docker services"
	@echo "make clean          - Clean build artifacts"

setup: backend ai-engine

backend:
	cd backend && pip install -r requirements/dev.txt

ai-engine:
	cd ai-engine && pip install -r requirements.txt

mobile:
	cd apps/mobile_app && flutter pub get
	cd apps/packages/shared && flutter pub get

web:
	cd apps/web_app && flutter pub get

admin:
	cd apps/admin_panel && flutter pub get

teacher:
	cd apps/teacher_dashboard && flutter pub get

migrate:
	cd backend && alembic upgrade head

seed:
	cd backend && python -m app.db.seeds

seed-sources:
	cd backend && python -m app.db.seeds.seed_sources

lint:
	cd backend && flake8 app tests
	cd ai-engine && flake8 engine tests

test:
	cd backend && pytest
	cd ai-engine && pytest

docker-up:
	docker-compose -f infrastructure/docker/docker-compose.yml up -d

docker-up-prod:
	docker-compose -f infrastructure/docker/docker-compose.yml -f infrastructure/docker/docker-compose.prod.yml up -d

docker-down:
	docker-compose -f infrastructure/docker/docker-compose.yml down

setup-ssl:
	chmod +x infrastructure/scripts/setup_ssl.sh && ./infrastructure/scripts/setup_ssl.sh

download-models:
	chmod +x infrastructure/scripts/download_models.sh && ./infrastructure/scripts/download_models.sh

ifeq ($(OS),Windows_NT)
clean:
	@if exist . rmdir /s /q __pycache__ 2>nul & rmdir /s /q .pytest_cache 2>nul & rmdir /s /q *.egg-info 2>nul & del /s /q *.pyc 2>nul || true
else
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name *.egg-info -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name *.pyc -delete 2>/dev/null || true
endif

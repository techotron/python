.PHONY: deps
deps:
	pipenv install --dev

.PHONY: up-db
up-db:
	docker-compose up -d chapter5_db

.PHONY: down
down:
	docker-compose down

.PHONY: chapter5_setup_db
chapter5_setup_db:
	python chapter5_3_synchronous_schema_setup.py
	python chapter5_5_inserting_random_brands.py
	python chapter5_6_inserting_random_products_skus.py

.PHONY: chapter9_8_start_uvicorn
chapter9_8_start_uvicorn:
	uvicorn --workers 8 --log-level error chapter9_8_starlette_brands_endpoint:app

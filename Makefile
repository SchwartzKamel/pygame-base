build:
	docker build -t sierrahackingco/pygame-flapper:latest .

test:
	pytest tests/ -v --cov=app --cov-report=term-missing

lint:
	flake8 app/ tests/ --max-line-length=120 --ignore=E203,W503

ci: lint test

help:
	@echo "build test"
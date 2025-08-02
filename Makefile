build:
	docker build -t sierrahackingco/pygame-flapper:latest .

test:
	docker run --name pygame-flapper sierrahackingco/pygame-flapper:latest

help:
	@echo "build test"

help:
	cat Makefile
run:
	docker-compose up
exec:
	docker-compose exec dssv-dev-env bash
build: stop .FORCE
	docker-compose build
rebuild: stop .FORCE
	docker-compose build --force-rm
stop:
	docker stop dssv || true; docker rm dssv || true;
.FORCE:

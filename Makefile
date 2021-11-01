build:
	docker build . --tag autotest
remove:
	docker rmi -f autotest
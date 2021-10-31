build:
	sudo docker build . --tag autotest
remove:
	sudo docker rmi -f autotest
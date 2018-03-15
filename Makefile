build: Dockerfile
	docker build -t graphtheorycompetition .

run: build
	docker run -d --rm --name graphtheorycompetitionc -p 8888:8888 -v `pwd`:/home/jovyan/work graphtheorycompetition start-notebook.sh --NotebookApp.token=''

stop:
	docker stop graphtheorycompetitionc

terminal:
	docker run --rm -it -v `pwd`:/home/jovyan/work graphtheorycompetition /bin/bash

clean:
	docker rmi graphtheorycompetition
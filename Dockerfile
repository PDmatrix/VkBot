FROM 		python:3.7.1-slim
WORKDIR 	/usr/src/app
COPY 		requirements.txt ./
RUN 		pip install --no-cache-dir -r requirements.txt
COPY 		. .
ENV		    PYTHONPATH /usr/src/app
ENV 		PYTHONUNBUFFERED 1
EXPOSE		8080
CMD 		[ "python", "./src/app.py" ]

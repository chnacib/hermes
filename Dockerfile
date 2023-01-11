FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN apt-get update -y 
RUN apt-get install -y awscli
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3","main.py" ]
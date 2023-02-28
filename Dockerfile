FROM python:3.8.10
USER root
RUN mkdir /app
COPY . /app/
WORKDIR /app/
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python", "./main.py] 
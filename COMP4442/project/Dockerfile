FROM python:3.13.1

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN rm -rf Dockerfile
RUN rm -rf requirements.txt
RUN rm -rf docker-compose.yml
RUN rm -rf .gitignore

EXPOSE 5000

CMD ["python", "/app/application.py"]
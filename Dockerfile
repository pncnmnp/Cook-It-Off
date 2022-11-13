FROM python:3.8-alpine
RUN python3 -m pip install flask
WORKDIR /app
COPY . .
ENTRYPOINT [ "flask", "--app", "server", "--debug", "run", "--host", "0.0.0.0" ]

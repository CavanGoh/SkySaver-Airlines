FROM python:3.9-slim
WORKDIR /app
COPY ./app
RUN pip install flask
EXPOSE 5002
ENV FLASK_APP=price.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--port=5002"]

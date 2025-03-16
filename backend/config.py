import os

class Config:
    # Flask Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    DEBUG = os.getenv("DEBUG", True)

    # RabbitMQ Settings
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "notifications.exchange")
    RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "notifications.queue")

    # OutSystems API (For Notifications)
    OUTSYSTEMS_API_URL = os.getenv("OUTSYSTEMS_API_URL", "https://your-outsystems-app.com/api/notifications")

# Load Config
config = Config()

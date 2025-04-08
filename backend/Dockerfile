# Use the official RabbitMQ 3.x image with management plugin
FROM rabbitmq:3-management

# Set hostname for RabbitMQ node
ENV HOSTNAME=skysaver-rabbit

# Expose RabbitMQ ports
# 5672: AMQP protocol used by the microservices
# 15672: Management UI
EXPOSE 5672 15672


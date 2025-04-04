# Start from Python slim image
FROM python:3-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements.txt and install dependencies
COPY ./BookFlight/requirements.txt ./
RUN python -m pip install --no-cache-dir -r ./BookFlight/requirements.txt

# Copy the specific files needed for your composite microservice
COPY ./BookFlight/BookFlight.py ./compositeMicroServices/
COPY ./wrapperServices/invokes.py ./wrapperServices/

# Set the command to run the composite microservice
CMD ["python", "./compositeMicroServices/bookFlight.py"]


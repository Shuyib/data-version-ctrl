# Use latest Python runtime as a parent image
FROM python:3.12-slim

# Meta-data
LABEL maintainer="Shuyib" \
      description="Regression test using data version control principles" 
      
# Set the working directory to /app
WORKDIR /app

# ensures that the python output is sent to the terminal without buffering
ENV PYTHONUNBUFFERED=TRUE

# Copy the current directory contents into the container at /app
COPY . /app
COPY kaggle.json /root/.kaggle/

# Set the environment variable for kaggle 
ENV KAGGLE_CONFIG_DIR=/root/.kaggle

# Install make and other dependencies
RUN apt-get update && apt-get install -y make


# create a virtual environment, activate it and install the required libraries
RUN python3 -m venv .venv &&\
            . .venv/bin/activate &&\
            pip --no-cache-dir install --upgrade pip &&\
            pip --no-cache-dir install --requirement requirements.txt


# Create mountpoint
VOLUME /app

# Run makefile
CMD ["make", "all"]
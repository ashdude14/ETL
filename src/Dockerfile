FROM python:3.9-alpine

# Environment Variable

ENV PYTHONUNBUFFERED=1


# To Display GUI inside the container [Ref: https://www.geeksforgeeks.org/how-to-run-gui-based-applications-inside-docker/ ]
# [Ref: https://medium.com/@priyamsanodiya340/running-gui-applications-in-docker-containers-a-step-by-step-guide-335b54472e4b]
# x11 display server :99 is often used in the context of Docker and headless browsers 
# Managed by [Xvfb] [Ref: https://en.wikipedia.org/wiki/Xvfb ]
ENV DISPLAY=:99  

# Install dependencies (Installind dependencies needed to run project including OS setup, ensuring reduced size of image)
RUN apk update && apk add --no-cache \
    bash \
    curl \
    wget \
    unzip \
    libx11 \
    libxcomposite \
    libxrandr \
    libxdamage \
    mesa-gl \
    nss \
    ca-certificates \
    ttf-freefont \
    chromium \
    chromium-chromedriver \
    xvfb \
    && rm -rf /var/cache/apk/*


 # Set Location for the chromium and chromium-webdriver
 RUN ln -s /usr/bin/chromium /usr/bin/google-chrome-stable

# Set environment variable for Chrome binary
ENV CHROME_BIN=/usr/bin/chromium

 # Installing Python Dependencies from requirement.txt

 COPY requirements.txt app/requirements.txt

 WORKDIR /app

 RUN pip install --no-cache-dir -r requirements.txt

 # Set the working directory to /app
WORKDIR /app

EXPOSE 4444

# Copy the script into the container
COPY test.py /app/test.py

# Step 1: Creating data.csv file inside container
RUN mkdir -p /app/data && touch /app/data/data.csv

# Step 2: Running the Xvfb server and Python script
#CMD ["sh", "-c", "Xvfb :99 -screen 0 1280x1024x24 & python test.py"]

CMD ["python", "test.py"]



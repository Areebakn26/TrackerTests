FROM python:3.10-slim

# Install dependencies
RUN apt update && apt install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome repo
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-linux.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google.list

# Install Chrome (fixed stable version)
RUN apt update && apt install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*

# FIXED VERSION CHROMEDRIVER (always compatible with stable Chrome)
ENV CHROMEDRIVER_VERSION=latest

RUN LATEST=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json \
    | grep -B3 "chrome-stable" | grep linux64 | grep chromedriver | head -1 | cut -d '"' -f 4) \
    && wget -q $LATEST -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Set workdir
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "-s"]

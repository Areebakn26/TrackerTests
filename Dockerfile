FROM python:3.10-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt update && apt install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome repository
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google.list

# Install Google Chrome
RUN apt update && apt install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver SAME VERSION as Chrome
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json" \
    | grep -B3 $CHROME_VERSION | grep linux64 | grep chromedriver | head -1 | cut -d '"' -f 4) \
    && wget -q $DRIVER_VERSION -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Install Python dependencies
RUN pip install selenium webdriver-manager pytest

# Copy tests
WORKDIR /tests
COPY . .

CMD ["pytest", "-q"]

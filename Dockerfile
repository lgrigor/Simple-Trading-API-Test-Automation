# Use a Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app/Tests/API

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install JMeter
ARG JMETER_VERSION=5.4.1
RUN apt-get update && apt-get install -y wget \
    && wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz \
    && tar -xzf apache-jmeter-${JMETER_VERSION}.tgz \
    && rm apache-jmeter-${JMETER_VERSION}.tgz \
    && mv apache-jmeter-${JMETER_VERSION} /opt/jmeter

# Add JMeter to the PATH variable
ENV PATH="${PATH}:/opt/jmeter/bin"

# Copy the test scripts and any other necessary files
COPY . .

# Uncomment below to do full regression run
# CMD ["pytest", "-s"]

# Uncomment below to run regression without performance tests
# CMD ["pytest", "-s", "-m", "api_test", "--html=/app/Results/report.html"]

# Uncomment below to run only performance tests
CMD ["pytest", "-s", "-m", "performance_test", "--html=/app/Results/report.html"]


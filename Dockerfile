FROM python:3.11-slim-buster

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install the latest SQLite version (e.g., 3.46.1 as of now)
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3460100.tar.gz && \
    tar xvfz sqlite-autoconf-3460100.tar.gz && \
    cd sqlite-autoconf-3460100 && \
    ./configure --prefix=/usr && \
    make && make install && \
    cd .. && rm -rf sqlite-autoconf-3460100* \

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set workdir to the project directory
WORKDIR /app

# Copy requirements.txt.txt and install dependencies
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app/

# Expose the port that the Django app runs on
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
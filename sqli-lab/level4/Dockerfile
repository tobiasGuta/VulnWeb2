FROM php:8.2-apache

# Install dependencies for pdo_sqlite build
RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    pkg-config \
 && docker-php-ext-install pdo_sqlite \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html
COPY app/ /var/www/html/

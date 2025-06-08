FROM php:8.2-apache

# Enable mysqli extension
RUN docker-php-ext-install mysqli

# Copy custom apache config for pretty URLs (optional)
#COPY apache.conf /etc/apache2/sites-available/000-default.conf

# Enable mod_rewrite if needed
RUN a2enmod rewrite

WORKDIR /var/www/html

FROM php:8.2-apache

COPY . /var/www/html/

RUN docker-php-ext-install mysqli

COPY php.ini /usr/local/etc/php/php.ini

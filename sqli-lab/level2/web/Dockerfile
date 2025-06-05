FROM php:7.4-apache

RUN docker-php-ext-install mysqli

COPY user.php /var/www/html/user.php

EXPOSE 80

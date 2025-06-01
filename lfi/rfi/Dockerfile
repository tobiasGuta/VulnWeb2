FROM php:8.4-cli

RUN echo "allow_url_fopen=On" >> /usr/local/etc/php/php.ini \
 && echo "allow_url_include=On" >> /usr/local/etc/php/php.ini

WORKDIR /var/www/html

COPY . /var/www/html/

EXPOSE 8080

CMD ["php", "-S", "0.0.0.0:8080", "-t", "/var/www/html"]

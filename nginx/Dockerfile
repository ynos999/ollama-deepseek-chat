FROM nginx:alpine

# Dzēšam noklusēto Nginx lapu
RUN rm /usr/share/nginx/html/index.html

# Iekopējam tavus failus (ceļi atbilst "context: ." tavā compose failā)
COPY ./frontend /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/mime.types /etc/nginx/mime.types

EXPOSE 80
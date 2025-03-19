FROM nginx:alpine
WORKDIR /usr/share/nginx/html
# Remove default Nginx HTML files
RUN rm -rf /usr/share/nginx/html/*
COPY . .
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
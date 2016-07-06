FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/app.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY uwsgi_params /etc/nginx/uwsgi_params
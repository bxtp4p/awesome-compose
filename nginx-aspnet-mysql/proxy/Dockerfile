FROM ubuntu/nginx:1.18-20.04_beta

COPY nginx.conf /etc/nginx/

COPY conf /etc/nginx/conf.d/default.conf

COPY otel_ngx_module.so /etc/nginx/modules/otel_ngx_module.so

RUN chmod +x /etc/nginx/modules/otel_ngx_module.so
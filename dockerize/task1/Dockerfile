FROM alpine:3.18

WORKDIR /app

ENV COUNT 8
ENV MSG "Hello Docker!"

COPY ./lucas.sh .
COPY ./echo.sh .
RUN chmod +x lucas.sh
CMD ["./lucas.sh"]
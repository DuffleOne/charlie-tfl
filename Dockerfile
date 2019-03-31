FROM alpine:3.9.2
RUN apk add --update python py-pip
COPY web.py /src/web.py
EXPOSE 9000
CMD ["python", "/src/web.py"]

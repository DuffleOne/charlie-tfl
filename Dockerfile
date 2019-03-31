FROM alpine:3.9.2
RUN apk add --no-cache ca-certificates
RUN apk add --update python py-pip
RUN pip install requests
COPY web.py /src/web.py
EXPOSE 8000
CMD ["python", "/src/web.py"]

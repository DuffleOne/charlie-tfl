FROM python:3
RUN pip install requests
COPY web.py /src/web.py
EXPOSE 8000
CMD ["python", "/src/web.py"]

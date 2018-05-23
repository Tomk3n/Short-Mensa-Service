FROM python:3.6.5-alpine3.7
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app
#EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]

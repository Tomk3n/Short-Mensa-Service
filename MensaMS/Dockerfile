FROM python:3
WORKDIR /app
ADD . /app
#EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

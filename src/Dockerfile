FROM python:3.8
RUN mkdir /usr/src/app/
COPY . /usr/src/app/
WORKDIR /usr/src/app/
RUN pip3 install -r requirements.txt
CMD ["python3", "./app.py"]
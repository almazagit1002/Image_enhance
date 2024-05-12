FROM python:3.8-slim-buster

RUN apt update -y
WORKDIR /Image_enhance

COPY . /Image_enhance
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
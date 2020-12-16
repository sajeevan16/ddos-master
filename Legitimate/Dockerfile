FROM python:3.8-alpine
RUN echo "@main http://dl-cdn.alpinelinux.org/alpine/v3.12/main" >> /etc/apk/repositories
RUN apk add --update --no-cache py3-numpy
ENV PYTHONPATH=/usr/lib/python3.8/site-packages

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip --no-cache-dir install -r requirements.txt

COPY . /app

EXPOSE 5000
ENTRYPOINT [ "python" ] 
CMD [ "Legitimate.py" ]


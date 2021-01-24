FROM ubuntu:16.04
RUN apt-get update -y 
RUN apt-get install -y python-pip
RUN apt-get install -y python2.7


WORKDIR /app

#COPY ./requirements.txt /app/requirements.txt

RUN pip install colorama termcolor requests

COPY . /app

EXPOSE 5000
#ENTRYPOINT [ "python" ] 
#CMD [ "Legitimate.py" ]

#CMD python pyddos1.py -d www.google.com -p 80 -T 200 -Synflood
#CMD python3 Legitimate.py > logFile.txt &

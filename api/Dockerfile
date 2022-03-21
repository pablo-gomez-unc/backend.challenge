FROM python:3.8

WORKDIR /usr/app

ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ ./

EXPOSE 8082

CMD ["flask", "run" , "-h" , "0.0.0.0" , "-p" , "8082" ]

FROM python:3.8-slim-buster
ADD . /app
WORKDIR /app
ADD ./requirements.txt /srv/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP main.py
CMD ["sh", "entrypoint.sh"]
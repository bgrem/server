FROM python:3.8-slim-buster
ADD . /app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . . 
EXPOSE 8070
ENV FLASK_APP main.py
CMD ["sh", "entrypoint.sh"]
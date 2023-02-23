FROM python:3.9 
WORKDIR /usr/app
COPY requirements.txt .
run pip install -r requirements.txt
COPY . .

CMD ["flask","--app", "app", "run","--host=0.0.0.0","--port=8012"]
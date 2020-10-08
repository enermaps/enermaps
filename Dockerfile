FROM ubuntu

RUN apt update && apt install --yes --nointeractive python3-mapnick

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

ENTRYPOINT ["python", "app.py"]

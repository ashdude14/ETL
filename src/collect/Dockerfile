FROM python:3.12-alpine

WORKDIR /app
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY collect.py /app/collect.py

CMD [ "python","/app/collect.py" ]

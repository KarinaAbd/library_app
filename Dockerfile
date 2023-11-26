FROM python:3.10

ADD . ./app
WORKDIR /app
RUN python3 -m pip install --no-cache-dir --no-warn-script-location --upgrade pip \
    && pip install -r requirements.txt

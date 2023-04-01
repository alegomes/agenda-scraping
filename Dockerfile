#
# Build Image
# docker build -t agenda-scraper-job .
#
# Run it
# docker run -d --mount type=bind,source="$(pwd)"/log,target="/app/log" agenda-scraper-job
# docker run -it --mount type=bind,source="$(pwd)"/log,target="/app/log" agenda-scraper-job bash

FROM python:3.9-alpine

RUN apk update ; apk upgrade ; apk add bash

WORKDIR /app

COPY hello.py /app/hello.py
COPY crontab /app/crontab

RUN mkdir log

RUN chmod 0644 /app/crontab
RUN crontab /app/crontab

CMD ["crond", "-f"]

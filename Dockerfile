#
# Build Image
# docker build -t agenda-scraper-job .
#
# Run it and leave
# docker run -d --mount type=bind,source="$(pwd)"/log,target="/app/log" agenda-scraper-job
#
# Run and log into it
# docker run -it --mount type=bind,source="$(pwd)"/log,target="/app/log" agenda-scraper-job bash
#
# Run and see sysout:
# docker run -it --mount type=bind,source="$(pwd)"/log,target="/app/log" agenda-scraper-job

FROM python:3.9-alpine

RUN apk update ; apk upgrade ; apk add bash

WORKDIR /app

COPY hello.py /app/hello.py
COPY agenda_scraping_logging.py /app/
COPY crontab /app/crontab

RUN mkdir log

RUN chmod 0644 /app/crontab
RUN crontab /app/crontab

CMD ["crond", "-f"]

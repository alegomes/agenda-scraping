#
# Build Image
# docker build -t agenda-scraper-job .
#
# Create agenda-net, if it doesn't exist yet
# docker create network agenda-net
#
# Run it and leave
# docker run --name job --network agenda-net --rm -d --mount type=bind,source="$(pwd)"/log,target="/app/log" agenda-scraper-job
#
# Run and log into it
# docker run -it --mount type=bind,source="$(pwd)"/log,target="/app/log" agenda-scraper-job bash
#
# Run and see sysout:
# docker run -it --mount type=bind,source="$(pwd)"/log,target="/app/log" agenda-scraper-job
#
# Just get into it
# docker exec -it job bash

FROM python:3.11-alpine

ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"

RUN apk update ; apk upgrade 

RUN apk --no-cache add \
    bash \
    musl-locales \
    musl-locales-lang \
    ssmtp

WORKDIR /app

COPY src /app/src
COPY crontab /app/crontab

RUN pip install -r src/requirements.txt

RUN mkdir log
RUN mkdir -p data/raw

RUN chmod 0644 /app/crontab
RUN crontab /app/crontab

CMD ["crond", "-f"]

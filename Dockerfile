FROM python:3.9-slim as compile

RUN apt-get update \
    && apt-get install make gcc g++ -y --no-install-recommends \
    && apt-get clean

RUN mkdir /install
WORKDIR /install
COPY requirements.txt .
RUN pip install --prefix=/install --no-warn-script-location --no-cache-dir -r requirements.txt && rm -rf /root/.cache

FROM python:3.9-slim as build
COPY --from=compile /install /usr/local
COPY . /app
WORKDIR /app

EXPOSE 8080

# Default command
CMD ["/app/entrypoint.sh"]

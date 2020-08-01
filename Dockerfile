FROM python:3.8-slim

RUN apt-get update \
    && apt-get install make gcc g++ -y \
    && apt-get clean
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache
COPY . /app
EXPOSE 8080

# Default command
CMD ["/app/entrypoint.sh"]

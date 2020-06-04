# Environment
ENV = "local"
SERVICE_NAME = "mono"

# JWT
JWT_SECRET = "secret"
JWT_REFRESH_SECRET = "refresh_secret"
JWT_EXPIRATION = 24 * 3600
JWT_REFRESH_EXPIRATION = 7 * 24 * 3600

# Database
MASTER_DATABASE_URL = ["postgresql+psycopg2://user:pass@localhost:5432/dbname"]
SLAVE_DATABASE_URL = MASTER_DATABASE_URL
REDIS_URL = "redis://localhost"

# Instrument
SENTRY_DSN = "https://28ed46e0f403456091ee6b71ba29a272@o376446.ingest.sentry.io/5197268"

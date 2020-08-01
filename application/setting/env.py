# Environment
import os

ENV = "development"
SERVICE_NAME = "mono"

# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "secret")
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET", "refresh_secret")
JWT_EXPIRATION = int(os.getenv("JWT_EXPIRATION", "3600"))
JWT_REFRESH_EXPIRATION = int(os.getenv("JWT_REFRESH_EXPIRATION", "86400"))

# Database
PRIMARY_DB_URL = os.getenv(
    "PRIMARY_DB_URL", "postgresql+psycopg2://user:pass@localhost:5432/dbname"
)
REPLICA_DB_URL = os.getenv("REPLICA_DB_URL", PRIMARY_DB_URL)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost")

# Instrument
SENTRY_DSN = "https://28ed46e0f403456091ee6b71ba29a272@o376446.ingest.sentry.io/5197268"

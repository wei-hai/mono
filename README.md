# Mono

The mono service built with python web framework [Sanic](https://github.com/huge-success/sanic)

## Development

### Environment setup

```bash
# python 3.8
brew install python@3.8
# virtual environment
make init-venv
# requirements
make install-all
# infrastructure
make start-infra
# migration
make db-upgrade
```

### Run the server

#### Debug mode

```bash
make dev
```

#### Production mode

```bash
make run
```

### Run test cases

```bash
make test
```

### Check code quality

```bash
make check
```

### Format code

```bash
make format
```

### Database migration

#### Revision

```bash
make db-revision r="001" m="user"
```

WARNING: Statement like extension creation in the migration file will fail because the service account does not have the privilege, you must contact the DB creator who has the admin account to create the extension for you manually before deploying the migration file, and you must keep the extension creation statement in the migration file to keep everything consistent.

```python
op.execute('CREATE EXTENTION IF NOT EXISTS pg_trgm;')
```

TIPS: When you create index, upgrade local database, run all test cases several times and run the following SQL statement to see if the index is used

```sql
SELECT
    s.indexrelid,
    s.schemaname,
    s.relname AS tablename,
    s.indexrelname AS indexname,
    pg_relation_size(s.indexrelid) AS index_size,
    pg_size_pretty(pg_relation_size(s.indexrelid)) AS size_gb,
    s.idx_scan AS n_scans
FROM pg_catalog.pg_stat_user_indexes s
JOIN pg_catalog.pg_index i ON s.indexrelid = i.indexrelid
WHERE
  s.schemaname = 'public'
  AND NOT i.indisunique   -- is not a UNIQUE index
  AND NOT EXISTS          -- does not enforce a constraint
     (SELECT 1 FROM pg_catalog.pg_constraint c WHERE c.conindid = s.indexrelid)
ORDER BY tablename, n_scans ASC;
```

#### Upgrade

```bash
make db-upgrade
```

#### Downgrade

```bash
make db-downgrade
```

### Browse APIs

```bash
http://localhost:8080/swagger
```

## Project Structure

```text
.
├── application
│   ├── api                 # Controller
│   ├── model               # Model
│   ├── repository          # Data Access Object
│   ├── service             # Service
│   ├── setting             # Setting
│   ├── util                # Utility
├── migration               # Model migration
└── tests                   # Test cases
```

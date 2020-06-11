# Mono

Mono service, it uses [Sanic](https://github.com/huge-success/sanic) and works with sqlalchemy, postgres and redis to build a service that demonstrates user sign up, sign in and jwt refresh.

## Development

### Environment

```.bash
make init-env
```

### Run

```.bash
make debug
```

### Test

```.bash
make test
```

### Code quality

```.bash
make check
```

## Database migration

### Revision

```.bash
make db-revision r="001" m="user"
```

### Upgrade

```.bash
make db-upgrade
```

### Downgrade

```.bash
make db-downgrade
```

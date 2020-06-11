# Mono

Mono service

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

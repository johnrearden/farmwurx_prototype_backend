# farmwurx_prototype_backend

### Deployment

The backend application (prototype) is currently deployed on a single Hetzner CX22 instance (2 CPU, 4GB RAM, 40GB disk, 20TB traffic out)

###### IP Address
46.62.150.15


### Setting up Redis and Celery
```
pip install redis celery
```

```
sudo apt update && sudo apt install redis-server -y
```

```
redis-server
```

```
celery -A config worker --loglevel=info
```
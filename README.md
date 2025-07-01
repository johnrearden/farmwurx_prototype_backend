# farmwurx_prototype_backend


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
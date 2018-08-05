from redis import Redis

from blog import settings

rds = Redis(**settings.REDIS)
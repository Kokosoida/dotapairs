import os
from itertools import cycle

import dota2api
from logzero import logger
from pymongo import MongoClient

dota_apis = []
for i in range(1, 10):
    try:
        env_var = 'D2_API_KEY_%s' % i
        dota_apis.append(dota2api.Initialise(os.environ[env_var]))
    except KeyError:
        break
logger.info('Working with %s apis' % len(dota_apis))

dota_api_iter = cycle(dota_apis)


mongo_client = MongoClient()
mongo_db = mongo_client['dotapairs']

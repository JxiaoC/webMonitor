# -*- coding:utf-8 -*-

from db.conn import mc

# mc = mongo_client
MONGO_DB_MAPPING = {
    'db': {
        'web-monitor': mc['web_monitor'],
    },
    'db_file': {
    }
}

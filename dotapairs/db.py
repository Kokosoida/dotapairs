from dotapairs.ext import mongo_db


def ensure_indexes():
    mongo_db.matches.create_index('match_seq_num', unique=True)

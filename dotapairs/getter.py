from datetime import datetime
from json.decoder import JSONDecodeError

from logzero import logger
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential

from dotapairs.ext import dota_api_iter, mongo_db

MODE_IDS_SUITABLE = {1, 2, 3, 4, 5, 16, 22}
LOBBY_TYPE_ID_PUB = 0
MINIMUM_DURATION = 10 * 60

STARTING_MATCH_ID = 2753240690

class MatchGetter:

    def check_match_suitable(self, match):
        if match['lobby_type'] != LOBBY_TYPE_ID_PUB:
            return False
        if match['game_mode'] not in MODE_IDS_SUITABLE:
            return False
        if match['duration'] < MINIMUM_DURATION:
            return False
        return True

    def get_team(self, player_slot):
        if player_slot >> 7:
            return 'dire'
        return 'radiant'

    @retry(wait=wait_exponential(multiplier=1, max=60), stop=stop_after_attempt(10))
    def get_matches(self, starting_seq_num):
        try:
            api = next(dota_api_iter)
            matches = api.get_match_history_by_seq_num(starting_seq_num)['matches']
        except JSONDecodeError:
            logger.warning('Error getting match history /w api %s', api)
            raise

        results = []
        for match in matches:
            if not self.check_match_suitable(match):
                continue

            heroes = {'radiant': [], 'dire': []}

            for player in match['players']:
                heroes[self.get_team(player['player_slot'])].append(player['hero_id'])

            match_dict = {
                'match_id': match['match_id'],
                'match_seq_num': match['match_seq_num'],
                'game_mode': match['game_mode'],
                'radiant_win': match['radiant_win'],
                'start_time': match['start_time'],
                'heroes': heroes,
            }
            results.append(match_dict)
        return results


def get_and_save_matches(starting_seq_num):
    matches = MatchGetter().get_matches(starting_seq_num)
    mongo_db.matches.insert_many(matches)


def get_max_seq_num():
    max_match = mongo_db.matches.find_one(sort=[('match_seq_num', -1)])
    logger.info('Max TS is %s now', datetime.fromtimestamp(max_match['start_time']))
    return max_match['match_seq_num']

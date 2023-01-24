import asyncio
import pprint
from typing import Iterable

from loguru import logger

from app.core.finder.data import HandshakesLevel, HandshakesGraph
from app.core.requester.data import GetFriendsQuery
from app.core.requester.requester import a_get
from app.core.requester.tools import iterate_responses
from app.utils.base import get_access_token


async def get_handshakes_level(identifiers: Iterable, access_token: str):
    handshakes_level = HandshakesLevel()
    verbose_responses = await a_get(GetFriendsQuery(identifiers=identifiers, access_token=access_token))
    for friends_info, identifier in iterate_responses(verbose_responses):
        if len(friends_info['items']) > 0:
            if isinstance(friends_info['items'][0], int):
                handshakes_level.add_to_handshakes((identifier, friends_info['items']))
            else:
                handshakes_level.add_to_handshakes((identifier, [friend_info['id'] for friend_info in friends_info['items']]))
    return handshakes_level


async def find_handshakes(user_id_1: int, user_id_2: int, access_token: str, handshakes_bound: int = 3):
    handshakes_graph_1 = HandshakesGraph()
    handshakes_graph_2 = HandshakesGraph()
    visited = {user_id_1, user_id_2}
    for level in range(handshakes_bound):
        logger.info(f"handshakes level: {level}")
        if level == 0:
            next_users_1 = [user_id_1]
            next_users_2 = [user_id_2]
        else:
            next_users_1 = handshakes_graph_1.levels[-1].get_children() - visited
            next_users_2 = handshakes_graph_2.levels[-1].get_children() - visited
        handshakes_1 = await get_handshakes_level(next_users_1, access_token)
        handshakes_graph_1.add_to_levels(handshakes_1)
        common_users = None
        handshakes_graph_1_found_level = None
        handshakes_graph_2_found_level = None
        for handshake_level in handshakes_graph_2.levels:
            common_users = handshake_level.get_children().intersection(handshakes_1.get_children())
            if common_users:
                handshakes_graph_1_found_level = level
                handshakes_graph_2_found_level = handshakes_graph_2.levels.index(handshake_level)
                break
        if not common_users:
            handshakes_graph_2_found_level = level
            handshakes_2 = await get_handshakes_level(next_users_2, access_token)
            handshakes_graph_2.add_to_levels(handshakes_2)
            for handshake_level in handshakes_graph_1.levels:
                common_users = handshake_level.get_children().intersection(handshakes_2.get_children())
                if common_users:
                    handshakes_graph_1_found_level = handshakes_graph_1.levels.index(handshake_level)
                    break

        if common_users:
            answer = []
            for common_user in common_users:
                paths_1 = handshakes_graph_1.find_paths_to_child(common_user, handshakes_graph_1_found_level)
                paths_2 = handshakes_graph_2.find_paths_to_child(common_user, handshakes_graph_2_found_level)
                for path_1 in paths_1:
                    for path_2 in paths_2:
                        answer.append([*reversed(path_1), common_user, *path_2])
            return answer


def find_handshakes_2(user_id_1: int, user_id_2: int, access_token: str, level_bound: int = 3):
    graph_user_1 = HandshakesGraph()
    graph_user_2 = HandshakesGraph()
    graph_user_1.add_to_levels(HandshakesLevel(handshakes=[(None, [user_id_1])]))
    graph_user_2.add_to_levels(HandshakesLevel(handshakes=[(None, [user_id_2])]))
    visited_users = set()
    for level in range(level_bound):
        users_to_visit_1 = graph_user_1.get_level(-1).get_children() - visited_users
        visited_users.update(users_to_visit_1)

        users_to_visit_2 = graph_user_2.get_level(-1).get_children() - visited_users
        visited_users.update(users_to_visit_2)

        handshakes_level_1 = await get_handshakes_level(users_to_visit_1, access_token)
        handshakes_level_2 = await get_handshakes_level(users_to_visit_2, access_token)

        graph_user_1.add_to_levels(handshakes_level_1)
        graph_user_2.add_to_levels(handshakes_level_2)




if __name__ == "__main__":
    pass

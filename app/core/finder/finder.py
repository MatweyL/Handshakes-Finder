from typing import Iterable

from app.core.finder.data import HandshakesLevel, HandshakesGraph
from app.core.requester.data import GetFriendsQuery
from app.core.requester.requester import a_get
from app.core.requester.tools import iterate_responses


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


def get_level_common_users(graph_user_1: HandshakesGraph, graph_user_2: HandshakesGraph):
    common_users = None
    handshakes_level_index_1 = None
    handshakes_level_index_2 = None
    last_level_2 = graph_user_2.get_level(-1)
    for level_1 in graph_user_1.get_levels():
        common_users = level_1.get_children().intersection(last_level_2.get_children())
        if common_users:
            handshakes_level_index_1, handshakes_level_index_2 = level_1.level, last_level_2.level
            break
    return common_users, handshakes_level_index_1, handshakes_level_index_2


def get_common_users(graph_user_1: HandshakesGraph, graph_user_2: HandshakesGraph):
    common_users, handshakes_index_1, handshakes_index_2 = get_level_common_users(graph_user_1, graph_user_2)
    if not common_users:
        common_users, handshakes_index_1, handshakes_index_2 = get_level_common_users(graph_user_2, graph_user_1)
    return common_users, handshakes_index_1, handshakes_index_2


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

        common_users, handshakes_level_1, handshakes_level_2 = get_common_users(graph_user_1, graph_user_2)
        if common_users:
            handshakes = []
            for common_user in common_users:
                handshakes_part_1 = graph_user_1.find_paths_to_child(common_user, handshakes_level_1)
                handshakes_part_2 = graph_user_2.find_paths_to_child(common_user, handshakes_level_2)
                for handshake_part_1 in handshakes_part_1:
                    for handshake_part_2 in handshakes_part_2:
                        handshakes.append([*reversed(handshake_part_1[1:]), *handshake_part_2])
            return handshakes


if __name__ == "__main__":
    pass

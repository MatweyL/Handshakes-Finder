import asyncio
from typing import Iterable

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


async def find_handshakes(user_id_1: int, user_id_2: int, access_token: str, handshakes_level: int = 3):
    handshakes_graph_1 = HandshakesGraph()
    handshakes_graph_2 = HandshakesGraph()
    pass


if __name__ == "__main__":
    hl: HandshakesLevel = asyncio.run(get_handshakes_level([57300449, 140351546, 103162724], access_token=get_access_token()))
    for item in hl.get_handshakes():
        print(item[0], len(item[1]))
    print(len(hl.get_children()))

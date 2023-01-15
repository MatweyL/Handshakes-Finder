from dataclasses import dataclass, field
from typing import List, Tuple, Set


@dataclass
class HandshakesLevel:
    level: int = None
    handshakes: List[Tuple[int, List[int]]] = field(default_factory=list)
    children: Set[int] = field(default_factory=set)

    def add_to_handshakes(self, handshake: Tuple[int, List[int]]):
        self.handshakes.append(handshake)
        self.children.update(handshake[1])

    def get_handshakes(self) -> List[Tuple[int, List[int]]]:
        return self.handshakes

    def get_children(self) -> Set[int]:
        return self.children

    def find_parents(self, child: int) -> List[int]:
        parents = []
        for handshake in self.handshakes:
            if handshake[1][0] <= child <= handshake[1][-1] and child in handshake[1]:
                parents.append(handshake[0])
        return parents

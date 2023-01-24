from dataclasses import dataclass, field
from typing import List, Tuple, Set


@dataclass
class HandshakesLevel:
    level: int = None
    handshakes: List[Tuple[int | None, List[int]]] = field(default_factory=list)
    children: Set[int] = field(default_factory=set)

    def __post_init__(self):
        if self.handshakes and not self.children:
            for handshake in self.handshakes:
                self.children.update(handshake[1])

    def add_to_handshakes(self, handshake: Tuple[int, List[int]]):
        self.handshakes.append(handshake)
        self.children.update(handshake[1])

    def get_handshakes(self) -> List[Tuple[int, List[int]]]:
        return self.handshakes

    def get_children(self) -> Set[int]:
        return self.children

    def find_parents(self, child: int) -> List[int]:
        parents = []
        if child not in self.children:
            return parents
        for handshake in self.handshakes:
            if handshake[1][0] <= child <= handshake[1][-1] and child in handshake[1]:
                parents.append(handshake[0])
        return parents


@dataclass
class HandshakesGraph:
    levels: List[HandshakesLevel] = field(default_factory=list)

    def __post_init__(self):
        if self.levels:
            level_number = 0
            for handshake_level in self.levels:
                handshake_level.level = level_number
                level_number += 1

    def get_level(self, level: int):
        return self.levels[level]

    def get_levels(self):
        return self.levels

    def add_to_levels(self, handshakes_level: HandshakesLevel):
        if not handshakes_level.level:
            handshakes_level.level = len(self.levels)
        self.levels.append(handshakes_level)

    def find_paths_to_child(self, child: int, level: int):
        if level == 0:
            return [self.levels[level].get_handshakes()[0][1]]
        else:
            paths = []
            parents = self.levels[level].find_parents(child)
            for parent in parents:
                paths_to_child = self.find_paths_to_child(parent, level - 1)
                for path_to_child in paths_to_child:
                    paths.append([child, *path_to_child])
            return paths


if __name__ == "__main__":
    l0 = [(None, [1])]
    l1 = [(1, [2, 3])]
    l2 = [(2, [1, 4, 5, 6, 77]), (3, [1, 4, 5, 6])]
    l3 = [(4, [5, 7, 8, 10]), (5, [4, 7, 8, 9]), (6, [10, 11, 12])]
    hg = HandshakesGraph(
        levels=[HandshakesLevel(handshakes=l0), HandshakesLevel(handshakes=l1), HandshakesLevel(handshakes=l2), HandshakesLevel(handshakes=l3)]
    )
    print(hg.find_paths_to_child(1, 0))

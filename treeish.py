from typing import Iterable, Iterator, Mapping, Sequence, Tuple, Union


VERSION = "0.1.0"


LEAF_TYPES = (bool, int, float, str)
KEY_TYPES = (int, str)
BRANCH_TYPES = (Mapping, Sequence)


LT = Union[bool, int, float, str]
KT = Union[int, str]


Treeish = Union[Mapping[KT, Union["Treeish", LT]], Sequence[Union["Treeish", LT]]]
TreeishPath = Sequence[KT]


class treepath(TreeishPath):
    def __init__(self, *pathelements: KT) -> None:
        self.path = pathelements

    def __repr__(self) -> str:
        return f"treepath({', '.join(repr(el) for el in self.path)})"

    def __str__(self) -> str:
        return "".join(f"[{el!r}]" for el in self.path)

    def __add__(self, other: TreeishPath) -> "treepath":
        try:
            new = type(self)()
            new.path = self.path + tuple(other)
            return new
        except TypeError:
            raise TypeError(f"can only concatenate tuple or treepath to treepath")

    def __eq__(self, other) -> bool:
        return self.path == tuple(other)

    def __getitem__(self, key):
        return self.path[key]

    def __len__(self) -> int:
        return len(self.path)


def walk(tree: Treeish, path: treepath = None) -> Iterator[Tuple[TreeishPath, LT]]:
    if path is None:
        path = treepath()

    iterator: Iterable
    if isinstance(tree, list):
        iterator = enumerate(tree)
    elif isinstance(tree, dict):
        iterator = tree.items()
    else:
        raise TypeError(f"tree should be one of {BRANCH_TYPES}")

    for key, element in iterator:
        newpath = path + [key]
        if isinstance(element, BRANCH_TYPES):
            yield from walk(element, path=newpath)
        elif isinstance(element, LEAF_TYPES):
            yield newpath, element


def leaves(tree: Treeish) -> Iterator[LT]:
    for _, leaf in walk(tree):
        yield leaf


def paths(tree: Treeish) -> Iterator[TreeishPath]:
    for path, _ in walk(tree):
        yield path

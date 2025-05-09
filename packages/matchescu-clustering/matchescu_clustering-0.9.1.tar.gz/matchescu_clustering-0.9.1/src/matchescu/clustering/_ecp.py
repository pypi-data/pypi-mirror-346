from collections.abc import Iterable
from typing import Generic

from matchescu.similarity import ReferenceGraph

from matchescu.clustering._base import T, ClusteringAlgorithm


class EquivalenceClassPartitioner(Generic[T]):
    def __init__(self, all_refs: Iterable[T]) -> None:
        self._items = list(set(all_refs))
        self._rank = {item: 0 for item in self._items}
        self._parent = {item: item for item in self._items}

    def _find(self, x: T) -> T:
        if self._parent[x] == x:
            return x
        # path compression
        self._parent[x] = self._find(self._parent[x])
        return self._parent[x]

    def _union(self, x: T, y: T) -> None:
        x_root = self._find(x)
        y_root = self._find(y)

        if x_root == y_root:
            return

        if self._rank[x_root] < self._rank[y_root]:
            self._parent[x_root] = y_root
        elif self._rank[y_root] < self._rank[x_root]:
            self._parent[y_root] = x_root
        else:
            # does not matter which goes where
            # make sure we increase the correct rank
            self._parent[y_root] = x_root
            self._rank[x_root] += 1

    def __call__(self, pairs: Iterable[tuple[T, T]]) -> frozenset[frozenset[T]]:
        for x, y in pairs:
            self._union(x, y)
        classes = {item: dict() for item in self._items}
        for item in self._items:
            classes[self._find(item)][item] = None
        return frozenset(
            frozenset(eq_class) for eq_class in classes.values() if len(eq_class) > 0
        )


class EquivalenceClassClustering(ClusteringAlgorithm[T]):
    def __init__(self, all_refs: Iterable[T], threshold: float = 0.75) -> None:
        super().__init__(all_refs, threshold)
        self._ecp = EquivalenceClassPartitioner(self._items)

    def __call__(self, reference_graph: ReferenceGraph) -> frozenset[frozenset[T]]:
        return self._ecp(reference_graph.matches(self._threshold))

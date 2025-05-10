import logging
from dataclasses import dataclass
from typing import override

import dwave_networkx as dnx
from quark.core import Core, Data, Result
from quark.interface_types import Graph, Other, Qubo


@dataclass
class TspQuboMappingDnx(Core):
    """
    A module for mapping a graph to a QUBO formalism for the TSP problem
    """

    @override
    def preprocess(self, data: Graph) -> Result:
        # if not isinstance(data, Graph):
        #     # TODO add error message
        #     raise TypeError
        self._graph = data.as_nx_graph()
        q = dnx.traveling_salesperson_qubo(self._graph)
        return Data(Qubo.from_dict(q))

    @override
    def postprocess(self, data: Other) -> Result:
        d = data.data
        # TODO documentation why sorted?
        relevant_data = filter(lambda x: x[1] == 1, d.items())
        tuples = map(lambda x: x[0], relevant_data)
        sorted_tuples = sorted(tuples, key=lambda x: x[1])
        path = map(lambda x: x[0], sorted_tuples)
        time_steps = map(lambda x: x[1], sorted_tuples)

        if list(time_steps) != list(range(self._graph.number_of_nodes())):
            logging.warn("Invalid route")
            return Data(None)

        return Data(Other(list(path)))

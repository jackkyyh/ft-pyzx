# PyZX - Python library for quantum circuit rewriting
#        and optimization using the ZX-calculus
# Copyright (C) 2018 - Aleks Kissinger and John van de Wetering

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Any, List, Optional, TypeVar

ET = TypeVar("ET")  # Copied from `~pyzx.graph.base`. Can't do import here due to circular import.


class BaseNoiseModel:
    """Base class for noise models."""

    def __init__(self, default_noise_param=0):
        from pyzx.graph.base import BaseGraph  # Import here to avoid circular import.

        self.graph = BaseGraph()  # Placeholder for the actual graph to which the noise model is applied

        self.default_noise_param = default_noise_param  # Default noise parameter for edges
        self.noise_data_key = "_noise"  # Key for storing noise data in edge data

    def remove(self):
        """Remove noise from the graph."""
        for edge in self.graph.edges():
            self.graph.drop_edata(edge, self.noise_data_key)

    def set_edge_noise_param(self, edge: ET, param: Any) -> None:
        self.graph.set_edata(edge, self.noise_data_key, param)

    def edge_decorations(self, edge: ET) -> List[str]:
        raise NotImplementedError("This method should be implemented by subclasses.")


class EdgeFlipNoiseModel(BaseNoiseModel):
    """A simple edge flip noise model where edges can be flipped with a certain probability."""

    def __init__(self):
        super().__init__(default_noise_param=1)

    def set_idealized(self, edge: ET):
        """Set an edge to be idealized (no noise)."""
        self.set_edge_noise_param(edge, float("inf"))

    def edge_decorations(self, edge: ET) -> List[str]:
        is_idealized = self.graph.edata(edge, self.noise_data_key) == float("inf")
        return ["ideal"] if is_idealized else []

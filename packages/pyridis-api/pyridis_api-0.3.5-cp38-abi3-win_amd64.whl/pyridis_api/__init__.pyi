import pyarrow as pa

from abc import ABC, abstractmethod
from datetime import datetime

from typing import Callable, Dict, Any

class Header:
    @property
    def source_node(self) -> str:
        pass

    @property
    def source_io(self) -> str:
        pass

    @property
    def timestamp(self) -> datetime:
        pass

    @property
    def elapsed(self) -> int:
        pass

class PyDataflowMessage:
    @property
    def data(self) -> pa.Array:
        pass

    @property
    def header(self) -> Header:
        pass

class Node(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def new(self, inputs: Inputs, outputs: Outputs, queries: Queries, queryables: Queryables, config: Dict[str, Any]):
        pass

    @abstractmethod
    async def start(self):
        pass

class Inputs:
    async def with_input(self, input: str) -> Input:
        pass

class Outputs:
    async def with_output(self, output: str) -> Output:
        pass

class Queries:
    async def with_query(self, query: str) -> Query:
        pass

class Queryables:
    async def with_queryable(self, queryable: str) -> Queryable:
        pass

class Input:
    async def recv(self) -> PyDataflowMessage:
        pass

class Output:
    async def send(self, message: PyDataflowMessage):
        pass

class Query:
    async def query(self, message: PyDataflowMessage) -> PyDataflowMessage:
        pass

class Queryable:
    async def on_query(self, func: Callable[[PyDataflowMessage], pa.Array]):
        pass

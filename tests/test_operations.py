import typing

from compgraph import Graph
from compgraph.operations import Divide, Del, Evaluate, First, CountRows, UniversalReducer, Mean

table = [
    {'text': 'word', 'doc_id': 1, 'first': 100, 'second': 5},
    {'text': 'word', 'doc_id': 2, 'first': 100, 'second': 1},
    {'text': 'hello', 'doc_id': 2, 'first': 100, 'second': 20},
    {'text': 'word', 'doc_id': 1, 'first': 4, 'second': 2},
]


def test_divide() -> None:
    graph = Graph.graph_from_iter('table').map(Divide('first', 'second', 'result'))
    result = list(graph.run(table=lambda: iter(table)))
    answer = [{'doc_id': 1, 'result': 20.0, 'text': 'word'},
              {'doc_id': 2, 'result': 100.0, 'text': 'word'},
              {'doc_id': 2, 'result': 5.0, 'text': 'hello'},
              {'doc_id': 1, 'result': 2.0, 'text': 'word'}]
    assert result == answer


def test_del() -> None:
    graph = Graph.graph_from_iter('table').map(Del(['first', 'second']))
    result = list(graph.run(table=lambda: iter(table)))
    answer = [{'doc_id': 1, 'text': 'word'},
              {'doc_id': 2, 'text': 'word'},
              {'doc_id': 2, 'text': 'hello'},
              {'doc_id': 1, 'text': 'word'}]
    assert result == answer


def test_evaluate() -> None:
    def inc(x: dict[str, typing.Any]) -> typing.Any:
        return {**x, x['second']: -1}

    graph = Graph.graph_from_iter('table').map(Evaluate(inc))
    result = list(graph.run(table=lambda: iter(table)))
    answer = [{5: -1, 'doc_id': 1, 'first': 100, 'second': 5, 'text': 'word'},
              {1: -1, 'doc_id': 2, 'first': 100, 'second': 1, 'text': 'word'},
              {20: -1, 'doc_id': 2, 'first': 100, 'second': 20, 'text': 'hello'},
              {2: -1, 'doc_id': 1, 'first': 4, 'second': 2, 'text': 'word'}]
    assert result == answer


def test_first() -> None:
    graph = Graph.graph_from_iter('table').reduce(First('text'), ['doc_id'])
    result = list(graph.run(table=lambda: iter(table)))
    answer = table
    assert result == answer


def test_count_rows() -> None:
    graph = Graph.graph_from_iter('table').sort(['doc_id']).reduce(CountRows('text'), ['doc_id'])
    result = list(graph.run(table=lambda: iter(table)))
    answer = [{'doc_count': 2, 'doc_id': 1}, {'doc_count': 2, 'doc_id': 2}]
    assert result == answer


def test_universal_reducer() -> None:
    def func(x: list[typing.Any]) -> dict[str, int]:
        return {'1': 123}

    graph = Graph.graph_from_iter('table').sort(['doc_id']).reduce(UniversalReducer(func), ['doc_id'])
    result = list(graph.run(table=lambda: iter(table)))
    answer = ['1', '1']
    assert result == answer


def test_mean() -> None:
    graph = Graph.graph_from_iter('table').sort(['doc_id']).reduce(Mean('second'), ['doc_id'])
    result = list(graph.run(table=lambda: iter(table)))
    answer = [{'doc_id': 1, 'second': 3.5}, {'doc_id': 2, 'second': 10.5}]
    assert result == answer

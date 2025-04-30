from unittest.mock import MagicMock
from compgraph import Graph
from compgraph import operations as ops

table = [
    {'text': 'word', 'doc_id': 1},
    {'text': 'word', 'doc_id': 2},
    {'text': 'hello', 'doc_id': 2},
    {'text': 'word', 'doc_id': 1},
]


def test_graph_from_iter() -> None:
    graph = Graph.graph_from_iter('table')
    result = list(graph.run(table=lambda: iter(table)))
    assert result == table


def test_graph_from_file() -> None:
    parser_mock = MagicMock()
    graph = Graph.graph_from_file('test_file.txt', parser_mock)
    assert len(graph.operations) == 1
    assert graph.operations[0][0] == 'read'
    assert isinstance(graph.operations[0][1], ops.Read)
    assert graph.operations[0][1].filename == 'test_file.txt'
    assert graph.operations[0][1].parser == parser_mock


def test_map_operation() -> None:
    graph = Graph.graph_from_iter('table').map(ops.DummyMapper())
    result = list(graph.run(table=lambda: iter(table)))
    assert result == table


def test_reduce_operation() -> None:
    graph = Graph.graph_from_iter('table').sort(['doc_id']).reduce(ops.FirstReducer(), ['doc_id'])
    result = list(graph.run(table=lambda: iter(table)))
    answer = [{'doc_id': 1, 'text': 'word'}, {'doc_id': 2, 'text': 'word'}]
    assert result == answer


def test_sort_operation() -> None:
    graph = Graph.graph_from_iter('table').sort(['doc_id'])
    answer = [
        {'text': 'word', 'doc_id': 1},
        {'text': 'word', 'doc_id': 1},
        {'text': 'word', 'doc_id': 2},
        {'text': 'hello', 'doc_id': 2}
    ]
    result = list(graph.run(table=lambda: iter(table)))
    assert result == answer


def test_join_operation() -> None:
    first = [
        {'text': 'word', 'doc_id': 1},
        {'text': 'word', 'doc_id': 1},
    ]
    second = [
        {'text': 'hello', 'doc_id': 2},
        {'text': 'word', 'doc_id': 2}
    ]
    graph1 = Graph.graph_from_iter('first').sort(['doc_id'])
    graph2 = Graph.graph_from_iter('second').sort(['doc_id'])

    result = list(
        graph1.join(ops.OuterJoiner(), graph2, ['doc_id']).run(first=lambda: iter(first), second=lambda: iter(second)))
    answer = [{'doc_id': 1, 'text': 'word'},
              {'doc_id': 1, 'text': 'word'},
              {'doc_id': 2, 'text': 'hello'},
              {'doc_id': 2, 'text': 'word'}]
    assert result == answer


def test_run() -> None:
    graph = Graph.graph_from_iter('table')
    result = list(graph.run(table=lambda: iter(table)))
    assert result == table


table1 = [
    {'text': 'word', 'doc_id': 1},
    {'text': 'word', 'doc_id': 2},
    {'text': 'hello', 'doc_id': 2},
    {'text': 'word', 'doc_id': 1},
]


def test_graph_idempotence1() -> None:
    graph = Graph.graph_from_iter('table')
    result1 = list(graph.run(table=lambda: iter(table1)))
    result2 = list(graph.run(table=lambda: iter(table1)))
    assert result1 == result2 == table1


def test_graph_idempotence2() -> None:
    graph = Graph.graph_from_iter('table').map(ops.Del(['text']))
    result1 = list(graph.run(table=lambda: iter(table1)))
    result2 = list(graph.run(table=lambda: iter(table1)))
    answer = [{'doc_id': 1}, {'doc_id': 2}, {'doc_id': 2}, {'doc_id': 1}]
    assert result1 == result2 == answer


def test_graph_idempotence3() -> None:
    graph1 = Graph.graph_from_iter('table').map(ops.Del(['text']))
    graph2 = Graph.graph_from_iter('table')
    result1 = list(graph1.run(table=lambda: iter(table1)))
    result2 = list(graph2.run(table=lambda: iter(table1)))
    assert result1 != result2

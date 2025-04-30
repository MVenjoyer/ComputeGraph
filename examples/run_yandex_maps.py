import argparse
import json
import typing as tp
from compgraph.algorithms import yandex_maps_graph


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Yandex Maps graph.")
    parser.add_argument("--input_time", required=True, help="Path to the travel times file.")
    parser.add_argument("--input_length", required=True, help="Path to the road graph data file.")
    parser.add_argument("--output", required=True, help="Path to the output file.")
    args = parser.parse_args()
    graph = yandex_maps_graph(
        input_stream_name_time='time',
        input_stream_name_length='length'
    )

    def read_input(filepath: str) -> tp.Any:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                yield json.loads(line.strip())

    result = graph.run(time=lambda: read_input(args.input_time),
                       length=lambda: read_input(args.input_length))
    with open(args.output, "w", encoding="utf-8") as out:
        for row in result:
            print(row, file=out)


if __name__ == "__main__":
    main()

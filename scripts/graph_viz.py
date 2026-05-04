import os
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from graph.workflow import build_graph


def main() -> None:
    graph = build_graph()
    print(graph.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()

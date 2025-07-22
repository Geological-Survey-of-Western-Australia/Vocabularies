from pathlib import Path

import pytest
import pyshacl
from httpx import request
from rdflib import Graph


@pytest.fixture
def get_vocpub_graph() -> Graph:
    graph = Graph()
    graph.parse(Path("validation/vocpub.ttl"))
    return graph


@pytest.fixture
def get_agents_graph() -> Graph:
    graph = Graph()
    graph.parse(Path("background/agents.ttl"))
    return graph


def _get_vocab_files():
    directories = Path(".").glob("./vocabularies")
    background = Path(".").glob("./background")
    system = Path(".").glob("./system")
    files = []
    backgroundFiles = []
    systemFiles = []
    for directory in directories:
        files += directory.glob("**/*.ttl")
    for directory in background:
        backgroundFiles += directory.glob("**/*.ttl")
    for backgroundFile in backgroundFiles:
        if backgroundFile in files:
            files.remove(backgroundFile)
    for directory in system:
        systemFiles += directory.glob("**/*.ttl")
    for systemFile in systemFiles:
        if systemFile in files:
            files.remove(systemFile)
    return files


@pytest.mark.parametrize("file", _get_vocab_files())
def test_vocabs(file: Path, get_vocpub_graph: Graph, get_agents_graph: Graph):
    conforms, _, results_text = pyshacl.validate(
        data_graph=Graph().parse(file) + get_agents_graph,
        shacl_graph=get_vocpub_graph,
        allow_warnings=True,
    )

    assert conforms, f"{file} failed:\n{results_text}"

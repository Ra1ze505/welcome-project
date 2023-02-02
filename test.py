from collections import defaultdict

import pytest

from parse_and_collect_data import ParseException, parse_and_collect_data


def test_parse_and_collect_data_normal_case() -> None:
    data = [
        ("POST", "/api/v1/cluster/plugins"),
        ("GET", "/api/v1/cluster/metrics"),
    ]
    expected_output = defaultdict(
        dict, {"cluster": {"metrics": "GET", "plugins": "POST"}}
    )
    output = parse_and_collect_data(data)
    assert output == expected_output, f"Expected {expected_output}, but got {output}"


def test_parse_and_collect_data_double_call() -> None:
    first_data = [
        ("GET", "/api/v1/cluster/metrics"),
        ("POST", "/api/v1/cluster/{cluster}/plugins"),
        ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
    ]

    second_data = [
        ("GET", "/api/v1/cluster/freenodes/list"),
        ("GET", "/api/v1/cluster/nodes"),
        ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}"),
        ("POST", "/api/v1/cluster/{cluster}/plugins"),
    ]
    api_map = parse_and_collect_data(first_data)
    api_map = parse_and_collect_data(second_data, api_map)

    expected_map = defaultdict(
        dict,
        {
            "cluster": {
                "metrics": "GET",
                "plugins": "POST",
                "freenodes": {"list": "GET"},
                "nodes": "GET",
            }
        },
    )

    assert api_map == expected_map


def test_parse_and_collect_data_empty_input() -> None:
    data: list = []
    expected_output: defaultdict = defaultdict(dict)
    output = parse_and_collect_data(data)
    assert output == expected_output, f"Expected {expected_output}, but got {output}"


def test_parse_and_collect_data_conflict_case() -> None:
    data = [
        ("POST", "/api/v1/cluster/plugins"),
        ("GET", "/api/v1/cluster/plugins"),
    ]
    with pytest.raises(
        ParseException, match="Conflict at path /api/v1/cluster/plugins: POST vs GET"
    ):
        parse_and_collect_data(data)

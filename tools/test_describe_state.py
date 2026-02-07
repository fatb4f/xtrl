"""Unit tests for describe_state helpers."""

from tools.describe_state import parse_trailers


def test_parse_trailers_collects_multiple_keys() -> None:
    msg = """Subject line\n\nPacket: pkt-loop-0001\nEvidence: out/xtrl/pkt-loop-0001\nPacket: pkt-loop-0002\n"""
    trailers = parse_trailers(msg)
    assert trailers["Packet"] == ["pkt-loop-0001", "pkt-loop-0002"]
    assert trailers["Evidence"] == ["out/xtrl/pkt-loop-0001"]

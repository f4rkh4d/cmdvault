"""Tests for cmdvault.runner."""

from cmdvault.runner import find_placeholders, substitute


def test_find_placeholders():
    assert find_placeholders("ssh {{user}}@{{host}}") == ["user", "host"]
    assert find_placeholders("echo hello") == []
    assert find_placeholders("{{a}} and {{b}} and {{a}}") == ["a", "b", "a"]


def test_substitute():
    cmd = "ssh {{user}}@{{host}}"
    result = substitute(cmd, {"user": "root", "host": "10.0.0.1"})
    assert result == "ssh root@10.0.0.1"


def test_substitute_partial():
    cmd = "{{greeting}} {{name}}"
    result = substitute(cmd, {"greeting": "hello"})
    assert result == "hello {{name}}"

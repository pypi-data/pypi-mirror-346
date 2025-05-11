import pytest


pytest_plugins = ["pytester"]


def parse_tests_from_output(lines: list[str]) -> list[tuple[str, str, str]]:
    result = []
    for line in lines:
        if line.startswith("test_"):
            parts = line.split(" ")
            result.append((parts[0].split("::")[1], parts[1]))
    return result


def test_filter_works(pytester: pytest.Pytester):
    t = pytester.makepyfile(
        """
        import pytest

        pytestmark = [
            pytest.mark.skipif(match="skip")
        ]

        def test_normal():
            pass
        def test_skip():
            pass
        def test_other():
            pass
        """
    )
    result = pytester.runpytest(t, "-v")
    res = parse_tests_from_output(result.outlines)
    assert len(res) == 3
    assert res[0][0] == "test_normal" and res[0][1] == "PASSED"
    assert res[1][0] == "test_skip" and res[1][1] == "SKIPPED"
    assert res[2][0] == "test_other" and res[2][1] == "PASSED"


def test_not_filter_works(pytester: pytest.Pytester):
    t = pytester.makepyfile(
        """
        import pytest

        pytestmark = [
            pytest.mark.skipif(not_match="skip")
        ]

        def test_normal():
            pass
        def test_skip():
            pass
        def test_other():
            pass
        """
    )
    result = pytester.runpytest(t, "-v")
    res = parse_tests_from_output(result.outlines)
    assert len(res) == 3
    assert res[0][0] == "test_normal" and res[0][1] == "SKIPPED"
    assert res[1][0] == "test_skip" and res[1][1] == "PASSED"
    assert res[2][0] == "test_other" and res[2][1] == "SKIPPED"


def test_both_filters(pytester: pytest.Pytester):
    t = pytester.makepyfile(
        """
        import pytest

        pytestmark = [
            pytest.mark.skipif(match="this", not_match="thing")
        ]

        def test_this():
            pass
        def test_this_thing():
            pass
        def test_other():
            pass
        """
    )
    result = pytester.runpytest(t, "-v")
    res = parse_tests_from_output(result.outlines)
    assert len(res) == 3
    assert res[0][0] == "test_this" and res[0][1] == "SKIPPED"
    assert res[1][0] == "test_this_thing" and res[1][1] == "PASSED"
    assert res[2][0] == "test_other" and res[2][1] == "PASSED"

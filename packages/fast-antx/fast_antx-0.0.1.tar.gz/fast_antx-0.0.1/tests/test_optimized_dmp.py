import pytest

from fast_antx.utils import optimized_diff_match_patch


@pytest.fixture(scope="module")
def input_texts():
    return "Hello World.", "Goodbye World."

def test_optimized_dmp(input_texts):
    text1, text2 = input_texts
    dmp = optimized_diff_match_patch()

    diffs = dmp.diff_main(text1, text2)

    assert list(diffs) == [(-1, "Hell"), (1, "G"), (0, "o"), (1, "odbye"), (0, " World.")]

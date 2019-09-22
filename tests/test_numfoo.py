import cookiepy as py
import numpy as np


def test_numfoo():
    ones = [
        [1.0, 1.0],
        [1.0, 1.0]
    ]
    assert np.array_equal(py.numfoo(), ones)

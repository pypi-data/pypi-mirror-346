import numpy as np
import pytest
from numpy.testing import assert_allclose

from axis_batch import AxisBatch


@pytest.mark.parametrize("axis", [0, 1, 2, -1, -2, -3])
def test_main(axis: int) -> None:
    rng = np.random.default_rng(0)
    a = rng.uniform(0, 1, (10, 11, 12))
    b = AxisBatch(a, axis=0, size=3)
    for x in b:
        b.send(x * 2)
    assert_allclose(b.value, a * 2)

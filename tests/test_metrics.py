"""Evaluation statistics against hand-computed values (architecture §12.1)."""

from __future__ import annotations

import math

from evaluation.metrics import mcnemar_exact, paired_bootstrap, ratio


def test_mcnemar_exact_known_values() -> None:
    assert mcnemar_exact(0, 0) == 1.0
    # b=0, c=5: two-sided p = 2 * (1/32) = 0.0625
    assert math.isclose(mcnemar_exact(0, 5), 0.0625)
    # b=1, c=6: 2 * (1 + 7) / 128 = 0.125
    assert math.isclose(mcnemar_exact(1, 6), 0.125)
    assert mcnemar_exact(3, 3) == 1.0


def test_paired_bootstrap_is_deterministic_and_brackets_the_difference() -> None:
    x = [0.0, 0.0, 1.0, 1.0, 0.0, 1.0]
    y = [1.0, 0.0, 1.0, 1.0, 1.0, 1.0]
    a, b = paired_bootstrap(x, y), paired_bootstrap(x, y)
    assert a == b
    assert a["ci_low"] <= a["diff"] <= a["ci_high"]
    assert math.isclose(a["diff"], 2 / 6, abs_tol=1e-4)


def test_zero_denominators() -> None:
    assert ratio(0, 0)["rate"] is None
    assert paired_bootstrap([], []) == {"diff": 0.0, "ci_low": 0.0, "ci_high": 0.0}

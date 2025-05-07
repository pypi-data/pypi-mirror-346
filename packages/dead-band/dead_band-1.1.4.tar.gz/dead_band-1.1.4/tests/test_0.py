from pytest import raises

from dead_band import apply_deadband

from .payloads import input_1, input_2, output_1, output_2, output_3, output_4


def test_slow_deadband():
    assert apply_deadband(input_1, 10, 30, use_cython=False) == output_1
    assert apply_deadband([], 10, 30, use_cython=False) == []
    with raises(Exception):
        apply_deadband(input_1, 10, 30, time_unit="invalid", use_cython=False)
    with raises(Exception):
        apply_deadband(
            input_1, 10, 30, deadband_type="invalid", use_cython=False
        )
    assert (
        apply_deadband(
            input_1, 10, 30, deadband_type="percent", use_cython=False
        )
        == output_2
    )
    assert apply_deadband(input_1, 10, 30, 5, use_cython=False) == output_3
    assert (
        apply_deadband(input_1, 10, 30000, time_unit="ms", use_cython=False)
        == output_1
    )
    assert (
        apply_deadband(input_1, 10, 30000000, time_unit="us", use_cython=False)
        == output_1
    )
    assert apply_deadband(input_2, 10, 30, use_cython=False) == output_4


def test_fast_deadband():
    assert apply_deadband(input_1, 10, 30) == output_1
    assert apply_deadband([], 10, 30) == []
    with raises(Exception):
        apply_deadband(input_1, 10, 30, time_unit="invalid")
    with raises(Exception):
        apply_deadband(input_1, 10, 30, deadband_type="invalid")
    assert apply_deadband(input_1, 10, 30, deadband_type="percent") == output_2
    assert apply_deadband(input_1, 10, 30, 5) == output_3
    assert apply_deadband(input_1, 10, 30000, time_unit="ms") == output_1
    assert apply_deadband(input_1, 10, 30000000, time_unit="us") == output_1
    assert apply_deadband(input_2, 10, 30) == output_4

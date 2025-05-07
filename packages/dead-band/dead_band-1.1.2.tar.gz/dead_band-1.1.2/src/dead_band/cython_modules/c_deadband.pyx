# cython: language_level=3
from datetime import datetime
from typing import List, Optional, Tuple, Union

import cython

from cpython.datetime cimport PyDateTime_IMPORT

# Necessário para trabalhar com datetime em Cython
PyDateTime_IMPORT

@cython.boundscheck(False)
@cython.wraparound(False)
def apply_c_deadband(
    series: List[Union[Tuple[float, datetime], Tuple[float, datetime, int]]],
    deadband_value: float,
    max_time_interval: float,
    min_time_interval: float = 0,
    time_unit: str = "s",
    deadband_type: str = "abs",
    save_on_quality_change: bool = True
) -> List[Union[Tuple[float, datetime], Tuple[float, datetime, int]]]:
    """
    Optimized Cython version of deadband filter for time series data.
    """
    if not series:
        return []

    # Convert time units once
    cdef double multiplier
    if time_unit == "s":
        multiplier = 1_000_000.0
    elif time_unit == "ms":
        multiplier = 1_000.0
    elif time_unit == "us":
        multiplier = 1.0
    else:
        raise ValueError("time_unit must be 's', 'ms', or 'us'")

    cdef double min_time_interval_us = min_time_interval * multiplier
    cdef double max_time_interval_us = max_time_interval * multiplier

    # Pre-define variables for performance
    cdef double time_delta_us, variation, current_value, last_value
    cdef bint has_quality, quality_changed
    cdef int last_quality, current_quality
    cdef object last_timestamp, current_timestamp  # Usando object para datetime
    
    # Determine deadband calculation function
    if deadband_type == "abs":
        def calc_variation(double current, double last):
            return abs(current - last)
    elif deadband_type == "percent":
        def calc_variation(double current, double last):
            if last != 0:
                return abs(current - last) / abs(last) * 100.0
            return abs(current)
    else:
        raise ValueError("deadband_type must be 'abs' or 'percent'")

    has_quality = len(series[0]) == 3

    if not has_quality:
        filtered_series = [series[0]]
        last_value, last_timestamp = series[0]

        for point in series[1:]:
            current_value, current_timestamp = point
            time_delta_us = (current_timestamp - last_timestamp).total_seconds() * 1_000_000.0

            if time_delta_us >= min_time_interval_us:
                variation = calc_variation(current_value, last_value)
                if variation > deadband_value or time_delta_us >= max_time_interval_us:
                    filtered_series.append(point)
                    last_value, last_timestamp = current_value, current_timestamp
        return filtered_series

    # With quality handling
    filtered_series = [series[0]]
    last_value, last_timestamp, last_quality = series[0]

    for point in series[1:]:
        current_value, current_timestamp, current_quality = point
        time_delta_us = (current_timestamp - last_timestamp).total_seconds() * 1_000_000.0

        if time_delta_us < min_time_interval_us:
            continue

        if save_on_quality_change and current_quality != last_quality:
            filtered_series.append(point)
            last_value, last_timestamp, last_quality = current_value, current_timestamp, current_quality
            continue

        variation = calc_variation(current_value, last_value)
        if variation > deadband_value or time_delta_us >= max_time_interval_us:
            filtered_series.append(point)
            last_value, last_timestamp, last_quality = current_value, current_timestamp, current_quality

    return filtered_series
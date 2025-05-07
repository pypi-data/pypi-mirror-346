from .cython_modules.c_deadband import apply_c_deadband  # type: ignore


def apply_deadband(
    series,
    deadband_value,
    max_time_interval,
    min_time_interval=0,
    time_unit="s",
    deadband_type="abs",
    save_on_quality_change=True,
    use_cython=True,
):
    """
    Applies a deadband filter to a time series, considering value variation, time intervals (in selectable units), and optional quality changes.

    Args:
        series (list): List of tuples (value: float, timestamp: datetime.datetime, quality: Optional[int]). Quality can be omitted (value, timestamp) or included (value, timestamp, quality).
        deadband_value (float): Deadband threshold (absolute value or percentage, depending on deadband_type).
        max_time_interval (float): Maximum time interval (unit defined by time_unit) to force saving a new point.
        min_time_interval (float): Minimum time interval (unit defined by time_unit) to allow saving a new point even with small variation. Default is 0.
        time_unit (str): Unit for time intervals: 's' (seconds), 'ms' (milliseconds), or 'us' (microseconds). Default is 's'.
        deadband_type (str): 'abs' for absolute deadband or 'percent' for percentage-based deadband. Default is 'abs'.
        save_on_quality_change (bool): If True, saves a point whenever the quality changes compared to the last saved point. Only used when quality is provided in the series. Default is True.
        use_cython (bool): If True, uses the Cython implementation for performance. Default is True.

    Returns:
        list: New list of tuples with the same structure as input (with or without quality) after applying the deadband filter.
    """  # noqa: E501
    if use_cython:
        return apply_c_deadband(
            series,
            deadband_value,
            max_time_interval,
            min_time_interval,
            time_unit,
            deadband_type,
            save_on_quality_change,
        )

    if not series:
        return []

    # Convert time units once
    if time_unit == "s":
        multiplier = 1_000_000
    elif time_unit == "ms":
        multiplier = 1_000
    elif time_unit == "us":
        multiplier = 1
    else:
        raise ValueError("time_unit must be 's', 'ms', or 'us'")

    min_time_interval_us = min_time_interval * multiplier
    max_time_interval_us = max_time_interval * multiplier

    if deadband_type == "abs":

        def calc_variation(current, last):
            return abs(current - last)

    elif deadband_type == "percent":

        def calc_variation(current, last):
            return (
                abs(current - last) / abs(last) * 100
                if last != 0
                else abs(current)
            )

    else:
        raise ValueError("deadband_type must be 'abs' or 'percent'")

    has_quality = len(series[0]) == 3

    if not has_quality:
        filtered_series = [series[0]]
        last_value, last_timestamp = series[0]

        for point in series[1:]:
            value, timestamp = point
            time_delta_us = (
                timestamp - last_timestamp
            ).total_seconds() * 1_000_000

            if time_delta_us >= min_time_interval_us:
                variation = calc_variation(value, last_value)
                if (
                    variation > deadband_value
                    or time_delta_us >= max_time_interval_us
                ):
                    filtered_series.append(point)
                    last_value, last_timestamp = value, timestamp
        return filtered_series

    filtered_series = [series[0]]
    last_value, last_timestamp, last_quality = series[0]

    for point in series[1:]:
        value, timestamp, quality = point
        time_delta_us = (
            timestamp - last_timestamp
        ).total_seconds() * 1_000_000

        if time_delta_us < min_time_interval_us:
            continue

        if save_on_quality_change and quality != last_quality:
            filtered_series.append(point)
            last_value, last_timestamp, last_quality = (
                value,
                timestamp,
                quality,
            )
            continue

        variation = calc_variation(value, last_value)
        if variation > deadband_value or time_delta_us >= max_time_interval_us:
            filtered_series.append(point)
            last_value, last_timestamp, last_quality = (
                value,
                timestamp,
                quality,
            )

    return filtered_series

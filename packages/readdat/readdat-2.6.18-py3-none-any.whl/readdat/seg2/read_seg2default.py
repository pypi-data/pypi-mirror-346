from typing import List
import warnings
import parse
import obspy
import numpy as np
from obspy.core import Trace, Stream, UTCDateTime
import datetime


def is_seg2_written_by_readdat(stream: Stream) -> bool:
    """
    determines whether a stream was written by readdat or not
    :return answer: True or False
    """

    assert isinstance(stream, obspy.core.stream.Stream), TypeError(type(stream))

    try:
        # hasattr is hazardous
        stream.stats["seg2"]

    except (AttributeError, KeyError):
        # probably not even a seg2 file
        return False

    try:
        stream.stats.seg2['NOTE']

        # search in the notes at the stream level
        stream_notes: List[str] = stream.stats.seg2['NOTE']

        for note in stream_notes:
            if "WRITTEN_BY_READDAT" in note:
                return True
    except (AttributeError, KeyError):
        return False

    return False


def extract_receiver_location(trace: Trace) -> None:
    try:
        receiver_location = trace.stats.seg2['RECEIVER_LOCATION']
        receiver_x, receiver_y, receiver_z = receiver_location.split()

        # unpack string as 3 floats (x, y, z in meters)
        trace.stats.receiver_x = float(receiver_x)
        trace.stats.receiver_y = float(receiver_y)
        trace.stats.receiver_z = float(receiver_z)

    except (KeyError, ValueError) as err:
        warnings.warn(str(err))


def extract_source_location(trace: Trace) -> None:
    try:
        source_location = trace.stats.seg2['SOURCE_LOCATION']
        source_x = source_location

        trace.stats.source_x = float(source_x)

    except (KeyError, ValueError) as err:
        warnings.warn(str(err))


def extract_temp_rh(trace: obspy.Trace) -> None:
    """
    Extract temperature and relative humidity from the trace notes if present
    """
    temperature_format = "TEMPE_C {temperature_degc:e}"
    relative_humidity_format = "RH_% {relative_humidity_percent:e}"

    temperature_degc = np.nan
    relative_humidity_percent = np.nan

    try:
        trace.stats.seg2['NOTE']
    except (AttributeError, KeyError):
        trace.stats['temperature_degc'] = temperature_degc
        trace.stats['relative_humidity_percent'] = relative_humidity_percent
        return

    for field in trace.stats.seg2['NOTE']:
        if field.startswith('TEMPE_C'):
            temperature_degc_ = parse.parse(temperature_format, field)
            if temperature_degc_ is None:
                raise ValueError(f'could not parse {field=} into {temperature_format=}')
            temperature_degc = temperature_degc_["temperature_degc"]
            break
    else:
        # temperature field not found
        pass

    for field in trace.stats.seg2['NOTE']:
        if field.startswith('RH_%'):
            relative_humidity_percent_ = parse.parse(relative_humidity_format, field)
            if relative_humidity_percent_ is None:
                raise ValueError(f'could not parse {field=} into {relative_humidity_format=}')
            relative_humidity_percent = relative_humidity_percent_['relative_humidity_percent']
            break
    else:
        # relative_humidity field not found
        pass

    trace.stats['temperature_degc'] = temperature_degc
    trace.stats['relative_humidity_percent'] = relative_humidity_percent


def default_to_seg2obspy(stream: obspy.core.stream.Stream, verbose: bool=True) \
        -> obspy.core.stream.Stream:

    for trace in stream:

        # coordinates
        extract_receiver_location(trace=trace)
        extract_source_location(trace=trace)

        # Temperature / Relative humidity
        extract_temp_rh(trace=trace)

    return stream

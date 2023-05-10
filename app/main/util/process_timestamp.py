import datetime

from app.main.custom_exceptions import ConvertingTimestampError


def process_timestamp_dual_string(timestamp: str):
    """
    Process a timestamp string into a tuple of datetime objects.
    """
    if len(timestamp.split('/')) != 2:
        raise ConvertingTimestampError('Timestamp must be a string with two elements separated by a /, use .. for '
                                       'open ranges')
    start_timestamp = timestamp.split('/')[0]
    end_timestamp = timestamp.split('/')[1]
    potential_timestamp_formats = ['%Y-%m-%dT%H:%M:%S%Z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z',
                                   '%Y-%m-%dT%H:%M:%S.%f']
    start_timestamp_datetime = None
    end_timestamp_datetime = None
    if start_timestamp is not None and start_timestamp != '..':
        for fmt in potential_timestamp_formats:
            try:
                start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, fmt)
                break
            except ValueError:
                continue
        if start_timestamp_datetime is None:
            raise ConvertingTimestampError
    if end_timestamp is not None and end_timestamp != '..':
        for fmt in potential_timestamp_formats:
            try:
                end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, fmt)
                break
            except ValueError:
                continue
        if end_timestamp_datetime is None:
            raise ConvertingTimestampError
    return start_timestamp_datetime, end_timestamp_datetime


def process_timestamp_single_string(timestamp: str) -> datetime:
    """
    Process a timestamp string into a datetime object.
    """
    potential_timestamp_formats = ['%Y-%m-%dT%H:%M:%S%Z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z',
                                   '%Y-%m-%dT%H:%M:%S.%f']
    timestamp_datetime = None
    if timestamp is not None and timestamp != '..':
        for fmt in potential_timestamp_formats:
            try:
                timestamp_datetime = datetime.datetime.strptime(timestamp, fmt)
                break
            except ValueError:
                continue
        if timestamp_datetime is None:
            print(timestamp)
            raise ConvertingTimestampError
    return timestamp_datetime

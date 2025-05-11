from datetime import datetime, date


def meta_handler(obj):
    """Datetime Handlers (TODO: Have Converters for Various SQL Variants)

    Parameters
    ----------
    obj : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    if isinstance(obj, (datetime, date)):
        return obj.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    if isinstance(obj, None):
        return None

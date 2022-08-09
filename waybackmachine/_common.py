
from datetime import datetime, date, timedelta

def parse_datetime(dt):
    if dt is None:
        return None
    elif isinstance(dt, datetime):
        return dt
    elif isinstance(dt, date):
        return datetime(dt.year, dt.month, dt.day)
    elif isinstance(dt, str):
        for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"]:
            try:
                dt = datetime.strptime(dt, fmt)
                return dt
            except:
                pass
        else:
            raise ValueError("invalid input date string format")
    else:
        raise TypeError("invalid input date type")

def parse_timedelta(td):
	if isinstance(td, timedelta):
		return td
	elif isinstance(td, str):
		raise NotImplementedError('string timedelta is planned to be added')
	elif isinstance(td, float) or isinstance(td, int):
		return timedelta(days = td)
	else:
		raise TypeError("invalid input timedelta type")
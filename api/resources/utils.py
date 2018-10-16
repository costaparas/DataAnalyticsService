from datetime import datetime
def release_date_to_datetime(release_date_str):
    try:
        dt = datetime.strptime(release_date_str,"%d %b %Y")
        return dt
    except ValueError:
        return datetime(year=1000,month=1,day=1)

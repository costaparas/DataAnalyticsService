from datetime import datetime
def release_date_to_datetime(release_date_str):
    dt = datetime.strptime(release_date_str,"%d %b %Y")
    return dt
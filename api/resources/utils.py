from datetime import datetime
def release_date_and_year_strings_to_datetime(release_date_str, year_str):
    """

    :param release_date_str: Example : "12 Oct 2006"
    :param year_str: Example: "1951"
    :return: release_date_str as a datetime if its a valid date, otherwise try parsing year_str and returning January 1st for that year. If both are invalid (i.e. "N/A"), then return a default datetime value.
    """
    return None
def release_date_to_datetime(release_date_str):
    try:
        dt = datetime.strptime(release_date_str,"%d %b %Y")
        return dt
    except ValueError:
        return datetime(year=1000,month=1,day=1)

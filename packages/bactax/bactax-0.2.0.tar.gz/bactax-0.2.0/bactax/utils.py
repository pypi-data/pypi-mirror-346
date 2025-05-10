from typing import Optional
from importlib import resources
import re
from datetime import date, timedelta
from pathlib import Path


def get_taxonomy_data_filepath() -> Optional[Path]:
    """
    Gets the filepath to the gzip taxonomy file (if there is one downloaded).
    """
    pattern = re.compile(r"^taxonomy_\d{4}-\d{2}-\d{2}\.csv\.gz$")
    for file in resources.files(__package__).iterdir():
        if pattern.match(file.name):
            return file
    return None


def new_taxonomy_data_filepath() -> Path:
    """
    Generates a name for the gzip taxonomy file based on today's date.
    """
    return resources.files(__package__) / f"taxonomy_{date.today()}.csv.gz"


def last_taxonomy_update() -> Optional[date]:
    """
    Gets the date from the filename of the currently downloaded taxonomy file.
    """
    taxonomy_file = get_taxonomy_data_filepath()

    if taxonomy_file is None:
        return None

    date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})")
    return date.fromisoformat(
        date_pattern.findall(str(taxonomy_file))[-1]
    )  # Get last match in case there is a date somewhere earlier in the filepath


def time_since_last_taxonomy_update() -> Optional[timedelta]:
    """
    Calculates how long it has been since the last taxonomy update.

    Returns
    -------
    timedelta | None
        Returns a `datetime.timedelta` object with the time since the
        last taxonomy update, or `None` if no taxonomy data has
        been downloaded.
    """
    last_update = last_taxonomy_update()
    if last_update is None:
        return None
    return date.today() - last_update

from os.path import join
from os.path import normpath

from .constants import MIXDB_NAME
from .constants import TEST_MIXDB_NAME


def db_file(location: str, test: bool = False) -> str:
    name = TEST_MIXDB_NAME if test else MIXDB_NAME
    return normpath(join(location, name))

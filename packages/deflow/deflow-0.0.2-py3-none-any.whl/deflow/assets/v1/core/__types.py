import re
from re import (
    IGNORECASE,
    UNICODE,
    VERBOSE,
    Pattern,
)


class Re:
    __group_regex: str = r"""
        (?P<name>\w+)(?:\.(?P<tier>\w+))?(?:\.(?P<priority>\d+))
    """
    RE_GROUP: Pattern = re.compile(
        __group_regex, IGNORECASE | UNICODE | VERBOSE
    )

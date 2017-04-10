# -*- encoding: utf-8 -*-
"""
All exceptions used in LogMeIn API derives from `APIError`
"""


class APIError(Exception):
    """Base LogMeIn API exception, all specific exceptions inherits from it."""
    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response', None)
        super(APIError, self).__init__(*args, **kwargs)

    def __str__(self):
        return super(APIError, self).__str__()

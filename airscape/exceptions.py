""" Airscape Fan Exceptions.

These are exceptions that are throw as a result 
of a caught exception from the requests class.
These exceptions boil down all the possible exceptions
from the requests class.
"""


class AirscapeException(IOError):
    """There was an ambiguous exception that occurred while handling your
    request.
    """

    def __init__(self, *args, **kwargs):
        """Initialize ModernFormsException with `request` and `response` objects."""
        response = kwargs.pop('response', None)
        self.response = response
        self.request = kwargs.pop('request', None)
        if (response is not None and not self.request and
                hasattr(response, 'request')):
            self.request = self.response.request
        super(AirscapeException, self).__init__(*args, **kwargs)


class ConnectionError(AirscapeException):
    """A Connection error occurred."""

class Timeout(AirscapeException):
    """The request timed out."""

class JSONDecoderError(AirscapeException):
    """An error in the JSON return"""
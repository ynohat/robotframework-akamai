from .RequestsKeywords import RequestsKeywords
from .CacheKeyKeywords import CacheKeyKeywords
from .ExtractedValuesKeywords import ExtractedValuesKeywords
from .version import VERSION

# Avoid Python http error when response contains more than 100 headers.
# This is common when using Pragma: akamai-x-get-extracted-values.
import http.client as httplib
httplib._MAXHEADERS = 10000

class AkamaiLibrary(RequestsKeywords,
                    ExtractedValuesKeywords,
                    CacheKeyKeywords,
                    ):
    __doc__ = """
    Provides RobotFramework keywords for testing Akamai.

    == Requests ==

    {RequestsKeywords}

    == Cache Key ==

    {CacheKeyKeywords}

    == Extracted Values ==

    {ExtractedValuesKeywords}
    """.format(
      RequestsKeywords=RequestsKeywords.__doc__,
      CacheKeyKeywords=CacheKeyKeywords.__doc__,
      ExtractedValuesKeywords=ExtractedValuesKeywords.__doc__,
    )

    __version__ = VERSION
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

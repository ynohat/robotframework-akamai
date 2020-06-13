from robot.libraries.BuiltIn import BuiltIn
from .builtinMethods import builtin_method_names

class ExtractedValuesKeywords:
    __doc__ = """
    When ``Pragma: akamai-x-get-extracted-values`` is in the request, the server
    will include ``x-akamai-session-info`` headers in the response.
    
    These are formatted as key/value pairs:

    ``x-akamai-session-info: name=TCP_OPT_APPLIED; value=medium``

    ``[#Get Extracted Value|Get Extracted Value]`` returns the value of a given parameter.

    Additionally, the following comparisons are available:

    - {Comparisons}

    In some cases, an extra field is present:

    ``x-akamai-session-info: name=X; value=Y; full_location_id=Z``

    There are no keywords provided for testing the value of full_location_id.
    """.format(Comparisons="\n- ".join(list(("Extracted Value %s" % meth.replace("_", " ")).title() for meth in builtin_method_names)))

    def get_extracted_value(self, resp, name):
        """
        This keyword retrieves the value of a specific extracted value, or ``None``.

        Examples:
        | Get Extracted Value | TCP_OPT_APPLIED |
        """
        ev = ExtractedValuesKeywords._parse(resp.headers.get("x-akamai-session-info"))
        return ev.get(name, None)

    @staticmethod
    def _parse(ev):
        """
        Returns a dict of extracted values.
        """
        def enforce_pair(p): return p if len(
            p) == 2 else p[0:2] if len(p) > 2 else (p[0], None)

        def parse_pair_item(s): return s.split("=").pop()
        def parse_pair(s): return enforce_pair(
            tuple(parse_pair_item(pi) for pi in s.split("; ")[0:2]))
        return dict((parse_pair(s) for s in ev.split(", ")))

# given a BuiltIn method name, returns a name value tuple specializing it
# for this component of the cache key, e.g.:
# ("cpcode_should_be_equal", <implementation>)
def _create_method(name):
    builtIn = BuiltIn()
    builtInImpl = getattr(builtIn, name)
    impl = lambda self, resp, name, expected, *args, **kwargs: builtInImpl(self.get_extracted_value(resp, name), expected, *args, **kwargs)
    impl.__doc__ = """
    Extracts the value from the response ``${resp}`` and applies the ``%s`` comparison from BuiltIns.
    
    %s
    """ % (name.replace("_", " "), getattr(builtIn, name).__doc__)
    return ("extracted_value_%s" % (name), impl)

for builtin_method_name in builtin_method_names:
    setattr(ExtractedValuesKeywords, *_create_method(builtin_method_name))

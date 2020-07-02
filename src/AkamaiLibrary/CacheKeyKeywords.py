from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import not_keyword
from .builtinMethods import builtin_method_names

class CacheKeyKeywords:
    __doc__ = """
    Convenience keywords for testing the value of the ``x-cache-key`` header.

    === Accessors ===

    - ``[#Get Cache Key|Get Cache Key]``
    - ``[#Get Cache Key Serial|Get Cache Key Serial]``
    - ``[#Get Cache Key Typecode|Get Cache Key Typecode]``
    - ``[#Get Cache Key CPCode|Get Cache Key CPCode]``
    - ``[#Get Cache Key TTL|Get Cache Key TTL]``
    - ``[#Get Cache Key Hostname|Get Cache Key Hostname]``
    - ``[#Get Cache Key Path|Get Cache Key Path]``
    - ``[#Get Cache Id|Get Cache Id]``

    === Comparisons ===

    For the cache key, or for any of the components, provides keywords for
    comparing them to other values. These extract the component from the cache
    key, and apply the corresponding [https://robotframework.org/robotframework/latest/libraries/BuiltIn.html|BuiltIn] keyword.

    The full list of comparisons implemented is:

    - {Comparisons}

    Examples:
    | Cache Key CPCode Should Be | ${{resp}} | 123456 |
    | Cache Key Path Should Match | ${{resp}} | /assets/* |
    | Cache Key Hostname Should Match Regexp | ${{resp}} | [^.]\.acme\.org |

    """.format(Comparisons="\n- ".join(list(("Cache Key <Component> %s" % meth.replace("_", " ")).title() for meth in builtin_method_names)))

    def get_cache_key(self, resp):
        """
        Retrieves the value of the X-Cache-Key header from the response.
        """
        return resp.headers.get("x-cache-key")

    @not_keyword
    def get_cache_key_(self, resp):
        return self.get_cache_key(resp)

    def is_secure_network_delivery(self, resp):
        """
        The first component of the cache key will be "S" if the traffic
        was served over the Akamai secure network. 
        """
        ck = self.get_cache_key(resp)
        return ck.split("/")[0] == "S"

    def get_cache_key_typecode(self, resp):
        """
        The typecode is the second component of the ARL.
        """
        ck = self.get_cache_key(resp)
        return ck.split("/")[1]

    def get_cache_key_serial(self, resp):
        ck = self.get_cache_key(resp)
        return ck.split("/")[2]

    def get_cache_key_cpcode(self, resp):
        ck = self.get_cache_key(resp)
        return ck.split("/")[3]

    def get_cache_key_ttl(self, resp):
        ck = self.get_cache_key(resp)
        return ck.split("/")[4]

    def get_cache_key_hostname(self, resp):
        ck = self.get_cache_key(resp)
        return ck.split("/")[5]

    def get_cache_key_path(self, resp):
        ck = self.get_cache_key(resp)
        return "/" + "/".join(ck.split("/")[6:])

    def get_cache_id(self, resp):
        """
        Returns the contents of the Flexible Cache Id, depending
        on the scenario:

        | **Scenario**                   | **Return value**  |
        | Enabled, ``?lang`` in cache id | "lang=eng-us"     |
        | Enabled, nothing in cache id   | "__"              |
        | Disabled                       | None              |
        """
        try:
            ck = self.get_cache_key(resp)
            if "cid=" in ck:
                return ck.split("cid=")[1]
            return None
        except:
            return None # default value for the 'cid='

_components = (
    # (component name, accessor, prefix)
    ("", CacheKeyKeywords.get_cache_key, "cache_key"),
    ("serial", CacheKeyKeywords.get_cache_key_serial, "cache_key_serial"),
    ("typecode", CacheKeyKeywords.get_cache_key_typecode, "cache_key_typecode"),
    ("cpcode", CacheKeyKeywords.get_cache_key_cpcode, "cache_key_cpcode"),
    ("ttl", CacheKeyKeywords.get_cache_key_ttl, "cache_key_ttl"),
    ("hostname", CacheKeyKeywords.get_cache_key_hostname, "cache_key_hostname"),
    ("path", CacheKeyKeywords.get_cache_key_path, "cache_key_path"),
    ("cache_id", CacheKeyKeywords.get_cache_id, "cache_id")
)

_builtIn = BuiltIn()
def _create_cache_key_component_keyword(component, accessor, kw):
    _impl = getattr(_builtIn, kw)
    impl = lambda self, resp, expected, *args, **kwargs: _impl(accessor(self, resp), expected, *args, **kwargs)
    impl.__doc__ = """
    Extracts the %s component of the cache key from the response ``${resp}`` applies the ``%s`` comparison from BuiltIns.
    
    %s
    """ % (component.replace("_", " ").title(), kw.replace("_", " ").title(), _impl.__doc__)
    return impl

for (component, accessor, prefix) in _components:
    for kw in builtin_method_names:
        real_kw = _create_cache_key_component_keyword(component, accessor, kw)
        setattr(CacheKeyKeywords, "%s_%s" % (prefix, kw), real_kw)

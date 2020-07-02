from RequestsLibrary import RequestsLibrary
from .pragmas import DEFAULT_PRAGMAS
from robot.libraries.BuiltIn import BuiltIn
from .builtinMethods import builtin_method_names

class RequestsKeywords(RequestsLibrary):
    __doc__ = """
    Extends the RequestsLibrary, making all of its keywords available without needing to
    import them explicitly. Their functionality is unchanged.

    The following are added for convenience:

    - ``[#Set Session Pragma Header|Set Session Pragma Header]``
    - ``[#Set Session Header|Set Session Header]``
    - ``[#Unset Session Header|Unset Session Header]``
    - ``[#Set Session Cookie|Set Session Cookie]``
    - ``[#Unset Session Cookie|Unset Session Cookie]``
    """

    def set_session_header(self, session, name, value):
        """
        Shortcut to add a header to all subsequent requests made over the session.

        Examples:
        | Set Session Header | session | Authorization | Basic xyz |
        """
        self.update_session(session, headers={name: value})

    def unset_session_header(self, session, name):
        """
        Removes a header from all subsequent requests made over the session.

        Examples:
        | Set Session Header | session | Authorization |
        """
        self.set_session_header(session, name, None)

    def set_session_cookie(self, session, name, value):
        """
        Shortcut to add a cookie to all subsequent requests made over the session.

        Examples:
        | Set Session Cookie | session | SESSIONID | xyz |
        """
        if value is None:
            self.unset_session_cookie(session, name)
        else:
            self.update_session(session, cookies={name: value})

    def unset_session_cookie(self, session, name):
        """
        Removes a cookie from all subsequent requests made over the session.

        Examples:
        | Unset Session Cookie | session | SESSIONID |
        """
        session = self._cache.switch(session)
        for cookie_in_jar in session.cookies:
            if cookie_in_jar.name == name:
                session.cookies.clear(cookie_in_jar.domain, cookie_in_jar.path, cookie_in_jar.name)

    def set_session_pragma_header(self, session, *pragmas):
        """
        Add pragma headers to the session.

        Specific pragmas can be added by listing them explicitly.
        If omitted, the default set of pragmas will be used.

        {DEFAULT_PRAGMAS}

        Examples:
        | Set Session Pragma Header | session | akamai-x-get-request-id | akamai-x-get-cache-key |
        | Set Session Pragma Header | session |
        """
        if len(pragmas) == 0:
            pragmas = DEFAULT_PRAGMAS
        self.set_session_header(session, "pragma", ",".join(pragmas))

    def log_headers(self, resp):
        return BuiltIn().log("\n".join(
            "%s: %s" % (k, v)
            for (k, v) in resp.headers.items()
        ))

_builtIn = BuiltIn()
def _create_header_keyword(method):
    _impl = getattr(_builtIn, method)
    impl = lambda self, resp, hdr, expected, *args, **kwargs: _impl(resp.headers.get(hdr, None), expected, *args, **kwargs)
    impl.__doc__ = """
    Extracts a response header from ``${resp}`` and applies the ``%s`` comparison from BuiltIns.

    %s
    """ % (method.replace("_", " ").title(), _impl.__doc__)
    return impl

for method in builtin_method_names:
    name = "header_%s" % method
    pretty_name = name.replace("_", " ").title()
    RequestsKeywords.__doc__ += "    - ``[#%s|%s]``\n" % (
        pretty_name,
        pretty_name
    )
    setattr(RequestsKeywords, name, _create_header_keyword(method))

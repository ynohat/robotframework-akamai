from RequestsLibrary import RequestsLibrary
from .pragmas import DEFAULT_PRAGMAS

# Avoid Python http error when response contains more than 100 headers.
# This is common when using Pragma: akamai-x-get-extracted-values.
import http.client as httplib
httplib._MAXHEADERS = 10000

class RequestsKeywords(RequestsLibrary):
    """
    Extends the RequestsLibrary, making all of its keywords available without needing to
    import them explicitly. Their functionality is unchanged.

    Additionally, provides the following convenience keywords:

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
        self.update_session(session, cookies={name: value})

    def unset_session_cookie(self, session, name):
        """
        Removes a cookie from all subsequent requests made over the session.

        Examples:
        | Set Session Cookie | session | SESSIONID |
        """
        self.set_session_cookie(session, name, None)

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

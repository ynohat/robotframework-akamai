from RequestsLibrary import RequestsLibrary

# Avoid Python http error when response contains more than 100 headers.
# This is common when using Pragma: akamai-x-get-extracted-values.
import http.client as httplib
httplib._MAXHEADERS = 10000

class RequestsKeywords(RequestsLibrary):
    """
    Extends the RequestsLibrary, making all of its keywords available without needing to
    import them explicitly. Their functionality is unchanged.

    Additionally, provides the following convenience keywords:

    - ``[#Set Session Header|Set Session Header]``
    - ``[#Unset Session Header|Unset Session Header]``
    - ``[#Set Session Cookie|Set Session Cookie]``
    - ``[#Unset Session Cookie|Unset Session Cookie]``
    """

    def set_session_header(self, session, name, value):
        """
        Shortcut to add a header to all subsequent requests made over the session.

        Examples:
        | Set Session Header | Authorization | Basic xyz |
        """
        self.update_session(session, headers={name: value})

    def unset_session_header(self, session, name):
        """
        Removes a header from all subsequent requests made over the session.

        Examples:
        | Set Session Header | Authorization |
        """
        self.set_session_header(session, name, None)

    def set_session_cookie(self, session, name, value):
        """
        Shortcut to add a cookie to all subsequent requests made over the session.

        Examples:
        | Set Session Cookie | SESSIONID | xyz |
        """
        self.update_session(session, cookies={name: value})

    def unset_session_cookie(self, session, name):
        """
        Removes a cookie from all subsequent requests made over the session.

        Examples:
        | Set Session Cookie | SESSIONID |
        """
        self.set_session_cookie(session, name, None)

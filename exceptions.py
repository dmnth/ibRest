#! /usr/bin/env python3

class NotLoggedIn(Exception):
    # Is triggered if user is unauthenticated 
    # Either was not logged in or session timed out
    pass

class Unauthorized(Exception):
    pass

class NotAuthenticated(Exception):
    # Is triggered on occasion when there is a TWS or IBGateway session running
    # Or if the previous session was not properly exited by logging out of the 
    # TWS or calling /logout endpoint.
    pass

class CompetingSessionException(Exception):
    # is raised if there is a competing session running. Only one session
    # is allowed per username
    pass

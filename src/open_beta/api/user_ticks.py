import os
from base import open_beta_request

def fetch_user_ticks(username=os.getenv('OB_USERNAME')):
    return open_beta_request(user_tick_query(username))

def user_tick_query(username):
    return """
    query UserTicksQuery {
      userTicks(username: "%s") {
        _id
        userId
        name
        notes
        climbId
        style
        attemptType
        dateClimbed
        grade
        source
      }
    }
    """ % username
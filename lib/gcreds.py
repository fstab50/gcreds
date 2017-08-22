"""
gcreds Module

Args:

Returns:

"""

import os
import json
import argparse
import boto3
from botocore.exceptions import ClientError


class gcreds():
    """
    Parse environment variables, validate characters, convert type(s). default
    should be used to avoid conversion of an variable and retain string type

    Example usage:

    >>> from lambda_utils import read_env_variable
    >>> os.environ['DBUGMODE'] = 'True'
    >>> myvar = read_env_variable('DBUGMODE')
    >>> type(myvar)
    True

    >>> from lambda_utils import read_env_variable
    >>> os.environ['MYVAR'] = '1345'
    >>> myvar = read_env_variable('MYVAR', 'default')
    >>> type(myvar)
    str
    """
    def __init__(self):
        """ initalization
        Args:
            - checks deps, existence of creds, existence of Settings

        Returns:

        """

    def help_menu(self):
        """ displays gcreds help menu, options """

    def get_session_token(self, iam_user, code):
        """ generates session token for use in gen temp credentials """


    def generate_credentials(self, iam_user, roles):


    def calc_time(self):
        """ remaining time left in session and credential lifetime """

    def display_time(self):


class colors():
    """ formats """

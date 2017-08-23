"""
gcreds Module

Args:

Returns:

"""
from __init__ import __version__
import os
import json
import boto3
from botocore.exceptions import ClientError
import loggers

logger = loggers.getLogger(__version__)


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
    def __init__(self, iam_user):
        """ initalization
        Args:
            - checks deps, existence of creds, existence of Settings

        Returns:

        """
        self.sts_max = 720              # minutes, 12 hours
        self.sts_min = 15               # minutes, 0.25 hours
        self.token_default = 60         # minutes
        self.credential_default = 60    # minutes
        self.iam_user = iam_user
        try:
            boto3.setup_default_session(profile_name=self.iam_user)
        except ProfileNotFound:
            logger.warning('iam user not found in local config')
        else:
            self.iam_client = boto3.client('iam')
            self.users = self.get_valid_users(self.iam_client)
            self.serial_numer = self.get_mfa_serial(self.iam_user)
            # no way to use boto3 to extract mfa_serial for iam_user, WTF.
            # MAYBE botocore
    def setup_clients(self, user):


    def get_session_token(self, token_life, mfa_code):
        """
        Summary:
            generates session token for use in gen temp credentials
        Args:
            token_life: token duration in minutes
            SerialNumber:
            TokenCode:

        Returns:
            session token | TYPE: dict
        """
        sts_client = boto3.client('sts')
        iam_user = sts_client.get_caller_identity()['Arn'].split('/')[1]

        token_seconds = token_life * 60
        if self.sts_min < token_seconds < self.sts_max:
            token = sts_client.get_session_token(
                DurationSeconds=token_life,
                SerialNumber=self.arn
                TokenCode=mfa_code
            )
        return token['Credentials']

    def generate_credentials(self, iam_user, roles):
        """ generate temporary credentials for profiles """
        return 0

    def calc_time(self, session=''):
        """ remaining time left in session and credential lifetime """
        return 0

    def display_time(self):
        """ return remaining time on credential """
        return 0

    def get_valid_users(self, client):
        """ Summary
        Retrieve list valid iam users from local config

        Arg:  iam client object

        Returns: list of iam users from the account
        """
        users = [x['UserName'] for x in client.list_users()['Users']]
        return users

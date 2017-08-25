"""
gcreds Module

Args:

Returns:

"""
from __init__ import __version__
import os
import json
import subprocess
import boto3
from botocore.exceptions import ClientError
import loggers

logger = loggers.getLogger(__version__)


class gcreds():
    """
    Summary:
        gcreds generates temporary credentials used to assume roles across
        many AWS accounts. It is commonly used for progammatic use cases where
        avoiding a multi-factor auth prompt in a cli environment is desired

    Example usage:

    >>> from lambda_utils import read_env_variable
    >>> os.environ['DBUGMODE'] = 'True'
    >>> myvar = read_env_variable('DBUGMODE')
    >>> type(myvar)
    True
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
            self.mfa_serial = self.get_mfa_id(self.iam_user)
            # no way to use boto3 to extract mfa_serial for iam_user, WTF.
            # iam_user = sts_client.get_caller_identity()['Arn'].split('/')[1]
    def get_mfa_id(self, user):
        """
        Extracts the mfa_serial arn (soft token) or mfa_serial (hw token)
        from the awscli local configuration
        """
        awscli = 'aws'
        cmd = 'type ' + awscli + ' 2>/dev/null'
        if subprocess.getoutput(cmd):
            cmd = awscli + ' configure get ' + user + '.mfa_serial'
            try:
                mfa_id = subprocess.getoutput(cmd)
            except Exception as e:
                logger.warning('failed to identify mfa_serial')
        return mfa_id

    def generate_session_token(self, token_life, mfa_code=''):
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

        if (self.sts_min < token_life < self.sts_max):
            if self.mfa_serial:
                token = sts_client.get_session_token(
                    DurationSeconds=token_life * 60,
                    SerialNumber=self.mfa_serial,
                    TokenCode=mfa_code
                )
            else:
                token = sts_client.get_session_token(
                    DurationSeconds=token_life * 60
                )
        return token['Credentials']

    def generate_credentials(self, iam_user, roles):
        """ generate temporary credentials for profiles """
        return 0

    def calc_session_life(self, session=''):
        """ remaining time left in session and credential lifetime """
        return 0

    def calc_credenfital_life(self):
        """ return remaining time on credential """
        return 0

    def get_valid_users(self, client):
        """ Summary
        Retrieve list valid iam users from local config

        Arg:
            iam client object

        Returns:
            list of iam users from the account
        """
        users = [x['UserName'] for x in client.list_users()['Users']]
        return users

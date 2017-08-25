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
    def __init__(self, iam_user=''):
        """ initalization
        Args:
            iam_user: username with permissions to assume roles in target aws
            accounts

        Returns:

        """
        self.sts_max = 720                      # minutes, 12 hours
        self.sts_min = 15                       # minutes, 0.25 hours
        self.token_default = 60                 # minutes
        self.credential_default = 60            # minutes
        self.iam_user = iam_user or 'default'
        try:
            boto3.setup_default_session(profile_name=self.iam_user)
        except ProfileNotFound:
            logger.warning('iam user not found in local config')
        else:
            self.iam_client = boto3.client('iam')
            self.sts_client = boto3.client('sts')
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
            token_life:   token lifetime duration in minutes
            SerialNumber: mfa device arn (soft token) or mfa_serial
                          (hardware token)  # this technically not an input - should OMIT?
            mfa_code:     6 digit authorization code from a multi-factor
                          (mfa) authentication device

        Returns:
            session credentials | TYPE: dict

            {
                'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
                'Expiration': datetime.datetime(2017, 8, 25, 20, 5, 37, tzinfo=tzutc()),
                'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
                'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
            }
        """

        token_life = int(token_life)
        mfa_code = str(mfa_code)

        try:
            if (self.sts_min < token_life < self.sts_max):
                if self.mfa_serial:
                    self.token = self.sts_client.get_session_token(
                        DurationSeconds=token_life * 60,
                        SerialNumber=self.mfa_serial,
                        TokenCode=mfa_code
                    )
                else:
                    self.token = self.sts_client.get_session_token(
                        DurationSeconds=token_life * 60
                    )
        except ClientError as e:
            logger(
                'Exception generating session token in account %s (Code: %s Message: %s)' %
                (str(arn.split(':')[4]), e.response['Error']['Code'],
                e.response['Error']['Message']
            ))
            raise
        return self.token['Credentials']

    def generate_credentials(self, roles):
        """
        Summary:
            generate temporary credentials for profiles

        Args:
            roles: List of profile names from the local awscli configuration

        Returns:
            iam role temporary credentials | TYPE: dict

            {
                'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
                'Expiration': datetime.datetime(2017, 8, 25, 20, 5, 37, tzinfo=tzutc()),
                'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
                'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
            }
        """
        # somehow lookup corresponding role_arn for each profile name in roles
        # arn = $ aws configure get roles[0].role_arn
        try:
            for arn in roles:
                response = self.sts_client.assume_role(
                    RoleArn=arn,
                    DurationSeconds=self.credential_default
                )
        except ClientError as e:
            logger(
                'Exception assuming role in account %s (Code: %s Message: %s)' %
                (str(arn.split(':')[4]), e.response['Error']['Code'],
                e.response['Error']['Message']
            ))
            raise
        return response['Credentials']

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
        try:
            users = [x['UserName'] for x in client.list_users()['Users']]
        except ClientError as e:
            logger(
                'Exception listing iam users in account %s (Code: %s Message: %s)' %
                (str(arn.split(':')[4]), e.response['Error']['Code'],
                e.response['Error']['Message']
            ))
            raise
        return users

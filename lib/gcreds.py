"""
gcreds Module

Args:

Returns:

"""
from __init__ import __version__
import os
import json
from json import JSONDecodeError
import subprocess
import boto3
from botocore.exceptions import ClientError, ProfileNotFound
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
        self.token_default = 60                 # minutes, 1 hour
        self.credential_default = 60            # minutes, 1 hour (AWS Default)
        self.iam_user = iam_user or 'default'
        self.config_dir = os.environ['HOME'] + '/.gcreds'
        self.profiles = self.profile_setup()
        try:
            boto3.setup_default_session(profile_name=iam_user)
        except ProfileNotFound as e:
            logger.critical('iam user not found in local config. Error %s' % str(e))
        except Exception:
            logger.critical('Unable to establish session. Error %s' % str(e))
            raise e
        else:
            self.iam_client = boto3.client('iam')
            self.sts_client = boto3.client('sts')
            self.users = self.get_valid_users(self.iam_client)
            self.mfa_serial = self.get_mfa_id(iam_user)

    def profile_setup(self):
        """
        Summary:
            creates profile obj from local configuration file
        Args:
            None

        Returns:
            profile_obj: list of aws account profile role names, role arns
            TYPE: dict
        """
        profile_file = self.config_dir + '/profiles.json'
        try:
            with open(profile_file) as f1:
                profile_obj = json.load(f1)
        except IOError as e:
            logger.critical('problem opening file %s. Error %s' %
                (profile_file, str(e)))
            return 1
        except JSONDecodeError as e:
            logger.critical('%s file not properly formed json. Error %s' %
                (profile_file, str(e)))
            return 1
        return profile_obj

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
                return 1
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
                    response = self.sts_client.get_session_token(
                        DurationSeconds=token_life * 60,
                        SerialNumber=self.mfa_serial,
                        TokenCode=mfa_code
                    )
                else:
                    response = self.sts_client.get_session_token(
                        DurationSeconds=token_life * 60
                    )
                self.token = response['Credentials']
            else:
                return logger.warning(
                    'Requested lifetime must be STS service limits (%s - %s minutes)'
                    % (self.sts_min, self.sts_max)
                    )
        except ClientError as e:
            logger(
                'Exception generating session token in account %s (Code: %s Message: %s)' %
                (str(arn.split(':')[4]), e.response['Error']['Code'],
                e.response['Error']['Message']
            ))
            return 1
        return self.token

    def generate_credentials(self, profile_names):
        """
        Summary:
            generate temporary credentials for profiles

        Args:
            roles: List of profile names from the local awscli configuration

        Returns:
            iam role temporary credentials | TYPE: List

            {
                'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
                'Expiration': datetime.datetime(2017, 8, 25, 20, 5, 37, tzinfo=tzutc()),
                'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
                'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
            }
        """

        temp_credentials = []
        sts_client = boto3.client(
            'sts',
            aws_access_key_id=self.token['AccessKeyId'],
            aws_secret_access_key=self.token['SecretAccessKey'],
            aws_session_token=self.token['SessionToken']
        )
        try:
            for alias in profile_names:
                for profile in self.profiles:
                    if profile['account_alias'] == alias:
                        response = sts_client.assume_role(
                            RoleArn=profile['role_arn'],
                            DurationSeconds=self.credential_default * 60
                        )
                        temp_credentials.append(response['Credentials'])
        except ClientError as e:
            logger(
                'Exception assuming role in account %s (Code: %s Message: %s)' %
                (str(arn.split(':')[4]), e.response['Error']['Code'],
                e.response['Error']['Message']
            ))
            return 1
        return temp_credentials

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
            return 1
        return users

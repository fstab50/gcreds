"""
gcreds Module

Args:

Returns:

"""
from __init__ import __version__
import os
import json
from json import JSONDecodeError
import datetime
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
    def __init__(self, filename, profile_user=''):
        """

        Summary:
            initalization, attribute assignment

        Args:
            filename: name of a json structured file located gcreds config directory
                in the home directory. File contains information about roles for
                which you which to generate temporary credentials

            profile_user: username configured in local awscli config with
                permissions to assume roles in target aws accounts

        """
        self.sts_max = 720                      # minutes, 12 hours
        self.sts_min = 15                       # minutes, 0.25 hours
        self.token_default = 60                 # minutes, 1 hour
        self.token_expiration = ''
        self.credential_expiration = ''
        self.credential_default = 60            # minutes, 1 hour (AWS Default)
        self.profile_user = profile_user or 'default'
        self.config_dir = os.environ['HOME'] + '/.gcreds'
        self.profiles = self.parse_profiles(filename)
        try:
            boto3.setup_default_session(profile_name=profile_user)
        except ProfileNotFound as e:
            logger.critical('iam user not found in local awscli config. Error %s' % str(e))
            # FUTURE: support other local creds configs besides awscli; use real iam
            # user to establish session, look up mfa_serial, etc before declaring fail
        except Exception:
            logger.critical('Unable to establish session. Error %s' % str(e))
            raise e
        else:
            self.iam_client = boto3.client('iam')
            self.sts_client = boto3.client('sts')
            self.iam_user = self.sts_client.get_caller_identity()['Arn'].split('/')[1]
            self.users = self.get_valid_users(self.iam_client)
            self.mfa_serial = self.get_mfa_info(self.iam_user, self.iam_client)

    def parse_profiles(self, file):
        """

        Summary:
            creates list of account profiles from local configuration file

        Args:
            file: name of json file containing role profiles for which gcreds
                  will generate temporary credentials.  This file must be located
                  in ~/.gcreds directory and has the following format:

                [
                    {
                        "account_alias": "acme-gen-ra1-prod",
                        "role_arn": "arn:aws:iam::270145492687:role/UR-AcmeAdmin",
                        "mfa_serial": "arn:aws:iam::354161853056:mfa/IAMAdmin05",
                        "source_profile": "iam-access1"
                    }
                ]
        Returns:
            profile_obj: list of aws account profile role names, role arns
            TYPE: list

        """

        profile_file = self.config_dir + '/' + str(file)

        try:
            with open(profile_file) as f1:
                profile_list = json.load(f1)
        except IOError as e:
            logger.critical('problem opening file %s. Error %s' %
                (profile_file, str(e)))
            return [str(e)]
        except JSONDecodeError as e:
            logger.critical('%s file not properly formed json. Error %s' %
                (profile_file, str(e)))
            return [str(e)]
        return profile_list

    def get_mfa_info(self, user, client):
        """

        Summary:
            Extracts the mfa_serial arn (soft token) or SerialNumber
            (if hardware token assigned)

        Args:
            user:  iam_user in local awscli profile.  user may be a profile name
                   which is used exclusively in the awscli but does not represent an
                   actual iam name recorded in the Amazon Web Services account.

        Returns:
            TYPE: string

        """

        response = client.list_mfa_devices(UserName=user)
        try:
            if response['MFADevices']:
                mfa_id = response['MFADevices'][0]['SerialNumber']
                # Not sure what to do with user_id yet
                user_id = response['MFADevices'][0]['UserName']
            else:
                mfa_id = ''
        except ClientError as e:
            logger.warning(
                'Exception accessing mfa info for profile user %s (Code: %s Message: %s)' %
                (user, e.response['Error']['Code'], e.response['Error']['Message']
            ))
            return str(e)
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
                'StartTime': datetime.datetime(2017, 8, 25, 20, 2, 37, tzinfo=tzutc()),
                'Expiration': datetime.datetime(2017, 8, 25, 20, 5, 37, tzinfo=tzutc()),
                'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
                'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
            }
        """

        token_life = int(token_life)
        mfa_code = str(mfa_code)
        now = datetime.datetime.utcnow()    # needs to be converted to offset datetime

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
                response['Credentials']['StartTime'] = now
                self.token = response['Credentials']
                self.calc_session_life(self.token['Expiration'])
            else:
                return logger.warning(
                    'Requested lifetime must be STS service limits (%s - %s minutes)'
                    % (self.sts_min, self.sts_max)
                    )
        except ClientError as e:
            logger.warning(
                'Exception generating session token with iam user %s (Code: %s Message: %s)' %
                (self.iam_user, e.response['Error']['Code'], e.response['Error']['Message']
            ))
            return {'Error': str(e)}
        return self.token

    def generate_credentials(self, accounts):
        """
        Summary:
            generate temporary credentials for profiles

        Args:
            accounts: List of account aliases or profile names from the local
                      awscli configuration in accounts to assume a role

        Returns:
            iam role temporary credentials | TYPE: Dict

            {
                'gcreds-acme-gen-ra1-prod' : {
                    'AccessKeyId': 'ASIAI6QV2U3JJAYRHCJQ',
                    'Expiration': datetime.datetime(2017, 8, 25, 20, 5, 37, tzinfo=tzutc()),
                    'SecretAccessKey': 'MdjPAkXTHl12k64LSjmgTWMsmnHk4cJfeMHdXMLA',
                    'SessionToken': 'FQoDYXdzEDMaDHAaP2wi/+77fNJJryKvAdVZjYKk...zQU='
                },
                'gcreds-acme-gen-ra1-dev' : {
                    ...
                }
            }
        """

        role_credentials = {}
        sts_client = boto3.client(
            'sts',
            aws_access_key_id=self.token['AccessKeyId'],
            aws_secret_access_key=self.token['SecretAccessKey'],
            aws_session_token=self.token['SessionToken']
        )
        try:
            if self._validate(accounts):
                for alias in accounts:
                    for profile in self.profiles:
                        if profile['account_alias'] == alias:
                            response = sts_client.assume_role(
                                RoleArn=profile['role_arn'],
                                DurationSeconds=self.credential_default * 60,
                                RoleSessionName='gcreds-' + alias
                            )
                            role_credentials['gcreds-' + alias] = response['Credentials']
            else:
                return {}
        except ClientError as e:
            logger(
                'Exception assuming role in account %s (Code: %s Message: %s)' %
                (str(arn.split(':')[4]), e.response['Error']['Code'],
                e.response['Error']['Message']
            ))
            return {str(e)}
        return role_credentials

    def _validate(self, list):
        """

        Summary:
            validates parameter list is a subsset of profiles list object
        Args:
            TYPE: list

        Returns:
            TYPE: Boolean

        """

        profile_aliases = []

        for profile in self.profiles:
            profile_aliases.append(profile['account_alias'])

        if set(list).issubset(set(profile_aliases)):
            return True
        else:
            missing = set(list) - set(profile_aliases)
            ex = Exception('Account profiles not found: %s'% set(missing))
            logger.exception(ex)
            return False

    def calc_session_life(self, timestamp=''):
        """

        Summary:
            remaining time left in session lifetime. The calc_session_life
            method can also be used to reset session life to clear remaining time

        Args:
            timestamp:  datetime object

        Returns:
            TYPE: session remaining lifetime (minutes)

        """

        now = datetime.datetime.utcnow()    # must make offset aware

        try:
            if not self.token_expiration:
                self.token_expiration = self.token['Expiration'] or timestamp    # convert to epoch?
        except NameError:
            return logger.warning('there is no active session established')
        return 0 # stub in for: now - self.token_expiration

    def calc_credential_life(self):
        """ return remaining time on temporary credentials """
        return 0

    def get_valid_users(self, client):
        """

        Summary:
            Retrieve list valid iam users from local config

        Arg:
            iam client object

        Returns:
            TYPE list
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

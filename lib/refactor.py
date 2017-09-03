#!/usr/bin/env python3
""" refactor Module Level comments NEEDED HERE """

from __init__ import __version__
import os
import json
import configparser
import sys
import argparse
import inspect
import loggers

logger = loggers.getLogger(__version__)

# globals
home_dir = os.environ['HOME']
config_dir = home_dir + '/.gcreds'
awscli_default = os.getenv('AWS_SHARED_CREDENTIALS_FILE') or home_dir + '/.aws/credentials'


# -- function declarations  ----------------------------------------------------

def parse_awscli(parameter_input='', parameter_output=''):
    """

    Summary:
        imports awscli credentials file, refactors format to json

    Args:
        parameter_input: TYPE: string, optional input file if not awscli default
        parameter_output: TYPE: string, optional ouput file if not gcreds default

    Returns:
        Success or Failure, TYPE: Boolean

    """
    awscli_file = parameter_input or awscli_default
    output_file = parameter_output or config_dir + '/profiles.json'
    total_dict, tmp = {}, {}

    if not os.path.exists(config_dir):
        logger.info('Configuration dir [%s] missing, creating it' % config_dir)
        os.mkdir(config_dir)

    config = configparser.ConfigParser()
    config.read(awscli_file)

    try:
        for profile in filter(lambda x: 'gcreds' not in x, config.sections()):
            if 'aws_access_key_id' in config[profile].keys():
                tmp['aws_access_key_id'] = config[profile]['aws_access_key_id']
                tmp['aws_secret_access_key'] =  config[profile]['aws_secret_access_key']
                # test if cli secured with mfa
                if 'mfa_serial' in config[profile].keys():
                    tmp['mfa_serial'] = config[profile]['mfa_serial']

            elif 'role_arn' in config[profile].keys():
                tmp['role_arn'] = config[profile]['role_arn']
                tmp['mfa_serial'] = config[profile]['mfa_serial']
                tmp['source_profile'] =  config[profile]['source_profile']
            total_dict[profile] = tmp
            tmp = {}

        # write output file
        with open(output_file, 'w') as f2:
            f2.write(json.dumps(total_dict, indent=4))
            f2.close()

        # secure file permissions
        os.chmod(output_file, 0o700)

    except KeyError as e:
        logger.critical('%s: Cannot find Key %s parsing file %s' %
            (inspect.stack()[0][3], str(e), input_file))
        return False
    except IOError as e:
        logger.critical('%s: problem opening file %s. Error %s' %
            (inspect.stack()[0][3], input_file, str(e)))
        return False
    except Exception as e:
        logger.critical('%s: Unknown error. Error %s' %
            (inspect.stack()[0][3], str(e))
        raise e
    return True

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='gcreds credential data build')
    parser.add_argument("-i", "--input", help="awscli format Input File", required=True)
    parser.add_argument("-o", "--output", help="Credential Output File", required=True)
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    elif not os.path.exists(input_file):
        logger.info('Input file [%s] not found' % input_file)
        sys.exit(1)

    # refactor with manual input
    parse_awscli(parameter_input=input_file, parameter_output=output_file)

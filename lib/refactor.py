#!/usr/bin/env python3

from __init__ import __version__
import os
import json
import configparser
import sys
import argparse
import loggers

logger = loggers.getLogger(__version__)

# globals
home_dir = os.environ['HOME']
config_dir = home_dir + '/.gcreds'
awscli_dir = home_dir + '/.aws' or os.environ['AWS_SHARED_CREDENTIALS_FILE']

parser = argparse.ArgumentParser(description='gcreds credential data build')
parser.add_argument("-i", "--input", help="awscli format Input File", required=True)
parser.add_argument("-o", "--output", help="Credential Output File", required=True)
args = parser.parse_args()

input_file = args.input
output_file = config_dir + '/' + args.output

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

# configuration dir
if not os.path.exists(config_dir):
    logger.info('Configuration dir [%s] missing, creating it' % config_dir)
    os.mkdir(config_dir)

if not os.path.exists(input_file):
    logger.info('Input file [%s] not found' % input_file)
    exit(1)
else:
    config = configparser.ConfigParser()
    config.read(input_file)

total_dict, tmp = {}, {}

try:
    for profile in config.sections():
        if 'gcreds' in profile:
            continue
        elif 'aws_access_key_id' in config[profile].keys():
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

except KeyError as e:
    logger.critical('Cannot find Key %s parsing file %s' % (str(e), input_file))
except IOError as e:
    logger.critical('problem opening file %s. Error %s' % (input_file, str(e)))
except Exception as e:
    logger.critical('unknown error. Error %s' % str(e))

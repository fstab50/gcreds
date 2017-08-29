#!/usr/bin/env python3

from __init__ import __version__
import os
import json
import configparser
import argparse
import loggers

logger = loggers.getLogger(__version__)

# globals
home_dir = os.environ['HOME']
config_dir = home_dir + '/.gcreds'

argparser = argparse.ArgumentParser(description='gcreds credential data build')
argparser.add_argument("-i", "--input", help="awscli format Input File", required=True)
argparser.add_argument("-o", "--output", help="Credential Output File", required=True)
args = argparser.parse_args()

input_file = args.input
output_file = config_dir + '/' + args.output

# configuration dir
if not os.path.exists(config_dir):
    logger.info('Configuration dir [%s] missing, creating it' % config_dir)
    os.mkdir(config_dir)

config = configparser.ConfigParser()
config.read(input_file)

tmp, tdict = {}, {}

try:
    for profile in config.sections():
        tmp['role_arn'] = config[profile]['role_arn']
        tmp['mfa_serial'] = config[profile]['mfa_serial']
        tmp['source_profile'] =  config[profile]['source_profile']
        tdict[profile] = tmp

except KeyError as e:
    logger.critical('Cannot find Key %s parsing file %s' % (str(e), input_file))
    pass
except IOError as e:
    logger.critical('problem opening file %s. Error %s' % (input_file, str(e)))
except Exception as e:
    logger.critical('unknown error. Error %s' % str(e))

# write output file
with open(output_file, 'w') as f2:
    f2.write(json.dumps(tdict, indent=4))
    f2.close()

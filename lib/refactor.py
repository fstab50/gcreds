#!/usr/bin/env python3

from __init__ import __version__
import os
import json
import argparse
import loggers

logger = loggers.getLogger(__version__)

# globals
container = []
dict = {}
ct = 0
home_dir = os.environ['HOME']
config_dir = home_dir + '/.gcreds'

argparser = argparse.ArgumentParser(description='gcreds credential data build')
argparser.add_argument("-f", "--file", help="Credential Input File", required=True)
args = argparser.parse_args()

input_file = args.file
output_file = config_dir + '/profiles.json'

# configuration dir
if not os.path.exists(config_dir):
    logger.info('Configuration dir [%s] missing, creating it' % config_dir)
    os.mkdir(config_dir)

try:
    with open(input_file) as f1:
        for line in f1:
            if line.strip():
                if '[' and ']' in line:
                    profile_name = line.split('[')[1].split(']')[0]
                    dict['profile'] = profile_name

                elif 'role_arn' in line:
                    dict['role_arn'] = line.split('=')[1].strip()

                elif 'mfa_serial' in line:
                    dict['mfa_serial'] = line.split('=')[1].strip()

                elif 'source_profile' in line:
                    dict['source_profile'] = line.split('=')[1].strip()
                ct += 1
                if ct == 4:
                    print(json.dumps(dict, indent=4))
                    container.append(dict)
                    dict = {}
                    ct = 0
        f1.close()
except IOError as e:
    logger.critical('problem opening file %s. Error %s' % (input_file, str(e)))
except Exception as e:
    logger.critical('unknown error. Error %s' % str(e))

else:
    # write output file
    with open(output_file, 'w') as f2:
        f2.write(json.dumps(container, indent=4))
        f2.close()

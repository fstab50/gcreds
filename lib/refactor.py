#!/usr/bin/env python3

import os
import json

container = []
dict = {}
ct = 0
home_dir = os.environ['HOME']

input_file = home_dir + '/.aws/credentials'
output_file = 'credential_refactor.json'

try:
    with open() as f1:
        for line in f1:
            if line.strip():
                if '[' and ']' in line:
                    profile_name = line.split('[')[1].split(']')[0]
                    dict['profile'] = profile_name

                elif 'role_arn' in line:
                    dict['role_arn'] = line.strip()

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
    print('problem opening file %s. Error %s' % (input_file, str(e))

else:
    # write output file
    with open(output_file, 'w') as f2:
        f2.write(json.dumps(container, indent=4))
        f2.close()

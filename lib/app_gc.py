#!/usr/bin/env python3

import boto3
import argparse

argparser = argparse.ArgumentParser(description='Testing ARN stuff')
argparser.add_argument("--role", help="If running with a role provide it here", required=True)
argparser.add_argument("--profile", help="Credential profile", required=True)
argparser.add_argument('--region', help='AWS Region to work within, defaults to eu-central-1', default='eu-central-1', required=False)
args = argparser.parse_args()
role = args.role
profile = args.profile
region = args.region

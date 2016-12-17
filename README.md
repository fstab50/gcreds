* * *
# README :  gcreds (v1.0)
* * *

### Purpose

**gcreds** gets temporary credentials

* * * 

### Deployment Owner/ Author

Blake Huber  
Slack: [@blake](https://mpcaws.slack.com/team/blake)  

* * * 

### Contents

* [README.md](./README.md):  This file
* [cloudformation/](./cloudformation/):  CloudFormation templates and deployment artifacts
* [deployed_last](./deployed_last/):  Last zip file tested and deployed
* [policies](./policies/): dir containing IAM policies for roles created
* [zipfile/](./zipfile/):  location of lambda functions and dependent libraries

* * * 

### Dependencies

- Base SNS topic referenced via cfn export variable ```SNGenericCWTopic```, _must exist_
- Slack-Alerts must be deployed in one of three Atos Tooling Accounts:
    - **atos-tooling-dev** (development)
    - **atos-tooling-qa** (QA)
    - **atos-tooling-pr** (Production)
- s3 bucket containing codebase must exist and contain codebase in zip format prior to stack creation
- s3bucket = ```s3-eu-west-1-lambda```, region eu-west-1
- s3key = ```slack-alerts/slack-alerts-codebase.zip```
- Cloudformation deployment stack must be deployed in same region as s3 bucket containing codebase

* * *

### Details 


* * * 
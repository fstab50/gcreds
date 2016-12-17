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
* [gcreds](./gcreds):  gcreds main executable

* * * 

### Dependencies

- awscli | must be installed and configured
- jq | json parser

* * *

### Usage 

Help Menu

![](./images/help-menu.png)

* * *

## Installation ##

* General Dependencies
    - One of the following python versions: 2.6.5, 2.7.X+, 3.3.X+, 3.4.X+
    - Installation Amazon CLI tools (awscli, see below this section)
    - awk, see your dist repo
    - sed, see your dist repo

* Install jq, a JSON parser from your local distribution repository.
```bash
    $ sudo apt-get install jq    # Ubuntu, most Debian-based distributions
```
```bash
    $ sudo yum install jq        # RedHat, Fedora, CentOS 
```

* Install [awscli](https://github.com/aws/aws-cli/)
    
    Detailed instructions can be found in the README located at:
    https://github.com/aws/aws-cli/

    The easiest method, provided your platform supports it, is via [pip](http://www.pip-installer.org/en/latest).

```bash
    $ sudo pip install awscli
```

* If you have the aws-cli installed and want to upgrade to the latest version you can run:

```bash
    $ sudo pip install --upgrade awscli
```

* Clone this git repo in a writeable directory:

```bash
    $ git clone https://blakeca00@bitbucket.org/blakeca00/gcreds.git
```


* * *

### Output

Sample Output - generating credentials

![](./images/sample-output.png)

* * * 
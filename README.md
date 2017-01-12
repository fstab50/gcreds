# README :  gcreds (v1.2.5)
* * *

## Purpose ##

**gcreds** requests temporary credentials from [Amazon Security Token Service (STS)](http://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html)  
for roles that normally require mfa credentials in order to authenticate.  

The primary use case for **gcreds** is for generating a temporary set of AWS access  
credentials for programmatic use by automation tools running on your local machine.

See [v1.2 Release Notes](./notes/release_v1.2.md)

* * *

## Deployment Owner/ Author ##

Blake Huber  
Slack: [@blake](https://mpcaws.slack.com/team/blake)  

* * *

## Contents ##

* [README.md](./README.md):  This file
* [gcreds](./gcreds):  gcreds main executable
* [notes/](./notes/):  Directory containing all release notes

* * *

## Dependencies ##

- One of the following python versions: 2.6.5, 2.7.X+, 3.3.X+, 3.4.X+
- Installation Amazon CLI tools (awscli, see Installation section)
- [jq](https://stedolan.github.io/jq), a json parser generally available from your distribution repo
- bash (4.x)
- Standard linux utilities: grep, awk, sed, cat, hostname

* * *

## Usage ##

Help Menu

```bash
    $ ./gcreds -h  
```

![help-menu](./.images/help-menu.png)

* * *

## Installation ##

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
    $ git clone <domain>/gcreds.git
```

* Add an alias to your local shell profile (optional, but recommended)

```bash
    $  echo "alias gcreds='~/<directory>/gcreds/gcreds'" >> ~/.bashrc

    OR

    $  echo "alias gcreds='~/<directory>/gcreds/gcreds'" >> ~/.bash_profile
```

* * *

## Output ##

**stdout** - when generating credentials

![gcreds output](./.images/stdout.png)

**Modifications to local awscli configuration** (account ids have been obscured):  

```bash
    $ less ./aws/credentials
```  

![aws example credentials file](./.images/credentials.png)

**Example Use** of profiles created by **greds**:

![example usage](./.images/example-usage.png)

**Show Option** -- show current temporary credentials; associated lifetime

```bash
    $ gcreds --show
```

![option show](./.images/gcreds-show.png)  

**Log output** (colors courtesy of pkg [source-highlight](https://www.gnu.org/software/src-highlite/)):

```bash
    $ less ~/gcreds/logs/gcreds.log
```

![example gcreds.log](./.images/log-output.png)  

* * *

## Enhancement Roadmap ##

1. flag passed at runtime to suppress all stdout msgs, diverting instead to log only.

2. Pass a run time parameter to function gcreds-revert_creds() that will bypass currently  
required user input to clear or restore credentials.

3. Upon startup, check the $AWS_SHARED_CREDENTIALS_FILE variable for an alternate location of the  
awscli credentials dir.  Set cred_path = value if found; else use default location (~/.aws).  
From a cli, see:
```bash
    $ aws help config-vars
```

<a name="top"></a>
* * *
# gcreds
* * *

## Summary

**gcreds** (pronounced "gee-creds" for _generate credentials_) is a utility for creation and managment of IAM temporary access credentials using Amazon's [Security Token Service (STS)](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html).  [Temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) are used to access AWS resources when assuming a role identity.

For more information on the above terms and functions, see [an explanation of IAM roles in the Amazon Web Services](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) documentation.

**Version**:	2.4.4


* * *

## Contents

* [**Purpose**](#purpose)

* [**Dependencies**](#dependencies)

* [**Program Options**](#program-options)

* [**Build Options**](#build-options)

* [**Configuration**](#configuration)

* [**Installation**](#installation)
    * [Ubuntu, Linux Mint, Debian-based Distributions](#debian-distro-install)
    * [Redhat, CentOS](#redhat-distro-install)
    * [Amazon Linux 2, Fedora](#amzn2-distro-install)

* [**Screenshots**](#screenshots)

* [**Author & Copyright**](#author--copyright)

* [**License**](#license)

* [**Disclaimer**](#disclaimer)

--

[back to the top](#top)

* * *

## Purpose ##

**gcreds** requests temporary credentials from [Amazon's Security Token Service (STS)](http://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html) for roles that normally require [multi-factor credentials](https://en.wikipedia.org/wiki/Multi-factor_authentication) in order to authenticate.

A primary use case for **gcreds** is generating a temporary set of AWS access credentials for programmatic use by automation tools running on your local machine.

**gcreds** manages temporary credentials it generates to prevent corruption of your local awscli config. When generating new temporary credentials, **gcreds** will automatically clear expired credentials from your local awscli config to block the presence of duplicate sets of credentials.


#### Previous Releases ####
* [v2.0 Release Notes](./notes/release_v2.0.md)
* [v1.2 Release Notes](./notes/release_v1.2.md)
* [v1.0 Release Notes](./notes/release_v1.0.md)
* [v1.3 Release Notes](./notes/release_v1.3.md)

--

[back to the top](#top)

* * *

## Dependencies

[gcreds](https://github.com/fstab50/gcreds) requires the following:

- [Python version 3.6+](https://docs.python.org/3/)
- Installation Amazon CLI tools (awscli, see Installation section)
- [jq](https://stedolan.github.io/jq), a json parser generally available from your distribution repo
- bash (4.x)
- Standard linux utilities:
    * grep
    * awk
    * sed
    * cat
    * hostname

--

[back to the top](#top)

* * *

## Program Options

To display the **gcreds** help menu:

```bash
    $ gcreds --help
```

<p align="center">
    <a href="http://images.awspros.world/gcreds/help-menu.png" target="_blank"><img src="./assets/help-menu.png">
</p>

--

[back to the top](#top)

* * *
## Build options

**[GNU Make](https://www.gnu.org/software/make) Targets**.  Type the following to display the available make targets from the root of the project:

```bash
    $  make help
```

<p align="center">
    <a href="http://images.awspros.world/gcreds/make-help.png" target="_blank"><img src="./assets/make-help.png">
</p>

--

[back to the top](#top)

* * *
## Configuration

Configure [gcreds](https://github.com/fstab50/gcreds) runtime options by entering the configuration menu:

```bash
    $ gcreds --configure
```

[![cinfugyre2](./assets/configure-1.png)](http://images.awspros.world/gcreds/configure-1.png)&nbsp;

--

If the same IAM user will be utilised to generate role credentials, set the default gcreds IAM user here to avoid entering "--profile <user>" every time gcreds is called to generate credentials for your local awscli configuration:

[![option a](./assets/configure-2.png)](http://images.awspros.world/gcreds/configure-2.png)

--

Choose a default color scheme for gcreds accent highlighting via the next menu:

[![configure3](./assets/configure-3.png)](http://images.awspros.world/gcreds/configure-3.png)&nbsp;

--


[![configure4](./assets/configure-4.png)](http://images.awspros.world/gcreds/configure-4.png)

--

[back to the top](#top)

* * *
## Installation
* * *

<a name="debian-distro-install"></a>
### Ubuntu, Linux Mint, Debian variants  (Python 3.6, 3.7)

The easiest way to install **gcreds** on debian-based Linux distributions is via the debian-tools package repository:


1. Open a command line terminal.

    [![deb-install0](./assets/deb-install-0.png)](http://images.awspros.world/gcreds/deb-install-0.png)

2. Download and install the repository definition file

    ```
    $ sudo apt install wget
    ```

    ```
    $ wget http://awscloud.center/deb/debian-tools.list
    ```

    [![deb-install1](./assets/deb-install-1.png)](http://images.awspros.world/gcreds/deb-install-1.png)

    ```
    $ sudo chown 0:0 debian-tools.list && sudo mv debian-tools.list /etc/apt/sources.list.d/
    ```

3. Install the package repository public key on your local machine

    ```
    $ wget -qO - http://awscloud.center/keys/public.key | sudo apt-key add -
    ```

    [![deb-install2](./assets/deb-install-2.png)](http://images.awspros.world/gcreds/deb-install-2.png)

4. Update the local package repository cache

    ```
    $ sudo apt update
    ```

5. Install **gcreds** os package

    ```
    $ sudo apt install gcreds
    ```

    Answer "y":

    [![deb-install3](./assets/deb-install-3.png)](http://images.awspros.world/gcreds/deb-install-3.png)


6. Verify Installation

    ```
    $ apt show gcreds
    ```

    [![apt-show](./assets/deb-install-4.png)](http://images.awspros.world/gcreds/deb-install-4.png)


[back to the top](#top)

* * *
<a name="redhat-distro-install"></a>
### Redhat, CentOS  (Python 3.6)

Redhat Package Manager (RPM) format installation package under development.  Check [rpm.awscloud.center](http://s3.us-east-2.amazonaws.com/rpm.awscloud.center/index.html) page for updates.


[back to the top](#top)

* * *
<a name="amzn2-distro-install"></a>
### Amazon Linux 2 / Fedora (Python 3.7+)

Redhat Package Manager (RPM) format used by Amazon Linux under development.  Check [amzn2.awscloud.center](http://s3.us-east-2.amazonaws.com/amzn2.awscloud.center/index.html) page for updates.

--

[back to the top](#top)

* * *
## Screenshots

#### Authentication Status

Runtime statistics displayed while authenitcation is active.   Alternatively, the command below displays same information anytime.

```bash
    $ gcreds  --show
```

<p align="center">
    <a href="http://images.awspros.world/gcreds/gcreds-status.png"><img src="./assets/gcreds-status.png">
</p>


[back to the top](#top)

* * *

#### Green Accent Scheme

```bash
    $ gcreds  --help
```

<p align="center">
    <a href="http://images.awspros.world/gcreds/help-menu-green.png"><img src="./assets/help-menu-green.png">
</p>


[back to the top](#top)

* * *

#### Blue Accent Scheme (green terminal)

<p align="right">
    <a href="http://images.awspros.world/gcreds/help-menu-blue.png"><img src="./assets/help-menu-blue.png">
</p>


[back to the top](#top)

* * *

#### Log file

<p align="right">
    <a href="http://images.awspros.world/gcreds/log-output.png"><img src="./assets/log-output.png">
</p>


[back to the top](#top)

* * *

## Author & Copyright

All works contained herein copyrighted via below author unless work is explicitly noted by an alternate author.

* Copyright Blake Huber, All Rights Reserved.

[back to the top](#top)

* * *

## License

* Software contained in this repo is licensed under the [license agreement](./LICENSE.md).  You may display the license and copyright information by issuing the following command:

```
$ gcreds --version
```

[![help](./assets/version-copyright.png)](https://images.awspros.world/gcreds/version-copyright.png)


[back to the top](#top)

* * *

## Disclaimer

*Code is provided "as is". No liability is assumed by either the code's originating author nor this repo's owner for their use at AWS or any other facility. Furthermore, running function code at AWS may incur monetary charges; in some cases, charges may be substantial. Charges are the sole responsibility of the account holder executing code obtained from this library.*

Additional terms may be found in the complete [license agreement](./LICENSE.md).

[back to the top](#top)

* * *

<a name="top"></a>
* * *
# gcreds
* * *

## Summary

**gcreds** (pronounced "gee-creds" for _generate credentials_) is a utility for creation and managment of IAM temporary access credentials using Amazon's [Security Token Service (STS)](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html).  [Temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) are used to access AWS resources when assuming a role identity.

For more information on the above terms and functions, see [an explanation of IAM roles in the Amazon Web Services](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) documentation.

**Version**:	2.4.3


* * *

## Contents

* [**Dependencies**](#dependencies)

* [**Program Options**](#program-options)

* [**Build Options**](#build-options)

* [**Configuration**](#configuration)

* [**Installation**](#installation)
    * [Pip Install](#installation)
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

[![toc](./assets/configure_toc.png)](http://images.awspros.world/gcreds/configure_toc.png)&nbsp;

[back to the top](#top)

--

Option "A" (shown below) allows addition of file types to be excluded (skipped) from line totals

[![option a](./assets/configure_a.png)](http://images.awspros.world/gcreds/configure_a.png)

[back to the top](#top)

--

Option "B" (shown below) allows deletion of file types from the exclusion list so that a specific file extension will be included in total line counts:

[![option b](./assets/configure_b.png)](http://images.awspros.world/gcreds/configure_b.png)&nbsp;

[back to the top](#top)

--

Option "C" (shown below) allows user-customization of files highlighted for containing a large number of lines of text:

[![option c](./assets/configure_c.png)](http://images.awspros.world/gcreds/configure_c.png)

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
    $ sudo apt install python3-gcreds
    ```

    Answer "y":

    [![deb-install3](./assets/deb-install-3.png)](http://images.awspros.world/gcreds/deb-install-3.png)


6. Verify Installation

    ```
    $ apt show python3-gcreds
    ```

    [![rpm-install4](./assets/rpm-install-4.png)](http://images.awspros.world/gcreds/rpm-install-4.png)


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

#### Project 1: Line count, low complexity git repository:

```bash
    $ gcreds  --sum  git/branchdiff
```

<p align="center">
    <a href="http://images.awspros.world/gcreds/gcreds-output-branchdiff.png"><img src="./assets/gcreds-output-branchdiff-md.png" width="900">
</p>


[back to the top](#top)

* * *

#### Project 2: Line count, medium complexity git repository:

<p align="right">
    <a href="http://images.awspros.world/gcreds/gcreds-awslabs.png"><img src="./assets/awslabs-content.png">
</p>


[back to the top](#top)

* * *

#### Project 3: Line count, high complexity git repository:

<p align="right">
    <a href="http://images.awspros.world/gcreds/gcreds_output_large.png"><img src="./assets/awslabs-serverless.png">
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

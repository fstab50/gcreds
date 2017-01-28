# gcreds v1.3 | Release Notes

* * *
**Release date**:  January 28, 2017
* * *

## Features and Fixes Implemented in v1.3

* [**Parameter Option Change**]: -f (--file) has been replaced with -a | --accounts.  
For backward compatibility, **gcreds** will continue to accept -f or --file as a  
Parameter set, as long as properly formatted file with one aws account role per line  
is still referenced. This change was made for consistency with upstream cloudformation  
automation tooling.

* [**Usability**]: **gcreds** will now accept an account file located in any location.  
Additionally, either an absolute or relative path to the file may be specified in  
the -a (--accounts) parameter set.

* * *

## Limitations

#### Working with Duplicate Sets of Credentials

* **gcreds** still needs integration testing in the following environments to  
determine full compatibility:
    * Redhat Enterprise Linux 7
    * Amazon Linux 03.2017
    * SUSE Enterprise Linux 12

* * *

( [Back to README](../README.md) )


* * *

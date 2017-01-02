# v1.2 Release Notes
* * * 

## Features Implemented in v1.2

* [**Security**]: Enhanced logging to now include attempted generation of session token for  
the master IAM profile used to assume roles as well as creating log record of all new profiles  
generated with temporary credentials.

* [**User setable credential lifetime:  Option -t | --timeout**]: Previous versions defaulted only  
to 15 minute credential lifetime.  Users can now pass option -t (or --timeout) to generate  
credentials up to 36 hour Amazon STS maximum. (previously item (1) on the Enhancement Roadmap  
section of the [README](../README.md)))

* [**Parameter Refactoring**]: Parameters provided when invoking gcreds can now be given in any  
random order and processed successfully (previously item (3) on the Enhancement Roadmap section  
of the [README](../README.md)))

* * *

## Limitations

#### Working with Duplicate Sets of Credentials

* **gcreds** will complain if you want to have more than 1 set of temporary credentials in awscli  
config at a time. This is to prevent corruption of the local awscli config.  _You can choose not  
to clear credentials from your config before generating a new set of temp credentials; however, this  
**will corrupt your local awscli config with duplicate entries unless generating credentials for  
accounts and roles that are not represented in the first set of temp credentials already present in  
the config**._

* * *

( [Back to README](../README.md) )


* * *
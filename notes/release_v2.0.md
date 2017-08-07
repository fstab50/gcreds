# gcreds v2.0 | Release Notes

* * *
**Release date**:  August, 2017
* * *

## Features and Fixes Implemented in v2.0

* **Auto-refresh** :  `-A, --auto <# hours>`  
When auto parameters are passed, **gcreds** will Auto-refresh temporary credentials  
in the local awscli config without the user having to authenticate again. Durations  
up to 12 hours may be used. **gcreds** may still be used without auto refresh to generate  
temporary credentials that expire in 1 hour.  

* **Configure Mode** :  `-C, --config`  
By invoking the configure option, parameters may be passed automatically to **gcreds**  
Two parameters are currently supported:
    * default_profile: sets the default iam profile to be used so that -p, --profile  
    option does not need to be provided
    * default_color scheme: color scheme can be changed to improve visibility on screens  
    with white backgrounds, a problem in previous releases.      

* **help_menu** : clean up and rewrite of help menu

* * *

## Limitations

#### Integration Testing

* **gcreds** still needs integration testing in the following environments to  
determine full compatibility:
    * Redhat Enterprise Linux 7
    * Amazon Linux 03.2017
    * SUSE Enterprise Linux 12

* * *

( [Back to README](../README.md) )


* * *

"""
Summary:
    - Script sanitizes accounts provided to gcreds as account lists.
    - Ensures all accounts are present in awscli config and do not have duplicates
    - Automatically supresses output to standout to only return bool values if redirected

"""
import collections
import os
import argparse
import sys
from colors import Colors

HOME = os.environ["HOME"]


def tty():
    """
    Summary:
        Determines if output is displayed to the screen or redirected
    Returns:
        True if tty terminal | False if redirected, TYPE: bool
    """
    if sys.stdout.isatty():
        return True
    return False


def duplicates(chklist, silent=tty()):
    """
    Identifies duplicates in a list
    Return:
        True (no duplicates) | False (duplicates), TYPE: bool
    """
    # find duplicates
    d = [item for item, count in collections.Counter(chklist).items() if count > 1]

    if d:
        stdout_message(
            message='Duplicates identified: %s' % str(list(filter(lambda x: str(x) + '\n', d))),
            prefix='WARN',
            severity='WARNING',
            quiet=not silent
        )
        return False
    else:
        stdout_message(message='No duplicates found', quiet=not silent)
    return True


def options(parser):
    """
    Summary:
        parse cli parameter options
    Returns:
        TYPE: argparse object, parser argument set
    """
    parser.add_argument("-s", "--subset", nargs='?', type=str, required=True)
    parser.add_argument("-S", "--superset", nargs='?', default=HOME + '/.aws/credentials.orig', type=str, required=False)
    return parser.parse_args()


def stdout_message(message, prefix='INFO', quiet=False, multiline=False, indent=4, severity=''):
    """
    Summary:
        Prints message to cli stdout while indicating type and severity

    Args:
        :message (str): text characters to be printed to stdout
        :prefix (str):  4-letter string message type identifier.
        :quiet (bool):  Flag to suppress all output
        :multiline (bool): indicates multiline message; removes blank lines
            on either side of printed message
        :indent (int): left justified number of spaces to indent before
            printing message ouput
        :severity (str): header msg determined color instead of prefix

    .. code-block:: python

        # Examples:

            - INFO (default)
            - ERROR (error, problem occurred)
            - WARN (warning)
            - NOTE (important to know)

    Returns:
        TYPE: bool, Success (printed) | Failure (no output)
    """
    prefix = prefix.upper()
    tabspaces = int(indent)
    # prefix color handling
    choices = ('RED', 'BLUE', 'WHITE', 'GREEN', 'ORANGE')
    critical_status = ('ERROR', 'FAIL', 'WTF', 'STOP', 'HALT', 'EXIT', 'F*CK')
    bracket = Colors.RESET + Colors.UNBOLD + Colors.GOLD2

    if quiet:
        return False
    else:
        if prefix in critical_status or severity.upper() == 'CRITICAL':
            header = ('\t' + Colors.YELLOW + '[ ' + Colors.RED + prefix +
                      Colors.YELLOW + ' ]' + Colors.RESET + ': ')
        elif severity.upper() == 'WARNING':
            header = ('\t' + bracket + '[ ' + Colors.ORANGE + prefix +
                      bracket + ' ]' + Colors.RESET + ': ')
        else:    # default color scheme
            header = ('\t' + bracket + '[ ' + Colors.DARKCYAN + prefix +
                      bracket + ' ]' + Colors.RESET + ': ')
        if multiline:
            print(header.expandtabs(tabspaces) + str(message))
        else:
            print('\n' + header.expandtabs(tabspaces) + str(message) + '\n')
    return True


def subset_test(super, sub, silent=tty()):
    """
    Args:
        super (list): superset elements
        sub (list): subset elements
    Returns:
        TYPE: bool
        True if all elements in sub are contained in super; False otherwise
    """
    if set(sub) - set(super):
        stdout_message(
            message='The following accounts not found in local awscli config:',
            prefix='WARN',
            severity='WARNING',
            quiet=not silent
        )
        if tty():
            for i in set(sub) - set(super):
                print('\t\t' + str(i))
        return False
    else:
        stdout_message(
            message='All elements in subset confirmed in local awscli config',
            quiet=not silent
            )
        return True


def init_cli():

    subset, superset = [], []

    try:
        parser = argparse.ArgumentParser()
        args = options(parser)
    except Exception as e:
        print('Problem parsing parameters')
        return False

    if len(sys.argv) == 1:
        stdout_message('You must provide an acct list using the --subset parameter. Exit')
        return False

    try:
        with open(args.subset) as f1:
            f2 = f1.readlines()
            for name in f2:
                subset.append(name[:-1])

        with open(args.superset) as f1:
            f2 = f1.readlines()
            for name in f2:
                if name.startswith('['):
                    superset.append(name[1:-2])
    except OSError as e:
        print(str(e))
        return False

    # test subset within superset
    if subset_test(superset, subset):
        # test subset to determine duplicates
        return duplicates(subset)
    return False


if __name__ == '__main__':
    sys.exit(init_cli())

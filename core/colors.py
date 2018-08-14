"""
Summary:
    ANSI color and formatting code class
    See: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#256-colors
    VERSION:  1.13
Args:
    None

Returns:
    ansi codes

Raises:
    None.  AttributeError if no code match returns the reset ansi codes
"""


class Colors():
    """
    Class attributes provide different format variations
    """
    # forground colors
    AQUA = '\u001b[38;5;14m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    DARKBLUE = '\033[38;5;95;38;5;24m'
    GREEN = '\033[92m'
    DARKGREEN = '\u001b[38;5;2m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ORANGE = '\033[38;5;95;38;5;214m'
    GOLD2 = '\033[38;5;95;38;5;136m'                    # yellow-orange, lighter than GOLD3
    GOLD3 = '\033[38;5;95;38;5;178m'                    # yellow-orange
    WHITE = '\033[37m'
    WHITEGRAY = '\033[38;5;95;38;5;250m'                # white-gray
    LT1GRAY = '\033[38;5;95;38;5;245m'                  # light gray
    LT2GRAY = '\033[38;5;95;38;5;246m'
    LT3GRAY = '\u001b[38;5;249m'
    DARKGRAY1 = '\033[90m'
    DARKGRAY2 = '\033[38;5;95;38;5;8m'                  # darkest gray

    # bright colors
    BRIGHTBLUE = '\033[38;5;51m'
    BRIGHTCYAN = '\033[38;5;36m'
    BRIGHTGREEN = '\033[38;5;95;38;5;46m'
    BRIGHTPURPLE = '\033[38;5;68m'
    BRIGHTRED = '\u001b[31;1m'
    BRIGHTYELLOW = '\033[38;5;11m'
    BRIGHTYELLOW2 = '\033[38;5;95;38;5;226m'
    BRIGHTYELLOWGREEN = '\033[38;5;95;38;5;155m'
    BRIGHTWHITE = '\033[38;5;15m'

    # background colors
    BKGND_BLACK = '\u001b[40m'
    BKGND_BLUE = '\u001b[44m'
    BKGND_CYAN = '\u001b[46m'
    BKGND_GREEN = '\u001b[42m'
    BKGND_MAGENTA = '\u001b[45m'
    BKGND_RED = '\u001b[41m'
    BKGND_WHITE = '\u001b[47m'
    BKGND_WHITE_BOLD = '\u001b[47;1m'
    BKGND_YELLOW = '\u001b[43m'

    # background colors; bright
    BKGND_BRIGHT_BLACK = '\u001b[40;1m'
    BKGND_BRIGHT_BLUE = '\u001b[44;1m'
    BKGND_BRIGHT_CYAN = '\u001b[46;1m'
    BKGND_BRIGHT_GREEN = '\u001b[42;1m'
    BKGND_BRIGHT_GRAY = '\u001b[38;1m'
    BKGND_BRIGHT_MAGENTA = '\u001b[45;1m'
    BKGND_BRIGHT_RED = '\u001b[41;1m'
    BKGND_BRIGHT_WHITE = '\u001b[47;1m'
    BKGND_BRIGHT_YELLOW = '\u001b[43;1m'

    # formats
    BOLD = '\033[1m'
    UNBOLD = '\033[22m'
    UNDERLINE = '\033[4m'
    ITALIC = '\e[3m'
    END = '\033[0m'
    REVERSE = '\033[;7m'
    RESET = '\033[0;0m'
    RESET_ALT = '\u001b[0m'

    # special formats
    URL = UNDERLINE + CYAN
    TITLE = UNDERLINE + BOLD

    #except AttributeError as e:
    #    logger.info('Ansi color code not found (%s), returning reset code' % str(e))

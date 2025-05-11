def generate(*code):
    """For concat too many codes.

    :param code: An ANSI code or number code
    :type code: str | int

    :return: The ANSI escape sequence
    :rtype: str
    """

    def normalize(x):
        """

        Arguments:
            x (str | int):

        Returns:
            str:
        """
        if str(x).startswith('\033'):
            return x.removeprefix('\033[').removesuffix('m')
        else:
            return str(x)

    return f"\033[{';'.join(normalize(c) for c in code)}m"


class Color:
    """ Class for control the color of the text."""

    @staticmethod
    def get_rgb(red, green, blue):
        """ Get the ANSI escape sequence for an RGB color.

        Arguments:
            red (int) : The red color: 0 -> 255
            green (int) : The green color: 0 -> 255
            blue (int) : The blue color: 0 -> 255

        Returns:
            str : The ANSI escape sequence
        """
        return f"\033[38;2;{red};{green};{blue}m"

    @staticmethod
    def get_hex(hexadecimal):
        """ Get the ANSI escape sequence for a Hex color.

        Arguments:
            hexadecimal (str) : The hexadecimal color: #000000 -> #FFFFFF

        Returns:
            str : The ANSI escape sequence
        """
        if hexadecimal[0] == "#":
            hexadecimal = hexadecimal[1:]
        return Color.get_rgb(
            red=int(hexadecimal[:2], 16),
            green=int(hexadecimal[2:4], 16),
            blue=int(hexadecimal[4:], 16)
        )

    BLACK: str = '\033[30m'
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    BLUE: str = '\033[34m'
    PURPLE: str = '\033[35m'
    CYAN: str = '\033[36m'
    WHITE: str = '\033[37m'

    LIGHT_BLACK: str = '\033[90m'
    LIGHT_RED: str = '\033[91m'
    LIGHT_GREEN: str = '\033[92m'
    LIGHT_YELLOW: str = '\033[93m'
    LIGHT_BLUE: str = '\033[94m'
    LIGHT_PURPLE: str = '\033[95m'
    LIGHT_CYAN: str = '\033[96m'
    LIGHT_WHITE: str = '\033[97m'

    STOP: str = '\033[39m'

    def __init__(self, red=..., green=..., blue=..., *, hexadecimal=...):
        """ Use red, green, blue OR hexadecimal.

        **WARNING**: Hexadecimal overwrites red, green and blue.

        Arguments:
            red (int) : The red color: 0 -> 255
            green (int) : The green color: 0 -> 255
            blue (int) : The blue color: 0 -> 255
            hexadecimal (str) : The hexadecimal color: #000000 -> #FFFFFF
        """
        self.set(red, green, blue, hexadecimal=hexadecimal)

    def __str__(self):
        """Get the Hexadecimal value"""

        def make(x):
            return hex(x).replace('0x', '').upper().rjust(2, '0')

        return f"#{make(self.red)}{make(self.green)}{make(self.blue)}"

    def __repr__(self):
        return f"<ANSI Color:{self.red}, {self.green}, {self.blue}>"

    def __int__(self):
        return int(str(self)[1:], 16)

    def __next__(self):
        def make(x):
            return hex(x).replace('0x', '').upper().rjust(6, '0')

        value = int(self) + 1
        if value > 16777215:
            raise StopIteration
        self.set(hexadecimal=make(value))
        return self

    @property
    def ansi_escape_sequence(self):
        return self.get_hex(str(self))

    def set(self, red=..., green=..., blue=..., *, hexadecimal=...):
        """ Use red, green, blue OR hexadecimal.

        **WARNING**: Hexadecimal overwrites red, green and blue.

        Arguments:
            red (int) : The red color: 0 -> 255
            green (int) : The green color: 0 -> 255
            blue (int) : The blue color: 0 -> 255
            hexadecimal (str) : The hexadecimal color: #000000 -> #FFFFFF
        """
        if hexadecimal is not ...:
            if hexadecimal[0] == "#":
                hexadecimal = hexadecimal[1:]
            red = int(hexadecimal[:2], 16)
            green = int(hexadecimal[2:4], 16)
            blue = int(hexadecimal[4:], 16)
        self.red = red
        self.green = green
        self.blue = blue


class Highlight:
    """ Class for control the color of the highlight."""

    @staticmethod
    def get_rgb(red=..., green=..., blue=...):
        """ Get the ANSI escape sequence for an RGB color.

        Arguments:
            red (int) : The red color: 0 -> 255
            green (int) : The green color: 0 -> 255
            blue (int) : The blue color: 0 -> 255

        Returns:
            str : The ANSI escape sequence
        """
        return f"\033[48;2;{red};{green};{blue}m"

    @staticmethod
    def get_hex(hexadecimal):
        """ Get the ANSI escape sequence for a Hex color.

        Arguments:
            hexadecimal (str) : The hexadecimal color: #000000 -> #FFFFFF

        Returns:
            str : The ANSI escape sequence
        """
        if hexadecimal[0] == "#":
            hexadecimal = hexadecimal[1:]
        return Color.get_rgb(
            red=int(hexadecimal[:2], 16),
            green=int(hexadecimal[2:4], 16),
            blue=int(hexadecimal[4:], 16)
        )

    BLACK: str = '\033[40m'
    RED: str = '\033[41m'
    GREEN: str = '\033[42m'
    YELLOW: str = '\033[43m'
    BLUE: str = '\033[44m'
    PURPLE: str = '\033[45m'
    CYAN: str = '\033[46m'
    WHITE: str = '\033[47m'

    LIGHT_BLACK: str = '\033[100m'
    LIGHT_RED: str = '\033[101m'
    LIGHT_GREEN: str = '\033[102m'
    LIGHT_YELLOW: str = '\033[103m'
    LIGHT_BLUE: str = '\033[104m'
    LIGHT_PURPLE: str = '\033[105m'
    LIGHT_CYAN: str = '\033[106m'
    LIGHT_WHITE: str = '\033[107m'

    STOP: str = '\033[49m'

    def __init__(self, red=..., green=..., blue=..., *, hexadecimal=...):
        """ Use red, green, blue OR hexadecimal.

        **WARNING**: Hexadecimal overwrites red, green and blue.

        Arguments:
            red (int) : The red color: 0 -> 255
            green (int) : The green color: 0 -> 255
            blue (int) : The blue color: 0 -> 255
            hexadecimal (str) : The hexadecimal color: #000000 -> #FFFFFF
        """
        self.set(red, green, blue, hexadecimal=hexadecimal)

    def __str__(self):
        """Get the Hexadecimal value"""

        def make(x):
            return hex(x).replace('0x', '').upper().rjust(2, '0')

        return f"#{make(self.red)}{make(self.green)}{make(self.blue)}"

    def __repr__(self):
        return f"<ANSI Highlight:{self.red}, {self.green}, {self.blue}>"

    def __int__(self):
        return int(str(self)[1:], 16)

    def __next__(self):
        def make(x):
            return hex(x).replace('0x', '').upper().rjust(6, '0')

        value = int(self) + 1
        if value > 16777215:
            raise StopIteration
        self.set(hexadecimal=make(value))
        return self

    @property
    def ansi_escape_sequence(self):
        return self.get_hex(str(self))

    def set(self, red=..., green=..., blue=..., *, hexadecimal=...):
        """ Use red, green, blue OR hexadecimal.

        **WARNING**: Hexadecimal overwrites red, green and blue.

        Arguments:
            red (int) : The red color: 0 -> 255
            green (int) : The green color: 0 -> 255
            blue (int) : The blue color: 0 -> 255
            hexadecimal (str) : The hexadecimal color: #000000 -> #FFFFFF
        """
        if hexadecimal is not ...:
            if hexadecimal[0] == "#":
                hexadecimal = hexadecimal[1:]
            red = int(hexadecimal[:2], 16)
            green = int(hexadecimal[2:4], 16)
            blue = int(hexadecimal[4:], 16)
        self.red = red
        self.green = green
        self.blue = blue


class Style:
    """ Class for control the style of the text."""

    BOLD = "\033[1m"
    NO_BOLD = "\033[21m"

    LOW_INTENSITY = "\033[2m"
    NO_LOW_INTENSITY = "\033[22m"

    ITALIC = "\033[3m"
    NO_ITALIC = "\033[23m"

    UNDERLINE = "\033[4m"
    NO_UNDERLINE = "\033[24m"

    SLOWLY_FLASHING = "\033[5m"
    NO_SLOWLY_FLASHING = "\033[25m"

    RAPIDLY_FLASHING = "\033[6m"
    NO_RAPIDLY_FLASHING = "\033[26m"

    NEGATIVE = "\033[7m"
    NO_NEGATIVE = "\033[27m"

    HIDDEN = "\033[8m"
    NO_HIDDEN = "\033[28m"

    STRIKETHROUGH = "\033[9m"
    NO_STRIKETHROUGH = "\033[29m"

    STOP_ALL = generate(*range(21, 30))


def information():
    """ All ANSI code in table

    Returns:
        str: A table of information
    """
    return """\
╔═════════╦══════════════════════════════╦════════════════════════════════════════════════════════════════════════╗
║   Code  ║            Effect            ║                                  Note                                  ║
╠═════════╬══════════════════════════════╬════════════════════════════════════════════════════════════════════════║
║    0    ║        Reset / Normal        ║                      all attributes off (default)                      ║
║    1    ║  Bold or increased intensity ║                                                                        ║
║    2    ║   Dim (decreased intensity)  ║                          Not widely supported.                         ║
║    3    ║            Italic            ║           Not widely supported. Sometimes treated as inverse.          ║
║    4    ║           Underline          ║                                                                        ║
║    5    ║          Slow blink          ║                        less than 150 per minute                        ║
║    6    ║          Rapid blink         ║         MS-DOS ANSI.SYS; 150+ per minute; not widely supported         ║
║    7    ║       [[Inverse video]]      ║                  swap foreground and background colors                 ║
║    8    ║            Conceal           ║                          Not widely supported.                         ║
║    9    ║            Crossed           ║   Characters legible, but marked for deletion. Not widely supported.   ║
║    10   ║    Primary (default) font    ║                                                                        ║
║  11–19  ║        Alternate font        ║                      Select alternate font `n-10`                      ║
║    20   ║            Fraktur           ║                          hardly ever supported                         ║
║    21   ║ Bold off or double underline ║ Bold off not widely supported; double underline hardly ever supported. ║
║    22   ║  Normal color or intensity   ║                         Neither bold nor faint                         ║
║    23   ║    Not italic, not Fraktur   ║                                                                        ║
║    24   ║         Underline off        ║                     Not singly or doubly underlined                    ║
║    25   ║           Blink off          ║                                                                        ║
║    27   ║          Inverse off         ║                                                                        ║
║    28   ║            Reveal            ║                               conceal off                              ║
║    29   ║          Not crossed         ║                                                                        ║
║  30–37  ║     Set foreground color     ║                          See color table below                         ║
║    38   ║     Set foreground color     ║            next arguments are `5;n` or `2;r;g;b`, see below            ║
║    39   ║   Default foreground color   ║             implementation defined (according to standard)             ║
║  40–47  ║     Set background color     ║                          See color table below                         ║
║    48   ║     Set background color     ║            next arguments are `5;n` or `2;r;g;b`, see below            ║
║    49   ║   Default background color   ║             implementation defined (according to standard)             ║
║    51   ║            Framed            ║                                                                        ║
║    52   ║           Encircled          ║                                                                        ║
║    53   ║           Overlined          ║                                                                        ║
║    54   ║    Not framed or encircled   ║                                                                        ║
║    55   ║         Not overlined        ║                                                                        ║
║    60   ║      Ideogram underline      ║                          hardly ever supported                         ║
║    61   ║  Ideogram double underline   ║                          hardly ever supported                         ║
║    62   ║       Ideogram overline      ║                          hardly ever supported                         ║
║    63   ║   Ideogram double overline   ║                          hardly ever supported                         ║
║    64   ║     Ideogram stress mark     ║                          hardly ever supported                         ║
║    65   ║    Ideogram attributes off   ║                     reset the effects of all 60-64                     ║
║  90–97  ║  Set bright foreground color ║                        aixterm (not in standard)                       ║
║ 100–107 ║  Set bright background color ║                        aixterm (not in standard)                       ║
╚═════════╩══════════════════════════════╩════════════════════════════════════════════════════════════════════════╝
"""


STOP = "\033[0m"

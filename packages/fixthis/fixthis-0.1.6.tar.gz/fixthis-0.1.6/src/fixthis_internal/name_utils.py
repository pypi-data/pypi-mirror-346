import unicodedata
def parse_english_number(text: str) -> int:
    """Parse an English‑word number in lowercase with underscores"""
    # 0–19 and tens
    units = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16,
        "seventeen": 17, "eighteen": 18, "nineteen": 19,
    }
    tens = {
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
    }

    # Extendable list of -illion names
    SCALE_NAMES = [
        "thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
        "sextillion", "septillion", "octillion", "nonillion", "decillion",
        "undecillion", "duodecillion", "tredecillion", "quattuordecillion",
        "quindecillion", "sexdecillion", "septendecillion", "octodecillion",
        "novemdecillion", "vigintillion", "centillion",
    ]
    scales = {
        name: 10 ** (i * 3)
        for i, name in enumerate(SCALE_NAMES, start=1)
    }

    numwords = {**units, **tens, **scales, "hundred": 100}

    tokens = text.split("_")
    if not tokens:
        raise ValueError("Empty input")

    negative = False
    if tokens[0] == "minus":
        negative = True
        tokens = tokens[1:]
        if not tokens:
            raise ValueError("Nothing after 'minus'")

    current = total = 0

    for tok in tokens:
        if tok not in numwords:
            raise ValueError(f"Invalid token: {tok!r}")
        val = numwords[tok]

        if val < 100:
            current += val
        elif val == 100:
            current = (current or 1) * 100
        else:
            current = (current or 1) * val
            total += current
            current = 0

    result = total + current
    return -result if negative else result


_ALIASES = {
    # ASCII punctuation
    "PLUS": "+",
    "PLUS_SIGN": "+",
    "MINUS": "-",  # hyphen-minus
    "HYPHEN": "-",
    "SLASH": "/",  # solidus
    "BACKSLASH": "\\",  # reverse solidus
    "STAR": "*",  # asterisk
    "ASTERISK": "*",
    "PERCENT": "%",
    "PERCENT_SIGN": "%",
    "HASH": "#",  # number sign
    "NUMBER": "#",
    "AT": "@",  # commercial at
    "COMMERCIAL_AT": "@",
    "DOLLAR": "$",
    "DOLLAR_SIGN": "$",
    "CARET": "^",  # circumflex accent
    "CIRCUMFLEX": "^",
    "CARET_ACCENT": "^",
    "UNDERSCORE": "_",  # low line
    "LOW_LINE": "_",
    "PIPE": "|",  # vertical line
    "VERTICAL_BAR": "|",
    "TILDE": "~",
    "GRAVE": "`",  # grave accent
    "BACKTICK": "`",
    "QUOTE": "\"",  # quotation mark
    "QUOTE_MARK": "\"",
    "APOSTROPHE": "'",
    "SINGLE_QUOTE": "'",
    "DOT": ".",  # full stop
    "PERIOD": ".",
    "COMMA": ",",
    "SEMICOLON": ";",
    "COLON": ":",
    "QUESTION": "?",
    "QUESTION_MARK": "?",
    "EXCLAMATION": "!",
    "EXCLAMATION_MARK": "!",
    "SP": " ",
    "SPACE": " ",
    "EQ": "=",
    "EQUALS": "=",
    "IS": "=",
    "LESS": "<",
    "MORE": ">",
    "GREATER": ">",


    # German extra letters
    "AE": "Ä",  # LATIN CAPITAL LETTER A WITH DIAERESIS
    "OE": "Ö",
    "UE": "Ü",
    "SS": "ẞ",  # LATIN CAPITAL LETTER SHARP S
    "SZ": "ẞ",
    "AE_SMALL": "ä",
    "OE_SMALL": "ö",
    "UE_SMALL": "ü",
    "SS_SMALL": "ß",
    "SZ_SMALL": "ß",
}


def char_from_name(name: str) -> str:
    """
    Lookup a single character by its name or alias.

    Parameters
    ----------
    name : str
        The character name in uppercase ASCII letters, with underscores for spaces
        (e.g. "PLUS_SIGN", "LATIN_CAPITAL_LETTER_A_WITH_RING_ABOVE", "AE").

    Returns
    -------
    str
        The corresponding single-character string.

    Raises
    ------
    ValueError
        If no alias or Unicode name matches.
    """
    key = name.strip().upper()
    # 1) check aliases
    if key in _ALIASES:
        return _ALIASES[key]
    # 2) try the official Unicode name
    uni_name = key.replace("_", " ")
    try:
        return unicodedata.lookup(uni_name)
    except KeyError:
        raise ValueError(f"No character found for name or alias: {name!r}")

def parse_string(text: str)->str:
    parts = text.split('__')
    res = ""
    number = False
    for part in parts:
        if part.isupper():
            try:
                res += char_from_name(part)
            except ValueError:
                res += part.replace('_', ' ')
        else:
            try:
                res += str(numval := parse_english_number(part))
                number = True
            except:
                res += part.replace('_',  ' ')
    if len(parts) == 1 and number:
        return numval
    return res


import re

from ovos_number_parser.util import (convert_to_mixed_fraction, is_numeric,
                                     look_for_fractions, Scale, GrammaticalGender,
                                     NumberVocabulary, RomanceNumberExtractor)

# Undefined articles ["un", "une"] cannot be supressed,
# in French, "un cheval" means "a horse" or "one horse".
_ARTICLES_FR = ["le", "la", "du", "de", "les", "des"]

_NUMBERS_FR = {
    "zéro": 0,
    "un": 1,
    "une": 1,
    "deux": 2,
    "trois": 3,
    "quatre": 4,
    "cinq": 5,
    "six": 6,
    "sept": 7,
    "huit": 8,
    "neuf": 9,
    "dix": 10,
    "onze": 11,
    "douze": 12,
    "treize": 13,
    "quatorze": 14,
    "quinze": 15,
    "seize": 16,
    "vingt": 20,
    "trente": 30,
    "quarante": 40,
    "cinquante": 50,
    "soixante": 60,
    "soixante-dix": 70,
    "septante": 70,
    "quatre-vingt": 80,
    "quatre-vingts": 80,
    "octante": 80,
    "huitante": 80,
    "quatre-vingt-dix": 90,
    "nonante": 90,
    "cent": 100,
    "cents": 100,
    "mille": 1000,
    "mil": 1000,
    "millier": 1000,
    "milliers": 1000,
    "million": 1000000,
    "millions": 1000000,
    "milliard": 1000000000,
    "milliards": 1000000000,
    "billion": 1000000000000,
    "billions": 1000000000000}

_ORDINAL_ENDINGS_FR = ("er", "re", "ère", "nd", "nde", "ième", "ème", "e")

_NUM_STRING_FR = {
    0: 'zéro',
    1: 'un',
    2: 'deux',
    3: 'trois',
    4: 'quatre',
    5: 'cinq',
    6: 'six',
    7: 'sept',
    8: 'huit',
    9: 'neuf',
    10: 'dix',
    11: 'onze',
    12: 'douze',
    13: 'treize',
    14: 'quatorze',
    15: 'quinze',
    16: 'seize',
    20: 'vingt',
    30: 'trente',
    40: 'quarante',
    50: 'cinquante',
    60: 'soixante',
    70: 'soixante-dix',
    80: 'quatre-vingt',
    90: 'quatre-vingt-dix'
}

_FRACTION_STRING_FR = {
    2: 'demi',
    3: 'tiers',
    4: 'quart',
    5: 'cinquième',
    6: 'sixième',
    7: 'septième',
    8: 'huitième',
    9: 'neuvième',
    10: 'dixième',
    11: 'onzième',
    12: 'douzième',
    13: 'treizième',
    14: 'quatorzième',
    15: 'quinzième',
    16: 'seizième',
    17: 'dix-septième',
    18: 'dix-huitième',
    19: 'dix-neuvième',
    20: 'vingtième'
}


def swap_gender_fr(word, gender):
    """Swap a French number word to the requested grammatical gender.

    Only "un" inflects for gender in the cardinals used here ("un"/"une");
    every other word is returned unchanged.
    """
    if gender == GrammaticalGender.FEMININE and word == "un":
        return "une"
    if gender == GrammaticalGender.MASCULINE and word == "une":
        return "un"
    return word


def pluralize_fr(word):
    """Regular French plural for the scale/hundred words used here."""
    if not word.endswith("s"):
        return word + "s"
    return word


# Number vocabulary driving the shared RomanceNumberExtractor. French is
# vigesimal in the 70s/80s/90s and the standalone twenties/teens are single
# words; the standard-French (France) system used here follows the Académie
# francaise numeral rules and the 1990 rectifications orthographiques
# (Journal officiel de la Republique francaise, 6 dec. 1990) - see the
# extract_number_fr docstring for the full citation. The vigesimal tens and
# the invariable "et"/"tiers"/"demi" quirks are handled by the French hooks
# below rather than by editing the shared engine.
_FR = NumberVocabulary(
    LANG="fr-FR",
    swap_gender=swap_gender_fr,
    pluralize=pluralize_fr,

    HUNDRED_PARTICLE="cent",  # "cent un" - no "un cent"
    DENOMINATOR_PARTICLE="ièmes",
    DIVIDED_BY_ZERO="divisé par zéro",
    NO_PREV_UNIT=[100, 1000],  # "cent"/"mille", never "un cent"/"un mille"
    NO_PLURAL=[1000],  # "mille" is invariable: "deux mille", never "deux milles"

    NUMBER_OVERFLOW="nombre extrêmement grand",
    # French follows the long scale: million 10^6, milliard 10^9, billion 10^12
    DEFAULT_SCALE=Scale.LONG,
    JOIN_WORD=["et"],

    JOINER_ON_TWENTYS=True,   # "vingt et un" (extraction keeps the joiner)
    JOINER_ON_HUNDREDS=False,  # "cent un", never "cent et un"
    JOINER_ON_THOUSANDS=False,
    JOINER_ON_SCALE_REMAINDER=False,

    # the word for hundred multiplies the preceding units ("deux cents" = 200)
    MULTIPLY_HUNDREDS=True,

    DECIMAL_MARKER=["virgule"],
    NEGATIVE_SIGN=["moins"],
    UNITS={
        0: 'zéro',
        1: 'un',
        2: 'deux',
        3: 'trois',
        4: 'quatre',
        5: 'cinq',
        6: 'six',
        7: 'sept',
        8: 'huit',
        9: 'neuf'
    },
    TENS={
        10: 'dix',
        11: 'onze',
        12: 'douze',
        13: 'treize',
        14: 'quatorze',
        15: 'quinze',
        16: 'seize',
        20: 'vingt',
        30: 'trente',
        40: 'quarante',
        50: 'cinquante',
        60: 'soixante'
        # 70/80/90 are vigesimal ("soixante-dix", "quatre-vingts",
        # "quatre-vingt-dix"): they are composed by addition after the French
        # vigesimal hook collapses "quatre-vingt(s)" to a single 80 token, and
        # the regional forms (septante/octante/nonante) are ALT_SPELLINGS.
    },
    HUNDREDS={
        100: 'cent'  # 200-900 are "deux cent" .. "neuf cent" via MULTIPLY_HUNDREDS
    },
    FRACTION={
        2: 'demi',
        3: 'tiers',
        4: 'quart',
        5: 'cinquième',
        6: 'sixième',
        7: 'septième',
        8: 'huitième',
        9: 'neuvième',
        10: 'dixième',
        11: 'onzième',
        12: 'douzième',
        13: 'treizième',
        14: 'quatorzième',
        15: 'quinzième',
        16: 'seizième',
        17: 'dix-septième',
        18: 'dix-huitième',
        19: 'dix-neuvième',
        20: 'vingtième',
        100: 'centième',
        1000: 'millième'
    },
    FRACTION_FEMALE={},
    SHORT_SCALE={
        10 ** 3: "mille",
        10 ** 6: "million",
        10 ** 9: "milliard",
        10 ** 12: "billion"
    },
    LONG_SCALE={
        10 ** 3: "mille",
        10 ** 6: "million",
        10 ** 9: "milliard",
        10 ** 12: "billion",
        10 ** 18: "trillion"
    },
    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {1: "une"},
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={
        "une": 1,
        # Belgian / Swiss regional decades stand as single tens words
        "septante": 70,
        "octante": 80,
        "huitante": 80,
        "nonante": 90,
        # the vigesimal hook collapses "quatre-vingt(s)" to this token
        "quatrevingt": 80,
        "quatrevingts": 80,
        # thousand spelled "mil"/"millier"; accent-free "zero"
        "mil": 1000,
        "millier": 1000,
        "milliers": 1000,
        "zero": 0,
    },
    ORDINAL_UNITS={
        1: 'premier',
        2: 'deuxième',
        3: 'troisième',
        4: 'quatrième',
        5: 'cinquième',
        6: 'sixième',
        7: 'septième',
        8: 'huitième',
        9: 'neuvième'
    },
    ORDINAL_TENS={
        10: 'dixième',
        20: 'vingtième',
        30: 'trentième',
        40: 'quarantième',
        50: 'cinquantième',
        60: 'soixantième',
        70: 'soixante-dixième',
        80: 'quatre-vingtième',
        90: 'quatre-vingt-dixième'
    },
    ORDINAL_HUNDREDS={
        100: 'centième'
    },
    ORDINAL_SHORT_SCALE={
        10 ** 3: "millième",
        10 ** 6: "millionième",
        10 ** 9: "milliardième"
    },
    ORDINAL_LONG_SCALE={
        10 ** 3: "millième",
        10 ** 6: "millionième",
        10 ** 9: "milliardième"
    }
)

FR = RomanceNumberExtractor(_FR)

# "quatre-vingt(s)" (80) and "quatre-vingt-dix" (90) are vigesimal: the shared
# engine accumulates by addition, so "quatre" + "vingt" would give 24. This
# hook collapses "quatre-vingt(s)" - spaced or hyphenated, any case - into a
# single token the vocabulary maps to 80, after which every 80/90 compound is a
# plain addition: 80, 80+1=81, 80+10=90, 80+11=91, 80+10+9=99.
_VIGESIMAL_RE_FR = re.compile(r"\bquatre[\s-]vingts?\b", re.IGNORECASE)

# a bare-digit ordinal such as "2nde" / "21ème" reduces to its digits so the
# engine reads the cardinal ("la 2nde place" -> 2)
_NUMERIC_ORDINAL_RE_FR = re.compile(
    r"\b(\d+)(?:ers?|res?|ère|nde?|ièmes?|èmes?|es?)\b", re.IGNORECASE)


def _collapse_vigesimal_fr(text):
    """Collapse "quatre-vingt(s)" to a single 80 token for the shared engine."""
    return _VIGESIMAL_RE_FR.sub("quatrevingts", text)


def _extract_fraction_fr(text):
    """Resolve a French numerator fraction, or None when there is no fraction.

    French fraction nouns are invariable and multiply the preceding cardinal
    numerator ("un demi" = 1/2, "deux tiers" = 2/3, "trois quarts" = 3/4),
    unlike the shared engine's "and a half" additive model, so they are
    resolved here. Also handles a bare "n/m" slash fraction.
    """
    for token in text.replace("-", " ").split():
        if "/" in token:
            pieces = token.split("/")
            if look_for_fractions(pieces):
                return float(pieces[0]) / float(pieces[1])
    words = text.replace("-", " ").split()
    for idx, word in enumerate(words):
        frac = is_fractional_fr(word)
        if frac is not False:
            if idx == 0:
                return frac
            numerator = FR.extract_number(" ".join(words[:idx]),
                                          scale=_FR.DEFAULT_SCALE)
            if numerator is False:
                return frac
            return numerator * frac
    return None


def nice_number_fr(number, speech=True, denominators=range(1, 21)):
    """ French helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 et demi" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    strNumber = ""
    whole = 0
    num = 0
    den = 0

    result = convert_to_mixed_fraction(number, denominators)

    if not result:
        # Give up, just represent as a 3 decimal number
        whole = round(number, 3)
    else:
        whole, num, den = result

    if not speech:
        if num == 0:
            strNumber = '{:,}'.format(whole)
            strNumber = strNumber.replace(",", " ")
            strNumber = strNumber.replace(".", ",")
            return strNumber
        else:
            return '{} {}/{}'.format(whole, num, den)
    else:
        if num == 0:
            # if the number is not a fraction, nothing to do
            strNumber = str(whole)
            strNumber = strNumber.replace(".", ",")
            return strNumber
        den_str = _FRACTION_STRING_FR[den]
        # if it is not an integer
        if whole == 0:
            # if there is no whole number
            if num == 1:
                # if numerator is 1, return "un demi", for example
                strNumber = 'un {}'.format(den_str)
            else:
                # else return "quatre tiers", for example
                strNumber = '{} {}'.format(num, den_str)
        elif num == 1:
            # if there is a whole number and numerator is 1
            if den == 2:
                # if denominator is 2, return "1 et demi", for example
                strNumber = '{} et {}'.format(whole, den_str)
            else:
                # else return "1 et 1 tiers", for example
                strNumber = '{} et 1 {}'.format(whole, den_str)
        else:
            # else return "2 et 3 quart", for example
            strNumber = '{} et {} {}'.format(whole, num, den_str)
        if num > 1 and den != 3:
            # if the numerator is greater than 1 and the denominator
            # is not 3 ("tiers"), add an s for plural
            strNumber += 's'

    return strNumber


def _pronounce_sub_thousand_fr(n):
    """Spoken form of 0-999."""
    assert 0 <= n <= 999
    if n < 100:
        return pronounce_number_fr(n)
    q, r = divmod(n, 100)
    if q == 1:
        part = "cent"
    else:
        part = pronounce_number_fr(q) + " cent"
        if r == 0:
            part += "s"  # "deux cents" but "deux cent un"
    if r:
        part += " " + pronounce_number_fr(r)
    return part


def _pronounce_whole_number_fr(n):
    """Spoken form of any whole number below 10^15.

    French uses the long scale, where each new named magnitude is 10^6
    times the previous one: million = 10^6, milliard = 10^9,
    billion = 10^12 (see Wikipedia, "Long and short scales",
    https://en.wikipedia.org/wiki/Long_and_short_scales). This differs
    from the short scale where "billion" means 10^9.
    """
    assert n >= 0
    if n < 1000:
        return _pronounce_sub_thousand_fr(n)
    if n < 10 ** 6:
        thousands, rest = divmod(n, 1000)
        part = "mille" if thousands == 1 \
            else _pronounce_sub_thousand_fr(thousands) + " mille"
        if rest:
            part += " " + _pronounce_sub_thousand_fr(rest)
        return part
    if n < 10 ** 9:
        millions, rest = divmod(n, 10 ** 6)
        part = "un million" if millions == 1 \
            else _pronounce_whole_number_fr(millions) + " millions"
        if rest:
            part += " " + _pronounce_whole_number_fr(rest)
        return part
    if n < 10 ** 12:
        milliards, rest = divmod(n, 10 ** 9)
        part = "un milliard" if milliards == 1 \
            else _pronounce_whole_number_fr(milliards) + " milliards"
        if rest:
            part += " " + _pronounce_whole_number_fr(rest)
        return part
    billions, rest = divmod(n, 10 ** 12)
    part = "un billion" if billions == 1 \
        else _pronounce_whole_number_fr(billions) + " billions"
    if rest:
        part += " " + _pronounce_whole_number_fr(rest)
    return part


def pronounce_number_fr(number, places=2):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'cinq virgule deux'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    result = ""
    if number < 0:
        result = "moins "
    number = abs(number)

    # Scientific-notation floats (very small or very large magnitudes) have
    # no long-scale word form and str() renders them with an exponent, which
    # has no "." to split for the decimal part. Return the numeric string
    # rather than raising.
    if number != 0 and (number >= 10 ** 15 or number < 1e-4):
        return result + str(number)

    if number >= 100:
        if number >= 10 ** 15 or int(number) != number and number >= 1000:
            return result + str(number)
        result += _pronounce_whole_number_fr(int(number))
        if number != int(number) and places > 0:
            result += " virgule"
            _num_str = str(number).split(".")[1][0:places]
            for char in _num_str:
                result += " " + _NUM_STRING_FR[int(char)]
        return result

    if number > 16:
        tens = int(number - int(number) % 10)
        ones = int(number - tens)
        if ones != 0:
            if tens > 10 and tens <= 60 and int(number - tens) == 1:
                result += _NUM_STRING_FR[tens] + "-et-" + _NUM_STRING_FR[ones]
            elif number == 71:
                result += "soixante-et-onze"
            elif tens == 70:
                result += _NUM_STRING_FR[60] + "-"
                if ones < 7:
                    result += _NUM_STRING_FR[10 + ones]
                else:
                    result += _NUM_STRING_FR[10] + "-" + _NUM_STRING_FR[ones]
            elif tens == 90:
                result += _NUM_STRING_FR[80] + "-"
                if ones < 7:
                    result += _NUM_STRING_FR[10 + ones]
                else:
                    result += _NUM_STRING_FR[10] + "-" + _NUM_STRING_FR[ones]
            else:
                result += _NUM_STRING_FR[tens] + "-" + _NUM_STRING_FR[ones]
        else:
            if number == 80:
                result += "quatre-vingts"
            else:
                result += _NUM_STRING_FR[tens]
    else:
        result += _NUM_STRING_FR[int(number)]

    # Deal with decimal part
    if not number == int(number) and places > 0:
        if abs(number) < 1.0 and (result == "moins " or not result):
            result += "zéro"
        result += " virgule"
        _num_str = str(number)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + _NUM_STRING_FR[int(char)]
    return result


def _number_parse_fr(words, i):
    """ Parses a list of words to find a number
    Takes in a list of words (strings without whitespace) and
    extracts a number that starts at the given index.
    Args:
        words (array): the list to extract a number from
        i (int): the index in words where to look for the number
    Returns:
        tuple with number, index of next word after the number.

        Returns None if no number was found.
    """

    def cte_fr(i, s):
        # Check if string s is equal to words[i].
        # If it is return tuple with s, index of next word.
        # If it is not return None.
        if i < len(words) and s == words[i]:
            return s, i + 1
        return None

    def number_word_fr(i, mi, ma):
        # Check if words[i] is a number in _NUMBERS_FR between mi and ma.
        # If it is return tuple with number, index of next word.
        # If it is not return None.
        if i < len(words):
            val = _NUMBERS_FR.get(words[i])
            # Numbers [1-16,20,30,40,50,60,70,80,90,100,1000]
            if val is not None:
                if val >= mi and val <= ma:
                    return val, i + 1
                else:
                    return None
            # The number may be hyphenated (numbers [17-999])
            splitWord = words[i].split('-')
            if len(splitWord) > 1:
                val1 = _NUMBERS_FR.get(splitWord[0])
                if val1:
                    i1 = 0
                    val2 = 0
                    val3 = 0
                    if val1 < 10 and splitWord[1] == "cents":
                        val1 = val1 * 100
                        i1 = 2

                    # For [81-99], e.g. "quatre-vingt-deux"
                    if len(splitWord) > i1 and splitWord[0] == "quatre" and \
                            splitWord[1] == "vingt":
                        val1 = 80
                        i1 += 2

                    # We still found a number
                    if i1 == 0:
                        i1 = 1

                    if len(splitWord) > i1:
                        # For [21,31,41,51,61,71]
                        if len(splitWord) > i1 + 1 and splitWord[i1] == "et":
                            val2 = _NUMBERS_FR.get(splitWord[i1 + 1])
                            if val2 is not None:
                                i1 += 2
                        # For [77-79],[97-99] e.g. "soixante-dix-sept"
                        elif splitWord[i1] == "dix" and \
                                len(splitWord) > i1 + 1:
                            val2 = _NUMBERS_FR.get(splitWord[i1 + 1])
                            if val2 is not None:
                                val2 += 10
                                i1 += 2
                        else:
                            val2 = _NUMBERS_FR.get(splitWord[i1])
                            if val2 is not None:
                                i1 += 1
                                if len(splitWord) > i1:
                                    val3 = _NUMBERS_FR.get(splitWord[i1])
                                    if val3 is not None:
                                        i1 += 1

                        if val2:
                            if val3:
                                val = val1 + val2 + val3
                            else:
                                val = val1 + val2
                        else:
                            return None
                    if i1 == len(splitWord) and val and ma >= val >= mi:
                        return val, i + 1

        return None

    def number_1_99_fr(i):
        # Check if words[i] is a number between 1 and 99.
        # If it is return tuple with number, index of next word.
        # If it is not return None.

        # Is it a number between 1 and 16?
        result1 = number_word_fr(i, 1, 16)
        if result1:
            return result1

        # Is it a number between 10 and 99?
        result1 = number_word_fr(i, 10, 99)
        if result1:
            val1, i1 = result1
            result2 = cte_fr(i1, "et")
            # If the number is not hyphenated [21,31,41,51,61,71]
            if result2:
                i2 = result2[1]
                result3 = number_word_fr(i2, 1, 11)
                if result3:
                    val3, i3 = result3
                    return val1 + val3, i3
            return result1

        # It is not a number
        return None

    def number_1_999_fr(i):
        # Check if words[i] is a number between 1 and 999.
        # If it is return tuple with number, index of next word.
        # If it is not return None.

        # Is it 100 ?
        result = number_word_fr(i, 100, 100)

        # Is it [200,300,400,500,600,700,800,900]?
        if not result:
            resultH1 = number_word_fr(i, 2, 9)
            if resultH1:
                valH1, iH1 = resultH1
                resultH2 = number_word_fr(iH1, 100, 100)
                if resultH2:
                    iH2 = resultH2[1]
                    result = valH1 * 100, iH2

        if result:
            val1, i1 = result
            result2 = number_1_99_fr(i1)
            if result2:
                val2, i2 = result2
                return val1 + val2, i2
            else:
                return result

        # Is it hyphenated? [101-999]
        result = number_word_fr(i, 101, 999)
        if result:
            return result

        # [1-99]
        result = number_1_99_fr(i)
        if result:
            return result

        return None

    def number_1_999999_fr(i):
        """ Find a number in a list of words
        Checks if words[i] is a number between 1 and 999,999.

        Args:
            i (int): the index in words where to look for the number
        Returns:
            tuple with number, index of next word after the number.

            Returns None if no number was found.
        """

        # check for zero
        result1 = number_word_fr(i, 0, 0)
        if result1:
            return result1

        # check for [1-999]
        result1 = number_1_999_fr(i)
        if result1:
            val1, i1 = result1
        else:
            val1 = 1
            i1 = i
        # check for 1000
        result2 = number_word_fr(i1, 1000, 1000)
        if result2:
            # it's [1000-999000]
            i2 = result2[1]
            # check again for [1-999]
            result3 = number_1_999_fr(i2)
            if result3:
                val3, i3 = result3
                return val1 * 1000 + val3, i3
            else:
                return val1 * 1000, i2
        elif result1:
            return result1
        return None

    def number_1_billions_fr(i):
        # Check for numbers including millions and milliards.
        result1 = number_1_999999_fr(i)
        if result1:
            val1, i1 = result1
        else:
            val1, i1 = 1, i
        # check for million(s) / milliard(s) / billion(s)
        result2 = number_word_fr(i1, 1000000, 1000000000000)
        if result2:
            scale, i2 = result2
            result3 = number_1_billions_fr(i2)
            if result3 and result3[0] < scale:
                return val1 * scale + result3[0], result3[1]
            return val1 * scale, i2
        elif result1:
            return result1
        return None

    return number_1_billions_fr(i)


def _get_ordinal_fr(word):
    """ Get the ordinal number
    Takes in a word (string without whitespace) and
    extracts the ordinal number.
    Args:
        word (string): the word to extract the number from
    Returns:
        number (int)

        Returns None if no ordinal number was found.
    """
    if word:
        for ordinal in _ORDINAL_ENDINGS_FR:
            if word[0].isdigit() and ordinal in word:
                result = word.replace(ordinal, "")
                if result.isdigit():
                    return int(result)

    return None


def _number_ordinal_fr(words, i):
    """ Find an ordinal number in a list of words
    Takes in a list of words (strings without whitespace) and
    extracts an ordinal number that starts at the given index.
    Args:
        words (array): the list to extract a number from
        i (int): the index in words where to look for the ordinal number
    Returns:
        tuple with ordinal number (str),
        index of next word after the number (int).

        Returns None if no ordinal number was found.
    """
    val1 = None
    strOrd = ""
    # it's already a digit, normalize to "1er" or "5e"
    val1 = _get_ordinal_fr(words[i])
    if val1 is not None:
        if val1 == 1:
            strOrd = "1er"
        else:
            strOrd = str(val1) + "e"
        return strOrd, i + 1

    # if it's a big number the beginning should be detected as a number
    result = _number_parse_fr(words, i)
    if result:
        val1, i = result
    else:
        val1 = 0

    if i < len(words):
        word = words[i]
        if word in ["premier", "première"]:
            strOrd = "1er"
        elif word == "second":
            strOrd = "2e"
        elif word.endswith("ième"):
            val2 = None
            word = word[:-4]
            # centième
            if word == "cent":
                if val1:
                    strOrd = str(val1 * 100) + "e"
                else:
                    strOrd = "100e"
            # millième
            elif word == "mill":
                if val1:
                    strOrd = str(val1 * 1000) + "e"
                else:
                    strOrd = "1000e"
            else:
                # "cinquième", "trente-cinquième"
                if word.endswith("cinqu"):
                    word = word[:-1]
                # "neuvième", "dix-neuvième"
                elif word.endswith("neuv"):
                    word = word[:-1] + "f"
                result = _number_parse_fr([word], 0)
                if not result:
                    # "trentième", "douzième"
                    word = word + "e"
                    result = _number_parse_fr([word], 0)
                if result:
                    val2, i = result
                if val2 is not None:
                    strOrd = str(val1 + val2) + "e"
        if strOrd:
            return strOrd, i + 1

    return None


def extract_number_fr(text, short_scale=True, ordinals=False):
    """Extract a number from standard-French (France) text.

    Delegates to the shared :class:`RomanceNumberExtractor`. The heavy legacy
    recursive parser is replaced by a French :class:`NumberVocabulary` plus two
    French hooks: a vigesimal collapse of "quatre-vingt(s)" so 80/90 compounds
    add correctly, and a numerator-fraction resolver for the invariable "demi"/
    "tiers"/"quart".

    French keeps the composite tens the Académie française prescribes: the
    seventies compose as 60 + teens ("soixante-dix" 70, "soixante et onze" 71,
    "soixante-douze" 72 … "soixante-dix-neuf" 79); the eighties as 4 × 20
    ("quatre-vingts" 80, "quatre-vingt-un" 81 … "quatre-vingt-neuf" 89) and the
    nineties as 80 + teens ("quatre-vingt-dix" 90, "quatre-vingt-onze" 91 …
    "quatre-vingt-dix-neuf" 99). The conjunction "et" appears only in "vingt et
    un" (21), "trente et un" (31) … "soixante et un" (61) and "soixante et
    onze" (71); never in "quatre-vingt-un" (81) or "quatre-vingt-onze" (91).
    "cent" takes the plural -s only when it closes a round number ("deux cents"
    200, but "deux cent un" 201); "mille" is invariable ("deux mille"). Both
    the traditional spaced spellings and the hyphenated forms of the 1990
    rectifications orthographiques ("vingt-et-un", "trois-cent-cinquante") are
    accepted on input.

    Sources: Académie française, "Questions de langue - Nombres (écriture,
    accord)" (https://www.academie-francaise.fr/questions-de-langue#57_strong-em-nombres-em-strong)
    and the 1990 rectifications orthographiques, Journal officiel de la
    République française, "Les rectifications de l'orthographe", 6 December
    1990 (deposited under ~/AgentWorkspaces/papers/general/).

    The scale is always the long scale used in France (milliard 10^9, billion
    10^12); ``short_scale`` is kept for API compatibility but does not change
    the result.

    Args:
        text (str): the string to extract a number from
        short_scale (bool): accepted for API compatibility; France always uses
            the long scale
        ordinals (bool): also recognise ordinal words
    Returns:
        (int, float) or False: the extracted number, or False if none is found
    """
    if not isinstance(text, str):
        return False

    # reduce bare-digit ordinals to their digits so the engine reads them
    prepared = _NUMERIC_ORDINAL_RE_FR.sub(r"\1", text)

    # French numerator fractions ("un demi", "deux tiers", "2/3") multiply
    # rather than add, so they are resolved before the cardinal engine
    fraction = _extract_fraction_fr(prepared)
    if fraction is not None:
        return fraction

    prepared = _collapse_vigesimal_fr(prepared)
    result = FR.extract_number(prepared, ordinals=ordinals,
                               scale=_FR.DEFAULT_SCALE)
    return result


def is_fractional_fr(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.
    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    input_str = input_str.lower()

    if input_str != "tiers" and input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "quarts"

    aFrac = ["entier", "demi", "tiers", "quart", "cinquième", "sixième",
             "septième", "huitième", "neuvième", "dixième", "onzième",
             "douzième", "treizième", "quatorzième", "quinzième", "seizième",
             "dix-septième", "dix-huitième", "dix-neuvième", "vingtième"]

    if input_str in aFrac:
        return 1.0 / (aFrac.index(input_str) + 1)
    if _get_ordinal_fr(input_str):
        return 1.0 / _get_ordinal_fr(input_str)
    if input_str == "trentième":
        return 1.0 / 30
    if input_str == "centième":
        return 1.0 / 100
    if input_str == "millième":
        return 1.0 / 1000

    return False


def normalize_fr(text, remove_articles=True):
    """ French string normalization """
    text = text.lower()
    words = text.split()  # this also removed extra spaces
    normalized = ""
    i = 0
    while i < len(words):
        # remove articles
        if remove_articles and words[i] in _ARTICLES_FR:
            i += 1
            continue
        if remove_articles and words[i][:2] in ["l'", "d'"]:
            words[i] = words[i][2:]
        # remove useless punctuation signs
        if words[i] in ["?", "!", ";", "…"]:
            i += 1
            continue
        # Normalize ordinal numbers
        if i > 0 and words[i - 1] in _ARTICLES_FR:
            result = _number_ordinal_fr(words, i)
            if result is not None:
                val, i = result
                normalized += " " + str(val)
                continue
        # Convert numbers into digits
        result = _number_parse_fr(words, i)
        if result is not None:
            val, i = result
            normalized += " " + str(val)
            continue

        normalized += " " + words[i]
        i += 1

    return normalized[1:]  # strip the initial space

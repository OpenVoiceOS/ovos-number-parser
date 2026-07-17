from ovos_number_parser.util import (convert_to_mixed_fraction, look_for_fractions,
                                     is_numeric)

_NUM_STRING_EU = {
    "zero": 0,
    "bat": 1,
    "bi": 2,
    "hiru": 3,
    "lau": 4,
    "bost": 5,
    "sei": 6,
    "zazpi": 7,
    "zortzi": 8,
    "bederatzi": 9,
    "hamar": 10,
    "hamaika": 11,
    "hamabi": 12,
    "hamahiru": 13,
    "hamalau": 14,
    "hamabost": 15,
    "hamasei": 16,
    "hamazazpi": 17,
    "hemezortzi": 18,
    "hemeretzi": 19,
    "hogei": 20,
    "hogeita hamar": 30,
    "hogeita hamaika": 31,
    "berrogei": 40,
    "berrogeita hamar": 50,
    "hirurogei": 60,
    "hirurogeita hamar": 70,
    "laurogei": 80,
    "laurogeita hamar": 90,
    "ehun": 100,
    "berrehun": 200,
    "hirurehun": 300,
    "laurehun": 400,
    "bostehun": 500,
    "seiehun": 600,
    "zazpiehun": 700,
    "zortziehun": 800,
    "bederatziehun": 900,
    # legacy "-rehun" spellings still accepted on input for back-compat
    "seirehun": 600,
    "zazpirehun": 700,
    "zortzirehun": 800,
    "bederatzirehun": 900,
    "mila": 1000,
    "milioi": 1000000,
    "bilioi": 1000000000}

NUM_STRING_EU = {
    0: 'zero',
    1: 'bat',
    2: 'bi',
    3: 'hiru',
    4: 'lau',
    5: 'bost',
    6: 'sei',
    7: 'zazpi',
    8: 'zortzi',
    9: 'bederatzi',
    10: 'hamar',
    11: 'hamaika',
    12: 'hamabi',
    13: 'hamahiru',
    14: 'hamalau',
    15: 'hamabost',
    16: 'hamasei',
    17: 'hamazazpi',
    18: 'hemezortzi',
    19: 'hemeretzi',
    20: 'hogei',
    30: 'hogeita hamar',
    40: 'berrogei',
    50: 'berrogeita hamar',
    60: 'hirurogei',
    70: 'hirurogeita hamar',
    80: 'laurogei',
    90: 'laurogeita hamar',
    100: 'ehun',
    200: 'berrehun',
    300: 'hirurehun',
    400: 'laurehun',
    500: 'bostehun',
    600: 'seiehun',
    700: 'zazpiehun',
    800: 'zortziehun',
    900: 'bederatziehun',
    1000: 'mila'
}

FRACTION_STRING_EU = {
    2: 'erdi',
    3: 'heren',
    4: 'laurden',
    5: 'bosten',
    6: 'seiren',
    7: 'zazpiren',
    8: 'zortziren',
    9: 'bederatziren',
    10: 'hamarren',
    11: 'hamaikaren',
    12: 'hamabiren',
    13: 'hamahiruren',
    14: 'hamalauren',
    15: 'hamabosten',
    16: 'hamaseiren',
    17: 'hamazazpiren',
    18: 'hemezortziren',
    19: 'hemeretziren',
    20: 'hogeiren'
}


def nice_number_eu(number, speech=True, denominators=range(1, 21)):
    """ Euskara helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 eta erdi" for speech and "4 1/2" for text

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
        den_str = FRACTION_STRING_EU[den]
        # if it is not an integer
        if whole == 0:
            # if there is no whole number
            if num == 1:
                # if numerator is 1, return "un medio", for example
                strNumber = '{} bat'.format(den_str)
            else:
                # else return "cuatro tercios", for example
                strNumber = '{} {}'.format(num, den_str)
        elif num == 1:
            # if there is a whole number and numerator is 1
            if den == 2:
                # if denominator is 2, return "1 y medio", for example
                strNumber = '{} eta {}'.format(whole, den_str)
            else:
                # else return "1 y 1 tercio", for example
                strNumber = '{} eta {} bat'.format(whole, den_str)
        else:
            # else return "2 y 3 cuarto", for example
            strNumber = '{} eta {} {}'.format(whole, num, den_str)

    return strNumber


# Vigesimal (base-20) cardinal composer.
#
# Basque tens are built on ``hogei`` (20), ``berrogei`` (40 = 2x20),
# ``hirurogei`` (60 = 3x20) and ``laurogei`` (80 = 4x20); 30/50/70/90 are the
# preceding twenty *plus ten* (``hogeita hamar`` = 20-and-10 = 30). The
# copulative ``eta`` ("and") joins groups and contracts to ``-ta`` on the
# twenties (``hogeita hamaika`` = 31). Spelled verbatim / composed from the
# rules in Euskaltzaindia Araua 7 ("Zenbakien idazkeraz", 1994).
_AND_EU = "eta"

_TWENTIES_EU = {1: "hogei", 2: "berrogei", 3: "hirurogei", 4: "laurogei"}


def _under_100_eu(n):
    if n < 20:
        return NUM_STRING_EU[n]
    twenties, rem = divmod(n, 20)
    head = _TWENTIES_EU[twenties]
    if rem == 0:
        return head
    # ``eta`` contracts to ``-ta`` on the twenty head (hogei+eta -> hogeita),
    # but the "ten" stays a separate word (Araua 7: hogeita hamar, never
    # *hogeitamar).
    return f"{head}ta {NUM_STRING_EU[rem]}"


def _under_1000_eu(n):
    if n < 100:
        return _under_100_eu(n)
    hundreds, rem = divmod(n, 100)
    head = NUM_STRING_EU[100] if hundreds == 1 else NUM_STRING_EU[hundreds * 100]
    if rem == 0:
        return head
    return f"{head} {_AND_EU} {_under_100_eu(rem)}"


def _join_rem_eu(rem):
    # Araua 7 ("Oharrak"): ``eta`` links the last two chunks but drops when a
    # lower remainder follows the hundreds -- ``mila eta berrehun`` (1200) vs
    # ``mila berrehun eta bi`` (1202). ``eta`` is inserted only when the
    # remainder is a single terminal chunk (below 100, or a bare hundreds
    # multiple); a remainder carrying its own internal ``eta`` is juxtaposed.
    if rem < 100 or rem % 100 == 0:
        return f"{_AND_EU} {_spell_cardinal_eu(rem)}"
    return _spell_cardinal_eu(rem)


def _spell_cardinal_eu(n):
    """Spell a non-negative integer as a Basque cardinal (vigesimal)."""
    if n == 0:
        return NUM_STRING_EU[0]
    if n < 1000:
        return _under_1000_eu(n)
    for divisor, word in ((1_000_000_000, "bilioi"), (1_000_000, "milioi")):
        if n >= divisor:
            count, rem = divmod(n, divisor)
            # "a million" is "milioi bat"; N million is "<N> milioi"
            head = f"{word} {NUM_STRING_EU[1]}" if count == 1 \
                else f"{_under_1000_eu(count)} {word}"
            return head if rem == 0 else f"{head} {_join_rem_eu(rem)}"
    # thousands
    thousands, rem = divmod(n, 1000)
    # 1000 is bare "mila", not "*bat mila"
    head = NUM_STRING_EU[1000] if thousands == 1 \
        else f"{_under_1000_eu(thousands)} {NUM_STRING_EU[1000]}"
    return head if rem == 0 else f"{head} {_join_rem_eu(rem)}"


def pronounce_number_eu(num, places=2):
    """
    Convert a number to its spoken Basque equivalent.

    For example, '5.2' would return 'bost koma bi'. Integers of any magnitude
    up to the thousand-millions (``bilioi``) are composed with the vigesimal
    ``eta`` rule of Euskaltzaindia Araua 7 ("Zenbakien idazkeraz", 1994); the
    fractional part is read digit by digit after ``koma``.

    Args:
        num(float or int): the number to pronounce
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number
    """
    result = ""
    if num < 0:
        result = "minus "
    num = abs(num)

    whole = int(num)
    result += _spell_cardinal_eu(whole)

    # Deal with decimal part; in Basque the comma is commonly used instead of
    # the dot, and when pronounced it is read as "koma".
    if not num == int(num) and places > 0:
        result += " koma"
        _num_str = str(num).split(".")[1][0:places]
        for char in _num_str:
            result += " " + NUM_STRING_EU[int(char)]

    return result


# Ordinals: the suffix is ``-garren``; 1st is suppletive (``lehenengo`` /
# ``lehen``) and ``bost`` drops its ``t`` before the suffix (``bosgarren``, not
# *bostgarren). Spelled / ruled in Euskaltzaindia Araua 18 ("Ordinalen eta
# banatzaileen idazkera", 1994).
_ORDINAL_SUFFIX_EU = "garren"

ORDINAL_BASE_EU = {
    1: "lehenengo",
    2: "bigarren",
    3: "hirugarren",
    4: "laugarren",
    5: "bosgarren",
    6: "seigarren",
    7: "zazpigarren",
    8: "zortzigarren",
    9: "bederatzigarren",
    10: "hamargarren",
}


def _ordinalize_word_eu(word):
    if word.endswith("bost"):
        word = word[:-1]  # bost -> bos (bosgarren)
    return f"{word}{_ORDINAL_SUFFIX_EU}"


def pronounce_ordinal_eu(num):
    """
    Convert an integer to its spoken Basque ordinal (``-garren``).

    1-10 use the attested table (1st suppletive ``lehenengo``). Above ten the
    suffix attaches to the cardinal's final element, with the euphonic
    ``bost`` -> ``bos`` drop (``hamabost`` -> ``hamabosgarren``).
    """
    num = int(num)
    if num in ORDINAL_BASE_EU:
        return ORDINAL_BASE_EU[num]
    words = _spell_cardinal_eu(num).split()
    words[-1] = _ordinalize_word_eu(words[-1])
    return " ".join(words)


# both suppletive forms for "first" are attested; pronunciation emits
# lehenengo, extraction accepts either
_ORDINAL_VARIANTS_EU = {"lehen": 1}


def is_ordinal_eu(input_str):
    """Return the number an ordinal string denotes, or False."""
    s = input_str.lower().strip()
    if s in _ORDINAL_VARIANTS_EU:
        return _ORDINAL_VARIANTS_EU[s]
    for value, word in ORDINAL_BASE_EU.items():
        if s == word:
            return value
    if s.endswith(_ORDINAL_SUFFIX_EU):
        stem = s[:-len(_ORDINAL_SUFFIX_EU)]
        if stem.endswith("bos"):
            stem += "t"  # bos- -> bost for lookup
        val = extract_number_eu(stem)
        if val is not False:
            return val
    return False


def is_fractional_eu(input_str):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        text (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "fifths"

    aFrac = {"erdia": 2, "erdi": 2, "heren": 3, "laurden": 4,
             "laurdena": 4, "bosten": 5, "bostena": 5, "seiren": 6, "seirena": 6,
             "zazpiren": 7, "zapirena": 7, "zortziren": 8, "zortzirena": 8,
             "bederatziren": 9, "bederatzirena": 9, "hamarren": 10, "hamarrena": 10,
             "hamaikaren": 11, "hamaikarena": 11, "hamabiren": 12, "hamabirena": 12}

    if input_str.lower() in aFrac:
        return 1.0 / aFrac[input_str]
    if (input_str == "hogeiren" or input_str == "hogeirena"):
        return 1.0 / 20
    if (input_str == "hogeita hamarren" or input_str == "hogeita hamarrena"):
        return 1.0 / 30
    if (input_str == "ehunen" or input_str == "ehunena"):
        return 1.0 / 100
    if (input_str == "milaren" or input_str == "milarena"):
        return 1.0 / 1000
    return False


# Scale words that flush the accumulated group; everything else (units,
# teens, the vigesimal twenties and the lexical hundreds) adds into the
# current group, because Basque composes tens and hundreds additively:
# "berrehun eta berrogeita hamasei" = 200 + (40 + 16) = 256 (Euskaltzaindia
# Araua 7, "Zenbakien idazkeraz", 1994).
_SCALES_EU = (1000, 1000000, 1000000000)


def _word_value_eu(word):
    """Value of a single Basque cardinal token, or None.

    Handles the vigesimal ``-ta`` joiner form of the twenties: ``hogeita``
    (from ``hogei`` 20), ``berrogeita`` (40), ``hirurogeita`` (60) and
    ``laurogeita`` (80), which are written joined to the following ten/unit
    (Araua 7).
    """
    if word in _NUM_STRING_EU:
        return _NUM_STRING_EU[word]
    if word.endswith("ta"):
        stem = word[:-2]
        if stem in _NUM_STRING_EU and _NUM_STRING_EU[stem] in (20, 40, 60, 80):
            return _NUM_STRING_EU[stem]
    return None


# TODO: short_scale and ordinals don't do anything here.
# The parameters are present in the function signature for API compatibility
# reasons.
def extract_number_eu(text, short_scale=True, ordinals=False):
    """
    Extract the first number from Basque text.

    Basque cardinals are vigesimal and compose additively: the twenties
    (``hogei``, ``berrogei``, ``hirurogei``, ``laurogei``) and the lexical
    hundreds (``berrehun`` 200 ...) join their remainders with ``eta``, and a
    trailing scale word multiplies the whole preceding group ("berrehun eta
    berrogeita hamasei mila" = (200 + 56) x 1000 = 256000). The composition is
    that of Euskaltzaindia Araua 7 ("Zenbakien idazkeraz", 1994); ``milioi``
    and ``bilioi`` take the head-final "bat" idiom for a count of one
    ("milioi bat" = 1000000).

    Args:
        text (str): the string to normalize
    Returns:
        (int) or (float): The value of extracted number, or False
    """
    aWords = text.lower().split()
    negative = False
    while aWords and aWords[0] in ('minus', 'ken'):
        negative = True
        aWords = aWords[1:]

    decimals = ('puntu', 'koma', '.', ',')
    total = 0          # sum of flushed scale groups
    current = 0        # value being built for the current scale group
    result = None      # explicit result (decimal / fraction), overrides total
    got_number = False
    idx = 0
    n = len(aWords)
    while idx < n:
        word = aWords[idx]

        if word == 'eta':          # copulative joiner, carries no value
            idx += 1
            continue

        if word in decimals and got_number:
            # read the decimal tail digit by digit ("koma bat lau" -> .14)
            digits = ""
            j = idx + 1
            while j < n:
                w = aWords[j]
                if w.isdigit():
                    digits += w
                else:
                    dv = _word_value_eu(w)
                    if dv is not None and dv < 10:
                        digits += str(dv)
                    else:
                        break
                j += 1
            if digits:
                result = float(f"{total + current}.{digits}")
                idx = j
            break

        val = _word_value_eu(word)
        if val is not None:
            got_number = True
            if val in _SCALES_EU:
                if val == 1000:
                    total += (current or 1) * val
                elif current:
                    total += current * val
                else:
                    # bare "milioi"/"bilioi": count is one, spelled with a
                    # following "bat" ("milioi bat" = 1000000)
                    total += val
                    if idx + 1 < n and aWords[idx + 1] == 'bat':
                        idx += 1
                current = 0
            else:
                current += val
            idx += 1
            continue

        if word.isdigit():
            current += int(word)
            got_number = True
            idx += 1
            continue

        if is_numeric(word):
            result = float(word)
            got_number = True
            idx += 1
            break

        aPieces = word.split('/')
        if look_for_fractions(aPieces):
            result = float(aPieces[0]) / float(aPieces[1])
            got_number = True
            idx += 1
            break

        frac = is_fractional_eu(word)
        if frac:
            base = (total + current) if got_number else 1
            if not got_number and idx + 1 < n:
                nxt = _word_value_eu(aWords[idx + 1])
                if nxt is not None:
                    # "erdi bat", "bi heren"
                    base = nxt
                    idx += 1
            result = base * frac
            got_number = True
            idx += 1
            break

        # unrecognised token: skip leading junk until a number begins, but
        # stop once the running number is interrupted by non-number text
        if got_number:
            break
        idx += 1

    if result is None:
        if not got_number:
            return False
        result = total + current

    if isinstance(result, float) and result.is_integer():
        result = int(result)

    if negative:
        result = -result
    return result if result is not False else False


# TODO Not parsing 'cero'
def eu_number_parse(words, i):
    def eu_cte(i, s):
        if i < len(words) and s == words[i]:
            return s, i + 1
        return None

    def eu_number_word(i, mi, ma):
        if i < len(words):
            v = _NUM_STRING_EU.get(words[i])
            if v and v >= mi and v <= ma:
                return v, i + 1
        return None

    def eu_number_1_99(i):
        if i >= len(words):
            return None
        r1 = eu_number_word(i, 1, 29)
        if r1:
            return r1

        composed = False
        if words[i] != "eta" and words[i][-2:] == "ta":
            composed = True
            words[i] = words[i][:-2]

        r1 = eu_number_word(i, 20, 90)

        if r1:
            v1, i1 = r1

            if composed:
                # i2 = r2[1]
                r3 = eu_number_word(i1, 1, 19)
                if r3:
                    v3, i3 = r3
                    return v1 + v3, i3
            return r1
        return None

    def eu_number_1_999(i):
        r1 = eu_number_word(i, 100, 900)
        if r1:
            v1, i1 = r1
            r2 = eu_cte(i1, "eta")
            if r2:
                i2 = r2[1]
                r3 = eu_number_1_99(i2)
                if r3:
                    v3, i3 = r3
                    return v1 + v3, i3
            else:
                return r1

        # [1-99]
        r1 = eu_number_1_99(i)
        if r1:
            return r1

        return None

    def eu_number(i):
        # check for cero
        r1 = eu_number_word(i, 0, 0)
        if r1:
            return r1

        # check for [1-999] (mil [0-999])?
        r1 = eu_number_1_999(i)
        if r1:
            v1, i1 = r1
            r2 = eu_cte(i1, "mila")
            if r2:
                i2 = r2[1]
                r3 = eu_number_1_999(i2)
                if r3:
                    v3, i3 = r3
                    return v1 * 1000 + v3, i3
                else:
                    return v1 * 1000, i2
            else:
                return r1
        return None

    return eu_number(i)

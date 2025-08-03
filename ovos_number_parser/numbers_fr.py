from ovos_number_parser.util import convert_to_mixed_fraction, is_numeric, look_for_fractions

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
    "milliards": 1000000000}

_ORDINAL_ENDINGS_FR = ("er", "re", "ère", "nd", "nde" "ième", "ème", "e")

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
    if abs(number) >= 100:
        # TODO: Support for numbers over 100
        return str(number)

    result = ""
    if number < 0:
        result = "moins "
    number = abs(number)

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

    return number_1_999999_fr(i)


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
    """Takes in a string and extracts a number.
    Args:
        text (str): the string to extract a number from
    Returns:
        (str): The number extracted or the original text.
    """
    # TODO: short_scale and ordinals don't do anything here.
    # The parameters are present in the function signature for API compatibility
    # reasons.
    # normalize text, keep articles for ordinals versus fractionals
    text = normalize_fr(text, False)
    # split words by whitespace
    aWords = text.split()
    count = 0
    result = None
    add = False
    while count < len(aWords):
        val = None
        word = aWords[count]
        wordNext = ""
        wordPrev = ""
        if count < (len(aWords) - 1):
            wordNext = aWords[count + 1]
        if count > 0:
            wordPrev = aWords[count - 1]

        if word in _ARTICLES_FR:
            count += 1
            continue
        if word in ["et", "plus", "+"]:
            count += 1
            add = True
            continue

        # is current word a numeric number?
        if word.isdigit():
            val = int(word)
            count += 1
        elif is_numeric(word):
            val = float(word)
            count += 1
        elif wordPrev in _ARTICLES_FR and _get_ordinal_fr(word):
            val = _get_ordinal_fr(word)
            count += 1
        # is current word the denominator of a fraction?
        elif is_fractional_fr(word):
            val = is_fractional_fr(word)
            count += 1

        # is current word the numerator of a fraction?
        if val and wordNext:
            valNext = is_fractional_fr(wordNext)
            if valNext:
                val = float(val) * valNext
                count += 1

        if not val:
            count += 1
            # is current word a numeric fraction like "2/3"?
            aPieces = word.split('/')
            # if (len(aPieces) == 2 and is_numeric(aPieces[0])
            #   and is_numeric(aPieces[1])):
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])

        # is current word followed by a decimal value?
        if wordNext == "virgule":
            zeros = 0
            newWords = aWords[count + 1:]
            # count the number of zeros after the decimal sign
            for word in newWords:
                if word == "zéro" or word == "0":
                    zeros += 1
                else:
                    break
            afterDotVal = None
            # extract the number after the zeros
            if newWords[zeros].isdigit():
                afterDotVal = newWords[zeros]
                countDot = count + zeros + 2
            # if a number was extracted (since comma is also a
            # punctuation sign)
            if afterDotVal:
                count = countDot
                if not val:
                    val = 0
                # add the zeros
                afterDotString = zeros * "0" + afterDotVal
                val = float(str(val) + "." + afterDotString)
        if val:
            if add:
                result += val
                add = False
            else:
                result = val

    return result or False


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

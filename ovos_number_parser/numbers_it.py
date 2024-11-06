import collections

from ovos_number_parser.util import convert_to_mixed_fraction, is_numeric, look_for_fractions

_SHORT_ORDINAL_STRING_IT = {
    1: 'primo',
    2: 'secondo',
    3: 'terzo',
    4: 'quarto',
    5: 'quinto',
    6: 'sesto',
    7: 'settimo',
    8: 'ottavo',
    9: 'nono',
    10: 'decimo',
    11: 'undicesimo',
    12: 'dodicesimo',
    13: 'tredicesimo',
    14: 'quattordicesimo',
    15: 'quindicesimo',
    16: 'sedicesimo',
    17: 'diciassettesimo',
    18: 'diciottesimo',
    19: 'diciannovesimo',
    20: 'ventesimo',
    30: 'trentesimo',
    40: 'quarantesimo',
    50: 'cinquantesimo',
    60: 'sessantesimo',
    70: 'settantesimo',
    80: 'ottantesimo',
    90: 'novantesimo',
    1e2: 'centesimo',
    1e3: 'millesimo',
    1e6: 'milionesimo',
    1e9: 'miliardesimo',
    1e12: 'trilionesimo',
    1e15: 'quadrilionesimo',
    1e18: 'quintilionesim',
    1e21: 'sestilionesimo',
    1e24: 'settilionesimo',
    1e27: 'ottilionesimo',
    1e30: 'nonilionesimo',
    1e33: 'decilionesimo'
    # TODO > 1e-33
}

#  per i > 10e12 modificata solo la desinenza: da sistemare a fine debug
_LONG_ORDINAL_STRING_IT = {
    1: 'primo',
    2: 'secondo',
    3: 'terzo',
    4: 'quarto',
    5: 'quinto',
    6: 'sesto',
    7: 'settimo',
    8: 'ottavo',
    9: 'nono',
    10: 'decimo',
    11: 'undicesimo',
    12: 'dodicesimo',
    13: 'tredicesimo',
    14: 'quattordicesimo',
    15: 'quindicesimo',
    16: 'sedicesimo',
    17: 'diciassettesimo',
    18: 'diciottesimo',
    19: 'diciannovesimo',
    20: 'ventesimo',
    30: 'trentesimo',
    40: 'quarantesimo',
    50: 'cinquantesimo',
    60: 'sessantesimo',
    70: 'settantesimo',
    80: 'ottantesimo',
    90: 'novantesimo',
    1e2: 'centesimo',
    1e3: 'millesimo',
    1e6: 'milionesimo',
    1e12: 'bilionesimo',
    1e18: 'trilionesimo',
    1e24: 'quadrilionesimo',
    1e30: 'quintilionesimo',
    1e36: 'sestilionesimo',
    1e42: 'settilionesimo',
    1e48: 'ottilionesimo',
    1e54: 'nonilionesimo',
    1e60: 'decilionesimo'
    # TODO > 1e60
}

# Undefined articles ['un', 'una', 'un\''] can not be supressed,
# in Italian, 'un cavallo' means 'a horse' or 'one horse'.
_ARTICLES_IT = ['il', 'lo', 'la', 'i', 'gli', 'le']

_STRING_NUM_IT = {
    'zero': 0,
    'un': 1,
    'uno': 1,
    'una': 1,
    'un\'': 1,
    'due': 2,
    'tre': 3,
    'quattro': 4,
    'cinque': 5,
    'sei': 6,
    'sette': 7,
    'otto': 8,
    'nove': 9,
    'dieci': 10,
    'undici': 11,
    'dodici': 12,
    'tredici': 13,
    'quattordici': 14,
    'quindici': 15,
    'sedici': 16,
    'diciassette': 17,
    'diciotto': 18,
    'diciannove': 19,
    'venti': 20,
    'vent': 20,
    'trenta': 30,
    'trent': 30,
    'quaranta': 40,
    'quarant': 40,
    'cinquanta': 50,
    'cinquant': 50,
    'sessanta': 60,
    'sessant': 60,
    'settanta': 70,
    'settant': 70,
    'ottanta': 80,
    'ottant': 80,
    'novanta': 90,
    'novant': 90,
    'cento': 100,
    'duecento': 200,
    'trecento': 300,
    'quattrocento': 400,
    'cinquecento': 500,
    'seicento': 600,
    'settecento': 700,
    'ottocento': 800,
    'novecento': 900,
    'mille': 1000,
    'mila': 1000,
    'centomila': 100000,
    'milione': 1000000,
    'miliardo': 1000000000,
    'primo': 1,
    'secondo': 2,
    'mezzo': 0.5,
    'mezza': 0.5,
    'paio': 2,
    'decina': 10,
    'decine': 10,
    'dozzina': 12,
    'dozzine': 12,
    'centinaio': 100,
    'centinaia': 100,
    'migliaio': 1000,
    'migliaia': 1000
}

_NUM_STRING_IT = {
    0: 'zero',
    1: 'uno',
    2: 'due',
    3: 'tre',
    4: 'quattro',
    5: 'cinque',
    6: 'sei',
    7: 'sette',
    8: 'otto',
    9: 'nove',
    10: 'dieci',
    11: 'undici',
    12: 'dodici',
    13: 'tredici',
    14: 'quattordici',
    15: 'quindici',
    16: 'sedici',
    17: 'diciassette',
    18: 'diciotto',
    19: 'diciannove',
    20: 'venti',
    30: 'trenta',
    40: 'quaranta',
    50: 'cinquanta',
    60: 'sessanta',
    70: 'settanta',
    80: 'ottanta',
    90: 'novanta'
}

_FRACTION_STRING_IT = {
    2: 'mezz',
    3: 'terz',
    4: 'quart',
    5: 'quint',
    6: 'sest',
    7: 'settim',
    8: 'ottav',
    9: 'non',
    10: 'decim',
    11: 'undicesim',
    12: 'dodicesim',
    13: 'tredicesim',
    14: 'quattordicesim',
    15: 'quindicesim',
    16: 'sedicesim',
    17: 'diciassettesim',
    18: 'diciottesim',
    19: 'diciannovesim',
    20: 'ventesim'
}

# fonte: http://tulengua.es/numeros-texto/default.aspx
_LONG_SCALE_IT = collections.OrderedDict([
    (100, 'cento'),
    (1000, 'mila'),
    (1000000, 'milioni'),
    (1e9, "miliardi"),
    (1e12, "bilioni"),
    (1e18, 'trilioni'),
    (1e24, "quadrilioni"),
    (1e30, "quintilioni"),
    (1e36, "sestilioni"),
    (1e42, "settilioni"),
    (1e48, "ottillioni"),
    (1e54, "nonillioni"),
    (1e60, "decemillioni"),
    (1e66, "undicilione"),
    (1e72, "dodicilione"),
    (1e78, "tredicilione"),
    (1e84, "quattordicilione"),
    (1e90, "quindicilione"),
    (1e96, "sedicilione"),
    (1e102, "diciasettilione"),
    (1e108, "diciottilione"),
    (1e114, "dicianovilione"),
    (1e120, "vintilione"),
    (1e306, "unquinquagintilione"),
    (1e312, "duoquinquagintilione"),
    (1e336, "sesquinquagintilione"),
    (1e366, "unsexagintilione")
])

_SHORT_SCALE_IT = collections.OrderedDict([
    (100, 'cento'),
    (1000, 'mila'),
    (1000000, 'milioni'),
    (1e9, "miliardi"),
    (1e12, 'bilioni'),
    (1e15, "biliardi"),
    (1e18, "trilioni"),
    (1e21, "triliardi"),
    (1e24, "quadrilioni"),
    (1e27, "quadriliardi"),
    (1e30, "quintilioni"),
    (1e33, "quintiliardi"),
    (1e36, "sestilioni"),
    (1e39, "sestiliardi"),
    (1e42, "settilioni"),
    (1e45, "settiliardi"),
    (1e48, "ottilioni"),
    (1e51, "ottiliardi"),
    (1e54, "nonilioni"),
    (1e57, "noniliardi"),
    (1e60, "decilioni"),
    (1e63, "deciliardi"),
    (1e66, "undicilioni"),
    (1e69, "undiciliardi"),
    (1e72, "dodicilioni"),
    (1e75, "dodiciliardi"),
    (1e78, "tredicilioni"),
    (1e81, "trediciliardi"),
    (1e84, "quattordicilioni"),
    (1e87, "quattordiciliardi"),
    (1e90, "quindicilioni"),
    (1e93, "quindiciliardi"),
    (1e96, "sedicilioni"),
    (1e99, "sediciliardi"),
    (1e102, "diciassettilioni"),
    (1e105, "diciassettiliardi"),
    (1e108, "diciottilioni"),
    (1e111, "diciottiliardi"),
    (1e114, "dicianovilioni"),
    (1e117, "dicianoviliardi"),
    (1e120, "vintilioni"),
    (1e123, "vintiliardi"),
    (1e153, "quinquagintillion"),
    (1e183, "sexagintillion"),
    (1e213, "septuagintillion"),
    (1e243, "ottogintilioni"),
    (1e273, "nonigintillioni"),
    (1e303, "centilioni"),
    (1e306, "uncentilioni"),
    (1e309, "duocentilioni"),
    (1e312, "trecentilioni"),
    (1e333, "decicentilioni"),
    (1e336, "undicicentilioni"),
    (1e363, "viginticentilioni"),
    (1e366, "unviginticentilioni"),
    (1e393, "trigintacentilioni"),
    (1e423, "quadragintacentillion"),
    (1e453, "quinquagintacentillion"),
    (1e483, "sexagintacentillion"),
    (1e513, "septuagintacentillion"),
    (1e543, "ctogintacentillion"),
    (1e573, "nonagintacentillion"),
    (1e603, "ducentillion"),
    (1e903, "trecentillion"),
    (1e1203, "quadringentillion"),
    (1e1503, "quingentillion"),
    (1e1803, "sescentillion"),
    (1e2103, "septingentillion"),
    (1e2403, "octingentillion"),
    (1e2703, "nongentillion"),
    (1e3003, "millinillion")
])


def is_fractional_it(input_str, short_scale=False):
    """
    This function takes the given text and checks if it is a fraction.
    Updated to italian from en version 18.8.9

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    input_str = input_str.lower()
    if input_str.endswith('i', -1) and len(input_str) > 2:
        input_str = input_str[:-1] + "o"  # normalizza plurali

    fracts_it = {"intero": 1, "mezza": 2, "mezzo": 2}

    if short_scale:
        for num in _SHORT_ORDINAL_STRING_IT:
            if num > 2:
                fracts_it[_SHORT_ORDINAL_STRING_IT[num]] = num
    else:
        for num in _LONG_ORDINAL_STRING_IT:
            if num > 2:
                fracts_it[_LONG_ORDINAL_STRING_IT[num]] = num

    if input_str in fracts_it:
        return 1.0 / fracts_it[input_str]
    return False


def _extract_number_long_it(word):
    """
     This function converts a long textual number like
     milleventisette -> 1027 diecimila -> 10041 in
     integer value, covers from  0 to 999999999999999
     for now limited to 999_e21 but ready for 999_e63
     example:
        milleventisette -> 1027
        diecimilaquarantuno-> 10041
        centottomiladuecentotredici -> 108213
    Args:
         word (str): the word to convert in number
    Returns:
         (bool) or (int): The extracted number or False if no number
                                   was found
    """

    units = {'zero': 0, 'uno': 1, 'due': 2, 'tre': 3, 'quattro': 4,
             'cinque': 5, 'sei': 6, 'sette': 7, 'otto': 8, 'nove': 9}

    tens = {'dieci': 10, 'venti': 20, 'trenta': 30, 'quaranta': 40,
            'cinquanta': 50, 'sessanta': 60, 'settanta': 70, 'ottanta': 80,
            'novanta': 90}

    tens_short = {'vent': 20, 'trent': 30, 'quarant': 40, 'cinquant': 50,
                  'sessant': 60, 'settant': 70, 'ottant': 80, 'novant': 90}

    nums_long = {'undici': 11, 'dodici': 12, 'tredici': 13, 'quattordici': 14,
                 'quindici': 15, 'sedici': 16, 'diciassette': 17,
                 'diciotto': 18, 'diciannove': 19}

    multipli_it = collections.OrderedDict([
        # (1e63, 'deciliardi'),
        # (1e60, 'decilioni'),
        # (1e57, 'noviliardi'),
        # (1e54, 'novilioni'),
        # (1e51, 'ottiliardi'),
        # (1e48, 'ottilioni'),
        # (1e45, 'settiliardi'),
        # (1e42, 'settilioni'),
        # (1e39, 'sestiliardi'),
        # (1e36, 'sestilioni'),
        # (1e33, 'quintiliardi'),
        # (1e30, 'quintilioni'),
        # (1e27, 'quadriliardi'),
        # (1e24, 'quadrilioni'),    # yotta
        (1e21, 'triliardi'),  # zetta
        (1e18, 'trilioni'),  # exa
        (1e15, 'biliardi'),  # peta
        (1e12, 'bilioni'),  # tera
        (1e9, 'miliardi'),  # giga
        (1e6, 'milioni')  # mega
    ])

    multiplier = {}
    un_multiplier = {}

    for num in multipli_it:
        if num > 1000 and num <= 1e21:
            # plurali
            multiplier[multipli_it[num]] = int(num)
            # singolari - modificare per eccezioni *liardo
            if multipli_it[num][-5:-1] == 'iard':
                un_multiplier['un' + multipli_it[num][:-1] + 'o'] = int(num)
            else:
                un_multiplier['un' + multipli_it[num][:-1] + 'e'] = int(num)

    value = False

    # normalizza ordinali singoli o plurali -esimo -esimi
    if word[-5:-1] == 'esim':
        base = word[:-5]
        normalize_ita3 = {'tre': '', 'ttr': 'o', 'sei': '', 'ott': 'o'}
        normalize_ita2 = {'un': 'o', 'du': 'e', 'qu': 'e', 'tt': 'e',
                          'ov': 'e'}

        if base[-3:] in normalize_ita3:
            base += normalize_ita3[base[-3:]]
        elif base[-2:] in normalize_ita2:
            base += normalize_ita2[base[-2:]]

        word = base

    for item in un_multiplier:
        components = word.split(item, 1)
        if len(components) == 2:
            if not components[0]:  # inizia con un1^x
                if not components[1]:  # unmilione
                    word = str(int(un_multiplier[item]))
                else:  # unmilione + x
                    word = str(int(un_multiplier[item]) +
                               _extract_number_long_it(components[1]))

    for item in multiplier:
        components = word.split(item, 1)
        if len(components) == 2:
            if not components[0]:  # inizia con un1^x
                word = str(int(multiplier[item]) +
                           _extract_number_long_it(components[1]))
            else:
                if not components[1]:
                    word = str(_extract_number_long_it(components[0])) + '*' \
                           + str(int(multiplier[item]))
                else:
                    word = str(_extract_number_long_it(components[0])) + '*' \
                           + str(int(multiplier[item])) + '+' \
                           + str(_extract_number_long_it(components[1]))

    for item in tens:
        word = word.replace(item, '+' + str(tens[item]))

    for item in tens_short:
        word = word.replace(item, '+' + str(tens_short[item]))

    for item in nums_long:
        word = word.replace(item, '+' + str(nums_long[item]))

    word = word.replace('cento', '+1xx')
    word = word.replace('cent', '+1xx')
    word = word.replace('mille', '+1000')  # unmilionemille
    word = word.replace('mila', '*1000')  # unmilioneduemila

    for item in units:
        word = word.replace(item, '+' + str(units[item]))

    # normalizzo i cento
    occorrenze = word.count('+1xx')
    for _ in range(0, occorrenze):
        components = word.rsplit('+1xx', 1)
        if len(components[0]) > 1 and components[0].endswith('0'):
            word = components[0] + '+100' + components[1]
        else:
            word = components[0] + '*100' + components[1]

    components = word.rsplit('*1000', 1)
    if len(components) == 2:
        if components[0].startswith('*'):  # centomila
            components[0] = components[0][1:]
        word = str(_extract_number_long_it(components[0])) + \
               '*1000' + str(components[1])

    # gestione eccezioni
    if word.startswith('*') or word.startswith('+'):
        word = word[1:]

    addends = word.split('+')
    for c, _ in enumerate(addends):
        if '*' in addends[c]:
            factors = addends[c].split('*')
            result = int(factors[0]) * int(factors[1])
            if len(factors) == 3:
                result *= int(factors[2])
            addends[c] = str(result)

    # check if all token are numbers
    if all([s.isdecimal() for s in addends]):
        value = sum([int(s) for s in addends])
    else:
        value = False
    return value


def extract_number_it(text, short_scale=False, ordinals=False):
    """
    This function extracts a number from a text string,
    handles pronunciations in long scale and short scale

    https://en.wikipedia.org/wiki/Names_of_large_numbers

    Args:
        text (str): the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found

    """

    text = text.lower()
    string_num_ordinal_it = {}
    # first, second...
    if ordinals:
        if short_scale:
            for num in _SHORT_ORDINAL_STRING_IT:
                num_string = _SHORT_ORDINAL_STRING_IT[num]
                string_num_ordinal_it[num_string] = num
                _STRING_NUM_IT[num_string] = num
        else:
            for num in _LONG_ORDINAL_STRING_IT:
                num_string = _LONG_ORDINAL_STRING_IT[num]
                string_num_ordinal_it[num_string] = num
                _STRING_NUM_IT[num_string] = num

    # negate next number (-2 = 0 - 2)
    negatives = ['meno']  # 'negativo' non è usuale in italiano

    # multiply the previous number (one hundred = 1 * 100)
    multiplies = ['decina', 'decine', 'dozzina', 'dozzine',
                  'centinaia', 'centinaio', 'migliaia', 'migliaio', 'mila']

    # split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
    fraction_marker = [' e ']

    # decimal marker ( 1 point 5 = 1 + 0.5)
    decimal_marker = [' punto ', ' virgola ']

    if short_scale:
        for num in _SHORT_SCALE_IT:
            num_string = _SHORT_SCALE_IT[num]
            _STRING_NUM_IT[num_string] = num
            multiplies.append(num_string)
    else:
        for num in _LONG_SCALE_IT:
            num_string = _LONG_SCALE_IT[num]
            _STRING_NUM_IT[num_string] = num
            multiplies.append(num_string)

    # 2 e 3/4 ed altri casi
    for separator in fraction_marker:
        components = text.split(separator)
        zeros = 0

        if len(components) == 2:
            # count zeros in fraction part
            sub_components = components[1].split(' ')
            for element in sub_components:
                if element == 'zero' or element == '0':
                    zeros += 1
                else:
                    break
            # ensure first is not a fraction and second is a fraction
            num1 = extract_number_it(components[0])
            num2 = extract_number_it(components[1])
            if num1 is not None and num2 is not None \
                    and num1 >= 1 and 0 < num2 < 1:
                return num1 + num2
            # sette e quaranta  sette e zero zero due
            elif num1 is not None and num2 is not None \
                    and num1 >= 1 and num2 > 1:
                return num1 + num2 / pow(10, len(str(num2)) + zeros)

    # 2 punto 5
    for separator in decimal_marker:
        zeros = 0
        # count zeros in fraction part
        components = text.split(separator)

        if len(components) == 2:
            sub_components = components[1].split(' ')
            for element in sub_components:
                if element == 'zero' or element == '0':
                    zeros += 1
                else:
                    break

            number = int(extract_number_it(components[0]))
            decimal = int(extract_number_it(components[1]))
            if number is not None and decimal is not None:
                if '.' not in str(decimal):
                    return number + decimal / pow(10,
                                                  len(str(decimal)) + zeros)

    all_words = text.split()
    val = False
    prev_val = None
    to_sum = []
    for idx, word in enumerate(all_words):

        if not word:
            continue
        prev_word = all_words[idx - 1] if idx > 0 else ''
        next_word = all_words[idx + 1] if idx + 1 < len(all_words) else ''

        # is this word already a number ?
        if is_numeric(word):
            val = float(word)

        # is this word the name of a number ?
        if word in _STRING_NUM_IT:
            val = _STRING_NUM_IT[word]

        #  tre quarti  un quarto  trenta secondi
        if is_fractional_it(word) and prev_val:
            if word[:-1] == 'second' and not ordinals:
                val = prev_val * 2
            else:
                val = prev_val

        # is the prev word a number and should we multiply it?
        # twenty hundred, six hundred
        if word in multiplies:
            if not prev_val:
                prev_val = 1
            val = prev_val * val

        # is this a spoken fraction?
        # mezza tazza
        if val is False:
            val = is_fractional_it(word, short_scale=short_scale)

        # 2 quinti
        if not ordinals:
            next_value = is_fractional_it(next_word, short_scale=short_scale)
            if next_value:
                if not val:
                    val = 1
                val = val * next_value

        # is this a negative number?
        if val and prev_word and prev_word in negatives:
            val = 0 - val

        if not val:
            val = _extract_number_long_it(word)

        # let's make sure it isn't a fraction
        if not val:
            # look for fractions like '2/3'
            all_pieces = word.split('/')
            if look_for_fractions(all_pieces):
                val = float(all_pieces[0]) / float(all_pieces[1])
        else:
            prev_val = val
            # handle long numbers
            # six hundred sixty six
            # two million five hundred thousand
            if word in multiplies and next_word not in multiplies:
                to_sum.append(val)
                val = 0
                prev_val = 0
            elif _extract_number_long_it(word) > 100 and \
                    _extract_number_long_it(next_word) and \
                    next_word not in multiplies:
                to_sum.append(val)
                val = 0
                prev_val = 0

    if val is not None:
        for addend in to_sum:
            val = val + addend
    return val


def nice_number_it(number, speech=True, denominators=range(1, 21)):
    """ Italian helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 e un mezz" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """

    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        # Give up, just represent as a 3 decimal number
        return str(round(number, 3))

    whole, num, den = result

    if not speech:
        if num == 0:
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    # denominatore
    den_str = _FRACTION_STRING_IT[den]
    # frazione
    if whole == 0:
        if num == 1:
            # un decimo
            return_string = 'un {}'.format(den_str)
        else:
            # tre mezzi
            return_string = '{} {}'.format(num, den_str)
    # interi  >10
    elif num == 1:
        # trenta e un
        return_string = '{} e un {}'.format(whole, den_str)
    # interi >10 con frazioni
    else:
        # venti e 3 decimi
        return_string = '{} e {} {}'.format(whole, num, den_str)

    # gestisce il plurale del denominatore
    if num > 1:
        return_string += 'i'
    else:
        return_string += 'o'

    return return_string


def pronounce_number_it(number, places=2, short_scale=False, scientific=False):
    """
    Convert a number to it's spoken equivalent
    adapted to italian fron en version

    For example, '5.2' would return 'cinque virgola due'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
    Returns:
        (str): The pronounced number
    """
    num = number
    # gestione infinito
    if num == float("inf"):
        return "infinito"
    elif num == float("-inf"):
        return "meno infinito"

    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            return '{}{} per dieci elevato alla {}{}'.format(
                'meno ' if float(n) < 0 else '',
                pronounce_number_it(abs(float(n)), places, short_scale, False),
                'meno ' if power < 0 else '',
                pronounce_number_it(abs(power), places, short_scale, False))

    if short_scale:
        number_names = _NUM_STRING_IT.copy()
        number_names.update(_SHORT_SCALE_IT)
    else:
        number_names = _NUM_STRING_IT.copy()
        number_names.update(_LONG_SCALE_IT)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale:
        hundreds = [_SHORT_SCALE_IT[n] for n in _SHORT_SCALE_IT.keys()]
    else:
        hundreds = [_LONG_SCALE_IT[n] for n in _LONG_SCALE_IT.keys()]

    # deal with negatives
    result = ""
    if num < 0:
        result = "meno "
    num = abs(num)

    # check for a direct match
    if num in number_names:
        if num > 90:
            result += ""  # inizio stringa
        result += number_names[num]
    else:
        def _sub_thousand(n):
            assert 0 <= n <= 999
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                _deci = tens[q - 1]
                _unit = r
                _partial = _deci
                if _unit > 0:
                    if _unit == 1 or _unit == 8:
                        _partial = _partial[:-1]  # ventuno  ventotto
                    _partial += number_names[_unit]
                return _partial
            else:
                q, r = divmod(n, 100)
                if q == 1:
                    _partial = "cento"
                else:
                    _partial = digits[q] + "cento"
                _partial += (
                    " " + _sub_thousand(r) if r else "")  # separa centinaia
                return _partial

        def _short_scale(n):
            if n >= max(_SHORT_SCALE_IT.keys()):
                return "numero davvero enorme"
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000)):
                if not z:
                    continue
                number = _sub_thousand(z)
                if i:
                    number += ""  # separa ordini grandezza
                    number += hundreds[i]
                res.append(number)

            return ", ".join(reversed(res))

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        def _long_scale(n):
            if n >= max(_LONG_SCALE_IT.keys()):
                return "numero davvero enorme"
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000000)):
                if not z:
                    continue
                number = pronounce_number_it(z, places, True, scientific)
                # strip off the comma after the thousand
                if i:
                    # plus one as we skip 'thousand'
                    # (and 'hundred', but this is excluded by index value)
                    number = number.replace(',', '')
                    number += " " + hundreds[i + 1]
                res.append(number)
            return ", ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # normalizza unità misura singole e 'ragionevoli' ed ad inizio stringa
    if result == 'mila':
        result = 'mille'
    if result == 'milioni':
        result = 'un milione'
    if result == 'miliardi':
        result = 'un miliardo'
    if result[0:7] == 'unomila':
        result = result.replace('unomila', 'mille', 1)
    if result[0:10] == 'unomilioni':
        result = result.replace('unomilioni', 'un milione', 1)
    # if result[0:11] == 'unomiliardi':
    # result = result.replace('unomiliardi', 'un miliardo', 1)

    # Deal with fractional part
    if not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "meno " or not result):
            result += "zero"
        result += " virgola"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result

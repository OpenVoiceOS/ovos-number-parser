#
# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Dutch number words.

Rules and sources:

* Cardinals: Taaladvies.net (Nederlandse Taalunie), "Aaneenschrijven van
  telwoorden (algemeen)", https://taaladvies.net/aaneenschrijven-van-telwoorden/
  Cardinals are written as one word up to and including "duizend" ("135
  honderdvijfendertig", "6000 zesduizend"). "Na het woord duizend (en
  samenstellingen hiermee, zoals vierduizend) staat een spatie": 4002 is
  "vierduizend twee" and 28 064 is "achtentwintigduizend vierenzestig".
  "Miljoen en miljard zijn altijd aparte woorden": 3 000 000 is "drie miljoen".
  Onze Taal, "Getallen uitschrijven",
  https://onzetaal.nl/taalloket/getallen-uitschrijven, gives the same rule and
  says it holds for cardinals and ordinals.
* Ordinals: the same Taaladvies page ("Rangtelwoorden worden gevormd door
  toevoeging van het achtervoegsel -ste, -de of -e aan het overeenkomstige
  hoofdtelwoord. Met de hoofdtelwoorden een en drie corresponderen evenwel de
  rangtelwoorden eerste en derde"; examples "102e honderdentweede", "3220e
  drieduizend tweehonderdtwintigste", "4 000 000e vier miljoenste"). Onze Taal,
  "Honderdeneende / honderdeneerste",
  https://onzetaal.nl/taalloket/honderdeneende-honderdeneerste: "In
  samengestelde rangtelwoorden ga je van het laatste deel uit:
  negenhonderdzevende, driehonderdachtste, honderdeneerste"; the forms without
  "en" ("honderdeerste") are correct as well. The suffix follows the last
  part: 1 "eerste", 3 "derde", 8 "achtste", the other numbers up to 19 take
  "-de", tens, "honderd", "duizend" and the scale words take "-ste". The
  Wiktionary entries "eerste", "derde", "achtste" and "miljoenste" agree.
  Onze Taal writes the 1001st as "duizendeneerste" and "duizendeerste" in
  that page; the spacing rule of Taaladvies and of Onze Taal's "Getallen
  uitschrijven" ("Deze regel geldt zowel voor hoofdtelwoorden als voor
  rangtelwoorden") wins, so the 1001st is "duizend eerste".
* Stress mark: Taaladvies.net, "Klemtoonteken (algemeen)": accents are only
  needed where a misreading threatens, so a number inside a longer number
  ("tweeduizend een", "honderdeen") takes no accent, and the numeral on its
  own and before "miljoen" or "miljard" takes "één".
* Trema: Taaladvies.net, "Klinkerbotsing" ("tweeëntwintig").
"""

from decimal import Decimal
from math import floor

from ovos_number_parser.util import convert_to_mixed_fraction, invert_dict
from ovos_number_parser import numtag_readers
from ovos_number_parser.util import warn_reader_removed
from ovos_number_parser.util import Scale


_NUM_STRING_NL = {
    0: 'nul',
    1: 'een',
    2: 'twee',
    3: 'drie',
    4: 'vier',
    5: 'vijf',
    6: 'zes',
    7: 'zeven',
    8: 'acht',
    9: 'negen',
    10: 'tien',
    11: 'elf',
    12: 'twaalf',
    13: 'dertien',
    14: 'veertien',
    15: 'vijftien',
    16: 'zestien',
    17: 'zeventien',
    18: 'achttien',
    19: 'negentien',
    20: 'twintig',
    30: 'dertig',
    40: 'veertig',
    50: 'vijftig',
    60: 'zestig',
    70: 'zeventig',
    80: 'tachtig',
    90: 'negentig',
    100: 'honderd'
}

_FRACTION_STRING_NL = {
    2: 'half',
    3: 'derde',
    4: 'vierde',
    5: 'vijfde',
    6: 'zesde',
    7: 'zevende',
    8: 'achtste',
    9: 'negende',
    10: 'tiende',
    11: 'elfde',
    12: 'twaalfde',
    13: 'dertiende',
    14: 'veertiende',
    15: 'vijftiende',
    16: 'zestiende',
    17: 'zeventiende',
    18: 'achttiende',
    19: 'negentiende',
    20: 'twintigste'
}


_ORDINAL_STRING_BASE_NL = {
    1: 'eerste',
    2: 'tweede',
    3: 'derde',
    4: 'vierde',
    5: 'vijfde',
    6: 'zesde',
    7: 'zevende',
    8: 'achtste',
    9: 'negende',
    10: 'tiende',
    11: 'elfde',
    12: 'twaalfde',
    13: 'dertiende',
    14: 'veertiende',
    15: 'vijftiende',
    16: 'zestiende',
    17: 'zeventiende',
    18: 'achttiende',
    19: 'negentiende',
    20: 'twintigste',
    30: 'dertigste',
    40: "veertigste",
    50: "vijftigste",
    60: "zestigste",
    70: "zeventigste",
    80: "tachtigste",
    90: "negentigste",
    100: "honderdste",
    1e3: "duizendste"
}

_SHORT_ORDINAL_STRING_NL = {
    1e6: "miljoenste",
    1e9: "miljardste",
    1e12: "biljoenste",
    1e15: "biljardste",
    1e18: "triljoenste",
    1e21: "triljardste",
    1e24: "quadriljoenste",
    1e27: "quadriljardste",
    1e30: "quintiljoenste",
    1e33: "quintiljardste"
    # TODO > 1e-33
}
_SHORT_ORDINAL_STRING_NL.update(_ORDINAL_STRING_BASE_NL)

_LONG_ORDINAL_STRING_NL = {
    1e6: "miljoenste",
    1e9: "miljardste",
    1e12: "biljoenste",
    1e15: "biljardste",
    1e18: "triljoenste",
    1e21: "triljardste",
    1e24: "quadriljoenste",
    1e27: "quadriljardste",
    1e30: "quintiljoenste",
    1e33: "quintiljardste"
    # TODO > 1e60
}
_LONG_ORDINAL_STRING_NL.update(_ORDINAL_STRING_BASE_NL)


_STRING_NUM_NL = invert_dict(_NUM_STRING_NL)
_STRING_NUM_NL.update({
    "een": 1,
    "half": 0.5,
    "driekwart": 0.75,
    "anderhalf": 1.5,
    "paar": 2
})


_MONTHS_NL = ['januari', 'februari', 'maart', 'april', 'mei', 'juni',
              'juli', 'augustus', 'september', 'oktober', 'november',
              'december']


# Dutch uses "long scale" https://en.wikipedia.org/wiki/Long_and_short_scales
# Currently, numbers are limited to 1000000000000000000000000,
# but _NUM_POWERS_OF_TEN can be extended to include additional number words


_NUM_POWERS_OF_TEN = [
    '', 'duizend', 'miljoen', 'miljard', 'biljoen', 'biljard', 'triljoen',
    'triljard'
]

# Numbers below 1 million are written in one word in dutch, yielding very
# long words
# In some circumstances it may better to seperate individual words
# Set _EXTRA_SPACE_NL=" " for separating numbers below 1 million (
# orthographically incorrect)
# Set _EXTRA_SPACE_NL="" for correct spelling, this is standard

# _EXTRA_SPACE_NL = " "
_EXTRA_SPACE_NL = ""


def nice_number_nl(number, speech=True, denominators=range(1, 21)):
    """ Dutch helper for nice_number
    This function formats a float to human understandable functions. Like
    4.5 becomes "4 einhalb" for speech and "4 1/2" for text
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
        return str(round(number, 3)).replace(".", ",")
    whole, num, den = result
    if not speech:
        if num == 0:
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_NL[den]
    if whole == 0:
        if num == 1:
            return_string = 'één {}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} en één {}'.format(whole, den_str)
    else:
        return_string = '{} en {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_nl(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'five point two'

    Args:
        number(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """

    # TODO short_scale, scientific and ordinals
    # currently ignored

    def pronounce_triplet_nl(num):
        result = ""
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                # 100 is "honderd", never "eenhonderd": Dutch drops the "een"
                # before "honderd" and "duizend" (Nederlandse Taalunie,
                # Taaladvies "Aaneenschrijven van telwoorden": 800 =
                # "achthonderd", 135 = "honderdvijfendertig"), so the leading
                # "one" is written only from two hundred up.
                if hundreds > 1:
                    result += _NUM_STRING_NL[hundreds] + _EXTRA_SPACE_NL
                result += 'honderd' + _EXTRA_SPACE_NL
                num -= hundreds * 100
        if num == 0:
            result += ''  # do nothing
        elif num <= 20:
            result += _NUM_STRING_NL[num]  # + _EXTRA_SPACE_DA
        elif num > 20:
            ones = num % 10
            tens = num - ones
            if ones > 0:
                ones_word = _NUM_STRING_NL[ones]
                result += ones_word + _EXTRA_SPACE_NL
                if tens > 0:
                    # Klinkerbotsing: "twee" and "drie" end in a vowel, so the
                    # "e" of the joining "en" would be read together with it
                    # ("tweeen"). Taaladvies.net (Nederlandse Taalunie), entry
                    # "Klinkerbotsing": the ambiguity is resolved by separating
                    # the vowels with a trema "in afleidingen en samengestelde
                    # telwoorden" -- compound numerals are an explicit
                    # exception to the hyphen used in ordinary compounds, and
                    # "tweeentwintig" is cited there as "tweeëntwintig".
                    joiner = 'ën' if ones_word.endswith(('e', 'ie')) else 'en'
                    result += joiner + _EXTRA_SPACE_NL
            if tens > 0:
                result += _NUM_STRING_NL[tens] + _EXTRA_SPACE_NL
        return result

    def pronounce_fractional_nl(num,
                                places):  # fixed number of places even with
        # trailing zeros
        result = ""
        for digit in f"{Decimal(str(num)):f}".split(".")[1][:places].ljust(places, "0"):
            result += " " + _NUM_STRING_NL[int(digit)]
        return result

    def pronounce_whole_number_nl(num):
        # Taaladvies.net, "Aaneenschrijven van telwoorden": a space follows
        # "duizend" and its compounds, and "miljoen", "miljard" ... are
        # separate words, so every group of the number is its own word.
        num = floor(num)
        groups = []
        scale_level = 0
        while num:
            triplet = num % 1000
            if triplet:
                if scale_level == 0:
                    groups.append("een" if triplet == 1
                                  else pronounce_triplet_nl(triplet))
                elif scale_level == 1:
                    # 1000 is "duizend", not "eenduizend" (same Taalunie rule)
                    groups.append("duizend" if triplet == 1 else
                                  pronounce_triplet_nl(triplet) + "duizend")
                else:
                    # from a million up the count word IS written; "één"
                    # marks the numeral where "een" would read as the article
                    count = "één" if triplet == 1 \
                        else pronounce_triplet_nl(triplet)
                    groups.append(count + " " + _NUM_POWERS_OF_TEN[scale_level])
            num //= 1000
            scale_level += 1
        return " ".join(reversed(groups))

    result = ""
    if abs(number) >= 1000000000000000000000000:  # cannot do more than this
        return str(number)
    elif number == 0:
        return str(_NUM_STRING_NL[0])
    elif number < 0:
        return "min " + pronounce_number_nl(abs(number), places)
    else:
        if number == int(number):
            spoken = pronounce_whole_number_nl(number)
            # the standalone numeral takes the accent: "één appel" vs the
            # article "een appel"; compounds stay unaccented (eenentwintig)
            if spoken == "een":
                return "één"
            return spoken
        else:
            whole_number_part = floor(number)
            whole_spoken = pronounce_whole_number_nl(whole_number_part) or \
                _NUM_STRING_NL[0]
            if whole_spoken == "een":
                whole_spoken = "één"
            result += whole_spoken
            if places > 0:
                result += " komma"
                result += pronounce_fractional_nl(number, places)
            return result


def pronounce_ordinal_nl(number):
    """
    This function pronounces a number as an ordinal

    1 -> eerste
    2 -> tweede
    101 -> honderdeerste
    4002 -> vierduizend tweede
    1000000 -> miljoenste

    The ending follows the last part of the number: 1, 3 and 8 are irregular
    ("eerste", "derde", "achtste"), the rest of 1 to 19 take "-de", and the
    tens and the scale words take "-ste".

    Sources: Taaladvies.net, "Aaneenschrijven van telwoorden (algemeen)"
    (rangtelwoorden: "-ste, -de of -e" at the matching cardinal, "eerste" and
    "derde" for 1 and 3, "drieduizend tweehonderdtwintigste", "vier
    miljoenste"); Onze Taal, "Honderdeneende / honderdeneerste" ("In
    samengestelde rangtelwoorden ga je van het laatste deel uit:
    negenhonderdzevende, driehonderdachtste, honderdeneerste"); Onze Taal,
    "Getallen uitschrijven" (the spacing rule holds for ordinals);
    Wiktionary nl "eerste", "derde", "achtste".

    Args:
        number (int): the number to format
    Returns:
        (str): The pronounced number string.
    """
    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    number = int(number)
    if number >= 10 ** 24:
        raise NotImplementedError(
            f"cannot pronounce {number} as a Dutch ordinal")
    if number == 0:
        return "nulste"
    spoken = pronounce_number_nl(number)
    if spoken == "één":
        return "eerste"
    if spoken.split(" ")[0] == "één" and len(spoken.split(" ")) == 2:
        spoken = spoken.split(" ")[1]  # "één miljoen" -> "miljoenste"
    last = number % 100
    if last == 1:
        return spoken[:-len("een")] + "eerste"
    if last == 3:
        return spoken[:-len("drie")] + "derde"
    if last == 8:
        return spoken + "ste"
    if 0 < last < 20:
        return spoken + "de"
    return spoken + "ste"


def is_fractional_nl(input_str, short_scale=True):
    """This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    fracts = {"heel": 1, "half": 2, "halve": 2, "kwart": 4}
    if short_scale:
        for num in _SHORT_ORDINAL_STRING_NL:
            if num > 2:
                fracts[_SHORT_ORDINAL_STRING_NL[num]] = num
    else:
        for num in _LONG_ORDINAL_STRING_NL:
            if num > 2:
                fracts[_LONG_ORDINAL_STRING_NL[num]] = num

    if input_str.lower() in fracts:
        return 1.0 / fracts[input_str.lower()]
    return False


def extract_number_nl(text, short_scale=True, ordinals=False):
    """Deprecated: use ``ovos_number_parser.extract_number(text, "nl")``."""
    warn_reader_removed("extract_number_nl", 'ovos_number_parser.extract_number(text, "nl")')
    return numtag_readers.extract_number(text, "nl", short_scale, ordinals)


def numbers_to_digits_nl(text, short_scale=True, ordinals=False):
    """Deprecated: use ``ovos_number_parser.numbers_to_digits(text, "nl")``."""
    warn_reader_removed("numbers_to_digits_nl", 'ovos_number_parser.numbers_to_digits(text, "nl")')
    return numtag_readers.numbers_to_digits(text, "nl", Scale.SHORT if short_scale else Scale.LONG, ordinals)

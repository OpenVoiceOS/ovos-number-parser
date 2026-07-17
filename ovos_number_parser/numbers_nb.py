"""Norwegian number parsing and pronunciation.

Covers both written standards of Norwegian:

* Bokmål (``nb``) — tables suffixed ``_NB``
* Nynorsk (``nn``) — implemented in :mod:`ovos_number_parser.numbers_nn`,
  which reuses this engine with its own tables (the two standards share
  all grammar relevant here and differ only in word forms)

Both Norwegian counting traditions are understood when parsing:

* the modern tens-first order introduced by the Storting in 1951
  ("den nye tellemåten"): ``tjueen`` = 21
* the traditional units-first order still common in speech
  ("den gamle tellemåten"): ``enogtyve`` = 21

Pronunciation always uses the modern order and the official modern forms
(``sju``, ``tjue``), per the 1951 counting reform.

Sources:
    - https://snl.no/den_nye_tellem%C3%A5ten (1951 counting reform)
    - https://snl.no/den_gamle_tellem%C3%A5ten (traditional counting)
    - https://ordbokene.no (Språkrådet/UiB: Bokmålsordboka & Nynorskordboka;
      every pronounced form in this module is an attested entry)
"""
from math import floor

from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, tokenize,
                                     ReplaceableNumber, Token, look_for_fractions)

# indefinite articles are homographs of "one"
_ARTICLES_NB = {'en', 'ei', 'et', 'ett'}

_NUM_STRING_NB = {
    0: 'null',
    1: 'en',
    2: 'to',
    3: 'tre',
    4: 'fire',
    5: 'fem',
    6: 'seks',
    7: 'sju',
    8: 'åtte',
    9: 'ni',
    10: 'ti',
    11: 'elleve',
    12: 'tolv',
    13: 'tretten',
    14: 'fjorten',
    15: 'femten',
    16: 'seksten',
    17: 'sytten',
    18: 'atten',
    19: 'nitten',
    20: 'tjue',
    30: 'tretti',
    40: 'førti',
    50: 'femti',
    60: 'seksti',
    70: 'sytti',
    80: 'åtti',
    90: 'nitti',
}

# words accepted when parsing: the pronounced forms above plus official
# variants (Bokmålsordboka: "syv" and "sju" are equal Bokmål forms) and the
# traditional counting words "tyve"/"tredve" documented in
# https://snl.no/den_gamle_tellem%C3%A5ten
_STRING_NUM_NB = invert_dict(_NUM_STRING_NB)
_STRING_NUM_NB.update({
    'én': 1,
    'ei': 1,
    'ett': 1,
    'syv': 7,
    'tyve': 20,
    'tredve': 30,
})

_SCALE_NB = {
    'hundre': 100,
    'tusen': 1000,
    'million': 1000000,
    'millioner': 1000000,
    'milliard': 1000000000,
    'milliarder': 1000000000,
    'billion': 1000000000000,
    'billioner': 1000000000000,
    'billiard': 1000000000000000,
    'billiarder': 1000000000000000,
    'trillion': 1000000000000000000,
    'trillioner': 1000000000000000000,
}

# scale words in singular, in ascending order, for pronunciation
_SCALE_ORDER_NB = ['hundre', 'tusen', 'million', 'milliard',
                   'billion', 'billiard', 'trillion']

_ORDINAL_STRING_NB = {
    0: 'nulte',
    1: 'første',
    2: 'andre',
    3: 'tredje',
    4: 'fjerde',
    5: 'femte',
    6: 'sjette',
    7: 'sjuende',
    8: 'åttende',
    9: 'niende',
    10: 'tiende',
    11: 'ellevte',
    12: 'tolvte',
    13: 'trettende',
    14: 'fjortende',
    15: 'femtende',
    16: 'sekstende',
    17: 'syttende',
    18: 'attende',
    19: 'nittende',
    20: 'tjuende',
    30: 'trettiende',
    40: 'førtiende',
    50: 'femtiende',
    60: 'sekstiende',
    70: 'syttiende',
    80: 'åttiende',
    90: 'nittiende',
    100: 'hundrede',
    1000: 'tusende',
    1000000: 'millionte',
}

# variant ordinal forms accepted when parsing (Bokmålsordboka)
_STRING_ORDINAL_NB = invert_dict(_ORDINAL_STRING_NB)
_STRING_ORDINAL_NB.update({
    'annen': 2,
    'annet': 2,
    'syvende': 7,
    'tyvende': 20,
})

_FRACTION_STRING_NB = {
    2: 'halv',
    3: 'tredjedel',
    4: 'fjerdedel',
    5: 'femtedel',
    6: 'sjettedel',
    7: 'sjuendedel',
    8: 'åttendedel',
    9: 'niendedel',
    10: 'tiendedel',
    11: 'ellevtedel',
    12: 'tolvtedel',
    13: 'trettendedel',
    14: 'fjortendedel',
    15: 'femtendedel',
    16: 'sekstendedel',
    17: 'syttendedel',
    18: 'attendedel',
    19: 'nittendedel',
    20: 'tjuendedel',
}

# variant fraction forms accepted when parsing (Bokmålsordboka)
_STRING_FRACTION_NB = invert_dict(_FRACTION_STRING_NB)
_STRING_FRACTION_NB.update({
    'halvdel': 2,
    'tredel': 3,
    'kvart': 4,
    'firedel': 4,
    'femdel': 5,
    'seksdel': 6,
    'sjudel': 7,
    'syvendedel': 7,
    'åttedel': 8,
    'nidel': 9,
    'tidel': 10,
})

_NEGATIVES_NB = {'minus'}
_NUMBER_CONNECTORS_NB = {'og'}
_COMMA_NB = {'komma'}

# fraction plural suffix: "to tredjedeler"
_FRACTION_PLURAL_SUFFIX_NB = 'er'

_TABLES_NB = None  # populated at the end of the module


class _NorwegianTables:
    """Bundle of the variant-specific word tables used by the engine."""

    def __init__(self, num_string, string_num, scale, scale_order,
                 ordinal_string, string_ordinal, fraction_string,
                 string_fraction, articles, negatives, connectors, comma,
                 fraction_plural_suffix, one_word, one_neuter_word):
        self.num_string = num_string
        self.string_num = string_num
        self.scale = scale
        self.scale_order = scale_order
        self.ordinal_string = ordinal_string
        self.string_ordinal = string_ordinal
        self.fraction_string = fraction_string
        self.string_fraction = string_fraction
        self.articles = articles
        self.negatives = negatives
        self.connectors = connectors
        self.comma = comma
        self.fraction_plural_suffix = fraction_plural_suffix
        self.one_word = one_word  # "en" / "ein"
        self.one_neuter_word = one_neuter_word  # "ett" / "eitt"


# ---------------------------------------------------------------------------
# pronunciation
# ---------------------------------------------------------------------------

def _pronounce_below_hundred(num, t):
    """21 -> 'tjueen' (modern tens-first order, written as one word)."""
    if num == 1:
        return t.one_word
    if num <= 20:
        return t.num_string[num]
    tens = (num // 10) * 10
    ones = num % 10
    result = t.num_string[tens]
    if ones > 0:
        result += t.num_string[ones] if ones != 1 else t.one_word
    return result


def _pronounce_triplet(num, t):
    """256 -> 'to hundre og femtiseks' (space-separated per Språkrådet)."""
    result = ""
    num = floor(num)
    if num > 99:
        hundreds = num // 100
        if hundreds == 1:
            result += 'hundre'
        else:
            result += t.num_string[hundreds] + ' hundre'
        num -= hundreds * 100
        if num > 0:
            result += ' og '
    if num > 0:
        result += _pronounce_below_hundred(num, t)
    return result


def _pronounce_whole_number(num, t, scale_level=0):
    if num == 0:
        return ''
    num = floor(num)
    result = ''
    last_triplet = num % 1000

    if last_triplet > 0:
        if scale_level == 0:
            result = _pronounce_triplet(last_triplet, t)
        elif scale_level == 1:
            if last_triplet == 1:
                result = 'tusen '
            else:
                result = _pronounce_triplet(last_triplet, t) + ' tusen '
        else:
            scale_word = t.scale_order[scale_level]
            if last_triplet == 1:
                result = t.one_word + ' ' + scale_word + ' '
            else:
                result = _pronounce_triplet(last_triplet, t) + ' ' + \
                    scale_word + t.fraction_plural_suffix + ' '

    higher = _pronounce_whole_number(num // 1000, t, scale_level + 1)
    if higher and scale_level == 0 and last_triplet:
        # "og" before a final part below one hundred: "to tusen og tjuetre"
        if last_triplet < 100:
            result = 'og ' + result
        return higher.rstrip() + ' ' + result
    return higher + result


def _pronounce_number(number, t, places=2):
    result = ""
    if abs(number) >= 1000000000000000000000:  # beyond named scale words
        return str(number)
    if number == 0:
        return t.num_string[0]
    if number < 0:
        return "minus " + _pronounce_number(abs(number), t, places)
    if number == int(number):
        return _pronounce_whole_number(number, t).strip()
    whole_number_part = floor(number)
    fractional_part = number - whole_number_part
    result += _pronounce_whole_number(whole_number_part, t).strip() or \
        t.num_string[0]
    if places > 0:
        result += " komma"
        num = round(fractional_part, places)
        place = 10
        while places > 0:
            result += " " + t.num_string[int(num * place) % 10]
            place *= 10
            places -= 1
    return result


def _pronounce_ordinal(number, t):
    if number < 0 or number != int(number):
        return str(number)
    number = int(number)
    if number in t.ordinal_string:
        return t.ordinal_string[number]
    if number < 100:
        tens = (number // 10) * 10
        ones = number % 10
        return t.num_string[tens] + t.ordinal_string[ones]
    # 121 -> "hundre og tjueførste": cardinal prefix + ordinal last element
    for scale in (1000000, 1000, 100):
        if number >= scale:
            remainder = number % scale
            if remainder == 0:
                prefix = number // scale
                lead = '' if prefix == 1 and scale <= 1000 else \
                    _pronounce_whole_number(prefix, t).strip() + ' '
                if prefix == 1 and scale == 100:
                    return t.ordinal_string[100]
                if prefix == 1 and scale == 1000:
                    return t.ordinal_string[1000]
                return lead + t.ordinal_string[scale]
            head = number - remainder
            return _pronounce_whole_number(head, t).strip() + ' og ' + \
                _pronounce_ordinal(remainder, t)
    return str(number)


def _nice_number(number, t, speech=True, denominators=range(1, 21)):
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        return str(round(number, 3)).replace(".", ",")
    whole, num, den = result
    if not speech:
        if num == 0:
            return str(whole)
        return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    den_str = t.fraction_string[den]
    if num > 1:
        den_str += t.fraction_plural_suffix
    if whole == 0:
        return '{} {}'.format(num, den_str)
    return '{} og {} {}'.format(whole, num, den_str)


# ---------------------------------------------------------------------------
# parsing
# ---------------------------------------------------------------------------

def _is_numeric(input_str):
    if input_str.endswith('.'):
        return False
    try:
        float(input_str)
        return True
    except ValueError:
        return False


def _is_number(word, t):
    if _is_numeric(word):
        return int(word) if word.isdigit() else float(word)
    if word in t.string_num:
        return t.string_num[word]
    if word in t.scale:
        return t.scale[word]
    return None


def _split_compound_number(word, t):
    """Split a compound number word into its component number words.

    Handles both counting traditions:
    "tjueen" -> ["tjue", "en"] and "enogtyve" -> ["en", "og", "tyve"]
    "tohundreogfemtiseks" -> ["to", "hundre", "og", "femti", "seks"]

    Returns None if the word is not composed purely of known number words.
    """
    if word in t.string_num or word in t.scale:
        return None
    keys = sorted(set(t.string_num) | set(t.scale), key=len, reverse=True)
    parts, rest = [], word
    while rest:
        if rest.startswith("og") and parts:
            candidate = rest[2:]
            if any(candidate.startswith(k) for k in keys):
                parts.append("og")
                rest = candidate
                continue
        for k in keys:
            if rest.startswith(k):
                parts.append(k)
                rest = rest[len(k):]
                break
        else:
            return None
    return parts if len(parts) > 1 else None


def _compound_value(parts, t):
    """Evaluate the numeric value of a split compound number word.

    Simple summation below one hundred covers both counting traditions:
    tjue + en = enogtyve = 21.
    """
    total = current = 0
    for p in parts:
        if p == "og":
            continue
        v = t.string_num.get(p)
        if v is None:
            v = t.scale.get(p)
            if v is None:
                return None
            if v >= 1000:
                total += max(current, 1) * v
                current = 0
            else:  # hundre
                current = max(current, 1) * 100
        else:
            current += v
    return total + current


def _word_value(word, t):
    """Value of a single (possibly compound) Norwegian number word."""
    if word in t.string_num:
        return t.string_num[word]
    if word in t.scale:
        return t.scale[word]
    parts = _split_compound_number(word, t)
    if parts:
        return _compound_value(parts, t)
    return None


def _expand_compound_numbers(text, t):
    """Rewrite compound number words as their digit value for parsing.

    Norwegian writes large numbers as space-separated phrases per Språkrådet
    ("to hundre og femtiseks"), so after expanding single-word compounds the
    resulting digit and scale tokens are merged into one value.
    """
    expanded = []
    for w in text.split():
        parts = _split_compound_number(w, t)
        if parts:
            value = _compound_value(parts, t)
            expanded.append(str(int(value)) if value is not None else w)
        else:
            expanded.append(w)

    def _int_value(w):
        if w.isdigit():
            return int(w)
        if w in t.string_num:
            return t.string_num[w]
        return None

    out = []
    i = 0
    while i < len(expanded):
        word = expanded[i]
        if _int_value(word) is None and word not in t.scale:
            out.append(word)
            i += 1
            continue
        # accumulate a span of number/scale tokens, "og"-joined parts only
        # when they refine a larger magnitude ("hundre og tjuetre")
        total = current = 0
        prev_was_scale = True  # a span may open with any number token
        span_len = 0
        j = i
        while j < len(expanded):
            w = expanded[j]
            v = _int_value(w)
            if w in t.scale and (current or total or w != 'million'):
                scale = t.scale[w]
                if scale >= 1000:
                    total += max(current, 1) * scale
                    current = 0
                else:  # hundre
                    current = max(current, 1) * 100
                prev_was_scale = True
            elif v is not None and (prev_was_scale or span_len == 0):
                current += v
                prev_was_scale = False
            elif w == 'og' and j + 1 < len(expanded) and span_len:
                nxt = _int_value(expanded[j + 1])
                if nxt is not None and nxt < (total + current):
                    j += 1
                    current += nxt
                    prev_was_scale = False
                else:
                    break
            else:
                break
            span_len = j - i + 1
            j += 1
        if span_len > 1:
            out.append(str(total + current))
            i += span_len
        else:
            out.append(word)
            i += 1
    return " ".join(out)


def _is_ordinal(input_str, t):
    """Ordinal detection, including compounds like "tjueførste" (21st)."""
    word = input_str.lower().strip()
    if word in t.string_ordinal:
        return t.string_ordinal[word]
    # compound: cardinal prefix + ordinal tail ("tjueførste", "tohundrede")
    for tail in sorted(t.string_ordinal, key=len, reverse=True):
        if word.endswith(tail) and len(word) > len(tail):
            prefix = word[:-len(tail)]
            if prefix.endswith("og"):
                prefix = prefix[:-2]
            prefix_val = _word_value(prefix, t)
            if prefix_val is None:
                continue
            tail_val = t.string_ordinal[tail]
            if tail_val >= 100:
                return max(prefix_val, 1) * tail_val
            return prefix_val + tail_val
    return False


def _is_fractional(input_str, t):
    """Check if the input is a spoken fraction, return its value."""
    input_str = input_str.lower()
    if input_str in t.string_num or input_str in t.scale:
        return False

    numerator = 1
    prev_number = 0
    denominator = False

    _bucket = input_str.split('/')
    if look_for_fractions(_bucket):
        return float(_bucket[0]) / float(_bucket[1])

    word = input_str
    # plural: "tredjedeler" (nb) / "tredjedelar" (nn)
    for suffix in (t.fraction_plural_suffix, 'e'):
        if word.endswith('del' + suffix):
            word = word[:-len(suffix)]
            break

    remainder = ""
    for fraction in sorted(t.string_fraction, key=len, reverse=True):
        if word.endswith(fraction):
            denominator = t.string_fraction[fraction]
            remainder = word[:-len(fraction)]
            break

    if not denominator:
        if word == "trekvart":
            return 3.0 / 4
        return False

    if remainder:
        value = _word_value(remainder, t)
        if value is None:
            return False
        numerator = value

    return prev_number + (numerator / denominator)


def _extract_real_number_with_text(tokens, t):
    """Token-level extraction engine (shared with the Danish parser design)."""
    number_words = []
    val = _val = _current_val = None
    _comma = False
    to_sum = []

    for idx, token in enumerate(tokens):
        _prev_val = _current_val
        _current_val = None
        word = token.word

        if word in t.connectors and not number_words:
            continue
        if word in (t.negatives | t.connectors | t.comma):
            number_words.append(token)
            if word in t.comma:
                _comma = token
                _current_val = _val or _prev_val
            continue

        prev_word = tokens[idx - 1].word if idx > 0 else ""
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""

        if word not in t.string_num and \
                word not in t.scale and \
                not _is_numeric(word) and \
                not _is_fractional(word, t):
            words_only = [tok.word for tok in number_words]
            if _val is not None:
                to_sum.append(_val)
            if to_sum:
                if to_sum[0] < 0:
                    val = to_sum[0] - sum(to_sum[1:])
                else:
                    val = sum(to_sum)

            if number_words and (not all([w in t.articles | t.negatives
                                          | t.connectors for w in words_only])
                                 or str(val) == number_words[-1].word):
                break
            else:
                number_words.clear()
                to_sum.clear()
                val = _val = _prev_val = None
            continue
        elif word not in t.scale \
                and prev_word not in t.scale \
                and prev_word not in t.connectors \
                and prev_word not in t.negatives \
                and prev_word not in t.comma \
                and prev_word not in t.string_num \
                and not _is_numeric(prev_word) \
                and not _is_fractional(prev_word, t):
            number_words = [token]
        else:
            number_words.append(token)

        _val = _current_val = _is_number(word, t)

        if _current_val is not None and prev_word in t.negatives:
            _val = 0 - _current_val

        # is the prev word a number and should we multiply it?
        if _prev_val is not None and (word in t.scale or word in t.articles):
            to_sum.append(_prev_val * _current_val or _current_val)
            _val = _current_val = None

        _fraction_val = _is_fractional(word, t)
        if _fraction_val:
            if _prev_val is not None and prev_word not in t.articles and \
                    word not in t.string_fraction:  # compound fraction word
                _val = _prev_val + _fraction_val
                if prev_word not in t.connectors and \
                        tokens[idx - 1] not in number_words:
                    number_words.append(tokens[idx - 1])
            elif _prev_val is not None:
                _val = _prev_val * _fraction_val
                if tokens[idx - 1] not in number_words:
                    number_words.append(tokens[idx - 1])
            else:
                _val = _fraction_val
            _current_val = _val

        # directly following numbers without relation
        if (_is_numeric(prev_word) or prev_word in t.string_num) \
                and not _fraction_val and not _is_fractional(next_word, t) \
                and not to_sum:
            val = _prev_val
            number_words.pop(-1)
            break

        # spoken decimals
        if _current_val is not None and _comma:
            to_sum.append(_current_val if _current_val >= 10 else
                          _current_val / (10 ** (token.index - _comma.index)))
            _val = _current_val = None

        if _current_val is not None and \
                next_word in (t.connectors | t.comma | {""}):
            to_sum.append(_val or _current_val)
            _val = _current_val = None

        if not next_word and number_words:
            _negative = any(_tok.word.lower() in t.negatives
                            for _tok in number_words)
            if to_sum and to_sum[0] < 0:
                val = to_sum[0] - sum(to_sum[1:])
            else:
                val = sum(to_sum) if to_sum else _val
            # a zero whole part ("minus null komma fem") leaves the sign in
            # neither the value nor to_sum[0]; recover it from the minus token
            if _negative and isinstance(val, (int, float)) and val > 0:
                val = -val

    return val, number_words


def _extract_number_with_text(tokens, t, ordinals=False):
    if ordinals:
        for token in tokens:
            ordinal = _is_ordinal(token.word, t)
            if ordinal is not False:
                return ReplaceableNumber(ordinal, [token])
    val, number_words = _extract_real_number_with_text(tokens, t)
    return ReplaceableNumber(val, number_words)


def _extract_numbers_with_text(tokens, t, ordinals=False, fractions=True):
    placeholder = "<placeholder>"
    results = []
    while True:
        to_replace = _extract_number_with_text(tokens, t, ordinals)
        if not to_replace:
            break
        if isinstance(to_replace.value, float) and not fractions:
            pass
        else:
            results.append(to_replace)
        tokens = [
            tok if not
            to_replace.start_index <= tok.index <= to_replace.end_index
            else Token(placeholder, tok.index) for tok in tokens
        ]
    results.sort(key=lambda n: n.start_index)
    return results


def _extract_number(text, t, ordinals=False):
    text = _expand_compound_numbers(text.lower(), t)
    if ordinals:
        for word in text.split():
            ordinal = _is_ordinal(word.strip(".,!?;:"), t)
            if ordinal is not False:
                return ordinal
        return False
    numbers = _extract_numbers_with_text(tokenize(text), t)
    if not numbers:
        return False
    number = float(numbers[0].value)
    if number.is_integer():
        number = int(number)
    return number


def _numbers_to_digits(text, t, ordinals=False, fractions=True):
    text = _expand_compound_numbers(text, t)
    tokens = tokenize(text)
    numbers_to_replace = _extract_numbers_with_text(tokens, t, ordinals,
                                                    fractions)
    numbers_to_replace.sort(key=lambda number: number.start_index)

    results = []
    for token in tokens:
        if not numbers_to_replace or \
                token.index < numbers_to_replace[0].start_index:
            results.append(token.word)
        else:
            if numbers_to_replace and \
                    token.index == numbers_to_replace[0].start_index:
                results.append(str(numbers_to_replace[0].value))
            if numbers_to_replace and \
                    token.index == numbers_to_replace[0].end_index:
                numbers_to_replace.pop(0)

    return ' '.join(results)


_TABLES_NB = _NorwegianTables(
    num_string=_NUM_STRING_NB,
    string_num=_STRING_NUM_NB,
    scale=_SCALE_NB,
    scale_order=_SCALE_ORDER_NB,
    ordinal_string=_ORDINAL_STRING_NB,
    string_ordinal=_STRING_ORDINAL_NB,
    fraction_string=_FRACTION_STRING_NB,
    string_fraction=_STRING_FRACTION_NB,
    articles=_ARTICLES_NB,
    negatives=_NEGATIVES_NB,
    connectors=_NUMBER_CONNECTORS_NB,
    comma=_COMMA_NB,
    fraction_plural_suffix=_FRACTION_PLURAL_SUFFIX_NB,
    one_word='en',
    one_neuter_word='ett',
)


# ---------------------------------------------------------------------------
# public Bokmål API
# ---------------------------------------------------------------------------

def nice_number_nb(number, speech=True, denominators=range(1, 21)):
    """Bokmål helper for nice_number: 4.5 -> "4 og 1 halv"."""
    return _nice_number(number, _TABLES_NB, speech, denominators)


def pronounce_number_nb(number, places=2, short_scale=False,
                        scientific=False, ordinals=False):
    """Convert a number to its spoken Bokmål equivalent.

    Uses the modern tens-first counting order ("tjueen") and the official
    modern forms "sju"/"tjue" (1951 counting reform).
    """
    if ordinals:
        return pronounce_ordinal_nb(number)
    return _pronounce_number(number, _TABLES_NB, places)


def pronounce_ordinal_nb(number):
    """Pronounce a number as a Bokmål ordinal: 21 -> "tjueførste"."""
    return _pronounce_ordinal(number, _TABLES_NB)


def is_ordinal_nb(input_str):
    """Return the value of a Bokmål ordinal word, or False."""
    return _is_ordinal(input_str, _TABLES_NB)


def is_fractional_nb(input_str, short_scale=False):
    """Return the value of a Bokmål fraction word, or False."""
    return _is_fractional(input_str, _TABLES_NB)


def extract_number_nb(text, short_scale=False, ordinals=False):
    """Extract a number from Bokmål text, both counting traditions."""
    return _extract_number(text, _TABLES_NB, ordinals)


def numbers_to_digits_nb(text, short_scale=False, ordinals=False,
                         fractions=True):
    """Replace spoken Bokmål numbers in a text with digits."""
    return _numbers_to_digits(text, _TABLES_NB, ordinals, fractions)

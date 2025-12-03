"""Asturian number parser

Ported by a non-speaker based on
https://www.omniglot.com/language/numbers/asturian.htm
https://www.languagesandnumbers.com/how-to-count-in-asturian/en/ast

Supports:
- cardinal pronunciation (0..large) with short/long scales
- ordinal pronunciation (masculine/feminine)
- fraction recognition and pronunciation
- extraction of numbers from Asturian text (cardinals, ordinals, fractions, decimals)
- conversion of written numbers in text to digits
- tokenization utility

Notes about Asturian specifics implemented:
- Units, tens, hundreds, and composite 20s included
- Hundreds do NOT insert a conjunction before the remainder ("ciento un", not "ciento y un")
- Tens+units are joined with "y" (e.g. "trenta y un")
- Scale grouping (mil, millón) does not insert conjunctions between groups
- Fraction phrases like "tres cuartos" -> 0.75 are supported
"""

import re
from typing import List, Union, Dict, Tuple

from ovos_number_parser.util import Scale, GrammaticalGender, DigitPronunciation

# --- Asturian number dictionaries ---
# Units (base masculine forms). Feminine handled at runtime.
_UNITS_AST: Dict[int, str] = {
    1: 'un', 2: 'dos', 3: 'tres', 4: 'cuatro', 5: 'cinco', 6: 'seis',
    7: 'siete', 8: 'ocho', 9: 'nueve'
}

# Feminine special forms
_FEMALE_UNITS_AST: Dict[str, int] = {
    'una': 1
}

# Tens and teens
_TENS_AST: Dict[int, str] = {
    10: 'diez', 11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce',
    15: 'quince', 16: 'dieciséis', 17: 'diecisiete', 18: 'dieciocho',
    19: 'diecinueve', 20: 'venti', 30: 'trenta', 40: 'cuarenta',
    50: 'cincuenta', 60: 'sesenta', 70: 'setenta', 80: 'ochenta',
    90: 'noventa'
}

# Composite 20s (common written forms)
_COMPOSITE_20s_AST: Dict[int, str] = {
    21: 'ventiuno', 22: 'ventidós', 23: 'ventitrés', 24: 'venticuatro',
    25: 'venticinco', 26: 'ventiséis', 27: 'ventisiete', 28: 'ventiocho',
    29: 'ventinueve'
}

# Hundreds
_HUNDREDS_AST: Dict[int, str] = {
    100: 'cien', 200: 'doscientos', 300: 'trescientos', 400: 'cuatrocientos',
    500: 'quinientos', 600: 'seiscientos', 700: 'setecientos',
    800: 'ochocientos', 900: 'novecientos'
}

# Fraction word base (denominator -> word)
_FRACTION_STRING_AST: Dict[int, str] = {
    2: 'mediu', 3: 'terciu', 4: 'cuartu', 5: 'quintu', 6: 'sestu',
    7: 'séptimu', 8: 'octavu', 9: 'novenu', 10: 'décimu',
    11: 'onceavos', 12: 'doceavos'
}

# Ordinals (masculine base). Feminine formed by changing -u -> -a when possible.
_ORDINAL_UNITS_AST: Dict[int, str] = {
    1: 'primeru', 2: 'segundu', 3: 'terceru', 4: 'cuartu', 5: 'quintu',
    6: 'sestu', 7: 'séptimu', 8: 'octavu', 9: 'novenu'
}

_ORDINAL_TENS_AST: Dict[int, str] = {
    10: 'décimu', 20: 'ventésimu', 30: 'trentésimu', 40: 'cuarentenu',
    50: 'cincuentenu', 60: 'sesentenu', 70: 'setentenu', 80: 'ochentenu',
    90: 'noventenu'
}

_ORDINAL_HUNDREDS_AST: Dict[int, str] = {
    100: 'centésimu'
}

# Ordinal scales (value, masculine form)
_ORDINAL_SCALES_AST: Dict[Scale, List[Tuple[int, str]]] = {
    # TODO - bigger numbers
    Scale.SHORT: [
        (10 ** 6, 'millonésimu'),
        (10 ** 3, 'milésimu')
    ],
    Scale.LONG: [
        (10 ** 6, 'millonésimu'),
        (10 ** 3, 'milésimu')
    ]
}

# Cardinal scales: (value, singular, plural)
_SCALES_AST: Dict[Scale, List[Tuple[int, str, str]]] = {
    # TODO - bigger numbers
    Scale.SHORT: [
        (10 ** 6, 'millón', 'millones'),
        (10 ** 3, 'mil', 'mil')
    ],
    Scale.LONG: [
        (10 ** 6, 'millón', 'millones'),
        (10 ** 3, 'mil', 'mil')
    ]
}

# Build base token map including composite forms
_NUMBERS_BASE_AST: Dict[str, int] = {
    **_FEMALE_UNITS_AST,
    **{v: k for k, v in _UNITS_AST.items()},
    **{v: k for k, v in _TENS_AST.items()},
    **{v: k for k, v in _HUNDREDS_AST.items()},
    **{v: k for k, v in _COMPOSITE_20s_AST.items()},
    'ciento': 100
}


def _swap_gender_ast(word: str, gender: GrammaticalGender) -> str:
    """Swap ordinal/adjective endings between masculine and feminine where applicable.

    For Asturian, ordinals typically end in -u (masc.) and -a (fem.).
    """
    if gender == GrammaticalGender.FEMININE:
        if word.endswith('u'):
            return word[:-1] + 'a'
        if word.endswith('imu'):
            return word[:-1] + 'a'
    else:
        if word.endswith('a'):
            return word[:-1] + 'u'
    return word


def _pronounce_up_to_999_ast(n: int, gender: GrammaticalGender = GrammaticalGender.MASCULINE) -> str:
    """Pronounce integers from 0..999 in Asturian.

    Important rules implemented:
    - Hundreds do not insert conjunction before remainder (ciento un)
    - Tens+units are joined by 'y' (trenta y un)
    - Composite 20s handled (ventiuno...)
    """
    if gender == GrammaticalGender.FEMININE and n == 1:
        return 'una'
    if not 0 <= n <= 999:
        raise ValueError('Number must be between 0 and 999.')
    if n == 0:
        return 'ceru'
    if n == 100:
        return 'cien'

    parts: List[str] = []

    # Hundreds
    if n >= 100:
        hundred = (n // 100) * 100
        if hundred == 100 and n > 100:
            # use 'ciento' as prefix
            parts.append('ciento')
        else:
            parts.append(_HUNDREDS_AST[hundred])
        n %= 100

    # Tens and units
    if n > 0:
        # composite 20s
        if n in _COMPOSITE_20s_AST:
            parts.append(_COMPOSITE_20s_AST[n])
        elif n < 20:
            parts.append(_TENS_AST.get(n) or _UNITS_AST.get(n, ''))
        else:
            ten = (n // 10) * 10
            unit = n % 10
            parts.append(_TENS_AST[ten])
            if unit > 0:
                parts.append('y')
                parts.append(_UNITS_AST[unit])

    return ' '.join(parts)


def _pronounce_ordinal_up_to_999_ast(n: int, gender: GrammaticalGender = GrammaticalGender.MASCULINE) -> str:
    """Return Asturian ordinal (0..999) with gender adjustment."""
    if not 0 <= n <= 999:
        raise ValueError('Number must be between 0 and 999.')
    if n == 0:
        return 'ceru'

    parts: List[str] = []

    # Hundreds
    if n >= 100:
        hundred_val = (n // 100) * 100
        h_word = _ORDINAL_HUNDREDS_AST.get(hundred_val)
        if h_word:
            parts.append(_swap_gender_ast(h_word, gender))
        n %= 100

    if n > 0:
        if n % 10 == 0 and n > 10:
            tens_word = _ORDINAL_TENS_AST.get(n)
            if tens_word:
                parts.append(_swap_gender_ast(tens_word, gender))
        elif n < 10:
            units_word = _ORDINAL_UNITS_AST.get(n)
            if units_word:
                parts.append(_swap_gender_ast(units_word, gender))
        elif n < 20:
            tens_base = _ORDINAL_TENS_AST.get(10)
            units_word = _ORDINAL_UNITS_AST.get(n - 10)
            if tens_base and units_word:
                parts.append(f"{_swap_gender_ast(tens_base, gender)} {_swap_gender_ast(units_word, gender)}")
        else:
            tens_word = _ORDINAL_TENS_AST.get((n // 10) * 10)
            units_word = _ORDINAL_UNITS_AST.get(n % 10)
            if tens_word and units_word:
                parts.append(f"{_swap_gender_ast(tens_word, gender)} {_swap_gender_ast(units_word, gender)}")

    return ' '.join(parts)


def pronounce_ordinal_ast(number: Union[int, float], gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                          scale: Scale = Scale.LONG) -> str:
    """Pronounce ordinals in Asturian, supporting large scales."""
    if not isinstance(number, (int, float)):
        raise TypeError('Number must be an int or float.')
    if number == 0:
        return 'ceru'
    if number < 0:
        return f"menos {pronounce_ordinal_ast(abs(number), gender, scale)}"

    n = int(number)
    if n < 1000:
        return _pronounce_ordinal_up_to_999_ast(n, gender)

    ordinal_scale_defs = _ORDINAL_SCALES_AST[scale]

    # find largest scale
    scale_val = None
    scale_name = None
    for sv, sname in ordinal_scale_defs:
        if n >= sv:
            scale_val = sv
            scale_name = sname
            break

    if scale_val is None:
        # fallback
        return _pronounce_ordinal_up_to_999_ast(n, gender)

    count = n // scale_val
    remainder = n % scale_val

    if count == 1 and scale_val >= 1000:
        count_str = _swap_gender_ast(scale_name, gender)
    else:
        count_pron = pronounce_number_ast(count, scale=scale)
        scale_word = _swap_gender_ast(scale_name, gender)
        count_str = f"{count_pron} {scale_word}"

    if remainder == 0:
        return count_str

    remainder_str = pronounce_ordinal_ast(remainder, gender, scale)
    return f"{count_str} {remainder_str}"


def _fraction_variants(word: str) -> List[str]:
    """Generate common variants for a denominator word: asturian u->o and plural forms."""
    variants = {word, word + 's'}
    # if ends with 'u', produce 'o' variant
    if word.endswith('u'):
        o = word[:-1] + 'o'
        variants.add(o)
        variants.add(o + 's')
    return list(variants)


def is_fractional_ast(input_str: str) -> Union[float, bool]:
    """Return fractional float value if input is recognized as Asturian fraction word."""
    s = input_str.lower().strip()
    # normalize plural forms
    if s.endswith('s') and s not in _FRACTION_STRING_AST.values():
        s = s[:-1]
    # handle 'mediu' / 'media' variants
    if s == 'media':
        s = 'mediu'
    for den, word in _FRACTION_STRING_AST.items():
        for v in _fraction_variants(word):
            if s == v:
                return 1.0 / den
    return False


def pronounce_fraction_ast(word: str, scale: Scale = Scale.LONG) -> str:
    n1, n2 = word.split('/')
    n1_i, n2_i = int(n1), int(n2)
    if n2_i in _FRACTION_STRING_AST:
        denom = _FRACTION_STRING_AST[n2_i]
        if n1_i != 1 and not denom.endswith('s'):
            denom = denom + 's'
    else:
        denom = pronounce_number_ast(n2_i, scale=scale)
        if n1_i > 1:
            denom += ' avos'
    num = pronounce_number_ast(n1_i, scale=scale)
    return f"{num} {denom}"


# -------------------- Recognition / Extraction --------------------

def is_ordinal_ast(input_str: str) -> bool:
    """Check whether a token is an Asturian ordinal (masculine or feminine)."""
    tok = input_str.lower().strip()
    # normalize to masculine for lookup
    if tok.endswith('a'):
        tok_m = tok[:-1] + 'u'
    else:
        tok_m = tok
    if tok_m in set(_ORDINAL_UNITS_AST.values()):
        return True
    if tok_m in set(_ORDINAL_TENS_AST.values()):
        return True
    if tok_m in set(_ORDINAL_HUNDREDS_AST.values()):
        return True
    # scales
    for sv, sname in _ORDINAL_SCALES_AST[Scale.SHORT]:
        if tok == sname or tok == _swap_gender_ast(sname, GrammaticalGender.FEMININE):
            return True
    return False


def extract_number_ast(text: str, ordinals: bool = False, scale: Scale = Scale.LONG) -> Union[int, float, bool]:
    """
    Extract numeric value from Asturian text phrase.
    Supports cardinals, ordinals (if ordinals=True), fraction phrases, decimals and scales.
    """
    numbers_map = {
        **_NUMBERS_BASE_AST,
        **{s_name: val for val, s_name, _ in _SCALES_AST[scale]},
        **{p_name: val for val, _, p_name in _SCALES_AST[scale]}
    }

    clean = text.lower().replace('-', ' ')
    tokens = [t for t in clean.split()]

    result = 0.0
    current = 0.0
    number_consumed = False

    i = 0
    while i < len(tokens):
        token = tokens[i]
        # handle feminine 'una'
        if token in _FEMALE_UNITS_AST:
            val = _FEMALE_UNITS_AST[token]
        else:
            val = numbers_map.get(token)

        # standalone fraction words like 'mediu'
        frac = is_fractional_ast(token)
        if frac is not False:
            if current != 0:
                result += current * frac
            else:
                result += frac
            current = 0
            number_consumed = True
            i += 1
            continue

        # fraction phrases like 'tres cuartos'
        next_tok = tokens[i + 1] if i + 1 < len(tokens) else None
        if next_tok:
            nt_norm = next_tok[:-1] if next_tok.endswith('s') else next_tok
            matched = False
            for den, word in _FRACTION_STRING_AST.items():
                for variant in _fraction_variants(word):
                    if nt_norm == variant or nt_norm == variant.rstrip('s'):
                        num_val = val if val is not None else 1
                        result += float(num_val) * (1.0 / den)
                        current = 0
                        number_consumed = True
                        i += 2
                        matched = True
                        break
                if matched:
                    break
            if matched:
                continue

        if val is not None:
            # detect explicit scale tokens at current position: 'million/millones' etc.
            scale_handled = False
            for scale_val, sing, plur in _SCALES_AST[scale]:
                if token == sing or token == plur:
                    if current == 0:
                        current = 1
                    result += current * scale_val
                    current = 0
                    scale_handled = True
                    number_consumed = True
                    break
                # case 'dos millones' -> current token is 'dos' and next token 'millones'
                if next_tok and (next_tok == sing or next_tok == plur):
                    if val is None:
                        val = 1
                    result += val * scale_val
                    i += 2
                    scale_handled = True
                    number_consumed = True
                    break
            if scale_handled:
                continue

            # normal cardinal token
            current += val
            i += 1
            continue

        # ordinals (if requested)
        if ordinals and is_ordinal_ast(token):
            tok = token
            if tok.endswith('a'):
                tok = tok[:-1] + 'u'
            for num, word in _ORDINAL_UNITS_AST.items():
                if word == tok:
                    current += num
                    break
            for num, word in _ORDINAL_TENS_AST.items():
                if word == tok:
                    current += num
                    break
            i += 1
            continue

        # decimal marker
        if token in ['punto', 'coma', '.', ',']:
            decimal_str = ''
            j = i + 1
            while j < len(tokens):
                t = tokens[j]
                if t in numbers_map:
                    decimal_str += str(numbers_map[t])
                elif t.isdigit():
                    decimal_str += t
                else:
                    break
                j += 1
            if decimal_str:
                result += current + float('0.' + decimal_str)
                current = 0
                number_consumed = True
            i = j
            continue

        # otherwise skip
        i += 1

    if not number_consumed:
        result += current

    if result == int(result):
        return int(result)
    return result if result > 0 else False


def pronounce_number_ast(number: Union[int, float], places: int = 5, scale: Scale = Scale.LONG,
                         ordinals: bool = False, digits: DigitPronunciation = DigitPronunciation.FULL_NUMBER,
                         gender: GrammaticalGender = GrammaticalGender.MASCULINE) -> str:
    """Pronounce a number in Asturian (cardinal or ordinal), with decimals and large scales.

    API mirrors the original Portuguese implementation but with Asturian data and simplified gender rules.
    """
    if not isinstance(number, (int, float)):
        raise TypeError('Number must be an int or float.')
    if ordinals:
        return pronounce_ordinal_ast(number, gender, scale)
    if number == 0:
        return 'cero'
    if number < 0:
        return f"menos {pronounce_number_ast(abs(number), places, scale, ordinals, digits, gender)}"

    # Handle decimals (string check to avoid float representation issues)
    if isinstance(number, float) and '.' in str(number):
        integer_part = int(number)
        decimal_part_str = f"{number:.{places}f}".split('.')[1].rstrip('0')
        if decimal_part_str and int(decimal_part_str) == 0:
            return pronounce_number_ast(integer_part, places, scale, ordinals, digits, gender)

        int_pr = pronounce_number_ast(integer_part, places, scale, ordinals, digits, gender)

        decimal_parts: List[str] = []
        if decimal_part_str:
            if digits == DigitPronunciation.FULL_NUMBER:
                # pronounce up to first three digits as whole number
                decimal_parts.append(_pronounce_up_to_999_ast(int(decimal_part_str[:3]), gender))
            else:
                for ch in decimal_part_str:
                    decimal_parts.append(_pronounce_up_to_999_ast(int(ch), gender))

        decimal_pron = ' '.join(decimal_parts) or 'cero'
        decimal_word = 'punto'
        return f"{int_pr} {decimal_word} {decimal_pron}"

    # Integer handling
    n = int(number)
    if n < 1000:
        return _pronounce_up_to_999_ast(n, gender)

    scale_defs = _SCALES_AST[scale]
    # find largest scale that fits
    for scale_val, s_name, p_name in scale_defs:
        if n >= scale_val:
            break

    count = n // scale_val
    remainder = n % scale_val

    scale_word = s_name if count == 1 else p_name
    if count == 1 and scale_word == 'mil':
        count_str = scale_word
    else:
        count_pr = pronounce_number_ast(count, places, scale, ordinals, digits, gender)
        count_str = f"{count_pr} {scale_word}"

    if remainder == 0:
        return count_str

    # no conjunction between groups; just append remainder phrase
    remainder_str = pronounce_number_ast(remainder, places, scale, ordinals, digits, gender)
    return f"{count_str} {remainder_str}"


def numbers_to_digits_ast(utterance: str, scale: Scale = Scale.LONG) -> str:
    """Replace written Asturian numbers in a text string with digit equivalents."""
    words = tokenize(utterance)
    output: List[str] = []
    i = 0
    NUMBERS = {**_NUMBERS_BASE_AST, **{s_name: val for val, s_name, _ in _SCALES_AST[scale]},
               **{p_name: val for val, _, p_name in _SCALES_AST[scale]}}

    while i < len(words):
        if words[i] in NUMBERS or words[i] in _FEMALE_UNITS_AST:
            span = []
            j = i
            while j < len(words) and (words[j] in NUMBERS or words[j] in _FEMALE_UNITS_AST or words[j] in ['y', 'e']):
                span.append(words[j])
                j += 1
            phrase = ' '.join(span)
            val = extract_number_ast(phrase, scale=scale)
            if val is not False:
                output.append(str(val))
                i = j
            else:
                output.append(words[i])
                i += 1
        else:
            output.append(words[i])
            i += 1
    return ' '.join(output)


def tokenize(utterance: str) -> List[str]:
    """Tokenize text into words/punctuation.

    Preserves simple punctuation tokens and splits hyphenated words where appropriate.
    """
    # separate percent
    utterance = re.sub(r"([0-9]+)([\%])", r"\1 \2", utterance)
    # split #1
    utterance = re.sub(r"(\#)([0-9]+\b)", r"\1 \2", utterance)
    # split a-b but preserve numeric ranges
    utterance = re.sub(r"([a-zA-Z]+)(-)([a-zA-Z]+\b)", r"\1 \2 \3", utterance)
    tokens = utterance.split()
    if tokens and tokens[-1] == '-':
        tokens = tokens[:-1]
    return tokens


if __name__ == '__main__':
    print('--- Asturian number tests ---')
    print('16 ->', pronounce_number_ast(16))
    print('21 ->', pronounce_number_ast(21))
    print('35 ->', pronounce_number_ast(35))
    print('101 ->', pronounce_number_ast(101))
    print('1,234 ->', pronounce_number_ast(1234))
    print('1,000,000 ->', pronounce_number_ast(1_000_000))

    print('\n--- Ordinals ---')
    print('1st (m):', pronounce_ordinal_ast(1))
    print('1st (f):', pronounce_ordinal_ast(1, GrammaticalGender.FEMININE))
    print('23rd (m):', pronounce_ordinal_ast(23))
    print('100th:', pronounce_ordinal_ast(100))

    print('\n--- Extraction ---')
    print("'un millón' ->", extract_number_ast('un millón'))
    print("'dos millones trescientos' ->", extract_number_ast('dos millones trescientos'))
    print("'ventiuno' ->", extract_number_ast('ventiuno'))
    print("'tres cuartos' (fraction word) ->", extract_number_ast('tres cuartos'))

    print('\n--- numbers_to_digits_ast ---')
    print(numbers_to_digits_ast('hai dos millones e cincuenta persoas'))
    print(numbers_to_digits_ast('merquei ventiuno panes'))

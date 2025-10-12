from typing import List, Union, Dict, Tuple

from ovos_number_parser.numbers_pt import tokenize, _swap_gender  # consider implementing a mwl version if needed
from ovos_number_parser.util import Scale, GrammaticalGender, DigitPronunciation

DECIMAL_MARKERS = ["ponto", "birgula", "bírgula", ".", ","]

# --- Base Pronunciation Dictionaries ---

_UNITS: Dict[int, str] = {
    1: 'un', 2: 'dous', 3: 'trés', 4: 'quatro', 5: 'cinco', 6: 'seis',
    7: 'siete', 8: 'uito', 9: 'nuobe'
}

_TENS_MWL: Dict[int, str] = {
    10: 'dieç', 11: 'onze', 12: 'duoze', 13: 'treze', 14: 'catorze',
    15: 'quinze', 16: 'zasseis', 17: 'zassiete', 18: 'zuio', 19: 'zanuobe',
    20: 'binte', 30: 'trinta', 40: 'quarenta', 50: 'cinquenta', 60: 'sessenta',
    70: 'setenta', 80: 'uitenta', 90: 'nobenta'
}
_TENS_ALT_MWL: Dict[int, str] = {
    16: 'dezasseis', 17: 'dezassiete', 18: 'dezuito', 19: 'dezanuobe',
}

_HUNDREDS: Dict[int, str] = {
    100: 'cien', 200: 'duzientos', 300: 'trezientos', 400: 'quatrocientos',
    500: 'quinhentos', 600: 'seiscientos', 700: 'sietecientos',
    800: 'uitocientos', 900: 'nuobecientos'
}
_HUNDREDS_ALT: Dict[int, str] = {
    100: 'un ciento',
    200: 'dous cientos',
    300: 'trés cientos',
    400: 'quatro cientos',
    500: 'cinco cientos',
    600: 'seis cientos',
    700: 'siete cientos',
    800: 'uito cientos',
    900: 'nuobe cientos'
}

_FRACTION_STRING_M_MWL: Dict[int, str] = {
    2: 'meio', 3: 'tércio', 4: 'quarto', 5: 'quinto', 6: 'sesto',
    7: 'sétimo', 8: 'uitabo', 9: 'nono', 10: 'décimo',
    11: 'onze abos', 12: 'doze abos', 13: 'treze abos', 14: 'catorze abos',
    15: 'quinze abos', 16: 'dezasseis abos', 17: 'dezassete abos',
    18: 'dezoito abos', 19: 'dezanuobe abos',
    20: 'bigésimo', 30: 'trigésimo', 100: 'centésimo', 1000: 'milésimo'
}
_FRACTION_STRING_F_MWL: Dict[int, str] = {
    k: v[:-1] + "a"
    for k, v in _FRACTION_STRING_M_MWL.items() if v.endswith("o")
}
_FRACTION_STRING_MWL: Dict[int, str] = {
    **_FRACTION_STRING_M_MWL, **_FRACTION_STRING_F_MWL
}

_FEMALE_NUMS = {
    "ũa": 1,
    "dues": 2
}

# --- Ordinal Pronunciation Dictionaries (Masculine Base) ---

_ORDINAL_UNITS_MASC: Dict[int, str] = {
    1: 'purmerio', 2: 'segundo', 3: 'terceiro', 4: 'quarto', 5: 'quinto',
    6: 'sesto', 7: 'sétimo', 8: 'uitabo', 9: 'nono'
}
_ORDINAL_UNITS_FEM: Dict[int, str] = {
    k: v[:-1] + "a"
    for k, v in _ORDINAL_UNITS_MASC.items()
}

_ORDINAL_TENS_MASC: Dict[int, str] = {
    10: 'décimo', 20: 'bigésimo', 30: 'trigésimo', 40: 'quadragésimo',
    50: 'quinquagésimo', 60: 'sessagésimo', 70: 'setuagésimo',
    80: 'uctogésimo', 90: 'nonagésimo'
}
_ORDINAL_TENS_FEM: Dict[int, str] = {
    k: v[:-1] + "a"
    for k, v in _ORDINAL_TENS_MASC.items()
}

_ORDINAL_HUNDREDS_MASC: Dict[int, str] = {
    100: 'centésimo', 200: 'ducentésimo', 300: 'tricentésimo',
    400: 'quadringentésimo', 500: 'quingentésimo', 600: 'seiscentésimo',
    700: 'setingentésimo', 800: 'uctingentésimo', 900: 'noningentésimo'
}
_ORDINAL_HUNDREDS_FEM: Dict[int, str] = {
    k: v[:-1] + "a"
    for k, v in _ORDINAL_HUNDREDS_MASC.items()
}

_ORDINAL_SCALES_MASC: Dict[Scale, List[Tuple[int, str]]] = {
    Scale.SHORT: [
        (10 ** 21, "sextilionésimo"),
        (10 ** 18, "quintilionésimo"),
        (10 ** 15, "quadrilionésimo"),
        (10 ** 12, "trilionésimo"),
        (10 ** 9, "bilionésimo"),
        (10 ** 6, "milionésimo"),
        (10 ** 3, "milésimo")
    ],
    Scale.LONG: [
        (10 ** 36, "sextilionésimo"),
        (10 ** 30, "quintilionésimo"),
        (10 ** 24, "quadrilionésimo"),
        (10 ** 18, "trilionésimo"),
        (10 ** 12, "bilionésimo"),
        (10 ** 6, "milionésimo"),
        (10 ** 3, "milésimo")
    ]
}

_ORDINAL_SCALES_FEM: Dict[Scale, List[Tuple[int, str]]] = {
    Scale.SHORT: [(k, v[:-1] + "a")
                  for k, v in _ORDINAL_SCALES_MASC[Scale.SHORT]],
    Scale.LONG: [(k, v[:-1] + "a")
                 for k, v in _ORDINAL_SCALES_MASC[Scale.LONG]],

}

_SCALES: Dict[Scale, List[Tuple[int, str, str]]] = {
    Scale.SHORT: [
        (10 ** 21, "sextilion", "sextiliones"),
        (10 ** 18, "quintilion", "quintiliones"),
        (10 ** 15, "quadrilion", "quadriliones"),
        (10 ** 12, "trilion", "triliones"),
        (10 ** 9, "bilion", "biliones"),
        (10 ** 6, "milhon", "milhones"),
        (10 ** 3, "mil", "mil")
    ],
    Scale.LONG: [
        (10 ** 36, "sextilion", "sextiliones"),
        (10 ** 30, "quintilion", "quintiliones"),
        (10 ** 24, "quadrilion", "quadriliones"),
        (10 ** 18, "trilion", "triliones"),
        (10 ** 12, "bilion", "biliones"),
        (10 ** 6, "milhon", "milhones"),
        (10 ** 3, "mil", "mil")
    ]
}

# Mapping of number words to their integer values.
_NUMBERS_BASE = {
    **_FEMALE_NUMS,
    **{v: k for k, v in _UNITS.items()},
    **{v: k for k, v in _TENS_MWL.items()},
    **{v: k for k, v in _TENS_ALT_MWL.items()},
    **{v: k for k, v in _HUNDREDS.items()},
    **{v: k for k, v in _HUNDREDS_ALT.items()},
    "ciento": 100
}


def get_number_map(scale: Scale = Scale.LONG):
    return {
        **_NUMBERS_BASE,
        **{s_name: val for val, s_name, _ in _SCALES[scale]},
        **{p_name: val for val, _, p_name in _SCALES[scale]}
    }


_NUMBERS_MWL = get_number_map()

_ORDINAL_WORDS_MASC = {
    **{v: k for k, v in _ORDINAL_UNITS_MASC.items()},
    **{v: k for k, v in _ORDINAL_TENS_MASC.items()},
    **{v: k for k, v in _ORDINAL_HUNDREDS_MASC.items()},
    **{s_name: val for val, s_name in _ORDINAL_SCALES_MASC[Scale.SHORT]},
}
_ORDINAL_WORDS_FEM = {
    **{v: k for k, v in _ORDINAL_UNITS_FEM.items()},
    **{v: k for k, v in _ORDINAL_TENS_FEM.items()},
    **{v: k for k, v in _ORDINAL_HUNDREDS_FEM.items()},
    **{s_name: val for val, s_name in _ORDINAL_SCALES_FEM[Scale.SHORT]},
}
_ORDINAL_WORDS = {
    **_ORDINAL_WORDS_FEM,
    **_ORDINAL_WORDS_MASC,
}


def _pronounce_up_to_999(
        n: int,
        gender: GrammaticalGender = GrammaticalGender.MASCULINE
) -> str:
    """
    Returns the Mirandese cardinal pronunciation of an integer from 0 to 999

    Parameters:
        n (int): Integer to pronounce (must be between 0 and 999).

    Returns:
        str: The number pronounced in Mirandese words.

    Raises:
        ValueError: If n is not in the range 0 to 999.
    """
    # special cases for feminine 1 and 2  "ũa", "dues"
    if gender == GrammaticalGender.FEMININE:
        if n == 1:
            return "ũa"
        if n == 2:
            return "dues"

    if not 0 <= n <= 999:
        raise ValueError("Number must be between 0 and 999.")
    if n == 0:
        return "zero"
    if n == 100:
        return "cien"

    parts = []

    # Hundreds
    if n >= 100:
        hundred = n // 100 * 100
        parts.append("ciento" if hundred == 100 else _HUNDREDS_ALT[hundred])
        n %= 100
        if n > 0:
            parts.append("i")

    # Tens and Units
    if n > 0:
        if n < 20:
            parts.append(_TENS_MWL.get(n) or _UNITS.get(n, ""))
        else:
            ten = n // 10 * 10
            unit = n % 10
            parts.append(_TENS_MWL[ten])
            if unit > 0:
                parts.append("i")
                parts.append(_UNITS[unit])

    return " ".join(parts)


def _pronounce_ordinal_up_to_999(
        n: int,
        gender: GrammaticalGender = GrammaticalGender.MASCULINE
) -> str:
    """
    Returns the Mirandese ordinal word for an integer between 0 and 999, adjusting for grammatical gender

    Parameters:
        n (int): The integer to convert (must be between 0 and 999).

    Returns:
        str: The ordinal representation of the number in Mirandese.

    Raises:
        ValueError: If n is not between 0 and 999.
    """
    if not 0 <= n <= 999:
        raise ValueError("Number must be between 0 and 999.")
    if n == 0:
        return "zero"

    parts = []

    # Handle hundreds
    if n >= 100:
        hundred_val = n // 100 * 100
        hundred_word_masc = _ORDINAL_HUNDREDS_MASC.get(hundred_val)
        if hundred_word_masc:
            parts.append(_swap_gender(hundred_word_masc, gender))
        n %= 100

    # Handle tens and units
    if n > 0:
        # Ordinal numbers don't use 'e' as a separator
        if n % 10 == 0 and n > 10:
            tens_word_masc = _ORDINAL_TENS_MASC[n]
            parts.append(_swap_gender(tens_word_masc, gender))
        elif n < 10:
            units_word_masc = _ORDINAL_UNITS_MASC[n]
            parts.append(_swap_gender(units_word_masc, gender))
        elif n < 20:
            tens_word_masc = _ORDINAL_TENS_MASC[10]
            units_word_masc = _ORDINAL_UNITS_MASC[n - 10]
            parts.append(f"{_swap_gender(tens_word_masc, gender)} {_swap_gender(units_word_masc, gender)}")
        else:
            tens_word_masc = _ORDINAL_TENS_MASC[n // 10 * 10]
            units_word_masc = _ORDINAL_UNITS_MASC[n % 10]
            parts.append(f"{_swap_gender(tens_word_masc, gender)} {_swap_gender(units_word_masc, gender)}")

    return " ".join(parts)


def pronounce_ordinal_mwl(
        number: Union[int, float],
        gender: GrammaticalGender = GrammaticalGender.MASCULINE,
        scale: Scale = Scale.LONG
) -> str:
    """
    Return the ordinal pronunciation of a number in Mirandese, supporting grammatical gender and scale (short or long)

    Parameters:
        number (int or float): The number to pronounce as an ordinal.
        gender (GrammaticalGender, optional): The grammatical gender for the ordinal form (masculine or feminine).
        scale (Scale, optional): The numerical scale to use (short or long).

    Returns:
        str: The ordinal pronunciation of the number in Mirandese.

    Raises:
        TypeError: If `number` is not an int or float.
    """
    if not isinstance(number, (int, float)):
        raise TypeError("Number must be an int or float.")
    if number == 0:
        return "zero"

    if number < 0:
        return f"menos {pronounce_ordinal_mwl(abs(number), gender, scale)}"

    n = int(number)
    if n < 1000:
        return _pronounce_ordinal_up_to_999(n, gender)

    ordinal_scale_defs = _ORDINAL_SCALES_MASC[scale]

    # Find the largest scale that fits the number
    for scale_val, s_name in ordinal_scale_defs:
        if n >= scale_val:
            break

    count = n // scale_val
    remainder = n % scale_val

    # Special case for "milésimo" and other large scales where 'um' is not needed
    if count == 1 and scale_val >= 1000:
        count_str = _swap_gender(s_name, gender)
    else:
        # Pronounce the 'count' part of the number and the scale word
        count_pronunciation = pronounce_number_mwl(count, scale=scale)
        scale_word_masc = s_name
        scale_word = _swap_gender(scale_word_masc, gender)
        count_str = f"{count_pronunciation} {scale_word}"

    # If there's no remainder, we're done
    if remainder == 0:
        return count_str

    # Pronounce the remainder and join
    remainder_str = pronounce_ordinal_mwl(remainder, gender, scale)

    return f"{count_str} {remainder_str}"


def is_fractional_mwl(
        input_str: str
) -> Union[float, bool]:
    """
    Checks if the input string corresponds to a recognized Mirandese fractional word.

    Returns:
        The fractional value as a float if recognized (e.g., 0.5 for "meio" or "meia"); otherwise, False.
    """
    input_str = input_str.lower().strip()
    fraction_map = _FRACTION_STRING_MWL

    # Handle plural forms
    if input_str.endswith('s') and input_str not in fraction_map.values():
        input_str = input_str[:-1]

    # Handle "meio" vs "meia"
    if input_str == "meia":
        input_str = "meio"

    # Use a dynamic lookup instead of a hardcoded list
    for den, word in fraction_map.items():
        # Handle cases like "onze abos", so we check for the whole word
        if input_str == word:
            return 1.0 / den

    # Special case for "meia" as a female form of "meio" (1/2)
    if input_str in ["meia", "meio"]:
        return 0.5

    return False


def is_ordinal_mwl(input_str: str) -> bool:
    """
    Determine if a string is a Mirandese ordinal word.

    Returns:
        bool: True if the input string is recognized as a Mirandese ordinal, otherwise False.
    """
    return input_str in _ORDINAL_WORDS


def extract_number_mwl(
        text: str,
        ordinals: bool = False,
        scale: Scale = Scale.LONG
) -> Union[int, float, bool]:
    """
    Extracts a numeric value from a Mirandese text phrase, supporting cardinals, ordinals, fractions, and large scales.

    Parameters:
        text (str): The input phrase potentially containing a number.
        ordinals (bool): If True, recognizes ordinal words as numbers.
        scale (Scale): Specifies whether to use the short or long numerical scale.

    Returns:
        int or float: The extracted number if found; otherwise, False.
    """
    text = text.replace("bint'i", "binte i")
    numbers_map = get_number_map(scale)
    scales_map = _SCALES[scale]

    clean_text = text.lower().replace('-', ' ')
    tokens = [t for t in clean_text.split() if t != "i"]

    result = 0
    current_number = 0
    number_consumed = False

    for i, token in enumerate(tokens):
        if token is None:
            continue  # consumed in previous idx
        next_token = tokens[i + 1] if i < len(tokens) - 1 else None
        next_digit = numbers_map.get(next_token) if next_token else None
        val = numbers_map.get(token)
        if val is not None:
            if next_digit and next_digit > val:
                tokens[i + 1] = None
                current_number += val * next_digit
            else:
                current_number += val
        elif ordinals and is_ordinal_mwl(token):
            current_number += _ORDINAL_WORDS[token]
        elif is_fractional_mwl(token):
            fraction = is_fractional_mwl(token)
            result += current_number + fraction
            current_number = 0
            number_consumed = True
        else:
            # Handle large scales like milhão, bilhão
            found_scale = False
            for scale_val, singular, plural in scales_map:
                if token == singular or token == plural:
                    if current_number == 0:
                        current_number = 1
                    result += current_number * scale_val
                    current_number = 0
                    found_scale = True
                    number_consumed = True
                    break
            if not found_scale:
                if token in DECIMAL_MARKERS:
                    decimal_str = ''.join(
                        str(numbers_map.get(t, '')) for t in tokens[i + 1:]
                        if t in numbers_map
                    )
                    if decimal_str:
                        result += current_number + float(f"0.{decimal_str}")
                        number_consumed = True
                    current_number = 0
                    break

    if not number_consumed:
        result += current_number

    return result if result > 0 else False


def pronounce_number_mwl(
        number: Union[int, float],
        places: int = 5,
        scale: Scale = Scale.LONG,
        ordinals: bool = False,
        digits: DigitPronunciation = DigitPronunciation.FULL_NUMBER,
        gender: GrammaticalGender = GrammaticalGender.MASCULINE
) -> str:
    """
    Return the full Mirandese pronunciation of a number, supporting cardinal and ordinal forms, decimals, scales and grammatical gender

    Parameters:
        number (int or float): The number to pronounce.
        places (int): Number of decimal places to include for floats.
        scale (Scale): Numerical scale to use (short or long).
        ordinals (bool): If True, pronounce as an ordinal number.
        gender (GrammaticalGender): Grammatical gender for ordinal numbers.

    Returns:
        str: The number expressed as a Mirandese phrase.
    """
    if not isinstance(number, (int, float)):
        raise TypeError("Number must be an int or float.")

    if ordinals:
        return pronounce_ordinal_mwl(number, gender, scale)

    if number == 0:
        return "zero"

    if number < 0:
        return f"menos {pronounce_number_mwl(abs(number), places, scale=scale, digits=digits, gender=gender)}"

    # Handle decimals
    if "." in str(number):
        integer_part = int(number)
        decimal_part_str = f"{number:.{places}f}".split('.')[1].rstrip("0")

        # Handle cases where the decimal part rounds to zero
        if decimal_part_str and int(decimal_part_str) == 0:
            return pronounce_number_mwl(integer_part, places,
                                        scale=scale,
                                        digits=digits, gender=gender)

        int_pronunciation = pronounce_number_mwl(integer_part, places,
                                                 scale=scale,
                                                 digits=digits, gender=gender)

        decimal_pronunciation_parts = []
        #  pronounce decimals either as a whole number or digit by digit
        if decimal_part_str:
            if digits == DigitPronunciation.FULL_NUMBER:
                decimal_pronunciation_parts.append(_pronounce_up_to_999(int(decimal_part_str[:3]), gender))
            else:
                for digit in decimal_part_str:
                    decimal_pronunciation_parts.append(_pronounce_up_to_999(int(digit), gender))

        decimal_pronunciation = " ".join(decimal_pronunciation_parts) or "zero"
        decimal_word = "bírgula"
        return f"{int_pronunciation} {decimal_word} {decimal_pronunciation}"

    # --- Integer Pronunciation Logic ---
    n = int(number)

    # Base case for recursion: numbers less than 1000
    if n < 1000:
        return _pronounce_up_to_999(n, gender)

    scale_definitions = _SCALES[scale]

    # Find the largest scale that fits the number
    for scale_val, s_name, p_name in scale_definitions:
        if n >= scale_val:
            break

    count = n // scale_val
    remainder = n % scale_val

    # Pronounce the 'count' part of the number
    scale_word = s_name if count == 1 else p_name
    if count == 1 and scale_word == "mil":
        count_str = scale_word
    else:
        count_pronunciation = pronounce_number_mwl(count, places, scale)
        count_str = f"{count_pronunciation} {scale_word}"

    # If there's no remainder, we're done
    if remainder == 0:
        return count_str

    # Pronounce the remainder and join with the correct conjunction
    remainder_str = pronounce_number_mwl(remainder, places, scale)

    # Conjunction logic: add "i" if the remainder is the last group and is
    # less than 100 or a multiple of 100.
    if remainder < 100 or (remainder < 1000 and remainder % 100 == 0):
        return f"{count_str} e {remainder_str}"
    else:
        return f"{count_str} {remainder_str}"


def numbers_to_digits_mwl(
        utterance: str,
        scale: Scale = Scale.LONG
) -> str:
    """
    Converts written Mirandese numbers in a text string to their digit equivalents, preserving all other text.

    Identifies spans of number words (including the joiner "i"), extracts their numeric values, and replaces them with digit strings. Non-number words and context are left unchanged.

    Parameters:
        utterance (str): Input text possibly containing written Mirandese numbers.
        scale (Scale, optional): Numerical scale (short or long) to interpret large numbers. Defaults to Scale.LONG.

    Returns:
        str: The input text with written numbers replaced by their digit representations.
    """
    utterance = utterance.replace("bint'i", "binte i")
    for n, v in _HUNDREDS_ALT.items():
        # normalize alternative multi-word spelling to single word
        utterance = utterance.replace(v, _HUNDREDS[n])

    words = tokenize(utterance)
    output = []
    i = 0
    NUMBERS = get_number_map(scale)
    while i < len(words):
        # Look for the start of a number span
        if words[i] in NUMBERS:
            # Start a new span
            number_span_words = []
            j = i
            # Continue the span as long as we find number words or the joiner 'e'
            while j < len(words) and (words[j] in NUMBERS or words[j] == "i"):
                number_span_words.append(words[j])
                j += 1

            # Form the phrase from the span and extract the number value
            phrase = " ".join(number_span_words)
            number_val = extract_number_mwl(phrase)

            if number_val is not False:
                # If a valid number is found, add its digit representation to the output
                output.append(str(number_val))
                # Advance the main index 'i' past the entire span
                i = j
            else:
                # If the span doesn't form a valid number, treat the first word as non-numeric
                # and move to the next word. This handles cases like "i" at the beginning of a sentence.
                output.append(words[i])
                i += 1
        else:
            # If the current word is not a number word, add it to the output
            # and move to the next word
            output.append(words[i])
            i += 1

    return " ".join(output)


def pronounce_fraction_mwl(word: str, scale: Scale = Scale.LONG) -> str:
    """
    Return the Mirandese pronunciation of a fraction given as a string (e.g., "1/2").

    The numerator is pronounced as a cardinal number, and the denominator as an ordinal or fraction name, pluralized if appropriate. For denominators not in the known fraction list, the denominator is pronounced as a cardinal number followed by "abos" if plural.

    Parameters:
        word (str): Fraction in the form "numerator/denominator" (e.g., "3/4").

    Returns:
        str: The Mirandese pronunciation of the fraction.
    """
    word = word.replace("bint'i", "binte i")
    n1, n2 = word.split("/")
    n1_int, n2_int = int(n1), int(n2)

    # Pronounce the denominator (second number) as an ordinal, and pluralize it if needed.
    if n2_int in _FRACTION_STRING_MWL:
        denom = _FRACTION_STRING_MWL[n2_int]
        if n1_int != 1:
            denom += "s"  # plural
    else:
        # For other numbers
        denom = pronounce_number_mwl(n2_int, scale=scale)
        if n1_int > 1:  # plural
            denom += " abos"

    # Pronounce the numerator (first number) as a cardinal.
    num = pronounce_number_mwl(n1_int, scale=scale)
    return f"{num} {denom}"


if __name__ == "__main__":
    print("--- Testing Pronunciation (Short Scale) ---")
    print(f"1,234,567: {pronounce_number_mwl(1_234_567, scale=Scale.SHORT)}")
    print(f"1,000,000,000: {pronounce_number_mwl(1_000_000_000, scale=Scale.SHORT)}")

    print("\n--- Testing Pronunciation (Long Scale) ---")
    print(f"1,000,000: {pronounce_number_mwl(1_000_000, scale=Scale.LONG)}")
    print(f"1,000,100: {pronounce_number_mwl(1_000_100, scale=Scale.LONG)}")
    print(f"1,000,000,000: {pronounce_number_mwl(1_000_000_000, scale=Scale.LONG)}")
    print(f"1,000,000,000,000: {pronounce_number_mwl(1_000_000_000_000, scale=Scale.LONG)}")
    print(f"2,500,000,000: {pronounce_number_mwl(2_500_000_000, scale=Scale.LONG)}")
    print(f"2,500,123,456: {pronounce_number_mwl(2_500_123_456, scale=Scale.LONG)}")
    print(f"16: {pronounce_number_mwl(16)}")

    print("\n--- Testing Edge Cases ---")
    print(f"-123.45: {pronounce_number_mwl(-123.45)}")
    print(f"10.05: {pronounce_number_mwl(10.05)}")
    print(f"2000: {pronounce_number_mwl(2000)}")
    print(f"2001: {pronounce_number_mwl(2001)}")
    print(f"123.456789: {pronounce_number_mwl(123.456789)}")

    print("\n--- Testing Ordinal Pronunciation ---")
    print(f"1st (masculine): {pronounce_number_mwl(1, ordinals=True, gender=GrammaticalGender.MASCULINE)}")
    print(f"1st (feminine): {pronounce_number_mwl(1, ordinals=True, gender=GrammaticalGender.FEMININE)}")
    print(f"23rd (masculine): {pronounce_number_mwl(23, ordinals=True)}")
    print(f"23rd (feminine): {pronounce_number_mwl(23, ordinals=True, gender=GrammaticalGender.FEMININE)}")
    print(f"100th: {pronounce_number_mwl(100, ordinals=True)}")
    print(f"101st: {pronounce_number_mwl(101, ordinals=True)}")
    print(f"1000th: {pronounce_number_mwl(1000, ordinals=True)}")
    print(f"1,000,000th: {pronounce_number_mwl(1_000_000, ordinals=True)}")
    print(f"1,000,000,000,000th (long): {pronounce_number_mwl(1_000_000_000_000, ordinals=True, scale=Scale.LONG)}")

    print("\n--- Testing numbers_to_digits_mwl ---")
    print(f"'duzientos i cinquenta' -> '{numbers_to_digits_mwl('duzientos i cinquenta')}'")
    print(f"'un milhon' -> '{numbers_to_digits_mwl('un milhon')}'")
    print(f"'zasseis' -> '{numbers_to_digits_mwl('zasseis')}'")
    print(f"'hai duzientos i cinquenta carros' -> '{numbers_to_digits_mwl('hai duzientos i cinquenta carros')}'")

    print("\n--- Testing Ordinal Extraction ---")
    print(f"'l segundo carro' -> {extract_number_mwl('l segundo carro', ordinals=True)}")
    print(f"'purmerio lugar' -> {extract_number_mwl('purmerio lugar', ordinals=True)}")
    print(f"'l milésimo die' -> {extract_number_mwl('l milésimo dia', ordinals=True)}")
    print(f"'la milésima beç' -> {extract_number_mwl('la milésima beç', ordinals=True)}")
    print(f"'la purmeria beç' -> {extract_number_mwl('la purmeria beç', ordinals=True)}")
    print(f"'la sessagésima quarta beç' -> {extract_number_mwl('la sessagésima quarta beç', ordinals=True)}")

    print("\n--- Testing Cardinal Extraction ---")
    print(f"'un' -> {extract_number_mwl('un')}")
    print(f"'ũa' -> {extract_number_mwl('ũa')}")
    print(f"'bint'i un' ->", extract_number_mwl("bint'i un"))
    print(f"'bint'i ũa' ->", extract_number_mwl("bint'i ũa"))
    print(f"'bint'i dous' ->", extract_number_mwl("bint'i dous"))
    print(f"'bint'i dues' ->", extract_number_mwl("bint'i dues"))
    print(f"'un milhon' -> {extract_number_mwl('un milhon')}")
    print(f"'dous milhones e quinhentos' -> {extract_number_mwl('dous milhones i quinhentos')}")
    print(f"'mil i binte i trés' -> {extract_number_mwl('mil i binte i trés')}")
    print(f"'trinta i cinco bírgula quatro' -> {extract_number_mwl('trinta i cinco bírgula quatro')}")

    print("\n--- Testing Fractions ---")
    print(f"1/2: {pronounce_fraction_mwl('1/2')}")
    print(f"2/2: {pronounce_fraction_mwl('2/2')}")
    print(f"5/2: {pronounce_fraction_mwl('5/2')}")
    print(f"5/3: {pronounce_fraction_mwl('5/3')}")
    print(f"5/4: {pronounce_fraction_mwl('5/4')}")
    print(f"7/5: {pronounce_fraction_mwl('7/5')}")
    print(f"0/20: {pronounce_fraction_mwl('0/20')}")

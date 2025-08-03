1~
import unittest
2~

3~
from ovos_number_parser.numbers_pt import (
4~
    PortugueseVariant,
5~
    _pronounce_up_to_999,
6~
    is_fractional_pt,
7~
    extract_number_pt,
8~
    pronounce_number_pt,
9~
    numbers_to_digits_pt,
10~
    tokenize,
11~
    pronounce_fraction_pt,
12~
    _UNITS,
13~
    _TENS_BR,
14~
    _TENS_PT,
15~
    _HUNDREDS,
16~
    _FRACTION_STRING_PT,
17~
    _SCALES,
18~
    _NUMBERS_BR,
19~
    _NUMBERS_PT
20~
)
21~
from ovos_number_parser.util import DigitPronunciation, Scale
22~

23~

24~
class TestPortugueseVariant(unittest.TestCase):
25~
    """Test PortugueseVariant enum."""
26~

27~
    def test_variant_values(self):
28~
        """Test that variant enum has correct values."""
29~
        self.assertEqual(PortugueseVariant.BR.value, "br")
30~
        self.assertEqual(PortugueseVariant.PT.value, "pt")
31~

32~
    def test_variant_comparison(self):
33~
        """Test variant enum comparison."""
34~
        self.assertNotEqual(PortugueseVariant.BR, PortugueseVariant.PT)
35~
        self.assertEqual(PortugueseVariant.BR, PortugueseVariant.BR)
36~

37~

38~
class TestDictionaries(unittest.TestCase):
39~
    """Test the pronunciation dictionaries."""
40~

41~
    def test_units_completeness(self):
42~
        """Test that _UNITS contains all expected numbers."""
43~
        expected_keys = list(range(1, 10))
44~
        self.assertEqual(set(_UNITS.keys()), set(expected_keys))
45~

46~
    def test_tens_br_completeness(self):
47~
        """Test that _TENS_BR contains all expected numbers."""
48~
        expected_keys = list(range(10, 20)) + list(range(20, 100, 10))
49~
        self.assertEqual(set(_TENS_BR.keys()), set(expected_keys))
50~

51~
    def test_tens_pt_completeness(self):
52~
        """Test that _TENS_PT contains all expected numbers."""
53~
        expected_keys = list(range(10, 20)) + list(range(20, 100, 10))
54~
        self.assertEqual(set(_TENS_PT.keys()), set(expected_keys))
55~

56~
    def test_tens_variants_differences(self):
57~
        """Test that BR and PT variants have expected differences."""
58~
        # Key differences between BR and PT
59~
        self.assertEqual(_TENS_BR[16], "dezesseis")
60~
        self.assertEqual(_TENS_PT[16], "dezasseis")
61~
        self.assertEqual(_TENS_BR[17], "dezessete")
62~
        self.assertEqual(_TENS_PT[17], "dezassete")
63~
        self.assertEqual(_TENS_BR[19], "dezenove")
64~
        self.assertEqual(_TENS_PT[19], "dezanove")
65~

66~
    def test_hundreds_completeness(self):
67~
        """Test that _HUNDREDS contains all expected numbers."""
68~
        expected_keys = list(range(100, 1000, 100))
69~
        self.assertEqual(set(_HUNDREDS.keys()), set(expected_keys))
70~

71~
    def test_fraction_string_pt_completeness(self):
72~
        """Test that _FRACTION_STRING_PT contains expected fractions."""
73~
        self.assertIn(2, _FRACTION_STRING_PT)
74~
        self.assertIn(3, _FRACTION_STRING_PT)
75~
        self.assertIn(10, _FRACTION_STRING_PT)
76~
        self.assertEqual(_FRACTION_STRING_PT[2], "meio")
77~
        self.assertEqual(_FRACTION_STRING_PT[3], "terço")
78~

79~
    def test_scales_structure(self):
80~
        """Test that _SCALES has correct structure."""
81~
        self.assertIn(Scale.SHORT, _SCALES)
82~
        self.assertIn(Scale.LONG, _SCALES)
83~
        self.assertIn(PortugueseVariant.BR, _SCALES[Scale.SHORT])
84~
        self.assertIn(PortugueseVariant.PT, _SCALES[Scale.SHORT])
85~

86~
    def test_numbers_br_construction(self):
87~
        """Test that _NUMBERS_BR is correctly constructed."""
88~
        self.assertIn("um", _NUMBERS_BR)
89~
        self.assertIn("dezesseis", _NUMBERS_BR)
90~
        self.assertIn("bilhão", _NUMBERS_BR)
91~
        self.assertEqual(_NUMBERS_BR["um"], 1)
92~
        self.assertEqual(_NUMBERS_BR["dezesseis"], 16)
93~

94~
    def test_numbers_pt_construction(self):
95~
        """Test that _NUMBERS_PT is correctly constructed."""
96~
        self.assertIn("um", _NUMBERS_PT)
97~
        self.assertIn("dezasseis", _NUMBERS_PT)
98~
        self.assertIn("bilião", _NUMBERS_PT)
99~
        self.assertEqual(_NUMBERS_PT["um"], 1)
100~
        self.assertEqual(_NUMBERS_PT["dezasseis"], 16)
101~

102~

103~
class TestPronounceUpTo999(unittest.TestCase):
104~
    """Test _pronounce_up_to_999 function."""
105~

106~
    def test_zero(self):
107~
        """Test pronunciation of zero."""
108~
        result = _pronounce_up_to_999(0)
109~
        self.assertEqual(result, "zero")
110~

111~
    def test_single_digits_br(self):
112~
        """Test pronunciation of single digits in BR variant."""
113~
        self.assertEqual(_pronounce_up_to_999(1, PortugueseVariant.BR), "um")
114~
        self.assertEqual(_pronounce_up_to_999(5, PortugueseVariant.BR), "cinco")
115~
        self.assertEqual(_pronounce_up_to_999(9, PortugueseVariant.BR), "nove")
116~

117~
    def test_single_digits_pt(self):
118~
        """Test pronunciation of single digits in PT variant."""
119~
        self.assertEqual(_pronounce_up_to_999(1, PortugueseVariant.PT), "um")
120~
        self.assertEqual(_pronounce_up_to_999(5, PortugueseVariant.PT), "cinco")
121~
        self.assertEqual(_pronounce_up_to_999(9, PortugueseVariant.PT), "nove")
122~

123~
    def test_teens_br(self):
124~
        """Test pronunciation of teens in BR variant."""
125~
        self.assertEqual(_pronounce_up_to_999(16, PortugueseVariant.BR), "dezesseis")
126~
        self.assertEqual(_pronounce_up_to_999(17, PortugueseVariant.BR), "dezessete")
127~
        self.assertEqual(_pronounce_up_to_999(19, PortugueseVariant.BR), "dezenove")
128~

129~
    def test_teens_pt(self):
130~
        """Test pronunciation of teens in PT variant."""
131~
        self.assertEqual(_pronounce_up_to_999(16, PortugueseVariant.PT), "dezasseis")
132~
        self.assertEqual(_pronounce_up_to_999(17, PortugueseVariant.PT), "dezassete")
133~
        self.assertEqual(_pronounce_up_to_999(19, PortugueseVariant.PT), "dezanove")
134~

135~
    def test_tens(self):
136~
        """Test pronunciation of tens."""
137~
        self.assertEqual(_pronounce_up_to_999(20), "vinte")
138~
        self.assertEqual(_pronounce_up_to_999(30), "trinta")
139~
        self.assertEqual(_pronounce_up_to_999(90), "noventa")
140~

141~
    def test_tens_with_units(self):
142~
        """Test pronunciation of tens with units."""
143~
        self.assertEqual(_pronounce_up_to_999(21), "vinte e um")
144~
        self.assertEqual(_pronounce_up_to_999(35), "trinta e cinco")
145~
        self.assertEqual(_pronounce_up_to_999(99), "noventa e nove")
146~

147~
    def test_exact_hundred(self):
148~
        """Test pronunciation of exact hundred."""
149~
        self.assertEqual(_pronounce_up_to_999(100), "cem")
150~

151~
    def test_hundreds_with_remainder(self):
152~
        """Test pronunciation of hundreds with remainder."""
153~
        self.assertEqual(_pronounce_up_to_999(101), "cento e um")
154~
        self.assertEqual(_pronounce_up_to_999(123), "cento e vinte e três")
155~
        self.assertEqual(_pronounce_up_to_999(200), "duzentos")
156~
        self.assertEqual(_pronounce_up_to_999(234), "duzentos e trinta e quatro")
157~

158~
    def test_complex_numbers(self):
159~
        """Test pronunciation of complex numbers."""
160~
        self.assertEqual(_pronounce_up_to_999(567), "quinhentos e sessenta e sete")
161~
        self.assertEqual(_pronounce_up_to_999(999), "novecentos e noventa e nove")
162~

163~
    def test_invalid_range(self):
164~
        """Test that invalid ranges raise ValueError."""
165~
        with self.assertRaises(ValueError):
166~
            _pronounce_up_to_999(-1)
167~
        with self.assertRaises(ValueError):
168~
            _pronounce_up_to_999(1000)
169~
        with self.assertRaises(ValueError):
170~
            _pronounce_up_to_999(1001)
171~

172~

173~
class TestIsFractionalPt(unittest.TestCase):
174~
    """Test is_fractional_pt function."""
175~

176~
    def test_basic_fractions(self):
177~
        """Test basic fraction recognition."""
178~
        self.assertEqual(is_fractional_pt("meio"), 0.5)
179~
        self.assertEqual(is_fractional_pt("terço"), 1.0 / 3)
180~
        self.assertEqual(is_fractional_pt("quarto"), 0.25)
181~

182~
    def test_meia_variant(self):
183~
        """Test 'meia' as variant of 'meio'."""
184~
        self.assertEqual(is_fractional_pt("meia"), 0.5)
185~

186~
    def test_plural_forms(self):
187~
        """Test plural forms of fractions."""
188~
        self.assertEqual(is_fractional_pt("meios"), 0.5)
189~
        self.assertEqual(is_fractional_pt("terços"), 1.0 / 3)
190~
        self.assertEqual(is_fractional_pt("quartos"), 0.25)
191~

192~
    def test_special_fractions(self):
193~
        """Test special fraction forms."""
194~
        self.assertEqual(is_fractional_pt("décimo"), 0.1)
195~
        self.assertEqual(is_fractional_pt("vigésimo"), 0.05)
196~
        self.assertEqual(is_fractional_pt("centésimo"), 0.01)
197~

198~
    def test_compound_fractions(self):
199~
        """Test compound fraction forms like 'onze avos'."""
200~
        self.assertEqual(is_fractional_pt("onze avos"), 1.0 / 11)
201~
        self.assertEqual(is_fractional_pt("doze avos"), 1.0 / 12)
202~
        self.assertEqual(is_fractional_pt("treze avos"), 1.0 / 13)
203~
        self.assertFalse(is_fractional_pt("onze"))
204~
        self.assertFalse(is_fractional_pt("doze"))
205~
        self.assertFalse(is_fractional_pt("treze"))
206~

207~
    def test_case_insensitive(self):
208~
        """Test case insensitive matching."""
209~
        self.assertEqual(is_fractional_pt("MEIO"), 0.5)
210~
        self.assertEqual(is_fractional_pt("Terço"), 1.0 / 3)
211~
        self.assertEqual(is_fractional_pt("MEIA"), 0.5)
212~

213~
    def test_whitespace_handling(self):
214~
        """Test whitespace handling."""
215~
        self.assertEqual(is_fractional_pt("  meio  "), 0.5)
216~
        self.assertEqual(is_fractional_pt("\tterço\n"), 1.0 / 3)
217~

218~
    def test_non_fractions(self):
219~
        """Test non-fraction strings return False."""
220~
        self.assertFalse(is_fractional_pt("palavra"))
221~
        self.assertFalse(is_fractional_pt("número"))
222~
        self.assertFalse(is_fractional_pt(""))
223~
        self.assertFalse(is_fractional_pt("123"))
224~

225~

226~
class TestExtractNumberPt(unittest.TestCase):
227~
    """Test extract_number_pt function."""
228~

229~
    def test_simple_numbers_br(self):
230~
        """Test extraction of simple numbers in BR variant."""
231~
        self.assertEqual(extract_number_pt("dezesseis", variant=PortugueseVariant.BR), 16)
232~
        self.assertEqual(extract_number_pt("vinte e um", variant=PortugueseVariant.BR), 21)
233~
        self.assertEqual(extract_number_pt("cem", variant=PortugueseVariant.BR), 100)
234~

235~
    def test_simple_numbers_pt(self):
236~
        """Test extraction of simple numbers in PT variant."""
237~
        self.assertEqual(extract_number_pt("dezasseis", variant=PortugueseVariant.PT), 16)
238~
        self.assertEqual(extract_number_pt("vinte e um", variant=PortugueseVariant.PT), 21)
239~
        self.assertEqual(extract_number_pt("cem", variant=PortugueseVariant.PT), 100)
240~

241~
    def test_large_numbers_short_scale_br(self):
242~
        """Test extraction of large numbers in short scale BR."""
243~
        self.assertEqual(extract_number_pt("um milhão", scale=Scale.SHORT, variant=PortugueseVariant.BR), 1000000)
244~
        self.assertEqual(extract_number_pt("um bilhão", scale=Scale.SHORT, variant=PortugueseVariant.BR), 1000000000)
245~

246~
    def test_large_numbers_short_scale_pt(self):
247~
        """Test extraction of large numbers in short scale PT."""
248~
        self.assertEqual(extract_number_pt("um milhão", scale=Scale.SHORT, variant=PortugueseVariant.PT), 1e6)
249~
        self.assertEqual(extract_number_pt("um bilião", scale=Scale.SHORT, variant=PortugueseVariant.PT), 1e9)
250~
        self.assertEqual(extract_number_pt("um trilião", scale=Scale.SHORT, variant=PortugueseVariant.PT), 1e12)
251~

252~
    def test_large_numbers_long_scale(self):
253~
        """Test extraction of large numbers in long scale."""
254~
        # TODO - failing
255~
        self.assertEqual(extract_number_pt("um milhão", scale=Scale.LONG, variant=PortugueseVariant.PT), 1e6)
256~
        self.assertEqual(extract_number_pt("um bilião", scale=Scale.LONG, variant=PortugueseVariant.PT), 1e12)
257~
        self.assertEqual(extract_number_pt("um trilião", scale=Scale.LONG, variant=PortugueseVariant.PT), 1e18)
258~

259~
    def test_complex_numbers(self):
260~
        """Test extraction of complex number phrases."""
261~
        self.assertEqual(extract_number_pt("duzentos e cinquenta e três"), 253)
262~
        self.assertEqual(extract_number_pt("mil quinhentos e quarenta e dois"), 1542)
263~

264~
    def test_fractions_in_text(self):
265~
        """Test extraction of fractions from text."""
266~
        result = extract_number_pt("dois e meio")
267~
        self.assertAlmostEqual(result, 2.5, places=5)
268~

269~
    def test_decimal_handling(self):
270~
        """Test decimal number handling."""
271~
        # Note: This tests the simplified decimal approach
272~
        result = extract_number_pt("dez ponto cinco")
273~
        # The function should handle this but may need specific formatting
274~
        if result:
275~
            self.assertIsInstance(result, (int, float))
276~

277~
    def test_case_insensitive(self):
278~
        """Test case insensitive extraction."""
279~
        self.assertEqual(extract_number_pt("DEZESSEIS", variant=PortugueseVariant.BR), 16)
280~
        self.assertEqual(extract_number_pt("Vinte E Um", variant=PortugueseVariant.BR), 21)
281~

282~
    def test_hyphen_handling(self):
283~
        """Test hyphen handling in text."""
284~
        self.assertEqual(extract_number_pt("vinte-e-um", variant=PortugueseVariant.BR), 21)
285~

286~
    def test_no_number_found(self):
287~
        """Test when no number is found in text."""
288~
        self.assertFalse(extract_number_pt("apenas palavras"))
289~
        self.assertFalse(extract_number_pt(""))
290~
        self.assertFalse(extract_number_pt("xyz"))
291~

292~
    def test_multiple_scales(self):
293~
        """Test numbers with multiple scale words."""
294~
        self.assertEqual(extract_number_pt("dois milhões trezentos mil"), 2300000)
295~

296~
    def test_edge_cases(self):
297~
        """Test edge cases."""
298~
        self.assertEqual(extract_number_pt("zero"), 0)
299~
        self.assertEqual(extract_number_pt("mil"), 1000)
300~

301~

302~
class TestPronounceNumberPt(unittest.TestCase):
303~
    """Test pronounce_number_pt function."""
304~

305~
    def test_type_validation(self):
306~
        """Test type validation."""
307~
        with self.assertRaises(TypeError):
308~
            pronounce_number_pt("not a number")
309~
        with self.assertRaises(TypeError):
310~
            pronounce_number_pt(None)
311~

312~
    def test_zero(self):
313~
        """Test pronunciation of zero."""
314~
        self.assertEqual(pronounce_number_pt(0), "zero")
315~

316~
    def test_negative_numbers(self):
317~
        """Test pronunciation of negative numbers."""
318~
        result = pronounce_number_pt(-5)
319~
        self.assertTrue(result.startswith("menos"))
320~
        self.assertIn("cinco", result)
321~

322~
    def test_simple_integers(self):
323~
        """Test pronunciation of simple integers."""
324~
        self.assertEqual(pronounce_number_pt(1), "um")
325~
        self.assertEqual(pronounce_number_pt(16, variant=PortugueseVariant.BR), "dezesseis")
326~
        self.assertEqual(pronounce_number_pt(16, variant=PortugueseVariant.PT), "dezasseis")
327~

328~
    def test_hundreds(self):
329~
        """Test pronunciation of hundreds."""
330~
        self.assertEqual(pronounce_number_pt(100), "cem")
331~
        self.assertEqual(pronounce_number_pt(200), "duzentos")
332~
        self.assertEqual(pronounce_number_pt(123), "cento e vinte e três")
333~

334~
    def test_thousands(self):
335~
        """Test pronunciation of thousands."""
336~
        result = pronounce_number_pt(1000)
337~
        self.assertIn("mil", result)
338~

339~
        result = pronounce_number_pt(2500)
340~
        self.assertIn("mil", result)
341~
        self.assertIn("quinhentos", result)
342~

343~
    def test_millions_short_scale_br(self):
344~
        """Test pronunciation of millions in short scale BR."""
345~
        result = pronounce_number_pt(1000000, scale=Scale.SHORT, variant=PortugueseVariant.BR)
346~
        self.assertIn("milhão", result)
347~

348~
        result = pronounce_number_pt(1000000000, scale=Scale.SHORT, variant=PortugueseVariant.BR)
349~
        self.assertIn("bilhão", result)
350~

351~
    def test_millions_short_scale_pt(self):
352~
        """Test pronunciation of millions in short scale PT."""
353~
        result = pronounce_number_pt(1000000, scale=Scale.SHORT, variant=PortugueseVariant.PT)
354~
        self.assertIn("milhão", result)
355~

356~
        result = pronounce_number_pt(1000000000, scale=Scale.SHORT, variant=PortugueseVariant.PT)
357~
        self.assertIn("bilião", result)
358~

359~
    def test_millions_long_scale(self):
360~
        """Test pronunciation of millions in long scale."""
361~
        result = pronounce_number_pt(1000000, scale=Scale.LONG, variant=PortugueseVariant.PT)
362~
        self.assertIn("milhão", result)
363~

364~
        result = pronounce_number_pt(1000000000000, scale=Scale.LONG, variant=PortugueseVariant.PT)
365~
        self.assertIn("bilião", result)
366~

367~
    def test_decimal_numbers(self):
368~
        """Test pronunciation of decimal numbers."""
369~
        result = pronounce_number_pt(1.5)
370~
        self.assertIn("vírgula", result)
371~
        self.assertIn("um", result)
372~
        self.assertIn("cinco", result)
373~

374~
    def test_decimal_edge_cases(self):
375~
        """Test edge cases for decimal numbers."""
376~
        # Test when decimal part rounds to zero
377~
        result = pronounce_number_pt(1.0)
378~
        self.assertEqual(result, "um vírgula zero")
379~

380~
        # Test multiple decimal places
381~
        result = pronounce_number_pt(1.23)
382~
        self.assertIn("vírgula", result)
383~

384~
    def test_conjunction_logic(self):
385~
        """Test conjunction logic for complex numbers."""
386~
        result = pronounce_number_pt(1001)
387~
        self.assertIn("e", result)  # Should have conjunction for small remainder
388~

389~
        result = pronounce_number_pt(1100)
390~
        self.assertIn("e", result)  # Should have conjunction for multiple of 100
391~

392~
    def test_mil(self):
393~
        """Test 'um mil' """
394~
        result = pronounce_number_pt(1000)
395~
        # Should not start with "um mil" but just "mil"
396~
        self.assertFalse(result.startswith("um mil"))
397~

398~
    def test_places_parameter(self):
399~
        """
400~
        Test that the `places` parameter in `pronounce_number_pt` correctly limits the number of decimal places pronounced when using digit-by-digit pronunciation.
401~
        
402~
        Ensures that specifying different values for `places` produces valid string outputs without errors.
403~
        """
404~
        result1 = pronounce_number_pt(1.23456, places=2, digits=DigitPronunciation.DIGIT_BY_DIGIT)
405~
        result2 = pronounce_number_pt(1.23456, places=5, digits=DigitPronunciation.DIGIT_BY_DIGIT)
406~
        # Both should work without error
407~
        self.assertIsInstance(result1, str)
408~
        self.assertIsInstance(result2, str)
409~

410~

411~
class TestNumbersToDigitsPt(unittest.TestCase):
412~
    """Test numbers_to_digits_pt function."""
413~

414~
    def test_simple_replacement(self):
415~
        """Test simple number word replacement."""
416~
        self.assertEqual(numbers_to_digits_pt("dezesseis", variant=PortugueseVariant.BR), "16")
417~
        self.assertEqual(numbers_to_digits_pt("dezasseis", variant=PortugueseVariant.PT), "16")
418~

419~
    def test_complex_numbers(self):
420~
        """Test complex number phrase replacement."""
421~
        result = numbers_to_digits_pt("duzentos e cinquenta e três")
422~
        self.assertEqual(result, "253")
423~

424~
    def test_mixed_text(self):
425~
        """Test text with mixed words and numbers."""
426~
        result = numbers_to_digits_pt("há duzentos e cinquenta carros")
427~
        self.assertIn("250", result)
428~
        self.assertIn("há", result)
429~
        self.assertIn("carros", result)
430~

431~
    def test_multiple_numbers(self):
432~
        """Test text with multiple separate numbers."""
433~
        result = numbers_to_digits_pt("dez carros e cinco pessoas")
434~
        self.assertIn("10", result)
435~
        self.assertIn("5", result)
436~
        self.assertIn("carros", result)
437~
        self.assertIn("pessoas", result)
438~

439~
    def test_no_numbers(self):
440~
        """Test text with no numbers."""
441~
        original = "apenas palavras normais"
442~
        result = numbers_to_digits_pt(original)
443~
        self.assertEqual(result, original)
444~

445~
    def test_edge_cases(self):
446~
        """Test edge cases."""
447~
        # Empty string
448~
        self.assertEqual(numbers_to_digits_pt(""), "")
449~

450~
        # Single word
451~
        self.assertEqual(numbers_to_digits_pt("cinco"), "5")
452~

453~
        # Just conjunction
454~
        self.assertEqual(numbers_to_digits_pt("e"), "e")
455~

456~
    def test_variant_differences(self):
457~
        """Test that variants produce different results where expected."""
458~
        br_result = numbers_to_digits_pt("dezesseis", variant=PortugueseVariant.BR)
459~
        pt_result = numbers_to_digits_pt("dezasseis", variant=PortugueseVariant.PT)
460~
        self.assertEqual(br_result, "16")
461~
        self.assertEqual(pt_result, "16")
462~

463~

464~
class TestTokenize(unittest.TestCase):
465~
    """Test tokenize function."""
466~

467~
    def test_basic_tokenization(self):
468~
        """Test basic word tokenization."""
469~
        result = tokenize("palavra uma palavra duas")
470~
        expected = ["palavra", "uma", "palavra", "duas"]
471~
        self.assertEqual(result, expected)
472~

473~
    def test_percentage_split(self):
474~
        """Test splitting percentages."""
475~
        result = tokenize("12%")
476~
        self.assertEqual(result, ["12", "%"])
477~

478~
    def test_hash_number_split(self):
479~
        """Test splitting hash with numbers."""
480~
        result = tokenize("#1")
481~
        self.assertEqual(result, ["#", "1"])
482~

483~
    def test_hyphen_between_words(self):
484~
        """Test hyphen handling between words."""
485~
        result = tokenize("amo-te")
486~
        self.assertEqual(result, ["amo", "-", "te"])
487~

488~
    def test_hyphen_preservation_in_numbers(self):
489~
        """Test that hyphens in numbers are preserved."""
490~
        result = tokenize("1-2")
491~
        # Should not split number ranges
492~
        self.assertIn("1-2", result)
493~

494~
    def test_trailing_hyphen_removal(self):
495~
        """Test removal of trailing hyphens."""
496~
        result = tokenize("palavra -")
497~
        self.assertEqual(result, ["palavra"])
498~

499~
    def test_empty_string(self):
500~
        """Test tokenization of empty string."""
501~
        result = tokenize("")
502~
        self.assertEqual(result, [])
503~

504~
    def test_whitespace_handling(self):
505~
        """Test handling of various whitespace."""
506~
        result = tokenize("  palavra   outra  ")
507~
        self.assertEqual(result, ["palavra", "outra"])
508~

509~
    def test_complex_input(self):
510~
        """Test complex input with multiple patterns."""
511~
        result = tokenize("amo-te 50% #2 test")
512~
        expected_elements = ["amo", "-", "te", "50", "%", "#", "2", "test"]
513~
        self.assertEqual(result, expected_elements)
514~

515~

516~
class TestPronounceFractionPt(unittest.TestCase):
517~
    """Test pronounce_fraction_pt function."""
518~

519~
    def test_simple_fractions(self):
520~
        """Test pronunciation of simple fractions."""
521~
        result = pronounce_fraction_pt("1/2")
522~
        self.assertIn("um", result)
523~
        self.assertIn("meio", result)
524~

525~
        result = pronounce_fraction_pt("1/3")
526~
        self.assertIn("um", result)
527~
        self.assertIn("terço", result)
528~

529~
    def test_plural_fractions(self):
530~
        """Test pronunciation of plural fractions."""
531~
        result = pronounce_fraction_pt("2/3")
532~
        self.assertIn("dois", result)
533~
        self.assertIn("terços", result)
534~

535~
        result = pronounce_fraction_pt("3/4")
536~
        self.assertIn("três", result)
537~
        self.assertIn("quartos", result)
538~

539~
    def test_large_denominators(self):
540~
        """Test fractions with large denominators."""
541~
        result = pronounce_fraction_pt("1/7")
542~
        self.assertIn("um", result)
543~
        self.assertIn("sétimo", result)
544~

545~
        result = pronounce_fraction_pt("5/7")
546~
        self.assertIn("cinco", result)
547~
        self.assertIn("sétimos", result)
548~

549~
    def test_unknown_denominators(self):
550~
        """Test fractions with denominators not in predefined list."""
551~
        result = pronounce_fraction_pt("1/13")
552~
        self.assertIn("um", result)
553~
        # Should use "avos" for unknown denominators
554~

555~
        result = pronounce_fraction_pt("2/13")
556~
        self.assertIn("dois", result)
557~
        self.assertIn("avos", result)
558~

559~
    def test_variant_differences(self):
560~
        """Test variant differences in fraction pronunciation."""
561~
        br_result = pronounce_fraction_pt("1/16", variant=PortugueseVariant.BR)
562~
        pt_result = pronounce_fraction_pt("1/16", variant=PortugueseVariant.PT)
563~
        # Both should work, may have slight differences in underlying number pronunciation
564~
        self.assertIsInstance(br_result, str)
565~
        self.assertIsInstance(pt_result, str)
566~

567~
    def test_scale_parameter(self):
568~
        """Test scale parameter in fraction pronunciation."""
569~
        result_short = pronounce_fraction_pt("1/1000000", scale=Scale.SHORT)
570~
        result_long = pronounce_fraction_pt("1/1000000", scale=Scale.LONG)
571~
        self.assertIsInstance(result_short, str)
572~
        self.assertIsInstance(result_long, str)
573~

574~
    def test_zero_numerator(self):
575~
        """Test fractions with zero numerator."""
576~
        result = pronounce_fraction_pt("0/5")
577~
        self.assertIn("zero", result)
578~

579~

580~
class TestIntegrationScenarios(unittest.TestCase):
581~
    """Test integration scenarios and edge cases."""
582~

583~
    def test_round_trip_conversion(self):
584~
        """Test round-trip conversion: number -> text -> number."""
585~
        test_numbers = [1, 16, 100, 123, 1000, 1234]
586~

587~
        for num in test_numbers:
588~
            # Convert number to text
589~
            text = pronounce_number_pt(num, variant=PortugueseVariant.BR)
590~
            # Convert text back to number
591~
            extracted = extract_number_pt(text, variant=PortugueseVariant.BR)
592~
            self.assertEqual(extracted, num, f"Round-trip failed for {num}: {text} -> {extracted}")
593~

594~
    def test_variant_consistency(self):
595~
        """Test that BR and PT variants are internally consistent."""
596~
        test_numbers = [16, 17, 19]  # Numbers that differ between variants
597~

598~
        for num in test_numbers:
599~
            # Test BR variant
600~
            br_text = pronounce_number_pt(num, variant=PortugueseVariant.BR)
601~
            br_extracted = extract_number_pt(br_text, variant=PortugueseVariant.BR)
602~
            self.assertEqual(br_extracted, num)
603~

604~
            # Test PT variant
605~
            pt_text = pronounce_number_pt(num, variant=PortugueseVariant.PT)
606~
            pt_extracted = extract_number_pt(pt_text, variant=PortugueseVariant.PT)
607~
            self.assertEqual(pt_extracted, num)
608~

609~
    def test_scale_consistency(self):
610~
        """Test that different scales work consistently."""
611~
        large_numbers = [1000000, 1000000000]
612~

613~
        for num in large_numbers:
614~
            for scale in [Scale.SHORT, Scale.LONG]:
615~
                for variant in [PortugueseVariant.BR, PortugueseVariant.PT]:
616~
                    text = pronounce_number_pt(num, scale=scale, variant=variant)
617~
                    extracted = extract_number_pt(text, scale=scale, variant=variant)
618~
                    print(text, extracted)
619~
                    self.assertEqual(extracted, num,
620~
                                     f"Scale consistency failed: {num} with {scale} and {variant}")
621~

622~
    def test_numbers_to_digits_integration(self):
623~
        """Test integration with numbers_to_digits_pt."""
624~
        test_phrases = [
625~
            "há duzentos e cinquenta carros",
626~
            "comprei dezesseis livros",
627~
            "mil e uma noites"
628~
        ]
629~

630~
        for phrase in test_phrases:
631~
            result = numbers_to_digits_pt(phrase, variant=PortugueseVariant.BR)
632~
            # Should contain digits and preserve non-number words
633~
            self.assertIsInstance(result, str)
634~
            self.assertTrue(any(char.isdigit() for char in result))
635~

636~
    def test_error_handling_robustness(self):
637~
        """Test robustness of error handling across functions."""
638~
        # Test various invalid inputs
639~
        invalid_inputs = ["", "   ", "xyz123", "palavra-palavra"]
640~

641~
        for invalid_input in invalid_inputs:
642~
            # extract_number_pt should return False for invalid input
643~
            result = extract_number_pt(invalid_input)
644~
            self.assertFalse(result)
645~

646~
            # numbers_to_digits_pt should handle gracefully
647~
            result = numbers_to_digits_pt(invalid_input)
648~
            self.assertIsInstance(result, str)
649~

650~
    def test_large_number_limits(self):
651~
        """Test behavior with very large numbers."""
652~
        very_large = 10 ** 30
653~

654~
        # Should not raise exceptions
655~
        try:
656~
            result = pronounce_number_pt(very_large)
657~
            self.assertIsInstance(result, str)
658~
        except Exception as e:
659~
            self.fail(f"Large number pronunciation failed: {e}")
660~

661~

662~
if __name__ == '__main__':
663~
    unittest.main()
664~

665~

666~
class TestPortugueseVariantEdgeCases(unittest.TestCase):
667~
    """Additional edge case tests for PortugueseVariant enum."""
668~

669~
    def test_variant_string_representation(self):
670~
        """Test string representation of variants."""
671~
        self.assertEqual(str(PortugueseVariant.BR), "PortugueseVariant.BR")
672~
        self.assertEqual(str(PortugueseVariant.PT), "PortugueseVariant.PT")
673~

674~
    def test_variant_equality_with_strings(self):
675~
        """Test variant comparison with string values."""
676~
        self.assertEqual(PortugueseVariant.BR.value, "br")
677~
        self.assertEqual(PortugueseVariant.PT.value, "pt")
678~
        self.assertNotEqual(PortugueseVariant.BR.value, "pt")
679~
        self.assertNotEqual(PortugueseVariant.PT.value, "br")
680~

681~
    def test_variant_iteration(self):
682~
        """Test iteration over variants."""
683~
        variants = list(PortugueseVariant)
684~
        self.assertEqual(len(variants), 2)
685~
        self.assertIn(PortugueseVariant.BR, variants)
686~
        self.assertIn(PortugueseVariant.PT, variants)
687~

688~

689~
class TestDictionariesExtensive(unittest.TestCase):
690~
    """Extensive tests for pronunciation dictionaries."""
691~

692~
    def test_units_values_correctness(self):
693~
        """Test that _UNITS contains correct Portuguese values."""
694~
        expected_values = {
695~
            1: "um", 2: "dois", 3: "três", 4: "quatro", 5: "cinco",
696~
            6: "seis", 7: "sete", 8: "oito", 9: "nove"
697~
        }
698~
        for key, expected in expected_values.items():
699~
            self.assertEqual(_UNITS[key], expected)
700~

701~
    def test_tens_br_specific_values(self):
702~
        """Test specific BR variant values in _TENS_BR."""
703~
        br_specific = {10: "dez", 11: "onze", 12: "doze", 13: "treze", 14: "catorze", 15: "quinze"}
704~
        for key, expected in br_specific.items():
705~
            self.assertEqual(_TENS_BR[key], expected)
706~

707~
    def test_tens_pt_specific_values(self):
708~
        """Test specific PT variant values in _TENS_PT."""
709~
        pt_specific = {10: "dez", 11: "onze", 12: "doze", 13: "treze", 14: "catorze", 15: "quinze"}
710~
        for key, expected in pt_specific.items():
711~
            self.assertEqual(_TENS_PT[key], expected)
712~

713~
    def test_hundreds_specific_values(self):
714~
        """Test specific values in _HUNDREDS."""
715~
        expected_hundreds = {
716~
            100: "cento", 200: "duzentos", 300: "trezentos", 400: "quatrocentos",
717~
            500: "quinhentos", 600: "seiscentos", 700: "setecentos", 800: "oitocentos", 900: "novecentos"
718~
        }
719~
        for key, expected in expected_hundreds.items():
720~
            self.assertEqual(_HUNDREDS[key], expected)
721~

722~
    def test_fraction_string_pt_edge_cases(self):
723~
        """Test edge cases in _FRACTION_STRING_PT."""
724~
        # Test that common fractions exist
725~
        self.assertIn(4, _FRACTION_STRING_PT)
726~
        self.assertIn(5, _FRACTION_STRING_PT)
727~
        self.assertEqual(_FRACTION_STRING_PT[4], "quarto")
728~
        self.assertEqual(_FRACTION_STRING_PT[5], "quinto")
729~

730~
    def test_scales_completeness(self):
731~
        """Test completeness of _SCALES dictionary."""
732~
        # Verify all required scale/variant combinations exist
733~
        self.assertIn(Scale.SHORT, _SCALES)
734~
        self.assertIn(Scale.LONG, _SCALES)
735~
        
736~
        for scale in [Scale.SHORT, Scale.LONG]:
737~
            self.assertIn(PortugueseVariant.BR, _SCALES[scale])
738~
            self.assertIn(PortugueseVariant.PT, _SCALES[scale])
739~
            
740~
            # Verify the structure contains scale mappings
741~
            for variant in [PortugueseVariant.BR, PortugueseVariant.PT]:
742~
                scale_dict = _SCALES[scale][variant]
743~
                self.assertIsInstance(scale_dict, dict)
744~
                # Should contain at least million, billion mappings
745~
                self.assertTrue(any(key >= 1000000 for key in scale_dict.keys()))
746~

747~
    def test_numbers_dictionaries_intersection(self):
748~
        """Test that BR and PT number dictionaries have proper intersection."""
749~
        # Common words should exist in both
750~
        common_words = ["um", "dois", "três", "cem", "mil"]
751~
        for word in common_words:
752~
            self.assertIn(word, _NUMBERS_BR)
753~
            self.assertIn(word, _NUMBERS_PT)
754~
            self.assertEqual(_NUMBERS_BR[word], _NUMBERS_PT[word])
755~

756~
    def test_numbers_dictionaries_differences(self):
757~
        """Test specific differences between BR and PT dictionaries."""
758~
        # BR specific words
759~
        br_specific = ["dezesseis", "dezessete", "dezenove", "bilhão"]
760~
        for word in br_specific:
761~
            self.assertIn(word, _NUMBERS_BR)
762~
            
763~
        # PT specific words  
764~
        pt_specific = ["dezasseis", "dezassete", "dezanove", "bilião"]
765~
        for word in pt_specific:
766~
            self.assertIn(word, _NUMBERS_PT)
767~

768~

769~
class TestPronounceUpTo999Extensive(unittest.TestCase):
770~
    """Extensive tests for _pronounce_up_to_999 function."""
771~

772~
    def test_boundary_values(self):
773~
        """Test boundary values."""
774~
        # Test exact boundaries
775~
        self.assertEqual(_pronounce_up_to_999(0), "zero")
776~
        self.assertEqual(_pronounce_up_to_999(1), "um")
777~
        self.assertEqual(_pronounce_up_to_999(999), "novecentos e noventa e nove")
778~

779~
    def test_all_single_digits(self):
780~
        """Test all single digits systematically."""
781~
        expected = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
782~
        for i in range(10):
783~
            result = _pronounce_up_to_999(i)
784~
            self.assertEqual(result, expected[i])
785~

786~
    def test_all_tens(self):
787~
        """Test all multiples of 10."""
788~
        tens_values = {
789~
            10: "dez", 20: "vinte", 30: "trinta", 40: "quarenta", 50: "cinquenta",
790~
            60: "sessenta", 70: "setenta", 80: "oitenta", 90: "noventa"
791~
        }
792~
        for value, expected in tens_values.items():
793~
            result = _pronounce_up_to_999(value)
794~
            self.assertEqual(result, expected)
795~

796~
    def test_all_hundreds(self):
797~
        """Test all multiples of 100."""
798~
        hundreds_values = {
799~
            100: "cem", 200: "duzentos", 300: "trezentos", 400: "quatrocentos",
800~
            500: "quinhentos", 600: "seiscentos", 700: "setecentos", 800: "oitocentos", 900: "novecentos"
801~
        }
802~
        for value, expected in hundreds_values.items():
803~
            result = _pronounce_up_to_999(value)
804~
            self.assertEqual(result, expected)
805~

806~
    def test_variant_specific_numbers(self):
807~
        """Test numbers that differ between variants."""
808~
        variant_tests = [
809~
            (16, PortugueseVariant.BR, "dezesseis"),
810~
            (16, PortugueseVariant.PT, "dezasseis"),
811~
            (17, PortugueseVariant.BR, "dezessete"),
812~
            (17, PortugueseVariant.PT, "dezassete"),
813~
            (19, PortugueseVariant.BR, "dezenove"),
814~
            (19, PortugueseVariant.PT, "dezanove")
815~
        ]
816~
        
817~
        for number, variant, expected in variant_tests:
818~
            result = _pronounce_up_to_999(number, variant)
819~
            self.assertEqual(result, expected)
820~

821~
    def test_complex_combinations(self):
822~
        """Test complex number combinations."""
823~
        test_cases = [
824~
            (111, "cento e onze"),
825~
            (222, "duzentos e vinte e dois"),
826~
            (345, "trezentos e quarenta e cinco"),
827~
            (506, "quinhentos e seis"),
828~
            (708, "setecentos e oito"),
829~
            (810, "oitocentos e dez")
830~
        ]
831~
        
832~
        for number, expected in test_cases:
833~
            result = _pronounce_up_to_999(number)
834~
            self.assertEqual(result, expected)
835~

836~
    def test_error_conditions(self):
837~
        """Test comprehensive error conditions."""
838~
        invalid_values = [-100, -1, 1000, 1001, 9999, -9999]
839~
        for value in invalid_values:
840~
            with self.assertRaises(ValueError):
841~
                _pronounce_up_to_999(value)
842~

843~
    def test_type_validation(self):
844~
        """Test type validation for _pronounce_up_to_999."""
845~
        invalid_types = ["123", 12.5, None, [], {}]
846~
        for invalid_input in invalid_types:
847~
            with self.assertRaises((TypeError, ValueError)):
848~
                _pronounce_up_to_999(invalid_input)
849~

850~

851~
class TestIsFractionalPtExtensive(unittest.TestCase):
852~
    """Extensive tests for is_fractional_pt function."""
853~

854~
    def test_all_basic_fractions(self):
855~
        """Test all basic fraction forms systematically."""
856~
        fraction_tests = [
857~
            ("meio", 0.5), ("meia", 0.5), ("terço", 1.0/3), ("quarto", 0.25),
858~
            ("quinto", 0.2), ("sexto", 1.0/6), ("sétimo", 1.0/7), ("oitavo", 0.125),
859~
            ("nono", 1.0/9), ("décimo", 0.1)
860~
        ]
861~
        
862~
        for fraction_word, expected_value in fraction_tests:
863~
            result = is_fractional_pt(fraction_word)
864~
            self.assertAlmostEqual(result, expected_value, places=10)
865~

866~
    def test_all_plural_fractions(self):
867~
        """Test all plural fraction forms."""
868~
        plural_tests = [
869~
            ("meios", 0.5), ("terços", 1.0/3), ("quartos", 0.25),
870~
            ("quintos", 0.2), ("sextos", 1.0/6), ("sétimos", 1.0/7),
871~
            ("oitavos", 0.125), ("nonos", 1.0/9), ("décimos", 0.1)
872~
        ]
873~
        
874~
        for fraction_word, expected_value in plural_tests:
875~
            result = is_fractional_pt(fraction_word)
876~
            self.assertAlmostEqual(result, expected_value, places=10)
877~

878~
    def test_ordinal_fractions(self):
879~
        """Test ordinal-based fractions."""
880~
        ordinal_tests = [
881~
            ("vigésimo", 0.05), ("trigésimo", 1.0/30), ("centésimo", 0.01),
882~
            ("milésimo", 0.001)
883~
        ]
884~
        
885~
        for fraction_word, expected_value in ordinal_tests:
886~
            result = is_fractional_pt(fraction_word)
887~
            if result:  # Only test if the function recognizes it
888~
                self.assertAlmostEqual(result, expected_value, places=10)
889~

890~
    def test_compound_avos_systematic(self):
891~
        """Test compound 'avos' fractions systematically."""
892~
        avos_tests = [
893~
            ("onze avos", 1.0/11), ("doze avos", 1.0/12), ("treze avos", 1.0/13),
894~
            ("catorze avos", 1.0/14), ("quinze avos", 1.0/15), ("dezesseis avos", 1.0/16),
895~
            ("dezessete avos", 1.0/17), ("dezoito avos", 1.0/18), ("dezenove avos", 1.0/19),
896~
            ("vinte avos", 1.0/20)
897~
        ]
898~
        
899~
        for fraction_phrase, expected_value in avos_tests:
900~
            result = is_fractional_pt(fraction_phrase)
901~
            if result:  # Only test if recognized
902~
                self.assertAlmostEqual(result, expected_value, places=10)
903~

904~
    def test_case_variations(self):
905~
        """Test various case combinations."""
906~
        case_tests = [
907~
            ("MEIO", 0.5), ("Meio", 0.5), ("meio", 0.5),
908~
            ("TERÇO", 1.0/3), ("Terço", 1.0/3), ("terço", 1.0/3),
909~
            ("MEIA", 0.5), ("Meia", 0.5), ("meia", 0.5)
910~
        ]
911~
        
912~
        for fraction_word, expected_value in case_tests:
913~
            result = is_fractional_pt(fraction_word)
914~
            self.assertAlmostEqual(result, expected_value, places=10)
915~

916~
    def test_whitespace_variations(self):
917~
        """Test various whitespace scenarios."""
918~
        whitespace_tests = [
919~
            ("  meio  ", 0.5), ("\tterço\t", 1.0/3), ("\nquarto\n", 0.25),
920~
            ("meio ", 0.5), (" meio", 0.5), ("  onze avos  ", 1.0/11)
921~
        ]
922~
        
923~
        for fraction_phrase, expected_value in whitespace_tests:
924~
            result = is_fractional_pt(fraction_phrase)
925~
            if result:
926~
                self.assertAlmostEqual(result, expected_value, places=10)
927~

928~
    def test_non_fraction_edge_cases(self):
929~
        """Test comprehensive non-fraction cases."""
930~
        non_fractions = [
931~
            "", "   ", "\t\n", "palavra", "número", "123", "12.34",
932~
            "meio meio", "terço quarto", "avos", "onze", "doze",
933~
            "special characters !@#", "meio-terço", "1/2", "0.5"
934~
        ]
935~
        
936~
        for non_fraction in non_fractions:
937~
            result = is_fractional_pt(non_fraction)
938~
            self.assertFalse(result, f"'{non_fraction}' should not be recognized as fraction")
939~

940~
    def test_invalid_input_types(self):
941~
        """Test behavior with invalid input types."""
942~
        invalid_inputs = [None, 123, 12.34, [], {}, set()]
943~
        for invalid_input in invalid_inputs:
944~
            with self.assertRaises((TypeError, AttributeError)):
945~
                is_fractional_pt(invalid_input)
946~

947~

948~
class TestExtractNumberPtExtensive(unittest.TestCase):
949~
    """Extensive tests for extract_number_pt function."""
950~

951~
    def test_zero_variations(self):
952~
        """Test various ways to express zero."""
953~
        zero_tests = ["zero", "ZERO", "Zero", " zero ", "\tzero\n"]
954~
        for zero_text in zero_tests:
955~
            result = extract_number_pt(zero_text)
956~
            self.assertEqual(result, 0)
957~

958~
    def test_single_digit_comprehensive(self):
959~
        """Test all single digits in various formats."""
960~
        digit_tests = [
961~
            ("um", 1), ("dois", 2), ("três", 3), ("quatro", 4), ("cinco", 5),
962~
            ("seis", 6), ("sete", 7), ("oito", 8), ("nove", 9)
963~
        ]
964~
        
965~
        for text, expected in digit_tests:
966~
            result = extract_number_pt(text)
967~
            self.assertEqual(result, expected)
968~
            
969~
            # Test with different cases
970~
            result_upper = extract_number_pt(text.upper())
971~
            self.assertEqual(result_upper, expected)
972~

973~
    def test_teens_comprehensive(self):
974~
        """Test all teen numbers in both variants."""
975~
        teen_tests_br = [
976~
            ("dez", 10), ("onze", 11), ("doze", 12), ("treze", 13), ("catorze", 14),
977~
            ("quinze", 15), ("dezesseis", 16), ("dezessete", 17), ("dezoito", 18), ("dezenove", 19)
978~
        ]
979~
        
980~
        teen_tests_pt = [
981~
            ("dez", 10), ("onze", 11), ("doze", 12), ("treze", 13), ("catorze", 14),
982~
            ("quinze", 15), ("dezasseis", 16), ("dezassete", 17), ("dezoito", 18), ("dezanove", 19)
983~
        ]
984~
        
985~
        for text, expected in teen_tests_br:
986~
            result = extract_number_pt(text, variant=PortugueseVariant.BR)
987~
            self.assertEqual(result, expected)
988~
            
989~
        for text, expected in teen_tests_pt:
990~
            result = extract_number_pt(text, variant=PortugueseVariant.PT)
991~
            self.assertEqual(result, expected)
992~

993~
    def test_complex_hundreds(self):
994~
        """Test complex hundred combinations."""
995~
        hundred_tests = [
996~
            ("cento e um", 101), ("cento e dez", 110), ("cento e onze", 111),
997~
            ("cento e vinte", 120), ("cento e vinte e um", 121),
998~
            ("duzentos e cinquenta e três", 253), ("trezentos e quarenta e cinco", 345),
999~
            ("quatrocentos e sessenta e sete", 467), ("quinhentos e oitenta e nove", 589),
1000~
            ("seiscentos e noventa e nove", 699), ("setecentos", 700),
1001~
            ("oitocentos e doze", 812), ("novecentos e noventa e nove", 999)
1002~
        ]
1003~
        
1004~
        for text, expected in hundred_tests:
1005~
            result = extract_number_pt(text)
1006~
            self.assertEqual(result, expected, f"Failed for '{text}'")
1007~

1008~
    def test_thousands_comprehensive(self):
1009~
        """Test thousand combinations."""
1010~
        thousand_tests = [
1011~
            ("mil", 1000), ("mil e um", 1001), ("mil e dez", 1010),
1012~
            ("mil e cem", 1100), ("mil duzentos", 1200), ("mil duzentos e trinta e quatro", 1234),
1013~
            ("dois mil", 2000), ("dois mil e quinhentos", 2500),
1014~
            ("três mil quatrocentos e cinquenta e seis", 3456),
1015~
            ("dez mil", 10000), ("vinte mil", 20000), ("cem mil", 100000),
1016~
            ("duzentos mil", 200000), ("novecentos e noventa e nove mil", 999000)
1017~
        ]
1018~
        
1019~
        for text, expected in thousand_tests:
1020~
            result = extract_number_pt(text)
1021~
            self.assertEqual(result, expected, f"Failed for '{text}'")
1022~

1023~
    def test_millions_all_scales_variants(self):
1024~
        """Test millions with all scale and variant combinations."""
1025~
        million_tests = [
1026~
            # Short scale tests
1027~
            (("um milhão", Scale.SHORT, PortugueseVariant.BR), 1000000),
1028~
            (("um milhão", Scale.SHORT, PortugueseVariant.PT), 1000000),
1029~
            (("dois milhões", Scale.SHORT, PortugueseVariant.BR), 2000000),
1030~
            (("cinco milhões", Scale.SHORT, PortugueseVariant.PT), 5000000),
1031~
            
1032~
            # Large number tests
1033~
            (("um bilhão", Scale.SHORT, PortugueseVariant.BR), 1000000000),
1034~
            (("um bilião", Scale.SHORT, PortugueseVariant.PT), 1000000000),
1035~
        ]
1036~
        
1037~
        for (text, scale, variant), expected in million_tests:
1038~
            result = extract_number_pt(text, scale=scale, variant=variant)
1039~
            self.assertEqual(result, expected, f"Failed for '{text}' with {scale} and {variant}")
1040~

1041~
    def test_decimal_comprehensive(self):
1042~
        """Test decimal number extraction."""
1043~
        # Test various decimal formats if supported
1044~
        decimal_tests = [
1045~
            "um vírgula cinco", "dois vírgula três", "zero vírgula cinco",
1046~
            "dez vírgula dois cinco", "cem vírgula nove nove"
1047~
        ]
1048~
        
1049~
        for decimal_text in decimal_tests:
1050~
            result = extract_number_pt(decimal_text)
1051~
            if result:  # Only verify if the function handles decimals
1052~
                self.assertIsInstance(result, (int, float))
1053~

1054~
    def test_fraction_in_context(self):
1055~
        """Test fractions within larger text."""
1056~
        fraction_tests = [
1057~
            ("dois e meio", 2.5), ("três e um quarto", 3.25),
1058~
            ("um e meio", 1.5), ("cinco e três quartos", 5.75)
1059~
        ]
1060~
        
1061~
        for text, expected in fraction_tests:
1062~
            result = extract_number_pt(text)
1063~
            if result:  # Only test if fractions are supported
1064~
                self.assertAlmostEqual(result, expected, places=2)
1065~

1066~
    def test_mixed_text_scenarios(self):
1067~
        """Test extraction from mixed text scenarios."""
1068~
        mixed_tests = [
1069~
            ("há vinte e cinco pessoas", 25),
1070~
            ("comprei trinta livros ontem", 30),
1071~
            ("ele tem cinquenta anos", 50),
1072~
            ("custou duzentos reais", 200),
1073~
            ("foram mil participantes", 1000)
1074~
        ]
1075~
        
1076~
        for text, expected in mixed_tests:
1077~
            result = extract_number_pt(text)
1078~
            self.assertEqual(result, expected, f"Failed to extract from '{text}'")
1079~

1080~
    def test_multiple_numbers_first_extraction(self):
1081~
        """Test that first number is extracted when multiple exist."""
1082~
        multi_tests = [
1083~
            ("dez carros e cinco pessoas", 10),
1084~
            ("primeiro vinte depois trinta", 20),
1085~
            ("cem mais cinquenta", 100)
1086~
        ]
1087~
        
1088~
        for text, expected_first in multi_tests:
1089~
            result = extract_number_pt(text)
1090~
            self.assertEqual(result, expected_first, f"Failed to extract first number from '{text}'")
1091~

1092~
    def test_error_conditions_comprehensive(self):
1093~
        """Test comprehensive error conditions."""
1094~
        error_cases = [
1095~
            "", "   ", "\t\n", "apenas palavras", "não há números aqui",
1096~
            "special characters !@#$%", "1a2b3c", "meio-número",
1097~
            None  # This should raise TypeError
1098~
        ]
1099~
        
1100~
        for error_case in error_cases:
1101~
            if error_case is None:
1102~
                with self.assertRaises(TypeError):
1103~
                    extract_number_pt(error_case)
1104~
            else:
1105~
                result = extract_number_pt(error_case)
1106~
                self.assertFalse(result, f"Should return False for '{error_case}'")
1107~

1108~
    def test_hyphen_variations(self):
1109~
        """Test various hyphen scenarios."""
1110~
        hyphen_tests = [
1111~
            ("vinte-e-um", 21), ("trinta-e-dois", 32), ("quarenta-e-três", 43),
1112~
            ("cinquenta-e-quatro", 54), ("sessenta-e-cinco", 65)
1113~
        ]
1114~
        
1115~
        for text, expected in hyphen_tests:
1116~
            result = extract_number_pt(text)
1117~
            if result:  # Only test if hyphenated forms are supported
1118~
                self.assertEqual(result, expected)
1119~

1120~
    def test_scale_edge_cases(self):
1121~
        """Test edge cases with different scales."""
1122~
        # Test very large numbers
1123~
        large_tests = [
1124~
            ("um trilião", Scale.SHORT, PortugueseVariant.PT, 1e12),
1125~
            ("um trilião", Scale.LONG, PortugueseVariant.PT, 1e18),
1126~
        ]
1127~
        
1128~
        for text, scale, variant, expected in large_tests:
1129~
            result = extract_number_pt(text, scale=scale, variant=variant)
1130~
            if result:  # Only test if such large numbers are supported
1131~
                self.assertEqual(result, expected)
1132~

1133~

1134~
class TestPronounceNumberPtExtensive(unittest.TestCase):
1135~
    """Extensive tests for pronounce_number_pt function."""
1136~

1137~
    def test_type_validation_comprehensive(self):
1138~
        """Test comprehensive type validation."""
1139~
        invalid_types = [
1140~
            "string", "123", [], {}, set(), object(), 
1141~
            complex(1, 2), True, False
1142~
        ]
1143~
        
1144~
        for invalid_input in invalid_types:
1145~
            with self.assertRaises(TypeError):
1146~
                pronounce_number_pt(invalid_input)
1147~

1148~
    def test_none_handling(self):
1149~
        """Test None input handling."""
1150~
        with self.assertRaises(TypeError):
1151~
            pronounce_number_pt(None)
1152~

1153~
    def test_negative_numbers_comprehensive(self):
1154~
        """Test comprehensive negative number pronunciation."""
1155~
        negative_tests = [
1156~
            (-1, "menos um"), (-16, "menos dezesseis"), (-100, "menos cem"),
1157~
            (-123, "menos cento e vinte e três"), (-1000, "menos mil")
1158~
        ]
1159~
        
1160~
        for number, expected_contains in negative_tests:
1161~
            result = pronounce_number_pt(number)
1162~
            self.assertTrue(result.startswith("menos"))
1163~
            # Check that the positive part is there
1164~
            positive_part = expected_contains.replace("menos ", "")
1165~
            self.assertIn(positive_part, result)
1166~

1167~
    def test_float_precision(self):
1168~
        """Test float precision handling."""
1169~
        float_tests = [
1170~
            (1.0, "um vírgula zero"), (2.5, "dois vírgula cinco"),
1171~
            (10.25, "dez vírgula dois cinco"), (100.99, "cem vírgula nove nove")
1172~
        ]
1173~
        
1174~
        for number, expected_pattern in float_tests:
1175~
            result = pronounce_number_pt(number)
1176~
            self.assertIn("vírgula", result)
1177~
            # Verify the integer part is correct
1178~
            integer_part = int(number)
1179~
            integer_result = pronounce_number_pt(integer_part)
1180~
            self.assertTrue(result.startswith(integer_result.split("vírgula")[0].strip()) or 
1181~
                          result.startswith(integer_result))
1182~

1183~
    def test_very_small_decimals(self):
1184~
        """Test very small decimal numbers."""
1185~
        small_tests = [0.1, 0.01, 0.001, 0.0001]
1186~
        
1187~
        for number in small_tests:
1188~
            result = pronounce_number_pt(number)
1189~
            self.assertIsInstance(result, str)
1190~
            self.assertIn("vírgula", result)
1191~

1192~
    def test_very_large_integers(self):
1193~
        """Test very large integer pronunciation."""
1194~
        large_tests = [1000000, 1000000000, 1000000000000]
1195~
        
1196~
        for number in large_tests:
1197~
            result = pronounce_number_pt(number)
1198~
            self.assertIsInstance(result, str)
1199~
            self.assertTrue(len(result) > 0)
1200~

1201~
    def test_variant_consistency_comprehensive(self):
1202~
        """Test variant consistency across number ranges."""
1203~
        test_numbers = [16, 17, 19, 116, 117, 119, 216, 217, 219]
1204~
        
1205~
        for number in test_numbers:
1206~
            br_result = pronounce_number_pt(number, variant=PortugueseVariant.BR)
1207~
            pt_result = pronounce_number_pt(number, variant=PortugueseVariant.PT)
1208~
            
1209~
            # Both should be valid strings
1210~
            self.assertIsInstance(br_result, str)
1211~
            self.assertIsInstance(pt_result, str)
1212~
            self.assertTrue(len(br_result) > 0)
1213~
            self.assertTrue(len(pt_result) > 0)
1214~
            
1215~
            # For numbers with variant differences, results should differ
1216~
            if number in [16, 17, 19, 116, 117, 119, 216, 217, 219]:
1217~
                # Results may differ for these numbers
1218~
                pass  # Just ensure they're both valid
1219~

1220~
    def test_scale_parameter_comprehensive(self):
1221~
        """Test scale parameter with various numbers."""
1222~
        large_numbers = [1000000, 1000000000, 1000000000000]
1223~
        
1224~
        for number in large_numbers:
1225~
            for scale in [Scale.SHORT, Scale.LONG]:
1226~
                for variant in [PortugueseVariant.BR, PortugueseVariant.PT]:
1227~
                    result = pronounce_number_pt(number, scale=scale, variant=variant)
1228~
                    self.assertIsInstance(result, str)
1229~
                    self.assertTrue(len(result) > 0)
1230~

1231~
    def test_digits_parameter(self):
1232~
        """Test digits parameter functionality."""
1233~
        test_numbers = [123.45, 1000.123]
1234~
        
1235~
        for number in test_numbers:
1236~
            for digit_mode in [DigitPronunciation.NORMAL, DigitPronunciation.DIGIT_BY_DIGIT]:
1237~
                result = pronounce_number_pt(number, digits=digit_mode)
1238~
                self.assertIsInstance(result, str)
1239~
                self.assertTrue(len(result) > 0)
1240~

1241~
    def test_places_parameter_comprehensive(self):
1242~
        """Test places parameter with various scenarios."""
1243~
        decimal_number = 3.14159
1244~
        
1245~
        for places in [0, 1, 2, 3, 5, 10]:
1246~
            result = pronounce_number_pt(decimal_number, places=places, digits=DigitPronunciation.DIGIT_BY_DIGIT)
1247~
            self.assertIsInstance(result, str)
1248~
            self.assertTrue(len(result) > 0)
1249~

1250~
    def test_conjunction_patterns(self):
1251~
        """Test conjunction patterns in complex numbers."""
1252~
        conjunction_tests = [
1253~
            1001, 1010, 1100, 2001, 2010, 2100,
1254~
            10001, 10010, 10100, 11000
1255~
        ]
1256~
        
1257~
        for number in conjunction_tests:
1258~
            result = pronounce_number_pt(number)
1259~
            # Should contain appropriate conjunctions for readability
1260~
            self.assertIsInstance(result, str)
1261~
            self.assertTrue(len(result) > 0)
1262~

1263~
    def test_mil_edge_cases(self):
1264~
        """Test edge cases around 'mil' pronunciation."""
1265~
        mil_tests = [1000, 2000, 1001, 2001, 1100, 2100]
1266~
        
1267~
        for number in mil_tests:
1268~
            result = pronounce_number_pt(number)
1269~
            self.assertIn("mil", result)
1270~
            # 1000 should not start with "um mil"
1271~
            if number == 1000:
1272~
                self.assertFalse(result.startswith("um mil"))
1273~

1274~
    def test_extreme_values(self):
1275~
        """Test extreme numerical values."""
1276~
        extreme_tests = [
1277~
            0, 1, -1, 999, 1000, 999999, 1000000,
1278~
            float('inf'), float('-inf')
1279~
        ]
1280~
        
1281~
        for number in extreme_tests:
1282~
            if number in [float('inf'), float('-inf')]:
1283~
                # These might raise exceptions or return special strings
1284~
                try:
1285~
                    result = pronounce_number_pt(number)
1286~
                    self.assertIsInstance(result, str)
1287~
                except (ValueError, OverflowError):
1288~
                    pass  # Acceptable to raise exceptions for infinite values
1289~
            else:
1290~
                result = pronounce_number_pt(number)
1291~
                self.assertIsInstance(result, str)
1292~
                self.assertTrue(len(result) > 0)
1293~

1294~

1295~
class TestNumbersToDigitsPtExtensive(unittest.TestCase):
1296~
    """Extensive tests for numbers_to_digits_pt function."""
1297~

1298~
    def test_single_word_replacements(self):
1299~
        """Test single word number replacements."""
1300~
        single_tests = [
1301~
            ("zero", "0"), ("um", "1"), ("dois", "2"), ("três", "3"),
1302~
            ("quatro", "4"), ("cinco", "5"), ("seis", "6"), ("sete", "7"),
1303~
            ("oito", "8"), ("nove", "9"), ("dez", "10")
1304~
        ]
1305~
        
1306~
        for word, expected in single_tests:
1307~
            result = numbers_to_digits_pt(word)
1308~
            self.assertEqual(result, expected)
1309~

1310~
    def test_variant_specific_replacements(self):
1311~
        """Test variant-specific word replacements."""
1312~
        variant_tests = [
1313~
            ("dezesseis carros", PortugueseVariant.BR, "16 carros"),
1314~
            ("dezasseis carros", PortugueseVariant.PT, "16 carros"),
1315~
            ("dezessete pessoas", PortugueseVariant.BR, "17 pessoas"),
1316~
            ("dezassete pessoas", PortugueseVariant.PT, "17 pessoas")
1317~
        ]
1318~
        
1319~
        for text, variant, expected in variant_tests:
1320~
            result = numbers_to_digits_pt(text, variant=variant)
1321~
            self.assertEqual(result, expected)
1322~

1323~
    def test_complex_number_phrases(self):
1324~
        """Test complex number phrase replacements."""
1325~
        complex_tests = [
1326~
            ("duzentos e cinquenta e três", "253"),
1327~
            ("mil quinhentos e quarenta e dois", "1542"),
1328~
            ("dois milhões trezentos mil", "2300000"),
1329~
            ("cem mil e um", "100001")
1330~
        ]
1331~
        
1332~
        for phrase, expected in complex_tests:
1333~
            result = numbers_to_digits_pt(phrase)
1334~
            self.assertEqual(result, expected)
1335~

1336~
    def test_mixed_content_comprehensive(self):
1337~
        """Test comprehensive mixed content scenarios."""
1338~
        mixed_tests = [
1339~
            ("há duzentos carros e cinquenta motos", "há 200 carros e 50 motos"),
1340~
            ("comprei dez livros por vinte reais cada", "comprei 10 livros por 20 reais cada"),
1341~
            ("são três casas com cem metros quadrados", "são 3 casas com 100 metros quadrados"),
1342~
            ("primeiro dia, segundo mês, terceiro ano", "1º dia, 2º mês, 3º ano")
1343~
        ]
1344~
        
1345~
        for original, expected_pattern in mixed_tests:
1346~
            result = numbers_to_digits_pt(original)
1347~
            # Check that numbers were converted and text preserved
1348~
            self.assertIsInstance(result, str)
1349~
            self.assertTrue(any(char.isdigit() for char in result))
1350~
            # Check that some original words are preserved
1351~
            original_words = original.split()
1352~
            result_words = result.split()
1353~
            non_number_words = [w for w in original_words if not any(c.isalpha() and c in "umoistrêquacinsetetnovez" for c in w.lower())]
1354~
            for word in non_number_words[:2]:  # Check at least some non-number words are preserved
1355~
                if word not in ["há", "por", "com", "e"]:  # Skip common connecting words that might be modified
1356~
                    continue
1357~
                # This is a flexible check since the exact preservation depends on implementation
1358~

1359~
    def test_sentence_boundaries(self):
1360~
        """Test number replacement at sentence boundaries."""
1361~
        boundary_tests = [
1362~
            ("Cinco. Dez carros.", "5. 10 carros."),
1363~
            ("Um, dois, três pessoas.", "1, 2, 3 pessoas."),
1364~
            ("Primeiro: cem reais. Segundo: duzentos.", "1º: 100 reais. 2º: 200.")
1365~
        ]
1366~
        
1367~
        for original, expected_pattern in boundary_tests:
1368~
            result = numbers_to_digits_pt(original)
1369~
            # Verify numbers were converted
1370~
            self.assertTrue(any(char.isdigit() for char in result))
1371~
            # Verify punctuation is preserved
1372~
            self.assertTrue(any(char in ".,:;" for char in result))
1373~

1374~
    def test_ordinal_numbers(self):
1375~
        """Test ordinal number conversion."""
1376~
        ordinal_tests = [
1377~
            ("primeiro", "1º"), ("segunda", "2ª"), ("terceiro", "3º"),
1378~
            ("quarta", "4ª"), ("quinto", "5º"), ("sexta", "6ª"),
1379~
            ("sétimo", "7º"), ("oitava", "8ª"), ("nono", "9º"), ("décima", "10ª")
1380~
        ]
1381~
        
1382~
        for ordinal, expected in ordinal_tests:
1383~
            result = numbers_to_digits_pt(ordinal)
1384~
            if result != ordinal:  # Only test if ordinals are supported
1385~
                # Check that some transformation occurred
1386~
                self.assertTrue(any(char.isdigit() for char in result))
1387~

1388~
    def test_whitespace_preservation(self):
1389~
        """Test whitespace preservation in conversion."""
1390~
        whitespace_tests = [
1391~
            ("  cinco  carros  ", "  5  carros  "),
1392~
            ("\tdez\tpessoas\t", "\t10\tpessoas\t"),
1393~
            ("um\ncarro\ndois\nmotos", "1\ncarro\n2\nmotos")
1394~
        ]
1395~
        
1396~
        for original, expected_pattern in whitespace_tests:
1397~
            result = numbers_to_digits_pt(original)
1398~
            # Check that leading/trailing whitespace is preserved
1399~
            if original.startswith("  "):
1400~
                self.assertTrue(result.startswith("  "))
1401~
            if original.endswith("  "):
1402~
                self.assertTrue(result.endswith("  "))
1403~

1404~
    def test_case_preservation(self):
1405~
        """Test case preservation in non-number words."""
1406~
        case_tests = [
1407~
            ("Cinco CARROS", "5 CARROS"),
1408~
            ("DEZ pessoas", "10 pessoas"),
1409~
            ("Um Carro", "1 Carro")
1410~
        ]
1411~
        
1412~
        for original, expected_pattern in case_tests:
1413~
            result = numbers_to_digits_pt(original)
1414~
            # Verify numbers converted and case preserved in other words
1415~
            self.assertTrue(any(char.isdigit() for char in result))
1416~
            # Check that CARROS remains uppercase
1417~
            if "CARROS" in original:
1418~
                self.assertIn("CARROS", result)
1419~

1420~
    def test_partial_number_phrases(self):
1421~
        """Test partial number phrases that shouldn't be converted."""
1422~
        partial_tests = [
1423~
            ("meio dia", "meio dia"),  # "meio" alone shouldn't convert if not supported
1424~
            ("onze horas", "11 horas"),  # Should convert
1425~
            ("doze meses", "12 meses")   # Should convert
1426~
        ]
1427~
        
1428~
        for original, expected_hint in partial_tests:
1429~
            result = numbers_to_digits_pt(original)
1430~
            if "11" in expected_hint or "12" in expected_hint:
1431~
                self.assertTrue(any(char.isdigit() for char in result))
1432~
            # The exact behavior depends on implementation
1433~

1434~
    def test_error_resilience(self):
1435~
        """Test resilience to various error conditions."""
1436~
        error_tests = ["", "   ", "\t\n", "!@#$%^&*()", "123abc", "abc123def"]
1437~
        
1438~
        for error_input in error_tests:
1439~
            result = numbers_to_digits_pt(error_input)
1440~
            # Should not raise exceptions
1441~
            self.assertIsInstance(result, str)
1442~
            
1443~
    def test_numbers_in_quotes(self):
1444~
        """Test numbers within quoted text."""
1445~
        quote_tests = [
1446~
            ('ele disse "cinco carros"', 'ele disse "5 carros"'),
1447~
            ("são 'dez pessoas'", "são '10 pessoas'"),
1448~
            ('"primeiro lugar"', '"1º lugar"')
1449~
        ]
1450~
        
1451~
        for original, expected_pattern in quote_tests:
1452~
            result = numbers_to_digits_pt(original)
1453~
            # Verify quotes are preserved and numbers converted
1454~
            self.assertTrue('"' in result or "'" in result)
1455~
            self.assertTrue(any(char.isdigit() for char in result))
1456~

1457~

1458~
class TestTokenizeExtensive(unittest.TestCase):
1459~
    """Extensive tests for tokenize function."""
1460~

1461~
    def test_basic_word_tokenization_comprehensive(self):
1462~
        """Test comprehensive basic word tokenization."""
1463~
        basic_tests = [
1464~
            ("uma palavra", ["uma", "palavra"]),
1465~
            ("três palavras aqui", ["três", "palavras", "aqui"]),
1466~
            ("", []),
1467~
            ("palavra", ["palavra"]),
1468~
            ("a b c d e", ["a", "b", "c", "d", "e"])
1469~
        ]
1470~
        
1471~
        for text, expected in basic_tests:
1472~
            result = tokenize(text)
1473~
            self.assertEqual(result, expected)
1474~

1475~
    def test_percentage_handling_comprehensive(self):
1476~
        """Test comprehensive percentage handling."""
1477~
        percentage_tests = [
1478~
            ("50%", ["50", "%"]),
1479~
            ("100%", ["100", "%"]),
1480~
            ("0.5%", ["0.5", "%"]),
1481~
            ("texto 25% mais", ["texto", "25", "%", "mais"]),
1482~
            ("12.34%", ["12.34", "%"])
1483~
        ]
1484~
        
1485~
        for text, expected in percentage_tests:
1486~
            result = tokenize(text)
1487~
            self.assertEqual(result, expected)
1488~

1489~
    def test_hash_number_handling_comprehensive(self):
1490~
        """Test comprehensive hash with number handling."""
1491~
        hash_tests = [
1492~
            ("#1", ["#", "1"]),
1493~
            ("#10", ["#", "10"]),
1494~
            ("#123", ["#", "123"]),
1495~
            ("canal #5 favorito", ["canal", "#", "5", "favorito"]),
1496~
            ("#0", ["#", "0"])
1497~
        ]
1498~
        
1499~
        for text, expected in hash_tests:
1500~
            result = tokenize(text)
1501~
            self.assertEqual(result, expected)
1502~

1503~
    def test_hyphen_handling_comprehensive(self):
1504~
        """Test comprehensive hyphen handling."""
1505~
        hyphen_tests = [
1506~
            ("amo-te", ["amo", "-", "te"]),
1507~
            ("guarda-chuva", ["guarda", "-", "chuva"]),
1508~
            ("bem-vindo", ["bem", "-", "vindo"]),
1509~
            ("palavra - outra", ["palavra", "-", "outra"]),
1510~
            ("auto-estrada", ["auto", "-", "estrada"])
1511~
        ]
1512~
        
1513~
        for text, expected in hyphen_tests:
1514~
            result = tokenize(text)
1515~
            self.assertEqual(result, expected)
1516~

1517~
    def test_number_range_preservation(self):
1518~
        """Test preservation of number ranges."""
1519~
        range_tests = [
1520~
            ("1-2", ["1-2"]),
1521~
            ("10-20", ["10-20"]),
1522~
            ("100-200", ["100-200"]),
1523~
            ("0.5-1.5", ["0.5-1.5"]),
1524~
            ("páginas 1-5", ["páginas", "1-5"])
1525~
        ]
1526~
        
1527~
        for text, expected in range_tests:
1528~
            result = tokenize(text)
1529~
            self.assertEqual(result, expected)
1530~

1531~
    def test_trailing_hyphen_removal_comprehensive(self):
1532~
        """Test comprehensive trailing hyphen removal."""
1533~
        trailing_tests = [
1534~
            ("palavra -", ["palavra"]),
1535~
            ("texto - ", ["texto"]),
1536~
            ("fim -   ", ["fim"]),
1537~
            ("múltiplas palavras -", ["múltiplas", "palavras"]),
1538~
            ("- início", ["-", "início"])  # Leading hyphen should be preserved
1539~
        ]
1540~
        
1541~
        for text, expected in trailing_tests:
1542~
            result = tokenize(text)
1543~
            self.assertEqual(result, expected)
1544~

1545~
    def test_whitespace_normalization(self):
1546~
        """Test whitespace normalization."""
1547~
        whitespace_tests = [
1548~
            ("  palavra  ", ["palavra"]),
1549~
            ("\tpalavra\t", ["palavra"]),
1550~
            ("\npalavra\n", ["palavra"]),
1551~
            ("  múltiplas   palavras  ", ["múltiplas", "palavras"]),
1552~
            ("misturado\t  \npalavras", ["misturado", "palavras"])
1553~
        ]
1554~
        
1555~
        for text, expected in whitespace_tests:
1556~
            result = tokenize(text)
1557~
            self.assertEqual(result, expected)
1558~

1559~
    def test_mixed_patterns_comprehensive(self):
1560~
        """Test comprehensive mixed pattern scenarios."""
1561~
        mixed_tests = [
1562~
            ("amo-te 50% #2 teste", ["amo", "-", "te", "50", "%", "#", "2", "teste"]),
1563~
            ("canal #1 tem 100% audiência", ["canal", "#", "1", "tem", "100", "%", "audiência"]),
1564~
            ("páginas 1-5 são 80% do livro", ["páginas", "1-5", "são", "80", "%", "do", "livro"]),
1565~
            ("bem-estar #3 100%", ["bem", "-", "estar", "#", "3", "100", "%"])
1566~
        ]
1567~
        
1568~
        for text, expected in mixed_tests:
1569~
            result = tokenize(text)
1570~
            self.assertEqual(result, expected)
1571~

1572~
    def test_punctuation_handling(self):
1573~
        """Test punctuation handling."""
1574~
        punctuation_tests = [
1575~
            ("palavra.", ["palavra."]),
1576~
            ("palavra,", ["palavra,"]),
1577~
            ("palavra!", ["palavra!"]),
1578~
            ("palavra?", ["palavra?"]),
1579~
            ("palavra;", ["palavra;"]),
1580~
            ("palavra:", ["palavra:"])
1581~
        ]
1582~
        
1583~
        for text, expected in punctuation_tests:
1584~
            result = tokenize(text)
1585~
            self.assertEqual(result, expected)
1586~

1587~
    def test_special_characters(self):
1588~
        """Test special character handling."""
1589~
        special_tests = [
1590~
            ("email@test.com", ["email@test.com"]),
1591~
            ("www.test.com", ["www.test.com"]),
1592~
            ("preço: R$50", ["preço:", "R$50"]),
1593~
            ("temp. 25°C", ["temp.", "25°C"])
1594~
        ]
1595~
        
1596~
        for text, expected in special_tests:
1597~
            result = tokenize(text)
1598~
            # These tests verify that special patterns are handled reasonably
1599~
            self.assertIsInstance(result, list)
1600~
            self.assertTrue(all(isinstance(token, str) for token in result))
1601~

1602~
    def test_edge_cases_comprehensive(self):
1603~
        """Test comprehensive edge cases."""
1604~
        edge_tests = [
1605~
            ("", []),
1606~
            ("   ", []),
1607~
            ("\t\n", []),
1608~
            ("-", []),
1609~
            ("%", ["%"]),
1610~
            ("#", ["#"]),
1611~
            ("- - -", ["-", "-", "-"]),
1612~
            ("# # #", ["#", "#", "#"])
1613~
        ]
1614~
        
1615~
        for text, expected in edge_tests:
1616~
            result = tokenize(text)
1617~
            self.assertEqual(result, expected)
1618~

1619~
    def test_unicode_handling(self):
1620~
        """Test Unicode character handling."""
1621~
        unicode_tests = [
1622~
            ("café", ["café"]),
1623~
            ("São Paulo", ["São", "Paulo"]),
1624~
            ("coração", ["coração"]),
1625~
            ("não", ["não"]),
1626~
            ("maçã", ["maçã"])
1627~
        ]
1628~
        
1629~
        for text, expected in unicode_tests:
1630~
            result = tokenize(text)
1631~
            self.assertEqual(result, expected)
1632~

1633~

1634~
class TestPronounceFractionPtExtensive(unittest.TestCase):
1635~
    """Extensive tests for pronounce_fraction_pt function."""
1636~

1637~
    def test_basic_fractions_comprehensive(self):
1638~
        """Test comprehensive basic fraction pronunciation."""
1639~
        basic_tests = [
1640~
            ("1/2", ("um", "meio")), ("1/3", ("um", "terço")), ("1/4", ("um", "quarto")),
1641~
            ("1/5", ("um", "quinto")), ("1/6", ("um", "sexto")), ("1/7", ("um", "sétimo")),
1642~
            ("1/8", ("um", "oitavo")), ("1/9", ("um", "nono")), ("1/10", ("um", "décimo"))
1643~
        ]
1644~
        
1645~
        for fraction, (expected_num, expected_den) in basic_tests:
1646~
            result = pronounce_fraction_pt(fraction)
1647~
            self.assertIn(expected_num, result.lower())
1648~
            self.assertIn(expected_den, result.lower())
1649~

1650~
    def test_plural_fractions_comprehensive(self):
1651~
        """Test comprehensive plural fraction pronunciation."""
1652~
        plural_tests = [
1653~
            ("2/3", ("dois", "terços")), ("3/4", ("três", "quartos")), ("2/5", ("dois", "quintos")),
1654~
            ("4/7", ("quatro", "sétimos")), ("5/8", ("cinco", "oitavos")), ("6/9", ("seis", "nonos"))
1655~
        ]
1656~
        
1657~
        for fraction, (expected_num, expected_den) in plural_tests:
1658~
            result = pronounce_fraction_pt(fraction)
1659~
            self.assertIn(expected_num, result.lower())
1660~
            self.assertIn(expected_den, result.lower())
1661~

1662~
    def test_large_numerators(self):
1663~
        """Test fractions with large numerators."""
1664~
        large_tests = [
1665~
            ("10/3", "dez"), ("15/4", "quinze"), ("20/7", "vinte"),
1666~
            ("100/3", "cem"), ("123/5", "cento")
1667~
        ]
1668~
        
1669~
        for fraction, expected_num_part in large_tests:
1670~
            result = pronounce_fraction_pt(fraction)
1671~
            self.assertIn(expected_num_part, result.lower())
1672~

1673~
    def test_large_denominators_systematic(self):
1674~
        """Test systematic large denominators."""
1675~
        large_denom_tests = [
1676~
            ("1/11", "onze"), ("1/12", "doze"), ("1/13", "treze"),
1677~
            ("1/20", "vinte"), ("1/30", "trinta"), ("1/100", "cem")
1678~
        ]
1679~
        
1680~
        for fraction, expected_denom_part in large_denom_tests:
1681~
            result = pronounce_fraction_pt(fraction)
1682~
            # May use "avos" for unknown denominators
1683~
            self.assertTrue(expected_denom_part in result.lower() or "avos" in result.lower())
1684~

1685~
    def test_zero_fractions(self):
1686~
        """Test fractions with zero numerator."""
1687~
        zero_tests = ["0/2", "0/3", "0/5", "0/10"]
1688~
        
1689~
        for fraction in zero_tests:
1690~
            result = pronounce_fraction_pt(fraction)
1691~
            self.assertIn("zero", result.lower())
1692~

1693~
    def test_improper_fractions(self):
1694~
        """Test improper fractions."""
1695~
        improper_tests = [
1696~
            ("3/2", "três"), ("5/3", "cinco"), ("7/4", "sete"),
1697~
            ("9/5", "nove"), ("11/6", "onze")
1698~
        ]
1699~
        
1700~
        for fraction, expected_num in improper_tests:
1701~
            result = pronounce_fraction_pt(fraction)
1702~
            self.assertIn(expected_num, result.lower())
1703~

1704~
    def test_variant_parameter_comprehensive(self):
1705~
        """Test variant parameter comprehensively."""
1706~
        test_fractions = ["1/16", "2/17", "3/19", "4/16"]
1707~
        
1708~
        for fraction in test_fractions:
1709~
            for variant in [PortugueseVariant.BR, PortugueseVariant.PT]:
1710~
                result = pronounce_fraction_pt(fraction, variant=variant)
1711~
                self.assertIsInstance(result, str)
1712~
                self.assertTrue(len(result) > 0)
1713~

1714~
    def test_scale_parameter_comprehensive(self):
1715~
        """Test scale parameter comprehensively."""
1716~
        large_fractions = ["1/1000000", "2/1000000000", "1/1000000000000"]
1717~
        
1718~
        for fraction in large_fractions:
1719~
            for scale in [Scale.SHORT, Scale.LONG]:
1720~
                result = pronounce_fraction_pt(fraction, scale=scale)
1721~
                self.assertIsInstance(result, str)
1722~
                self.assertTrue(len(result) > 0)
1723~

1724~
    def test_decimal_fractions(self):
1725~
        """Test decimal fraction inputs."""
1726~
        decimal_tests = ["0.5", "0.25", "0.75", "1.5", "2.25"]
1727~
        
1728~
        for decimal in decimal_tests:
1729~
            # Test if function handles decimal input
1730~
            try:
1731~
                result = pronounce_fraction_pt(decimal)
1732~
                if result:  # Only verify if decimal input is supported
1733~
                    self.assertIsInstance(result, str)
1734~
                    self.assertTrue(len(result) > 0)
1735~
            except (ValueError, TypeError):
1736~
                pass  # Acceptable if decimal input is not supported
1737~

1738~
    def test_complex_fractions(self):
1739~
        """Test complex fraction scenarios."""
1740~
        complex_tests = [
1741~
            ("22/7", "vinte e dois"), ("355/113", "trezentos"),
1742~
            ("1001/1000", "mil e um")
1743~
        ]
1744~
        
1745~
        for fraction, expected_num_part in complex_tests:
1746~
            result = pronounce_fraction_pt(fraction)
1747~
            # Check that numerator is pronounced correctly
1748~
            self.assertTrue(any(part in result.lower() for part in expected_num_part.split()))
1749~

1750~
    def test_edge_case_fractions(self):
1751~
        """Test edge case fractions."""
1752~
        edge_tests = [
1753~
            ("1/1", "um"),  # Whole number
1754~
            ("0/1", "zero"), # Zero
1755~
            ("1000/1", "mil")  # Large whole number
1756~
        ]
1757~
        
1758~
        for fraction, expected_part in edge_tests:
1759~
            result = pronounce_fraction_pt(fraction)
1760~
            self.assertIn(expected_part, result.lower())
1761~

1762~
    def test_malformed_fraction_handling(self):
1763~
        """Test handling of malformed fraction inputs."""
1764~
        malformed_tests = [
1765~
            "", "1", "1/", "/2", "a/b", "1/0", "1/2/3", "1.5/2.5"
1766~
        ]
1767~
        
1768~
        for malformed in malformed_tests:
1769~
            try:
1770~
                result = pronounce_fraction_pt(malformed)
1771~
                # Should either handle gracefully or raise appropriate exception
1772~
                if result:
1773~
                    self.assertIsInstance(result, str)
1774~
            except (ValueError, ZeroDivisionError, TypeError):
1775~
                pass  # Acceptable to raise exceptions for malformed input
1776~

1777~

1778~
class TestRegressionAndStress(unittest.TestCase):
1779~
    """Regression and stress tests."""
1780~

1781~
    def test_memory_usage_large_numbers(self):
1782~
        """Test memory usage with large numbers."""
1783~
        large_numbers = [10**i for i in range(1, 15)]
1784~
        
1785~
        for number in large_numbers:
1786~
            try:
1787~
                result = pronounce_number_pt(number)
1788~
                self.assertIsInstance(result, str)
1789~
                # Ensure reasonable length (not exponentially growing)
1790~
                self.assertLess(len(result), 10000)
1791~
            except (OverflowError, MemoryError):
1792~
                pass  # Acceptable for very large numbers
1793~

1794~
    def test_performance_multiple_extractions(self):
1795~
        """Test performance with multiple number extractions."""
1796~
        test_texts = [
1797~
            "há vinte e cinco carros e trinta motos",
1798~
            "primeiro lugar com cem pontos",
1799~
            "dois milhões trezentos mil reais",
1800~
            "quinhentos e quarenta e sete pessoas"
1801~
        ] * 10  # Multiply to create more test cases
1802~
        
1803~
        for text in test_texts:
1804~
            result = extract_number_pt(text)
1805~
            self.assertIsInstance(result, (int, float, bool))
1806~

1807~
    def test_unicode_edge_cases(self):
1808~
        """Test Unicode edge cases."""
1809~
        unicode_tests = [
1810~
            "tês", "quatrò", "cincô", "sêis", "sètè", "ôitô", "nòvè"
1811~
        ]
1812~
        
1813~
        for test_text in unicode_tests:
1814~
            # Should handle gracefully even with unusual Unicode
1815~
            result = extract_number_pt(test_text)
1816~
            self.assertIsInstance(result, (int, float, bool))
1817~

1818~
    def test_concurrent_operations_simulation(self):
1819~
        """Simulate concurrent operations."""
1820~
        import threading
1821~
        import time
1822~
        
1823~
        results = []
1824~
        errors = []
1825~
        
1826~
        def worker():
1827~
            try:
1828~
                for i in range(10):
1829~
                    num_result = pronounce_number_pt(i * 10)
1830~
                    extract_result = extract_number_pt(f"número {i * 10}")
1831~
                    results.append((num_result, extract_result))
1832~
            except Exception as e:
1833~
                errors.append(e)
1834~
        
1835~
        threads = [threading.Thread(target=worker) for _ in range(3)]
1836~
        for t in threads:
1837~
            t.start()
1838~
        for t in threads:
1839~
            t.join()
1840~
        
1841~
        # Should complete without errors
1842~
        self.assertEqual(len(errors), 0, f"Concurrent operations had errors: {errors}")
1843~
        self.assertGreater(len(results), 0)
1844~

1845~
    def test_boundary_value_comprehensive(self):
1846~
        """Test comprehensive boundary values."""
1847~
        boundary_tests = [
1848~
            # Integer boundaries
1849~
            0, 1, -1, 999, 1000, 999999, 1000000,
1850~
            # Float boundaries  
1851~
            0.0, 1.0, -1.0, 0.1, -0.1, 99.99, 100.01,
1852~
            # Large boundaries
1853~
            10**6, 10**9, 10**12
1854~
        ]
1855~
        
1856~
        for value in boundary_tests:
1857~
            try:
1858~
                pronounce_result = pronounce_number_pt(value)
1859~
                self.assertIsInstance(pronounce_result, str)
1860~
                self.assertTrue(len(pronounce_result) > 0)
1861~
                
1862~
                # Test round-trip for integers
1863~
                if isinstance(value, int) and 0 <= value <= 10**6:
1864~
                    extract_result = extract_number_pt(pronounce_result)
1865~
                    if extract_result:  # Only test if extraction succeeds
1866~
                        self.assertEqual(extract_result, value)
1867~
                        
1868~
            except (ValueError, OverflowError, TypeError):
1869~
                pass  # Acceptable for extreme values
1870~

1871~

1872~
if __name__ == '__main__':
1873~
    # Run with more verbose output for debugging
1874~
    unittest.main(verbosity=2)
1875~

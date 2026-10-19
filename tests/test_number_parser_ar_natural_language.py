"""Arabic numbers in whole sentences: prices, mileage, dates, quantities,
phone numbers and ordinals, as an agent says and hears them.

Two codes are covered. ``ar`` is Modern Standard Arabic; its expected words
follow Karin C. Ryding, "A Reference Grammar of Modern Standard Arabic"
(Cambridge UP, 2005), chapter 15: gender polarity in 3 to 10, both parts of
11 and 12 agreeing with the noun, the oblique dual and tens in -ayn/-iin, and
the ordinals as adjectives that agree in gender. ``ars`` is the Saudi table of
``AR_LECT_FORMS["ars"]``: the teens احدعش, ثنعش, ثلاثطعش to تسعطعش, the
hundreds مية and ميتين, a hundred from three to nine as a unit plus مية, and
the spoken half نص after a unit, a ten or a teen. Its sources are cited on
that table and on ``_SPOKEN_HALF_LOOKUP``.

Every sentence was written for this file. A case the library gets wrong is an
``xfail(strict=True)`` that states the right answer: no case asserts a wrong
output, and a fix makes its cases fail as XPASS until the mark is removed.
"""
import pytest

from ovos_number_parser import (extract_number, numbers_to_digits,
                                pronounce_number, pronounce_ordinal)
from ovos_number_parser.numbers_ar import extract_numbers_ar

BOTH = ("ar", "ars")


def gap(reason):
    return pytest.mark.xfail(strict=True, reason=reason)


# The gaps, each stated once and used by every case it covers.
TAMYIZ_ACCUSATIVE = gap(
    "after 11 to 99 the counted noun is singular accusative, so a thousand is "
    "ألفًا (Wikipedia 'Arabic grammar', 12,222: 'iṯnā ‘ašara alfan'), but "
    "the literary cardinal writes ألف")


def assert_value(actual, expected):
    if expected is False:
        assert actual is False
    else:
        assert actual is not False
        assert actual == pytest.approx(expected)


# ---------------------------------------------------------------------------
# pronounce_number
# ---------------------------------------------------------------------------

LITERARY_WORDS = [
    (0, "صفر"), (1, "واحد"), (2, "اثنان"), (3, "ثلاثة"), (7, "سبعة"),
    (8, "ثمانية"), (10, "عشرة"), (11, "أحد عشر"), (12, "اثنا عشر"),
    (13, "ثلاثة عشر"), (15, "خمسة عشر"), (19, "تسعة عشر"), (20, "عشرون"),
    (21, "واحد وعشرون"), (25, "خمسة وعشرون"), (48, "ثمانية وأربعون"),
    (99, "تسعة وتسعون"), (100, "مئة"), (101, "مئة وواحد"),
    (150, "مئة وخمسون"), (200, "مئتان"), (250, "مئتان وخمسون"),
    (300, "ثلاثمئة"), (475, "أربعمئة وخمسة وسبعون"), (800, "ثمانمئة"),
    (999, "تسعمئة وتسعة وتسعون"), (1000, "ألف"), (1500, "ألف وخمسمئة"),
    (1985, "ألف وتسعمئة وخمسة وثمانون"), (2000, "ألفان"),
    (2026, "ألفان وستة وعشرون"), (3000, "ثلاثة آلاف"),
    (10000, "عشرة آلاف"), (300000, "ثلاثمئة ألف"), (1000000, "مليون"),
    (2000000, "مليونان"), (5000000, "خمسة ملايين"),
    (2500000, "مليونان وخمسمئة ألف"), (1000000000, "مليار"),
    (3.5, "ثلاثة فاصلة خمسة"), (-5, "سالب خمسة"),
]


@pytest.mark.parametrize("number,words", LITERARY_WORDS)
def test_literary_cardinal(number, words):
    assert pronounce_number(number, lang="ar") == words


@pytest.mark.parametrize("number,words", [
    (2, "اثنين"), (12, "اثني عشر"), (20, "عشرين"), (22, "اثنين وعشرين"),
    (55, "خمسة وخمسين"), (200, "مئتين"), (2000, "ألفين"),
    (2026, "ألفين وستة وعشرين"),
])
def test_literary_cardinal_in_the_oblique(number, words):
    assert pronounce_number(number, lang="ar", case="oblique") == words


@pytest.mark.parametrize("number,words,case", [
    (1, "واحدة", None), (2, "اثنتان", None), (2, "اثنتين", "oblique"),
    (3, "ثلاث", None), (8, "ثمان", None), (10, "عشر", None),
    (11, "إحدى عشرة", None), (12, "اثنتا عشرة", None),
    (12, "اثنتي عشرة", "oblique"), (13, "ثلاث عشرة", None),
    (18, "ثماني عشرة", None), (23, "ثلاث وعشرون", None),
    (105, "مئة وخمس", None), (1003, "ألف وثلاث", None),
])
def test_literary_cardinal_for_a_feminine_noun(number, words, case):
    assert pronounce_number(number, lang="ar", gender="feminine",
                            case=case) == words


@pytest.mark.parametrize("number,words", [
    pytest.param(12000, "اثنا عشر ألفًا", marks=TAMYIZ_ACCUSATIVE),
    pytest.param(25000, "خمسة وعشرون ألفًا", marks=TAMYIZ_ACCUSATIVE),
])
def test_literary_thousands_after_eleven_to_ninety_nine(number, words):
    spoken = pronounce_number(number, lang="ar")
    assert spoken.split()[-1] in ("ألفًا", "ألفا"), spoken


@pytest.mark.parametrize("number,words", [
    (200000, "مئتا ألف"),
])
def test_literary_dual_hundred_before_a_thousand(number, words):
    assert pronounce_number(number, lang="ar") == words


SAUDI_WORDS = [
    (2, "اثنين"), (3, "ثلاثة"), (10, "عشرة"), (11, "احدعش"), (12, "ثنعش"),
    (13, "ثلاثطعش"), (14, "اربعطعش"), (15, "خمسطعش"), (16, "ستطعش"),
    (17, "سبعطعش"), (18, "ثمانطعش"), (19, "تسعطعش"), (20, "عشرين"),
    (45, "خمسة وأربعين"), (100, "مية"), (115, "مية وخمسطعش"),
    (200, "ميتين"), (250, "ميتين وخمسين"), (300, "ثلاث مية"),
    (400, "اربع مية"), (500, "خمس مية"), (650, "ست مية وخمسين"),
    (700, "سبع مية"), (800, "ثمان مية"), (900, "تسع مية"),
    (1200, "ألف وميتين"), (1500, "ألف وخمس مية"), (2000, "ألفين"),
    (2018, "ألفين وثمانطعش"), (3000, "ثلاثة آلاف"),
    (15000, "خمسطعش ألف"), (13500, "ثلاثطعش ألف وخمس مية"),
    (300000, "ثلاث مية ألف"), (250000, "ميتين وخمسين ألف"),
]


@pytest.mark.parametrize("number,words", SAUDI_WORDS)
def test_saudi_cardinal(number, words):
    assert pronounce_number(number, lang="ars") == words


ORDINAL_WORDS = [
    (1, "الأول", "masculine", None), (2, "الثاني", "masculine", None),
    (3, "الثالث", "masculine", None), (5, "الخامس", "masculine", None),
    (10, "العاشر", "masculine", None), (11, "الحادي عشر", "masculine", None),
    (12, "الثاني عشر", "masculine", None),
    (15, "الخامس عشر", "masculine", None), (20, "العشرون", "masculine", None),
    (21, "الحادي والعشرون", "masculine", None),
    (25, "الخامس والعشرون", "masculine", None),
    (100, "المئة", "masculine", None),
    (1, "الأولى", "feminine", None), (2, "الثانية", "feminine", None),
    (3, "الثالثة", "feminine", None), (11, "الحادية عشرة", "feminine", None),
    (12, "الثانية عشرة", "feminine", None),
    (21, "الحادية والعشرون", "feminine", None),
    (21, "الحادي والعشرين", "masculine", "oblique"),
    (30, "الثلاثين", "masculine", "oblique"),
]


@pytest.mark.parametrize("lang", BOTH)
@pytest.mark.parametrize("number,words,gender,case", ORDINAL_WORDS)
def test_ordinal(lang, number, words, gender, case):
    assert pronounce_ordinal(number, lang=lang, gender=gender,
                             case=case) == words


@pytest.mark.parametrize("number,words", [
    (1, "الأول"), (3, "الثالث"), (11, "الحادي عشر"),
    (25, "الخامس والعشرون"),
])
def test_ordinal_through_pronounce_number(number, words):
    assert pronounce_number(number, lang="ar", ordinals=True) == words


# ---------------------------------------------------------------------------
# extract_number from sentences
# ---------------------------------------------------------------------------

LITERARY_SENTENCES = [
    ("السعر النهائي خمسة وعشرون ألف ريال", 25000),
    ("المبلغ المطلوب ثلاثمئة وخمسون ريالا", 350),
    ("قطعت السيارة مئة وعشرين ألف كيلومتر", 120000),
    ("عداد السيارة يقرأ خمسة وأربعين ألف كيلو", 45000),
    ("ولدت في عام ألف وتسعمئة وخمسة وثمانين", 1985),
    ("نحتاج اثني عشر صندوقا", 12),
    ("عندي ثلاث سيارات في المعرض", 3),
    ("حجزت ثماني تذاكر للرحلة", 8),
    ("الخصم عشرة بالمئة على كل الطلبات", 10),
    ("القسط الشهري ألفان وخمسمئة ريال", 2500),
    ("الضمان لمدة خمس سنوات", 5),
    ("الوزن سبعمئة وخمسون غراما", 750),
    ("حجزنا إحدى عشرة غرفة في الفندق", 11),
    ("الطلب رقم ٤٥٧ جاهز", 457),
    ("السعر ١٢٫٥ ريال للكيلو", 12.5),
    ("الحساب ۱۲۰ ريال", 120),
    ("معدل الاستهلاك سبعة فاصلة خمسة لتر", 7.5),
    ("السعر تسعة وتسعون فاصلة خمسة وتسعون ريالا", 99.95),
    ("درجة الحرارة الليلة سالب خمسة", -5),
    ("رأس المال ثلاثة ملايين ريال", 3000000),
    ("قيمة المشروع مليار ريال", 1000000000),
    ("المبلغ مليون وخمسمئة ألف ريال", 1500000),
    ("يحتوي النص على خمسة أسطر", 5),
    ("قرأت النص كاملا قبل ثلاثة أيام", 3),
    ("توقفنا في نص الطريق مرة واحدة", 1),
    ("الأسعار تبدأ من ٥٠ ألف ريال", 50000),
    ("الفاتورة ألف ومئة وعشرة ريالات", 1110),
    ("عمري ستة وثلاثون عاما", 36),
    ("المسافة اثنان وعشرون كيلومترا", 22),
    ("الإيجار عشرين ألف وخمسمية في السنة", 20500),
    ("التذكرة بمئة وخمسين ريال", 150),
    ("اشتريتها بميتين وخمسين", 250),
    ("التذكرة بتسعمائة ريال", 900),
    ("الكيلو بعشرين", 20),
    ("عندي اربعة أولاد", 4),
    ("المكتب في الطابق إثنا عشر", 12),
    ("السعر خَمْسَةٌ وَعِشْرُونَ ريالًا", 25),
    ("الحساب خمسه وعشرين ريال", 25),
    ("موعدك يوم الاثنين الساعة عشرة", 10),
    ("موعدك الثلاثاء الساعة أربعة", 4),
    ("نفتح يوم الخميس الساعة ثمانية", 8),
    ("يوم الأحد الساعة ثلاثة نكون جاهزين", 3),
    ("ما في أحد في المكتب", False),
    ("الست مريم وصلت المكتب", False),
    ("اشرب مية كثير في الصيف", False),
    ("انتظر ثلاثين ثانية من فضلك", 30),
    ("كل ثانية مهمة في المكالمة", False),
    ("خلال ثانيتين يصلك الرمز", 2),
    ("انتظرت ساعتين في المعرض", 2),
    ("أحتاج ربع ساعة فقط", 0.25),
    ("ثلاثة آلاف وخمسمائة كيلو", 3500),
    ("سبعة عشر ألفا وخمسمئة ريال", 17500),
    ("مدة الإيجار اثنا عشر شهرا", 12),
    ("الدفعة الأولى عشرة آلاف", 10000),
    ("الطابق الثالث فيه عشرون مكتبا", 20),
    ("التمويل مئة بالمئة", 100),
    ("ثلاثمئة وأحد عشر ريالا", 311),
    ("المجموع مئة واثنا عشر ريالا", 112),
    ("المجموع ألف وأحد عشر ريالا", 1011),
    ("الحساب مية وأحد عشر ريال", 111),
    ("دفعت مئتي ريال", 200),
    ("هذه الأرض ثمنها مئتا ألف ريال", 200000),
    ("الميزانية ألفا ريال", 2000),
    ("اشتغلنا بميزانية ألفي ريال", 2000),
    ("رصدنا مليوني ريال للحملة", 2000000),
    ("ثمن السيارة مئة ألف ريال", 100000),
    ("بكم ثمن التذكرة؟ خمسون ريالا", 50),
]


@pytest.mark.parametrize("text,value", LITERARY_SENTENCES)
def test_literary_sentence(text, value):
    assert_value(extract_number(text, lang="ar"), value)


# ألفا with no count before it is the dual in construct, 2,000; written with
# the tanween of the accusative, ألفًا or ألفاً, it is the singular, 1,000.
@pytest.mark.parametrize("text,value", [
    ("الميزانية ألفا ريال", 2000),
    ("قتل ألفاً", 1000),
    ("قتل ألفًا", 1000),
    ("حضر ألفاً وخمسمئة شخص", 1500),
    ("ربح مليوناً في سنة واحدة", 1000000),
    ("سبعة عشر ألفاً وخمسمئة ريال", 17500),
])
def test_alfa_is_the_dual_without_tanween(text, value):
    assert_value(extract_number(text, lang="ar"), value)


# With no counted noun directly after it, ألفا is the accusative singular
# even without tanween, which speech and recognisers never write.
@pytest.mark.parametrize("text,value", [
    ("قتل ألفا", 1000),
    ("دفع ألفا للمحامي", 1000),
    ("دفع ألفا نقدا", 1000),
    ("ربح مليونا في سنة واحدة", 1000000),
    ("خسر مليارا", 1000000000),
    ("حضر ألفا وخمسمئة شخص", 1500),
    ("ألفا", 1000),
    ("قتل ألفا آخرين", 1000),
    ("دفع ألفا كاملة", 1000),
    ("دفع ألفا فقط", 1000),
    ("دفع ألفا بس", 1000),
    ("يدفع ألفا كل شهر", 1000),
    ("خسر مليارا خلال سنة", 1000000000),
    ("دفع ألفا أو أكثر", 1000),
    ("جمع ألفا وزيادة", 1000),
    ("دفع ألفا عند الباب", 1000),
    ("دفع ألفا بالضبط", 1000),
    ("خسر مليارا، ثم ربح", 1000000000),
])
def test_bare_alfa_is_the_singular(text, value):
    assert_value(extract_number(text, lang="ar"), value)


def test_bare_alfa_before_another_number():
    assert extract_numbers_ar("دفع ألفا أو ألفين") == [1000, 2000]


# numbers_to_digits reads ألفا as extraction does: the dual before a unit
# word, the singular anywhere else.
@pytest.mark.parametrize("text,digits", [
    ("الميزانية ألفا ريال", "الميزانية 2000 ريال"),
    ("المبلغ مليون وألفا ريال", "المبلغ 1002000 ريال"),
    ("قتل ألفا آخرين", "قتل 1000 آخرين"),
    ("دفع ألفا أو ألفين", "دفع 1000 أو 2000"),
    ("سبعة عشر ألفا وخمسمئة ريال", "17500 ريال"),
])
def test_alfa_converts_as_it_is_read(text, digits):
    assert numbers_to_digits(text, lang="ar") == digits
    assert extract_number(text, lang="ar") == \
        extract_number(digits, lang="ar")


# A definite ten after a plural noun counts it; only after a singular noun is
# it an ordinal.
@pytest.mark.parametrize("text,value", [
    ("خلال السنوات العشرين الماضية", 20),
    ("في الأعوام الثلاثين الأخيرة", 30),
    ("الدقائق العشرين الأولى كانت صعبة", 20),
    ("الرجال الأربعين", 40),
    ("الكتب الثلاثين", 30),
    ("بالسنوات العشرين", 20),
])
def test_a_definite_ten_after_a_plural_is_a_cardinal(text, value):
    assert_value(extract_number(text, lang="ar"), value)


SAUDI_SENTENCES = [
    ("السعر خمسطعش ألف ريال", 15000),
    ("عطني ثنعش حبة لو سمحت", 12),
    ("الكيلو بثلاثطعش ريال", 13),
    ("قطعت السيارة ميتين ألف كيلو", 200000),
    ("دفعت خمس مية ريال عربون", 500),
    ("المبلغ ثلاث مية وخمسين ريال", 350),
    ("الرحلة تاخذ ساعتين ونص", 2.5),
    ("المسافة ثلاثة ونص كيلو", 3.5),
    ("السعر خمسطعش ونص ريال", 15.5),
    ("الوزن عشرة ونص كيلو", 10.5),
    ("نحتاج اربع وعشرين ونص ساعة", 24.5),
    ("الخصم عشرين بالمية", 20),
    ("رقم الشقة احدعش", 11),
    ("الموعد بعد تسعطعش يوم", 19),
    ("عمره ستطعش سنة", 16),
    ("معاه ثمانطعش ألف ريال", 18000),
    ("الدفعة اربعطعش ألف", 14000),
    ("باقي سبعطعش يوم على الموعد", 17),
    ("السيارة موديل ألفين وثمانطعش", 2018),
    ("الإيجار اربع مية ريال بالأسبوع", 400),
    ("الجهاز بست مية ريال", 600),
    ("الشاشة بسبع مية وخمسين", 750),
    ("التصليح كلفني ثمان مية ريال", 800),
    ("القطعة بتسع مية ريال", 900),
    ("المجموع خمسطعش ألف وخمس مية ريال", 15500),
    ("الحساب ميتين وثنعش ريال", 212),
    ("الشحنة مية وخمسطعش كيلو", 115),
    ("رقم الغرفة خمس مية واحدعش", 511),
    ("رصيدك ثلاثطعش ألف ريال", 13000),
    ("ادفع ألف وميتين وخلاص", 1200),
    ("المسافة مية وعشرين كيلو", 120),
    ("أبي اثنين كيلو", 2),
    ("عندي ثلاثة أسئلة بس", 3),
    ("السعر ٣٥٠ ريال", 350),
    ("رقم الطلب ٧٨٩", 789),
    ("النص فيه عشرين كلمة", 20),
    ("حطيت نص الكمية بس", False),
    ("وقفنا في نص الطريق", False),
    ("قريت ثلاث صفحات ونص الفصل", 3),
    ("أرسلت لك الصور الخمسة ونص العقد", 5),
    ("أجرة الساعة خمسة ونص ريال", 5.5),
    ("الحساب مية وأحد عشر ريال", 111),
]


@pytest.mark.parametrize("text,value", SAUDI_SENTENCES)
def test_saudi_sentence(text, value):
    assert_value(extract_number(text, lang="ars"), value)


SEVERAL_NUMBERS = [
    ("عندي ثلاثة أولاد وخمس بنات", [3, 5]),
    ("من خمسة إلى عشرة أيام", [5, 10]),
    ("من ٥ إلى ١٠ أيام", [5, 10]),
    ("السعر من مئة إلى مئتين ريال", [100, 200]),
    ("بين مئة ومئتين ريال", [100, 200]),
    ("الغرفة رقم عشرة والطابق رقم ثلاثة", [10, 3]),
    ("ثلاثين أو أربعين دقيقة", [30, 40]),
    ("واحد اثنين ثلاثة", [1, 2, 3]),
    ("الرمز خمسة ستة سبعة ثمانية", [5, 6, 7, 8]),
    ("سبعة وثمانية", [7, 8]),
    ("عشرين وثلاثين", [20, 30]),
    ("خذ اثنين وأعطني ثلاثة", [2, 3]),
    ("ساعتين أو ثلاث ساعات", [2, 3]),
    ("من الساعة تسعة إلى الساعة خمسة", [9, 5]),
    ("بين ثلاثطعش وخمسطعش سنة", [13, 15]),
    ("ميتين وخمسين ألف أو ثلاث مية ألف", [250000, 300000]),
]


@pytest.mark.parametrize("lang", BOTH)
@pytest.mark.parametrize("text,values", SEVERAL_NUMBERS)
def test_several_numbers_in_one_sentence(lang, text, values):
    assert extract_numbers_ar(text, lect=lang) == pytest.approx(values)


ORDINAL_SENTENCES = [
    ("شقتي في الطابق الثالث", 3),
    ("الموعد الثاني يوم الأحد", 2),
    ("هذه المرة الأولى التي أتصل فيها", 1),
    ("مكتبنا في الدور الحادي عشر", 11),
    ("ابني في الصف الثاني عشر", 12),
    ("نحتفل بالذكرى الخامسة والعشرين", 25),
    ("نعيش في القرن الحادي والعشرين", 21),
    ("حصل على المركز العاشر", 10),
    ("الدرجة الثانية أرخص", 2),
    ("الموعد الساعة الثانية ظهرا", 2),
    ("هذا الطلب الرابع هذا الشهر", 4),
    ("وصلت الفاتورة السابعة", 7),
    ("الطابق الخامس عشر مغلق", 15),
    ("شاهدت الحلقة العشرين", 20),
    ("الأسبوع الأول من الشهر", 1),
    ("الدفع في اليوم الثلاثين", 30),
    ("انتظر ثانية واحدة", 1),
]


@pytest.mark.parametrize("lang", BOTH)
@pytest.mark.parametrize("text,value", ORDINAL_SENTENCES)
def test_ordinal_sentence(lang, text, value):
    assert_value(extract_number(text, lang=lang, ordinals=True), value)


@pytest.mark.parametrize("lang", BOTH)
@pytest.mark.parametrize("text", [
    "شقتي في الطابق الثالث",
    "الموعد الثاني يوم الأحد",
    "هذه المرة الأولى التي أتصل فيها",
    "مكتبنا في الدور الحادي عشر",
    "نحتفل بالذكرى الخامسة والعشرين",
    "ابني في الصف الثاني عشر",
    "شاهدت الحلقة العشرين",
    "والحلقة العشرين كانت أطول",
])
def test_an_ordinal_is_no_cardinal(lang, text):
    assert extract_number(text, lang=lang) is False


# ---------------------------------------------------------------------------
# numbers_to_digits
# ---------------------------------------------------------------------------

LITERARY_TO_DIGITS = [
    ("السعر خمسة وعشرون ألف ريال", "السعر 25000 ريال"),
    ("رقم الجوال ٠٥٥١٢٣٤٥٦٧", "رقم الجوال 0551234567"),
    ("الرمز ٠٠٧٤", "الرمز 0074"),
    ("موعدك يوم الاثنين الساعة عشرة", "موعدك يوم الاثنين الساعة 10"),
    ("من خمسة إلى عشرة أيام", "من 5 إلى 10 أيام"),
    ("عندي ثلاثة أولاد وخمس بنات", "عندي 3 أولاد و5 بنات"),
    ("قطعت السيارة مئة وعشرين ألف كيلومتر", "قطعت السيارة 120000 كيلومتر"),
    ("ولدت عام ألف وتسعمئة وخمسة وثمانين", "ولدت عام 1985"),
    ("شقتي في الطابق الثالث", "شقتي في الطابق الثالث"),
    ("الموعد الثاني يوم الأحد", "الموعد الثاني يوم الأحد"),
    ("يحتوي النص على خمسة أسطر", "يحتوي النص على 5 أسطر"),
    ("السعر ١٢٫٥ ريال", "السعر 12.5 ريال"),
    ("الخصم عشرة بالمئة", "الخصم 10 بالمئة"),
    ("ثلاثة آلاف وخمسمائة ريال", "3500 ريال"),
    ("التذكرة بمئة وخمسين ريال", "التذكرة ب150 ريال"),
    ("الحساب خمسه وعشرين ريال", "الحساب 25 ريال"),
    ("ما في أحد في المكتب", "ما في أحد في المكتب"),
    ("اشرب مية كثير في الصيف", "اشرب مية كثير في الصيف"),
    ("الست مريم وصلت المكتب", "الست مريم وصلت المكتب"),
    ("بين مئة ومئتين ريال", "بين 100 و200 ريال"),
    ("ثلاثين أو أربعين دقيقة", "30 أو 40 دقيقة"),
    ("الطلب رقم ٤٥٧ جاهز", "الطلب رقم 457 جاهز"),
    ("المبلغ مليون وخمسمئة ألف ريال", "المبلغ 1500000 ريال"),
    ("الرمز خمسة ستة سبعة ثمانية", "الرمز 5 6 7 8"),
    ("الإجازة خمسة عشر يوما", "الإجازة 15 يوما"),
    ("اشتريت ثلاثة عشر كتابا", "اشتريت 13 كتابا"),
    ("الدفعة الأولى عشرة آلاف", "الدفعة الأولى 10000"),
    ("مدة الإيجار اثنا عشر شهرا", "مدة الإيجار 12 شهرا"),
    ("حجزنا إحدى عشرة غرفة", "حجزنا 11 غرفة"),
    ("في المعرض اثنتا عشرة سيارة", "في المعرض 12 سيارة"),
    ("المجموع مئة واثنا عشر ريالا", "المجموع 112 ريالا"),
    ("قطعت أحد عشر ألف كيلو", "قطعت 11000 كيلو"),
    ("الحساب مية وأحد عشر ريال", "الحساب 111 ريال"),
    ("مكتبنا في الدور الحادي عشر", "مكتبنا في الدور الحادي عشر"),
    ("نحتفل بالذكرى الخامسة والعشرين",
     "نحتفل بالذكرى الخامسة والعشرين"),
    ("دفعت مئتي ريال", "دفعت 200 ريال"),
    ("المبلغ مليون ومئتا ألف ريال", "المبلغ 1200000 ريال"),
]


@pytest.mark.parametrize("text,digits", LITERARY_TO_DIGITS)
def test_literary_to_digits(text, digits):
    assert numbers_to_digits(text, lang="ar") == digits


@pytest.mark.parametrize("lang", BOTH)
@pytest.mark.parametrize("text,kept", [
    ("انتظرت ساعتين في المعرض",
     {"انتظرت ساعتين في المعرض", "انتظرت 2 ساعة في المعرض",
      "انتظرت 2 ساعات في المعرض"}),
    ("قرأت النص مرتين",
     {"قرأت النص مرتين", "قرأت النص 2 مرة", "قرأت النص 2 مرات"}),
])
def test_a_dual_noun_keeps_its_noun(lang, text, kept):
    """The dual may stay as written or become 2 before its noun, singular
    or plural, but the noun it counts stays."""
    assert numbers_to_digits(text, lang=lang) in kept


SAUDI_TO_DIGITS = [
    ("السعر خمسطعش ألف ريال", "السعر 15000 ريال"),
    ("دفعت ثلاث مية وخمسين ريال", "دفعت 350 ريال"),
    ("قطعت ميتين ألف كيلو", "قطعت 200000 كيلو"),
    ("السيارة موديل ألفين وثمانطعش", "السيارة موديل 2018"),
    ("وقفنا في نص الطريق", "وقفنا في نص الطريق"),
    ("النص فيه عشرين كلمة", "النص فيه 20 كلمة"),
    ("عطني ثنعش حبة", "عطني 12 حبة"),
    ("الكيلو بثلاثطعش ريال", "الكيلو ب13 ريال"),
    ("الوزن عشرة ونص كيلو", "الوزن 10.5 كيلو"),
    ("رقم الجوال ٠٥٠١٢٣٤٥٦٧", "رقم الجوال 0501234567"),
    ("الإيجار اربع مية ريال", "الإيجار 400 ريال"),
    ("الجهاز بست مية ريال", "الجهاز ب600 ريال"),
    ("المجموع خمسطعش ألف وخمس مية ريال", "المجموع 15500 ريال"),
    ("الحساب ميتين وثنعش ريال", "الحساب 212 ريال"),
    ("رقم الغرفة خمس مية واحدعش", "رقم الغرفة 511"),
    ("باقي سبعطعش يوم", "باقي 17 يوم"),
    ("عمره ستطعش سنة", "عمره 16 سنة"),
    ("قريت ثلاث صفحات ونص الفصل", "قريت 3 صفحات ونص الفصل"),
    ("حطيت نص الكمية بس", "حطيت نص الكمية بس"),
    ("خمسة ونص ريال وسبعة ريال", "5.5 ريال و7 ريال"),
    ("بين ثلاثطعش وخمسطعش سنة", "بين 13 و15 سنة"),
    ("أجرة الساعة خمسة ونص ريال", "أجرة الساعة 5.5 ريال"),
    ("الحساب مية وأحد عشر ريال", "الحساب 111 ريال"),
]


@pytest.mark.parametrize("text,digits", SAUDI_TO_DIGITS)
def test_saudi_to_digits(text, digits):
    assert numbers_to_digits(text, lang="ars") == digits


@pytest.mark.parametrize("lang", BOTH)
@pytest.mark.parametrize("text", ["تعال الساعة ثلاثة ونص",
                                  "موعدك الساعة ثلاثة ونص"])
def test_a_clock_time_is_no_decimal(lang, text):
    assert "3.5" not in numbers_to_digits(text, lang=lang)


# A half after a hundred or a thousand is not read. Whatever it is read as,
# it is never the hundred or the thousand plus 0.5.
HALF_AFTER_A_ROUND_NUMBER = [
    ("الحساب مية ونص", 100.5, "ars"),
    ("السعر الف ونص", 1000.5, "ars"),
    ("المبلغ حوالي مليون ونصف", 1000000.5, "ar"),
    ("تكلفة التصليح ألف ونصف", 1000.5, "ar"),
    ("رصيدك ثلاثة آلاف ونصف", 3000.5, "ar"),
]


@pytest.mark.parametrize("text,wrong,lang", HALF_AFTER_A_ROUND_NUMBER)
def test_a_half_after_a_round_number_never_adds_one_half(text, wrong, lang):
    assert wrong not in extract_numbers_ar(text, lect=lang)


@pytest.mark.parametrize("text,wrong,lang", HALF_AFTER_A_ROUND_NUMBER)
def test_a_half_after_a_round_number_never_converts_to_one_half(text, wrong,
                                                                 lang):
    assert str(wrong) not in numbers_to_digits(text, lang=lang)


# ---------------------------------------------------------------------------
# round trips: what the library says, it reads back
# ---------------------------------------------------------------------------

ROUND_TRIP_VALUES = [7, 12, 15, 19, 25, 99, 100, 111, 115, 150, 200, 212,
                     250, 300, 350, 999, 1200, 1500, 2018, 2026, 13500,
                     45000, 120000, 250000, 1000000, 2500000]

VOICES = [
    ("ar", {}),
    ("ar", {"case": "oblique"}),
    ("ar", {"gender": "feminine"}),
    ("ars", {}),
    ("ars", {"gender": "feminine"}),
]


@pytest.mark.parametrize("lang,options", VOICES,
                         ids=["ar", "ar-oblique", "ar-feminine", "ars",
                              "ars-feminine"])
@pytest.mark.parametrize("number", ROUND_TRIP_VALUES)
def test_said_in_a_sentence_reads_back(lang, options, number):
    spoken = pronounce_number(number, lang=lang, **options)
    assert extract_number(f"المبلغ {spoken} ريال", lang=lang) == number, spoken


@pytest.mark.parametrize("lang,number", [
    ("ars", 111000),
    ("ars", 211000),
    ("ar", 111000), ("ar", 211000), ("ars", 311000),
])
def test_feminine_above_ten_thousand_reads_back(lang, number):
    spoken = pronounce_number(number, lang=lang, gender="feminine")
    assert extract_number(spoken, lang=lang) == number, spoken


@pytest.mark.parametrize("lang", BOTH)
@pytest.mark.parametrize("number", ROUND_TRIP_VALUES)
def test_said_converts_to_its_digits(lang, number):
    spoken = pronounce_number(number, lang=lang)
    assert numbers_to_digits(f"المبلغ {spoken} ريال", lang=lang) == \
        f"المبلغ {number} ريال"


@pytest.mark.parametrize("lang", BOTH)
@pytest.mark.parametrize("gender", ["masculine", "feminine"])
@pytest.mark.parametrize("number", [1, 2, 3, 5, 8, 10, 11, 12, 13, 19, 20,
                                    21, 25, 30, 47, 99])
def test_ordinal_reads_back(lang, gender, number):
    spoken = pronounce_ordinal(number, lang=lang, gender=gender)
    assert extract_number(f"رقمك {spoken} في القائمة", lang=lang,
                          ordinals=True) == number, spoken

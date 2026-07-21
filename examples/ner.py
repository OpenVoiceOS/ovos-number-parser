"""NER: pull numeric entities out of free text.

`extract_number` finds a number in a span of text; `is_fractional` and
`is_ordinal` classify single tokens. Combine them with a tokenizer to tag the
numeric mentions in a document -- no ML model, no OVOS stack required:

    pip install ovos-number-parser
    python ner.py
"""
from ovos_number_parser import extract_number, is_fractional, is_ordinal

TEXT = (
    "The order shipped in three boxes weighing twelve kilos, "
    "the second box was late, and a quarter of the items were damaged."
)

# --- Sliding window: tag the numeric mention in each clause ----------------
print("Per-clause numeric entities:")
for clause in TEXT.split(","):
    clause = clause.strip()
    value = extract_number(clause, "en")
    if value is not False:
        print(f"  NUM  {value!s:6} <- {clause!r}")

# --- Token-level classification -------------------------------------------
print("\nToken classification:")
for token in ["three", "second", "quarter", "twelve", "damaged"]:
    frac = is_fractional(token, "en")
    ordn = is_ordinal(token, "en")
    card = extract_number(token, "en")
    if ordn is not False:
        print(f"  {token:10} ORDINAL   -> {ordn}")
    elif frac is not False:
        print(f"  {token:10} FRACTION  -> {frac}")
    elif card is not False:
        print(f"  {token:10} CARDINAL  -> {card}")
    else:
        print(f"  {token:10} (not numeric)")

# Expected output (verified):
# Per-clause numeric entities (extract_number reads cardinals; "second" is an
# ordinal, so that clause is classified at the token level below instead):
#   NUM  3      <- 'The order shipped in three boxes weighing twelve kilos'
#   NUM  0.25   <- 'and a quarter of the items were damaged.'
#
# Token classification:
#   three      CARDINAL  -> 3
#   second     ORDINAL   -> 2
#   quarter    FRACTION  -> 0.25
#   twelve     CARDINAL  -> 12
#   damaged    (not numeric)

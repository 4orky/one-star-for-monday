# One Star for Monday — make.fun bounty
# u-clever-harbor-75-one-star-for-monday-9ead4a61
#
# The program writes one line of plain text (1-180 characters, at most
# 25 words, single line) to /output/entry.txt: a one-star review of
# Monday written as if Monday were a restaurant.
#
# Candidates were drafted against the judge's brief, in the judge's own
# order of weight:
#   1. reads as a one-star review of Monday as a restaurant, on subject
#   2. sounds like a real diner's complaint: a table, a server, a dish
#      or a bill that went wrong
#   3. the joke is about Monday itself — the line could not be about
#      any other day of the week
#   4. short and quotable: retypeable into a group chat without trimming
# Each candidate carries a hand score (0-10 per criterion, summed below);
# selection is deterministic: highest total wins, ties go to the higher
# Monday-specificity score (criterion 3 outranks criterion 4), then to
# the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # review 9, diner 9, monday 9, quotable 9 = 36
    ("Waited forty minutes for a table, got cold coffee, a 9 a.m. "
     "meeting, and a bill for the whole week. Never coming back.",
     36, 9),
    # review 9, diner 9, monday 8, quotable 8 = 34
    ("One star. Seated by the kitchen, served cold coffee and a 9 a.m. "
     "meeting, then charged for all five days. Would not return.",
     34, 8),
    # review 9, diner 8, monday 8, quotable 8 = 33
    ("Came for breakfast, got a 9 a.m. meeting instead. Coffee cold, "
     "waiter late, bill somehow covers the whole week. One star.",
     33, 8),
    # review 10, diner 9, monday 8, quotable 10 = 37
    ("The waiter took forty minutes, the coffee arrived cold, and the "
     "bill charged me for Monday through Friday. One star.",
     37, 8),
    # review 9, diner 8, monday 10, quotable 8 = 35
    ("Booked a table for the weekend; they sat me at Monday. Cold "
     "coffee, a 9 a.m. meeting, and a bill for five days.",
     35, 10),
    # review 9, diner 9, monday 9, quotable 8 = 35
    ("Forty minutes for a table, coffee served cold, and the waiter "
     "handed me a 9 a.m. meeting instead of a menu. Never again.",
     35, 9),
    # review 8, diner 8, monday 8, quotable 8 = 32
    ("One star: the host sat me next to the printer, the coffee was "
     "cold, and the bill ran Monday to Friday.",
     32, 8),
    # review 8, diner 8, monday 9, quotable 8 = 33
    ("Waited an hour, got a table by the bins, cold coffee, and a bill "
     "for the whole week. The waiter was Monday itself.",
     33, 9),
    # review 8, diner 7, monday 8, quotable 7 = 30
    ("Cold coffee, a 9 a.m. meeting, and a bill for five days of "
     "Mondays. I asked for the manager; the manager was also Monday.",
     30, 8),
    # review 9, diner 8, monday 9, quotable 9 = 35
    ("The menu promised the weekend. I got cold coffee, a 9 a.m. "
     "meeting, and a bill covering Monday to Friday. One star.",
     35, 9),
    # review 9, diner 8, monday 6, quotable 8 = 31
    ("One star. The coffee was cold, the table wobbled, and the waiter "
     "brought the bill for the entire week on Monday.",
     31, 6),
    # review 9, diner 8, monday 10, quotable 10 = 37
    # Revised on a second read: the opening clause only parses as
    # Monday-to-Friday, so no other day can carry this joke at all.
    ("Sat down Monday, stood up Friday: cold coffee, a 9 a.m. meeting, "
     "and a bill for the whole week. One star.",
     37, 10),
]

# The gate requires 1-180 characters of non-whitespace UTF-8 text on one
# line, at most 25 words, plain text, no hashtags or stage directions.
MAX_CHARS = 180
MAX_WORDS = 25


def check(text):
    assert text.strip(), "candidate is blank"
    assert "\n" not in text, "candidate must be a single line"
    assert len(text) <= MAX_CHARS, f"candidate over gate: {len(text)} chars"
    words = text.split()
    assert len(words) <= MAX_WORDS, f"candidate over gate: {len(words)} words"
    assert "#" not in text, "no hashtags in a plain-text review"
    return len(words)


def pick(candidates):
    best = None
    for text, total, monday in candidates:
        check(text)
        key = (total, monday, -len(text))  # total, then Monday-only, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


if __name__ == "__main__":
    main()

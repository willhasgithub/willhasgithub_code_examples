"""
These challenges are found at edabit.com. I'll sometimes do these for fun.
While I have not maintained a public repository, and much of my past code is for work:
These challenges may help show how I work though problems.

I will add the links to the challenges for each.
Challenges are ordered by difficulty level (descending).
"""
import datetime
import re


# LINK: https://edabit.com/challenge/Xkc2iAjwCap2z9N5D
# TITLE: Friday the 13th
# EX: has_friday_13(3, 2020) --> true
def has_friday_13(month, year):
    month0 = month % 12
    year0 = year + int(month / 12)
    return datetime.date(year0, month0, 13).weekday() == 4


# LINK: https://edabit.com/challenge/KQ5H9aFBZDKEJuP6C
# TITLE: RegEx VII-A: Negative Lookbehind
# EX: lst = ["bad cookie", "good cookie", "bad cookie", "good cookie", "good cookie"]
def count_num_bad_cookies(cookies_list):
    my_pattern = r"(([a - z] +)(?<!good)(\scookie)(, \s)?)"
    return len(re.findall(my_pattern, ", ".join(cookies_list)))


# LINK: https://edabit.com/challenge/5bYXQfpyoithnQisa
# TITLE: Encode Morse
# EX: encode_morse("EDABBIT CHALLENGE") ➞ ". -.. .- -... -... .. -   -.-. .... .- .-.. .-.. . -. --. ."
def encode_morse(message):
    char_to_dots = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', ' ': ' ', '0': '-----',
        '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
        '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '&': '.-...', "'": '.----.', '@': '.--.-.', ')': '-.--.-', '(': '-.--.',
        ':': '---...', ',': '--..--', '=': '-...-', '!': '-.-.--', '.': '.-.-.-',
        '-': '-....-', '+': '.-.-.', '"': '.-..-.', '?': '..--..', '/': '-..-.'
    }
    dotables = char_to_dots.keys()

    dotted = []
    for char in message.upper():
        if char in dotables:
            char = char_to_dots[char]
        dotted.append(char)

    return ' '.join(dotted)


# LINK: https://edabit.com/challenge/xbjDMxzpFcsAWKp97
# TITLE: Concert Seats
# EX:
# Create a function that determines whether each seat can "see" the front-stage.
# A number can "see" the front-stage if it is strictly greater than the number before it.
# FRONT STAGE
# [[1, 2, 3, 2, 1, 1],
# [2, 4, 4, 3, 2, 2],
# [5, 5, 5, 10, 4, 4],
# [6, 6, 7, 6, 5, 5]]
# The 10 is directly in front of the 6 and blocking its view.
# can_see_stage([
#   [1, 2, 3],
#   [4, 5, 6],
#   [7, 8, 9]
# ]) ➞ True
def can_see_stage(seats):
    can_see = True
    for i in range(len(seats)):
        if i > 0:
            for j in range(len(seats[i])):
                if seats[i][j] <= seats[i - 1][j]:
                    can_see = False
    return can_see


# LINK: https://edabit.com/challenge/Fpymv2HieqEd7ptAq
# TITLE: Parentheses Clusters
# EX:
# split("()()()") ➞ ["()", "()", "()"]
# split("((()))") ➞ ["((()))"]
# split("((()))(())()()(()())") ➞ ["((()))", "(())", "()", "()", "(()())"]
# split("((())())(()(()()))") ➞ ["((())())", "(()(()()))"]
def split_parentheses(txt):
    balanced_parentheses = []
    last_split = 0

    for i in range(1, len(txt) + 1):
        if txt[last_split:i].count('(') - txt[last_split:i].count(')') == 0:
            balanced_parentheses.append(txt[last_split:i])
            last_split = i

    return balanced_parentheses


# LINK: https://edabit.com/challenge/K9MuSPs9W4zCJq6EM
# TITLE: Length of Sorting Cycle
# EX:
# [1, 9, 8, 4, 7, 2, 6, 3, 5]
# [1, 5, 8, 4, 7, 2, 6, 3, 9] # 9 swaps with 5; 9 is in its correct spot.
# [1, 7, 8, 4, 5, 2, 6, 3, 9] # 5 replaces 7; 5 is in its correct spot.
# [1, 6, 8, 4, 5, 2, 7, 3, 9] # 7 replaces 6; 7 is in its correct spot.
# [1, 2, 8, 4, 5, 6, 7, 3, 9] # 6 replaces 2; 6 is in its correct spot and 2 is in it's correct spot - done!
def cycle_length(lst, n):
    num_swaps = 0

    list_copied = lst.copy()
    list_sorted = lst.copy()
    list_sorted.sort()

    if list_copied.index(n) != list_sorted.index(n):
        focus_num = list_copied[list_sorted.index(n)]
        while focus_num != n:
            focus_num = list_copied[list_sorted.index(focus_num)]
            num_swaps += 1

    return num_swaps


# LINK: https://edabit.com/challenge/XQwPPHE6ZSu4Er9ht
# TITLE: Economical Numbers
# EX:
# is_economical(14) ➞ "Equidigital"
# The prime factorization of 14 (2 digits) is [2, 7] (2 digits)
# Exponents equal to 1 are not counted
#
# is_economical(125) ➞ "Frugal"
# The prime factorization of 125 (3 digits) is [5^3] (2 digits)
# Notice how exponents greater than 1 are counted
#
# is_economical(1024) ➞ "Frugal"
# The prime factorization of 1024 (4 digits) is [2^10] (3 digits)
#
# is_economical(30) ➞ "Wasteful"
# The prime factorization of 30 (2 digits) is [2, 3, 5] (3 digits)
def get_prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def scientific_notation_factors(factor_list):
    unique_factors = set(factor_list)
    num_occurance_factors = {factor: factor_list.count(factor) for factor in unique_factors}

    factor_list_short = []
    for factor, num_occurences in num_occurance_factors.items():
        if num_occurences > 1:
            factor_list_short.append(''.join([str(factor), '^', str(num_occurences)]))
        else:
            factor_list_short.append(str(factor))
    return factor_list_short


def is_economical(n):
    answers = ['Frugal', 'Equidigital', 'Wasteful']

    factors = get_prime_factors(n)
    factor_list_short = scientific_notation_factors(factors)

    num_digits_n = len(str(n))
    num_digits_factors = len(''.join(factor.replace('^', '') for factor in factor_list_short))

    difference = num_digits_factors - num_digits_n
    if difference < 0:
        return answers[0]
    elif difference == 0:
        return answers[1]
    else:
        return answers[2]


# LINK: https://edabit.com/challenge/RB6iWFrCd6rXWH3vi
# TITLE: Longest Alternating Substring
# EX:
# longest_substring("225424272163254474441338664823") ➞ "272163254"
# substrings = 254, 272163254, 474, 41, 38, 23
#
# longest_substring("594127169973391692147228678476") ➞ "16921472"
# substrings = 94127, 169, 16921472, 678, 476
#
# longest_substring("721449827599186159274227324466") ➞ "7214"
# substrings = 7214, 498, 27, 18, 61, 9274, 27, 32
# 7214 and 9274 have same length, but 7214 occurs first.
def get_longest_substring(digits):
    substrings = []

    previous_digit = digits[0]
    previous_digit_is_odd = (int(previous_digit) % 2) > 0
    substring = [previous_digit]
    for i in range(1, len(digits)):
        current_digit = digits[i]
        current_digit_is_odd = (int(current_digit) % 2) > 0
        alternated = previous_digit_is_odd != current_digit_is_odd
        if alternated:
            substring.append(current_digit)
        else:
            substrings.append(''.join(substring))
            substring = [current_digit]

        previous_digit = current_digit
        previous_digit_is_odd = (int(previous_digit) % 2) > 0

    substrings.append(''.join(substring))

    substring_lengths = [len(sbstrng) for sbstrng in substrings]
    length_longest = max(substring_lengths)

    return substrings[substring_lengths.index(length_longest)]


# LINK: https://edabit.com/challenge/4AjWvJdZpFEMbGALd
# TITLE: Josephus Permutation
# EX:
# who_goes_free(9, 2) ➞ 2
#
# Prisoners = [0, 1, 2, 3, 4, 5, 6, 7, 8]
# Executed people replaced by - (a dash) for illustration purposes.
# 1st round of execution = [0, -, 2, -, 4, -, 6, -, 8]  -> [0, 2, 4, 6, 8]
# 2nd round = [-, 2, -, 6, -] -> [2, 6]  # 0 is killed in this round because it's beside 8 who was skipped over.
# 3rd round = [2, -]
def who_goes_free(n, k):
    prisoners = [p for p in range(n)]

    skipped = 0
    while len(prisoners) > 1:
        prisoners_copy = prisoners.copy()
        for i in range(len(prisoners_copy)):
            if skipped >= (k - 1):
                prisoners_copy[i] = '-'
                skipped = 0
            else:
                skipped += 1
        prisoners = [prisoner for prisoner in prisoners_copy if prisoner != '-']

    return prisoners[0]


# LINK: https://edabit.com/challenge/BfSj2nBc33aCQrbSg
# TITLE: Truncatable Primes
# EX:
# truncatable(9137) ➞ "left"
# Because 9137, 137, 37 and 7 are all prime.
#
# truncatable(5939) ➞ "right"
# Because 5939, 593, 59 and 5 are all prime.
#
# truncatable(317) ➞ "both"
# Because 317, 17 and 7 are all prime and 317, 31 and 3 are all prime.
#
# truncatable(5) ➞ "both"
# The trivial case of single-digit primes is treated as truncatable from both directions.
#
# truncatable(139) ➞ False
# 1 and 9 are non-prime, so 139 cannot be truncatable from either direction.
#
# truncatable(103) ➞ False
# Because it contains a 0 digit (even though 103 and 3 are primes).
def check_prime(num):
    # If given number is greater than 1
    if num > 1:
        # Iterate from 2 to n / 2
        for i in range(2, num):
            # If num is divisible by any number between
            # 2 and n / 2, it is not prime
            if (num % i) == 0:
                return False
        else:
            return True
    else:
        return False


def check_primes(num, direction=0):
    checks = []

    while len(str(num)) > 1:
        print(num)
        checks.append(check_prime(num))
        # defaults right
        num = int(str(num)[1:]) if direction < 0 else int(str(num)[:-1])
    checks.append(check_prime(num))
    return all(checks)


def truncatable(n):
    if any([char == '0' for char in str(n)]):
        return False
    else:
        is_left = check_primes(n, direction=-1)
        is_right = check_primes(n, direction=1)
        if all([is_left, is_right]):
            return 'both'
        else:
            if not any([is_left, is_right]):
                return False
            else:
                if is_left:
                    return 'left'
                else:
                    return 'right'


# For testing targeted challenge
if __name__ == "__main__":
    print(truncatable(7331))

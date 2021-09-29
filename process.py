attributes = [
    ['', 'sunny', 'overcast', 'rainy'],
    ['', 'hot', 'mild', 'cool'],
    ['', 'high', 'normal'],
    ['', 'TRUE', 'FALSE'],
]

DATA_RULES = """sunny,hot,high,FALSE,no
sunny,hot,high,TRUE,no
overcast,hot,high,FALSE,yes
rainy,mild,high,FALSE,yes
rainy,cool,normal,FALSE,yes
rainy,cool,normal,TRUE,no
overcast,cool,normal,TRUE,yes
sunny,mild,high,FALSE,no
sunny,cool,normal,FALSE,yes
rainy,mild,normal,FALSE,yes
sunny,mild,normal,TRUE,yes
overcast,mild,high,TRUE,yes
overcast,hot,normal,FALSE,yes
rainy,mild,high,TRUE,no"""

"""
if sunny and humidity = high => play = no
if rainy and windy = true => play = no
if overcast => play = yes
if humidity = normal => play = yes
if none of the above => play = yes
"""

"""
supp 
r = pocet, kolikrat se dane atributy (i v kombinaci) nachazi v celkove sade
N = pocty pravidel v datasetu

conf
cmax = pocet prevazujici vetsiny (spravne, spatne) kombinaci atributu (=pravidlo), porovnat vuci DATA_RULES
r = 

"""


def gen_data(w_data: list, start: int, end: int, row: list) -> None:
    for x in attributes[start]:
        if start == end:
            w_data.append(row + [x])
        else:
            gen_data(w_data, start + 1, end, row + [x])


def calc_r(curr: int, rules: list) -> int:
    r = 0
    current_attrs = [x for x in rules[curr] if x]
    for i in range(len(rules)):
        is_same = all(item in rules[i] for item in current_attrs)
        r += 1 if is_same else 0
    return r


def get_cmax(rule: list) -> int:
    cyes = 0
    cno = 0
    rule_attrs = [attr for attr in rule if attr]
    for d_rule in DATA_RULES:
        matches = all(item in d_rule for item in rule_attrs)
        if matches:
            if d_rule[-1] == 'yes':
                cyes += 1
            else:
                cno += 1
        pass

    return max(cyes, cno)


def process():
    w_data = []

    gen_data(w_data, 0, len(attributes) - 1, [])
    n = len(w_data)
    for i, rule in enumerate(w_data):
        r = calc_r(i, w_data)
        cmax = get_cmax(rule)
        print(f'{i + 1}: {rule}, supp: {r / n}, conf: {cmax / r}')

    # subvalues = [item in w_data[10] for item in w_data[12] if item]
    # print(subvalues)
    # print(all(subvalues))

    pass


if __name__ == '__main__':
    DATA_RULES = DATA_RULES.split('\n')
    DATA_RULES = [rule.split(',') for rule in DATA_RULES]
    process()

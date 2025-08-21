import inspect
from math import isnan

from abydos import phonetic
from abydos import distance

a = 'al dhale"e /'
b = "ad dali"
c = "al bayda"

d = "Luganskaja Oblast".lower()
e = "Luhanska".lower()
f = "Lvivska".lower()

g = "Bas congo".lower()
h = "Kongo Central".lower()
i = "Bas Uele".lower()

j = "B MOUHOUN".lower()
k = "Boucle du Mouhoun".lower()
l = "Sud Ouest".lower()


def get_sims(diffs, name, measure, val1, val2, val3):
    output = name.ljust(24)
    try:
        sim1 = measure.sim(val1, val2)
    except (NotImplementedError, ValueError, RecursionError, AttributeError):
        return
    sim2 = measure.sim(val1, val3)
    if sim2 >= sim1:  # First pair should be more similar than second
        return
    if isnan(sim1) or isnan(sim2):
        return
    diff = sim1 - sim2
    diffs.append((diff, output, sim1, sim2))


diffs1 = []
diffs2 = []
diffs3 = []
diffs4 = []

for measure_name, obj in inspect.getmembers(phonetic):
    if not measure_name[0].isupper():
        continue
    pd = distance.PhoneticDistance(transforms=obj(), metric=distance.Levenshtein)
    get_sims(diffs1, measure_name, pd, a, b, c)
    get_sims(diffs2, measure_name, pd, d, e, f)
    get_sims(diffs3, measure_name, pd, g, h, i)
    get_sims(diffs4, measure_name, pd, j, k, l)

for measure_name, obj in inspect.getmembers(distance):
    if not measure_name[0].isupper():
        continue
    get_sims(diffs1, measure_name, obj(), a, b, c)
    get_sims(diffs2, measure_name, obj(), d, e, f)
    get_sims(diffs3, measure_name, obj(), g, h, i)
    get_sims(diffs4, measure_name, obj(), j, k, l)


def output_diffs(diffs):
    for result in sorted(diffs, reverse=True):
        diff, output, sim1, sim2 = result
        print(f"{output}\t{sim1:.4f} - {sim2:.4f} = {diff:.4f}")


print(f"Comparing {a} and {b}, {a} and {c}")
output_diffs(diffs1)
print(f"\nComparing {d} and {e}, {d} and {f}")
output_diffs(diffs2)
print(f"\nComparing {g} and {h}, {g} and {i}")
output_diffs(diffs3)
print(f"\nComparing {j} and {k}, {j} and {l}")
output_diffs(diffs4)
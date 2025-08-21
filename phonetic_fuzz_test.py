import inspect

from rapidfuzz import fuzz

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
    sim1 = measure(val1, val2)
    sim2 = measure(val1, val3)
    if not isinstance(sim1, float):
        sim1 = sim1.score
        sim2 = sim2.score
    diff = sim1 - sim2
    diffs.append((diff, output, sim1, sim2))


diffs1 = []
diffs2 = []
diffs3 = []
diffs4 = []

for measure_name, measure in inspect.getmembers(fuzz):
    if not measure_name[0].islower():
        continue
    if not callable(measure):
        continue
    get_sims(diffs1, measure_name, measure, a, b, c)
    get_sims(diffs2, measure_name, measure, d, e, f)
    get_sims(diffs3, measure_name, measure, g, h, i)
    get_sims(diffs4, measure_name, measure, j, k, l)

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
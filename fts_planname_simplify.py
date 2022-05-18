import re

from hdx.utilities.text import multiple_replace


def any_index(string_to_search, strings_to_try):
    for string in strings_to_try:
        try:
            index = string_to_search.index(string)
            return index
        except ValueError:
            pass
    return None


def map_planname(origname):
    name = None
    origname_simplified = origname.replace("  ", " ")
    origname_simplified = re.sub(r"\d\d\d\d(-\d\d\d\d)?", "", origname_simplified)  # strip date
    origname_simplified = re.sub(r"[\(\[].*?[\)\]]", "", origname_simplified)  # strip stuff in brackets
    origname_simplified = origname_simplified.strip()
    origname_lower = origname_simplified.lower()
    regional_strings = ["regional", "refugee", "migrant"]
    if any(x in origname_lower for x in regional_strings):
        location = None
        try:
            for_index = origname_lower.index(" for ")
            location = origname_simplified[for_index+5:]
            location = location.replace("the", "").strip()
        except ValueError:
            non_location_index = any_index(origname_lower, regional_strings)
            if non_location_index:
                location = origname_simplified[:non_location_index-1]
        if location:
            name = f"{location} Regional"
    if not name:
        name = multiple_replace(origname_simplified, {"Plan": "", "Intersectoral": "", "Joint": ""})
        name = name.strip()
    #
    # if "Refugee" in origname:
    #     words = origname.split(" ")
    #     try:
    #         index = words.index("Regional")
    #         name = " ".join(words[: index + 1])
    #     except ValueError:
    #         try:
    #             index = words.index("from")
    #             newwords = list()
    #             for word in words[index + 1 :]:
    #                 if "(" in word:
    #                     break
    #                 newwords.append(word)
    #             name = f"{' '.join(newwords)} Regional"
    #         except ValueError:
    #             index = words.index("Refugee")
    #             name = f"{' '.join(words[:index])} Regional"
    # if not name:
    #     name = re.sub(r"[\(\[].*?[\)\]]", "", origname)
    #     name = multiple_replace(
    #         name, {"Intersectoral": "", "Response": "", "Plan": "", "Joint": ""}
    #     )
    #     name = " ".join(name.split())
    if origname == name:
        print(f'Plan name "{name}" not simplified')
    else:
        print(f'Plan name "{name}" simplified from "{origname}"')
    return name


if __name__ == '__main__':
    map_planname("Syria Refugee Response and Resilience Plan (3RP) 2021")
    map_planname("Burundi Regional Refugee Response Plan 2021")
    map_planname("Bangladesh: Rohingya Refugee Crisis Joint Response Plan 2021")
    map_planname("Escalation of Hostilities in the oPt  Flash Appeal 2021")
    map_planname("Refugee and Migrant Response Plan for Venezuela 2021 (RMRP)")
    map_planname("Regional Migrant Humanitarian Response Plan for the Horn of Africa and Yemen 2021")
    map_planname("Democratic Republic of Congo Regional Refugee Response Plan 2021")
    map_planname("South Sudan Regional Refugee Response Plan 2021")
    map_planname("Lebanon Emergency Response Plan 2021")
    map_planname("Myanmar Interim Emergency Response Plan 2021")
    map_planname("Northern Ethiopia Response Plan 2021")
    map_planname("Haiti Flash Appeal")
    map_planname("Afghanistan Flash Appeal 2021")
    map_planname("Kenya Drought Flash Appeal 2021")
    map_planname("Honduras Flash Appeal 2020-2021")
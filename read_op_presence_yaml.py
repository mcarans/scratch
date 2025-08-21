from hdx.utilities.loader import load_yaml

path = "../hapi-pipelines/src/hapi/pipelines/configs/operational_presence.yaml"

data = load_yaml(path)
output = {}
for item, dataset in data["operational_presence_national"].items():
    iso3 = item[-3:].upper()
    country_output = output.get(iso3, {})
    country_output["dataset"] = dataset["dataset"]
    country_output["resource"] = dataset["resource"]
    country_output["adm"] = 0
    output[iso3] = country_output

for item, dataset in data["operational_presence_adminone"].items():
    iso3 = item[-3:].upper()
    country_output = output.get(iso3, {})
    country_output["dataset"] = dataset["dataset"]
    country_output["resource"] = dataset["resource"]
    country_output["adm"] = 1
    output[iso3] = country_output

for item, dataset in data["operational_presence_admintwo"].items():
    iso3 = item[-3:].upper()
    country_output = output.get(iso3, {})
    country_output["dataset"] = dataset["dataset"]
    country_output["resource"] = dataset["resource"]
    country_output["adm"] = 2
    output[iso3] = country_output

for iso3 in sorted(output):
    country_data = output[iso3]
    dataset = country_data["dataset"]
    resource = country_data["resource"]
    adm = country_data["adm"]
    print(f"{iso3},{dataset},{resource},{adm}")

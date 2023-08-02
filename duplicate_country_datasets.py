from os.path import join, expanduser

from hdx.data.dataset import Dataset
from hdx.data.hdxobject import HDXError
from hdx.facades.simple import facade
from hdx.utilities.dictandlist import dict_of_lists_add


def main():
    datasetlist = Dataset.search_in_hdx(fq="organization:fao")
    datasets = dict()
    for dataset in datasetlist:
        name = dataset["name"]
        if name.startswith("faostat-prices-for-"):
            countryiso3s = dataset.get_location_iso3s()
            if len(countryiso3s) == 1:
                dict_of_lists_add(datasets, countryiso3s[0], dataset)
    for possible_duplicates in datasets.values():
        number_of_duplicates = len(possible_duplicates)
        if number_of_duplicates != 2:
            continue
        names_str = ", ".join(x["name"] for x in possible_duplicates)
        print(f"{number_of_duplicates}: {names_str}")


if __name__ == '__main__':
    facade(
        main,
        hdx_site="prod",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yml"),
        user_agent_lookup="duplicate_country_datasets",
    )

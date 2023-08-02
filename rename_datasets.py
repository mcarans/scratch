from os.path import join, expanduser

from hdx.data.dataset import Dataset
from hdx.data.hdxobject import HDXError
from hdx.facades.simple import facade
from hdx.utilities.dictandlist import dict_of_lists_add


def main():
    datasetlist = Dataset.search_in_hdx(fq="organization:fao")
    for dataset in datasetlist:
        name = dataset["name"]
        if name.startswith("faostat-prices-for-"):
            countryname = name.replace("faostat-prices-for-", "")
            newname = f"faostat-food-prices-for-{countryname}"
            dataset["name"] = newname
            try:
                print(
                    "%s => %s" % (name, newname),
                    dataset["title"],
                    dataset.get_hdx_url(),
                )
                dataset.update_in_hdx(ignore_check=True)
            except HDXError as ex:
                print("Not updating %s: %s" % (newname, str(ex)))
                continue


if __name__ == '__main__':
    facade(
        main,
        hdx_site="prod",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yml"),
        user_agent_lookup="rename_datasets",
    )

import logging
from os.path import join, expanduser

from hdx.data.dataset import Dataset
from hdx.data.hdxobject import HDXError
from hdx.facades.simple import facade
from hdx.location.country import Country


logger = logging.getLogger(__name__)


def main():
    datasetlist = Dataset.search_in_hdx(fq="organization:ocha-fts")
    for dataset in datasetlist:
        if dataset["archived"] is True or dataset["private"] is True:
            continue
        name = dataset["name"]
        if name.startswith("fts-requirements-and-funding-data-for-"):
            countryname = name.replace("faostat-prices-for-", "")
            countryiso3, _ = Country.get_iso3_country_code_fuzzy(countryname)
            if not countryiso3:
                print(f"Skipping {name} as cannot get iso3 for {countryname}!")
                continue
            newname = f"{countryiso3.lower()}-requirements-and-funding-data"
            dataset["name"] = newname
            try:
                print(
                    "%s => %s" % (name, newname),
                    dataset["title"],
                    dataset.get_hdx_url(),
                )
                dataset.update_in_hdx(ignore_check=True)
            except HDXError as ex:
                logger.exception(ex)
                continue


if __name__ == "__main__":
    facade(
        main,
        hdx_site="prod",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="rename_datasets",
    )

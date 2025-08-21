#!/usr/bin/python
"""
Double update issue

"""

import logging
from os.path import join, expanduser

from hdx.data.dataset import Dataset
from hdx.facades.simple import facade

logger = logging.getLogger(__name__)


def main():
    dataset_name = "icpac-geonode-tanzania-flood-inundation-100-year-return-period"
    dataset = Dataset.read_from_hdx(dataset_name)
    if dataset:
        dataset.delete_from_hdx()
    dataset = Dataset.load_from_json("double_update/icpac_original.json")
    dataset.create_in_hdx(hxl_update=False, updated_by_script="HDX Scraper: ICPAC")
    dataset = Dataset.load_from_json("double_update/icpac_new.json")
    dataset.create_in_hdx(
        remove_additional_resources=True,
        hxl_update=False,
        updated_by_script="HDX Scraper: ICPAC",
    )
    logger.info("Completed!")


if __name__ == "__main__":
    facade(
        main,
        hdx_site="stage",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="test",
    )

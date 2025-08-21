#!/usr/bin/python
"""
Creates a dataset on HDX.

"""
import argparse
import csv
import logging
from os.path import join

from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
from hdx.facades.simple import facade
from hdx.utilities.dateparse import parse_date
from hdx.utilities.path import get_temp_dir

logger = logging.getLogger(__name__)

lookup = "GIS4tech"


def main():
    """Generate dataset and create it in HDX"""
    dataset = Dataset(
        {
            "name": "gis4tech-test",
            "title": "GIS4tech Test Dataset",
            "license_id": "cc-by-igo",
            "methodology": "Other",
            "private": False,
            "dataset_source": "GIS4tech"
        }
    )
    dataset["notes"] = "Long description of dataset goes here!"
    dataset["methodology_other"] = "Describe methodology here!"
    dataset["caveats"] = "Any caveats or comments about the data go here!"
    dataset.set_maintainer("ef08b055-e04b-40fe-8b7b-5441b263fc0c")  # gis4tech user
    dataset.set_organization(
        "ca3e5890-5507-454d-b1e2-fa2e1a74c25e"
    )  # gis4tech organisation
    dataset.set_expected_update_frequency("Every year")
    dataset.set_subnational(False)
    dataset.add_tags(["geodata"])
    dataset.set_time_period(parse_date("2020-03-05"), parse_date("2021-02-25"))

    dataset.add_country_location("AFG")
    # or
    dataset.add_country_locations(["AFG"])
    # or
    dataset.add_other_location("world")

    logger.info("Dataset metadata created!")

    path = join(get_temp_dir(), "test.csv")
    with open(path, "w", encoding="UTF8") as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(["heading1", "heading2", "heading3", "heading4"])

        # write the data
        writer.writerow([1, 2, 3, 4])
        writer.writerow([5, 6, 7, 8])

    logger.info(f"Test file {path} created!")

    resource = Resource(
        {"name": "test file", "description": "description of test file"}
    )
    resource.set_format("csv")
    resource.set_file_to_upload(path)

    logger.info("Resource metadata created!")

    dataset.add_update_resource(resource)
    dataset.create_in_hdx(
        remove_additional_resources=True,
        updated_by_script="GIS4tech",
    )
    logger.info("Completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=lookup)
    parser.add_argument("-ht", "--hdx_token", default=None, help="HDX api token")
    parser.add_argument("-hs", "--hdx_site", default=None, help="HDX site to use")
    args = parser.parse_args()
    hdx_site = args.hdx_site
    if hdx_site is None:
        hdx_site = "stage"
    facade(
        main,
        hdx_key=args.hdx_token,
        hdx_site=hdx_site,
        user_agent=lookup,
    )

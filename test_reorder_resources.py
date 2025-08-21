#!/usr/bin/python
"""
Creates a dataset on HDX.

"""
import logging
from os.path import expanduser, join

from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
from hdx.facades.simple import facade
from hdx.utilities.dateparse import parse_date

logger = logging.getLogger(__name__)


def main():

    def create_dataset_metadata():
        """Generate dataset and create it in HDX"""
        dataset = Dataset(
            {
                "name": "reorder-test",
                "title": "Reordering Test Dataset",
                "license_id": "cc-by-igo",
                "methodology": "Other",
                "private": False,
                "dataset_source": "Innago"
            }
        )
        dataset["notes"] = "Long description of dataset goes here!"
        dataset["methodology_other"] = "Describe methodology here!"
        dataset["caveats"] = "Any caveats or comments about the data go here!"
        dataset.set_maintainer("196196be-6037-4488-8b71-d786adf4c081")  # mcarans
        dataset.set_organization(
            "5a63012e-6c41-420c-8c33-e84b277fdc90"
        )  # innago organisation
        dataset.set_expected_update_frequency("Every year")
        dataset.set_subnational(False)
        dataset.add_tags(["geodata"])
        dataset.set_time_period(parse_date("2020-03-05"), parse_date("2021-02-25"))

        dataset.add_country_location("AFG")
        return dataset

    dataset = create_dataset_metadata()
    for i in range(10):
        name = f"resource-{i}"
        resource = Resource({"name": name, "description": name, "format": "xlsx"})
        resource.set_file_to_upload("test.xlsx")
        dataset.add_update_resource(resource)

    dataset.create_in_hdx()
    logger.info("Dataset created!")

    dataset = Dataset.read_from_hdx("reorder-test")
    for resource in dataset.get_resources():
        logger.info(f"Resource name: {resource['name']}")

    dataset = create_dataset_metadata()
    name = f"resource-inserted"
    resource = Resource({"name": name, "description": name, "format": "xlsx"})
    resource.set_file_to_upload("test.xlsx")
    dataset.add_update_resource(resource)
    for i in range(10):
        name = f"resource-{9-i}"
        resource = Resource({"name": name, "description": name, "format": "xlsx"})
        resource.set_file_to_upload("test.xlsx")
        dataset.add_update_resource(resource)

    dataset.update_in_hdx(match_resource_order=True)
    logger.info("Dataset updated!")

    dataset = Dataset.read_from_hdx("reorder-test")
    for resource in dataset.get_resources():
        logger.info(f"Resource name: {resource['name']}")

    dataset.delete_from_hdx()
    logger.info("Dataset deleted!")


if __name__ == "__main__":
    facade(
        main,
        hdx_site="demo",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="rename_datasets",
    )

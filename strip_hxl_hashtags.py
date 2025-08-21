import logging
from os import rename, remove
from os.path import join, expanduser

from hdx.data.dataset import Dataset
from hdx.data.organization import Organization
from hdx.facades.simple import facade
from hdx.utilities.downloader import Download
from hdx.utilities.path import temp_dir


logger = logging.getLogger(__name__)


def strip_hxl(folder, downloader, resource):
    csv_path = downloader.download_file(resource["url"], folder=folder)
    input_path = csv_path.replace(".csv", "_orig.csv")
    rename(csv_path, input_path)
    completed = False
    with open(input_path, "r") as infile, open(csv_path, "w") as outfile:
        for i, line in enumerate(infile):
            if i == 1:
                resource_name = resource["name"]
                if line[0] == "#":
                    logger.info(f"Processing resource {resource_name}")
                    completed = True
                else:
                    logger.warning(
                        f"Second line of resource {resource_name} isn't HXL!"
                    )
                    completed = False
                    break
            else:
                outfile.write(line)
    if completed:
        return csv_path
    remove(csv_path)
    return None


def main():
    with temp_dir(
        "strip_hxl_tags", delete_if_exists=True, delete_on_success=False
    ) as folder:
        with Download() as downloader:
            organisation = Organization.read_from_hdx("hdx-hapi")
            rainfall_datasets = Dataset.search_in_hdx(
                fq='dataseries_name:"WFP - Rainfall Indicators at Subnational Level"',
                sort="name asc",
            )
            hapi_datasets = organisation.get_datasets(sort="name asc")
            datasets = rainfall_datasets + hapi_datasets
            resource_uploads = []
            for dataset in datasets:
                logger.info(f"Processing dataset {dataset['name']}")
                for resource in dataset.get_resources():
                    path = strip_hxl(folder, downloader, resource)
                    if path:
                        resource.set_file_to_upload(path)
                        resource_uploads.append(resource)
                tags = dataset.get_tags()
                if "hxl" in tags:
                    dataset.remove_tag("hxl")
                    remove_tag = True
                else:
                    remove_tag = False
                no_resource_uploads = len(resource_uploads)
                if no_resource_uploads == 0:
                    logger.error(
                        f"No HXL resources found for dataset {dataset['name']}"
                    )
                    if remove_tag:
                        dataset.update_in_hdx(hxl_update=False)
                elif no_resource_uploads == 1 and not remove_tag:
                    resource_uploads[0].update_in_hdx()
                else:
                    dataset.update_in_hdx(hxl_update=False)


if __name__ == "__main__":
    facade(
        main,
        hdx_site="bluedemo",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="strip_hxl_tags",
    )

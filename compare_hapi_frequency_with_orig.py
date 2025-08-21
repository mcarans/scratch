import logging
from os.path import join, expanduser

from hdx.data.dataset import Dataset
from hdx.facades.simple import facade
from hdx.utilities.downloader import Download

logger = logging.getLogger(__name__)


def main():
    with Download(user_agent="test") as downloader:
        matching = []
        datasets = Dataset.search_in_hdx(fq="organization:hdx-hapi")
        for dataset in datasets:
            hapi_title = dataset["title"]
            if hapi_title.startswith("HDX HAPI -"):
                hapi_update_frequency = dataset.get_expected_update_frequency()
                hapi_url = dataset.get_hdx_url()
                dataset_ids = set()
                for resource in dataset.get_resources():
                    url = resource["url"]
                    headers, iterator = downloader.get_tabular_rows(
                        url, headers=1, dict_form=True
                    )
                    for row in iterator:
                        if "dataset_hdx_id" not in row:
                            break
                        dataset_id = row["dataset_hdx_id"]
                        if dataset_id[0] == "#":
                            continue
                        dataset_ids.add(dataset_id)
                match = True
                for dataset_id in dataset_ids:
                    dataset = Dataset.read_from_hdx(dataset_id)
                    dataset_expected_update_frequency = (
                        dataset.get_expected_update_frequency()
                    )
                    if dataset_expected_update_frequency != hapi_update_frequency:
                        match = False
                        dataset_title = dataset["title"]
                        dataset_url = dataset.get_hdx_url()
                        logger.error(
                            f"{hapi_title} ({hapi_url}) has frequency {hapi_update_frequency} but {dataset_title} ({dataset_url}) has {dataset_expected_update_frequency}!"
                        )
                if match:
                    matching.append(
                        f"{hapi_title} ({hapi_url}) has frequency {hapi_update_frequency} and all datasets match"
                    )
        for match in matching:
            logger.info(match)


if __name__ == "__main__":
    facade(
        main,
        hdx_site="prod",
        hdx_read_only=True,
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="test",
    )

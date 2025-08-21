from os.path import join, expanduser

from hdx.data.dataset import Dataset
from hdx.data.hdxobject import HDXError
from hdx.facades.simple import facade


def main():
    datasetlist = Dataset.search_in_hdx(
        fq="organization:oxford-poverty-human-development-initiative"
    )
    for dataset in datasetlist:
        dataset_name = dataset["name"]
        if not dataset_name.endswith("-mpi"):
            print(f"Ignoring non mpi dataset: {dataset_name}")
            continue
        for showcase in dataset.get_showcases():
            showcase_name = showcase["name"]
            if not showcase_name.endswith("sub-national-poverty"):
                print(f"Ignoring newer showcase: {showcase_name}")
                continue
            print(f"Removing dataset from {showcase_name}")
            try:
                showcase.remove_dataset(dataset)
                showcase.delete_from_hdx()
            except HDXError as ex:
                print(f"Failed to remove showcase: {showcase_name}\n{str(ex)}")
                continue


if __name__ == "__main__":
    facade(
        main,
        hdx_site="prod",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="delete_showcases",
    )

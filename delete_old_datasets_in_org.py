from os.path import join, expanduser

from hdx.data.dataset import Dataset
from hdx.facades.simple import facade


def main():
    datasets = Dataset.search_in_hdx(fq="organization:advanced-disaster-analysis-mapping")
    count = 0
    for dataset in datasets:
        name = dataset["name"]
        title = dataset["title"]
        if "Depth" in title or title[3] == ":":
#        if name.startswith("interaction-data-for-"):
            count += 1
            print(name, title, dataset.get_hdx_url())
            dataset.delete_from_hdx()
    print(f"total datasets {count} deleted!")


if __name__ == '__main__':
    facade(
        main,
        hdx_site="prod",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yml"),
        user_agent_lookup="delete_old_datasets",
    )

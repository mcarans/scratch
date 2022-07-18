from hdx.data.dataset import Dataset
from hdx.facades.simple import facade


def main():
    datasets = Dataset.search_in_hdx(fq="organization:interaction")
    count = 0
    for dataset in datasets:
        name = dataset["name"]
        if name.startswith("interaction-data-for-"):
            count += 1
            print(name, dataset["title"], dataset.get_hdx_url())
            dataset.delete_from_hdx()
    print(f"total datasets {count} deleted!")


if __name__ == "__main__":
    facade(main, hdx_site="stage", user_agent="test")

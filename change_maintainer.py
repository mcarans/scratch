from hdx.data.dataset import Dataset
from hdx.data.user import User
from hdx.facades.simple import facade

old_maintainer_ids = "bc83a4e6-df44-4d2b-95bf-9caf5d0f5e7b",  # John Marinos
new_maintainer_id = "a7ae6994-1685-4409-a0e5-9a10d4c3f55b"
#old_maintainer_ids = "a410b53c-3466-4517-a7d7-bedd76aa258b",  # hdx-amadou
#new_maintainer_id = "a303cd25-2073-4c72-9b22-7a2d61ff797a"


def main():
    maintainer_id_to_name = dict()
    for maintainer_id in old_maintainer_ids:
        old_maintainer = User.read_from_hdx(maintainer_id)
        name = old_maintainer["name"]
        maintainer_id_to_name[maintainer_id] = old_maintainer["name"]
        print(f"User to change from: {name}")
    new_maintainer = User.read_from_hdx(new_maintainer_id)
    print(f"User to change to: {new_maintainer['name']}")
    datasets = Dataset.get_all_datasets()
    count = 0
    changed_datasets = list()
    for dataset in datasets:
        maintainer_id = dataset["maintainer"]
        if maintainer_id not in old_maintainer_ids:
            continue
        old_maintainer_name = maintainer_id_to_name.get(maintainer_id)
        print(f"Dataset to change: {dataset['name']} with maintainer: {old_maintainer_name}")
        count += 1
        dataset.set_maintainer(new_maintainer)
        dataset.update_in_hdx(operation="patch", update_resources=False, batch_mode="KEEP_OLD", skip_validation=True, ignore_check=True, create_default_views=False, hxl_update=False)
        changed_datasets.append(dataset.get_hdx_url())
    print(f"Changed {count} datasets")
    datasets_str = "\n".join(changed_datasets)
    print(f"Datasets changed: {datasets_str}")


if __name__ == "__main__":
    facade(main, hdx_site="prod", user_agent='test')

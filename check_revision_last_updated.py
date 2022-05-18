from hdx.data.dataset import Dataset
from hdx.facades.simple import facade


def main():
    datasets = Dataset.get_all_datasets()
    for dataset in datasets:
        for resource in dataset.get_resources():
            revision_last_updated = resource.get('revision_last_updated')
            if revision_last_updated is not None:
                print(f'id: {resource["id"]}, dataset id: {resource["package_id"]}  revision_last_updated: {revision_last_updated}')

if __name__ == '__main__':
    facade(main, hdx_site='feature', user_agent='test')

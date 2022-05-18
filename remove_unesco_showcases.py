from hdx.data.dataset import Dataset
from hdx.data.hdxobject import HDXError
from hdx.facades.simple import facade


def main():
    datasetlist = Dataset.search_in_hdx(fq='organization:unesco')
    for dataset in datasetlist:
        dataset_name = dataset['name']
        if not dataset_name.startswith('unesco-data-for-'):
            print(f'Ignoring non education dataset: {dataset_name}')
            continue
        for showcase in dataset.get_showcases():
            showcase_name = showcase['name']
            if not showcase_name.startswith('unesco'):
                print(f'Ignoring non unesco showcase: {showcase_name}')
                continue
            if showcase_name.startswith('unesco-data-for-'):
                print(f'Ignoring {showcase_name}')
                continue
            print(f'Removing dataset from {showcase_name}')
            try:
                showcase.remove_dataset(dataset)
            except HDXError as ex:
                print(f'Failed to remove dataset from showcase: {showcase_name}\n{str(ex)}')
                continue


if __name__ == '__main__':
    facade(main, hdx_site='prod', user_agent='test')

from hdx.data.dataset import Dataset
from hdx.facades.simple import facade
from hdx.utilities import is_valid_uuid


def main():
    datasets = Dataset.get_all_datasets()
    fp = open('wrong_missing_maintainer.csv', 'wt')
    fp.write('name,maintainer,organization\n')
    for dataset in datasets:
        maintainer = dataset['maintainer']
        if not is_valid_uuid(maintainer):
            org = dataset.get('organization')
            if org:
                org = org['title']
            else:
                org = 'NONE!'
            if not maintainer:
                maintainer = 'NONE!'
            fp.write(f"{dataset['name']},{maintainer},{org}\n")
    fp.close()


if __name__ == '__main__':
    facade(main, hdx_site='prod')

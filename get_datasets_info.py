from hdx.data.dataset import Dataset
from hdx.facades.simple import facade


def main():
    datasets = Dataset.get_all_datasets()
    fp = open('datasets.csv', 'wt')
    fp.write('name,organization,date created,status\n')
    for dataset in datasets:
        org = dataset.get('organization')
        if org:
            org = org['title']
        else:
            org = 'NONE!'
        fp.write(f"{dataset['name']},{org},{dataset['metadata_created']},{dataset['private']}\n")
    fp.close()


if __name__ == '__main__':
    facade(main, hdx_site='prod', user_agent='test')

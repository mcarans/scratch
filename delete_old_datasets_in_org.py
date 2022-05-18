from hdx.data.dataset import Dataset
from hdx.facades.simple import facade


def main():
    datasets = Dataset.search_in_hdx(fq='organization:unesco')
    count = 0
    for dataset in datasets:
        name = dataset['name']
        if name.startswith('unesco-education-students-and-teachers'):
            count += 1
            print(name, dataset['title'], dataset.get_hdx_url())
            dataset.delete_from_hdx()
    print('total datasets %d deleted!' % count)


if __name__ == '__main__':
    facade(main, hdx_site='prod', user_agent='test')

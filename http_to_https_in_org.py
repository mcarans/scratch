from time import sleep

from hdx.data.dataset import Dataset
from hdx.facades.simple import facade


def main():
    datasets = Dataset.search_in_hdx(fq='organization:un-operational-satellite-appplications-programme-unosat')
    for dataset in datasets:
        name = dataset['name']
        for resource in dataset.get_resources():
            url = resource['url']
            if url[:5] == 'https':
                continue
            new_url = url.replace('http://', 'https://')
            print(name, url, new_url)
            resource['url'] = new_url
            resource.update_in_hdx(operation='patch', ignore_check=True, skip_validation=True)


if __name__ == '__main__':
    facade(main, hdx_site='prod', user_agent='test')

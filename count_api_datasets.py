from urllib.parse import urlsplit

from hdx.data.dataset import Dataset
from hdx.facades.simple import facade


def add_one(d, k):
    if k not in d:
        d[k] = 0
    d[k] += 1


botmapping = {'1a008a13-52b1-4326-a9ea-aa541372577c': 'hdx_bot_scrapers',
#              '154de241-38d6-47d3-a77f-0a9848a61df3': 'hdx_bot_datateam',
#              '060468e4-2f33-4488-8504-c4b10cc34821': 'hdx',
              '7ae95211-71dd-484e-8538-2c625315eb56': 'David Megginson',
              '6a0688ce-8521-46e2-8edd-8e26c0851ebd': 'HOT Bot',
              '83fa9515-3ba4-4f1d-9860-f38b20f80442': 'UNOSAT'}


def main():
    datasets = Dataset.get_all_datasets()
    updated_by_script = dict()
    bots = dict()
    for dataset in datasets:
        resources = dataset.get_resources()
        if len(resources) == 0:
            continue
        url = resources[0]['url']
        sourcehost = f"{dataset['dataset_source']}-{urlsplit(url).netloc}"
        if 'updated_by_script' in dataset:
            add_one(updated_by_script, sourcehost)
            continue
        maintainer = dataset['maintainer']
        if maintainer in botmapping:
            add_one(bots, sourcehost)
#            print('%s - %s' % (botmapping[maintainer], dataset.get_hdx_url()))
            continue
        if maintainer == 'a410b53c-3466-4517-a7d7-bedd76aa258b' and dataset['organization']['name'] in ['healthsites', 'unhabitat-guo']:
            add_one(bots, sourcehost)
            continue

    print('\nupdated_by_script')
    updated_by_script_total = 0
    for k in updated_by_script:
        c = updated_by_script[k]
        print('%s = %d' % (k, c))
        updated_by_script_total += c
    print('\nbots')
    bots_total = 0
    for k in bots:
        c = bots[k]
        print('%s = %d' % (k, c))
        bots_total += c
    print('\nUpdated by script = %d' % updated_by_script_total)
    print('Bots = %d' % bots_total)
    total_programmatic = updated_by_script_total + bots_total
    print('\nProgrammatically uploaded datasets = %d' % total_programmatic)
    total_datasets = len(datasets)
    proportion = float(total_programmatic) / float(total_datasets) * 100.0
    print('Total datasets = %d;           Proportion uploaded programmatically=%d%%' % (total_datasets, int(proportion)))


if __name__ == '__main__':
    facade(main, hdx_read_only=True, hdx_site='prod', user_agent='test')

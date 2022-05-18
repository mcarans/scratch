from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset
from hdx.utilities.dictandlist import write_list_to_csv

Configuration.create(hdx_site='prod', user_agent='A_Quick_Example', hdx_read_only=True)
# https://data.humdata.org/api/action/package_search?q=*:*&fq=metadata_created:[2018-07-01T00:00:00.000Z%20TO%202018-09-30T00:00:00.000Z]
rows = list()
datasets = Dataset.search_in_hdx(fq='metadata_created:[2019-04-01T00:00:00.000Z TO 2019-06-30T00:00:00.000Z]')
for dataset in datasets:
    resources = dataset.resources
    if len(resources) > 0:
        url = resources[0]['url']
    else:
        url = ''
    rows.append([dataset['name'], dataset['metadata_created'], url, dataset['organization']['name']])
write_list_to_csv(rows, 'createddatasets.csv', ['name', 'created', 'url', 'orgname'])
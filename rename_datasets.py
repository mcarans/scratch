from hdx.data.hdxobject import HDXError
from hdx.data.dataset import Dataset
from hdx.facades.simple import facade
from hdx.utilities.dictandlist import dict_of_lists_add


def main():
    datasetlist = Dataset.search_in_hdx(fq='organization:wfp')
    datasets = dict()
    for dataset in datasetlist:
        name = dataset['name']
        if name.startswith('wfp-food-prices'):
            countryiso3s = dataset.get_location_iso3s()
            if len(countryiso3s) == 1:
                dict_of_lists_add(datasets, countryiso3s[0], dataset)
    for possible_duplicates in datasets.values():
        number_of_duplicates = len(possible_duplicates)
        if number_of_duplicates != 2:
            continue
        names_str = ', '.join(x['name'] for x in possible_duplicates)
        print(f'{number_of_duplicates}: {names_str}')

        #
        # for key in mapping:
        #     if not name.endswith(key):
        #         continue
        #     countryname = name.replace('worldpop-', '').replace('-%s' % key, '')
        #     newname = mapping[key] % countryname
        #     dataset = datasets[name]
        #     newdataset = datasets.get(newname)
        #     if not newdataset:
        #         continue
        #     newdatasetcopy = Dataset(initial_data=newdataset.data)
        #     try:
        #         print('Deleting %s' % newname)
        #         newdatasetcopy.delete_from_hdx()
        #     except HDXError as ex:
        #         print('Failed to delete: %s\n%s' % (newname, str(ex)))
        #         continue
        #     newdataset['id'] = dataset['id']
        #     try:
        #         print('%s => %s' % (name, newname), newdataset['title'], newdataset.get_hdx_url())
        #         newdataset.update_in_hdx(ignore_check=True)
        #     except HDXError as ex:
        #         print('Not updating %s: %s' % (newname, str(ex)))
        #         continue


if __name__ == '__main__':
    facade(main, hdx_site='stage', user_agent='test')

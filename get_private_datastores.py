from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
from hdx.facades.simple import facade
from hdx.utilities.dictandlist import write_list_to_csv


def main():
    resource_ids = Resource.get_all_resource_ids_in_datastore()
    output = [['resource id', 'dataset title', 'organisation', 'dataset url']]
    for resource_id in resource_ids:
        if resource_id == '_table_metadata':
            continue
        resource = Resource.read_from_hdx(resource_id)
        if resource is None:
            print(f'{resource_id} does not exist!')
        else:
            dataset_id = resource['package_id']
            dataset = Dataset.read_from_hdx(dataset_id)
            dataset_name = dataset['name']
            dataset_title = dataset['title']
            organisation_title = dataset['organization']['title']
            if dataset['private']:
                output.append([resource_id, dataset_title, organisation_title, f'https://data.humdata.org/dataset/{dataset_name}'])
    write_list_to_csv('private_resources_datastores.csv', output, 1)


if __name__ == '__main__':
    facade(main, hdx_site='prod', user_agent='test')

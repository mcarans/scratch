from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
from hdx.facades.simple import facade


def main():
    resource_ids = Resource.get_all_resource_ids_in_datastore()
    for resource_id in resource_ids:
        if resource_id == '_table_metadata':
            continue
        resource = Resource.read_from_hdx(resource_id)
        if resource is None:
            print(f'{resource_id} does not exist! Deleting datastore')
            resource = Resource({'id': resource_id})
            resource.delete_datastore()
        elif resource['state'] != 'active':
            print(f'{resource_id} is not active! Deleting datastore')
            resource.delete_datastore()
        else:
            dataset_id = resource['package_id']
            dataset = Dataset.read_from_hdx(dataset_id)
            if dataset['private']:
                print(f'{resource_id} is in a private dataset {dataset_id}! Deleting datastore')
                resource.delete_datastore()


if __name__ == '__main__':
    facade(main, hdx_site='prod', user_agent='test')

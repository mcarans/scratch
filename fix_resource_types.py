from hdx.data.dataset import Dataset
from hdx.hdx_configuration import Configuration

Configuration.create(hdx_site='prod', user_agent='A_Quick_Example')
datasets = Dataset.get_all_datasets()
for dataset in datasets:
    for resource in dataset.get_resources():
        resource_name = resource['name']
        current_type = resource.get_file_type()
        if current_type == 'zip':
            if resource_name.endswith('_gdb.zip'):
                new_type = 'Geodatabase'
            elif resource_name.endswith('_csv.zip'):
                new_type = 'CSV'
            elif resource_name.endswith('_geotiff.zip'):
                new_type = 'GeoTIFF'
            else:
                continue
        elif current_type =='zipped kml':
            new_type = 'KML'
        elif current_type == 'zipped img':
            if 'garmin' in resource['description'].lower():
                new_type = 'Garmin IMG'
            else:
                continue
        else:
            continue
        dataset_name = dataset['name']
        print(f'Updating dataset {dataset_name}, resource {resource_name} format {current_type} -> {new_type}')
        resource.set_file_type(new_type)
        resource.update_in_hdx(ignore_check=True)
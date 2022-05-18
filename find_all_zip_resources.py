from hdx.data.dataset import Dataset
from hdx.hdx_configuration import Configuration

Configuration.create(hdx_site='prod', user_agent='A_Quick_Example')
datasets = Dataset.get_all_datasets()
for dataset in datasets:
    for resource in dataset.get_resources():
        file_type = resource.get_file_type()
        if 'zip' in file_type:
            dataset_name = dataset['name']
            print(f'Dataset {dataset.get_hdx_url()}, resource {resource["name"]} format {file_type} description {resource["description"]}')

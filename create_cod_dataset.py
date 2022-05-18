from datetime import datetime

from hdx.data.resource import Resource
from hdx.facades.simple import facade
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset
from hdx.utilities.path import script_dir_plus_file

Configuration.create(hdx_site='dev', user_agent='A_Quick_Example')


def main():
    dataset = Dataset({
        'name': 'mike_test',
        'title': 'mike test',
        'notes': 'mike test desc',
        'private': False,
        'license_id': 'cc-by-igo',
        'dataset_source': 'OCHA Financial Tracking Service',
        'methodology': 'Registry',
        'cod_level': 'cod-candidate'
    })
    dataset.set_maintainer('196196be-6037-4488-8b71-d786adf4c081')
    dataset.set_organization('fb7c2910-6080-4b66-8b4f-0be9b6dc4d8e')
    dataset.set_dataset_date_from_datetime(datetime.now())
    dataset.set_expected_update_frequency('Every day')
    dataset.add_country_locations(['AFG'])
    dataset.set_subnational(False)
    tags = ['hxl', 'financial tracking service - fts', 'aid funding']
    dataset.add_tags(tags)
    resource = Resource({
        'name': 'mike_test.csv',
        'description': 'mike test resource',
        'format': 'csv',
        'daterange_for_data': '[2020-03-11T21:16:48.838 TO *]',
        'grouping': 'Group 1'
    })
    resource.set_file_to_upload(script_dir_plus_file('Extract.csv', main))
    dataset.add_update_resource(resource)
    dataset.create_in_hdx(remove_additional_resources=True)


if __name__ == '__main__':
    facade(main, user_agent='test', hdx_site='dev')

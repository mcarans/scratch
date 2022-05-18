from hdx.data.showcase import Showcase
from hdx.data.user import User
from hdx.hdx_configuration import Configuration
from hdx.utilities.dictandlist import write_list_to_csv

Configuration.create(hdx_site='prod', user_agent='A_Quick_Example')
output = list()
for showcase in Showcase.get_all_showcases():
    datasets = showcase.get_datasets()
    if len(datasets) == 0:
        print(f"Deleting showcase https://data.humdata.org/showcase/{showcase['name']} ({showcase['id']}) {showcase['url']}")
        showcase.delete_from_hdx()

        # user = User.read_from_hdx(showcase['creator_user_id'])
        # output.append(['https://data.humdata.org/showcase/%s' % showcase['name'], showcase['id'], showcase['metadata_created'][:10], showcase['metadata_modified'][:10], user['name'], user['display_name'], user['email']])
        # print('Showcase https://data.humdata.org/showcase/%s (%s) created on %s, modified on %s has no datasets! Created by %s (%s %s)' % (showcase['name'], showcase['id'], showcase['metadata_created'][:10], showcase['metadata_modified'][:10], user['display_name'], user['name'], user['email']))
write_list_to_csv('empty_showcases.csv', output, headers=['url', 'id', 'created', 'modified', 'username', 'display name', 'email'])

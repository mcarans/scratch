from os.path import join, expanduser

from dateutil.relativedelta import relativedelta
from hdx.data.dataset import Dataset
from hdx.facades.simple import facade


def main():
    dataset_name = "worldpop-population-density-for-samoa"
    dataset = Dataset.read_from_hdx(dataset_name)
    resource = dataset.get_resource()
    last_modified = resource.get_date_data_updated()
    print(f"current last_modified is {last_modified}")
    last_modified += relativedelta(days=1)
    resource.set_date_data_updated(last_modified)
    dataset.update_in_hdx()
    print(f"changed last_modified to {last_modified}")


if __name__ == '__main__':
    facade(
        main,
        hdx_site="stage",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yml"),
        user_agent_lookup="test",
    )

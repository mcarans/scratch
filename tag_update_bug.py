from os.path import join, expanduser

from dateutil.relativedelta import relativedelta
from hdx.data.dataset import Dataset
from hdx.facades.simple import facade


def main():
    dataset = Dataset.read_from_hdx("hotosm_and_waterways")
    current_tags = dataset.get_tags()
    print(f"current tags: {current_tags}")
    dataset.remove_tag("hydrology")
    dataset.update_in_hdx(
        update_resources=False,
    )
    dataset = Dataset.read_from_hdx("hotosm_and_waterways")
    new_tags = dataset.get_tags()
    print(f"new tags: {new_tags}")


if __name__ == '__main__':
    facade(
        main,
        hdx_site="stage",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yml"),
        user_agent_lookup="test",
    )

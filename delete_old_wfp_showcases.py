from os.path import join, expanduser

from hdx.data.showcase import Showcase
from hdx.data.user import User
from hdx.api.configuration import Configuration
from hdx.facades.simple import facade
from hdx.utilities.dictandlist import write_list_to_csv


def main():
    for showcase in Showcase.get_all_showcases():
        name = showcase["name"]
        url = showcase["url"]
        if url.startswith("http://www.fao.org/faostat/en/#country/") or name.startswith("faostat-prices-for-") or name.endswith("for-food-security-showcase"):
            print(f"Deleting showcase https://data.humdata.org/showcase/{name} ({showcase['id']}) {url}")
            showcase.delete_from_hdx()


if __name__ == '__main__':
    facade(
        main,
        hdx_site="prod",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="delete_showcases",
    )

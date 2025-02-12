from os.path import join, expanduser

from hdx.data.dataset import Dataset
from hdx.facades.simple import facade
from hdx.utilities.session import get_session


def main():
    no_resources = 0
    no_int_resources = 0
    no_ext_resources = 0
    no_resources_no_size = 0
    no_resources_with_size = 0
    total_size = 0
    no_broken_resources = 0
    no_web_app_resources = 0
    session = get_session(retry_attempts=0)
    datasetlist = Dataset.search_in_hdx(fq="organization:wfp")
    print("Obtained dataset list. Processing...")
    for dataset in datasetlist:
        for resource in dataset.get_resources():
            no_resources += 1
            if no_resources % 100 == 0:
                print(f"Processed {no_resources}...")
            if resource["url_type"] != "api":
                no_int_resources += 1
                continue
            no_ext_resources += 1
            if resource["format"] == "Web App":
                no_web_app_resources += 1
                continue
            url = resource["url"]
            try:
                response = session.head(url, allow_redirects=True, timeout=10)
            except Exception:
                no_broken_resources += 1
                continue
            if response.status_code != 200:
                response.close()
                no_broken_resources += 1
                continue
            headers = response.headers
            size = headers.get("Content-Length")
            response.close()
            if not size:
                no_resources_no_size += 1
                continue
            no_resources_with_size += 1
            total_size += int(size)
    print(f"Number of resources: {no_resources}")
    print(f"Number of internal resources: {no_int_resources}")
    print(f"Number of external resources: {no_ext_resources}")
    print(f"Number of external web app resources: {no_web_app_resources}")
    print(f"Number of broken external resources: {no_broken_resources}")
    print(f"Number of external resources with no size info: {no_resources_no_size}")
    print(f"Number of external resources with size info: {no_resources_with_size}")
    print(f"Total size of external resources: {total_size}")


if __name__ == "__main__":
    facade(
        main,
        hdx_site="prod",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="test",
    )

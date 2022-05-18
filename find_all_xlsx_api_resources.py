from hdx.api.configuration import Configuration
from hdx.data.resource import Resource

Configuration.create(hdx_site="prod", user_agent="A_Quick_Example")
resources = Resource.search_in_hdx("format:xlsx")
filestore_resources = 0
for resource in resources:
    url = resource["url"]
    if url.startswith("https://data.humdata.org"):
        filestore_resources += 1

    print(f"Resource {resource['name']} url {resource['url']}")

no_resources = len(resources)
print(f"Number of resources = {no_resources}")
print(f"Number of filestore resources = {filestore_resources}")
print(f"Number of external resources = {no_resources - filestore_resources}")



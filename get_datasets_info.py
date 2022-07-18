from hdx.data.dataset import Dataset
from hdx.facades.simple import facade
from hdx.utilities.dictandlist import write_list_to_csv


def main():
    datasets = Dataset.get_all_datasets()
    rows = [("name", "title", "downloads", "date created", "date metadata updated", "date data updated", "dataset start date", "dataset end date", "update frequency", "organisation", "data link", "url,", "tags", "private", "requestable", "updated by script")]
    for dataset in datasets:
        name = dataset["name"]
        title = dataset["title"]
        downloads = dataset.get("total_res_downloads", "")
        created = dataset["metadata_created"]
        metadata_updated = dataset["metadata_modified"]
        data_updated = dataset["last_modified"]
        date_of_dataset = dataset.get_date_of_dataset()
        startdate = date_of_dataset["startdate_str"]
        if date_of_dataset["ongoing"]:
            enddate = "ongoing"
        else:
            enddate = date_of_dataset["enddate_str"]
        update_frequency = dataset.get("data_update_frequency", "")
        org = dataset.get("organization")
        if org:
            org = org["title"]
        else:
            org = "NONE!"
        requestable = dataset.is_requestable()
        if requestable:
            data_link = ""
            requestable = "Y"
        else:
            data_link = dataset.get_resource()["url"]
            requestable = "N"
        url = dataset.get_hdx_url()
        tags = ", ".join(dataset.get_tags())
        private = "Y" if dataset["private"] else "N"
        updated_by_script = dataset.get("updated_by_script", "")
        row = (name, title, downloads, created, metadata_updated, data_updated, startdate, enddate, update_frequency, org, data_link, url, tags, private, requestable, updated_by_script)
        rows.append(row)
    write_list_to_csv("datasets.csv", rows, headers=1)


if __name__ == "__main__":
    facade(main, hdx_site="prod", user_agent="test")

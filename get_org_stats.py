from datetime import datetime

from dateutil.relativedelta import relativedelta
from hdx.data.dataset import Dataset
from hdx.data.organization import Organization
from hdx.facades.simple import facade
from hdx.utilities.dateparse import parse_date
from hdx.utilities.dictandlist import write_list_to_csv


def main():
    organisations = dict()
    for dataset in Dataset.get_all_datasets():
        if dataset["private"]:
            continue
        organisation_name = dataset["organization"]["name"]
        organisation = organisations.get(organisation_name)
        downloads = dataset["total_res_downloads"]
        if not organisation:
            organisation = dataset.get_organization()
            organisations[organisation_name] = organisation
            organisation["downloads"] = downloads
            organisation["datasets"] = 1
        else:
            organisation["downloads"] += downloads
            organisation["datasets"] += 1
    headers = ["Organisation name", "Organisation title", "Downloads", "Datasets", "Followers"]
    rows = list()
    for organisation_name in sorted(organisations):
        organisation = organisations[organisation_name]
        row = [organisation_name, organisation["title"], organisation["downloads"], organisation["datasets"], organisation["num_followers"]]
        rows.append(row)
    if rows:
        write_list_to_csv("admin_stats.csv", rows, headers)


if __name__ == "__main__":
    facade(main, hdx_site="prod", user_agent='test')

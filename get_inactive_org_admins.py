from datetime import datetime

from dateutil.relativedelta import relativedelta
from hdx.data.organization import Organization
from hdx.facades.simple import facade
from hdx.utilities.dateparse import parse_date
from hdx.utilities.dictandlist import write_list_to_csv


def main():
    rows = list()
    for organization_name in Organization.get_all_organization_names():
        organization = Organization.read_from_hdx(organization_name)
        admins = organization.get_users("admin")
        admin_ids = {x["id"] for x in admins}
        organization_id = organization["id"]
        result, activities = organization._read_from_hdx("activity", organization_id, action="organization_activity_list", limit=1000)
        active_admin_ids = set()
        if result:
            for activity in activities:
                user_id = activity["user_id"]
                if user_id in admin_ids:
                    date = parse_date(activity["timestamp"])
                    if date > datetime.now() - relativedelta(years=1):
                        active_admin_ids.add(user_id)
        inactive_admin_ids = admin_ids - active_admin_ids
        inactive_admins = {(x["id"], x["display_name"]) for x in admins if x["id"] in inactive_admin_ids}
        headers = ["Organisation name", "Organisation title", "Inactive admin id", "Inactive admin name"]
        for inactive_admin in inactive_admins:
            row = [organization_name, organization["title"], inactive_admin[0], inactive_admin[1]]
            rows.append(row)
        print(f"Checked organisation: {organization_name}")
        if rows:
            write_list_to_csv("inactive_admins.csv", rows, headers)


if __name__ == "__main__":
    facade(main, hdx_site="prod", user_agent='test')

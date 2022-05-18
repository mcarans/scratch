import copy
from datetime import timedelta

from hdx.data.user import User
from hdx.facades.simple import facade
from hdx.utilities.dateparse import parse_date
from hdx.utilities.dictandlist import write_list_to_csv

start_date = parse_date("2021-01-01")
end_date = parse_date("2021-12-31")


def get_id_name_created(user):
    user_id = user["id"]
    name = user.get("fullname")
    if not name or name == user_id:
        name = user.get("display_name")
        if not name or name == user_id:
            name = user["name"]
    return user_id, name, parse_date(user["created"])


def main():
    rows = list()
    for user in User.get_all_users():
        user_id, user_name, created = get_id_name_created(user)
        if created < start_date or created > end_date:
#            print(f"User: {user_name} outside creation range")
            continue
        organisations = user.get_organizations()
        org_names = ",".join([x["name"] for x in organisations])
        created_str = created.date().isoformat()
        result, activities = user._read_from_hdx(
            "activity", user_id, action="user_activity_list", limit=10
        )
        if not result:
            raise ValueError(f"No activity list returned for {user_name}")
        base_row = [
            user_id,
            user_name,
            created_str,
        ]
        if result:
            no_activities = len(activities)

            def add_row(date_str, activity_type, inactive, msg):
                row = base_row + [date_str, activity_type, org_names, inactive]
                rows.append(row)
                print(msg)

            if no_activities == 0:
                add_row("", "", "Y", f"User: {user_name} has no activities!")
                continue
            activity = activities[0]
            date = parse_date(activity["timestamp"])
            activity_type = activity["activity_type"]
            if no_activities == 1:
                if activity_type != "new user":
                    raise ValueError(f"Only one activity type which is '{activity_type}' not 'new user'!")
                add_row(date.date().isoformat(), activity_type, "Y", f"User: {user_name} is inactive (new user only)!")
                continue
            for activity in activities:
                if activity_type in ("new user", "change user"):
                    activity_type = activity["activity_type"]
                new_date = parse_date(activity["timestamp"])
                if new_date > date:
                    date = new_date
            date_str = date.date().isoformat()
            if date - created > timedelta(days=7):
                add_row(date_str, activity_type, "N", f"User: {user_name} has activity after one week!")
                continue
            if activity_type not in ("new user", "changed user"):
                add_row(date_str, activity_type, "N", f"User: {user_name} has activity that isn't user related!")
                continue
            if len(organisations) == 0:
                add_row(date_str, activity_type, "Y", f"User: {user_name} is inactive!")
            else:
                add_row(date_str, activity_type, "N", f"User: {user_name} is in at least one organisation!")
    if rows:
        headers = [
            "Id",
            "Name",
            "Created",
            "Last Active",
            "Activity Type",
            "Organisations",
            "Inactive",
        ]
        write_list_to_csv("inactive_users.csv", rows, headers)


if __name__ == "__main__":
    facade(
        main,
        hdx_site="prod",
        user_agent="test",
    )

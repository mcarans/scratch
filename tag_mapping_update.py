import json
from os import getenv

import gspread
from hdx.utilities.downloader import Download

oldurl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRjeajloIuQl8mfTSHU71ZgbHSgYYUgHrLqyjHSuQJ-zMqS3SVM9hJqMs72L-84LQ/pub?gid=334970416&single=true&output=csv"
newurl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQJKjr25NZAIQELrFnUhVnL-7SxC8SwW9I6usm5Xvwyw00zRC-DhlLh74EVniX732w_BDFoQLrNDKKL/pub?gid=70008169&single=true&output=csv"
outputurl = "https://docs.google.com/spreadsheets/d/1LRR4oBl5uKmBwbECkZv0JzrUbxHjfHjpulXkkRn-Hco/edit#gid=0"

header = ["Current Tag", "Action to Take", "New Tag(s)"]
rows = list()

downloader = Download(user_agent="test")
headers, iterator = downloader.get_tabular_rows(newurl, dict_form=True)
new_tag_mapping = dict()
mapped_tags = set()
accepted_tags = set()
deleted_tags = set()
for row in iterator:
    current_tag = row["old tags"]
    new_tag = row["new tags"]
    if new_tag == "DELETE":
        rows.append([current_tag, "delete", ""])
        deleted_tags.add(current_tag)
        mapped_tags.add(current_tag)
        continue
    if new_tag != current_tag:
        new_tag_mapping[current_tag] = new_tag
        rows.append([current_tag, "merge", new_tag])
        mapped_tags.add(current_tag)
    if new_tag not in mapped_tags:
        accepted_tags.add(new_tag)
        rows.append([new_tag, "ok", ""])
        mapped_tags.add(new_tag)

headers, iterator = downloader.get_tabular_rows(oldurl, dict_form=True)
for row in iterator:
    old_tag = row["Current Tag"]
    if old_tag in mapped_tags:
        continue
    action = row["Action to Take"]
    if action == "delete":
        rows.append([old_tag, "delete", ""])
        mapped_tags.add(old_tag)
        continue
    if action == "ok":
        new_tag = new_tag_mapping.get(old_tag)
        if new_tag:
            rows.append([old_tag, "merge", new_tag])
            mapped_tags.add(old_tag)
        else:
            print(f"Tag {old_tag} not found in new mapping!")
        continue
    current_tags = row["New Tag(s)"].split(";")
    mappings = set()
    deletions = set()
    for current_tag in current_tags:
        if current_tag in deleted_tags:
            deletions.add(current_tag)
            continue
        if current_tag in accepted_tags:
            mappings.add(current_tag)
            continue
        new_tag = new_tag_mapping.get(current_tag)
        if new_tag:
            mappings.add(new_tag)
        else:
            print(f"Tag {current_tag} not found in new mapping!")

    if mappings:
        rows.append([old_tag, "merge", ";".join(sorted(mappings))])
        mapped_tags.add(old_tag)
    elif deletions:
        rows.append([old_tag, "delete", ""])
        mapped_tags.add(old_tag)
    else:
        print(f"Don't know what to do with {old_tag}!")

gsheet_auth = getenv("GSHEET_AUTH")
info = json.loads(gsheet_auth)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
gc = gspread.service_account_from_dict(info, scopes=scopes)
gsheet = gc.open_by_url(outputurl)

rows = sorted(rows)
outputtagmapping = gsheet.worksheet("Tag Mapping")
outputtagmapping.clear()
outputtagmapping.update("A1", [header] + rows)

a_rows = [[tag] for tag in sorted(accepted_tags)]
taglist = gsheet.worksheet("Full List of Accepted Tags")
taglist.clear()
taglist.update("A1", a_rows)

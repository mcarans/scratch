import json
from os import getenv

import gspread
from hdx.utilities.downloader import Download

# From https://docs.google.com/spreadsheets/d/1yXLu1jE2j6dDQ8bIbHzSH4DTfbIClJ6M_0PHVRqzsL8/edit#gid=334970416
oldurl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQmBj7HFLWhr6Ilvc-na5uqmdEUXYIIgESoQ5JX37PQbFNWkDyNe3LK0P_7htuTy-747sZkC-9DOFOK/pub?gid=334970416&single=true&output=csv"
# From https://docs.google.com/spreadsheets/d/1fTO8T8ZVXU9eoh3EIrw490Z2pX7E59MhHmCvT_cXmNs/edit#gid=70008169
newurl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQJKjr25NZAIQELrFnUhVnL-7SxC8SwW9I6usm5Xvwyw00zRC-DhlLh74EVniX732w_BDFoQLrNDKKL/pub?gid=70008169&single=true&output=csv"
# From https://docs.google.com/spreadsheets/d/1LRR4oBl5uKmBwbECkZv0JzrUbxHjfHjpulXkkRn-Hco/edit#gid=819440074
additional_mappings_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQD3ba751XbWS5GVwdJmzOF9mc7dnm56hE2U8di12JnpYkdseILmjfGSn1W7UVQzmHKSd6p8FWaXdFL/pub?gid=819440074&single=true&output=csv"
outputurl = "https://docs.google.com/spreadsheets/d/1LRR4oBl5uKmBwbECkZv0JzrUbxHjfHjpulXkkRn-Hco/edit#gid=0"

# update this by hand
# https://docs.google.com/spreadsheets/d/1_nhIETuzJhlsNEOv39PhZ66lpENTlfjH/edit?gid=334970416#gid=334970416

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
    if new_tag != current_tag and current_tag not in mapped_tags:
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

headers, iterator = downloader.get_tabular_rows(additional_mappings_url, dict_form=True)
for row in iterator:
    tag = row["Tag"]
    accepted_tag = row["Accepted Tag"]
    if accepted_tag != tag and tag not in mapped_tags:
        new_tag_mapping[tag] = accepted_tag
        rows.append([tag, "merge", accepted_tag])
        mapped_tags.add(tag)

gsheet_auth = getenv("GSHEET_AUTH")
info = json.loads(gsheet_auth)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
gc = gspread.service_account_from_dict(info, scopes=scopes)
gsheet = gc.open_by_url(outputurl)

rows = sorted(rows)
outputtagmapping = gsheet.worksheet("Tag Mapping")
outputtagmapping.clear()
outputtagmapping.update([header] + rows, "A1")

a_rows = [[tag] for tag in sorted(accepted_tags)]
taglist = gsheet.worksheet("Full List of Accepted Tags")
taglist.clear()
taglist.update(a_rows, "A1")

import argparse
import json
from copy import copy
from os import listdir
from os.path import join

from hdx.utilities.loader import load_json


def parse_args():
    parser = argparse.ArgumentParser(description="Shrink HDX JSON test files")
    parser.add_argument("-id", "--inputdir", default=None, help="Directory")
    parser.add_argument("-od", "--outputdir", default=None, help="Directory")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    for filename in listdir(args.inputdir):
        if not filename.endswith(".json"):
            continue
        if "datasets" not in filename:
            continue
        print(f"Processing {filename}")
        jsondata = load_json(join(args.inputdir, filename))
        for item in jsondata:
            for key, value in copy(item).items():
                if key in (
                    "batch",
                    "dataseries_name",
                    "dataset_preview",
                    "isopen",
                    "num_resources",
                    "num_tags",
                    "owner_org",
                    "pageviews_last_14_days",
                    "qa_completed",
                    "solr_additions",
                    "version",
                    "relationships_as_subject",
                    "relationships_as_object",
                    "creator_user_id",
                ):
                    del item[key]
                    continue
                if value is None:
                    del item[key]
                    continue
                if isinstance(value, str):
                    if key in ("notes", "methodology_other", "caveats"):
                        item[key] = value[:20]
                elif isinstance(value, dict):
                    for key2, value2 in copy(value).items():
                        if key2 in ("is_organization", "image_url", "approval_status"):
                            del item[key][key2]
                            continue
                        if value2 is None:
                            del item[key][key2]
                            continue
                        if isinstance(value2, str):
                            if key2 in ("description",):
                                item[key][key2] = value2[:20]
                elif isinstance(value, list):
                    for i, item2 in enumerate(value):
                        for key2, value2 in copy(item2).items():
                            if value2 is None:
                                del item[key][i][key2]
                                continue
                            if key2 in (
                                "originalHash",
                                "package_id",
                                "position",
                                "vocabulary_id",
                                "datastore_active",
                                "hdx_rel_url",
                                "microdata",
                                "resource_type",
                                "image_display_url",
                                "fs_check_info",
                            ):
                                del item[key][i][key2]
                                continue
                            if isinstance(value2, str):
                                if key2 in ("description",):
                                    item[key][i][key2] = value2[:20]

        with open(join(args.outputdir, filename), "w", encoding="utf-8") as f:
            json.dump(
                jsondata,
                f,
                indent=None,
                sort_keys=False,
                separators=(",", ":"),
            )

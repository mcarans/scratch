from hdx.data.dataset import Dataset
from hdx.facades.simple import facade


def main():
    datasets = Dataset.search_in_hdx(fq="organization:iati")
    count = 0
    for dataset in datasets:
        title = dataset["title"]
        if title.startswith("Current IATI aid activities in "):
            count += 1
            print(title, dataset.get_hdx_url())
            for resource in dataset.get_resources():
                url = resource["url"]
                url = url.replace("https://proxy.hxlstandard.org/data/c8ba28.csv?url=", "https://proxy.hxlstandard.org/data.csv?dest=data_edit&filter01=select&select-query01-01=status%3D2&filter02=cut&cut-skip-untagged02=on&filter03=add&add-tag03=%23activity%2Burl&add-value03=%7B%7B%23activity%2Bid%7D%7D&add-header03=activity_url&filter04=replace&replace-pattern04=%5E.%2Aaid%3D%28.%2A%29%24&replace-regex04=on&replace-value04=%5C1&replace-tags04=activity%2Bid&filter05=dedup&tagger-match-all=on&tagger-01-header=aid&tagger-01-tag=%23activity%2Bid&tagger-02-header=reporting&tagger-02-tag=%23org%2Breporting%2Bname&tagger-03-header=reporting_ref&tagger-03-tag=%23org%2Breporting%2Bcode&tagger-04-header=funder_ref&tagger-04-tag=%23org%2Bfunding%2Bcode&tagger-07-header=status_code&tagger-07-tag=%23status&tagger-08-header=day_start&tagger-08-tag=%23date%2Bstart&tagger-09-header=day_end&tagger-09-tag=%23date%2Bend&tagger-11-header=description&tagger-11-tag=%23description&tagger-21-header=country_code&tagger-21-tag=%23country%2Bname&tagger-23-header=sector_group&tagger-23-tag=%23sector&tagger-24-header=sector_code&tagger-24-tag=%23subsector&tagger-26-header=location_latitude&tagger-26-tag=%23geo%2Blat&tagger-27-header=location_longitude&tagger-27-tag=%23geo%2Blon&tagger-28-header=location_name&tagger-28-tag=%23loc%2Bname&name=IATI+D-Portal+HXL+conversion+filter&header-row=1&url=")
                resource["url"] = url
            dataset.update_in_hdx()
    print("total datasets %d updated!" % count)


if __name__ == "__main__":
    facade(main, hdx_site="prod", user_agent="test")

from os.path import join, expanduser

from dateutil.relativedelta import relativedelta
from hdx.data.dataset import Dataset
from hdx.facades.simple import facade
from hdx.utilities.downloader import Download


def main():
    datasetinfo = {
        "name": "hotosm_npl_roads",
        "title": "Nepal Roads (OpenStreetMap Export)",
        "owner_org": "225b9f7d-e7cb-4156-96a6-44c9c58d31e3",
        "maintainer": "6a0688ce-8521-46e2-8edd-8e26c0851ebd",
        "dataset_source": "OpenStreetMap contributors",
        "methodology": "Other",
        "methodology_other": "Volunteered geographic information",
        "license_id": "hdx-odc-odbl",
        "updated_by_script": "Hotosm OSM Exports (2024-03-28T15:18:44)",
        "caveats": "OpenStreetMap data is crowd sourced and cannot be considered to be exhaustive",
        "private": False,
        "notes": "OpenStreetMap contains roughly 279.1 thousand km of roads in this region. Based on AI-mapped estimates, this is approximately 84 % of the total road length in the dataset region. The average age of data for the region is 2 years  ( Last edited 6 days ago ) and 8% of roads were added or updated in the last 6 months.\nRead about what this summary means : [indicators](https://github.com/hotosm/raw-data-api/tree/develop/docs/src/stats/indicators.md) , [metrics](https://github.com/hotosm/raw-data-api/tree/develop/docs/src/stats/metrics.md)\n\nOpenStreetMap exports for use in GIS applications.\n\nThis theme includes all OpenStreetMap features in this area matching ( Learn what tags means [here](https://wiki.openstreetmap.org/wiki/Tags) ) :\n\ntags['highway'] IS NOT NULL\n\nFeatures may have these attributes:\n\n- [name](http://wiki.openstreetmap.org/wiki/Key:name)\n- [highway](http://wiki.openstreetmap.org/wiki/Key:highway)\n\nThis dataset is one of many [OpenStreetMap exports on\nHDX](https://data.humdata.org/organization/hot).\nSee the [Humanitarian OpenStreetMap Team](http://hotosm.org/) website for more\ninformation.\n",
        "subnational": 0,
        "data_update_frequency": "-2",
        "groups": [
            {
                "name": "npl"
            }
        ],
        "tags": [
            {
                "name": "roads",
                "vocabulary_id": "b891512e-9516-4bf5-962a-7a289772a2a1"
            },
            {
                "name": "transportation",
                "vocabulary_id": "b891512e-9516-4bf5-962a-7a289772a2a1"
            },
            {
                "name": "geodata",
                "vocabulary_id": "b891512e-9516-4bf5-962a-7a289772a2a1"
            }
        ],
        "resources": [
            {
                "name": "hotosm_npl_roads_lines_geojson.zip",
                "url": "exports/262bbdc95d814a12ac40eb808cfa9f69/ISO3/NPL/roads/lines/hotosm_npl_roads_lines_geojson.zip",
                "format": "geojson",
                "description": "GeoJSON",
                "size": 1393075,
                "last_modifed": "2024-03-28T15:18:44.243445",
                "resource_type": "api",
                "url_type": "api"
            }
        ]
    }
    dataset = Dataset(datasetinfo)
    dataset.update_in_hdx(hxl_update=False)


if __name__ == '__main__':
    facade(
        main,
        hdx_site="demo",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="test",
    )

from os.path import join, expanduser

from hapi_schema.db_humanitarian_needs import DBHumanitarianNeeds
from hdx.data.dataset import Dataset
from hdx.facades.simple import facade
from hdx.utilities.downloader import Download


def get_admin2_ref(countryiso3, row):
    adm1_code = row["Admin1 PCode"]
    adm2_code = row["Admin2 PCode"]
    return ""


def main():
    with Download() as retriever:
        datasets = Dataset.search_in_hdx(fq="name:hno-data-for-*")
        for dataset in datasets:
            countryiso3 = dataset.get_location_iso3s()[0]
            time_period = dataset.get_time_period()
            time_period_start = time_period["startdate_str"],
            time_period_end = time_period_end["enddate_str"]
            resource = dataset.get_resource()
            resource_id = resource["id"]
            url = resource["url"]
            headers, rows = retriever.get_tabular_rows(url, dict_form=True)
            # Admin 1 PCode,Admin 2 PCode,Sector,Gender,Age Group,Disabled,Population Group,Population,In Need,Targeted,Affected,Reached
            for row in rows:
                admin2_ref = get_admin2_ref(countryiso3, row)
                population_group_code = row["Population Group"]
                sector_code = row["Sector"]
                gender_code = row["Gender"]
                age_range_code = row["Age Group"]
                disabled_marker = row["Disabled"]
                humanitarian_needs_row = DBHumanitarianNeeds(
                    resource_ref=resource_id,
                    admin2_ref=self._admins.admin2_data[admin2_code],
                    population_status_code=population_status_code,
                    population_group_code=population_group_code,
                    sector_code=sector_code,
                    gender_code=gender_code,
                    age_range_code=age_range_code,
                    disabled_marker=disabled_marker,
                    population=value,
                    reference_period_start=time_period_start,
                    reference_period_end=time_period_end,
                    # TODO: For v2+, add to scraper (HAPI-199)
                    source_data="not yet implemented",
                )
                base_row = [
                    resource_id,
                    admin2_ref,
                    None,
                    population_group_code,
                    sector_code,
                    gender_code,
                    age_range_code,
                    disabled_marker,
                    None,
                    time_period["startdate_str"],
                    time_period["enddate_str"],
                ]

                def create_row(in_col, status):
                    out_row = copy(base_row)
                    population = row[in_col]
                    if population != "":
                        out_row[2] = status
                        out_row[8] = population
                        values.append(out_row)

                create_row("Population", "population")
                create_row("Affected", "affected")
                create_row("In Need", "inneed")
                create_row("Targeted", "targeted")
                create_row("Reached", "reached")


if __name__ == '__main__':
    facade(
        main,
        hdx_site="stage",
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="test",
    )

import logging
from os.path import expanduser, join

from hdx.facades.infer_arguments import facade
from hdx.location.adminlevel import AdminLevel
from hdx.utilities.base_downloader import DownloadError
from hdx.utilities.downloader import Download
from hdx.utilities.easy_logging import setup_logging
from hdx.utilities.path import temp_dir
from hdx.utilities.retriever import Retrieve
from hdx.utilities.saver import save_yaml


setup_logging()
logger = logging.getLogger(__name__)


def main(access_token: str, save: bool = False, use_saved: bool = False) -> None:
    """Generate datasets and create them in HDX

    Args:
        access_token (str): HPC access token
        save (bool): Save downloaded data. Defaults to False.
        use_saved (bool): Use saved data. Defaults to False.

    Returns:
        None
    """
    with temp_dir(
        "test_hpc_hno", delete_on_success=True, delete_on_failure=False
    ) as folder:
        with Download(
            extra_params_yaml=join(expanduser("~"), ".extraparams.yml"),
            extra_params_lookup="hdx-scraper-fts",
            rate_limit={"calls": 1, "period": 1},
        ) as downloader:
            retriever = Retrieve(
                downloader, folder, "saved_data", folder, save, use_saved
            )
            hpcapi = "https://api.hpc.tools/v2/"

            json = retriever.download_json(
                f"{hpcapi}fts/flow/plan/overview/progress/2024"
            )
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}",
            }
            downloader.session.auth = None

            for plan in json["data"]["plans"]:
                planid = plan["id"]
                if plan["planType"]["name"] != "Humanitarian response plan":
                    continue
                countries = plan["countries"]
                if len(countries) != 1:
                    continue
                countryiso3 = countries[0]["iso3"]
                # if countryiso3 != "AFG":
                #     continue
                logger.info(f"Processing {countryiso3}")
                try:
                    json = retriever.download_json(
                        f"{hpcapi}plan/{planid}/responseMonitoring?includeCaseloadDisaggregation=true&includeIndicatorDisaggregation=false&disaggregationOnlyTotal=false",
                        headers=headers,
                    )
                except DownloadError as err:
                    logger.exception(err)
                    continue
                data = json["data"]
                location_mapping = {}
                valid_pcodes = 0
                invalid_pcodes = 0
                for location in data["locations"]:
                    adminlevel = location.get("adminLevel")
                    if adminlevel is None or adminlevel > 2:
                        continue
                    if adminlevel != 0:
                        if AdminLevel.looks_like_pcode(location["pcode"]):
                            valid_pcodes += 1
                        else:
                            invalid_pcodes += 1
                    location_mapping[location["id"]] = location
                if valid_pcodes / (valid_pcodes + invalid_pcodes) > 0.9:
                    process_adm = True
                else:
                    logger.error(f"Country {countryiso3} has many invalid pcodes!")
                    process_adm = False
                errors = []
                country_results = {}
                for caseload in data["caseloads"]:
                    caseload_results = {"national": {}}
                    national_total = {}
                    key = None
                    if "totalPopulation" in caseload:
                        key = "population"
                        national_total[key] = national_total.get(key, 0) + 1
                    if "inNeed" in caseload:
                        key = "inneed"
                        national_total[key] = national_total.get(key, 0) + 1
                    if "target" in caseload:
                        key = "targeted"
                        national_total[key] = national_total.get(key, 0) + 1
                    if "affected" in caseload:
                        key = "affected"
                        national_total[key] = national_total.get(key, 0) + 1
                    if "expectedReach" in caseload:
                        key = "reached"
                        national_total[key] = national_total.get(key, 0) + 1
                    if national_total:
                        caseload_results["national"]["total"] = national_total
                    for attachment in caseload["disaggregatedAttachments"]:
                        location_id = attachment["locationId"]
                        location = location_mapping.get(location_id)
                        if not location:
                            error = f"Location {location_id} in {countryiso3} does not exist!"
                            if error not in errors:
                                errors.append(error)
                                logger.error(error)
                            continue
                        adminlevel = location.get("adminLevel")
                        if adminlevel is None or adminlevel > 2:
                            continue
                        if adminlevel == 0:
                            results = caseload_results.get("national", {})
                            caseload_results["national"] = results
                        elif not process_adm:
                            continue
                        else:
                            key = f"adm{adminlevel}"
                            results = caseload_results.get(key, {})
                            caseload_results[key] = results
                        category_name = attachment["categoryLabel"].lower()
                        category = results.get(category_name, {})
                        for population_status in attachment["dataMatrix"]:
                            match population_status["metricType"]:
                                case "totalPopulation":
                                    key = "population"
                                case "inNeed":
                                    key = "inneed"
                                case "target":
                                    key = "targeted"
                                case "affected":
                                    key = "affected"
                                case "expectedReach":
                                    key = "reached"
                            if key:
                                category[key] = category.get(key, 0) + 1
                        if category:
                            results[category_name] = category
                    country_results[caseload["caseloadCustomRef"]] = caseload_results
                save_yaml(country_results, join("hpc_hno", f"{countryiso3}.yaml"))


if __name__ == "__main__":
    facade(
        main,
        user_agent="test",
    )

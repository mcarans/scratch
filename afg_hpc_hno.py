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
        "test_afg_hpc_hno", delete_on_success=True, delete_on_failure=False
    ) as folder:
        with Download(
            rate_limit={"calls": 1, "period": 1},
        ) as downloader:
            retriever = Retrieve(
                downloader, folder, "saved_data", folder, save, use_saved
            )
            hpcapi = "https://api.hpc.tools/v2/"

            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}",
            }

            json = retriever.download_json(
                f"{hpcapi}plan/1117/responseMonitoring?includeCaseloadDisaggregation=true&includeIndicatorDisaggregation=false&disaggregationOnlyTotal=false",
                headers=headers,
            )

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
            logger.info(f"{valid_pcodes} valid pcodes and {invalid_pcodes} invalid pcodes!")

            data = {}
            for caseload in data["caseloads"]:
                sector = caseload["caseloadDescription"]
                statuses = []

                def status_check(status):
                    value = caseload.get(status)
                    if value is not None:
                        statuses.append(status)

                status_check("totalPopulation")
                status_check("inNeed")
                status_check("affected")
                status_check("target")
                status_check("expectedReach")

                sector_data = {"statuses": statuses}
                data[sector]= sector_data

                for

if __name__ == "__main__":
    facade(
        main,
        user_agent="test",
    )

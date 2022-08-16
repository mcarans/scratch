from os.path import expanduser, join

from hdx.utilities.loader import load_yaml
from mixpanel_utils import MixpanelUtils

home_folder = expanduser("~")
configuration = load_yaml(join(home_folder, ".mixpanel.yml"))
mputils = MixpanelUtils(
    configuration["api_secret"],
    project_id=configuration["project_id"],
    token=configuration["token"],
)

jql_query = """
function main() {
  return Events({
    from_date: '2016-08-01',
    to_date: '2022-08-15',
    event_selectors: [{event: "resource download"}]
  })
  .groupByUser(["properties.resource id","properties.dataset id",mixpanel.numeric_bucket('time',mixpanel.daily_time_buckets)],mixpanel.reducer.null())
  .groupBy(["key.2"], mixpanel.reducer.count())
    .map(function(r){
    return {
      dataset_id: r.key[0],
      value: r.value
    };
  });
}"""

result = mputils.query_jql(jql_query)
print(result)

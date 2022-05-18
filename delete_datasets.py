from hdx.data.dataset import Dataset
from hdx.facades.simple import facade

datasets_to_delete = ['fts-ebola-indicator', 'sidih-indicators', 'key-humanitarian-figure', 'wfp-vam-live-data', 'raw-fts-ebola-input', 'iraq-2014-2015-humanitarian-contributions', 'mdginfo-2012', 'who-gar-raw', 'food-shipments', 'producer-prices-annual', 'food-security', 'producer-price-indices-annual', 'average-monthly-temperature-and-rainfall-all-africa', 'undp-climate-change-country-profiles-all-africa', 'daily-summaries-of-precipitation-indicators-for-iceland', 'daily-summaries-of-precipitation-indicators-for-croatia', 'daily-summaries-of-precipitation-indicators-for-estonia', 'daily-summaries-of-precipitation-indicators-for-germany', 'daily-summaries-of-precipitation-indicators-for-austria', 'daily-summaries-of-precipitation-indicators-for-ireland', 'daily-summaries-of-precipitation-indicators-for-hungary', 'daily-summaries-of-precipitation-indicators-for-greenland', 'daily-summaries-of-precipitation-indicators-for-gibraltar', 'daily-summaries-of-precipitation-indicators-for-france', 'daily-summaries-of-precipitation-indicators-for-finland', 'daily-summaries-of-precipitation-indicators-for-denmark', 'daily-summaries-of-precipitation-indicators-for-bulgaria', 'daily-summaries-of-precipitation-indicators-for-belgium', 'daily-summaries-of-precipitation-indicators-for-antarctica', 'daily-summaries-of-precipitation-indicators-for-czech-republic', 'daily-summaries-of-precipitation-indicators-for-falkland-islands--malvinas-', 'daily-summaries-of-precipitation-indicators-for-bosnia-and-herzegovina', 'daily-summaries-of-precipitation-indicators-for-french-southern-territories', 'daily-summaries-of-precipitation-indicators-for-greece', 'daily-summaries-of-precipitation-indicators-for-georgia', 'daily-summaries-of-precipitation-indicators-for-cyprus', 'fts-clusters', 'ops-projects-with-targets', 'ors-key-figure', 'country-framework-with-targets', 'afghanistan-2015-humanitarian-contributions', 'cameroon-2015-humanitarian-contributions', 'nigeria-2015-humanitarian-contributions', 'mali-2015-humanitarian-contributions', 'chad-2015-humanitarian-contributions', 'ukraine-2015-humanitarian-contributions', 'central-african-republic-2015-humanitarian-contributions', 'somalia-2015-humanitarian-contributions', 'sudan-2015-humanitarian-contributions', 'democratic-republic-of-congo-2015-humanitarian-contributions', 'south-sudan-2015-humanitarian-contributions', 'occupied-palestinian-territory-2015-humanitarian-contributions', 'burkina-faso-2015-humanitarian-contributions', 'niger-2015-humanitarian-contributions', 'unhcr-information-portal-data']


def main():
    for i, dataset_name in enumerate(datasets_to_delete):
        dataset = Dataset.read_from_hdx(dataset_name)
        if dataset:
            print(i, dataset['title'])
            dataset.delete_from_hdx()
            dataset.get_resource()


if __name__ == '__main__':
    facade(main, hdx_site='test', user_agent='test')

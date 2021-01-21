from common.consts import SYSTEM_KEY, MULTIPLE_FARMS
from common.utils.utils import marker_wrapper_printer
from data.ETLs.Factory.ExtractorsFactory import ExtractorsFactory
from data.ETLs.Factory.LoaderFactory import LoadersFactory
from data.ETLs.Factory.TransformerFactory import TransformersFactory


class ETLRunner:
    def __init__(self, flow, token, farm=None, start_date=None, end_date=None, accounts=None, **kwargs):
        self.farm = farm
        self.accounts = accounts
        self._token = token
        self.start_date = start_date
        self.end_date = end_date
        self._flow = flow
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _extract(self) -> list:
        extractor_class = ExtractorsFactory.get_extractor_class(self._flow)
        extractor = extractor_class(farm=self.farm, start_date=self.start_date, end_date=self.end_date,
                                    token=self._token, accounts=self.accounts)
        extractor.system_key = self.system_key if hasattr(self, SYSTEM_KEY) else None
        extractor._multiple_farms = self.multiple_farms if hasattr(self, MULTIPLE_FARMS) else None
        data = extractor.extract()
        return data

    def _transform(self, data):
        transformer = TransformersFactory.get_transformer_class(self._flow)
        transformed_data = transformer(farm=self.farm, data=data).transform()
        return transformed_data

    def _load(self):
        marker_wrapper_printer(f"running {self._flow}")
        extracted_data = self._extract()
        marker_wrapper_printer('Transforming data')
        transformed_data = self._transform(extracted_data) if extracted_data is not None else None
        if transformed_data is None:
            marker_wrapper_printer(f'no data was found on {self._flow}')
            return None
        else:
            loader = LoadersFactory.get_loader_class(flow=self._flow)
            marker_wrapper_printer('Loading...')
            data = loader(transformed_data=transformed_data, farm=self.farm).load()  # noqa
            marker_wrapper_printer('Done!')
            return data

    def run_etl_flow(self):
        return self._load()

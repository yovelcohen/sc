from common.utils.utils import convert_camel_to_snake_case


class BaseTransformer:
    def __init__(self, farm, data):
        self.farm = farm
        self.data = data

    def transform(self):
        raise NotImplementedError

    def convert_cols_names_to_snake_case(self, df):
        """
        converts a dataframe's columns names to snake case
        """
        df.columns = df.columns.to_series().apply(convert_camel_to_snake_case)
        return df

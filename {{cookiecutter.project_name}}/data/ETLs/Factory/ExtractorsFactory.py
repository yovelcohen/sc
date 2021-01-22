from data.ETLs.Factory.Flows import ETLFlows  # noqa


class ExtractorsFactory:
    _extractors = {}

    @classmethod
    def get_extractor_class(cls, flow):
        try:
            return cls._extractors[flow]
        except KeyError:
            raise TypeError(f"the flow: {flow} has not been implemented on Extractors Factory")

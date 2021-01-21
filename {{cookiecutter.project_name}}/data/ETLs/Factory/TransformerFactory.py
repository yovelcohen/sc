class TransformersFactory:
    _transformers = {}

    @classmethod
    def get_transformer_class(cls, flow):
        try:
            return cls._transformers[flow]
        except KeyError:
            raise TypeError(f"the flow: {flow} has not been implemented on Transformers Factory")

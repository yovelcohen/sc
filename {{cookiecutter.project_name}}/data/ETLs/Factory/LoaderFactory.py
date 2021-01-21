

class LoadersFactory:
    _loaders = {}

    @classmethod
    def get_loader_class(cls, flow):
        try:
            return cls._loaders[flow]
        except KeyError:
            raise TypeError(f"the flow: {flow} has not been implemented on Loaders Factory")
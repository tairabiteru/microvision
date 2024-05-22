import toml


class Config:
    def __init__(self, path="./conf.toml", d=None):
        if d is not None:
            self._conf = d
        else:
            self._conf = toml.load(path)

        for key, item in self._conf.items():
            if isinstance(item, dict):
                setattr(self, key.lower(), Config(d=item))
            else:
                if key.lower() in ['front_min_size', 'side_min_size']:
                    item = tuple(map(int, item.lower().split("x")))

                setattr(self, key.lower(), item)
            
            
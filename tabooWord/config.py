import yaml
import glob

def get_config(fname):
    with open(fname, "r") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf

class Conf():
    """
    Represents configuration options' group, works like a dict
    """

    def __init__(self):
        self._root_path = "./config"
        self._layer_0 = []
        self._load_config()

    def _load_config(self):
        # load core config files
        _ = glob.glob(f"{self._root_path}/*.yml")
        for conf in _:
            val = get_config(conf)
            name = conf.split('\\')[-1].split('.')[0]
            #print(conf)
            self._layer_0.append(name)
            setattr(self, name, val)
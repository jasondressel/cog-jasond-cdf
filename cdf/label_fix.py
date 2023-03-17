from cdf.utils import GetClient

client = GetClient()

user_names= [
    "aker",
    "jason",
    "kiran",
    "hector",
    "salvador",
    "omar",
    "victor",
    "luis",
    "otoniel",
    "vruiz",
    "emamani",
    "sroque",
    "cespinosa",
    "jmartinez",
    "nramirez",
    "svasquez",
    "mbenites",
    "ecabrera",
    "frodriguez",
]

from cognite.client.data_classes import LabelDefinition
labels = [LabelDefinition(external_id=name.upper(), name=name.upper(), data_set_id=137409537563188) for name in user_names] 
client.labels.create(labels)

pass

aker_assets = [
    ("salvador", "salvador-valhall-6687602007296940"),
    ("frodriguez", "frodriguez-valhall-6687602007296940"),
    ("otoniel", "otoniel-valhall-6687602007296940"),
    ("jason", "jason-valhall-6687602007296940"),
    ("hector", "hector-valhall-6687602007296940"),
    ("vruiz", "vruiz-valhall-6687602007296940"),
    ("victor", "victor-valhall-6687602007296940"),
    ("omar", "omar-valhall-6687602007296940"),
    ("sroque", "sroque-valhall-6687602007296940")
]

from cognite.client.data_classes.assets import Asset
from cognite.client.data_classes.labels import Label

aker_root: Asset
for asset in aker_assets:
    aker_root = client.assets.retrieve(external_id=asset[1])
    aker_root.name = f"Aker BP {asset[0]}"
    #aker_root.labels = [Label(external_id={asset[0].upper()})]
    client.assets.update(aker_root)

aker_root = client.assets.retrieve(external_id="6687602007296940")
aker_root.name = f"Aker BP DONOT USE"
#aker_root.labels = [Label(external_id="SHARED")]
client.assets.update(aker_root)
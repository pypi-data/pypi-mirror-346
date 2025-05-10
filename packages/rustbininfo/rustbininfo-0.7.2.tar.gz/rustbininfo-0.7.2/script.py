from rich import print

from rustbininfo import Crate

c = Crate.from_depstring("tokio-1.29.0", False)
print(c)
print(c.download_untar())

import pathlib

import settings

pathlib.Path(settings.LOG_DIR).mkdir(exist_ok=True)

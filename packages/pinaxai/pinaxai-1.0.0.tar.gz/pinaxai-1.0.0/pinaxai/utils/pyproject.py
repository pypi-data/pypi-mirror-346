from pathlib import Path
from typing import Dict, Optional

from pinaxai.utils.log import log_debug, logger


def read_pyproject_pinaxai(pyproject_file: Path) -> Optional[Dict]:
    log_debug(f"Reading {pyproject_file}")
    try:
        import tomli

        pyproject_dict = tomli.loads(pyproject_file.read_text())
        pinaxai_conf = pyproject_dict.get("tool", {}).get("pinaxai", None)
        if pinaxai_conf is not None and isinstance(pinaxai_conf, dict):
            return pinaxai_conf
    except Exception as e:
        logger.error(f"Could not read {pyproject_file}: {e}")
    return None

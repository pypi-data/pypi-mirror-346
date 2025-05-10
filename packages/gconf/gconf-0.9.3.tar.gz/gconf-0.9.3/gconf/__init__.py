import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Union, List

from .gconf import NO_DEFAULT, DELETED, GConf

log = logging.getLogger(__name__)

_global_gconf = GConf()


def load(*configs: Union[Path, str], required=True) -> List[Path]:
	return _global_gconf.load(*configs, required=required)


def load_first(*configs: Union[Path, str], required=True) -> Path:
	return _global_gconf.load_first(*configs, required=required)


def add(dict_: dict):
	return _global_gconf.add(dict_)


def set_env_prefix(prefix: str | None):
	_global_gconf.env_var_prefix = prefix


@contextmanager
def override_conf(dict_: dict):
	global _global_gconf
	stored_gconf = _global_gconf
	_global_gconf = _global_gconf.clone()
	_global_gconf.add(dict_)
	try:
		yield
	finally:
		_global_gconf = stored_gconf


def reset():
	_global_gconf.reset()


def get(*args: str, default=NO_DEFAULT):
	return _global_gconf.get(*args, default=default)

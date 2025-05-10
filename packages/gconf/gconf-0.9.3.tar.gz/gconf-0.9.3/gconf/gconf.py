import itertools
import logging
from contextlib import contextmanager
from copy import deepcopy
from os import environ
from pathlib import Path
from typing import Union, List

import yaml

from .util import update, env_var_key, deep_get

log = logging.getLogger(__name__)

DELETED = object()  # Sentinel
NO_DEFAULT = object()  # Sentinel


class GConf:
	def __init__(self, *initial_configs: Union[Path, str]):
		self._dict: dict = {}
		self.env_var_prefix = 'GCONF'
		self.load(*initial_configs)

	def load(self, *configs: Union[Path, str], required=True) -> List[Path]:
		paths = [Path(config) for config in configs]

		non_existing = [p for p in paths if not p.exists()]
		if required and non_existing:
			raise FileNotFoundError(', '.join([str(p.resolve()) for p in non_existing]))

		existing = [p for p in paths if p.exists()]
		for p in existing:
			with open(p) as c:
				log.debug(f'Loading config from {p}')
				loaded_dict = yaml.safe_load(c)
				if loaded_dict:
					update(self._dict, loaded_dict)

		return existing

	def load_first(self, *configs: Union[Path, str], required=True) -> Path:
		paths = [Path(config) for config in configs]

		for p in paths:
			if p.exists():
				if not p.is_file():
					raise FileNotFoundError(p.resolve())

				loaded = self.load(p, required=False)
				if loaded:
					return loaded[0]

		if required:
			raise FileNotFoundError(', '.join(str(p.resolve()) for p in paths))

	def add(self, dict_: dict):
		update(self._dict, dict_)

	@contextmanager
	def override_conf(self, dict_: dict):
		override_dict = deepcopy(self._dict)
		update(override_dict, dict_)
		yield override_dict

	def reset(self):
		self._dict = {}

	def clone(self):
		result = GConf()
		result.add(deepcopy(self._dict))
		return result

	def get(self, *args: str, default=NO_DEFAULT):
		split_args = list(itertools.chain(*[a.split('.') for a in args]))

		try:
			try:
				return environ[env_var_key(split_args, prefix=self.env_var_prefix)]
			except KeyError:
				pass

			try:
				result = deep_get(split_args, self._dict)
			except KeyError as e:
				raise KeyError('.'.join(split_args)) from e

			if result is DELETED:
				raise KeyError('.'.join(split_args))
			else:
				return result

		except KeyError:
			if default is not NO_DEFAULT:
				return default
			else:
				raise

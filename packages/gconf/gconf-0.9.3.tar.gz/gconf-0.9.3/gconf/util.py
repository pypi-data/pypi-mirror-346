from typing import List, Union, Mapping, Sequence


def update(d: dict, u: Mapping):
	for k, v in u.items():
		if isinstance(v, Mapping):
			d[k] = update(d.get(k, None) or {}, v)
		else:
			d[k] = v
	return d


def deep_get(keys: List[str], container: Union[Mapping, Sequence]):
	if len(keys) == 0:
		return container
	elif isinstance(container, Mapping):
		next_value = container[keys[0]]
	elif isinstance(container, Sequence):
		i = int(keys[0])
		next_value = container[i]
	else:
		raise KeyError(keys[0])

	return deep_get(keys[1:], next_value)


def env_var_key(keys: List[str], prefix):
	key = '_'.join(k.upper().replace(' ', '_') for k in keys)
	if prefix is None:
		return key
	else:
		return f'{prefix}_{key}'

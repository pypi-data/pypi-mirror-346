from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from functools import cached_property
from pathlib import Path
from typing import Optional, Union

import orjson
from hugedict.sqlite import SqliteDict, SqliteDictFieldType
from loguru import logger


class GlobalStorage:
    """For storing actor states"""

    instance: Optional[GlobalStorage] = None

    def __init__(self, workdir: Path):
        self.workdir = workdir
        # register base paths to abstract away the exact locations of disk paths
        # similar to prefix & namespace
        self.registered_base_paths: dict[str, Path] = {}

    @staticmethod
    def get_instance():
        if GlobalStorage.instance is None:
            raise Exception("GlobalStorage must be initialized before using")
        return GlobalStorage.instance

    @staticmethod
    def init(workdir: Union[Path, str], verbose: bool = True):
        if GlobalStorage.instance is not None:
            # allow calling re-initialization if the workdir is the same
            if GlobalStorage.instance.workdir != Path(workdir):
                raise ValueError(
                    f"Cannot reinitialize GlobalStorage with workdir: {workdir}. It is already initialized with {GlobalStorage.instance.workdir}"
                )
        else:
            if verbose:
                logger.info("GlobalStorage: {}", workdir)
            Path(workdir).mkdir(exist_ok=True, parents=True)
            GlobalStorage.instance = GlobalStorage(Path(workdir))
        return GlobalStorage.instance

    def to_dict(self):
        return {
            "workdir": str(self.workdir),
            "registered_base_paths": {
                k: str(v) for k, v in self.registered_base_paths.items()
            },
        }

    @cached_property
    def key_mapping(self):
        return SqliteDict(
            self.workdir / "key_mapping.sqlite",
            keytype=SqliteDictFieldType.bytes,
            ser_value=lambda x: orjson.dumps(asdict(x)),
            deser_value=lambda x: MappedKey(**orjson.loads(x)),
        )

    def shorten_key(self, long_key: str):
        """Shorten the key to a shorter version"""
        if long_key in self.key_mapping:
            return self.key_mapping[long_key].short_key

        # shorten the key
        short_key = hashlib.sha256(long_key.encode()).hexdigest()[:8]
        if short_key in self.key_mapping:
            # if the short key already exists, we have an error
            raise Exception(
                f"Collision! Two keys {long_key} and {self.key_mapping[short_key].long_key} have the same short key: {short_key}"
            )
        self.key_mapping[long_key] = MappedKey(long_key=long_key, short_key=short_key)
        self.key_mapping[short_key] = MappedKey(long_key=long_key, short_key=short_key)

        return short_key


@dataclass
class MappedKey:
    long_key: str
    short_key: str

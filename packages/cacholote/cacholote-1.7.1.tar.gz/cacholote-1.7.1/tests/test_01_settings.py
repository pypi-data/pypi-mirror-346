from __future__ import annotations

import contextlib
import datetime
import os
import pathlib
from typing import Any

import pytest
import sqlalchemy as sa

from cacholote import config

does_not_raise = contextlib.nullcontext


def test_change_sessionmaker(tmp_path: pathlib.Path) -> None:
    old_sessionmaker = config.get().instantiated_sessionmaker
    new_db = "sqlite:///" + str(tmp_path / "dummy.db")

    with config.set(cache_db_urlpath=new_db):
        new_sessionmaker = config.get().instantiated_sessionmaker
        assert new_sessionmaker is not old_sessionmaker
    assert config.get().instantiated_sessionmaker is old_sessionmaker

    with config.set(sessionmaker=new_sessionmaker):
        assert config.get().instantiated_sessionmaker is new_sessionmaker
    assert config.get().instantiated_sessionmaker is old_sessionmaker

    config.set(cache_db_urlpath=new_db)
    assert config.get().instantiated_sessionmaker is new_sessionmaker

    config.set(sessionmaker=old_sessionmaker)
    assert config.get().instantiated_sessionmaker is old_sessionmaker


def test_change_cache_db_urlpath(tmp_path: pathlib.Path) -> None:
    old_db = config.get().cache_db_urlpath
    new_db = "sqlite:///" + str(tmp_path / "dummy.db")

    with config.set(cache_db_urlpath=new_db):
        assert str(config.get().engine.url) == config.get().cache_db_urlpath == new_db
    assert str(config.get().engine.url) == config.get().cache_db_urlpath == old_db

    config.set(cache_db_urlpath=new_db)
    assert str(config.get().engine.url) == config.get().cache_db_urlpath == new_db


@pytest.mark.parametrize(
    "key, reset",
    [
        ("cache_db_urlpath", True),
        ("create_engine_kwargs", True),
        ("cache_files_urlpath", False),
    ],
)
def test_set_engine_and_sessionmaker(
    tmp_path: pathlib.Path, key: str, reset: bool
) -> None:
    old_engine = config.get().engine
    old_sessionmaker = config.get().instantiated_sessionmaker

    kwargs: dict[str, Any] = {}
    if key == "cache_db_urlpath":
        kwargs[key] = "sqlite:///" + str(tmp_path / "dummy.db")
    elif key == "create_engine_kwargs":
        kwargs[key] = {"pool_recycle": 60}
    elif key == "cache_files_urlpath":
        kwargs[key] = str(tmp_path / "dummy_files")
    else:
        raise ValueError

    with config.set(**kwargs):
        if reset:
            assert config.get().engine is not old_engine
            assert config.get().instantiated_sessionmaker is not old_sessionmaker
        else:
            assert config.get().engine is old_engine
            assert config.get().instantiated_sessionmaker is old_sessionmaker
    assert config.get().engine is old_engine
    assert config.get().instantiated_sessionmaker is old_sessionmaker

    config.set(**kwargs)
    if reset:
        assert config.get().engine is not old_engine
        assert config.get().instantiated_sessionmaker is not old_sessionmaker
    else:
        assert config.get().engine is old_engine
        assert config.get().instantiated_sessionmaker is old_sessionmaker


def test_env_variables(tmp_path: pathlib.Path) -> None:
    # env variables
    old_environ = dict(os.environ)
    os.environ["CACHOLOTE_CACHE_DB_URLPATH"] = "sqlite://"

    # env file
    dotenv_path = tmp_path / ".env.cacholote"
    with dotenv_path.open("w") as f:
        f.write("CACHOLOTE_IO_DELETE_ORIGINAL=TRUE")

    config.reset(str(dotenv_path))
    try:
        assert config.get().cache_db_urlpath == "sqlite://"
        assert str(config.get().engine.url) == "sqlite://"
        assert config.get().io_delete_original is True
        assert str(config.get().engine.url) == "sqlite://"
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


@pytest.mark.parametrize("poolclass", ("NullPool", sa.pool.NullPool))
def test_set_poolclass(poolclass: str | sa.pool.Pool) -> None:
    config.set(create_engine_kwargs={"poolclass": poolclass})
    settings = config.get()
    assert settings.create_engine_kwargs["poolclass"] == sa.pool.NullPool
    assert isinstance(settings.engine.pool, sa.pool.NullPool)


@pytest.mark.parametrize(
    "expiration,raises",
    [
        (
            datetime.datetime.now(),
            pytest.raises(ValueError, match="Expiration is missing the timezone info."),
        ),
        (
            datetime.datetime.now().isoformat(),
            pytest.raises(ValueError, match="Expiration is missing the timezone info."),
        ),
        (datetime.datetime.now(tz=datetime.timezone.utc), does_not_raise()),
        (datetime.datetime.now(tz=datetime.timezone.utc).isoformat(), does_not_raise()),
    ],
)
def test_set_expiration(
    expiration: datetime.datetime | str,
    raises: contextlib.nullcontext,  # type: ignore[type-arg]
) -> None:
    with raises:
        config.set(expiration=expiration)


def test_create_engine_dict_kwargs() -> None:
    old_session_maker = config.get().instantiated_sessionmaker
    config.set(create_engine_kwargs={"connect_args": {"timeout": 30}})
    assert config.get().instantiated_sessionmaker is not old_session_maker

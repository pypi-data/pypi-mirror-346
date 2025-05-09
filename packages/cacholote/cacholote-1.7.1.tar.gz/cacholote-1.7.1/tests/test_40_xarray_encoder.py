from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

import fsspec
import pytest
import pytest_structlog
import structlog

from cacholote import cache, config, decode, encode, extra_encoders, utils

if TYPE_CHECKING:
    import xarray as xr
else:
    xr = pytest.importorskip("xarray")
dask = pytest.importorskip("dask")


def get_grib_ds() -> xr.Dataset:
    pytest.importorskip("cfgrib")
    eccodes = pytest.importorskip("eccodes")
    filename = pathlib.Path(eccodes.codes_samples_path()) / "GRIB2.tmpl"
    ds = xr.open_dataset(filename, engine="cfgrib", decode_timedelta=False)
    del ds.attrs["history"]
    return ds


@pytest.mark.filterwarnings(
    "ignore:distutils Version classes are deprecated. Use packaging.version instead."
)
def test_dictify_xr_dataset(tmp_path: pathlib.Path) -> None:
    pytest.importorskip("netCDF4")

    # Define readonly dir
    readonly_dir = str(tmp_path / "readonly")
    fsspec.filesystem("file").mkdir(readonly_dir)
    config.set(cache_files_urlpath_readonly=readonly_dir)

    # Create sample dataset
    ds = xr.Dataset({"foo": [0]}, attrs={})
    with dask.config.set({"tokenize.ensure-deterministic": True}):
        token = dask.base.tokenize(ds)

    # Check dict
    actual = extra_encoders.dictify_xr_object(ds)
    print(fsspec.filesystem("file").ls(f"{tmp_path}/cache_files"))
    href = f"{readonly_dir}/{token}.nc"
    local_path = f"{tmp_path}/cache_files/{token}.nc"
    expected = {
        "type": "python_call",
        "callable": "cacholote.extra_encoders:decode_xr_dataset",
        "args": (
            {
                "type": "application/netcdf",
                "href": href,
                "file:checksum": f"{fsspec.filesystem('file').checksum(local_path):x}",
                "file:size": 669,
                "file:local_path": local_path,
            },
            {},
        ),
        "kwargs": {"chunks": {}},
    }
    assert actual == expected

    # Use href when local_path is missing or corrupted
    fsspec.filesystem("file").mv(local_path, href)
    xr.testing.assert_identical(ds, decode.loads(encode.dumps(actual)))


@pytest.mark.parametrize(
    "xarray_cache_type,ext,importorskip",
    [
        ("application/netcdf", ".nc", "netCDF4"),
        ("application/x-grib", ".grib", "cfgrib"),
        ("application/vnd+zarr", ".zarr", "zarr"),
    ],
)
@pytest.mark.parametrize("set_cache", ["file", "cads"], indirect=True)
@pytest.mark.filterwarnings(
    "ignore:GRIB write support is experimental, DO NOT RELY ON IT!"
)
@pytest.mark.filterwarnings(
    "ignore:distutils Version classes are deprecated. Use packaging.version instead."
)
def test_xr_cacheable(
    tmp_path: pathlib.Path,
    xarray_cache_type: str,
    ext: str,
    importorskip: str,
    set_cache: str,
) -> None:
    pytest.importorskip(importorskip)

    config.set(xarray_cache_type=xarray_cache_type)

    # cache-db to check
    con = config.get().engine.raw_connection()
    cur = con.cursor()

    expected = get_grib_ds()
    cfunc = cache.cacheable(get_grib_ds)

    for expected_counter in (1, 2):
        actual = cfunc()

        # Check hits
        cur.execute("SELECT counter FROM cache_entries", ())
        assert cur.fetchall() == [(expected_counter,)]

        # Check result
        if xarray_cache_type == "application/x-grib":
            xr.testing.assert_equal(actual, expected)
        else:
            xr.testing.assert_identical(actual, expected)

        # Check opened with dask (i.e., read from file)
        assert dict(actual.chunks) == {"longitude": (16,), "latitude": (31,)}


@pytest.mark.parametrize(
    "xarray_cache_type,ext,importorskip",
    [
        ("application/netcdf", ".nc", "netCDF4"),
        ("application/vnd+zarr", ".zarr", "zarr"),
    ],
)
def test_xr_corrupted_files(
    xarray_cache_type: str,
    ext: str,
    importorskip: str,
) -> None:
    pytest.importorskip(importorskip)
    import dask

    config.set(xarray_cache_type=xarray_cache_type)

    # Cache file
    fs, dirname = utils.get_cache_files_fs_dirname()
    expected = get_grib_ds()
    cfunc = cache.cacheable(get_grib_ds)
    cfunc()

    # Get cached file path
    with dask.config.set({"tokenize.ensure-deterministic": True}):
        root = dask.base.tokenize(expected)
    cached_path = f"{dirname}/{root}{ext}"
    assert fs.exists(cached_path)

    # Warn if file is corrupted
    fs.touch(cached_path, truncate=False)
    touched_info = fs.info(cached_path)
    with pytest.warns(UserWarning, match="checksum mismatch"):
        actual = cfunc()
    xr.testing.assert_identical(actual, expected)
    assert fs.info(cached_path) != touched_info

    # Warn if file is deleted
    fs.rm(cached_path, recursive=True)
    with pytest.warns(UserWarning, match="No such file or directory"):
        actual = cfunc()
    xr.testing.assert_identical(actual, expected)
    assert fs.exists(cached_path)


def test_xr_logging(log: pytest_structlog.StructuredLogCapture) -> None:
    config.set(logger=structlog.get_logger(), raise_all_encoding_errors=True)

    # Cache dataset
    cfunc = cache.cacheable(get_grib_ds)
    cached_ds = cfunc()
    urlpath = f"file://{cached_ds.encoding['source']}"
    tmpfile = log.events[0]["urlpath"]
    assert urlpath.rsplit("/", 1)[1] == tmpfile.rsplit("/", 1)[1]

    expected = [
        {
            "urlpath": tmpfile,
            "event": "start write tmp file",
            "level": "info",
        },
        {
            "urlpath": tmpfile,
            "write_tmp_file_time": log.events[1]["write_tmp_file_time"],
            "event": "end write tmp file",
            "level": "info",
        },
        {
            "urlpath": urlpath,
            "size": 22597,
            "event": "start upload",
            "level": "info",
        },
        {
            "urlpath": urlpath,
            "size": 22597,
            "upload_time": log.events[3]["upload_time"],
            "event": "end upload",
            "level": "info",
        },
        {
            "urlpath": urlpath,
            "event": "retrieve cache file",
            "level": "info",
        },
    ]
    assert log.events == expected


@pytest.mark.parametrize(
    "original_obj",
    (
        xr.DataArray([0], name="foo"),
        xr.DataArray([0], name="foo").to_dataset(),
    ),
)
def test_xr_roundtrip(original_obj: xr.Dataset | xr.DataArray) -> None:
    @cache.cacheable
    def cache_xr_obj(
        obj: xr.Dataset | xr.DataArray,
    ) -> xr.Dataset | xr.DataArray:
        return obj

    cached_obj = cache_xr_obj(original_obj)
    xr.testing.assert_identical(cached_obj, original_obj)
    assert original_obj.encoding.get("source") is None
    assert cached_obj.encoding.get("source") is not None

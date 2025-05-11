import sys, time, threading, itertools
import cubexpress as ce
import pandas as pd

def download(
    lon: float,
    lat: float,
    edge_size: int,
    start: str,
    end: str,
    *,
    max_cscore: float = 1,
    min_cscore: float = 0,
    outfolder: str = "raw",
    nworks: int = 4,
    cache: bool = True,
    show_spinner: bool = True,
    verbose: bool = False
) -> pd.DataFrame:
    """
    """
    stop_flag = {"v": False}

    if show_spinner and not verbose:
        def _spin():
            for ch in itertools.cycle("|/-\\"):
                if stop_flag["v"]:
                    break
                sys.stdout.write(f"\rDownloading Sentinel-2 imagery & metadata… {ch}")
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write("\rDownloading Sentinel-2 imagery & metadata ✅\n")
            sys.stdout.flush()

        th = threading.Thread(target=_spin, daemon=True)
        th.start()
    else:
        th = None

    try:
        table = ce.s2_cloud_table(
            lon=lon,
            lat=lat,
            edge_size=edge_size,
            start=start,
            end=end,
            max_cscore=max_cscore,
            min_cscore=min_cscore,
            cache=cache,
            verbose=verbose
        )

        ce.get_cube(
            table=table,
            outfolder=outfolder,
            nworks=nworks,
            verbose=verbose,
            cache=cache
        )
    finally:
        stop_flag["v"] = True
        if th is not None:
            th.join()

    return table

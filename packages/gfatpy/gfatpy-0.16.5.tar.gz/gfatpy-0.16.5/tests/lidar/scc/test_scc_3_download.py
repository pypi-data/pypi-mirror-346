from pathlib import Path
from gfatpy.lidar.scc import scc_access

from gfatpy.lidar.scc.transfer import check_scc_connection
from gfatpy.utils.io import read_yaml

SCC_INFO = read_yaml(Path(r"./gfatpy/env_files/info_scc_user.yml"))

SCC_SERVER_SETTINGS = SCC_INFO["server_settings"]

scc_dir = Path("./tests/datos/PRODUCTS/alhambra/scc/scc781/2023/08/30/products")


def test_download_measurement():
    scc_id = 781
    year, month, day = "2023", "08", "30"
    measurementID: str = f"{year}{month}{day}gra0315"
    output_dir = Path(
        f"./tests/datos/PRODUCTS/alhambra/scc/scc{scc_id}/{year}/{month}/{day}/products"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    SCC_SERVER_SETTINGS["output_dir"] = output_dir
    # Check connection to SCC
    assert check_scc_connection(SCC_SERVER_SETTINGS)

    # Remove measurement from SCC
    scc_obj = scc_access.SCC(
        tuple(SCC_SERVER_SETTINGS["basic_credentials"]),
        SCC_SERVER_SETTINGS["output_dir"],
        SCC_SERVER_SETTINGS["base_url"],
    )

    scc_obj.login(SCC_SERVER_SETTINGS["website_credentials"])
    _ = scc_obj.monitor_processing(
        measurementID,
        download_raw=True,
        download_cloudmask=False,
        download_elpp=True,
        download_elda=True,
        download_elic=False,
        download_elquick=False,
    )

    scc_obj.logout()

    # assert check_was_removed
    assert (output_dir / "preprocessed_20230830gra0315.zip").exists()
    assert (output_dir / "raw_20230830gra0315.zip").exists()
    assert (output_dir / "optical_20230830gra0315.zip").exists()

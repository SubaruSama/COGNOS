import tbselenium.common as cm
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import launch_tbb_tor_with_stem

breached_hidden_service = 'http://breached65xqh64s7xbkvqgg7bmj4nj7656hcb7x4g42x753r7zmejqd.onion/'
tbb_dir = "/home/user/Documents/COGNOS/crafted_spiders/tor-browser_en-US"
tor_process = launch_tbb_tor_with_stem(tbb_path=tbb_dir)

with TorBrowserDriver(tbb_dir, tor_cfg=cm.USE_STEM) as driver:
    # driver.load_url("https://check.torproject.org")
    driver.load_url(breached_hidden_service)
    input()

tor_process.kill()

from pathlib import Path
import logging

std_max_retries = 3
std_1s_wait = 1
std_2s_wait = 2
std_3s_wait = 3
std_5s_wait = 5
std_10s_wait = 10
std_15s_wait = 15
std_20s_wait = 20
std_60s_wait = 60
search_depth = 20
root_directory = Path(__file__).parent.resolve()


LOGGER = logging.getLogger("Emerson")
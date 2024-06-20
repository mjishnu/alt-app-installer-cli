import asyncio
import logging
import os

from pypdl import PypdlFactory
from url_gen import url_generator


def default_logger(name: str) -> logging.Logger:
    """Creates a default debugging logger."""
    logger = logging.getLogger(name)
    handler = logging.FileHandler("log.txt", mode="a", delay=True)
    custom_format = (
        f"[{name} logs] \n[%(asctime)s]\n\n %(levelname)s: %(message)s\n{82*"-"}\n"
    )
    handler.setFormatter(logging.Formatter(custom_format, datefmt="%d-%m-%Y %H:%M:%S"))
    logger.addHandler(handler)
    return logger


def download(url, ignore_ver, all_dependencies):
    def new_url_gen(f_name):
        urls = asyncio.run(url_generator(url, ignore_ver, all_dependencies))
        return urls[0][f_name]

    print("Fetching data...")
    main_dict, final_data, file_name, uwp = asyncio.run(
        url_generator(url, ignore_ver, all_dependencies)
    )

    dwnpath = "downloads/"

    if not os.path.exists(dwnpath):
        os.makedirs(dwnpath)

    path_lst = []
    tasks = []
    d = PypdlFactory(instances=2, logger=default_logger("downloader"))
    for f_name in final_data:
        remote_url = main_dict[f_name]
        path = f"{dwnpath}{f_name}"
        path_lst.append(path)
        mirror_func = lambda: new_url_gen(f_name)
        tasks.append(
            (
                remote_url,
                {
                    "file_path": path,
                    "segments": 10,
                    "retries": 3,
                    "mirror_func": mirror_func,
                },
            )
        )
    d.start(tasks)
    print(f"Downloaded Package:{final_data}")

    return path_lst, uwp

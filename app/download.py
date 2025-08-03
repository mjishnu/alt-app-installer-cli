import asyncio
import logging
import os
import shutil
from time import sleep

from tqdm import tqdm
from pypdl import Pypdl
from url_gen import url_generator


def default_logger(name: str) -> logging.Logger:
    """Creates a default debugging logger."""
    logger = logging.getLogger(name)
    handler = logging.FileHandler("log.txt", mode="a", delay=True)
    custom_format = (
        f"[{name} logs] \n[%(asctime)s]\n\n %(levelname)s: %(message)s\n{82 * '-'}\n"
    )
    handler.setFormatter(logging.Formatter(custom_format, datefmt="%d-%m-%Y %H:%M:%S"))
    logger.addHandler(handler)
    return logger


def download(url, ignore_ver, all_dependencies, progress):
    print("Fetching data...")
    main_dict, final_data, file_name, uwp = asyncio.run(
        url_generator(url, ignore_ver, all_dependencies)
    )

    dwnpath = "downloads/"

    if not os.path.exists(dwnpath):
        os.makedirs(dwnpath)

    path_lst = []
    tasks = []
    d = Pypdl(logger=default_logger("downloader"), max_concurrent=2)
    for f_name in final_data:
        remote_url = main_dict[f_name]
        path = f"{dwnpath}{f_name}"
        path_lst.append(path)

        async def new_url_gen():
            urls = await url_generator(url, ignore_ver, all_dependencies)
            return urls[0][f_name]

        tasks.append(
            {
                "url": remote_url,
                "file_path": path,
                "mirrors": new_url_gen,
            }
        )
    display = True if progress == "full" else False
    block = False if progress == "simple" else True

    d.start(tasks=tasks, retries=3, overwrite=False, display=display, block=block)
    if progress == "simple":
        terminal_width = shutil.get_terminal_size().columns
        ncols = 105 if terminal_width >= 105 else None

        with tqdm(
            total=100, ascii=True, bar_format="[{bar}] {percentage:3.0f}%", ncols=ncols
        ) as pbar:
            while not d.completed:
                sleep(0.5)
                progress = d.progress if d.size else d.task_progress
                pbar.n = progress or 0
                pbar.refresh()
            pbar.n = 100
            pbar.refresh()
    print(f"Downloaded Package:{final_data}")

    return path_lst, uwp

import asyncio
import logging
import os
import shutil
from time import sleep

from tqdm import tqdm
from pypdl import Pypdl
from url_gen import url_generator


class FolderNotFoundError(Exception):
    pass


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


def download(
    url, progress, dwnpath, arch, ignore_ver, all_dependencies, no_dependencies
):
    if dwnpath is None:
        dwnpath = "downloads/"
        os.makedirs(dwnpath, exist_ok=True)

    if not os.path.exists(dwnpath):
        raise FolderNotFoundError(f"Output directory '{dwnpath}' does not exist!")
    print("Fetching data...")
    arch = arch if arch != "auto" else None
    main_dict, final_data, main_file, uwp = asyncio.run(
        url_generator(url, ignore_ver, all_dependencies, arch)
    )

    path_lst = []
    tasks = []

    def create_task(f_name):
        remote_url = main_dict[f_name]
        path = os.path.join(dwnpath, f_name)

        async def new_url_gen():
            urls = await url_generator(url, ignore_ver, all_dependencies)
            return urls[0][f_name]

        path_lst.append(path)
        tasks.append(
            {
                "url": remote_url,
                "file_path": path,
                "mirrors": new_url_gen,
            }
        )

    d = Pypdl(logger=default_logger("downloader"), max_concurrent=2)

    if no_dependencies:
        create_task(main_file)
        final_data = [main_file]
    else:
        for f_name in final_data:
            create_task(f_name)

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

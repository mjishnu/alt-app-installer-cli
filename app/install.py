import os
import time
from datetime import datetime

import clr

script_dir = os.path.dirname(os.path.abspath(__file__))
clr.AddReference(rf"{script_dir}\data\System.Management.Automation.dll")

from System.Management.Automation import PowerShell


def install(path, uwp):
    def log_error(source, e):
        with open(f"{script_dir}/log.txt", "a") as f:
            current_time = datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
            f.write(f"[powershell logs] \n{current_time}\n\n")
            f.write(f'Package Name: {s_path.split("/")[-1]}\n\n')
            f.write(str(source[e.Index].Exception.Message))
            f.write(f'{82*"-"}\n')

    for s_path in path.keys():
        ps = PowerShell.Create()
        ps.Streams.Error.DataAdded += log_error

        if uwp:
            ps.AddCommand("Add-AppxPackage")
            ps.AddParameter("Path", s_path)
        else:
            ps.AddCommand("Start-Process")
            ps.AddParameter("FilePath", s_path)

        try:
            ps.Invoke()
            print(f"Processed: {s_path.split('/')[-1]}")
        except Exception as e:
            print(e)

        time.sleep(0.3)

    print("Operation Completed, check logs.txt for more info")

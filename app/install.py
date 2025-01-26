import subprocess
import time
from datetime import datetime


def install(paths, uwp):
    def run(command):
        output = subprocess.run(
            [
                "C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe",
                command,
            ],
            capture_output=True,
            text=True,
        )
        return output

    for path in paths:
        if uwp:
            output = run(f'Add-AppPackage "{path}"')
        else:
            output = run(f'Start-Process "{path}"')

        print(f"Processed: {path.split('/')[-1]}")

        if output.returncode != 0:
            with open("log.txt", "a") as f:
                current_time = datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
                f.write(f"[powershell logs] \n{current_time}\n\n")
                f.write(f"command: {output.args[1]}\n\n")
                f.write(output.stderr)
                f.write(f"{82 * '-'}\n")

        time.sleep(0.3)

    print("Operation Completed, check logs.txt for more info")

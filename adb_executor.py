import subprocess
import os
from logger import *

logger = logging.getLogger(__name__)


class ADB:

    def pull(self, path):
        # TODO: Pulling by loop using json configure
        # Make path as absolute
        destination_path = os.path.abspath(path)

        # Create directory if not existance
        os.makedirs(destination_path) if not os.path.exists(destination_path) else None

        command = f"adb pull /sdcard/DCIM/Camera/IMG_20231026_204815.jpg {destination_path}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

        if result.returncode == 0:
            return success("Process result: " + result.stdout)
        else:
            return failure(f"Error occur while pulling media: {result.stderr}")
    def _check(self):
        pass

    def delete(self):
        if self._check():
            print("deleting data")


if __name__ == "__main__":
    adb = ADB()
    adb.pull("C:/Users/Daniel/Desktop/test")

import json
import subprocess
import os
from logger import *

logger = logging.getLogger(__name__)


class ExecutorADB:
    def __init__(self):
        with open('configs/adbexecutor.json', 'r') as file:
            config = json.load(file)
        self.medias = config['medias']
        self.execute = config['execute']

    def pull(self, path):
        # TODO: Pulling by loop using json configure
        # Make path as absolute
        destination_path = os.path.abspath(path)

        # Create directory if not exists
        os.makedirs(destination_path) if not os.path.exists(destination_path) else None

        results = []
        for media, source in self.medias.items():
            if self.execute[media]:
                command = f"adb pull {source} {destination_path}"
                result = subprocess.run(command,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        encoding='utf-8')

                if result.returncode == 0:
                    results.append(success(f"Pulling from {media}: " + result.stdout))
                else:
                    results.append(failure(f"Error occur while pulling {media}: {result.stdout}"))
        return success("Pulling OK") if all(results) else failure("Pulling NOK")

    def _check(self):
        pass

    def delete(self):
        if self._check():
            print("deleting data")


if __name__ == "__main__":
    adb = ExecutorADB()
    adb.pull("C:/Users/Daniel/Desktop/test")

import logging
import os
import subprocess

from utilities import success, failure, load_settings

logger = logging.getLogger('executor')


class PullingExecutor:
    def __init__(self):
        config = load_settings("adbexecutor.json")
        self.medias = config['medias']
        self.execute = config['execute']

    def pull(self, path):
        # TODO: Pulling by loop using json configure
        # Make path as absolute
        destination_path = os.path.abspath(path)

        # Create directory if not exists
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
            logger.info(f"Create directory: {destination_path}")

        results = []
        for media, source in self.medias.items():
            if self.execute[media]:
                command = f"adb pull {source} {destination_path}"
                logger.info(f"Send command: {command}")
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
    adb = PullingExecutor()
    adb.pull("C:/Users/Daniel/Desktop/test")

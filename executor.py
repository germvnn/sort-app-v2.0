import logging
import os
import shutil
import subprocess
import re

from utilities import success, failure, load_settings, create_directory

logger = logging.getLogger('executor')


class PullingExecutor:
    def __init__(self):
        media_config = load_settings("adbexecutor.json")
        self.medias = media_config['medias']
        self.execute = media_config['execute']

        runner_config = load_settings("runner.json")
        self.runner = runner_config['pulling_executor']

    def pull(self, path):
        # TODO: Pulling by loop using json configure
        # Make path as absolute
        destination_path = os.path.abspath(path)

        # Create directory if not exists
        create_directory(destination_path)

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
                    self._extract_images(path) if self.runner['extract'] else logger.info("Extract non_image: false")
                    self._delete(source, result.stdout) if self.runner['delete'] else logger.info("Delete set: false")
                else:
                    results.append(failure(f"Error occur while pulling {media}: {result.stdout}"))
        return success("Pulling OK") if all(results) else failure("Pulling NOK")

    @staticmethod
    def _extract_images(path):
        logger.debug("Run extraction process")
        non_image = 'non_image'
        non_image_dir = os.path.join(path, non_image)
        exclude_dir = {non_image}
        for root, dirs, files in os.walk(path, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude_dir]
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, path)
                target_dir = os.path.join(non_image_dir, relative_path)

                create_directory(target_dir)

                shutil.move(source_path, target_dir)
                logger.info(f"Moved {source_path} to {target_dir}")

    @staticmethod
    def _delete(source, pull_output):
        matches = re.search(r'(\d+) skipped', pull_output)
        skipped = int(matches.group(1))
        if skipped == 0:
            command = f"adb shell rm -r {source}"
            result = subprocess.run(command,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='utf-8')
            if result.returncode == 0:
                logger.info(f"Successfully removed {source} from device")
            else:
                logger.error(f"Failed to remove {source} from device: {result.stderr}")
        else:
            logger.warning(f"There are {skipped} skipped files. Cancel removing files.")


if __name__ == "__main__":
    adb = PullingExecutor()
    adb.pull("C:/Users/Daniel/Desktop/test")

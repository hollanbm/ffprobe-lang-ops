import argparse
import json
import os
import subprocess
from pathlib import Path
from sys import stdout

from loguru import logger


class LangParser:
    def __init__(self):
        logger_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "{extra[file]} | "
            "<level>{message}</level>"
        )
        logger.configure(extra={"file": ""})  # Default values
        logger.remove()
        logger.add(stdout, format=logger_format)

        parser = argparse.ArgumentParser()
        parser.parse_args()

    def start(self) -> None:
        fileList = Path("/home/hollanbm/Media/TV").rglob("*.mkv")
        for file in fileList:
            with logger.contextualize(file=str(file)):
                try:
                    result = subprocess.run(
                        [
                            "ffprobe",
                            "-v",
                            "error",  #'quiet',
                            "-print_format",
                            "json",
                            "-show_chapters",
                            "-show_format",
                            "-show_streams",
                            file,
                        ],
                        stdout=subprocess.PIPE,
                    ).stdout.decode("utf-8")

                    metadata = json.loads(result)

                    for stream in metadata["streams"]:
                        if (
                            stream["codec_type"] == "audio"
                            and stream.get("tags").get("language") is not None
                            and stream["tags"]["language"] != "eng"
                        ):
                            logger.info(
                                f"stream index {stream['index']} is not english"
                            )
                            os.remove(file)
                            logger.info("deleted")

                except:
                    logger.error("error encountered")


if __name__ == "__main__":
    LangParser().start()

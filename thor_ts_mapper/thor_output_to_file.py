import os
import json
from typing import Dict, Any, Iterator
from thor_ts_mapper.logger_config import LoggerConfig
from alive_progress import alive_bar
from thor_ts_mapper import constants
from thor_ts_mapper.exceptions import OutputError


logger = LoggerConfig.get_logger(__name__)


class THOROutputToFile:
    def __init__(self, output_file: str):
        self.output_file = output_file
        self.mode = 'a' if os.path.exists(self.output_file) else 'w'

    def _validate_file_extension(self)  -> None:
        try:
            file_name, extension = os.path.splitext(self.output_file)
            if extension.lower() != constants.OUTPUT_FILE_EXTENSION:
                self.output_file = file_name + constants.OUTPUT_FILE_EXTENSION
                logger.info(f"Changed output file from `{extension}` to `{self.output_file}` to ensure JSONL format")
        except Exception as e:
            logger.error("Error validating or modifying the output file: %s", e)

    def _prepare_output_dir(self) -> None:
        output_dir = os.path.dirname(self.output_file)
        if output_dir and not os.path.isdir(output_dir):
            try:
                logger.info(f"Creating output directory: {output_dir}")
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                logger.error(f"Failed to create output directory `{output_dir}`: {e}")
                raise OutputError(f"Cannot create output directory: {e}")


    def write_to_file(self, events: Iterator[Dict[str, Any]]) -> None:
        try:
            self._validate_file_extension()
            self._prepare_output_dir()
            with alive_bar(spinner='dots', title=f"Writing to {self.output_file}") as bar:
                with open(self.output_file, self.mode, encoding=constants.DEFAULT_ENCODING) as file:
                    for event in events:
                        file.write(json.dumps(event) + "\n")
                        bar()
                logger.debug(f"Successfully written events to {self.output_file}")
        except Exception as e:
            if self.output_file and os.path.exists(self.output_file):
                try:
                    os.remove(self.output_file)
                except OSError as e:
                    error_msg = f"Failed to remove output file: {e}"
                    logger.error(error_msg)
                    raise OutputError(error_msg)
            error_msg = f"Error writing to file: {e}"
            logger.error(error_msg)
            raise OutputError(error_msg)
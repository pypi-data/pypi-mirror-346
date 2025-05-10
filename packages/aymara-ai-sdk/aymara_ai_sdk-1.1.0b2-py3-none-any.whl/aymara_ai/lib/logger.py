__all__ = ["SDKLogger"]

import re
import time
import logging
from typing import Any, Dict
from contextlib import contextmanager

import IPython
from colorama import Fore, Style, init
from tqdm.auto import tqdm
from IPython.display import HTML, display  # type: ignore

from .status import Status


class SDKLogger(logging.Logger):
    def __init__(self, name="sdk", level=logging.DEBUG):  # type: ignore
        super().__init__(name, level)

        # Set up logging
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.addHandler(handler)

        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.tasks = {}
        self.is_notebook = self._is_running_in_notebook()
        if not self.is_notebook:
            init(autoreset=True)  # Initialize colorama

    @staticmethod
    def _is_running_in_notebook() -> bool:
        try:
            shell = IPython.get_ipython().__class__.__name__  # type: ignore
            if shell == "ZMQInteractiveShell":
                return True  # Jupyter notebook or qtconsole
            elif shell == "TerminalInteractiveShell":
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except (NameError, ImportError):
            return False  # Probably standard Python interpreter

    @contextmanager
    def progress_bar(self, name: str, uuid: str, status: str, upload_total: int = 0) -> Any:
        self.tasks[uuid] = {
            "name": name,
            "uuid": uuid,
            "status": status,
            "start_time": time.time(),
            "upload_progress": 0,
            "upload_total": upload_total,
        }
        desc = self._get_progress_description(uuid)
        with tqdm(
            total=None,
            desc=desc,
            unit="s",
            bar_format="{desc}",
            colour="orange" if self.is_notebook else None,
        ) as pbar:
            pbar.update()
            self.tasks[uuid]["pbar"] = pbar

            # Add methods to the progress bar object
            def update_upload_progress(n: int) -> None:
                self.tasks[uuid]["upload_progress"] = n
                self._update_progress_description(uuid)

            def update_uuid(new_uuid: str) -> None:
                old_task = self.tasks.pop(uuid)
                self.tasks[new_uuid] = old_task
                self.tasks[new_uuid]["uuid"] = new_uuid
                self._update_progress_description(new_uuid)

            pbar.update_upload_progress = update_upload_progress  # type: ignore
            pbar.update_uuid = update_uuid  # type: ignore

            try:
                yield pbar
            finally:
                if uuid in self.tasks:
                    del self.tasks[uuid]

    def _get_progress_description(self, uuid: str) -> str:
        task = self.tasks[uuid]
        elapsed_time = int(time.time() - task["start_time"])
        status_str = task["status"]

        if not self.is_notebook:
            if task["status"] == Status.FAILED:
                status_str = f"{Fore.RED}{status_str}{Style.RESET_ALL}"
            elif task["status"] == Status.FINISHED:
                status_str = f"{Fore.GREEN}{status_str}{Style.RESET_ALL}"
            elif task["status"] == Status.PROCESSING:
                status_str = f"{Fore.YELLOW}{status_str}{Style.RESET_ALL}"
            else:
                status_str = f"{Fore.YELLOW}{status_str}{Style.RESET_ALL}"

        description = f"{task['name']} | {task['uuid']} | {elapsed_time}s | {status_str}"

        # Only add upload progress if we're in the UPLOADING status
        if task.get("upload_total") and task["status"] == Status.PROCESSING:
            upload_progress = f" | {task['upload_progress']}/{task['upload_total']}"
            description += upload_progress

        return description

    def _update_progress_description(self, uuid: str) -> None:
        task = self.tasks[uuid]
        task["pbar"].set_description_str(self._get_progress_description(uuid))
        task["pbar"].update()

    def update_progress_bar(self, uuid: str, status: str) -> None:
        task = self.tasks[uuid]
        task["status"] = status
        task["pbar"].set_description_str(self._get_progress_description(uuid))
        if self.is_notebook:
            if status == Status.FAILED:
                task["pbar"].colour = "red"
            elif status == Status.FINISHED:
                task["pbar"].colour = "green"
            else:
                task["pbar"].colour = "orange"
        task["pbar"].update()

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:  # type: ignore
        if self.is_notebook:
            # Detect and create links if in notebook
            link_pattern = r"(https?://\S+?)([.,;:!?])?(\s|$)"
            colored_msg = re.sub(
                link_pattern,
                lambda m: f'<a href="{m.group(1)}" target="_blank">{m.group(1)}</a>{m.group(2) or ""}{m.group(3)}',
                msg,
            )
            colored_msg = f'<span style="color: orange;">{colored_msg}</span>'
            display(HTML(colored_msg))  # type: ignore
        else:
            msg = f"{Fore.YELLOW}{msg}{Style.RESET_ALL}"
            super().warning(msg, *args, **kwargs)

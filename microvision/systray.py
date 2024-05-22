"""
This module contains stuff relevant to running the system
tray icons, but also the rest of the program. The system tray
is the first thing to be initialized ultimately, and the
inheritance of pystray.Icon happens mainly so we can use
context managers to ensure proper closure.
"""
import logging
import sys

import pystray
from PIL import Image

from .cam import CameraThread, CameraClassifier


class SysTray(pystray.Icon):
    """
    Class abstracts pystray.Icon for system tray functionality.

    We do this mainly because we'd like to use context managers
    in the main thread to make sure everything gets closed properly.
    """
    def __init__(self, conf):
        super().__init__(
            "CV-MIC",
            icon=Image.open("assets/icon.png"),
            menu=pystray.Menu(
                pystray.MenuItem(
                    'Exit',
                    self.quit
                )
            )

        )

        self.logger = logging.getLogger()
        self.logger.setLevel(conf.log_level)

        classifier = CameraClassifier(
            conf,
            camera_index=conf.classifier.camera_index,
            front_scale_factor=conf.classifier.front_scale_factor,
            front_min_neighbors=conf.classifier.front_min_neighbors,
            front_min_size=conf.classifier.front_min_size,
            side_scale_factor=conf.classifier.side_scale_factor,
            side_min_neighbors=conf.classifier.side_min_neighbors,
            side_min_size=conf.classifier.side_min_size
        )
        self.camera_thread = CameraThread(conf, classifier=classifier)

    def __enter__(self):
        self.logger.info("Camera thread starting.")
        self.camera_thread.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.logger.info("Camera thread exiting.")
        self.camera_thread.stop()
        self.camera_thread.join()
        self.logger.info("Camera thread exited.")

    def quit(self):
        """Stop system tray and camera threads, then quit."""
        self.camera_thread.stop()
        self.camera_thread.join()
        self.logger.info("Stopping systray thread.")
        self.stop()
        self.logger.info("Bye!")
        sys.exit(0)

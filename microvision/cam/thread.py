"""
Module contains threding stuff.

In all honesty, it just didn't feel right including this
in the classifier file, so it's separate. This basically
only contains the stuff required to instantiate a special
stoppable thread which handles the camera loop, as well as
the actual mic switching.
"""
import logging
import threading
import time

from ..keyboard import Keyboard


class CameraThread(threading.Thread):
    """
    Implementation of a stoppable thread running
    the camera loop.
    """
    def __init__(self, conf, classifier, detection_threshold=5):
        self._stop_thread = threading.Event()
        self.conf = conf
        self.classifier = classifier
        self.detection_threshold = detection_threshold

        self.logger = logging.getLogger()
        self.logger.setLevel(conf.log_level)
        super().__init__(target=self.run)

    def stop(self):
        """Stop the thread."""
        self._stop_thread.set()

    def stopped(self):
        """Returns True if the thread has been stopped."""
        return self._stop_thread.is_set()

    def run(self):
        """Main target function of the thread."""
        keyboard = Keyboard()
        switched = False
        last_detection = time.time()

        with self.classifier as classifier:
            self.logger.info("Entering classifier loop.")
            while True:
                if self.stopped():
                    return

                if classifier.detected_any():
                    if switched is True:
                        self.logger.info("Presence detected, switching.")
                        keyboard.send(self.conf.mic.present_mic_keys)
                        switched = False
                    last_detection = time.time()
                else:
                    if switched is False:
                        elapsed = time.time() - last_detection
                        if elapsed > self.conf.mic.seconds_before_absent:
                            self.logger.info("Absence detected, switching.")
                            keyboard.send(self.conf.mic.absent_mic_keys)
                            switched = True
                time.sleep(1.0 / self.conf.classifier.frame_frequency)

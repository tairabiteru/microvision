"""
Module defines computer vision functionality.

The CameraClassifier is an abstraction of a few of
opencv's CasecadeClassifiers. What's essentially going
on is the main program is capturing a frame from the
camera, attempting to perform three different face detection
operations. We look for a front-facing face, a left-facing
one, and a right-facing one. If any of them are detected,
it means someone is at the computer.
"""
import cv2
import logging


class CameraClassifier:
    """Camera classifier abstracting opencv functionality."""
    def __init__(
            self,
            conf,
            camera_index=0,
            front_scale_factor=1.1,
            front_min_neighbors=7,
            front_min_size=(40, 40),
            side_scale_factor=1.3,
            side_min_neighbors=7,
            side_min_size=(40, 40),
        ):
        self.camera_index = camera_index
        self.front_scale_factor = front_scale_factor
        self.front_min_neighbors = front_min_neighbors
        self.front_min_size = front_min_size
        self.side_scale_factor = side_scale_factor
        self.side_min_neighbors = side_min_neighbors
        self.side_min_size = side_min_size

        self.camera = None

        self.frontal = cv2.CascadeClassifier(
            f"{cv2.data.haarcascades}haarcascade_frontalface_default.xml"
        )
        self.profile = cv2.CascadeClassifier(
            f"{cv2.data.haarcascades}haarcascade_profileface.xml"
        )

        self.logger = logging.getLogger()
        self.logger.setLevel(conf.log_level)

    def __enter__(self):
        self.camera = cv2.VideoCapture(self.camera_index)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.camera.release()

    def get_frame(self):
        """Obtain a single frame from the camera."""
        while True:
            ret, frame = self.camera.read()
            if ret:
                break
        return frame

    def detected_frontal(self, frame):
        """Return True if the frame passed contains a front-facing face."""
        loc = self.frontal.detectMultiScale(
            frame,
            scaleFactor=self.front_scale_factor,
            minNeighbors=self.front_min_neighbors,
            minSize=self.front_min_size
        )
        return len(loc) != 0

    def detected_left(self, frame):
        """Return True if the frame passed contains a left-facing face."""
        loc = self.profile.detectMultiScale(
            frame,
            scaleFactor=self.side_scale_factor,
            minNeighbors=self.side_min_neighbors,
            minSize=self.side_min_size
        )
        return len(loc) != 0

    def detected_right(self, frame):
        """Return True if the frame passed contains a right-facing face."""
        return self.detected_left(cv2.flip(frame, 1))

    def detected_any(self):
        """
        Return True if the camera presently has any in the set of a
        front-facing, left-facing, or right-facing face in view.
        """
        frame = self.get_frame()
        return any([
            self.detected_frontal(frame),
            self.detected_left(frame),
            self.detected_right(frame)
        ])

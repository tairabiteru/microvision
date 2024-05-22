"""Main entry point."""
import logging

from microvision import SysTray, Config

__AUTHOR__ = "Taira"
__VERSION__ = "1.0"

if __name__ == "__main__":
    conf = Config()

    logging.basicConfig(
        filename="cvmic.log",
        format='[%(asctime)s][%(levelname)s]: %(message)s',
        filemode='w'
    )

    with SysTray(conf) as systray:
        systray.run()

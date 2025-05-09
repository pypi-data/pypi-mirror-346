__version__ = "3.2.1b2"

from bcps import core, cli


__all__ = ["core", "cli"]


def run():
    from bcps import __main__

    __main__.main()

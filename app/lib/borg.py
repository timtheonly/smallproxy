from typing import Dict


class Borg(object):
    """
    borg pattern you will be assimilated
    """

    __shared_state: Dict = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

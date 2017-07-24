"""
    Pharos.Model.laser.santec.py
    ==================================
    Model for the santec lasers

    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""
from controller.santec.tsl710 import tsl710
from ._skeleton import LaserBase


class santec(tsl710):
    def __init__(self, **kwargs):
        tsl710.__init__(self, kwargs)
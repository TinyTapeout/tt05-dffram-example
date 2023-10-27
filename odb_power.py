#
# OpenDB script for custom Power for tt_top / user_project_wrapper
#
# Copyright (c) 2023 Sylvain Munaut <tnt@246tNt.com>
# SPDX-License-Identifier: Apache-2.0
#

import os
import sys

import odb
import click

from openlane.common.misc import get_openlane_root
sys.path.insert(0, os.path.join(get_openlane_root(), "scripts", "odbpy"))
from reader import click_odb


@click.command()
@click_odb
def power(reader):
  # Create ground / power nets
  tech = reader.db.getTech()
  vpwr_net = reader.block.findNet('VPWR')
  vgnd_net = reader.block.findNet('VGND')
  met4 = tech.findLayer('met4')
  vpwr_wire = vpwr_net.getSWires()[0]
  vgnd_wire = vgnd_net.getSWires()[0]
  odb.dbSBox_create(vpwr_wire, met4, 18280, 143520, 19880, 144120, "STRIPE")
  odb.dbSBox_create(vgnd_wire, met4, 95080, 143520, 96680, 144120, "STRIPE")

if __name__ == "__main__":
  power()

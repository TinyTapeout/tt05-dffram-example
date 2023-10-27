#!/usr/bin/env python3

#
# OpenLane2 build script to harden the tt_top macro inside
# the classic user_project_wrapper
#
# Copyright (c) 2023 Sylvain Munaut <tnt@246tNt.com>
# SPDX-License-Identifier: Apache-2.0
#

import argparse
import json
import os
import sys

from typing import List, Type

from openlane.flows.misc import OpenInKLayout
from openlane.flows.sequential import SequentialFlow
from openlane.steps.odb import OdbpyStep
from openlane.steps import (
	Step,
	Yosys,
	OpenROAD,
	Magic,
	Misc,
	KLayout,
	Odb,
	Netgen,
	Checker,
)

class CustomPower(OdbpyStep):

	id = "TT.Top.CustomPower"
	name = "Custom Power connections for DFFRAM macro"

	def get_script_path(self):
		return os.path.join(
			os.path.dirname(__file__),
			"odb_power.py"
		)


class ProjectFlow(SequentialFlow):

	Steps: List[Type[Step]] = [
		Yosys.JsonHeader,
		Yosys.Synthesis,
		Checker.YosysUnmappedCells,
		Checker.YosysSynthChecks,
		OpenROAD.CheckSDCFiles,
		OpenROAD.Floorplan,
		Odb.ApplyDEFTemplate,
		Odb.SetPowerConnections,
		Odb.ManualMacroPlacement,
		OpenROAD.GeneratePDN,
		CustomPower,
		OpenROAD.GlobalPlacement,
		OpenROAD.DetailedPlacement,
		OpenROAD.GlobalRouting,
		OpenROAD.DetailedRouting,
		Checker.TrDRC,
		Odb.ReportDisconnectedPins,
		Checker.DisconnectedPins,
		Odb.ReportWireLength,
		Checker.WireLength,
		OpenROAD.RCX,
		OpenROAD.STAPostPNR,
		OpenROAD.IRDropReport,
		Magic.StreamOut,
		Magic.WriteLEF,
		KLayout.StreamOut,
		KLayout.XOR,
		Checker.XOR,
		Magic.DRC,
		Checker.MagicDRC,
		Magic.SpiceExtraction,
		Checker.IllegalOverlap,
		Netgen.LVS,
		Checker.LVS,
	]


if __name__ == '__main__':
	# Argument processing
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--open-in-klayout", action="store_true", help="Open last run in KLayout")

	args = parser.parse_args()
	config = vars(args)

	PDK_ROOT = os.getenv('PDK_ROOT')

	# Load fixed required config for UPW
	flow_cfg = json.loads(open('config.json', 'r').read())

	# Run flow
	flow_class = OpenInKLayout if args.open_in_klayout else ProjectFlow
	flow = flow_class(
		flow_cfg,
		design_dir = ".",
		pdk_root   = PDK_ROOT,
		pdk        = "sky130A",
	)

	flow.start(last_run = args.open_in_klayout, run_tag = "wokwi")

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

from openlane.flows.misc import OpenInKLayout
from openlane.flows.classic import Classic
from openlane.steps.odb import OdbpyStep
from openlane.steps import OpenROAD

class CustomPower(OdbpyStep):

	id = "TT.Top.CustomPower"
	name = "Custom Power connections for DFFRAM macro"

	def get_script_path(self):
		return os.path.join(
			os.path.dirname(__file__),
			"odb_power.py"
		)


class ProjectFlow(Classic):
  pass

if __name__ == '__main__':
	# Argument processing
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--open-in-klayout", action="store_true", help="Open last run in KLayout")

  # Insert our custom step after the PDN generation
	ProjectFlow.Steps.insert(ProjectFlow.Steps.index(OpenROAD.GeneratePDN) + 1, CustomPower)

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

	flow.start(last_run = args.open_in_klayout, tag = "wokwi")

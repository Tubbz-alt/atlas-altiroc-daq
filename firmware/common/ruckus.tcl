# Load RUCKUS environment and library
source -quiet $::env(RUCKUS_DIR)/vivado_proc.tcl

# Load local Source Code and constraints
loadSource      -dir  "$::DIR_PATH/core"
loadSource      -dir  "$::DIR_PATH/asic"
loadSource      -dir  "$::DIR_PATH/eth"
loadSource      -dir  "$::DIR_PATH/pgp"
loadSource      -path "$::DIR_PATH/sem/FebSemWrapper.vhd"
loadIpCore      -path "$::DIR_PATH/sem/FebSem.xci"
loadConstraints -dir  "$::DIR_PATH/xdc"

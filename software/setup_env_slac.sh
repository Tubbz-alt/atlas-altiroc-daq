##############################################################################
## This file is part of 'ATLAS ALTIROC DEV'.
## It is subject to the license terms in the LICENSE.txt file found in the 
## top-level directory of this distribution and at: 
##    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
## No part of 'ATLAS ALTIROC DEV', including this file, 
## may be copied, modified, propagated, or distributed except according to 
## the terms contained in the LICENSE.txt file.
##############################################################################

# Setup environment
source /afs/slac.stanford.edu/g/reseng/vol26/anaconda/miniconda3/etc/profile.d/conda.sh

# Activate Rogue conda Environment
conda activate rogue_5.1.0
# conda activate rogue_3.7.0
# conda activate rogue_pre-release

# Python Package directories
export SURF_DIR=${PWD}/../firmware/submodules/surf/python

# Setup python path
export PYTHONPATH=${PWD}/python:${SURF_DIR}:${PYTHONPATH}

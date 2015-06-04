# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@

import os
import ConfigParser

from ...lib import hpdci
from ...lib import gvars
test_dir = hpdci.my_test_dir(__name__)
work_dir = hpdci.my_work_dir(__name__)

# Set your own catalog and schema.  Change the variable names if necessary.
w_catalog = gvars.test_catalog
w_schema = hpdci.my_schema(__name__)
my_schema = w_catalog + '.' + w_schema

# set SPJ library & procedure
spjrs_lib = 'qa_spjrs'
spjcall_lib = 'qa_spjcall'
dfr_lib = 'qa_dfr'
dfrrs_lib = 'qa_dfrrs'

spjrs_path = ''
spjcall_path = ''
dfr_path = ''
dfrrs_path = ''

def set_spjpath():
    global spjrs_path
    global spjcall_path
    global dfr_path
    global dfrrs_path

    spjroot = ''
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser.ConfigParser()
    config.read(os.path.abspath(scriptPath + '../../../../config.ini'))
    try:
        spjroot = config.get("pytest","libroot")
    except Exception:
        pass

    spjrs_path = spjroot + '/spjrs.jar'
    spjcall_path = spjroot + '/call.jar'
    dfr_path = spjroot + '/dfr.jar'
    dfrrs_path = spjroot + '/dfr_rs.jar'

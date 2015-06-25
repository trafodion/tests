# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

from ...lib import hpdci
from ...lib import gvars
test_dir = hpdci.my_test_dir(__name__)
work_dir = hpdci.my_work_dir(__name__)

# Set your own catalog and schema.  Change the variable names if necessary.
w_catalog = gvars.test_catalog
w_schema = hpdci.my_schema(__name__)
my_schema = w_catalog + '.' + w_schema

# Add additional variables here.
expfile = test_dir + """/hqc_exp"""
prepXX = """prepare XX from """
genexp = 0
qry = ''
num_hits = 0
num_pliterals = 0
pliterals = ''
num_npliterals = 0
npliterals = ''

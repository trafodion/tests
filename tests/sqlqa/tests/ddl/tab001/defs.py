# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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
a009_cat1 = w_catalog
a009_cat1_sch1 = w_schema + """_A009_CAT1_SCH1"""
a013_2_cat1 = w_catalog
a013_2_cat1_sch1 = w_schema + """_A013_2_CAT1_SCH1"""
a013_5_cat1 = w_catalog
a013_5_cat1_sch1 = w_schema + """_A013_5_CAT1_SCH1"""
a013_6_cat1 = w_catalog
a013_6_cat1_sch1 = w_schema + """_A013_6_CAT1_SCH1"""
a013_7_cat1 = w_catalog
a013_7_cat1_sch1 = w_schema + """_A013_7_CAT1_SCH1_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""
a013_7_cat1_sch2 = w_schema + """_A013_7_CAT1_SCH2_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"""
testcat = w_catalog
testcat2 = w_catalog
testsch1 = w_schema + """_T001A"""
testsch2 = w_schema + """_T001B"""
testsch3 = w_schema + """_SCH2"""
catddlA013 = w_catalog
schA013 = w_schema + """_schA013"""
aa11 = w_catalog

default_blocksize = '32768'


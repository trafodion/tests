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

from ...lib import hpdci
from ...lib import gvars
test_dir = hpdci.my_test_dir(__name__)
work_dir = hpdci.my_work_dir(__name__)

# Set your own catalog and schema.  Change the variable names if necessary.
w_catalog = gvars.test_catalog
w_schema = hpdci.my_schema(__name__)
my_schema = w_catalog + '.' + w_schema

# Add additional variables here.
# This is the mapping to the original test
# ${w_catalog}.${w_schema_new}       -> my_schema2
# ${w_catalog}.${w_schema_copy}      -> my_schema3
# ${w_catalog_new}.${w_schema}       -> my_schema4 
# ${w_catalog_new}.${w_schema_new}   -> my_schema5
# ${w_catalog_new}.${w_schema_copy}  -> my_schema6
# ${w_catalog_copy}.${w_schema}      -> my_schema7
# ${w_catalog_copy}.${w_schema_new}  -> my_schema8
# ${w_catalog_copy}.${w_schema_copy} -> my_schema9
my_schema2 = w_catalog + '.' + w_schema + '_2'
my_schema3 = w_catalog + '.' + w_schema + '_3'
my_schema4 = w_catalog + '.' + w_schema + '_4'
my_schema5 = w_catalog + '.' + w_schema + '_5'
my_schema6 = w_catalog + '.' + w_schema + '_6'
my_schema7 = w_catalog + '.' + w_schema + '_7'
my_schema8 = w_catalog + '.' + w_schema + '_8'
my_schema9 = w_catalog + '.' + w_schema + '_9'



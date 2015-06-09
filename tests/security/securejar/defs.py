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
#my_schema = w_catalog + '.' + w_schema
my_schema= 'SECURITY_SECUREJAR'
# Add additional variables here.

# set SPJ library & procedure

sec_libname1 = 'sec_lib1'
sec_libname2 = 'sec_lib2'
sec_lib1= 'SECURITY_SECUREJAR.' + sec_libname1
sec_lib2= 'SECURITY_SECUREJAR.' + sec_libname2

#spjrs_lib = 'qa_spjrs'
#spjcall_lib = 'qa_spjcall'
#dfr_lib = 'qa_dfr'
#dfrrs_lib = 'qa_dfrrs'

# set Jar file location
spjroot = '/home/trafodion'			# this location needs to be reset for test cluster
#spjroot = '/opt/home/chenjuan/pyframe'

#spjrs_path = spjroot + '/spjrs.jar'
#spjcall_path = spjroot + '/call.jar'
spjpath = spjroot + '/dfr.jar'
spjpathrs = spjroot + '/dfr_rs.jar'




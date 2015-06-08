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

import subprocess
from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None
_dbrootdci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    global _dbrootdci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    _dci.setup_schema(defs.my_schema)
    _dbrootdci = _testmgr.get_dbroot_dci_proc()
    _dbrootdci.setup_schema(defs.my_schema)

    # set up trafci command args
    defs.set_args()

    # replace schema names in .sql files
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c1.sql > " + defs.work_dir + "/c1.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c2.sql > " + defs.work_dir + "/c2.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c02.sql > " + defs.work_dir + "/c02.sql", shell=True)     
    
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.test_dir + "/c3.sql > " + defs.work_dir + "/c3.sql", shell=True) 
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c4.sql > " + defs.work_dir + "/c4.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.test_dir + "/c5.sql > " + defs.work_dir + "/c5.sql", shell=True)     
    
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.test_dir + "/c6.sql > " + defs.work_dir + "/c6.sql", shell=True) 
    
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.test_dir + "/c7.sql > " + defs.work_dir + "/c7.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.test_dir + "/c8.sql > " + defs.work_dir + "/c8.sql", shell=True) 
    
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.test_dir + "/c9.sql > " + defs.work_dir + "/c9.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c10.sql > " + defs.work_dir + "/c10.sql", shell=True)      
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c11.sql > " + defs.work_dir + "/c11.sql", shell=True)      
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c12.sql > " + defs.work_dir + "/c12_1.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.work_dir + "/c12_1.sql > " + defs.work_dir + "/c12.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c13.sql > " + defs.work_dir + "/c13.sql", shell=True)  
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c14.sql > " + defs.work_dir + "/c14.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c15.sql > " + defs.work_dir + "/c15.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c16.sql > " + defs.work_dir + "/c16.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c17.sql > " + defs.work_dir + "/c17.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c18.sql > " + defs.work_dir + "/c18_1.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.work_dir + "/c18_1.sql > " + defs.work_dir + "/c18.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c19.sql > " + defs.work_dir + "/c19.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c20.sql > " + defs.work_dir + "/c20_1.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.work_dir + "/c20_1.sql > " + defs.work_dir + "/c20.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c21.sql > " + defs.work_dir + "/c21.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c22.sql > " + defs.work_dir + "/c22.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c23.sql > " + defs.work_dir + "/c23.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c25.sql > " + defs.work_dir + "/c25.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c26.sql > " + defs.work_dir + "/c26.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c27.sql > " + defs.work_dir + "/c27.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c28.sql > " + defs.work_dir + "/c28.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c29.sql > " + defs.work_dir + "/c29.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c30.sql > " + defs.work_dir + "/c30.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c31.sql > " + defs.work_dir + "/c31_1.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.work_dir + "/c31_1.sql > " + defs.work_dir + "/c31.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c32.sql > " + defs.work_dir + "/c32_1.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.work_dir + "/c32_1.sql > " + defs.work_dir + "/c32.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c33.sql > " + defs.work_dir + "/c33_1.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.work_dir + "/c33_1.sql > " + defs.work_dir + "/c33.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c34.sql > " + defs.work_dir + "/c34_1.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.work_dir + "/c34_1.sql > " + defs.work_dir + "/c34.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c35.sql > " + defs.work_dir + "/c35_1.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.work_dir + "/c35_1.sql > " + defs.work_dir + "/c35.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c36.sql > " + defs.work_dir + "/c36.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c37.sql > " + defs.work_dir + "/c37.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c38.sql > " + defs.work_dir + "/c38.sql", shell=True)

    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c40.sql > " + defs.work_dir + "/c40.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c46.sql > " + defs.work_dir + "/c46_1.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.work_dir + "/c46_1.sql > " + defs.work_dir + "/c46.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/c48.sql > " + defs.work_dir + "/c48_1.sql", shell=True)
    subprocess.call("sed -e 's/TEST_SCHEMA_2/" + gvars.g_schema_tpch2x + "/g' " + defs.work_dir + "/c48_1.sql > " + defs.work_dir + "/c48.sql", shell=True)
    
    subprocess.call("sed -e 's/TEST_SCHEMA_1/" + defs.my_schema + "/g' " + defs.test_dir + "/cn002.sql > " + defs.work_dir + "/cn002.sql", shell=True)

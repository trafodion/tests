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

import b2pnl11_ddl
import b2pnl13_ddl
import b2pnl15_ddl
import b2pnl17_ddl
import b2pns01_ddl
import b2pns03_ddl
import b2pns05_ddl
import b2pns07_ddl
import b2pns09_ddl
import b2pwl02_ddl
import b2pwl04_ddl
import b2pwl06_ddl
import b2pwl08_ddl
import b2pwl10_ddl
import b2pwl12_ddl
import b2pwl14_ddl
import b2pwl16_ddl
import b2pwl18_ddl
import b2pwl20_ddl
import b2pwl22_ddl
import b2pwl24_ddl
import b2pwl26_ddl
import b2pwl28_ddl
import b2pwl30_ddl
import b2pwl32_ddl
import b2pwl34_ddl
import btpnl03_ddl
import btpnl17_ddl
import btpnl19_ddl
import btpnl21_ddl
import btpnl23_ddl
import btpns01_ddl
import btpns05_ddl
import btpns07_ddl
import btpns09_ddl
import btpns11_ddl
import btpns13_ddl
import btpns15_ddl
import btpns25_ddl
import btpwl02_ddl
import btpwl04_ddl
import btpwl06_ddl
import btpwl08_ddl
import btpwl10_ddl
import btpwl14_ddl
import btpwl16_ddl
import btpwl18_ddl
import btpwl20_ddl
import btpwl22_ddl
import btpws12_ddl
from ...lib import hpdci
import defs
import table

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

def test001(desc='Create tables'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    prop_template = defs.test_dir + '/../../lib/t4properties.template'
    prop_file = defs.work_dir + '/t4properties'
    hpdci.create_jdbc_propfile(prop_template, prop_file, defs.w_catalog, defs.w_schema)

    # turn off stats warning, so that they don't interfere with expect file
    stmt = """control query default hist_missing_stats_warning_level '0';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default hist_rowcount_requiring_stats '1000000';"""
    output = _dci.cmdexec(stmt)

    tablelist = [['btpns01', ['btpns01.dat'], '1500'], 
                 ['btpns05', ['btpns05.dat'], '1500'],
                 ['btpns07', ['btpns07.dat'], '1500'], 
                 ['btpns09', ['btpns09.dat'], '1500'],
                 ['btpns11', ['btpns11.dat'], '1500'], 
                 ['btpns13', ['btpns13.dat'], '1500'],
                 ['btpns15', ['btpns15.dat'], '1500'], 
                 ['btpns25', ['btpns25.dat'], '1500'],
                 ['btpnl03', ['btpnl03.dat'], '15000'], 
                 ['btpnl17', ['btpnl17.dat'], '150000'],
                 ['btpnl19', ['btpnl19.dat'], '150000'], 
                 ['btpnl21', ['btpnl21.dat'], '150000'],
                 ['btpnl23', ['btpnl23.dat'], '150000'], 
                 ['btpws12', ['btpws12.dat'], '1500'],
                 ['btpwl02', ['btpwl02.dat'], '5000'], 
                 ['btpwl04', ['btpwl04.dat'], '5000'],
                 ['btpwl06', ['btpwl06.dat'], '5000'], 
                 ['btpwl08', ['btpwl08.dat'], '5000'],
                 ['btpwl10', ['btpwl10.dat'], '5000'], 
                 ['btpwl14', ['btpwl14.dat'], '5000'],
                 ['btpwl16', ['btpwl16.dat'], '5000'], 
                 ['btpwl18', ['btpwl18.dat'], '5000'],
                 ['btpwl20', ['btpwl20.dat'], '5000'], 
                 ['btpwl22', ['btpwl22.dat'], '5000'],
                 ['b2pns01', ['b2pns01.dat'], '1500'], 
                 ['b2pns03', ['b2pns03.dat'], '1500'],
                 ['b2pns05', ['b2pns05.dat'], '1500'], 
                 ['b2pns07', ['b2pns07.dat'], '1500'],
                 ['b2pns09', ['b2pns09.dat'], '1500'], 
                 ['b2pnl11', ['b2pnl11.dat'], '150000'],
                 ['b2pnl13', ['b2pnl13.dat'], '150000'], 
                 ['b2pnl15', ['b2pnl15.dat'], '150000'],
                 ['b2pnl17', ['b2pnl17.dat'], '1500000'], 
                 ['b2pwl02', ['b2pwl02.dat'], '5000'],
                 ['b2pwl04', ['b2pwl04.dat'], '5000'], 
                 ['b2pwl06', ['b2pwl06.dat'], '5000'],
                 ['b2pwl08', ['b2pwl08.dat'], '5000'], 
                 ['b2pwl10', ['b2pwl10.dat'], '5000'],
                 ['b2pwl12', ['b2pwl12.dat'], '5000'], 
                 ['b2pwl14', ['b2pwl14.dat'], '5000'],
                 ['b2pwl16', ['b2pwl16.dat'], '5000'], 
                 ['b2pwl18', ['b2pwl18.dat'], '5000'],
                 ['b2pwl20', ['b2pwl20.dat'], '5000'], 
                 ['b2pwl22', ['b2pwl22.dat'], '5000'],
                 ['b2pwl24', ['b2pwl24.dat'], '5000'], 
                 ['b2pwl26', ['b2pwl26.dat'], '5000'],
                 ['b2pwl28', ['b2pwl28.dat'], '5000'], 
                 ['b2pwl30', ['b2pwl30.dat'], '5000'],
                 ['b2pwl32', ['b2pwl32.dat'], '5000'], 
                 ['b2pwl34', ['b2pwl34.dat'], '5000']]

    for items in tablelist:
        table.create_and_load(_testmgr, prop_file, items[0], items[1], items[2], ',')
   
    _testmgr.testcase_end(desc)


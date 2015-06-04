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

import b2unl11_ddl
import b2unl13_ddl
import b2unl15_ddl
import b2unl17_ddl
import b2uns01_ddl
import b2uns03_ddl
import b2uns05_ddl
import b2uns07_ddl
import b2uns09_ddl
import b2uwl02_ddl
import b2uwl04_ddl
import b2uwl06_ddl
import b2uwl08_ddl
import b2uwl10_ddl
import b2uwl12_ddl
import b2uwl14_ddl
import b2uwl16_ddl
import b2uwl18_ddl
import b2uwl20_ddl
import b2uwl22_ddl
import b2uwl24_ddl
import b2uwl26_ddl
import b2uwl28_ddl
import b2uwl30_ddl
import b2uwl32_ddl
import b2uwl34_ddl
import btunl03_ddl
import btunl17_ddl
import btunl19_ddl
import btunl21_ddl
import btunl23_ddl
import btuns01_ddl
import btuns05_ddl
import btuns07_ddl
import btuns09_ddl
import btuns11_ddl
import btuns13_ddl
import btuns15_ddl
import btuns25_ddl
import btuwl02_ddl
import btuwl04_ddl
import btuwl06_ddl
import btuwl08_ddl
import btuwl10_ddl
import btuwl14_ddl
import btuwl16_ddl
import btuwl18_ddl
import btuwl20_ddl
import btuwl22_ddl
import btuws12_ddl
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

    tablelist = [['b2unl11', ['b2unl11.dat'], '150000'], 
                 ['b2unl13', ['b2unl13.dat'], '150000'],
                 ['b2unl15', ['b2unl15.dat'], '150000'], 
                 ['b2unl17', ['b2unl17.dat'], '1500000'],
                 ['b2uns01', ['b2uns01.dat'], '1500'], 
                 ['b2uns03', ['b2uns03.dat'], '1500'],
                 ['b2uns05', ['b2uns05.dat'], '1500'], 
                 ['b2uns07', ['b2uns07.dat'], '1500'],
                 ['b2uns09', ['b2uns09.dat'], '1500'], 
                 ['b2uwl02', ['b2uwl02.dat'], '5000'],
                 ['b2uwl04', ['b2uwl04.dat'], '5000'], 
                 ['b2uwl06', ['b2uwl06.dat'], '5000'],
                 ['b2uwl08', ['b2uwl08.dat'], '5000'], 
                 ['b2uwl10', ['b2uwl10.dat'], '5000'],
                 ['b2uwl12', ['b2uwl12.dat'], '5000'], 
                 ['b2uwl14', ['b2uwl14.dat'], '5000'],
                 ['b2uwl16', ['b2uwl16.dat'], '5000'], 
                 ['b2uwl18', ['b2uwl18.dat'], '5000'],
                 ['b2uwl20', ['b2uwl20.dat'], '5000'], 
                 ['b2uwl22', ['b2uwl22.dat'], '5000'],
                 ['b2uwl24', ['b2uwl24.dat'], '5000'], 
                 ['b2uwl26', ['b2uwl26.dat'], '5000'],
                 ['b2uwl28', ['b2uwl28.dat'], '5000'], 
                 ['b2uwl30', ['b2uwl30.dat'], '5000'],
                 ['b2uwl32', ['b2uwl32.dat'], '5000'], 
                 ['b2uwl34', ['b2uwl34.dat'], '5000'],
                 ['btunl03', ['btunl03.dat'], '15000'], 
                 ['btunl17', ['btunl17.dat'], '150000'],
                 ['btunl19', ['btunl19.dat'], '150000'], 
                 ['btunl21', ['btunl21.dat'], '150000'],
                 ['btunl23', ['btunl23.dat'], '150000'], 
                 ['btuns01', ['btuns01.dat'], '1500'],
                 ['btuns05', ['btuns05.dat'], '1500'], 
                 ['btuns07', ['btuns07.dat'], '1500'],
                 ['btuns09', ['btuns09.dat'], '1500'], 
                 ['btuns11', ['btuns11.dat'], '1500'],
                 ['btuns13', ['btuns13.dat'], '1500'], 
                 ['btuns15', ['btuns15.dat'], '1500'],
                 ['btuns25', ['btuns25.dat'], '1500'], 
                 ['btuwl02', ['btuwl02.dat'], '5000'],
                 ['btuwl04', ['btuwl04.dat'], '5000'], 
                 ['btuwl06', ['btuwl06.dat'], '5000'],
                 ['btuwl08', ['btuwl08.dat'], '5000'], 
                 ['btuwl10', ['btuwl10.dat'], '5000'],
                 ['btuwl14', ['btuwl14.dat'], '5000'], 
                 ['btuwl16', ['btuwl16.dat'], '5000'],
                 ['btuwl18', ['btuwl18.dat'], '5000'], 
                 ['btuwl20', ['btuwl20.dat'], '5000'],
                 ['btuwl22', ['btuwl22.dat'], '5000'], 
                 ['btuws12', ['btuws12.dat'], '1500']]

    for items in tablelist:
        table.create_and_load(_testmgr, prop_file, items[0], items[1], items[2], ',')
    
    _testmgr.testcase_end(desc)


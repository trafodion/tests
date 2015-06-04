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
import defs

_testmgr = None
_testlist = []
_dci = None

#*********************************************
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""self_referencing update allowed"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #********************************************
    
    stmt = """control query default pos_num_of_partns '4';"""
    output = _dci.cmdexec(stmt)
    stmt = """create table loc
(locid       int           not null not droppable
,freelocstat int           not null not droppable
,dtimemod    timestamp(0)  not null not droppable
,usrmod      char(15)      not null not droppable
,pgmmod      char(15)      not null not droppable
,modcnt      int           not null not droppable
,said        int           not null not droppable
,rkid        int
,xx          int
,yy          int
,zz          int
,locposx     int
,coid        char(15)      default ''
,locstat     int
,primary key (locid)
)
attributes extent (16,64);"""

    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """control query default pos_num_of_partns reset;"""
    output = _dci.cmdexec(stmt)
    
    # #sh ${import} $my_schema.loc -I $test_dir/loc.dat
    prop_template = defs.test_dir + '/../../lib/t4properties.template'
    prop_file = defs.work_dir + '/t4properties'
    hpdci.create_jdbc_propfile(prop_template, prop_file, defs.w_catalog, defs.w_schema)

    table = defs.my_schema + """.loc"""
    data_file = defs.test_dir + """/loc.dat"""
    output = _testmgr.data_loader(defs.work_dir, prop_file, table, data_file, ',')
    _dci.expect_loaded_msg(output)

    stmt = """select count(*) from """ + defs.my_schema + """.loc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_str_token(output, """10000""")
    
    stmt = """create index locix1 on loc
(pgmmod, modcnt, dtimemod);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count(*)
from loc
where
said        = 10
and freelocstat <> 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    stmt = """UPDATE  loc
SET  freelocstat = 0,
dtimemod    = TIMESTAMP '2006-04-28 09:25:46',
usrmod      = '',
pgmmod      = 'resetStat',
modcnt      = modcnt+1
WHERE said        = 10
AND freelocstat <> 0
AND EXISTS (SELECT locid
FROM loc loc_x
WHERE loc_x.said    = loc.said
AND loc_x.rkid    = loc.rkid
AND loc_x.xx      = loc.xx
AND loc_x.yy      = loc.yy
AND loc_x.locposx = loc.locposx
AND loc.zz        < loc_x.zz
AND loc_x.locstat = 0
AND loc_x.coid    = '')
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select count(*)
from loc
where
freelocstat = 0 and
dtimemod    = TIMESTAMP '2006-04-28 09:25:46' and
usrmod      = '' and
pgmmod      = 'resetStat' and
modcnt      = modcnt+1 and
said        = 10 and
freelocstat <> 0;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output)
    
    _testmgr.testcase_end(desc)


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

# TEST:0389 95-character graphic subset of ASCII!
# NOTE:  OPTIONAL test
# NOTE:0389 Collating sequence is implementor defined

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """DELETE FROM AA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    # Making sure the table is empty
    
    # setup
    stmt = """INSERT INTO AA VALUES('@ at');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('`-qt');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('!exc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('"dqt');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('#pou');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('$dol');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('%pct');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('&amp');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('''+qt');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('(lpr');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES(')rpr');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('*ast');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('aaaa');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES(':col');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('+plu');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES(';sem');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('[lbk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('{lbc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES(',com');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('< lt');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('\bsl');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('|dvt');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('-hyp');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('=equ');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES(']rbk');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('}rbc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('.per');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('> gt');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('^hat');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('~til');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('/ sl');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('?que');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('_und');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #$SQL_inserted_msg 1
    stmt = """INSERT INTO AA VALUES('AAAA');"""
    output = _dci.cmdexec(stmt)
    stmt = """INSERT INTO AA VALUES('0000');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('9999');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('zzzz');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """INSERT INTO AA VALUES('  sp');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #$SQL_inserted_msg 1
    stmt = """INSERT INTO AA VALUES('ZZZZ');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SELECT * FROM VWAA
ORDER BY CHARTEST;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_selected_msg(output, 39)
    # PASS:0389 If character in 1st position matches                 ?
    # PASS:0389    description in positions 2-4                      ?
    # PASS:0389 If ASCII, then ORDER is: space followed by characters?
    
    stmt = """SELECT COUNT(*)
FROM VWAA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0389.exp""", """s2""")
    # PASS:0389 If count = 39?
    
    # restore
    stmt = """ROLLBACK WORK;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select count (*) FROM VWAA;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test0389.exp""", """s3""")
    # pass if count = 0
    
    # END TEST >>> 0389 <<< END TEST
    

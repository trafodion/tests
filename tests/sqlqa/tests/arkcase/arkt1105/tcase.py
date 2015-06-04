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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""a01"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1105:A01
    #  Description:        Verifies SQL Transaction for audited objects
    #  Expected Results:   Good transactions, no data corruption.
    #
    # =================== End Test Case Header  ===================
    #
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    
    #  ---------------------------
    
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTAUD values ('abc',1), ('abd',2), ('abe',3);"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from BTAUD;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from VUAUD;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from BTNOAUD ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTNOAUD values ('abd',2), ('noa',99);"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from BTNOAUD;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from VUNOAUD;"""
    output = _dci.cmdexec(stmt)
    
    #  ---------------------------
    #  Longevity of implicitly-started transaction; requires explicit user
    #  commit/rollback; 
    #
    #  Transaction implicitly started for DML on an audited table should
    #  live longer than the DML statement that caused the transaction to
    #  be started.
    #  ---------------------------
    #
    #  ---------------------------
    #    Id: TX.001   Warning on attempt to start user TXN when system-started TXN (for SELECT on audited table)
    #                       is in progress.
    #  ---------------------------
    #
    #  Expect { ('abc',1), ('abd',2), ('abe',3) }
    
    stmt = """select * from BTAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s0')
    
    # Expect success -- transaction in progress.
    
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Expect count=1 (audited joined to NONaudited table).
    stmt = """select count(*) from BTAUD ta, BTNOAUD tn
where (ta.c1,ta.c2)= (tn.c1,tn.c2) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s1')
    #
    # Expect success -- transaction in progress because audited table
    # was accessed within join.
    
    stmt = """show transaction;"""
    output = _dci.cmdexec(stmt)
    #
    # ---------------------------
    #   Id: TX.002   Message on attempt to start user TXN when system-started TXN (for INSERT into updateable view on audited table)
    #                      is in progress.
    # ---------------------------
    #
    stmt = """insert into VUAUD values ('aud',4), ('aud',5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #
    #  Expect error -- transaction in progress.
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    #
    #  Expect { ('abc',1), ('abd',2), ('abe',3), ('aud',4), ('aud',5) }
    stmt = """select * from BTAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3')
    #
    # Should succeed -- system-initiated transaction in progress.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check what remains and rollback.
    #  Expect { ('abc',1), ('abd',2), ('abe',3) }
    stmt = """select * from BTAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s4')
    #
    # ---------------------------
    #   Id: TX.003   Warning on attempt to start user TXN when system-started TXN (for UPDATE on audited table)
    #                      is in progress.
    #   Id: TX.031   EXECUTE is TXN-initiating when statement associated with it is TXN-initiating.
    # ---------------------------
    #
    # Expect 0 rows altered -- no value of c2 equals 42.
    # 08/09/07 This test passes only when the CQD POS is 'ON'. The table needs to
    # have the primary key defined; otherwise it fails with the error and warning.
    stmt = """Prepare s From update BTAUD set c2 = ( select max(c2) from BTAUD ) where c2=42 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s3a')
    #
    # Prepare does not start a transaction; start and end one
    # here to check.
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Execute then commit, which should be ok -- transaction starts because
    # of EXECUTE ... UPDATE even though no row satisfies the update.
    #$err_msg 15017 S
    stmt = """execute s ;"""
    output = _dci.cmdexec(stmt)
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check what remains and commit.
    #  Expect { ('abc',1), ('abd',2), ('abe',3) }
    stmt = """select * from BTAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s5')
    # Expect 2 rows altered (for rows with c2=1 and c2=2).
    stmt = """Prepare s From update BTAUD set c2 = 5 where c2<3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    #
    # Prepare does not start a transaction; start and end one
    # here to check.
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Expect error on BEGIN after execute; transaction in progress
    # from EXECUTE ... UPDATE.
    stmt = """execute s ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 2)
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    #
    #  Check what remains and Reset values.
    #  Expect { ('abc',5), ('abd',5), ('abe',3) }
    stmt = """select * from BTAUD order by c1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s7')
    stmt = """delete from BTAUD;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    stmt = """insert into BTAUD values ('abc',1), ('abd',2), ('abe',3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 3)
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #   Id: TX.004   Warning on attempt to start user TXN when system-started TXN (for DELETE on audited table)
    #                      is in progress.
    #                Also use DELETE within transactions.
    # ---------------------------
    #
    # Expect 1 rows deleted.
    stmt = """prepare prepd from delete from BTAUD where c2 = 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute prepd ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    #  Expect { ('abc',1), ('abe',3) }
    stmt = """select * from BTAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s8')
    #
    # Expect ok -- transaction in progress.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check what remains and commit.
    #  Expect { ('abc',1), ('abd',2), ('abe',3) }
    stmt = """select * from BTAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s9')
    # Try it again -- expect 0 rows deleted but transaction is started.
    stmt = """prepare prepd from delete from BTAUD where c2 = 47 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    stmt = """execute prepd ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    #
    #  Expect { ('abc',1), ('abd',2), ('abe',3) }
    stmt = """select * from BTAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a01exp""", 'a01s10')
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    # Cleanup -- remove tables in POSTUNIT cleanup.
    # ---------------------------
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)
    # We are done.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""a02"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1105:A02
    #  Description:        Verifies SQL Transaction for NONaudited objects
    #  Expected Results:   Good transactions, no data corruption.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    
    #  ---------------------------
    #
    #  ---------------------------
    #  Longevity of implicitly-started transaction; requires explicit user
    #  commit/rollback;
    #
    #  For non-audited table should NOT get transaction started
    #  by DML statements.
    #  ---------------------------
    
    stmt = """delete from BTNOAUD ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTNOAUD values ('abd',2), ('noa',99);"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from BTNOAUD;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from VUNOAUD;"""
    output = _dci.cmdexec(stmt)
    
    #  ---------------------------
    #  Transactions are not initiated by DML
    #  on NONaudited objects.
    #  ---------------------------
    #    Id: TX.005   No system-started TXN for SELECT on NONaudited table.
    #  ---------------------------
    #
    #  Expect { ('abd',2), ('noa',99) }
    stmt = """select * from BTNOAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s0')
    #
    #  Expect error -- no transaction already in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # ---------------------------
    #   Id: TX.006   No system-started TXN for INSERT into NONaudited table.
    # ---------------------------
    #
    # Insert 2 rows.
    
    stmt = """insert into BTNOAUD values ('aud',4), ('aud',5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 2)
    #
    #  Expect error -- no transaction in progress.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Should start work -- no transaction already in progress.
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Expect { ('abd',2), ('aud',4), ('aud',5), ('noa',99) }
    stmt = """select * from BTNOAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s3')
    #
    # Should succeed.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #   Id: TX.007   No system-started TXN for UPDATE on NONaudited table).
    # ---------------------------
    #
    # Expect 2 rows altered.
    stmt = """update BTNOAUD set c2 = 99 where c1>'auc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    # Should start work -- no transaction already in progress.
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    #
    #  Expect { ('abd',2), ('aud',99), ('aud',99), ('noa',99) }
    stmt = """select * from BTNOAUD order by c1, c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s4')
    stmt = """UNLOCK TABLE BTNOAUD;"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #   Id: TX.008   No system-started TXN for DELETE on updateable view on NONaudited table).
    #
    # ---------------------------
    #
    stmt = """delete from VUNOAUD where c2 = 99 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    # Should start work -- no transaction already in progress.
    stmt = """BEGIN WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    #
    #  Check what remains and commit.
    #  Expect { ('abd',2) }
    stmt = """select * from BTNOAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a02exp""", 'a02s5')
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    # Cleanup -- remove remaining rows!
    # ---------------------------
    #
    # DML on Unaudited objects doesn't start transaction.
    stmt = """delete from VUNOAUD where c2 = 99 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 0)
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test003(desc="""a03"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1105:A03
    #  Description:        Verifies SQL Transaction READ UNCOMMITTED.
    #  Expected Results:   Good transactions, no data corruption.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTAUD values ('abc',1), ('abd',2), ('abe',3);"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from BTAUD;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from VUAUD;"""
    output = _dci.cmdexec(stmt)
    # 05/11/09 added following commit work to clean out any active transaction
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    
    #
    # Transaction implicitly started for DML on an audited table should
    # live longer than the DML statement for it is started.
    # ---------------------------
    #
    # ---------------------------
    # Transactions are not initiated by DML executing under
    # READ UNCOMMITTED on audited objects.
    # ---------------------------
    #  Id:TX.010a READ UNCOMMITTED: No system-started TXN for SELECT
    #  on audited table.
    #  Id:TX.010b READ UNCOMMITTED: No system-started TXN for INSERT
    #  into audited table.
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;"""
    output = _dci.cmdexec(stmt)
    
    #  Attempt to insert rows; this fails; note that you cannot modify
    #  database with READ UNCOMMITTED.
    
    stmt = """insert into BTAUD values ('aud',4), ('aud',5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3140')
    
    #  Expect error -- no transaction in progress.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8609')
    #
    #  Expect (('abc',1), ('abd',2), ('abe',3))
    stmt = """select * from BTAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s2')
    #
    #  Expect error -- no transaction already in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
    
    # ---------------------------
    #   Id: TX.010c   READ UNCOMMITTED: No system-started TXN for UPDATE on updateable view on audited table).
    # ---------------------------
    
    stmt = """SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;"""
    output = _dci.cmdexec(stmt)
    
    #  Expect 3 rows altered.
    stmt = """update VUAUD set c2 = 99 where c1>'auc';"""
    output = _dci.cmdexec(stmt)
    #
    #  Expect error -- no transaction in progress.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8609')
    #
    #  Expect (('abc',1), ('abd',2), ('abe',3))
    stmt = """select * from VUAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s6')
    #
    #  Expect error -- no transaction already in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
    #
    # ---------------------------
    #   Id: TX.010d   READ UNCOMMITTED: No system-started TXN for DELETE on audited table).
    # ---------------------------
    
    stmt = """SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;"""
    output = _dci.cmdexec(stmt)
    
    # Attempt to remove row from the table; this fails; note that you cannot modify
    #  database with READ UNCOMMITTED.
    stmt = """delete from BTAUD where c2 = 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3140')
    #
    #  Expect error -- no transaction in progress.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8609')
    #
    #  Check what remains.
    #  Expect (('abc',1), ('abd',2), ('abe',3))
    stmt = """select * from BTAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a03exp""", 'a03s10')
    #
    #  Expect error -- no transaction already in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc="""a04"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1105:A04
    #  Description:        Verifies SQL Read Uncommitted for NONaudited objects
    #  Expected Results:   Good transactions, no data corruption.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """create table T1(
varchar1 varchar(21)
, varchar2 varchar(23)
, somenumber int
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert Into T1 Values('on', 'off', 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """SET TRANSACTION READ ONLY;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert Into T1 Values('non', 'compos', 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3141')
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from BTNOAUD ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTNOAUD values ('abd',2), ('noa',99);"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from BTNOAUD;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from VUNOAUD;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------
    # Transactions are not initiated by DML executing under
    # READ UNCOMMITTED on Unaudited objects.
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into BTAUD values ('ccc', 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """ROLLBACK;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into BTAUD values ('aaa', 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3140')
    
    #  Have to commente it out since it abends mxci.
    #
    stmt = """insert into BTAUD values ('ccc', 1);"""
    output = _dci.cmdexec(stmt)
    
    #  No transaction in progress (checked in negative tests).
    #
    #  ---------------------------
    #    Id: TX.013   With READ UNCOMMITTED: No system-started TXN for SELECT on NONaudited table.
    #    Id: TX.014   With READ UNCOMMITTED: No system-started TXN for INSERT into NONaudited table.
    #  ---------------------------
    #
    #  Attempt to empty the table; this fails; note that you cannot modify
    #  database with READ UNCOMMITTED.
    stmt = """delete from BTNOAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3140')
    #  Expect 2 rows as entered in pre-test code.
    stmt = """select count(*) from BTNOAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s1')
    #
    #  Attempt to insert rows; this fails; note that you cannot modify
    #  database with READ UNCOMMITTED.
    stmt = """insert into BTNOAUD values ('aud',4), ('aud',5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3140')
    #
    #  Expect error -- no transaction in progress.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8609')
    #
    #  Expect 2 rows (('abd',2), ('noa',99))
    stmt = """select * from BTNOAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s4')
    #  Expect error message on attempt to Delete.
    stmt = """delete from BTNOAUD where c2 > 3 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3140')
    #
    #  Expect error -- no transaction already in progress.
    stmt = """COMMIT WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8605')
    #
    #  Expect 2 rows (('abd',2), ('noa',99))
    stmt = """select * from BTNOAUD order by c2;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a04exp""", 'a04s7')
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test005(desc="""a05"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # =================  Begin Test Case Header  ==================
    #
    #  Test case name:     T1105:A05
    #  Description:        Verifies SQL Read Committed and Repeatable Read, for audited objects
    #  Expected Results:   Good transactions, no data corruption.
    #
    # =================== End Test Case Header  ===================
    
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    stmt = """insert into BTAUD values ('abc',1), ('abd',2), ('abe',3);"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from BTAUD;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from VUAUD;"""
    output = _dci.cmdexec(stmt)
    
    # ---------------------------
    # Longevity of implicitly-started transaction; requires explicit user
    # commit/rollback; 
    #
    # Transaction implicitly started for DML on an audited table should
    # live longer than the DML statement that caused the transaction to
    # be started.
    # ---------------------------
    #
    #   Id: TX.021   With READ COMMITTED, then ROLLBACK (should be ok).
    #                like "clean"
    # ---------------------------
    
    stmt = """SET TRANSACTION AUTOCOMMIT OFF;"""
    output = _dci.cmdexec(stmt)
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED ;"""
    output = _dci.cmdexec(stmt)
    
    #  Expect 3 rows as inserted in pre-test code: (('abc',1) ('abd',2) ('abe',3))
    stmt = """select * from BTAUD order by c2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s0')
    
    # stmt = """ROLLBACK WORK ;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    #
    # Insert/select/rollback.
    stmt = """insert into BTAUD values ('isolation level READ COMMITTED', 21) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into BTAUD values ('per ardua ad astra', 91) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    #  Expect 5 rows -- the 3 seen above plus the 2 just inserted.
    stmt = """select * from BTAUD order by c2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s1')
    # Expect Rollback should succeed.
    stmt = """ROLLBACK WORK ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    #  Check that the original 3 rows remain.
    stmt = """select * from BTAUD order by c2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s2')
    # Expect Rollback should succeed.
    # stmt = """ROLLBACK WORK ;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #   Id: TX.022   With REPEATABLE READ, INSERT, then COMMIT (should be ok).
    # ---------------------------
    
    stmt = """SET TRANSACTION ISOLATION LEVEL REPEATABLE READ ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into BTAUD values ('isolation level repeatable read', 22) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # Expect Commit should succeed.
    # stmt = """commit work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    #
    #  Expect 1 row inserted above.
    stmt = """select * from BTAUD where c2 = 22 order by c2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s3')
    #
    # Expect OK.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #   Id: TX.023   With READ COMMITTED, DELETE, then attempt to start a user TXN (should get warning that TXN is in progress); commit work.
    # ---------------------------
    
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED ;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """delete from BTAUD where c2 = 22 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)
    
    #  Expect error.
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    #
    # Expect Commit should succeed.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    #   Id: TX.024   With REPEATABLE READ, UPDATE, then attempt to start a user TXN (should get warning that TXN is in progress); commit work
    # ---------------------------
    
    stmt = """SET TRANSACTION ISOLATION LEVEL REPEATABLE READ ;"""
    output = _dci.cmdexec(stmt)
    
    #  Expect ((0))
    stmt = """select count(*) from BTAUD where c2 = 24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s5')
    #  Expect ((1))
    stmt = """select count(*) from BTAUD where c2 > 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s6')
    # Expect Commit should succeed.
    # stmt = """commit work;"""
    # output = _dci.cmdexec(stmt)
    # _dci.expect_complete_msg(output)
    #
    stmt = """update BTAUD set c2 = 24 where c2 > 2 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #
    #  Expect error.
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    #
    #  Expect ((1))
    stmt = """select count(*) from BTAUD where c2 = 24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s8')
    #
    # Expect Commit should succeed.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # Insert then as above.
    stmt = """insert into BTAUD values ('isolation level REPEATABLE READ', 24) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into BTAUD values ('Sufficient to the day is the care thereof', 94) ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """select count(*) from BTAUD where c2 = 24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s9')
    stmt = """select count(*) from BTAUD where c2 > 90 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s10')
    # Expect Commit should succeed.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """update BTAUD set c2 = 24 where c2 > 90 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    #  Expect error.
    stmt = """begin work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8603')
    #  Expect ((3))
    stmt = """select count(*) from BTAUD where c2 = 24 ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a05exp""", 'a05s12')
    # Expect Commit should succeed.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    #
    # ---------------------------
    # Cleanup -- here we remove rows.
    # Remove tables in POSTUNIT cleanup.
    # ---------------------------
    stmt = """delete from BTAUD ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 5)
    # Expect Commit should succeed.
    stmt = """commit work;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SET TRANSACTION AUTOCOMMIT ON;"""
    output = _dci.cmdexec(stmt)
    stmt = """SET TRANSACTION ISOLATION LEVEL READ COMMITTED ;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)


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
    
    stmt = """insert into T1 values(2, 1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T1 values(4, 2);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T1 values(6, 3);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T1 values(8,4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T1 values(10,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T1 values(12, -32768);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T1(A) values (11);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into T2 values(2, 1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T2 values(4, 2,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T2 values(6, 3,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T2 values(8, 4,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T2 values(10,5,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T2 values(6, 6,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T2 values(8, -32768 , -923720368547588);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T2(C,D) values (4,14);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into T3 values(2, 1,1,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T3 values(4, 2,2,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T3 values(6, 3,3,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T3 values(8, 4,4,1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T3 values(10, -32768 , -923720368547588, -99999.999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T3(F,G,H) values (12,5,5);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into T4 values(2, 1,1,1,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T4 values(4, 2,2,2,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T4 values(6, 3,3,3,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T4 values(8, 4,4,4,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T4 values(10, 5,5,5,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T4 values(12, -32768 , -923720368547588, -99999.999, -999999.99999999);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T4(J,K,L,M) values (14, 6,6,6);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into T5 values(2,1,1,1,0,  '1999-12-31', 1,1,1, TIMESTAMP'1999-01-01 00:00:00.000000', INTERVAL '99-02'YEAR TO MONTH, '1',TIME '00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T5 values(4, 2,1,2,0,  '1990-12-31', 1,1,1, TIMESTAMP '1997-01-01 00:00:00.000000', INTERVAL '99-02'YEAR TO MONTH, '2', TIME '00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T5 values(6, 3,1,3,0,  '1991-12-31', 1,1,1, TIMESTAMP'1998-01-01 00:00:00.000000',INTERVAL '99-02'YEAR TO MONTH, '2',  TIME '00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T5 values(7, -32768 , -923720368547588, -99999.999, -999999.99999999,  '1991-12-31', 1,1,1, TIMESTAMP '1998-01-01 00:00:00.000000', INTERVAL '99-02'YEAR TO MONTH, '2',  TIME '00:00:00');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T5(P,R) values (7, 7);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T5 values(8, -32768,  -923720368547588, -99999.900, -999999.99999000, '2006-06-15', 7.000000000001, -2.2250738585072014, -1.17549435e-38, TIMESTAMP '2006-06-23 17:56:59.300439', INTERVAL '06-06'YEAR TO MONTH, '1', TIME '17:05:45');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T5 values(9, 32767,  923720368547587,   999998.999, 9999999.999999999,  '2005-07-24', 6.000001, 4509.000000001, 3.40282347e+38, TIMESTAMP '2005-12-24 09:21:11.234039', INTERVAL '06-07'YEAR TO MONTH, '12', TIME '07:35:54');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into T5 values(10,  7892,  9809876586,  23990.78, 8769.1200454,  '2000-04-12', 11897.9998877656,  898889.00000997, 555.23,   TIMESTAMP '1999-01-01 02:11:33.100439', INTERVAL '06-11' YEAR TO MONTH, '123', TIME '00:21:30');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)

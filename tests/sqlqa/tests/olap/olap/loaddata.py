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

    stmt = """delete from ee1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
  
    stmt = """insert into ee1 values
(1,'Zacker'   ,'Abe'     ,'M',1,1,12000.00,1800.00,200.00,date '12/07/1941'),
(2,'Andersen' ,'Abby'    ,'F',1,1,12000.00,1800.00,200.00,date '12/07/1942'),
(3,'Quan'     ,'Abe'     ,'M',2,1,12000.00,NULL,NULL,date '12/09/1942'),
(4,'Yang'     ,'Arnold'  ,'M',3,1,12000.00,1500.00,150.00,date '12/07/1943'),
(5,'Richarson','Becky'   ,'F',9,2,15000.00,7500.00,200,date '12/09/1941'),
(6,'Li'       ,'Arthur'  ,'M',2,3,18000.00,1500.00,150.00,date '12/08/1942'),
(7,'Sharma'   ,'Arthur'  ,'M',5,3,18000.00,3000.00,1500.00,date '12/08/1943'),
(8,'Li'       ,'Amy'     ,'F',2,3,18000.00,3000.00,1500.00,date '12/07/1943'),
(9,'Martinez' ,'Annette' ,'F',6,4,24000.00,2000.00,500.00,date '12/09/1942'),
(10,'Zhang'   ,'Abby'    ,'F',3,4,24000.00,2000.00,500.00,date '12/07/1941'),
(11,'Yurgu'   ,'Becky'   ,'F',3,4,24000.00,NULL,NULL,date '12/07/1945'),
(12,'Kankark' ,'Bill'    ,'M',9,4,24000.00,1800.00,500.00,date '12/07/1941'),
(13,'Wilbert' ,'Aloysius','M',1,6,72000.00,1200.00,200.00,date '12/08/1942'),
(14,'Nelluru' ,'Bruce'   ,'M',9,7,90000.00,1800.00,500.00,date '12/09/1941'),
(15,'Therber' ,'Arnold'  ,'M',2,7,90000.00,1000.00,200,date '12/09/1941'),
(16,'Andersen','Bruce'   ,'M',5,7,90000.00,5000.00,2000,date '12/07/1941'),
(17,'Cate'    ,'Becky'   ,'F',9,7,90000.00,5000.00,2000.00,date '12/08/1941'),
(18,'Linville','Bruce'   ,'M',1,8,92000.00,1000.00,1500.00,date '12/09/1941'),
(19,'Zacker'  ,'Bill'    ,'M',5,5,30000.00,NULL,9000.00,date '12/08/1945'),
(20,'Buick'   ,'Bridget' ,'F',3,5,30000.00,1500.00,NULL,date '12/08/1941');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 20)
 

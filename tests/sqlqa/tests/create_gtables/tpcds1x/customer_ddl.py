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
    
    stmt = """create table customer
(
c_customer_sk             integer               not null,
c_customer_id             char(16)              not null,
c_current_cdemo_sk        integer                       ,
c_current_hdemo_sk        integer                       ,
c_current_addr_sk         integer                       ,
c_first_shipto_date_sk    integer                       ,
c_first_sales_date_sk     integer                       ,
c_salutation              char(10)                      ,
c_first_name              char(20)                      ,
c_last_name               char(30)                      ,
c_preferred_cust_flag     char(1)                       ,
c_birth_day               integer                       ,
c_birth_month             integer                       ,
c_birth_year              integer                       ,
c_birth_country           varchar(20)                   ,
c_login                   char(13)                      ,
c_email_address           char(50)                      ,
c_last_review_date        char(10)                      ,
primary key (c_customer_sk)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ hash2 partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    

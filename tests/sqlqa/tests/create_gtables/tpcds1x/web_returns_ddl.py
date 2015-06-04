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
    
    stmt = """create table web_returns
(
wr_returned_date_sk       integer                       ,
wr_returned_time_sk       integer                       ,
wr_item_sk                integer               not null,
wr_refunded_customer_sk   integer                       ,
wr_refunded_cdemo_sk      integer                       ,
wr_refunded_hdemo_sk      integer                       ,
wr_refunded_addr_sk       integer                       ,
wr_returning_customer_sk  integer                       ,
wr_returning_cdemo_sk     integer                       ,
wr_returning_hdemo_sk     integer                       ,
wr_returning_addr_sk      integer                       ,
wr_web_page_sk            integer                       ,
wr_reason_sk              integer                       ,
wr_order_number           integer               not null,
wr_return_quantity        integer                       ,
wr_return_amt             decimal(7,2)                  ,
wr_return_tax             decimal(7,2)                  ,
wr_return_amt_inc_tax     decimal(7,2)                  ,
wr_fee                    decimal(7,2)                  ,
wr_return_ship_cost       decimal(7,2)                  ,
wr_refunded_cash          decimal(7,2)                  ,
wr_reversed_charge        decimal(7,2)                  ,
wr_account_credit         decimal(7,2)                  ,
wr_net_loss               decimal(7,2)                  ,
primary key (wr_item_sk, wr_order_number)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ hash2 partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    

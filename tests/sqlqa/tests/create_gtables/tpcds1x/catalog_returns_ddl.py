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
    
    stmt = """create table catalog_returns
(
cr_returned_date_sk       integer                       ,
cr_returned_time_sk       integer                       ,
cr_item_sk                integer               not null,
cr_refunded_customer_sk   integer                       ,
cr_refunded_cdemo_sk      integer                       ,
cr_refunded_hdemo_sk      integer                       ,
cr_refunded_addr_sk       integer                       ,
cr_returning_customer_sk  integer                       ,
cr_returning_cdemo_sk     integer                       ,
cr_returning_hdemo_sk     integer                       ,
cr_returning_addr_sk      integer                       ,
cr_call_center_sk         integer                       ,
cr_catalog_page_sk        integer                       ,
cr_ship_mode_sk           integer                       ,
cr_warehouse_sk           integer                       ,
cr_reason_sk              integer                       ,
cr_order_number           integer               not null,
cr_return_quantity        integer                       ,
cr_return_amount          decimal(7,2)                  ,
cr_return_tax             decimal(7,2)                  ,
cr_return_amt_inc_tax     decimal(7,2)                  ,
cr_fee                    decimal(7,2)                  ,
cr_return_ship_cost       decimal(7,2)                  ,
cr_refunded_cash          decimal(7,2)                  ,
cr_reversed_charge        decimal(7,2)                  ,
cr_store_credit           decimal(7,2)                  ,
cr_net_loss               decimal(7,2)                  ,
primary key (cr_item_sk, cr_order_number)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ hash2 partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    

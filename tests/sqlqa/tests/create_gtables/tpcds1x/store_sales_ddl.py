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
    
    stmt = """create table store_sales
(
ss_sold_date_sk           integer                       ,
ss_sold_time_sk           integer                       ,
ss_item_sk                integer               not null,
ss_customer_sk            integer                       ,
ss_cdemo_sk               integer                       ,
ss_hdemo_sk               integer                       ,
ss_addr_sk                integer                       ,
ss_store_sk               integer                       ,
ss_promo_sk               integer                       ,
ss_ticket_number          integer               not null,
ss_quantity               integer                       ,
ss_wholesale_cost         decimal(7,2)                  ,
ss_list_price             decimal(7,2)                  ,
ss_sales_price            decimal(7,2)                  ,
ss_ext_discount_amt       decimal(7,2)                  ,
ss_ext_sales_price        decimal(7,2)                  ,
ss_ext_wholesale_cost     decimal(7,2)                  ,
ss_ext_list_price         decimal(7,2)                  ,
ss_ext_tax                decimal(7,2)                  ,
ss_coupon_amt             decimal(7,2)                  ,
ss_net_paid               decimal(7,2)                  ,
ss_net_paid_inc_tax       decimal(7,2)                  ,
ss_net_profit             decimal(7,2)                  ,
primary key (ss_item_sk, ss_ticket_number)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ hash2 partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    

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
    
    stmt = """create table web_sales
(
ws_sold_date_sk           integer                       ,
ws_sold_time_sk           integer                       ,
ws_ship_date_sk           integer                       ,
ws_item_sk                integer               not null,
ws_bill_customer_sk       integer                       ,
ws_bill_cdemo_sk          integer                       ,
ws_bill_hdemo_sk          integer                       ,
ws_bill_addr_sk           integer                       ,
ws_ship_customer_sk       integer                       ,
ws_ship_cdemo_sk          integer                       ,
ws_ship_hdemo_sk          integer                       ,
ws_ship_addr_sk           integer                       ,
ws_web_page_sk            integer                       ,
ws_web_site_sk            integer                       ,
ws_ship_mode_sk           integer                       ,
ws_warehouse_sk           integer                       ,
ws_promo_sk               integer                       ,
ws_order_number           integer               not null,
ws_quantity               integer                       ,
ws_wholesale_cost         decimal(7,2)                  ,
ws_list_price             decimal(7,2)                  ,
ws_sales_price            decimal(7,2)                  ,
ws_ext_discount_amt       decimal(7,2)                  ,
ws_ext_sales_price        decimal(7,2)                  ,
ws_ext_wholesale_cost     decimal(7,2)                  ,
ws_ext_list_price         decimal(7,2)                  ,
ws_ext_tax                decimal(7,2)                  ,
ws_coupon_amt             decimal(7,2)                  ,
ws_ext_ship_cost          decimal(7,2)                  ,
ws_net_paid               decimal(7,2)                  ,
ws_net_paid_inc_tax       decimal(7,2)                  ,
ws_net_paid_inc_ship      decimal(7,2)                  ,
ws_net_paid_inc_ship_tax  decimal(7,2)                  ,
ws_net_profit             decimal(7,2)                  ,
primary key (ws_item_sk, ws_order_number)
)"""
    if hpdci.tgtTR():
        stmt += """ salt using """ + defs.num_salt_partitions + """ partitions;"""
    else:
        stmt += """ hash2 partition attributes extent (256) maxextents 700;"""
    output = _dci.cmdexec(stmt)
    

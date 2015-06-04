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

# sortkey rewrite tables
# these are identical to those found in tpcds1x schema, but with different keys

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """create table sb_customer
(
c_customer_sk             integer               not null,
c_customer_id             char(16)              not null,
c_current_cdemo_sk        integer                       ,
c_current_hdemo_sk        integer                       ,
c_current_addr_sk         integer                       ,
c_first_shipto_date_sk    integer                       ,
c_first_sales_date_sk     integer                       ,
c_salutation              char(10)                      ,
c_first_name              char(20)              not null,
c_last_name               char(30)              not null,
c_preferred_cust_flag     char(1)                       ,
c_birth_day               integer                       ,
c_birth_month             integer                       ,
c_birth_year              integer                       ,
c_birth_country           varchar(20)                   ,
c_login                   char(13)                      ,
c_email_address           char(50)                      ,
c_last_review_date        char(10)                      ,
primary key (c_customer_sk, c_last_name, c_first_name)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = gvars.inscmd + """ sb_customer
(select * from """ + gvars.g_schema_tpcds1x + """.customer
where c_customer_sk is not null and
c_last_name is not null and
c_first_name is not null);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table sb_customer on every column,
(C_CUSTOMER_SK, C_LAST_NAME, C_BIRTH_DAY)  sample;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table sb_web_sales
(
WS_SOLD_DATE_SK                  INT DEFAULT NULL
, WS_SOLD_TIME_SK                  INT DEFAULT NULL
, WS_SHIP_DATE_SK                  INT DEFAULT NULL
, WS_ITEM_SK                       INT NO DEFAULT NOT NULL NOT DROPPABLE
, WS_BILL_CUSTOMER_SK              INT DEFAULT NULL
, WS_BILL_CDEMO_SK                 INT DEFAULT NULL
, WS_BILL_HDEMO_SK                 INT DEFAULT NULL
, WS_BILL_ADDR_SK                  INT DEFAULT NULL
, WS_SHIP_CUSTOMER_SK              INT DEFAULT NULL
, WS_SHIP_CDEMO_SK                 INT DEFAULT NULL
, WS_SHIP_HDEMO_SK                 INT DEFAULT NULL
, WS_SHIP_ADDR_SK                  INT DEFAULT NULL
, WS_WEB_PAGE_SK                   INT DEFAULT NULL
, WS_WEB_SITE_SK                   INT DEFAULT NULL
, WS_SHIP_MODE_SK                  INT DEFAULT NULL
, WS_WAREHOUSE_SK                  INT no default not null not droppable
, WS_PROMO_SK                      INT DEFAULT NULL
, WS_ORDER_NUMBER                  INT NO DEFAULT NOT NULL NOT DROPPABLE
, WS_QUANTITY                      INT no default not null not droppable
, WS_WHOLESALE_COST                DECIMAL(7, 2) DEFAULT NULL
, WS_LIST_PRICE                    DECIMAL(7, 2) no default not null
, WS_SALES_PRICE                   DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_DISCOUNT_AMT              DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_SALES_PRICE               DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_WHOLESALE_COST            DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_LIST_PRICE                DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_TAX                       DECIMAL(7, 2) DEFAULT NULL
, WS_COUPON_AMT                    DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_SHIP_COST                 DECIMAL(7, 2) DEFAULT NULL
, WS_NET_PAID                      DECIMAL(7, 2) no default not null
, WS_NET_PAID_INC_TAX              DECIMAL(7, 2) DEFAULT NULL
, WS_NET_PAID_INC_SHIP             DECIMAL(7, 2) DEFAULT NULL
, WS_NET_PAID_INC_SHIP_TAX         DECIMAL(7, 2) DEFAULT NULL
, WS_NET_PROFIT                    DECIMAL(7, 2) no default not null
)
store by (ws_order_number, ws_list_price, ws_net_paid, ws_net_profit);"""
    output = _dci.cmdexec(stmt)
    
    stmt = gvars.inscmd + """ sb_web_sales
(select * from """ + gvars.g_schema_tpcds1x + """.web_sales
where ws_order_number is not null and
WS_ITEM_SK is not null and
WS_WAREHOUSE_SK is not null and
WS_QUANTITY is not null and
ws_list_price is not null and
ws_net_paid is not null and
ws_net_profit is not null);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table sb_web_sales on every column sample;"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table sb_web_sales on (ws_quantity, ws_coupon_amt, ws_net_paid, ws_warehouse_sk) sample;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table sb_customer_address
(
ca_address_sk             integer               not null,
ca_address_id             char(16)              not null,
ca_street_number          char(10)                      ,
ca_street_name            varchar(60)                   ,
ca_street_type            char(15)                      ,
ca_suite_number           char(10)                      ,
ca_city                   varchar(60)           not null,
ca_county                 varchar(30)           not null,
ca_state                  char(2)               not null,
ca_zip                    char(10)              not null,
ca_country                varchar(20)                   ,
ca_gmt_offset             decimal(5,2)                  ,
ca_location_type          char(20)                      ,
primary key (ca_address_id, ca_city, ca_county,ca_state, ca_zip)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = gvars.inscmd + """ sb_customer_address
(select * from """ + gvars.g_schema_tpcds1x + """.customer_address
where ca_address_id is not null and
ca_city is not null and
ca_county is not null and
ca_state is not null and
ca_zip is not null);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table sb_customer_address on every column sample;"""
    output = _dci.cmdexec(stmt)
    
    # sortkey rewrite tables
    # these are identical to those found in tpcds1x schema, but with different keys
    
    stmt = """create table web_sales_clone
(
WS_SOLD_DATE_SK                  INT DEFAULT NULL
, WS_SOLD_TIME_SK                  INT DEFAULT NULL
, WS_SHIP_DATE_SK                  INT DEFAULT NULL
, WS_ITEM_SK                       INT NO DEFAULT NOT NULL NOT DROPPABLE
, WS_BILL_CUSTOMER_SK              INT DEFAULT NULL
, WS_BILL_CDEMO_SK                 INT DEFAULT NULL
, WS_BILL_HDEMO_SK                 INT DEFAULT NULL
, WS_BILL_ADDR_SK                  INT DEFAULT NULL
, WS_SHIP_CUSTOMER_SK              INT DEFAULT NULL
, WS_SHIP_CDEMO_SK                 INT DEFAULT NULL
, WS_SHIP_HDEMO_SK                 INT DEFAULT NULL
, WS_SHIP_ADDR_SK                  INT DEFAULT NULL
, WS_WEB_PAGE_SK                   INT DEFAULT NULL
, WS_WEB_SITE_SK                   INT DEFAULT NULL
, WS_SHIP_MODE_SK                  INT DEFAULT NULL
, WS_WAREHOUSE_SK                  INT no default not null not droppable
, WS_PROMO_SK                      INT DEFAULT NULL
, WS_ORDER_NUMBER                  INT NO DEFAULT NOT NULL NOT DROPPABLE
, WS_QUANTITY                      INT no default not null not droppable
, WS_WHOLESALE_COST                DECIMAL(7, 2) DEFAULT NULL
, WS_LIST_PRICE                    DECIMAL(7, 2) DEFAULT NULL
, WS_SALES_PRICE                   DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_DISCOUNT_AMT              DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_SALES_PRICE               DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_WHOLESALE_COST            DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_LIST_PRICE                DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_TAX                       DECIMAL(7, 2) DEFAULT NULL
, WS_COUPON_AMT                    DECIMAL(7, 2) DEFAULT NULL
, WS_EXT_SHIP_COST                 DECIMAL(7, 2) DEFAULT NULL
, WS_NET_PAID                      DECIMAL(7, 2) DEFAULT NULL
, WS_NET_PAID_INC_TAX              DECIMAL(7, 2) DEFAULT NULL
, WS_NET_PAID_INC_SHIP             DECIMAL(7, 2) DEFAULT NULL
, WS_NET_PAID_INC_SHIP_TAX         DECIMAL(7, 2) DEFAULT NULL
, WS_NET_PROFIT                    DECIMAL(7, 2) DEFAULT NULL
)
store by (ws_quantity, ws_warehouse_sk);"""
    output = _dci.cmdexec(stmt)
    
    stmt = gvars.inscmd + """ web_sales_clone
(select * from """ + gvars.g_schema_tpcds1x + """.web_sales where ws_warehouse_sk is not null and ws_quantity is not null);"""
    output = _dci.cmdexec(stmt)
    stmt = """update statistics for table web_sales_clone on every column, (ws_quantity, ws_warehouse_sk, ws_net_paid) sample;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table sb_store_returns_a
(
sr_returned_date_sk       integer                       ,
sr_return_time_sk         integer                       ,
sr_item_sk                integer               not null,
sr_customer_sk            integer                       ,
sr_cdemo_sk               integer                       ,
sr_hdemo_sk               integer                       ,
sr_addr_sk                integer                       ,
sr_store_sk               integer                       ,
sr_reason_sk              integer               not null,
sr_ticket_number          integer               not null,
sr_return_quantity        integer                       ,
sr_return_amt             decimal(7,2)                  ,
sr_return_tax             decimal(7,2)                  ,
sr_return_amt_inc_tax     decimal(7,2)                  ,
sr_fee                    decimal(7,2)                  ,
sr_return_ship_cost       decimal(7,2)                  ,
sr_refunded_cash          decimal(7,2)                  ,
sr_reversed_charge        decimal(7,2)                  ,
sr_store_credit           decimal(7,2)                  ,
sr_net_loss               decimal(7,2)                  ,
primary key (sr_ticket_number, sr_reason_sk, sr_item_sk)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = gvars.inscmd + """ sb_store_returns_a
(select * from """ + gvars.g_schema_tpcds1x + """.store_returns where sr_reason_sk is not NULL);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table sb_store_returns_a on every column sample;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table sb_store_returns_d
(
sr_returned_date_sk       integer                       ,
sr_return_time_sk         integer                       ,
sr_item_sk                integer               not null,
sr_customer_sk            integer                       ,
sr_cdemo_sk               integer                       ,
sr_hdemo_sk               integer                       ,
sr_addr_sk                integer                       ,
sr_store_sk               integer                       ,
sr_reason_sk              integer               not null,
sr_ticket_number          integer               not null,
sr_return_quantity        integer                       ,
sr_return_amt             decimal(7,2)                  ,
sr_return_tax             decimal(7,2)                  ,
sr_return_amt_inc_tax     decimal(7,2)                  ,
sr_fee                    decimal(7,2)                  ,
sr_return_ship_cost       decimal(7,2)                  ,
sr_refunded_cash          decimal(7,2)                  ,
sr_reversed_charge        decimal(7,2)                  ,
sr_store_credit           decimal(7,2)                  ,
sr_net_loss               decimal(7,2)                  ,
primary key (sr_ticket_number desc, sr_reason_sk desc, sr_item_sk)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = gvars.inscmd + """ sb_store_returns_d
(select * from """ + gvars.g_schema_tpcds1x + """.store_returns where sr_reason_sk is not NULL);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """update statistics for table sb_store_returns_d on every column sample;"""
    output = _dci.cmdexec(stmt)
    
    # stmt = """control query default query_cache '0';"""
    # output = _dci.cmdexec(stmt)
    # stmt = """control query default default_degree_of_parallelism '16';"""
    # output = _dci.cmdexec(stmt)
    
    # this CQD turns feature on, but does not force plans
    
    # stmt = """control query default comp_bool_86 'ON';"""
    # output = _dci.cmdexec(stmt)
    

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

    stmt = """set param ?curr_model 'T1';"""
    output = _dci.cmdexec(stmt)
    
def test001(desc="""TPCDS Baseline without multiblock sort"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    stmt = """set param ?q 1;"""
    output = _dci.cmdexec(stmt)
    
    # table/view customer_store_return doesn't exist on, remove test using that
    # object
    #set showshape on;
    #$SQL_prepared_msg
    #-- variant of TPCDS1
    
    #prepare xx from
    #select [first 100] c_customer_id
    # from $tpcds1x.customer_store_return ctr1
    #     ,$tpcds1x.store
    #     ,$tpcds1x.customer
    # where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
    #                          from $tpcds1x.customer_store_return ctr2)
    #      and s_store_sk = ctr1.ctr_store_sk
    #       and s_state = 'TN'
    #       and ctr1.ctr_customer_sk = c_customer_sk
    # order by c_customer_id;
    
    #set showshape off;
    
    #log $work_dir/dslog clear;
    #get statistics;
    #log off;
    
    ##sh export et=$(grep "Compile Time" $work_dir/dslog | awk ' { print $3 } ')
    #
    #execute save_plan;
    
    #$SQL_inserted_msg 1
    #insert into $my_schema.timetable (query,cardinal,T1_cost,T1_cmp_time)
    #(select ?q,cardinality,total_cost, time '$et' from table(explain(NULL,'XX'))
    #where operator = 'ROOT');
    
    #explain options 'f' xx;
    
    ##expectfile $test_dir/A100.RES ds1
    #execute xx;
    
    #log $work_dir/dslog clear;
    #get statistics;
    #log off;
    
    ##sh export et=$(grep "Elapsed Time" $work_dir/dslog | awk ' { print $3 } ')
    #
    #$SQL_updated_msg 1
    #update $my_schema.timetable set T1_time = time '$et'
    #where query = ?q;
    #==#endtestcase
    
    ##testcase TPCDS16X TPCDS Query 16 variant
    stmt = """set param ?q 16;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    stmt = """prepare xx from
select count(distinct cs_order_number)
,sum(cs_ext_ship_cost)
,sum(cs_net_profit)
from
catalog_sales cs1, date_dim, customer_address, call_center
where d_date between date '1998-07-30' and date '2008-07-30' + Interval '60' day
and cs1.cs_ship_date_sk = d_date_sk
and cs1.cs_ship_addr_sk = ca_address_sk
and ca_state < 'OK'
and cs1.cs_call_center_sk = cc_call_center_sk
and cc_county in
('Williamson County','Walker County ','Zieback County','Ziebach County','Ziebach County')
and exists
(select * from catalog_sales cs2
where cs1.cs_order_number = cs2.cs_order_number)
and not exists (select * from catalog_returns cr1
where cs1.cs_order_number = cr1.cr_order_number);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds16')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    ##endtestcase
    
    ##testcase TPCDS34 TPCDS Query 34
    stmt = """set param ?q 34;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPCDS34 rowcount = 467
    stmt = """prepare xx from
select [first 100]
c_last_name
,c_first_name
,c_salutation
,c_preferred_cust_flag
,ss_ticket_number
,cnt from
(select ss_ticket_number
,ss_customer_sk
,count(*) cnt
from """ + gvars.g_schema_tpcds1x + """.store_sales,
""" + gvars.g_schema_tpcds1x + """.date_dim,
""" + gvars.g_schema_tpcds1x + """.store,
""" + gvars.g_schema_tpcds1x + """.household_demographics
where ss_sold_date_sk = d_date_sk
and ss_store_sk = s_store_sk
and ss_hdemo_sk = hd_demo_sk
and (d_dom between 1 and 3 or d_dom between 25 and 28)
and (hd_buy_potential = '1001-5000' or
hd_buy_potential = '5001-10000')
and hd_vehicle_count > 0
and (case when hd_vehicle_count > 0
then hd_dep_count/ hd_vehicle_count
else null
end)  > 1.2
and d_year in (1998 ,1998 +1,1998 +2)
and s_county in ('Williamson County','Walker County',
'Ziebach County ','Ziebach County ',
'Williamson County','Walker County',
'Ziebach County ','Ziebach County ')
group by ss_ticket_number,ss_customer_sk) dn,
""" + gvars.g_schema_tpcds1x + """.customer
where ss_customer_sk = c_customer_sk
and cnt between 15 and 20
order by c_last_name,c_first_name,c_salutation,c_preferred_cust_flag desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds34')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    
    ##testcase TPCDS40 TPCDS Query 40
    #set showshape on;
    stmt = """set param ?q 40;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # TPCDS40 rowcount = 669
    stmt = """prepare xx from
select
w_state
,i_item_id
,sum(case when (cast(d_date as date) < date '1997-10-26')
then cs_sales_price - coalesce(cr_refunded_cash,0)
else 0 end) as sales_before
,sum(case when (cast(d_date as date) >= date '1997-10-26' )
then cs_sales_price - coalesce(cr_refunded_cash,0)
else 0 end) as sales_after
from
""" + gvars.g_schema_tpcds1x + """.catalog_sales left outer join """ + gvars.g_schema_tpcds1x + """.catalog_returns on
(cs_order_number = cr_order_number
and cs_item_sk = cr_item_sk)
,""" + gvars.g_schema_tpcds1x + """.warehouse
,""" + gvars.g_schema_tpcds1x + """.item
,""" + gvars.g_schema_tpcds1x + """.date_dim
where
i_current_price between 0.99 and 1.49
and i_item_sk          = cs_item_sk
and cs_warehouse_sk    = w_warehouse_sk
and cs_sold_date_sk    = d_date_sk
and d_date between date '1998-04-30' - interval '30' day
and date '1999-12-30' + interval '30' day
group by
w_state,i_item_id
order by i_item_id, w_state;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds40')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    ##endtestcase
    
    ##testcase TPCDS46x TPCDS Query 46 variant
    
    stmt = """set param ?q 46;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # variant of TPCDS46 38886 rows
    stmt = """prepare xx from
select  [first 100]
c_last_name
,c_first_name
,ca_city
,bought_city
,ss_ticket_number
,amt,profit
from
(select ss_ticket_number
,ss_customer_sk
,ca_city bought_city
,sum(ss_coupon_amt) amt
,sum(ss_net_profit) profit
from """ + gvars.g_schema_tpcds1x + """.store_sales,
""" + gvars.g_schema_tpcds1x + """.date_dim,store,
""" + gvars.g_schema_tpcds1x + """.household_demographics,
""" + gvars.g_schema_tpcds1x + """.customer_address
where ss_sold_date_sk = d_date_sk
and ss_store_sk = s_store_sk
and ss_hdemo_sk = hd_demo_sk
and ss_addr_sk = ca_address_sk
and d_dow in (6,0)
and d_year in (1998,1999+1,2000+2)
group by ss_ticket_number,ss_customer_sk,ss_addr_sk,ca_city) dn,
""" + gvars.g_schema_tpcds1x + """.customer,
""" + gvars.g_schema_tpcds1x + """.customer_address current_addr
where ss_customer_sk = c_customer_sk
and c_current_addr_sk = current_addr.ca_address_sk
and current_addr.ca_city <> bought_city
order by 1,2,4,6;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds46')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    ##endtestcase
    ##testcase TPCDS50x TPCDS Query 50 variant
    #set showshape on;
    stmt = """set param ?q 50;"""
    output = _dci.cmdexec(stmt)
    
    #set showshape on;
    # variant of TPCDS50 rowcount = 6
    stmt = """prepare xx from
select
s_store_name
,s_company_id
,s_street_number
,s_street_name
,s_street_type
,s_suite_number
,s_city
,s_county
,s_state
,s_zip
,sum(case when (sr_returned_date_sk - ss_sold_date_sk <= 30 ) then 1 else 0 end) ThirtyDays
,sum(case when (sr_returned_date_sk - ss_sold_date_sk > 30 ) and
(sr_returned_date_sk - ss_sold_date_sk <= 60) then 1 else 0 end) UnderSixtyDays
,sum(case when (sr_returned_date_sk - ss_sold_date_sk > 60 ) and
(sr_returned_date_sk - ss_sold_date_sk <= 90) then 1 else 0 end) UnderNinetyDays
,sum(case when (sr_returned_date_sk - ss_sold_date_sk > 90 ) and
(sr_returned_date_sk - ss_sold_date_sk <= 120) then 1 else 0 end) Under120Days
,sum(case when (sr_returned_date_sk - ss_sold_date_sk > 1200 )  then 1 else 0 end) Over120Days
from """ + gvars.g_schema_tpcds1x + """.store_sales
,""" + gvars.g_schema_tpcds1x + """.store_returns
,""" + gvars.g_schema_tpcds1x + """.store
,""" + gvars.g_schema_tpcds1x + """.date_dim d1
,""" + gvars.g_schema_tpcds1x + """.date_dim d2
where    

ss_ticket_number = sr_ticket_number
and ss_item_sk = sr_item_sk
and ss_sold_date_sk = d1.d_date_sk
and sr_returned_date_sk = d2.d_date_sk
and ss_customer_sk = sr_customer_sk
and ss_store_sk = s_store_sk
group by
s_store_name
,s_company_id
,s_street_number
,s_street_name
,s_street_type
,s_suite_number
,s_city
,s_county
,s_state
,s_zip
order by
s_store_name
,s_company_id
,s_street_number
,s_street_name
,s_street_type
,s_suite_number
,s_city
,s_county
,s_state
,s_zip ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    #set showshape off;
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into """ + defs.my_schema + """.timetable (query,cardinal,T1_cost,T1_cmp_time)
(select ?q,cardinality,total_cost, time '""" + defs.et + """' from table(explain(NULL,'XX'))
where operator = 'ROOT');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """explain options 'f' xx;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds50')
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Elapsed Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """update """ + defs.my_schema + """.timetable set T1_time = time '""" + defs.et + """'
where query = ?q;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    _testmgr.testcase_end(desc)


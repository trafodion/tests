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
    
def test001(desc="""TPCDS baseline queries"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    stmt = """set param ?q 3;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 3
    # rowcount = 6
    stmt = """prepare xx from
select  dt.d_year,
item.i_brand_id brand_id,
item.i_brand brand,
sum(ss_ext_sales_price) ext_price
from   date_dim dt,
store_sales, item
where dt.d_date_sk = store_sales.ss_sold_date_sk
and store_sales.ss_item_sk = item.i_item_sk
and item.i_manufact_id = 937
and dt.d_moy=11
group by dt.d_year, item.i_brand, item.i_brand_id
order by dt.d_year, ext_price desc, brand_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds3')
    
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    ##testcase O6 TPCDS Query 6
    stmt = """set param ?q 6;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 6
    # rowcount = 44
    stmt = """prepare xx from
select  a.ca_state state, count(*) cnt
from customer_address a
,customer c
,store_sales s
,date_dim d
,item i
where       a.ca_address_sk = c.c_current_addr_sk
and c.c_customer_sk = s.ss_customer_sk
and s.ss_sold_date_sk = d.d_date_sk
and s.ss_item_sk = i.i_item_sk
and d.d_month_seq =
(select distinct (d_month_seq)
from date_dim
where d_year = 2001
and d_moy = 2 )
and i.i_current_price > 1.2 *
(select avg(j.i_current_price)
from item j
where j.i_category = i.i_category)
group by a.ca_state
having count(*) >= 10
order by 2,1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds6')
    
    ##expectstat $test_dir/A100.$MODEL ex6a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 11;"""
    output = _dci.cmdexec(stmt)
    
    # query 11
    # rowcount = 83
    stmt = """prepare xx from
select  t_s_secyear.customer_id, t_s_secyear.customer_first_name, t_s_secyear.customer_last_name
,t_s_secyear.c_preferred_cust_flag,t_s_secyear.c_birth_country,t_s_secyear.c_login
from (
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ss_ext_list_price-ss_ext_discount_amt) year_total
,'s' sale_type
from customer
,store_sales
,date_dim
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,d_year
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
union all
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ws_ext_list_price-ws_ext_discount_amt) year_total
,'w' sale_type
from customer
,web_sales
,date_dim
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
) as t_s_firstyear
,(
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ss_ext_list_price-ss_ext_discount_amt) year_total
,'s' sale_type
from customer
,store_sales
,date_dim
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,d_year
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
union all
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ws_ext_list_price-ws_ext_discount_amt) year_total
,'w' sale_type
from customer
,web_sales
,date_dim
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
) as t_s_secyear
,(
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ss_ext_list_price-ss_ext_discount_amt) year_total
,'s' sale_type
from customer
,store_sales
,date_dim
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,d_year
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
union all
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ws_ext_list_price-ws_ext_discount_amt) year_total
,'w' sale_type
from customer
,web_sales
,date_dim
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
) as t_w_firstyear
,(
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ss_ext_list_price-ss_ext_discount_amt) year_total
,'s' sale_type
from customer
,store_sales
,date_dim
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,d_year
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
union all
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year dyear
,sum(ws_ext_list_price-ws_ext_discount_amt) year_total
,'w' sale_type
from customer
,web_sales
,date_dim
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
group by c_customer_id
,c_first_name
,c_last_name
,c_preferred_cust_flag
,c_birth_country
,c_login
,c_email_address
,d_year
) as t_w_secyear
where t_s_secyear.customer_id = t_s_firstyear.customer_id
and t_s_firstyear.customer_id = t_w_secyear.customer_id
and t_s_firstyear.customer_id = t_w_firstyear.customer_id
and t_s_firstyear.sale_type = 's'
and t_w_firstyear.sale_type = 'w'
and t_s_secyear.sale_type = 's'
and t_w_secyear.sale_type = 'w'
and t_s_firstyear.dyear = 1999
and t_s_secyear.dyear = 1999+1
and t_w_firstyear.dyear = 1999
and t_w_secyear.dyear = 1999+1
and t_s_firstyear.year_total > 0
and t_w_firstyear.year_total > 0
and case when t_w_firstyear.year_total > 0
then t_w_secyear.year_total / t_w_firstyear.year_total
else null end
> case when t_s_firstyear.year_total > 0
then t_s_secyear.year_total / t_s_firstyear.year_total
else null end
order by t_s_secyear.customer_id, t_s_secyear.customer_first_name,
t_s_secyear.customer_last_name,
t_s_secyear.c_preferred_cust_flag,t_s_secyear.c_birth_country,
t_s_secyear.c_login
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds11')
    ##expectstat $test_dir/A100.$MODEL ex11a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 13;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 13
    # rowcount = 1
    stmt = """prepare xx from
select  avg(ss_quantity), avg(ss_ext_sales_price), avg(ss_ext_wholesale_cost), sum(ss_ext_wholesale_cost)
from store_sales, store, customer_demographics, household_demographics, customer_address, date_dim
where s_store_sk = ss_store_sk
and  ss_sold_date_sk = d_date_sk and d_year = 2001
and
(
(
ss_hdemo_sk=hd_demo_sk
and
cd_demo_sk = ss_cdemo_sk
and
cd_marital_status = 'S'
and
cd_education_status = '2 yr Degree'
and
ss_sales_price between 100.00 and 150.00
and
hd_dep_count = 3
)
or
(
ss_hdemo_sk=hd_demo_sk
and
cd_demo_sk = ss_cdemo_sk
and
cd_marital_status = 'W'
and
cd_education_status = 'College'
and
ss_sales_price between 50.00 and 100.00
and
hd_dep_count = 1
)
or
(
ss_hdemo_sk=hd_demo_sk
and
cd_demo_sk = ss_cdemo_sk
and
cd_marital_status = 'D'
and
cd_education_status = 'Advanced Degree'
and
ss_sales_price between 150.00 and 200.00
and
hd_dep_count = 1
)
)
and
(
(
ss_addr_sk = ca_address_sk
and
ca_country = 'United States'
and
ca_state in ('WV', 'VT', 'IA')
and ss_net_profit between 100 and 200
)
or
(ss_addr_sk = ca_address_sk
and
ca_country = 'United States'
and
ca_state in ('NC', 'IA', 'OK')
and ss_net_profit between 150 and 300
)
or
(ss_addr_sk = ca_address_sk
and
ca_country = 'United States'
and
ca_state in ('SD', 'ND', 'OK')
and ss_net_profit between 50 and 250
)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds13')
    
    ##expectstat $test_dir/A100.$MODEL ex13a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 19;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 19
    # rowcount = 98
    stmt = """prepare xx from
select  i_brand_id brand_id, i_brand brand, i_manufact_id, i_manufact,
sum(ss_ext_sales_price) ext_price
from date_dim, store_sales, item,customer,customer_address,store
where d_date_sk = ss_sold_date_sk
and ss_item_sk = i_item_sk
and i_manager_id=36
and d_moy=11
and d_year=2001
and ss_customer_sk = c_customer_sk
and c_current_addr_sk = ca_address_sk
and substr(ca_zip,1,5) <> substr(s_zip,1,5)
and ss_store_sk = s_store_sk
group by i_brand, i_brand_id,i_manufact_id, i_manufact
order by ext_price desc, i_brand, i_brand_id,i_manufact_id, i_manufact
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds19')
    ##expectstat $test_dir/A100.$MODEL ex19a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 22;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 22
    # rowcount = 26
    stmt = """prepare xx from
select
c_last_name,c_first_name,ss_ticket_number,cnt
from
(select ss_ticket_number
,ss_customer_sk
,count(*) cnt
from store_sales,date_dim,store,household_demographics
where store_sales.ss_sold_date_sk = date_dim.d_date_sk
and store_sales.ss_store_sk = store.s_store_sk
and store_sales.ss_hdemo_sk = household_demographics.hd_demo_sk
and date_dim.d_dom between 1 and 5
and date_dim.d_year in (1999,1999+1,1999+2)
and store.s_city in ('Fairview','Midway','Midway',
'Fairview','Fairview','Fairview')
and (household_demographics.hd_buy_potential like '1001-5000%' or
household_demographics.hd_buy_potential like '5001-10000%')
group by ss_ticket_number,ss_customer_sk) mp,customer
where ss_customer_sk = c_customer_sk
and cnt between 1 and 5
order by 4,1,3 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds22')
    
    ##expectstat $test_dir/A100.$MODEL ex22a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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

    stmt = """set param ?q 25;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 25
    # rowcount = 1
    stmt = """prepare xx from
select
i_item_id
,i_item_desc
,s_store_id
,s_store_name
,sum(ss_net_profit) as store_sales_profit
,sum(sr_net_loss) as store_returns_loss
,sum(cs_net_profit) as catalog_sales_profit
from
store_sales
,store_returns
,catalog_sales
,date_dim d1
,date_dim d2
,date_dim d3
,store
,item
where
d1.d_moy = 4
and d1.d_year = 2001
and d1.d_date_sk = ss_sold_date_sk
and i_item_sk = ss_item_sk
and s_store_sk = ss_store_sk
and ss_customer_sk = sr_customer_sk
and ss_item_sk = sr_item_sk
and ss_ticket_number = sr_ticket_number
and sr_returned_date_sk = d2.d_date_sk
and d2.d_moy               between 4 and  4 +6
and d2.d_year              = 2001
and sr_customer_sk = cs_bill_customer_sk
and sr_item_sk = cs_item_sk
and cs_sold_date_sk = d3.d_date_sk
and d3.d_moy               between 4 and   4 +6
and d3.d_year              = 2001
group by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
order by
i_item_id
,i_item_desc
,s_store_id
,s_store_name
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds25')
    
    ##expectstat $test_dir/A100.$MODEL ex25a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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

    stmt = """set param ?q 30;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 30
    # rowcount = 109
    stmt = """prepare xx from
select  c_customer_id,c_salutation,c_first_name
,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year
,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
from (select wr_returning_customer_sk as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) as ctr_total_return
from web_returns
,date_dim
,customer_address
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk
,ca_state) as ctr1
,customer_address
,customer
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from (select wr_returning_customer_sk
as ctr_customer_sk
,ca_state as ctr_state,
sum(wr_return_amt) as ctr_total_return
from web_returns
,date_dim
,customer_address
where wr_returned_date_sk = d_date_sk
and d_year =2002
and wr_returning_addr_sk = ca_address_sk
group by wr_returning_customer_sk
,ca_state) as ctr2
where ctr1.ctr_state = ctr2.ctr_state)
and ca_address_sk = c_current_addr_sk
and ca_state = 'IL'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id,c_salutation,c_first_name
,c_last_name,c_preferred_cust_flag
,c_birth_day,c_birth_month,c_birth_year
,c_birth_country,c_login,c_email_address
,c_last_review_date,ctr_total_return
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds30')
    
    ##expectstat $test_dir/A100.$MODEL ex30a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 31;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 31
    # rowcount = 47
    stmt = """prepare xx from
select
ss1.ca_county
,ss1.d_year
,ws2.web_sales/ws1.web_sales web_q1_q2_increase
,ss2.store_sales/ss1.store_sales store_q1_q2_increase
,ws3.web_sales/ws2.web_sales web_q2_q3_increase
,ss3.store_sales/ss2.store_sales store_q2_q3_increase
from
(select ca_county,d_qoy, d_year,
sum(ss_ext_sales_price) as store_sales
from store_sales,date_dim,customer_address
where ss_sold_date_sk = d_date_sk
and ss_addr_sk=ca_address_sk
group by ca_county,d_qoy, d_year) as ss1
,(select ca_county,d_qoy, d_year,
sum(ss_ext_sales_price) as store_sales
from store_sales,date_dim,customer_address
where ss_sold_date_sk = d_date_sk
and ss_addr_sk=ca_address_sk
group by ca_county,d_qoy, d_year) as ss2
,(select ca_county,d_qoy, d_year,
sum(ss_ext_sales_price) as store_sales
from store_sales,date_dim,customer_address
where ss_sold_date_sk = d_date_sk
and ss_addr_sk=ca_address_sk
group by ca_county,d_qoy, d_year) as ss3
,(select ca_county,d_qoy, d_year,
sum(ws_ext_sales_price) as web_sales
from web_sales,date_dim,customer_address
where ws_sold_date_sk = d_date_sk
and ws_bill_addr_sk=ca_address_sk
group by ca_county,d_qoy, d_year) as ws1
,(select ca_county,d_qoy, d_year,
sum(ws_ext_sales_price) as web_sales
from web_sales,date_dim,customer_address
where ws_sold_date_sk = d_date_sk
and ws_bill_addr_sk=ca_address_sk
group by ca_county,d_qoy, d_year) as ws2
,(select ca_county,d_qoy, d_year,
sum(ws_ext_sales_price) as web_sales
from web_sales,date_dim,customer_address
where ws_sold_date_sk = d_date_sk
and ws_bill_addr_sk=ca_address_sk
group by ca_county,d_qoy, d_year) as ws3
where
ss1.d_qoy = 1
and ss1.d_year = 2000
and ss1.ca_county = ss2.ca_county
and ss2.d_qoy = 2
and ss2.d_year = 2000
and ss2.ca_county = ss3.ca_county
and ss3.d_qoy = 3
and ss3.d_year = 2000
and ss1.ca_county = ws1.ca_county
and ws1.d_qoy = 1
and ws1.d_year = 2000
and ws1.ca_county = ws2.ca_county
and ws2.d_qoy = 2
and ws2.d_year = 2000
and ws1.ca_county = ws3.ca_county
and ws3.d_qoy = 3
and ws3.d_year =2000
and case when ws1.web_sales > 0
then ws2.web_sales/ws1.web_sales
else null end
> case when ss1.store_sales > 0
then ss2.store_sales/ss1.store_sales
else null end
and case when ws2.web_sales > 0
then ws3.web_sales/ws2.web_sales
else null end
> case when ss2.store_sales > 0
then ss3.store_sales/ss2.store_sales
else null end
order by ss1.ca_county;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds31')
    
    ##expectstat $test_dir/A100.$MODEL ex31a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 73;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 73
    # rowcount = 5
    stmt = """prepare xx from
select  c_last_name
,c_first_name
,c_salutation
,c_preferred_cust_flag
,ss_ticket_number
,cnt from
(select ss_ticket_number
,ss_customer_sk
,count(*) cnt
from store_sales,date_dim,store,household_demographics
where store_sales.ss_sold_date_sk = date_dim.d_date_sk
and store_sales.ss_store_sk = store.s_store_sk
and store_sales.ss_hdemo_sk = household_demographics.hd_demo_sk
and date_dim.d_dom between 1 and 2
and (household_demographics.hd_buy_potential = '1001-5000' or
household_demographics.hd_buy_potential = '5001-10000')
and household_demographics.hd_vehicle_count > 0
and case when household_demographics.hd_vehicle_count > 0
then
household_demographics.hd_dep_count/
household_demographics.hd_vehicle_count
else null end > 1
and date_dim.d_year in (1999,1999+1,1999+2)
and store.s_county in ('Williamson County',
'Williamson County',
'Williamson County',
'Williamson County')
group by ss_ticket_number,ss_customer_sk) dj,customer
where ss_customer_sk = c_customer_sk
and cnt between 1 and 5
order by 5,1,4 desc;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds73')
    
    ##expectstat $test_dir/A100.$MODEL ex73a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 74;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 74
    # rowcount = 89
    stmt = """prepare xx from
select
t_s_secyear.customer_id,
t_s_secyear.customer_first_name,
t_s_secyear.customer_last_name
from (
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,d_year as "year"
,sum(ss_net_paid) year_total
,'s' sale_type
from customer
,store_sales
,date_dim
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
and d_year in (1999,1999+1)
group by c_customer_id
,c_first_name
,c_last_name
,d_year
union all
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,d_year as "year"
,sum(ws_net_paid) year_total
,'w' sale_type
from customer
,web_sales
,date_dim
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
and d_year in (1999,1999+1)
group by c_customer_id
,c_first_name
,c_last_name
,d_year
) as t_s_firstyear
,(
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,d_year as "year"
,sum(ss_net_paid) year_total
,'s' sale_type
from customer
,store_sales
,date_dim
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
and d_year in (1999,1999+1)
group by c_customer_id
,c_first_name
,c_last_name
,d_year
union all
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,d_year as "year"
,sum(ws_net_paid) year_total
,'w' sale_type
from customer
,web_sales
,date_dim
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
and d_year in (1999,1999+1)
group by c_customer_id
,c_first_name
,c_last_name
,d_year
) as t_s_secyear
,(
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,d_year as "year"
,sum(ss_net_paid) year_total
,'s' sale_type
from customer
,store_sales
,date_dim
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
and d_year in (1999,1999+1)
group by c_customer_id
,c_first_name
,c_last_name
,d_year
union all
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,d_year as "year"
,sum(ws_net_paid) year_total
,'w' sale_type
from customer
,web_sales
,date_dim
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
and d_year in (1999,1999+1)
group by c_customer_id
,c_first_name
,c_last_name
,d_year
) as t_w_firstyear
,(
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,d_year as "year"
,sum(ss_net_paid) year_total
,'s' sale_type
from customer
,store_sales
,date_dim
where c_customer_sk = ss_customer_sk
and ss_sold_date_sk = d_date_sk
and d_year in (1999,1999+1)
group by c_customer_id
,c_first_name
,c_last_name
,d_year
union all
select c_customer_id customer_id
,c_first_name customer_first_name
,c_last_name customer_last_name
,d_year as "year"
,sum(ws_net_paid) year_total
,'w' sale_type
from customer
,web_sales
,date_dim
where c_customer_sk = ws_bill_customer_sk
and ws_sold_date_sk = d_date_sk
and d_year in (1999,1999+1)
group by c_customer_id
,c_first_name
,c_last_name
,d_year
) as t_w_secyear
where t_s_secyear.customer_id = t_s_firstyear.customer_id
and t_s_firstyear.customer_id = t_w_secyear.customer_id
and t_s_firstyear.customer_id = t_w_firstyear.customer_id
and t_s_firstyear.sale_type = 's'
and t_w_firstyear.sale_type = 'w'
and t_s_secyear.sale_type = 's'
and t_w_secyear.sale_type = 'w'
and t_s_firstyear."year" = 1999
and t_s_secyear."year" = 1999+1
and t_w_firstyear."year" = 1999
and t_w_secyear."year" = 1999+1
and t_s_firstyear.year_total > 0
and t_w_firstyear.year_total > 0
and case when t_w_firstyear.year_total > 0
then t_w_secyear.year_total /
t_w_firstyear.year_total
else null end
> case when t_s_firstyear.year_total > 0
then t_s_secyear.year_total /
t_s_firstyear.year_total
else null end
order by 1
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds74')
    
    ##expectstat $test_dir/A100.$MODEL ex74a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 75;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 75
    # rowcount = 2
    stmt = """prepare xx from
select  i_item_id
,i_item_desc
,i_current_price
from item, inventory, date_dim
where i_current_price between 38 and 38+30
and inv_item_sk = i_item_sk
and d_date_sk=inv_date_sk
and d_date between cast('2001-01-18' as date) and (cast('2001-01-18' as date) +  60)
and i_manufact_id in (556,419,338,362)
and inv_quantity_on_hand between 100 and 500
group by i_item_id,i_item_desc,i_current_price
order by i_item_id;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds75')
    
    ##expectstat $test_dir/A100.$MODEL ex75a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 84;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 84
    # rowcount = 15
    stmt = """prepare xx from
select  c_customer_id as customer_id
,c_last_name || ', ' || c_first_name as customername
from customer
,customer_address
,customer_demographics
,household_demographics
,income_band
,store_returns
where ca_city          =  'Centerville'
and c_current_addr_sk = ca_address_sk
and ib_lower_bound   >=  68645
and ib_upper_bound   <=  68645 + 50000
and ib_income_band_sk = hd_income_band_sk
and cd_demo_sk = c_current_cdemo_sk
and hd_demo_sk = c_current_hdemo_sk
and sr_cdemo_sk = cd_demo_sk
order by c_customer_id
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds84')
    
    ##expectstat $test_dir/A100.$MODEL ex84a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 85;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 85
    # rowcount = 2
    stmt = """prepare xx from
select  substr(r_reason_desc,1,20)
,avg(ws_quantity)
,avg(wr_refunded_cash)
,avg(wr_fee)
from web_sales, web_returns, web_page, customer_demographics cd1,
customer_demographics cd2, customer_address, date_dim, reason
where ws_web_page_sk = wp_web_page_sk
and ws_item_sk = wr_item_sk
and ws_order_number = wr_order_number
and ws_sold_date_sk = d_date_sk and d_year = 2000
and cd1.cd_demo_sk = wr_refunded_cdemo_sk
and cd2.cd_demo_sk = wr_returning_cdemo_sk
and ca_address_sk = wr_refunded_addr_sk
and r_reason_sk = wr_reason_sk
and
(
(
cd1.cd_marital_status = 'U'
and
cd1.cd_marital_status = cd2.cd_marital_status
and
cd1.cd_education_status = '2 yr Degree'
and
cd1.cd_education_status = cd2.cd_education_status
and
ws_sales_price between 100.00 and 150.00
)
or
(
cd1.cd_marital_status = 'S'
and
cd1.cd_marital_status = cd2.cd_marital_status
and
cd1.cd_education_status = 'Advanced Degree'
and
cd1.cd_education_status = cd2.cd_education_status
and
ws_sales_price between 50.00 and 100.00
)
or
(
cd1.cd_marital_status = 'M'
and
cd1.cd_marital_status = cd2.cd_marital_status
and
cd1.cd_education_status = 'College'
and
cd1.cd_education_status = cd2.cd_education_status
and
ws_sales_price between 150.00 and 200.00
)
)
and
(
(
ca_country = 'United States'
and
ca_state in ('MS', 'ND', 'CA')
and ws_net_profit between 100 and 200
)
or
(
ca_country = 'United States'
and
ca_state in ('VA', 'NY', 'SD')
and ws_net_profit between 150 and 300
)
or
(
ca_country = 'United States'
and
ca_state in ('VA', 'OH', 'GA')
and ws_net_profit between 50 and 250
)
)
group by r_reason_desc
order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds85')
    
    ##expectstat $test_dir/A100.$MODEL ex85a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 88;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 88
    # rowcount = 1
    stmt = """prepare xx from
select
*
from
(select count(*) h8_30_to_9
from store_sales, household_demographics , time_dim, store
where ss_sold_time_sk = time_dim.t_time_sk
and ss_hdemo_sk = household_demographics.hd_demo_sk
and ss_store_sk = s_store_sk
and time_dim.t_hour = 8
and time_dim.t_minute >= 30
and ((household_demographics.hd_dep_count = 2
and household_demographics.hd_vehicle_count<=2+2) or
(household_demographics.hd_dep_count = 1
and household_demographics.hd_vehicle_count<=1+2) or
(household_demographics.hd_dep_count = 0
and household_demographics.hd_vehicle_count<=0+2))
and store.s_store_name = 'ese') s1,
(select count(*) h9_to_9_30
from store_sales, household_demographics , time_dim, store
where ss_sold_time_sk = time_dim.t_time_sk
and ss_hdemo_sk = household_demographics.hd_demo_sk
and ss_store_sk = s_store_sk
and time_dim.t_hour = 9
and time_dim.t_minute < 30
and ((household_demographics.hd_dep_count = 2
and household_demographics.hd_vehicle_count<=2+2) or
(household_demographics.hd_dep_count = 1
and household_demographics.hd_vehicle_count<=1+2) or
(household_demographics.hd_dep_count = 0
and household_demographics.hd_vehicle_count<=0+2))
and store.s_store_name = 'ese') s2,
(select count(*) h9_30_to_10
from store_sales, household_demographics , time_dim, store
where ss_sold_time_sk = time_dim.t_time_sk
and ss_hdemo_sk = household_demographics.hd_demo_sk
and ss_store_sk = s_store_sk
and time_dim.t_hour = 9
and time_dim.t_minute >= 30
and ((household_demographics.hd_dep_count = 2
and household_demographics.hd_vehicle_count<=2+2) or
(household_demographics.hd_dep_count = 1
and household_demographics.hd_vehicle_count<=1+2) or
(household_demographics.hd_dep_count = 0
and household_demographics.hd_vehicle_count<=0+2))
and store.s_store_name = 'ese') s3,
(select count(*) h10_to_10_30
from store_sales, household_demographics , time_dim, store
where ss_sold_time_sk = time_dim.t_time_sk
and ss_hdemo_sk = household_demographics.hd_demo_sk
and ss_store_sk = s_store_sk
and time_dim.t_hour = 10
and time_dim.t_minute < 30
and ((household_demographics.hd_dep_count = 2
and household_demographics.hd_vehicle_count<=2+2) or
(household_demographics.hd_dep_count = 1
and household_demographics.hd_vehicle_count<=1+2) or
(household_demographics.hd_dep_count = 0
and household_demographics.hd_vehicle_count<=0+2))
and store.s_store_name = 'ese') s4,
(select count(*) h10_30_to_11
from store_sales, household_demographics , time_dim, store
where ss_sold_time_sk = time_dim.t_time_sk
and ss_hdemo_sk = household_demographics.hd_demo_sk
and ss_store_sk = s_store_sk
and time_dim.t_hour = 10
and time_dim.t_minute >= 30
and ((household_demographics.hd_dep_count = 2
and household_demographics.hd_vehicle_count<=2+2) or
(household_demographics.hd_dep_count = 1
and household_demographics.hd_vehicle_count<=1+2) or
(household_demographics.hd_dep_count = 0 and household_demographics.hd_vehicle_count<=0+2))
and store.s_store_name = 'ese') s5,
(select count(*) h11_to_11_30
from store_sales, household_demographics , time_dim, store
where ss_sold_time_sk = time_dim.t_time_sk
and ss_hdemo_sk = household_demographics.hd_demo_sk
and ss_store_sk = s_store_sk
and time_dim.t_hour = 11
and time_dim.t_minute < 30
and ((household_demographics.hd_dep_count = 2
and household_demographics.hd_vehicle_count<=2+2) or
(household_demographics.hd_dep_count = 1
and household_demographics.hd_vehicle_count<=1+2) or
(household_demographics.hd_dep_count = 0
and household_demographics.hd_vehicle_count<=0+2))
and store.s_store_name = 'ese') s6,
(select count(*) h11_30_to_12
from store_sales, household_demographics , time_dim, store
where ss_sold_time_sk = time_dim.t_time_sk
and ss_hdemo_sk = household_demographics.hd_demo_sk
and ss_store_sk = s_store_sk
and time_dim.t_hour = 11
and time_dim.t_minute >= 30
and ((household_demographics.hd_dep_count = 2
and household_demographics.hd_vehicle_count<=2+2) or
(household_demographics.hd_dep_count = 1
and household_demographics.hd_vehicle_count<=1+2) or
(household_demographics.hd_dep_count = 0
and household_demographics.hd_vehicle_count<=0+2))
and store.s_store_name = 'ese') s7,
(select count(*) h12_to_12_30
from store_sales, household_demographics , time_dim, store
where ss_sold_time_sk = time_dim.t_time_sk
and ss_hdemo_sk = household_demographics.hd_demo_sk
and ss_store_sk = s_store_sk
and time_dim.t_hour = 12
and time_dim.t_minute < 30
and ((household_demographics.hd_dep_count = 2
and household_demographics.hd_vehicle_count<=2+2) or
(household_demographics.hd_dep_count = 1
and household_demographics.hd_vehicle_count<=1+2) or
(household_demographics.hd_dep_count = 0
and household_demographics.hd_vehicle_count<=0+2))
and store.s_store_name = 'ese') s8;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds88')
    
    ##expectstat $test_dir/A100.$MODEL ex88a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 90;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 90
    # rowcount = 1
    stmt = """prepare xx from
select  amc/pmc am_pm_ratio
from ( select count(*) amc
from web_sales, household_demographics , time_dim, web_page
where ws_sold_time_sk = time_dim.t_time_sk
and ws_ship_hdemo_sk = household_demographics.hd_demo_sk
and ws_web_page_sk = web_page.wp_web_page_sk
and time_dim.t_hour between 10 and 10+1
and household_demographics.hd_dep_count = 3
and web_page.wp_char_count between 5000 and 5200) "at",
( select count(*) pmc
from web_sales, household_demographics , time_dim, web_page
where ws_sold_time_sk = time_dim.t_time_sk
and ws_ship_hdemo_sk = household_demographics.hd_demo_sk
and ws_web_page_sk = web_page.wp_web_page_sk
and time_dim.t_hour between 19 and 19+1
and household_demographics.hd_dep_count = 3
and web_page.wp_char_count between 5000 and 5200) pt;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds90')
    
    ##expectstat $test_dir/A100.$MODEL ex90a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 93;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 93
    # rowcount = 1
    stmt = """prepare xx from
select
sum(ss_ext_discount_amt)  as "Excess Discount Amount"
from
store_sales
,item
,date_dim
where
i_manufact_id = 859
and i_item_sk = ss_item_sk
and d_date between cast('2002-08-20' as date) and
(cast('2002-08-20' as date) + 90 )
and d_date_sk = ss_sold_date_sk
and ss_ext_discount_amt
> (
SELECT
1.3 * avg(ss_ext_discount_amt)
FROM
store_sales
,date_dim
WHERE
ss_item_sk = i_item_sk
and d_date between cast('2002-08-20' as date) and
(cast('2002-08-20' as date) + 30 )
and d_date_sk = ss_sold_date_sk
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds93')
    
    ##expectstat $test_dir/A100.$MODEL ex93a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 96;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 96
    # rowcount = 1
    stmt = """prepare xx from
select   count(*)
from store_sales
,household_demographics
,time_dim, store
where ss_sold_time_sk = time_dim.t_time_sk
and ss_hdemo_sk = household_demographics.hd_demo_sk
and ss_store_sk = s_store_sk
and time_dim.t_hour = 16
and time_dim.t_minute >= 30
and household_demographics.hd_dep_count = 3
and store.s_store_name = 'ese';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds96')
    
    ##expectstat $test_dir/A100.$MODEL ex96a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 97;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 97
    # rowcount = 1
    stmt = """prepare xx from
select  promotions,total,promotions/total*100
from
(select count(DISTINCT ws_item_sk) promotions
from  web_sales
,warehouse
,promotion
,date_dim
,customer
,customer_address
,item
where ws_sold_date_sk = d_date_sk
and   ws_warehouse_sk = w_warehouse_sk
and   ws_promo_sk = p_promo_sk
and   ws_ship_customer_sk= c_customer_sk
and   ca_address_sk = c_current_addr_sk
and   ws_item_sk = i_item_sk
and   ca_gmt_offset = -6
and   i_category = 'Home'
and   (p_channel_dmail = 'Y' or p_channel_email = 'Y' or p_channel_tv = 'Y')
and   d_year = 1999
and   d_moy  = 12) promotional_sale,
(select count(DISTINCT ws_item_sk) total
from  web_sales
,warehouse
,date_dim
,customer
,customer_address
,item
where ws_sold_date_sk = d_date_sk
and   ws_warehouse_sk = w_warehouse_sk
and   ws_ship_customer_sk= c_customer_sk
and   ca_address_sk = c_current_addr_sk
and   ws_item_sk = i_item_sk
and   ca_gmt_offset = -6
and   i_category = 'Home'
and   d_year = 1999
and   d_moy  = 12) all_sales
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds97')
    
    ##expectstat $test_dir/A100.$MODEL ex97a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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
    
    stmt = """set param ?q 99;"""
    output = _dci.cmdexec(stmt)
    
    # Stream 0, Query 99
    # rowcount = 90
    stmt = """prepare xx from
select
substr(w_warehouse_name,1,20)
,sm_type
,cc_name
,sum(case when (cs_ship_date_sk - cs_sold_date_sk <= 30 ) then 1 else 0 end)  as "30 days"
,sum(case when (cs_ship_date_sk - cs_sold_date_sk > 30) and
(cs_ship_date_sk - cs_sold_date_sk <= 60) then 1 else 0 end )  as "31-60 days"
,sum(case when (cs_ship_date_sk - cs_sold_date_sk > 60) and
(cs_ship_date_sk - cs_sold_date_sk <= 90) then 1 else 0 end)  as "61-90 days"
,sum(case when (cs_ship_date_sk - cs_sold_date_sk > 90) and
(cs_ship_date_sk - cs_sold_date_sk <= 120) then 1 else 0 end)  as "91-120 days"
,sum(case when (cs_ship_date_sk - cs_sold_date_sk  > 120) then 1 else 0 end)  as ">120 days"
from
catalog_sales
,warehouse
,ship_mode
,call_center
,date_dim
where
extract (year from d_date) = 2002
and cs_ship_date_sk   = d_date_sk
and cs_warehouse_sk   = w_warehouse_sk
and cs_ship_mode_sk   = sm_ship_mode_sk
and cs_call_center_sk = cc_call_center_sk
group by
1
,sm_type
,cc_name
order by 1,2,3
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_prepared_msg(output)
    
    stmt = """log """ + defs.work_dir + """/dslog clear;"""
    output = _dci.cmdexec(stmt)
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    stmt = """log off;"""
    output = _dci.cmdexec(stmt)
    
    defs.et = _testmgr.shell_call("""grep "Compile Time" """ + defs.work_dir + """/dslog | awk ' { print $3 } '""").strip()
    
    stmt = """execute save_plan;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """explain options 'f' xx;"""
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
    _dci.expect_file(output, defs.test_dir + """/A100.RES""", 'ds99')
    
    ##expectstat $test_dir/A100.$MODEL ex99a
    stmt = """get statistics;"""
    output = _dci.cmdexec(stmt)
    
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


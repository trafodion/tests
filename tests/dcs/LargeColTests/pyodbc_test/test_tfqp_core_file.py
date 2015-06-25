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


#!/bin/env python
# -*- coding:utf-8 -*-

'''
    #FileName: __file__
    #Description: Purposed to do big column size test.
    #Author: 
    #CreatedTime: 2015/04
    #LastModifiedTime: 2015/04
    #Version: Undefined
    #Copy Right (c) reserved
'''

import os
import sys
import re
import unittest
import ConfigParser
import pypyodbc
import datetime
import inspect
import logging
import time

__prefixName = "MYSQL"

def _createLogFile():
    scriptName = str(__file__).split('/')[-1].split('.')[0]
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    logFilePath = os.path.abspath(scriptPath + "../../../results/ODBC/" + scriptName)
    logFileName = scriptName + '_' + str(datetime.datetime.now()).replace(' ', '_') + '.log'   
    os.system('mkdir -p ' + logFilePath + ' 1>/dev/null 2>&1')
    return (logFilePath + '/' + logFileName)

def _getConfigParser():
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    configPath = os.path.abspath(scriptPath + "../../../config.ini")
    configParser = ConfigParser.ConfigParser()
    configParser.read(configPath)
    return configParser

def _getConnectionString():
    configParser = _getConfigParser()
    elementsList = {}
    
    for key in ("dsn", "usr", "pwd", "catalog", "schema"):
        elementsList[key] = configParser.get("pytest", key)
        
    return ('DSN=' + elementsList['dsn'] + ';UID=' + elementsList['usr'] + ';PWD=' + elementsList['pwd'])

def _getCurrentFunctionName():
    return inspect.stack()[1][3]

def _getHPDCI():
    configParser = _getConfigParser()
    elementsList = {}
    
    for key in ("host", "port", "dsn", "usr", "pwd"):
        if key == "host":
            elementsList[key] = configParser.get("pytest", "tcp").split(":")[1]
        elif key == "port":
            elementsList[key] = configParser.get("pytest", "tcp").split(":")[2]
        else:
            elementsList[key] = configParser.get("pytest", key)
    target = elementsList["host"] + ":" + elementsList["port"]

    import tests.lib.gvars as gvars
    import tests.lib.hpdci as hpdci
    hpdci.prog_parse_args_from_initfile()
    testmgr = hpdci.HPTestMgr()
    assert testmgr is not None
    dci = testmgr.create_dci_proc(__prefixName, target, elementsList["dsn"], elementsList["usr"], elementsList["pwd"])
    assert dci is not None
    return dci

class MyConnection:
    connection_string = _getConnectionString()
    
    def __init__(self):
        self.conn = None
        self.timeout = 1800
    
    def __del__(self):
        try:
            self.conn.close()
        except:
            self.conn = None
        del self.timeout
    
    def getConnection(self):
        conn = None

        try: 
            conn = pypyodbc.connect(self.__class__.connection_string, autocommit = True, timeout = self.timeout)
            if conn.connected == 1:
                conn.timeout = self.timeout
            else:
                conn = None
        except: 
            logging.debug("[*] Initialize connection failed")
        
        self.conn = conn

        return self.conn
    
    def closeConnection(self, i):
        try:
            if self.conn is None:
                pass
            elif self.conn.connected == 0:
                self.conn = None
            elif self.conn.connected == 1:
                self.conn.close()
            else:
                self.conn = None
        except:
            logging.debug("[*] Close connnection failed.")
        
        self.conn = None
    
class ScenariosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.counter = 0
    
    @classmethod
    def tearDownClass(cls):
        del cls.counter
    
    @staticmethod
    def count(v):
        return (v + 1)
    
    def setUp(self):
        self.__class__.counter = self.count(self.__class__.counter)
        logging.info("================ Test Case %03d Start ================" % (self.__class__.counter))
    
    def tearDown(self):
        logging.info("================ Test Case %03d End ==================\n" % (self.__class__.counter))

    #@unittest.skip("reserved")
    def testTfqpCoreFile(self):
        logging.info("[*] Case Name: %s.%s" % (self.__class__.__name__, _getCurrentFunctionName()))
        obj = MyConnection()
        conn = obj.getConnection()
        cursor = conn.cursor()
        # for query_summary # no core dump on TRAF R1.1
        sql = "select t1.running_count as \"running_count\", cast( 0 as bigint) as \"queued_count\", (case when t2.total_count is null or t1.running_count + t1.failed_count > t2.total_count then 0 else t2.total_count - t1.running_count - t1.failed_count end) as \"completed_count\", t1.failed_count as \"failed_count\" from (select sum (case when exec_end_utc_ts is null then 1 end) as running_count, sum (case when 0 > sql_error_code and exec_end_utc_ts > ? then 1 else 0 end) as failed_count from TRAFODION.\"_REPOS_\".metric_query_table where exec_start_utc_ts > ?) as t1, (select sum(delta_selects + delta_inserts + delta_updates + delta_deletes) as total_count from TRAFODION.\"_REPOS_\".metric_query_aggr_table where session_start_utc_ts > ? and aggregation_last_update_utc_ts > ?) as t2"
        time_list = ["2015-05-22 00:03:44.661446", "2015-05-22 00:01:26.696907", "2015-05-11 01:29:27.848725", "2015-05-11 01:29:35.201634", ]
        cursor. execute(sql, time_list)
        rows = cursor.fetchall()
        print rows
        # for query_progress # core dump on TRAF R1.1, 
        sql = "select  \
rtrim( left( t1.user_name, 128 )) as \"user_longname\" \
, rtrim( t1.query_id ) as \"jobquery_longname\" \
, case  \
        when t1.query_status = 'EXECUTING' or t1.query_status = 'INIT' then 'RUNNING' \
        when t1.query_status = 'COMPLETED' then 'COMPLETED' \
        when t1.query_status = 'REJECTED' or t1.query_status = 'CANCELLED' then 'FAILED' \
        else \
            'UNKNOWN' \
  end as \"status_name\" \
, cast (timestampdiff( sql_tsi_second \
               , timestamp '1970-01-01 00:00:00.000000' \
               , t1.exec_start_utc_ts \
               ) * 1000000 as bigint) as \"starttime_utc_ts\" \
, cast (timestampdiff( sql_tsi_second \
               , timestamp '1970-01-01 00:00:00.000000' \
               , t1.exec_end_utc_ts \
               ) * 1000000 as bigint) as \"endtime_utc_ts\" \
, case \
        when t1.exec_end_utc_ts is null then \
            cast (timestampdiff(sql_tsi_second,  \
                t1.exec_start_utc_ts,  \
                current_timestamp) * 1000 as bigint) \
        else \
            cast (timestampdiff(sql_tsi_second,  \
                t1.exec_start_utc_ts,  \
                t1.exec_end_utc_ts) * 1000 as bigint) \
  end as \"runtime_ms\" \
, case \
        when t1.query_status = 'EXECUTING' then \
            cast ( 0 as int ) \
        else \
            cast ( 1 as int ) \
  end as \"running_bool\" \
, (t1.sql_process_busy_time + 500) / 1000 as \"cpu_ms\" \
, t1.total_mem_alloc as \"memory_bytes\" \
-- ,? as read_bytes \
-- ,? as written_bytes \
 \
, rtrim( t1.query_id )          as \"query_id\" \
, rtrim( t1.role_name )         as \"role_longname\" \
, rtrim( t1.query_sub_status )  as \"query_sub_status_name\" \
, t1.start_priority             as \"start_priority\" \
, rtrim( t1.master_process_id ) as \"master_process_id\" \
, rtrim( t1.session_id )        as \"session_id\" \
, rtrim( t1.client_name )       as \"client_name\" \
, rtrim( t1.application_name )  as \"application_name\" \
, rtrim( t1.process_name )      as \"dcs_server_process_name\" \
, rtrim( t1.statement_id )      as \"statement_id\" \
, rtrim( t1.statement_type )    as \"statement_type\" \
, rtrim( t1.statement_subtype ) as \"statement_subtype\" \
, cast (timestampdiff( sql_tsi_second \
               , timestamp '1970-01-01 00:00:00.000000' \
               , t1.submit_utc_ts \
               ) * 1000000 as bigint) as \"submit_utc_ts\" \
, cast (timestampdiff( sql_tsi_second \
               , timestamp '1970-01-01 00:00:00.000000' \
               , t1.compile_start_utc_ts  \
               ) * 1000000 as bigint) as \"compile_start_utc_ts\" \
, cast (timestampdiff( sql_tsi_second \
               , timestamp '1970-01-01 00:00:00.000000' \
               , t1.compile_end_utc_ts  \
               ) * 1000000 as bigint) as \"compile_end_utc_ts\" \
, (t1.compile_elapsed_time + 500) / 1000 as \"compile_elapsed_time_ms\" \
, t1.cmp_affinity_num           as \"cmp_affinity_num\" \
, t1.cmp_dop                    as \"cmp_dop_num\" \
, t1.cmp_txn_needed             as \"cmp_txn_needed_bool\" \
, t1.cmp_mandatory_x_prod       as \"cmp_mandatory_x_prod_bool\" \
, t1.cmp_missing_stats          as \"cmp_missing_stats_bool\" \
, t1.cmp_num_joins              as \"cmp_num_joins_count\" \
, t1.cmp_full_scan_on_table     as \"cmp_full_scan_on_table_bool\" \
, t1.cmp_rows_accessed_full_scan as \"cmp_rows_accessed_full_scan_num\" \
, t1.cmp_compiler_id            as \"cmp_compiler_id\" \
, t1.cmp_cpu_path_length        as \"cmp_cpu_path_length\" \
, t1.cmp_cpu_binder             as \"cmp_cpu_binder_num\" \
, t1.cmp_cpu_normalizer         as \"cmp_cpu_normalizer_num\" \
, t1.cmp_cpu_analyzer           as \"cmp_cpu_analyzer_num\" \
, t1.cmp_cpu_optimizer          as \"cmp_cpu_optimizer_num\" \
, t1.cmp_cpu_generator          as \"cmp_cpu_generator_num\" \
, t1.cmp_metadata_cache_hits    as \"cmp_metadata_cache_hits_count\" \
, t1.cmp_metadata_cache_lookups as \"cmp_metadata_cache_lookups_count\" \
, t1.cmp_query_cache_status     as \"cmp_query_cache_status\" \
, t1.cmp_histogram_cache_hits   as \"cmp_histogram_cache_hits_count\" \
, t1.cmp_histogram_cache_lookups as \"cmp_histogram_cache_lookups_count\" \
, t1.cmp_stmt_heap_size         as \"cmp_stmt_heap_size\" \
, t1.cmp_context_heap_size      as \"cmp_context_heap_size\" \
, t1.cmp_optimization_tasks     as \"cmp_optimization_tasks_count\" \
, t1.cmp_optimization_contexts  as \"cmp_optimization_contexts_count\" \
, t1.cmp_is_recompile           as \"cmp_is_recompile_bool\" \
, cast (t1.est_accessed_rows as bigint)         as \"est_accessed_rows_count\" \
, cast (t1.est_used_rows as bigint)             as \"est_used_rows_count\" \
, cast (t1.est_num_seq_ios as bigint)           as \"est_seq_ios_count\" \
, cast (t1.est_num_rand_ios as bigint)          as \"est_rand_ios_count\" \
, cast ((t1.est_cost * 1000) as bigint)         as \"est_cost_time_ms\" \
, cast (t1.est_cardinality as bigint)           as \"est_cardinality_rows_count\" \
, cast ((t1.est_io_time * 1000) as bigint)      as \"est_io_time_ms\" \
, cast ((t1.est_msg_time * 1000) as bigint)     as \"est_msg_time_ms\" \
, cast ((t1.est_idle_time * 1000) as bigint)    as \"est_idle_time_ms\" \
, cast ((t1.est_cpu_time * 1000) as bigint)     as \"est_cpu_time_ms\" \
, cast ((t1.est_total_time * 1000) as bigint)   as \"est_total_time_ms\" \
, cast ((t1.est_total_mem * 1000) as bigint)    as \"est_total_mem_bytes\" \
, cast (t1.est_resource_usage as bigint)        as \"est_resource_usage\" \
, t1.aggregate_option           as \"aggregate_option\" \
, t1.cmp_number_of_bmos         as \"cmp_number_of_bmos_count\" \
, t1.cmp_overflow_mode          as \"cmp_overflow_mode\" \
, t1.cmp_overflow_size          as \"cmp_overflow_size\" \
, t1.aggregate_total            as \"aggregate_total_count\" \
, t1.stats_error_code           as \"stats_error_code\" \
, (t1.query_elapsed_time + 500) / 1000 as \"query_elapsed_time_ms\" \
, (t1.disk_process_busy_time + 500) / 1000 as \"disk_process_busy_time_ms\" \
, t1.disk_ios                   as \"disk_ios_count\" \
, t1.num_sql_processes          as \"num_sql_processes_count\" \
, t1.sql_space_allocated        as \"sql_space_allocated_bytes\" \
, t1.sql_space_used             as \"sql_space_used_bytes\" \
, t1.sql_heap_allocated         as \"sql_heap_allocated_bytes\" \
, t1.sql_heap_used              as \"sql_heap_used_bytes\" \
, t1.max_mem_used               as \"max_mem_used_bytes\" \
, t1.transaction_id             as \"transaction_id\" \
, t1.num_request_msgs           as \"num_request_msgs_count\" \
, t1.num_request_msg_bytes      as \"num_request_msg_bytes\" \
, t1.num_reply_msgs             as \"num_reply_msgs_count\" \
, t1.num_reply_msg_bytes        as \"num_reply_msg_bytes\" \
, cast (timestampdiff( sql_tsi_second \
               , timestamp '1970-01-01 00:00:00.000000' \
               , t1.first_result_return_utc_ts  \
               ) * 1000000 as bigint) as \"first_result_return_utc_ts\" \
, t1.rows_returned_to_master    as \"rows_returned_to_master_count\" \
, rtrim( t1.parent_query_id )   as \"parent_query_id\" \
, rtrim( t1.parent_system_name ) as \"parent_system_name\" \
, (t1.master_execution_time + 500) / 1000 as \"master_execution_time_ms\" \
, t1.error_code                 as \"error_code\" \
, t1.sql_error_code             as \"sql_error_code\" \
, t1.error_text                 as \"error_text\" \
, rtrim(t1.query_text)          as \"query_text\" \
, rtrim(t1.explain_plan)        as \"explain_plan_text\" \
, t1.last_error_before_aqr      as \"last_error_before_aqr_code\" \
, t1.delay_time_before_aqr_sec  as \"delay_time_before_aqr_s\" \
, t1.total_num_aqr_retries      as \"total_num_aqr_retries_count\" \
, t1.msg_bytes_to_disk          as \"msg_bytes_to_disk_bytes\" \
, t1.msgs_to_disk               as \"msgs_to_disk_count\" \
, t1.rows_accessed              as \"rows_accessed_count\" \
, t1.rows_retrieved             as \"rows_retrieved_count\" \
, t1.num_rows_iud               as \"num_rows_iud_count\" \
, t1.processes_created          as \"processes_created_count\" \
, (t1.process_create_busy_time + 500) / 1000 as \"process_create_busy_time_ms\" \
, t1.ovf_file_count             as \"ovf_file_count\" \
, t1.ovf_space_allocated        as \"ovf_space_allocated_bytes\" \
, t1.ovf_space_used             as \"ovf_space_used_bytes\" \
, t1.ovf_block_size             as \"ovf_block_size\" \
, t1.ovf_write_read_count       as \"ovf_write_read_count\" \
, t1.ovf_write_count            as \"ovf_write_count\" \
, t1.ovf_buffer_blocks_written  as \"ovf_buffer_blocks_written_count\" \
, t1.ovf_buffer_bytes_written   as \"ovf_buffer_written_bytes\" \
, t1.ovf_read_count             as \"ovf_read_count\" \
, t1.ovf_buffer_blocks_read     as \"ovf_buffer_blocks_read_count\" \
, t1.ovf_buffer_bytes_read      as \"ovf_buffer_read_bytes\" \
, t1.num_nodes                  as \"nodes_num\" \
, (t1.udr_process_busy_time + 500) / 1000 as \"udr_process_busy_time_ms\" \
, t1.pertable_stats             as \"pertable_stats\" \
from TRAFODION.\"_REPOS_\".metric_query_table as t1 \
where t1.exec_start_utc_ts > ? \
      and (t1.exec_end_utc_ts >= ? or t1.exec_end_utc_ts is null)"
        time_list = ["2015-05-22 00:03:44.661446", "2015-05-22 00:01:26.696907", ]
        cursor. execute(sql, time_list)
        rows = cursor.fetchall()
        print rows
        # query session
        sql = "select  \
 rtrim( t1.session_id )             as \"session_id\" \
,t1.session_status                  as \"session_status\" \
,cast (timestampdiff( sql_tsi_second \
                    , timestamp '1970-01-01 00:00:00' \
                    , t1.session_start_utc_ts \
                    ) * 1000000 as bigint) as \"session_start_utc_ts\" \
,cast (timestampdiff( sql_tsi_second \
                    , timestamp '1970-01-01 00:00:00' \
                    , t1.session_end_utc_ts \
                    ) * 1000000 as bigint) as \"session_end_utc_ts\" \
,t1.user_id                         as \"user_id\" \
,rtrim( t1.user_name )              as \"user_name\" \
,rtrim( t1.role_name )              as \"role_name\" \
,rtrim( t1.client_name )            as \"client_name\" \
,rtrim( t1.client_user_name )       as \"client_user_name\" \
,rtrim( t1.application_name )       as \"application_name\" \
,(t1.total_execution_time + 500) / 1000  as \"total_execution_time_ms\" \
,(t1.total_elapsed_time + 500) / 1000    as \"total_elapsed_time_ms\" \
,t1.total_insert_stmts_executed     as \"total_insert_stmts_count\" \
,t1.total_delete_stmts_executed     as \"total_delete_stmts_count\" \
,t1.total_update_stmts_executed     as \"total_update_stmts_count\" \
,t1.total_select_stmts_executed     as \"total_select_stmts_count\" \
,t1.total_catalog_stmts             as \"total_catalog_stmts_count\" \
,t1.total_prepares                  as \"total_prepare_calls_count\" \
,t1.total_executes                  as \"total_execute_calls_count\" \
,t1.total_fetches                   as \"total_fetche_calls_count\" \
,t1.total_closes                    as \"total_close_calls_count\" \
,t1.total_execdirects               as \"total_execdirect_calls_count\" \
,t1.total_errors                    as \"total_errors_count\" \
,t1.total_warnings                  as \"total_warnings_count\" \
,(t1.total_login_elapsed_time_mcsec + 500) / 1000           as \"total_login_elapsed_time_ms\" \
,(t1.ldap_login_elapsed_time_mcsec + 500) / 1000            as \"ldap_login_elapsed_time_ms\" \
,(t1.sql_user_elapsed_time_mcsec + 500) / 1000              as \"sql_user_elapsed_time_ms\" \
,(t1.search_connection_elapsed_time_mcsec + 500) / 1000     as \"search_connection_elapsed_time_ms\" \
,(t1.search_elapsed_time_mcsec + 500) / 1000                as \"search_elapsed_time_ms\" \
,(t1.authentication_connection_elapsed_time_mcsec + 500) / 1000     as \"authentication_connection_elapsed_time_ms\" \
,(t1.authentication_elapsed_time_mcsec + 500) / 1000        as \"authentication_elapsed_time_ms\" \
from TRAFODION.\"_REPOS_\".metric_session_table as t1 \
where t1.session_start_utc_ts > ? \
    and t1.session_end_utc_ts >= ?"
        time_list = ["2015-05-11 01:29:27.848725", "2015-05-11 01:29:35.201634", ]
        cursor. execute(sql, time_list)
        rows = cursor.fetchall()
        print rows
        # query aggr
        sql = "select  \
 rtrim( t1.session_id )             as \"session_id\" \
,cast (timestampdiff( sql_tsi_second \
                    , timestamp '1970-01-01 00:00:00' \
                    , t1.session_start_utc_ts \
                    ) * 1000000 as bigint) as \"session_start_utc_ts\" \
,cast (timestampdiff( sql_tsi_second \
                    , timestamp '1970-01-01 00:00:00' \
                    , t1.aggregation_last_update_utc_ts \
                    ) * 1000000 as bigint) as \"aggregation_last_update_utc_ts\" \
,t1.aggregation_last_elapsed_time   as \"aggregation_last_elapsed_time_ms\" \
,t1.user_id                         as \"user_id\" \
,rtrim( t1.user_name )              as \"user_name\" \
,rtrim( t1.role_name )              as \"role_name\" \
,rtrim( t1.client_name )            as \"client_name\" \
,rtrim( t1.client_user_name )       as \"client_user_name\" \
,rtrim( t1.application_name )       as \"application_name\" \
,t1.total_est_rows_accessed         as \"total_est_accessed_rows_count\" \
,t1.total_est_rows_used             as \"total_est_used_rows_count\" \
,t1.total_rows_retrieved            as \"total_retrieved_rows_count\" \
,t1.total_num_rows_iud              as \"total_iud_rows_count\" \
,t1.total_selects                   as \"total_select_stmts_count\" \
,t1.total_inserts                   as \"total_insert_stmts_count\" \
,t1.total_updates                   as \"total_update_stmts_count\" \
,t1.total_deletes                   as \"total_delete_stmts_count\" \
,t1.total_ddl_stmts                 as \"total_ddl_stmts_count\" \
,t1.total_util_stmts                as \"total_util_stmts_count\" \
,t1.total_catalog_stmts             as \"total_catalog_stmts_count\" \
,t1.total_other_stmts               as \"total_other_stmts_count\" \
,t1.total_insert_errors             as \"total_insert_errors_count\" \
,t1.total_delete_errors             as \"total_delete_errors_count\" \
,t1.total_update_errors             as \"total_update_errors_count\" \
,t1.total_select_errors             as \"total_select_errors_count\" \
,t1.total_ddl_errors                as \"total_ddl_errors_count\" \
,t1.total_util_errors               as \"total_util_errors_count\" \
,t1.total_catalog_errors            as \"total_catalog_errors_count\" \
,t1.total_other_errors              as \"total_other_errors_count\" \
,t1.delta_estimated_rows_accessed   as \"delta_est_accessed_rows_count\" \
,t1.delta_estimated_rows_used       as \"delta_est_used_rows_count\" \
,t1.delta_rows_accessed              as \"delta_accessed_rows_count\" \
,t1.delta_rows_retrieved            as \"delta_retrieved_rows_count\" \
,t1.delta_num_rows_iud              as \"delta_iud_rows_count\" \
,t1.delta_selects                   as \"delta_select_stmts_count\" \
,t1.delta_inserts                   as \"delta_insert_stmts_count\" \
,t1.delta_updates                   as \"delta_update_stmts_count\" \
,t1.delta_deletes                   as \"delta_delete_stmts_count\" \
,t1.delta_ddl_stmts                 as \"delta_ddl_stmts_count\" \
,t1.delta_util_stmts                as \"delta_util_stmts_count\" \
,t1.delta_catalog_stmts             as \"delta_catalog_stmts_count\" \
,t1.delta_other_stmts               as \"delta_other_stmts_count\" \
,t1.delta_insert_errors             as \"delta_insert_errors_count\" \
,t1.delta_delete_errors             as \"delta_delete_errors_count\" \
,t1.delta_update_errors             as \"delta_update_errors_count\" \
,t1.delta_select_errors             as \"delta_select_errors_count\" \
,t1.delta_ddl_errors                as \"delta_ddl_errors_count\" \
,t1.delta_util_errors               as \"delta_util_errors_count\" \
,t1.delta_catalog_errors            as \"delta_catalog_errors_count\" \
,t1.delta_other_errors              as \"delta_other_errors_count\" \
from TRAFODION.\"_REPOS_\".metric_query_aggr_table as t1 \
where t1.session_start_utc_ts > ? \
     and (t1.aggregation_last_update_utc_ts >= ? or t1.aggregation_last_update_utc_ts is null)"
        time_list = ["2015-05-11 01:29:27.848725", "2015-05-11 01:29:35.201634", ]
        cursor. execute(sql, time_list)
        rows = cursor.fetchall()
        print rows

        conn.close()
        logging.info("[*] Passed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=_createLogFile(),
                filemode='w')
    unittest.main()

#!END

/**
  @@@ START COPYRIGHT @@@

  (C) Copyright 2015 Hewlett-Packard Development Company, L.P.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  @@@ END COPYRIGHT @@@
*/


#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	MAX_LEN_BUF	697	// This size is set because SQL_KEYWORDS returns a LOT of info.

/*
------------------------------------------------------------------
   TestSQLGetInfo: Tests SQLGetInfo                      
------------------------------------------------------------------
*/
PassFail TestMXSQLGetInfo(TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TCHAR Heading[MAX_STRING_SIZE];
 	SQLRETURN	returncode;
 	SQLHANDLE 	henv;
 	SQLHANDLE 	hdbc;
 	SQLHANDLE	hstmt;
	union{
	    SQLLEN      longInfoValue; //  
		SQLUINTEGER	intInfoValue;
		SQLUSMALLINT smiInfoValue;
		//char charInfoValue[MAX_LEN_BUF+1];
		TCHAR charInfoValue[MAX_LEN_BUF+1];
		} u1;

	SWORD	pcbInfoValue;
	#define INVALID_pcbINFOVALUE	-12345
	
	short i;
	TCHAR TempString[MAX_STRING_SIZE];
	TCHAR ExpectedStr[MAX_LEN_BUF];
	char ExpectedStrA[MAX_LEN_BUF];
	TCHAR ActualHex[MAX_STRING_SIZE];
	TCHAR ActualStr[MAX_LEN_BUF]; // Changed to reflect the very large amount of data SQL_KEYWORDS returns.
	TrueFalse DifferenceOK;
	
	// The following list of variables are alphabetized, 
	// please try and keep it that way!
	TCHAR *accessible_procedures=_T("N");
	TCHAR *accessible_tables=_T("N");
	SQLUSMALLINT active_environments = 0;
	SQLUINTEGER aggregate_functions = {SQL_AF_AVG | SQL_AF_COUNT | SQL_AF_MAX | 
										SQL_AF_MIN | SQL_AF_SUM};
	SQLUINTEGER alter_domain=0;
	SQLUINTEGER alter_table=0;
	SQLUINTEGER async_mode=SQL_AM_STATEMENT;
	SQLUINTEGER batch_row_count = 0;
	SQLUINTEGER batch_support = 0;
	SQLUINTEGER bookmark_persistence=0;
	SQLUSMALLINT catalog_location=SQL_CL_START;
	TCHAR *catalog_name=_T("Y");
	TCHAR *catalog_name_separator=_T(".");
	TCHAR *catalog_term=_T("CATALOG");
	SQLUINTEGER catalog_usage={SQL_CU_DML_STATEMENTS | SQL_CU_TABLE_DEFINITION |
								SQL_CU_INDEX_DEFINITION};
	TCHAR *collation_seq=_T("ISO 8859-1");
	TCHAR *column_alias=_T("Y");
	SQLUSMALLINT concat_null_behavior=SQL_CB_NULL;
	SQLUINTEGER convert_bigint={SQL_CVT_CHAR | SQL_CVT_BIGINT | SQL_CVT_DECIMAL | 
								SQL_CVT_DOUBLE | SQL_CVT_FLOAT | SQL_CVT_INTEGER |
								SQL_CVT_NUMERIC | SQL_CVT_REAL |
								SQL_CVT_SMALLINT | SQL_CVT_VARCHAR};
	SQLUINTEGER convert_binary=0;
	SQLUINTEGER convert_bit=0;
	// SQL_CVT_WLONGVARCHAR is no longer supported starting R2.4 SP2.
	SQLUINTEGER convert_char={SQL_CVT_CHAR | SQL_CVT_BIGINT | SQL_CVT_DATE |
								SQL_CVT_DECIMAL | SQL_CVT_DOUBLE | SQL_CVT_FLOAT |
								SQL_CVT_INTEGER | SQL_CVT_NUMERIC |
								SQL_CVT_REAL | SQL_CVT_SMALLINT | SQL_CVT_TIME |
								SQL_CVT_TIMESTAMP | SQL_CVT_VARCHAR};	
	
	SQLUINTEGER convert_wchar={SQL_CVT_CHAR | SQL_CVT_BIGINT | SQL_CVT_DATE |
								SQL_CVT_DECIMAL | SQL_CVT_DOUBLE | SQL_CVT_FLOAT |
								SQL_CVT_INTEGER | SQL_CVT_NUMERIC |
								SQL_CVT_REAL | SQL_CVT_SMALLINT | SQL_CVT_TIME |
								SQL_CVT_TIMESTAMP | SQL_CVT_VARCHAR |
								SQL_CVT_WCHAR | SQL_CVT_WVARCHAR};
	SQLUINTEGER convert_date={SQL_CVT_CHAR | SQL_CVT_DATE | 
								SQL_CVT_TIMESTAMP | SQL_CVT_VARCHAR};
	SQLUINTEGER convert_decimal=convert_bigint;
	SQLUINTEGER convert_double=convert_bigint;
	SQLUINTEGER convert_float=convert_bigint;
	SQLUINTEGER convert_functions=SQL_FN_CVT_CONVERT;
	SQLUINTEGER convert_integer=convert_bigint;
	SQLUINTEGER convert_interval_day_time = 0;
	SQLUINTEGER convert_interval_year_month = 0;
	SQLUINTEGER convert_longvarbinary=0;
	SQLUINTEGER convert_varchar=convert_char;
	SQLUINTEGER convert_longvarchar=0;
	SQLUINTEGER convert_numeric=convert_bigint;
	SQLUINTEGER convert_real=convert_bigint;
	SQLUINTEGER convert_smallint=convert_bigint;
	SQLUINTEGER convert_time={SQL_CVT_CHAR | SQL_CVT_TIME |
								SQL_CVT_TIMESTAMP | SQL_CVT_VARCHAR};
	SQLUINTEGER convert_timestamp={SQL_CVT_CHAR | SQL_CVT_DATE | 
									SQL_CVT_TIME | SQL_CVT_TIMESTAMP | SQL_CVT_VARCHAR};
	SQLUINTEGER convert_tinyint=0;
	SQLUINTEGER convert_varbinary=0;
	SQLUINTEGER convert_wvarchar = convert_wchar;
	//SQLUINTEGER convert_wlongvarchar = convert_wchar;
	SQLUSMALLINT correlation_name=SQL_CN_ANY;
	SQLUINTEGER create_assertion = 0;
	SQLUINTEGER create_character_set = 0;
	SQLUINTEGER create_collation = 0;
	SQLUINTEGER create_domain = 0;
	SQLUINTEGER create_schema = 0;
	SQLUINTEGER create_table = {SQL_CT_CREATE_TABLE};
	SQLUINTEGER create_translation = 0;
	SQLUINTEGER create_view = {SQL_CV_CREATE_VIEW | SQL_CV_CHECK_OPTION | SQL_CV_CASCADED};
	SQLUSMALLINT cursor_commit_behavior=SQL_CB_CLOSE;
	SQLUSMALLINT cursor_rollback_behavior=SQL_CB_CLOSE;
	SQLUINTEGER cursor_sensitivity=SQL_UNSPECIFIED;
	TCHAR data_source_name[60];
	TCHAR *data_source_read_only=_T("N");
	TCHAR database_name[60];
	SQLUINTEGER datetime_literals = {SQL_DL_SQL92_DATE | SQL_DL_SQL92_TIME | SQL_DL_SQL92_TIMESTAMP | SQL_DL_SQL92_INTERVAL_YEAR |
		SQL_DL_SQL92_INTERVAL_MONTH | SQL_DL_SQL92_INTERVAL_DAY |
		SQL_DL_SQL92_INTERVAL_HOUR | SQL_DL_SQL92_INTERVAL_MINUTE |
		SQL_DL_SQL92_INTERVAL_SECOND | SQL_DL_SQL92_INTERVAL_YEAR_TO_MONTH |
		SQL_DL_SQL92_INTERVAL_DAY_TO_HOUR | SQL_DL_SQL92_INTERVAL_DAY_TO_MINUTE |
		SQL_DL_SQL92_INTERVAL_DAY_TO_SECOND |SQL_DL_SQL92_INTERVAL_HOUR_TO_MINUTE |
		SQL_DL_SQL92_INTERVAL_HOUR_TO_SECOND | SQL_DL_SQL92_INTERVAL_MINUTE_TO_SECOND};

	TCHAR  *dbms_name=_T("HP Database");
//	TCHAR  *dbms_ver=_T("01.04.0000");
	TCHAR  *dbms_ver=_T("00.07.0000");
	SQLUINTEGER ddl_index = {SQL_DI_CREATE_INDEX | SQL_DI_DROP_INDEX};
	SQLUINTEGER default_txn_isolation=SQL_TXN_READ_COMMITTED;
	TCHAR  *describe_parameter=_T("Y");
	char *dm_ver = "03.51.4202.0000"; //must be greatr than 3.51.0: checking in test code
	SQLUINTEGER driver_hdbc=0;
	SQLUINTEGER driver_henv=0;
	SQLUINTEGER driver_hlib=0;
	SQLUINTEGER driver_hstmt=0;
#ifdef unixcli
	TCHAR  *driver_name=_T("libhpodbc");
#else
	TCHAR  *driver_name=_T("hpodbc03.dll");
#endif /* WIN32 */
//	char  *driver_odbc_ver="03.51"; // must be >= 3.51
	TCHAR  *driver_odbc_ver=_T("03.51"); // must be >= 3.51
	TCHAR  *driver_ver=_T("03.00");
	SQLUINTEGER drop_assertion = 0;
	SQLUINTEGER drop_character_set = 0;
	SQLUINTEGER drop_collation = 0;
	SQLUINTEGER drop_domain = 0;
	SQLUINTEGER drop_schema = 0;
	SQLUINTEGER drop_table = {SQL_DT_DROP_TABLE | SQL_DT_RESTRICT | SQL_DT_CASCADE};
	SQLUINTEGER drop_translation = 0;
	SQLUINTEGER drop_view = {SQL_DV_DROP_VIEW | SQL_DV_RESTRICT | SQL_DV_CASCADE};
	SQLUINTEGER dynamic_cursor_attributes1 = 0;
	SQLUINTEGER dynamic_cursor_attributes2 = 0;
	TCHAR  *expressions_in_orderby=_T("N");
	SQLUINTEGER fetch_direction=SQL_FD_FETCH_NEXT;
	SQLUSMALLINT file_usage=SQL_FILE_NOT_SUPPORTED;
	SQLUINTEGER forward_only_cursor_attributes1={SQL_CA1_NEXT | SQL_CA1_SELECT_FOR_UPDATE};
	SQLUINTEGER forward_only_cursor_attributes2={SQL_CA2_READ_ONLY_CONCURRENCY |
													SQL_CA2_LOCK_CONCURRENCY |
													SQL_CA2_MAX_ROWS_SELECT};
	SQLUINTEGER getdata_extensions={SQL_GD_ANY_COLUMN | SQL_GD_ANY_ORDER | SQL_GD_BOUND};
	SQLUSMALLINT group_by=SQL_GB_GROUP_BY_EQUALS_SELECT;
	SQLUSMALLINT identifier_case=SQL_IC_UPPER;
	TCHAR  *identifier_quote_char=_T("\"");
	SQLUINTEGER index_keywords = {SQL_IK_ASC | SQL_IK_DESC};
	SQLUINTEGER info_schema_views = 0;
	SQLUINTEGER insert_statement = {SQL_IS_INSERT_LITERALS | SQL_IS_INSERT_SEARCHED |
									SQL_IS_SELECT_INTO};
	TCHAR  *integrity=_T("N");
	SQLUINTEGER keyset_cursor_attributes1 = 0;
	SQLUINTEGER keyset_cursor_attributes2 = 0;
	//TCHAR  *keywords=_T("ABS,AFTER,ALIAS,BEFORE,BOOLEAN,BREADTH,CALL,COMPLETION,CONVERTTIMESTAMP,CYCLE,DATEFORMAT,DAYOFWEEK,DEPTH,DICTIONARY,EACH,EQUALS,GENERAL,IF,IGNORE,INDEX_TABLE,INVOKE,JULIANTIMESTAMP,LEAVE,LESS,LIMIT,LOAD_TABLE,LOOP,MODIFY,NEW,OBJECT,OFF,OID,OLD,OPERATION,OPERATORS,OTHERS,PARAMETERS,PENDANT,PREORDER,PRIVATE,PROTECTED,PROTOTYPE,RECURSIVE,REF,REFERENCING,REPLACE,RESIGNAL,RESOURCE_FORK,RETURN,RETURNS,ROLE,ROUTINE,ROW,SAVEPOINT,SEARCH,SENSITIVE,SHOWDDL,SHOWPLAN,SIGNAL,SIMILAR,SQLEXCEPTION,STDDEV,STRUCTURE,TEST,THERE,TRANSPOSE,TRIGGER,TYPE,UNDER,UPSHIFT,VARIABLE,VARIANCE,VIRTUAL,WAIT,WHILE,WITHOUT");
	TCHAR *keywords = _T("ABS,AFTER,ALIAS,BEFORE,BOOLEAN,BREADTH,CALL,COMPLETION,CONVERTTIMESTAMP,CYCLE,DATEFORMAT,DAYOFWEEK,DEPTH,DICTIONARY,EACH,EQUALS,GENERAL,IF,IGNORE,INDEX_TABLE,INVOKE,JULIANTIMESTAMP,LEAVE,LESS,LIMIT,LOAD_TABLE,LOOP,MODIFY,NEW,OBJECT,OFF,OID,OLD,OPERATION,OPERATORS,OTHERS,PARAMETERS,PENDANT,PREORDER,PRIVATE,PROTECTED,PROTOTYPE,RECURSIVE,REF,REFERENCING,REPLACE,RESIGNAL,RESOURCE_FORK,RETURN,RETURNS,ROLE,ROUTINE,ROW,SAVEPOINT,SEARCH,SENSITIVE,SHOWDDL,SHOWPLAN,SIGNAL,SIMILAR,SQLEXCEPTION,STDDEV,STRUCTURE,TEST,THERE,TRANSPOSE,TRIGGER,TYPE,UNDER,UPSHIFT,VARIABLE,VARIANCE,VIRTUAL,WAIT,WHILE,WITHOUT");
	TCHAR  *like_escape_clause=_T("Y");
	SQLUINTEGER lock_types = 0;
	SQLUINTEGER max_async_concurrent_statements=0;
	SQLUINTEGER max_binary_literal_len=8100;
	SQLUSMALLINT max_catalog_name_len=128; //Changed to 128 in R2.2
	SQLUINTEGER max_char_literal_len=4050;
	SQLUSMALLINT max_column_name_len=128;	//Changed to 128 in R2.2
	SQLUSMALLINT max_columns_in_group_by=0;
	SQLUSMALLINT max_columns_in_index=0;
	SQLUSMALLINT max_columns_in_order_by=0;
	SQLUSMALLINT max_columns_in_select=0;
	SQLUSMALLINT max_columns_in_table=0;
	SQLUSMALLINT max_concurrent_activities=0; // zero for unlimitted
	SQLUSMALLINT max_cursor_name_len=128; //Changed to 128 in R2.2
	SQLUSMALLINT max_driver_connections=0;
	SQLUSMALLINT max_identifier_len=128; //Changed to 128 in R2.2
	SQLUINTEGER max_index_size=4050;
	SQLUSMALLINT max_procedure_name_len=128;
	SQLUINTEGER max_row_size=4050;
	TCHAR  *max_row_size_includes_long=_T("Y");
	SQLUSMALLINT max_schema_name_len=128;	//Changed to 128 in R2.2
	SQLUINTEGER max_statement_len=0;
	SQLUSMALLINT max_table_name_len=128;	//Changed to 128 in R2.2
	SQLUSMALLINT max_tables_in_select=0;
	SQLUSMALLINT max_user_name_len=32;
	TCHAR  *mult_result_sets=_T("N");
	TCHAR  *multiple_active_txn=_T("N");
	TCHAR  *need_long_data_len=_T("N");
	SQLUSMALLINT non_nullable_columns=SQL_NNC_NON_NULL;
	SQLUSMALLINT null_collation=SQL_NC_HIGH;
	SQLUINTEGER numeric_functions={SQL_FN_NUM_ABS | SQL_FN_NUM_ACOS | SQL_FN_NUM_ASIN | 
									SQL_FN_NUM_ATAN | SQL_FN_NUM_ATAN2 | SQL_FN_NUM_CEILING | 
									SQL_FN_NUM_COS | SQL_FN_NUM_DEGREES | SQL_FN_NUM_EXP | 
									SQL_FN_NUM_FLOOR | SQL_FN_NUM_LOG | SQL_FN_NUM_LOG10 | 
									SQL_FN_NUM_MOD | SQL_FN_NUM_PI | SQL_FN_NUM_POWER | 
									SQL_FN_NUM_RADIANS | SQL_FN_NUM_RAND | SQL_FN_NUM_SIGN | 
									SQL_FN_NUM_SIN | SQL_FN_NUM_SQRT | SQL_FN_NUM_TAN};
	SQLUSMALLINT odbc_api_conformance=SQL_OAC_LEVEL2;
	SQLUINTEGER odbc_interface_conformance = {SQL_OIC_CORE};
	SQLUSMALLINT odbc_sql_conformance = {SQL_OSC_CORE};
	char *odbc_ver="03.52.0000";
	//TCHAR *odbc_ver=_T("03.52.0000");
	SQLUINTEGER oj_capabilities={SQL_OJ_LEFT | SQL_OJ_RIGHT | SQL_OJ_FULL |
									SQL_OJ_NESTED | SQL_OJ_NOT_ORDERED | 
									SQL_OJ_INNER | SQL_OJ_ALL_COMPARISON_OPS};
	TCHAR  *order_by_columns_in_select=_T("N");
	TCHAR  *outer_joins=_T("Y");
	SQLUINTEGER param_array_roy_counts = SQL_PARC_NO_BATCH;
	SQLUINTEGER param_array_selects = SQL_PAS_NO_SELECT;
	SQLUINTEGER pos_operations = 0;
	SQLUINTEGER positioned_statements = {SQL_PS_POSITIONED_DELETE |
											SQL_PS_POSITIONED_UPDATE |
											SQL_PS_SELECT_FOR_UPDATE};
	TCHAR  *procedure_term=_T("PROCEDURE");
	TCHAR  *procedures=_T("Y");
	SQLUSMALLINT quoted_identifier_case=SQL_IC_SENSITIVE;
	TCHAR  *row_updates=_T("N");
	TCHAR  *schema_term=_T("SCHEMA");
	SQLUINTEGER schema_usage={SQL_SU_DML_STATEMENTS | SQL_SU_TABLE_DEFINITION |
								SQL_SU_PRIVILEGE_DEFINITION};
	SQLUINTEGER scroll_concurrency = {SQL_SCCO_LOCK};
	SQLUINTEGER scroll_options=SQL_SO_FORWARD_ONLY;
	TCHAR  *search_pattern_escape=_T("\\");
	SQLUINTEGER sql_conformance = {SQL_SC_SQL92_ENTRY};
	SQLUINTEGER sql92_datetime_functions = {SQL_SDF_CURRENT_DATE | SQL_SDF_CURRENT_TIME |
											SQL_SDF_CURRENT_TIMESTAMP};
	SQLUINTEGER sql92_foreign_key_delete_rule = 0;
	SQLUINTEGER sql92_foreign_key_update_rule = 0;
	SQLUINTEGER sql92_grant = 0;
	SQLUINTEGER sql92_numeric_value_functions = {SQL_SNVF_CHAR_LENGTH |
													SQL_SNVF_CHARACTER_LENGTH | 
													SQL_SNVF_EXTRACT | SQL_SNVF_OCTET_LENGTH |
													SQL_SNVF_POSITION};
	SQLUINTEGER sql92_predicates = {SQL_SP_EXISTS | SQL_SP_ISNOTNULL | SQL_SP_ISNULL |
									SQL_SP_MATCH_FULL | SQL_SP_MATCH_PARTIAL | SQL_SP_LIKE |
									SQL_SP_IN | SQL_SP_BETWEEN | SQL_SP_COMPARISON |
									SQL_SP_QUANTIFIED_COMPARISON};
	SQLUINTEGER sql92_relational_join_operators = {SQL_SRJO_CORRESPONDING_CLAUSE |
													SQL_SRJO_CROSS_JOIN |
													SQL_SRJO_FULL_OUTER_JOIN |
													SQL_SRJO_INNER_JOIN |
													SQL_SRJO_LEFT_OUTER_JOIN |
													SQL_SRJO_NATURAL_JOIN |
													SQL_SRJO_RIGHT_OUTER_JOIN |
													SQL_SRJO_UNION_JOIN};
	SQLUINTEGER sql92_revoke = 0;
	SQLUINTEGER sql92_row_value_constructor = 0;
	SQLUINTEGER sql92_string_functions = {SQL_SSF_CONVERT | SQL_SSF_LOWER | SQL_SSF_UPPER |
											SQL_SSF_SUBSTRING | SQL_SSF_TRIM_BOTH |
											SQL_SSF_TRIM_LEADING | SQL_SSF_TRIM_TRAILING};
	SQLUINTEGER sql92_value_expressions = {SQL_SVE_CASE | SQL_SVE_CAST};
	SQLUINTEGER standard_cli_conformance = {SQL_SCC_XOPEN_CLI_VERSION1 | SQL_SCC_ISO92_CLI};
	SQLUINTEGER static_cursor_attributes1 = 0;
	SQLUINTEGER static_cursor_attributes2 = 0;
	TCHAR server_name[128];
	TCHAR  *special_characters=_T("$\\");
	SQLUINTEGER static_sensitivity = {SQL_SS_ADDITIONS | SQL_SS_DELETIONS | SQL_SS_UPDATES};
	SQLUINTEGER string_functions={SQL_FN_STR_ASCII | SQL_FN_STR_CHAR | SQL_FN_STR_CONCAT | 
									SQL_FN_STR_INSERT | SQL_FN_STR_LCASE | SQL_FN_STR_LEFT | 
									SQL_FN_STR_LENGTH | SQL_FN_STR_LOCATE_2 | SQL_FN_STR_LTRIM | 
									SQL_FN_STR_REPEAT | SQL_FN_STR_REPLACE | SQL_FN_STR_RIGHT | 
									SQL_FN_STR_RTRIM | SQL_FN_STR_SPACE | SQL_FN_STR_SUBSTRING | 
									SQL_FN_STR_UCASE };
	SQLUINTEGER subqueries={SQL_SQ_CORRELATED_SUBQUERIES | SQL_SQ_COMPARISON |
							SQL_SQ_EXISTS | SQL_SQ_IN | SQL_SQ_QUANTIFIED};
	SQLUINTEGER system_functions={SQL_FN_SYS_USERNAME};
	TCHAR  *table_term=_T("TABLE");
	SQLUINTEGER timedate_add_intervals={SQL_FN_TSI_FRAC_SECOND | SQL_FN_TSI_SECOND |
										SQL_FN_TSI_MINUTE | SQL_FN_TSI_HOUR |
										SQL_FN_TSI_DAY | SQL_FN_TSI_WEEK |
										SQL_FN_TSI_MONTH | SQL_FN_TSI_YEAR};
	SQLUINTEGER timedate_diff_intervals={SQL_FN_TSI_FRAC_SECOND | SQL_FN_TSI_SECOND |
											SQL_FN_TSI_MINUTE | SQL_FN_TSI_HOUR |
											SQL_FN_TSI_DAY | SQL_FN_TSI_WEEK |
											SQL_FN_TSI_MONTH | SQL_FN_TSI_YEAR};
	SQLUINTEGER timedate_functions={SQL_FN_TD_DAYOFMONTH
										 | SQL_FN_TD_DAYOFWEEK | SQL_FN_TD_DAYOFYEAR | SQL_FN_TD_MONTH | SQL_FN_TD_QUARTER
										 | SQL_FN_TD_WEEK | SQL_FN_TD_YEAR | SQL_FN_TD_HOUR | SQL_FN_TD_MINUTE | SQL_FN_TD_SECOND
										 | SQL_FN_TD_DAYNAME | SQL_FN_TD_MONTHNAME | SQL_FN_TD_CURRENT_DATE | SQL_FN_TD_CURRENT_TIME
										 | SQL_FN_TD_CURRENT_TIMESTAMP};
	SQLUSMALLINT txn_capable=SQL_TC_ALL;
	SQLUINTEGER txn_isolation_option={SQL_TXN_READ_UNCOMMITTED | SQL_TXN_READ_COMMITTED |
										SQL_TXN_REPEATABLE_READ | SQL_TXN_SERIALIZABLE};
	SQLUINTEGER sql_union={SQL_U_UNION};
	TCHAR user_name[32]; // size is based upon SQL_MAX_USER_NAME_LEN
	//TCHAR  *xopen_cli_year=_T("1995");
	TCHAR *xopen_cli_year = _T("1995");


	// The SQLGetInfo options initialized in this structure are in alphabetical
	// order to make it easier to maintain.  Please try and keep it that way
	struct{
		SQLUSMALLINT	InfoType;
		SQLPOINTER		pInfoValue;
		long			InfoValueLength;	// equals zero if variable length string returned
		int				isStringReturned;
	} ExpectedResults[] = {
		{SQL_ACCESSIBLE_PROCEDURES,accessible_procedures,1, 1},
		{SQL_ACCESSIBLE_TABLES,accessible_tables,1, 1},
		{SQL_ACTIVE_ENVIRONMENTS,&active_environments, 2, 0},
		{SQL_AGGREGATE_FUNCTIONS, &aggregate_functions, 4, 0},
		{SQL_ALTER_DOMAIN, &alter_domain, 4, 0},
		{SQL_ALTER_TABLE,&alter_table,4, 0},
		{SQL_ASYNC_MODE,&async_mode,4, 0},
		{SQL_BATCH_ROW_COUNT, &batch_row_count, 4, 0},
		{SQL_BATCH_SUPPORT, &batch_support, 4, 0},
		{SQL_BOOKMARK_PERSISTENCE,&bookmark_persistence,4, 0},
		{SQL_CATALOG_LOCATION,&catalog_location,2, 0},
		{SQL_CATALOG_NAME,catalog_name,1, 1},
		{SQL_CATALOG_NAME_SEPARATOR,catalog_name_separator,1, 1},
		{SQL_CATALOG_TERM,catalog_term,_tcslen(catalog_term), 1},
		{SQL_CATALOG_USAGE,&catalog_usage,4, 0},
		{SQL_COLLATION_SEQ,collation_seq,_tcslen(collation_seq), 1},
		{SQL_COLUMN_ALIAS,column_alias,_tcslen(column_alias), 1},
		{SQL_CONCAT_NULL_BEHAVIOR,&concat_null_behavior,2, 0},
		{SQL_CONVERT_BIGINT,&convert_bigint,4, 0},
		{SQL_CONVERT_BINARY,&convert_binary,4, 0},
		{SQL_CONVERT_BIT,&convert_bit,4, 0},
		{SQL_CONVERT_CHAR,&convert_char,4, 0},
		{SQL_CONVERT_DATE,&convert_date,4, 0},
		{SQL_CONVERT_DECIMAL,&convert_decimal,4, 0},
		{SQL_CONVERT_DOUBLE,&convert_double,4, 0},
		{SQL_CONVERT_FLOAT,&convert_float,4, 0},
		{SQL_CONVERT_FUNCTIONS,&convert_functions,4, 0},
		{SQL_CONVERT_INTERVAL_DAY_TIME, &convert_interval_day_time, 4, 0},
		{SQL_CONVERT_INTERVAL_YEAR_MONTH, &convert_interval_year_month, 4, 0},
		{SQL_CONVERT_INTEGER,&convert_integer,4, 0},
		{SQL_CONVERT_LONGVARBINARY,&convert_longvarbinary,4, 0},
		{SQL_CONVERT_LONGVARCHAR,&convert_longvarchar,4, 0},
		{SQL_CONVERT_NUMERIC,&convert_numeric,4, 0},
		{SQL_CONVERT_REAL,&convert_real,4, 0},
		{SQL_CONVERT_SMALLINT,&convert_smallint,4, 0},
		{SQL_CONVERT_TIME,&convert_time,4, 0},
		{SQL_CONVERT_TIMESTAMP,&convert_timestamp,4, 0},
		{SQL_CONVERT_TINYINT,&convert_tinyint,4, 0},
		{SQL_CONVERT_VARBINARY,&convert_varbinary,4, 0},
		{SQL_CONVERT_VARCHAR,&convert_varchar,4, 0},
		{SQL_CONVERT_WCHAR, &convert_wchar, 4, 0},
		//{SQL_CONVERT_WLONGVARCHAR, &convert_wlongvarchar, 4, 0},
		{SQL_CONVERT_WVARCHAR, &convert_wvarchar, 4, 0},
		{SQL_CORRELATION_NAME,&correlation_name,2, 0},
		{SQL_CREATE_ASSERTION, &create_assertion, 4, 0},
		{SQL_CREATE_CHARACTER_SET, &create_character_set, 4, 0},
		{SQL_CREATE_COLLATION, &create_collation, 4, 0},
		{SQL_CREATE_DOMAIN, &create_domain, 4, 0},
		{SQL_CREATE_SCHEMA, &create_schema, 4, 0},
		{SQL_CREATE_TABLE, &create_table, 4, 0},
		{SQL_CREATE_TRANSLATION, &create_translation, 4, 0},
		{SQL_CREATE_VIEW, &create_view, 4, 0},
		{SQL_CURSOR_COMMIT_BEHAVIOR,&cursor_commit_behavior,2, 0},
		{SQL_CURSOR_ROLLBACK_BEHAVIOR,&cursor_rollback_behavior,2, 0},
		{SQL_CURSOR_SENSITIVITY,&cursor_sensitivity,4, 0},
		{SQL_DATA_SOURCE_NAME,data_source_name,_tcslen(data_source_name), 1},
		{SQL_DATA_SOURCE_READ_ONLY,data_source_read_only,1, 1},
		{SQL_DATABASE_NAME,database_name,_tcslen(database_name), 1},
		{SQL_DATETIME_LITERALS, &datetime_literals, 4, 0},
		{SQL_DBMS_NAME,dbms_name,_tcslen(dbms_name), 1},
		{SQL_DBMS_VER,dbms_ver,_tcslen(dbms_ver), 1},
		{SQL_DDL_INDEX, &ddl_index, 4, 0},
		{SQL_DEFAULT_TXN_ISOLATION,&default_txn_isolation,4, 0},
		{SQL_DESCRIBE_PARAMETER,describe_parameter,1, 1},
		{SQL_DM_VER, dm_ver, strlen(dm_ver), 1},
#ifdef _LP64 //  
		{SQL_DRIVER_HDBC,&driver_hdbc,8, 0},
		{SQL_DRIVER_HENV,&driver_henv,8, 0},
#else
		{SQL_DRIVER_HDBC,&driver_hdbc,4, 0},
		{SQL_DRIVER_HENV,&driver_henv,4, 0},
#endif
//		{SQL_DRIVER_HLIB,&driver_hlib,4, 0},
#ifdef _LP64 //  
		{SQL_DRIVER_HSTMT,&driver_hstmt,8, 0},
#else
		{SQL_DRIVER_HSTMT,&driver_hstmt,4, 0},
#endif
		{SQL_DRIVER_NAME,driver_name,_tcslen(driver_name), 1},
//		{SQL_DRIVER_ODBC_VER,driver_odbc_ver,strlen(driver_odbc_ver), 1},
		{SQL_DRIVER_ODBC_VER,driver_odbc_ver,_tcslen(driver_odbc_ver), 1},
		{SQL_DRIVER_VER,driver_ver,_tcslen(driver_ver), 1},
		{SQL_DROP_ASSERTION, &drop_assertion, 4, 0},
		{SQL_DROP_CHARACTER_SET, &drop_character_set, 4, 0},
		{SQL_DROP_COLLATION, &drop_collation, 4, 0},
		{SQL_DROP_DOMAIN, &drop_domain, 4, 0},
		{SQL_DROP_SCHEMA, &drop_schema, 4, 0},
		{SQL_DROP_TABLE, &drop_table, 4, 0},
		{SQL_DROP_TRANSLATION, &drop_translation, 4, 0},
		{SQL_DROP_VIEW, &drop_view, 4, 0},
		{SQL_DYNAMIC_CURSOR_ATTRIBUTES1,&dynamic_cursor_attributes1,4, 0},
		{SQL_DYNAMIC_CURSOR_ATTRIBUTES2, &dynamic_cursor_attributes2, 4, 0},
		{SQL_EXPRESSIONS_IN_ORDERBY,expressions_in_orderby,1, 1},
		{SQL_FETCH_DIRECTION,&fetch_direction,4, 0},
		{SQL_FILE_USAGE,&file_usage,2, 0},
		{SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1,&forward_only_cursor_attributes1,4, 0},
		{SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES2, &forward_only_cursor_attributes2, 4, 0},
		{SQL_GETDATA_EXTENSIONS,&getdata_extensions,4, 0},
		{SQL_GROUP_BY,&group_by,2, 0},
		{SQL_IDENTIFIER_CASE,&identifier_case,2, 0},
		{SQL_IDENTIFIER_QUOTE_CHAR,identifier_quote_char,1, 1},
		{SQL_INDEX_KEYWORDS, &index_keywords, 4, 0},
		{SQL_INFO_SCHEMA_VIEWS, &info_schema_views, 4, 0},
		{SQL_INSERT_STATEMENT, &insert_statement, 4, 0},
		{SQL_INTEGRITY,integrity,1, 1},
		{SQL_KEYWORDS,keywords,_tcslen(keywords), 1},
		{SQL_KEYSET_CURSOR_ATTRIBUTES1,&keyset_cursor_attributes1,4, 0},
		{SQL_KEYSET_CURSOR_ATTRIBUTES2, &keyset_cursor_attributes2, 4, 0},
		{SQL_LIKE_ESCAPE_CLAUSE,like_escape_clause,1, 1},
		{SQL_LOCK_TYPES, &lock_types, 4, 0},
		{SQL_MAX_ASYNC_CONCURRENT_STATEMENTS,&max_async_concurrent_statements,4, 0},
		{SQL_MAX_BINARY_LITERAL_LEN,&max_binary_literal_len,4, 0},
		{SQL_MAX_CATALOG_NAME_LEN,&max_catalog_name_len,2, 0},
		{SQL_MAX_CHAR_LITERAL_LEN,&max_char_literal_len,4, 0},
		{SQL_MAX_COLUMN_NAME_LEN,&max_column_name_len,2, 0},
		{SQL_MAX_COLUMNS_IN_GROUP_BY,&max_columns_in_group_by,2, 0},
		{SQL_MAX_COLUMNS_IN_INDEX,&max_columns_in_index,2, 0},
		{SQL_MAX_COLUMNS_IN_ORDER_BY,&max_columns_in_order_by,2, 0},
		{SQL_MAX_COLUMNS_IN_SELECT,&max_columns_in_select,2, 0},
		{SQL_MAX_COLUMNS_IN_TABLE,&max_columns_in_table,2, 0},
		{SQL_MAX_CONCURRENT_ACTIVITIES,&max_concurrent_activities,2, 0},
		{SQL_MAX_CURSOR_NAME_LEN,&max_cursor_name_len,2, 0},
		{SQL_MAX_DRIVER_CONNECTIONS,&max_driver_connections,2, 0},
		{SQL_MAX_IDENTIFIER_LEN,&max_identifier_len,2, 0},
		{SQL_MAX_INDEX_SIZE,&max_index_size,4, 0},
		{SQL_MAX_PROCEDURE_NAME_LEN,&max_procedure_name_len,2, 0},
		{SQL_MAX_ROW_SIZE,&max_row_size,4, 0},
		{SQL_MAX_ROW_SIZE_INCLUDES_LONG,max_row_size_includes_long,1, 1},
		{SQL_MAX_SCHEMA_NAME_LEN,&max_schema_name_len,2, 0},
		{SQL_MAX_STATEMENT_LEN,&max_statement_len,4, 0},
		{SQL_MAX_TABLE_NAME_LEN,&max_table_name_len,2, 0},
		{SQL_MAX_TABLES_IN_SELECT,&max_tables_in_select,2, 0},
		{SQL_MAX_USER_NAME_LEN,&max_user_name_len,2, 0},
		{SQL_MULT_RESULT_SETS,mult_result_sets,1, 1},
		{SQL_MULTIPLE_ACTIVE_TXN,multiple_active_txn,1, 1},
		{SQL_NEED_LONG_DATA_LEN,need_long_data_len,1, 1},
		{SQL_NON_NULLABLE_COLUMNS,&non_nullable_columns,2, 0},
		{SQL_NULL_COLLATION,&null_collation,2, 0},
		{SQL_NUMERIC_FUNCTIONS,&numeric_functions,4, 0},
		{SQL_ODBC_API_CONFORMANCE,&odbc_api_conformance,2, 0},
		{SQL_ODBC_INTERFACE_CONFORMANCE, &odbc_interface_conformance, 4, 0},
		{SQL_ODBC_SAG_CLI_CONFORMANCE, &odbc_sql_conformance, 2, 0},
		{SQL_ODBC_SQL_CONFORMANCE, &odbc_sql_conformance, 2, 0},
		{SQL_ODBC_VER,odbc_ver,strlen(odbc_ver), 1},
		{SQL_OJ_CAPABILITIES,&oj_capabilities,4, 0},
		{SQL_ORDER_BY_COLUMNS_IN_SELECT,order_by_columns_in_select,1, 1},
		{SQL_OUTER_JOINS,outer_joins,1, 1},
		{SQL_PARAM_ARRAY_ROW_COUNTS, &param_array_roy_counts, 4, 0},
		{SQL_PARAM_ARRAY_SELECTS, &param_array_selects, 4, 0},
		{SQL_POS_OPERATIONS, &pos_operations, 4, 0},
		{SQL_POSITIONED_STATEMENTS, &positioned_statements, 4, 0},
		{SQL_PROCEDURE_TERM,procedure_term,_tcslen(procedure_term), 1},
		{SQL_PROCEDURES,procedures,1, 1},
		{SQL_QUOTED_IDENTIFIER_CASE,&quoted_identifier_case,2, 0},
		{SQL_ROW_UPDATES,row_updates,1, 1},
		{SQL_SCHEMA_TERM,schema_term,_tcslen(schema_term), 1},
		{SQL_SCHEMA_USAGE,&schema_usage,4, 0},
		{SQL_SCROLL_CONCURRENCY, &scroll_concurrency, 4, 0},
		{SQL_SCROLL_OPTIONS,&scroll_options,4, 0},
		{SQL_SEARCH_PATTERN_ESCAPE,search_pattern_escape,1, 1},
		{SQL_SERVER_NAME,server_name,_tcslen(server_name), 1},
		{SQL_SPECIAL_CHARACTERS,special_characters,_tcslen(special_characters), 1},
		{SQL_SQL_CONFORMANCE, &sql_conformance, 4, 0},
		{SQL_SQL92_DATETIME_FUNCTIONS, &sql92_datetime_functions, 4, 0},
		{SQL_SQL92_FOREIGN_KEY_DELETE_RULE, &sql92_foreign_key_delete_rule, 4, 0},
		{SQL_SQL92_FOREIGN_KEY_UPDATE_RULE, &sql92_foreign_key_update_rule, 4, 0},
		{SQL_SQL92_GRANT, &sql92_grant, 4, 0},
		{SQL_SQL92_NUMERIC_VALUE_FUNCTIONS, &sql92_numeric_value_functions, 4, 0},
		{SQL_SQL92_PREDICATES, &sql92_predicates, 4, 0},
		{SQL_SQL92_RELATIONAL_JOIN_OPERATORS, &sql92_relational_join_operators, 4, 0},
		{SQL_SQL92_REVOKE, &sql92_revoke, 4, 0},
		{SQL_SQL92_ROW_VALUE_CONSTRUCTOR, &sql92_row_value_constructor, 4, 0},
		{SQL_SQL92_STRING_FUNCTIONS, &sql92_string_functions, 4, 0},
		{SQL_SQL92_VALUE_EXPRESSIONS, &sql92_value_expressions, 4, 0},
		{SQL_STANDARD_CLI_CONFORMANCE, &standard_cli_conformance, 4, 0},
		{SQL_STATIC_CURSOR_ATTRIBUTES1,&static_cursor_attributes1,4, 0},
		{SQL_STATIC_CURSOR_ATTRIBUTES2, &static_cursor_attributes2, 4, 0},
		{SQL_STATIC_SENSITIVITY, &static_sensitivity, 4, 0},
		{SQL_STRING_FUNCTIONS,&string_functions,4, 0},
		{SQL_SUBQUERIES,&subqueries,4, 0},
		{SQL_SYSTEM_FUNCTIONS,&system_functions,4, 0},
		{SQL_TABLE_TERM,table_term,_tcslen(table_term), 1},
		{SQL_TIMEDATE_ADD_INTERVALS,&timedate_add_intervals,4, 0},
		{SQL_TIMEDATE_DIFF_INTERVALS,&timedate_diff_intervals,4, 0},
		{SQL_TIMEDATE_FUNCTIONS,&timedate_functions,4, 0},
		{SQL_TXN_CAPABLE,&txn_capable,2, 0},
		{SQL_TXN_ISOLATION_OPTION,&txn_isolation_option,4, 0},
		{SQL_UNION,&sql_union,4, 0},
		{SQL_USER_NAME,user_name,_tcslen(user_name), 1},
		{SQL_XOPEN_CLI_YEAR, xopen_cli_year, _tcslen(xopen_cli_year), 1}
	  };

	short TotalOptions=sizeof(ExpectedResults)/sizeof(ExpectedResults[0]);
	
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX specific SQLGetInfo.\n"));

	TEST_INIT;       
	TESTCASE_BEGIN("Setup for SQLGetInfo tests\n");
	
	returncode=FullConnect(pTestInfo);
	if (pTestInfo->hdbc == (SQLHANDLE)NULL)
	{
		TEST_FAILED;
		TEST_RETURN;
	}

  	/* Set up some local variables to save on typing in longer ones */
	henv = pTestInfo->henv;
	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	
	TESTCASE_END;

	// Further defining data for some of the test cases that are run-time dependant.
	for (i = 0; i < TotalOptions; i++)
	{
		switch (ExpectedResults[i].InfoType)
		{
			case SQL_DATA_SOURCE_NAME:
				_tcscpy(data_source_name,pTestInfo->DataSource);
				ExpectedResults[i].InfoValueLength = _tcslen(data_source_name);
				break;
			case SQL_DATABASE_NAME:
				_tcscpy(database_name,pTestInfo->Catalog);
				ExpectedResults[i].InfoValueLength = _tcslen(database_name);
				break;
			case SQL_SERVER_NAME:
				_tcscpy(server_name,_T("TCP:xxx.xxx.xxx.xxx/xxxxx"));
				_tcsupr(server_name);
				ExpectedResults[i].InfoValueLength = _tcslen(server_name);
				break;
			case SQL_USER_NAME:
				//We now return schema as user_name.
				//And now return the login name as user_name. 06/21/07 - R2.2
				_tcscpy(user_name,pTestInfo->UserID);
				//_tcscpy(user_name,pTestInfo->Schema);
				ExpectedResults[i].InfoValueLength = _tcslen(user_name);
			default:
				break;
		}
	}

	for (i = 0; i < TotalOptions; i++)
	{
		switch(ExpectedResults[i].InfoType)
		{
			case SQL_DM_VER:
//			case SQL_DRIVER_ODBC_VER:
			case SQL_ODBC_VER:
				break;
			default:
				if (ExpectedResults[i].isStringReturned)
					ExpectedResults[i].InfoValueLength *= sizeof(TCHAR);
		}
	}

	// Running tests
	for (i = 0; i < TotalOptions; i++){
		_stprintf(Heading,_T("Test SQLGetInfo(%s)\n"),
			InfoTypeToChar(ExpectedResults[i].InfoType, TempString));
		TESTCASE_BEGINW(Heading);
		
		memset(u1.charInfoValue,NULL_STRING,sizeof(u1.charInfoValue));
		pcbInfoValue=INVALID_pcbINFOVALUE;

		if(SQL_DRIVER_HSTMT==ExpectedResults[i].InfoType){
			u1.longInfoValue=(unsigned long)hstmt; //  
		}

		returncode = SQLGetInfo((SQLHANDLE)hdbc,ExpectedResults[i].InfoType,(char *)u1.charInfoValue,
								(SWORD)sizeof(u1.charInfoValue),&pcbInfoValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetInfo")){
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else{
			// Check results for correct values

			// Check returned length
			switch(ExpectedResults[i].InfoType){
				// These options can have a different length so don't check the length
				case SQL_DRIVER_NAME:
				case SQL_DRIVER_VER:
				case SQL_SERVER_NAME:
					break;
				default:
					if(ExpectedResults[i].InfoValueLength!=pcbInfoValue){
						LogMsg(ERRMSG,_T("Count of bytes returned is wrong\n"));
						if(pcbInfoValue==INVALID_pcbINFOVALUE){
							LogMsg(NONE,_T("   Expected:%ld  Actual:<no value returned>\n"),
								ExpectedResults[i].InfoValueLength);
							pcbInfoValue=(SWORD)ExpectedResults[i].InfoValueLength;	// set it to a safe value since no value was returned
						}
						else{
							LogMsg(NONE,_T("   Expected:%ld  Actual:%ld\n"),
								ExpectedResults[i].InfoValueLength,pcbInfoValue);
						}
						TEST_FAILED;
					}
					break;
			} // end of switch
			
			// Check returned value
			DifferenceOK=FALSE;
			if(memcmp(ExpectedResults[i].pInfoValue,u1.charInfoValue,ExpectedResults[i].InfoValueLength)){
				switch(ExpectedResults[i].InfoType){

					// Yes/No return values
					case SQL_ACCESSIBLE_PROCEDURES:
					case SQL_ACCESSIBLE_TABLES:
					case SQL_CATALOG_NAME:
					case SQL_COLUMN_ALIAS:
					case SQL_DATA_SOURCE_READ_ONLY:
					case SQL_DESCRIBE_PARAMETER:
					case SQL_EXPRESSIONS_IN_ORDERBY:
					case SQL_LIKE_ESCAPE_CLAUSE:
					case SQL_MULT_RESULT_SETS:
					case SQL_MULTIPLE_ACTIVE_TXN:
					case SQL_NEED_LONG_DATA_LEN:
					case SQL_ORDER_BY_COLUMNS_IN_SELECT:
					case SQL_PROCEDURES:
					case SQL_ROW_UPDATES:
					case SQL_OUTER_JOINS:
						_tcscpy(ExpectedStr,(TCHAR *)ExpectedResults[i].pInfoValue);
						BufferToHex(u1.charInfoValue,ActualHex,pcbInfoValue+1);
						_tcsncpy(ActualStr,u1.charInfoValue,pcbInfoValue+1);
						break;

					// SQLUINTEGER return values
					case SQL_AGGREGATE_FUNCTIONS:
						AggregateToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						AggregateToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_ALTER_TABLE:
						AlterTableToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						AlterTableToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_CATALOG_USAGE:
						CatalogUsageToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						CatalogUsageToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_CONVERT_BIGINT:
					case SQL_CONVERT_BINARY:
					case SQL_CONVERT_BIT:
					case SQL_CONVERT_CHAR:
					case SQL_CONVERT_DATE:
					case SQL_CONVERT_DECIMAL:
					case SQL_CONVERT_DOUBLE:
					case SQL_CONVERT_FLOAT:
					case SQL_CONVERT_INTERVAL_DAY_TIME:
					case SQL_CONVERT_INTERVAL_YEAR_MONTH:
					case SQL_CONVERT_INTEGER:
					case SQL_CONVERT_LONGVARBINARY:
					case SQL_CONVERT_LONGVARCHAR:
					case SQL_CONVERT_NUMERIC:
					case SQL_CONVERT_REAL:
					case SQL_CONVERT_SMALLINT:
					case SQL_CONVERT_TIME:
					case SQL_CONVERT_TIMESTAMP:
					case SQL_CONVERT_TINYINT:
					case SQL_CONVERT_VARBINARY:
					case SQL_CONVERT_VARCHAR:
					case SQL_CONVERT_WCHAR:
					case SQL_CONVERT_WLONGVARCHAR:
					case SQL_CONVERT_WVARCHAR:
						ConvertValueToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						ConvertValueToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_CONVERT_FUNCTIONS:
						CvtFunctionToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						CvtFunctionToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_DEFAULT_TXN_ISOLATION:
						TxnIsolationToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						TxnIsolationToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_DYNAMIC_CURSOR_ATTRIBUTES1:
					case SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1:
					case SQL_KEYSET_CURSOR_ATTRIBUTES1:
					case SQL_STATIC_CURSOR_ATTRIBUTES1:
						CA1ToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						CA1ToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_DYNAMIC_CURSOR_ATTRIBUTES2:
					case SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES2:
					case SQL_KEYSET_CURSOR_ATTRIBUTES2:
					case SQL_STATIC_CURSOR_ATTRIBUTES2:
						CA2ToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						CA2ToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_NUMERIC_FUNCTIONS:
						NumFunctionToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						NumFunctionToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_STRING_FUNCTIONS:
						StrFunctionToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						StrFunctionToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_TIMEDATE_ADD_INTERVALS:
					case SQL_TIMEDATE_DIFF_INTERVALS:
						TimeIntToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						TimeIntToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_TIMEDATE_FUNCTIONS:
						TimeFunctionToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						TimeFunctionToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_OJ_CAPABILITIES:
						OJToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						OJToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_GETDATA_EXTENSIONS:
						GDExtToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						GDExtToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_SCHEMA_USAGE:
						SchemaUsageToString(*((long *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						SchemaUsageToString(u1.intInfoValue,ActualStr);
						break;
					case SQL_DRIVER_HDBC:
					case SQL_DRIVER_HENV:
//					case SQL_DRIVER_HLIB:
					case SQL_DRIVER_HSTMT:
						DifferenceOK=TRUE;
						break;
					case SQL_ALTER_DOMAIN:
					case SQL_ASYNC_MODE:
					case SQL_BATCH_ROW_COUNT:
					case SQL_BATCH_SUPPORT:
					case SQL_BOOKMARK_PERSISTENCE:
					case SQL_SQL_CONFORMANCE:
					case SQL_CREATE_ASSERTION:
					case SQL_CREATE_CHARACTER_SET:
					case SQL_CREATE_COLLATION:
					case SQL_CREATE_DOMAIN:
					case SQL_CREATE_SCHEMA:
					case SQL_CREATE_TABLE:
					case SQL_CREATE_TRANSLATION:
					case SQL_CREATE_VIEW:
					case SQL_CURSOR_SENSITIVITY:
					case SQL_DATETIME_LITERALS:
					case SQL_DDL_INDEX:
					case SQL_DROP_ASSERTION:
					case SQL_DROP_CHARACTER_SET:
					case SQL_DROP_COLLATION:
					case SQL_DROP_DOMAIN:
					case SQL_DROP_SCHEMA:
					case SQL_DROP_TABLE:
					case SQL_DROP_TRANSLATION:
					case SQL_DROP_VIEW:
					case SQL_FETCH_DIRECTION:
					case SQL_INDEX_KEYWORDS:
					case SQL_INFO_SCHEMA_VIEWS:
					case SQL_INSERT_STATEMENT:
					case SQL_LOCK_TYPES:
					case SQL_MAX_ASYNC_CONCURRENT_STATEMENTS:
					case SQL_MAX_BINARY_LITERAL_LEN:
					case SQL_MAX_CHAR_LITERAL_LEN:
					case SQL_MAX_INDEX_SIZE:
					case SQL_MAX_ROW_SIZE:
					case SQL_MAX_STATEMENT_LEN:
					case SQL_ODBC_INTERFACE_CONFORMANCE:
					case SQL_PARAM_ARRAY_ROW_COUNTS:
					case SQL_PARAM_ARRAY_SELECTS:
					case SQL_POS_OPERATIONS:
					case SQL_POSITIONED_STATEMENTS:
					case SQL_SCROLL_CONCURRENCY:
					case SQL_SCROLL_OPTIONS:
					case SQL_SQL92_DATETIME_FUNCTIONS:
					case SQL_SQL92_FOREIGN_KEY_DELETE_RULE:
					case SQL_SQL92_FOREIGN_KEY_UPDATE_RULE:
					case SQL_SQL92_GRANT:
					case SQL_SQL92_NUMERIC_VALUE_FUNCTIONS:
					case SQL_SQL92_PREDICATES:
					case SQL_SQL92_RELATIONAL_JOIN_OPERATORS:
					case SQL_SQL92_REVOKE:
					case SQL_SQL92_ROW_VALUE_CONSTRUCTOR:
					case SQL_SQL92_STRING_FUNCTIONS:
					case SQL_SQL92_VALUE_EXPRESSIONS:
					case SQL_STANDARD_CLI_CONFORMANCE:
					case SQL_STATIC_SENSITIVITY:
					case SQL_SUBQUERIES:
					case SQL_SYSTEM_FUNCTIONS:
					case SQL_TXN_ISOLATION_OPTION:
					case SQL_UNION:
						_stprintf(ExpectedStr,_T("%ld"),*((long *)ExpectedResults[i].pInfoValue));
						_stprintf(ActualHex,_T("0x%08lX"),u1.intInfoValue);
						_stprintf(ActualStr,_T("%ld"),u1.intInfoValue);
						break;

					// SQLUSMALLINT return values
					case SQL_CATALOG_LOCATION:
						CatalogLocationToString(*((short *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%04X"),u1.smiInfoValue);
						CatalogLocationToString(u1.smiInfoValue,ActualStr);
						break;
					case SQL_CONCAT_NULL_BEHAVIOR:
						ConcatNullToString(*((short *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%04X"),u1.smiInfoValue);
						ConcatNullToString(u1.smiInfoValue,ActualStr);
						break;
					case SQL_CORRELATION_NAME:
						CorrelationToString(*((short *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%04X"),u1.smiInfoValue);
						CorrelationToString(u1.smiInfoValue,ActualStr);
						break;
					case SQL_CURSOR_COMMIT_BEHAVIOR:
					case SQL_CURSOR_ROLLBACK_BEHAVIOR:
						CursorBehaviorToString(*((short *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%04X"),u1.smiInfoValue);
						CursorBehaviorToString(u1.smiInfoValue,ActualStr);
						break;
					case SQL_FILE_USAGE:
						FileUsageToString(*((short *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%04X"),u1.smiInfoValue);
						FileUsageToString(u1.smiInfoValue,ActualStr);
						break;
					case SQL_GROUP_BY:
						GroupByToString(*((short *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%04X"),u1.smiInfoValue);
						GroupByToString(u1.smiInfoValue,ActualStr);
						break;
					case SQL_IDENTIFIER_CASE:
						CaseToString(*((short *)ExpectedResults[i].pInfoValue),ExpectedStr);
						_stprintf(ActualHex,_T("0x%04X"),u1.smiInfoValue);
						CaseToString(u1.smiInfoValue,ActualStr);
						break;
					case SQL_ACTIVE_ENVIRONMENTS:
					case SQL_MAX_CATALOG_NAME_LEN:
					case SQL_MAX_COLUMN_NAME_LEN:
					case SQL_MAX_COLUMNS_IN_GROUP_BY:
					case SQL_MAX_COLUMNS_IN_INDEX:
					case SQL_MAX_COLUMNS_IN_ORDER_BY:
					case SQL_MAX_COLUMNS_IN_SELECT:
					case SQL_MAX_COLUMNS_IN_TABLE:
					case SQL_MAX_CONCURRENT_ACTIVITIES:
					case SQL_MAX_CURSOR_NAME_LEN:
					case SQL_MAX_DRIVER_CONNECTIONS:
					case SQL_MAX_PROCEDURE_NAME_LEN:
					case SQL_MAX_SCHEMA_NAME_LEN:
					case SQL_MAX_TABLE_NAME_LEN:
					case SQL_MAX_TABLES_IN_SELECT:
					case SQL_MAX_USER_NAME_LEN:
					case SQL_ODBC_SAG_CLI_CONFORMANCE:
					case SQL_ODBC_SQL_CONFORMANCE:
						_stprintf(ExpectedStr,_T("%d"),*((short *)ExpectedResults[i].pInfoValue));
						_stprintf(ActualHex,_T("0x%04X"),u1.smiInfoValue);
						_stprintf(ActualStr,_T("%d"),u1.smiInfoValue);
						break;


					// Character string return values
					case SQL_CATALOG_NAME_SEPARATOR:
					case SQL_CATALOG_TERM:
					case SQL_COLLATION_SEQ:
					case SQL_DATA_SOURCE_NAME:
					case SQL_DATABASE_NAME:
					case SQL_DBMS_NAME:
					case SQL_DBMS_VER:

					

					//case SQL_DRIVER_ODBC_VER: special case
					case SQL_IDENTIFIER_QUOTE_CHAR:
//					case SQL_KEYWORDS:
					case SQL_PROCEDURE_TERM:
					case SQL_SCHEMA_TERM:
					case SQL_SEARCH_PATTERN_ESCAPE:
					case SQL_SPECIAL_CHARACTERS:
					case SQL_TABLE_TERM:
					case SQL_USER_NAME:
					case SQL_XOPEN_CLI_YEAR:
						// Verifying to see if our first check failed due to text casing.
						if (_tcscmp((TCHAR *)ExpectedResults[i].pInfoValue,
									_tcsupr(_tcsdup(u1.charInfoValue))) == 0) {
							DifferenceOK = TRUE;
							break;
						}
						// Mismatched casing wasn't the problem! Let's log this as an error.
						_tcscpy(ExpectedStr,(TCHAR *)ExpectedResults[i].pInfoValue);
						BufferToHex(u1.charInfoValue,ActualHex,pcbInfoValue+1);
						_tcsncpy(ActualStr,u1.charInfoValue,pcbInfoValue+1);
						break;
					case SQL_ODBC_VER:
					/*	
						if (strcmp((char *)ExpectedResults[i].pInfoValue, (char *)u1.charInfoValue) == 0) {
							DifferenceOK = TRUE;
							break;
						}
					*/
						if (_tcscmp((TCHAR *)ExpectedResults[i].pInfoValue,
					            _tcsupr(_tcsdup(u1.charInfoValue))) == 0) {
							DifferenceOK = TRUE;
							break;
						}

						_tcscpy(ExpectedStr,(TCHAR *)ExpectedResults[i].pInfoValue);
						BufferToHex(u1.charInfoValue,ActualHex,pcbInfoValue+1);
						_tcsncpy(ActualStr,u1.charInfoValue,pcbInfoValue+1);
						break;
					case SQL_KEYWORDS:
						// Verifying to see if our first check failed due to text casing.
						if (_tcscmp((TCHAR *)ExpectedResults[i].pInfoValue,
									_tcsupr(_tcsdup(u1.charInfoValue))) == 0) {
							DifferenceOK = TRUE;
							break;
						}
						// Mismatched casing wasn't the problem! Let's log this as an error.
						_tcscpy(ExpectedStr,(TCHAR *)ExpectedResults[i].pInfoValue);
						_tcsncpy(ActualStr,u1.charInfoValue,pcbInfoValue+1);
						break;
					case SQL_DRIVER_NAME:
					case SQL_DRIVER_VER:
					case SQL_SERVER_NAME:
						if(_tcsstr(_tcsupr(_tcsdup(u1.charInfoValue)),
							_T("TCP:"))==NULL)
						{
							_stprintf(ExpectedStr,_T(" something containing this string -->'%s'"),
									(TCHAR *)ExpectedResults[i].pInfoValue);
							BufferToHex(u1.charInfoValue,ActualHex,pcbInfoValue+1);
							_tcsncpy(ActualStr,u1.charInfoValue,pcbInfoValue+1);
						}
						else DifferenceOK=TRUE;
						break;

					//check for driver  version >= 3.51
					case SQL_DRIVER_ODBC_VER:
					case SQL_DM_VER:
						if(strstr((char *)u1.charInfoValue,"3.5")==NULL)
						{
							_stprintf(ExpectedStr,_T(" something containing this string -->'%s'"),_T("3.5"));
							BufferToHex(u1.charInfoValue,ActualHex,pcbInfoValue+1);
							_tcsncpy(ActualStr,u1.charInfoValue,pcbInfoValue+1);
						}
						else DifferenceOK=TRUE;
						break;

					// These options still need functions to convert their flag values to
					// a more user friendly string.  Until then, we'll simple display them
					// in hex.
					// SQLUSMALLINT
					case SQL_MAX_IDENTIFIER_LEN:
					case SQL_NON_NULLABLE_COLUMNS:
					case SQL_NULL_COLLATION:
					case SQL_QUOTED_IDENTIFIER_CASE:
					case SQL_TXN_CAPABLE:
					case SQL_ODBC_API_CONFORMANCE:
						_stprintf(ExpectedStr,_T("%d (0x%04X)"),*((short *)ExpectedResults[i].pInfoValue),
							*((short *)ExpectedResults[i].pInfoValue));
						_stprintf(ActualHex,_T("0x%04X"),u1.smiInfoValue);
						_stprintf(ActualStr,_T("%d"),u1.smiInfoValue);
						break;
				} // end of switch
				if(DifferenceOK){
					// don't display any message
				}
				else{
					LogMsg(ERRMSG,_T("Returned value is wrong\n\
								Expected:%s\n\
								Actual:%s\n\
								Actual(hex):%s\n"),ExpectedStr,ActualStr,ActualHex);
					TEST_FAILED;
				}
			} // end of if
		}
		TESTCASE_END;
	}

	// Test with StringLengthPtr set to NULL
	for (i = 0; i < TotalOptions; i++){
		_stprintf(Heading,_T("Test SQLGetInfo(%s) with StringLengthPtr set to NULL.\n"),
			InfoTypeToChar(ExpectedResults[i].InfoType, TempString));
		TESTCASE_BEGINW(Heading);
		
		if(SQL_DRIVER_HSTMT==ExpectedResults[i].InfoType){
			u1.longInfoValue=(unsigned long)hstmt; //  
		}

		returncode = SQLGetInfo((SQLHANDLE)hdbc,ExpectedResults[i].InfoType,u1.charInfoValue,
			(SWORD)sizeof(u1.charInfoValue),NULL);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetInfo")){
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;
	}

	// Test with InfoValuePtr set to NULL
	for (i = 0; i < TotalOptions; i++){
		_stprintf(Heading,_T("Test SQLGetInfo(%s) with InfoValuePtr set to NULL.\n"),
			InfoTypeToChar(ExpectedResults[i].InfoType, TempString));
		TESTCASE_BEGINW(Heading);

		if(ExpectedResults[i].InfoType==SQL_GETDATA_EXTENSIONS){
     	returncode = SQLGetInfo((SQLHANDLE)hdbc,ExpectedResults[i].InfoType,&u1.intInfoValue,
			(SWORD)sizeof(u1.intInfoValue),&pcbInfoValue);
		}
		else{
		returncode = SQLGetInfo((SQLHANDLE)hdbc,ExpectedResults[i].InfoType,NULL,
			(SWORD)sizeof(u1.charInfoValue),&pcbInfoValue);
		}
		if(SQL_DRIVER_HSTMT==ExpectedResults[i].InfoType){
			LogAllErrors(henv,hdbc,hstmt);
			if(!CHECKRC(SQL_ERROR,returncode,"SQLGetInfo")){
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
		else{
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetInfo")){
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
		TESTCASE_END;
	}
	
	// BufferLength should only effect character data returned.
	// BufferLength should be ignored for any numeric values returned.
	for (i = 0; i < TotalOptions; i++){
		_stprintf(Heading,_T("Test SQLGetInfo(%s) with BufferLength set to 1.\n"),
			InfoTypeToChar(ExpectedResults[i].InfoType, TempString));
		TESTCASE_BEGINW(Heading);
		
		if(SQL_DRIVER_HSTMT==ExpectedResults[i].InfoType){
			u1.longInfoValue=(unsigned long)hstmt; //  
		}

		returncode = SQLGetInfo((SQLHANDLE)hdbc,ExpectedResults[i].InfoType,
								u1.charInfoValue,1*sizeof(TCHAR),&pcbInfoValue);


		switch(ExpectedResults[i].InfoType){

			// character string return values
			case SQL_ACCESSIBLE_PROCEDURES:
			case SQL_ACCESSIBLE_TABLES:
			case SQL_CATALOG_NAME:
			case SQL_CATALOG_NAME_SEPARATOR:
			case SQL_CATALOG_TERM:
			case SQL_COLLATION_SEQ:
			case SQL_COLUMN_ALIAS:
			case SQL_DATA_SOURCE_NAME:
			case SQL_DATA_SOURCE_READ_ONLY:
			case SQL_DATABASE_NAME:
			case SQL_DBMS_NAME:
			case SQL_DBMS_VER:
			case SQL_DESCRIBE_PARAMETER:
			case SQL_DM_VER:
			case SQL_DRIVER_NAME:
			case SQL_DRIVER_ODBC_VER:
			case SQL_DRIVER_VER:
			case SQL_EXPRESSIONS_IN_ORDERBY:
			case SQL_IDENTIFIER_QUOTE_CHAR:
			case SQL_INTEGRITY:
			//case SQL_KEYWORDS: This is returning nothing and will return SQL_SUCCESS.
			case SQL_LIKE_ESCAPE_CLAUSE:
			case SQL_MAX_ROW_SIZE_INCLUDES_LONG:
			case SQL_MULT_RESULT_SETS:
			case SQL_MULTIPLE_ACTIVE_TXN:
			case SQL_NEED_LONG_DATA_LEN:
			case SQL_ODBC_VER:
			case SQL_ORDER_BY_COLUMNS_IN_SELECT:
			case SQL_OUTER_JOINS:
			//case SQL_PROCEDURE_TERM: This is returning nothing and will return SQL_SUCCESS.
			case SQL_PROCEDURES:
			case SQL_ROW_UPDATES:
			case SQL_SCHEMA_TERM:
			case SQL_SEARCH_PATTERN_ESCAPE:
			case SQL_SERVER_NAME:
			case SQL_SPECIAL_CHARACTERS:
			case SQL_TABLE_TERM:
			//case SQL_USER_NAME: This is returning nothing and will return SQL_SUCCESS.
			case SQL_XOPEN_CLI_YEAR:
				if(!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLGetInfo")){
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
					LogAllErrors(henv,hdbc,hstmt);
				break;

			// if not character, assume numeric return values
			default:
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetInfo")){
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				break;
		}
		TESTCASE_END;
	}
	
	// Testing with ConnectionHandle set to NULL
	for (i = 0; i < TotalOptions; i++){
		_stprintf(Heading,_T("Test SQLGetInfo(%s) with ConnectionHandle set to NULL.\n"),
			InfoTypeToChar(ExpectedResults[i].InfoType, TempString));
		TESTCASE_BEGINW(Heading);
		
		if(SQL_DRIVER_HSTMT==ExpectedResults[i].InfoType){
			u1.intInfoValue=(unsigned long)hstmt;
		}

		returncode = SQLGetInfo((SQLHANDLE)NULL,ExpectedResults[i].InfoType,u1.charInfoValue,
			(SWORD)sizeof(u1.charInfoValue),&pcbInfoValue);
		if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLGetInfo")){
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;
	}

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => MX specific SQLGetInfo.\n"));
	TEST_RETURN;
}

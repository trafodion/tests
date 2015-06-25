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
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/timeb.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define NAME_LEN 300

#define MAX_PartialYYTO 12
#define MAX_PartialMMTO 11
#define MAX_PartialDDTO 10
#define MAX_PartialHHTO  9
#define MAX_PartialMNTO  8
#define MAX_PartialSSTO  7

PassFail TestMXPartialDateTimeInputConversions(TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	TCHAR				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	int				i, j, TS_iteration;
	int				loop_bindparam;
	SQLSMALLINT	ParamType = SQL_PARAM_INPUT;

	
	
	
	struct // SQL field types for Datetime "Year To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialYYTO];
		TCHAR		*TestSQLType[MAX_PartialYYTO];
		SQLUINTEGER	ColPrec[MAX_PartialYYTO];
		SQLSMALLINT	ColScale[MAX_PartialYYTO];
	} CDataArgYYTO = {
			 SQL_DATE,SQL_DATE,SQL_DATE,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			_T("SQL_DATE"),_T("SQL_DATE"),_T("SQL_DATE"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),
		 	0,0,0,26,26,26,26,26,26,26,26,26,
			0,0,0,6,6,6,6,6,6,6,6,6};

	struct // SQL field types for Datetime "Month To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialMMTO];
		TCHAR		*TestSQLType[MAX_PartialMMTO];
		SQLUINTEGER	ColPrec[MAX_PartialMMTO];
		SQLSMALLINT	ColScale[MAX_PartialMMTO];
	} CDataArgMMTO = {
			 SQL_DATE,SQL_DATE,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			_T("SQL_DATE"),_T("SQL_DATE"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),
		 	0,0,26,26,26,26,26,26,26,26,26,
			0,0,6,6,6,6,6,6,6,6,6};

	struct // SQL field types for Datetime "Day To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialDDTO];
		TCHAR		*TestSQLType[MAX_PartialDDTO];
		SQLUINTEGER	ColPrec[MAX_PartialDDTO];
		SQLSMALLINT	ColScale[MAX_PartialDDTO];
	} CDataArgDDTO = {
			 SQL_DATE,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			_T("SQL_DATE"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),
		 	0,26,26,26,26,26,26,26,26,26,
			0,6,6,6,6,6,6,6,6,6};

	struct // SQL field types for Datetime "Hour To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialHHTO];
		TCHAR		*TestSQLType[MAX_PartialHHTO];
		SQLUINTEGER	ColPrec[MAX_PartialHHTO];
		SQLSMALLINT	ColScale[MAX_PartialHHTO];
	} CDataArgHHTO = {
			 SQL_TIME,SQL_TIME,SQL_TIME,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			_T("SQL_TIME"),_T("SQL_TIME"),_T("SQL_TIME"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),
		 	0,0,0,26,26,26,26,26,26,
			0,0,0,6,6,6,6,6,6};

	struct // SQL field types for Datetime "Minute To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialMNTO];
		TCHAR		*TestSQLType[MAX_PartialMNTO];
		SQLUINTEGER	ColPrec[MAX_PartialMNTO];
		SQLSMALLINT	ColScale[MAX_PartialMNTO];
	} CDataArgMNTO = {
			SQL_TIME,SQL_TIME,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			_T("SQL_TIME"),_T("SQL_TIME"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),
		 	0,0,26,26,26,26,26,26,
			0,0,6,6,6,6,6,6};
			
	struct // SQL field types for Datetime "Second To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialSSTO];
		TCHAR		*TestSQLType[MAX_PartialSSTO];
		SQLUINTEGER	ColPrec[MAX_PartialSSTO];
		SQLSMALLINT	ColScale[MAX_PartialSSTO];
	} CDataArgSSTO = {
			SQL_TIME,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			_T("SQL_TIME"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),_T("SQL_TIMESTAMP"),
		 	0,26,26,26,26,26,26,
			0,6,6,6,6,6,6};		 
			 
			 
			 
	struct
	{
		short int	year;
		unsigned short int	month;
		unsigned short int	day;
	} CDATETOSQL = {1997,10,12};

	struct
	{
		unsigned short int	hour;
		unsigned short int	minute;
		unsigned short int	second;

	} CTIMETOSQL = {11,33,41};

	struct
	{
		short int	year;
		unsigned short int	month;
		unsigned short int	day;
		unsigned short int	hour;
		unsigned short int	minute;
		unsigned short int	second;
		unsigned long int	fraction;
	} CTIMESTAMPTOSQL = {1997,10,12,11,33,41,123456};



	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		InputValue[MAX_PartialYYTO][35];
		TCHAR		OutputValue[MAX_PartialYYTO][35];
	} CDataValueYYTO[6] = {
#ifndef unixcli
	  	{SQL_C_TCHAR,
		_T("SQL_C_TCHAR"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997"),_T("1997-10"),_T("1997-10-12"),_T("1997-10-12 11"),_T("1997-10-12 11:33"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.1"),_T("1997-10-12 11:33:41.12"),_T("1997-10-12 11:33:41.123"),_T("1997-10-12 11:33:41.1234"),_T("1997-10-12 11:33:41.12345"),_T("1997-10-12 11:33:41.123456"),
		},
		{SQL_C_DATE,
		_T("SQL_C_DATE"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997"),_T("1997-10"),_T("1997-10-12"),_T("1997-10-12 00"),_T("1997-10-12 00:00"),_T("1997-10-12 00:00:00"),_T("1997-10-12 00:00:00.0"),_T("1997-10-12 00:00:00.00"),_T("1997-10-12 00:00:00.000"),_T("1997-10-12 00:00:00.0000"),_T("1997-10-12 00:00:00.00000"),_T("1997-10-12 00:00:00.000000"),
		},
		{SQL_C_TIME,
		_T("SQL_C_TIME"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997"),_T("1997-10"),_T("1997-10-12"),_T("1997-10-12 11"),_T("1997-10-12 11:33"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.0"),_T("1997-10-12 11:33:41.00"),_T("1997-10-12 11:33:41.000"),_T("1997-10-12 11:33:41.0000"),_T("1997-10-12 11:33:41.00000"),_T("1997-10-12 11:33:41.000000"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997"),_T("1997-10"),_T("1997-10-12"),_T("1997-10-12 11"),_T("1997-10-12 11:33"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.3"),_T("1997-10-12 11:33:41.23"),_T("1997-10-12 11:33:41.123"),_T("1997-10-12 11:33:41.0123"),_T("1997-10-12 11:33:41.00123"),_T("1997-10-12 11:33:41.000123"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997"),_T("1997-10"),_T("1997-10-12"),_T("1997-10-12 11"),_T("1997-10-12 11:33"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997"),_T("1997-10"),_T("1997-10-12"),_T("1997-10-12 11"),_T("1997-10-12 11:33"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.3"),_T("1997-10-12 11:33:41.23"),_T("1997-10-12 11:33:41.123"),_T("1997-10-12 11:33:41.0123"),_T("1997-10-12 11:33:41.00123"),_T("1997-10-12 11:33:41.000123"),
		},
		
		{999,}
#endif
		};

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		InputValue[MAX_PartialMMTO][35];
		TCHAR		OutputValue[MAX_PartialMMTO][35];
	} CDataValueMMTO[6] = {
#ifndef unixcli
		{SQL_C_TCHAR,
		_T("SQL_C_TCHAR"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("10"),_T("10-12"),_T("10-12 11"),_T("10-12 11:33"),_T("10-12 11:33:41"),_T("10-12 11:33:41.1"),_T("10-12 11:33:41.12"),_T("10-12 11:33:41.123"),_T("10-12 11:33:41.1234"),_T("10-12 11:33:41.12345"),_T("10-12 11:33:41.123456"),
		},
		{SQL_C_DATE,
		_T("SQL_C_DATE"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("10"),_T("10-12"),_T("10-12 00"),_T("10-12 00:00"),_T("10-12 00:00:00"),_T("10-12 00:00:00.0"),_T("10-12 00:00:00.00"),_T("10-12 00:00:00.000"),_T("10-12 00:00:00.0000"),_T("10-12 00:00:00.00000"),_T("10-12 00:00:00.000000"),
		},
		{SQL_C_TIME,
		_T("SQL_C_TIME"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("10"),_T("10-12"),_T("10-12 11"),_T("10-12 11:33"),_T("10-12 11:33:41"),_T("10-12 11:33:41.0"),_T("10-12 11:33:41.00"),_T("10-12 11:33:41.000"),_T("10-12 11:33:41.0000"),_T("10-12 11:33:41.00000"),_T("10-12 11:33:41.000000"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("10"),_T("10-12"),_T("10-12 11"),_T("10-12 11:33"),_T("10-12 11:33:41"),_T("10-12 11:33:41.3"),_T("10-12 11:33:41.23"),_T("10-12 11:33:41.123"),_T("10-12 11:33:41.0123"),_T("10-12 11:33:41.00123"),_T("10-12 11:33:41.000123"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("10"),_T("10-12"),_T("10-12 11"),_T("10-12 11:33"),_T("10-12 11:33:41"),_T("10-12 11:33:41.3"),_T("10-12 11:33:41.23"),_T("10-12 11:33:41.123"),_T("10-12 11:33:41.0123"),_T("10-12 11:33:41.00123"),_T("10-12 11:33:41.000123"),
		},
		{999,}
#endif
		};

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		InputValue[MAX_PartialDDTO][35];
		TCHAR		OutputValue[MAX_PartialDDTO][35];
	} CDataValueDDTO[6] = {
#ifndef unixcli
		{SQL_C_TCHAR,
		_T("SQL_C_TCHAR"),
		_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("12"),_T("12 11"),_T("12 11:33"),_T("12 11:33:41"),_T("12 11:33:41.1"),_T("12 11:33:41.12"),_T("12 11:33:41.123"),_T("12 11:33:41.1234"),_T("12 11:33:41.12345"),_T("12 11:33:41.123456"),
		},
		{SQL_C_DATE,
		_T("SQL_C_DATE"),
		_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("12"),_T("12 00"),_T("12 00:00"),_T("12 00:00:00"),_T("12 00:00:00.0"),_T("12 00:00:00.00"),_T("12 00:00:00.000"),_T("12 00:00:00.0000"),_T("12 00:00:00.00000"),_T("12 00:00:00.000000"),
		},
		{SQL_C_TIME,
		_T("SQL_C_TIME"),
		_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("12"),_T("12 11"),_T("12 11:33"),_T("12 11:33:41"),_T("12 11:33:41.0"),_T("12 11:33:41.00"),_T("12 11:33:41.000"),_T("12 11:33:41.0000"),_T("12 11:33:41.00000"),_T("12 11:33:41.000000"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("12"),_T("12 11"),_T("12 11:33"),_T("12 11:33:41"),_T("12 11:33:41.3"),_T("12 11:33:41.23"),_T("12 11:33:41.123"),_T("12 11:33:41.0123"),_T("12 11:33:41.00123"),_T("12 11:33:41.000123"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("12"),_T("12 11"),_T("12 11:33"),_T("12 11:33:41"),_T("12 11:33:41.3"),_T("12 11:33:41.23"),_T("12 11:33:41.123"),_T("12 11:33:41.0123"),_T("12 11:33:41.00123"),_T("12 11:33:41.000123"),
		},
		{999,}
#endif
		};

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		InputValue[MAX_PartialHHTO][35];
		TCHAR		OutputValue[MAX_PartialHHTO][35];
	} CDataValueHHTO[6] = {
#ifndef unixcli
		{SQL_C_TCHAR,
		_T("SQL_C_TCHAR"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("11"),_T("11:33"),_T("11:33:41"),_T("11:33:41.1"),_T("11:33:41.12"),_T("11:33:41.123"),_T("11:33:41.1234"),_T("11:33:41.12345"),_T("11:33:41.123456"),
		},
		{SQL_C_TIME,
		_T("SQL_C_TIME"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("11"),_T("11:33"),_T("11:33:41"),_T("11:33:41.0"),_T("11:33:41.00"),_T("11:33:41.000"),_T("11:33:41.0000"),_T("11:33:41.00000"),_T("11:33:41.000000"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("11"),_T("11:33"),_T("11:33:41"),_T("11:33:41.3"),_T("11:33:41.23"),_T("11:33:41.123"),_T("11:33:41.0123"),_T("11:33:41.00123"),_T("11:33:41.000123"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("11"),_T("11:33"),_T("11:33:41"),_T("11:33:41.3"),_T("11:33:41.23"),_T("11:33:41.123"),_T("11:33:41.0123"),_T("11:33:41.00123"),_T("11:33:41.000123"),
		},
		{999,}
#endif
		};

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		InputValue[MAX_PartialMNTO][35];
		TCHAR		OutputValue[MAX_PartialMNTO][35];
	} CDataValueMNTO[5] = {
#ifndef unixcli
		{SQL_C_TCHAR,
		_T("SQL_C_TCHAR"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("33"),_T("33:41"),_T("33:41.1"),_T("33:41.12"),_T("33:41.123"),_T("33:41.1234"),_T("33:41.12345"),_T("33:41.123456"),
		},
		{SQL_C_TIME,
		_T("SQL_C_TIME"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("33"),_T("33:41"),_T("33:41.0"),_T("33:41.00"),_T("33:41.000"),_T("33:41.0000"),_T("33:41.00000"),_T("33:41.000000"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("33"),_T("33:41"),_T("33:41.3"),_T("33:41.23"),_T("33:41.123"),_T("33:41.0123"),_T("33:41.00123"),_T("33:41.000123"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("33"),_T("33:41"),_T("33:41.3"),_T("33:41.23"),_T("33:41.123"),_T("33:41.0123"),_T("33:41.00123"),_T("33:41.000123"),
		},
		{999,}
#endif
		};

	struct
	{
		SQLSMALLINT	CType;
		TCHAR		*TestCType;
		TCHAR		InputValue[MAX_PartialSSTO][35];
		TCHAR		OutputValue[MAX_PartialSSTO][35];
	} CDataValueSSTO[5] = {
#ifndef unixcli
		{SQL_C_TCHAR,
		_T("SQL_C_TCHAR"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("41"),_T("41.1"),_T("41.12"),_T("41.123"),_T("41.1234"),_T("41.12345"),_T("41.123456"),
		},
		{SQL_C_TIME,
		_T("SQL_C_TIME"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("41"),_T("41.0"),_T("41.00"),_T("41.000"),_T("41.0000"),_T("41.00000"),_T("41.000000"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("41"),_T("41.3"),_T("41.23"),_T("41.123"),_T("41.0123"),_T("41.00123"),_T("41.000123"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("41"),_T("41.3"),_T("41.23"),_T("41.123"),_T("41.0123"),_T("41.00123"),_T("41.000123"),
		},
		{999,}
#endif
		};

	//YYTO...
	TCHAR	*DrpTabYYTO = _T("DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLYYTO");
	TCHAR	*DelTabYYTO = _T("DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLYYTO");
	TCHAR	*CrtTabYYTO = _T("CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLYYTO(C1 DATETIME YEAR ,C2 DATETIME YEAR TO MONTH,C3 DATETIME YEAR TO DAY,C4 DATETIME YEAR TO HOUR,C5 DATETIME YEAR TO MINUTE,C6 DATETIME YEAR TO SECOND,C7 DATETIME YEAR TO FRACTION(1),C8 DATETIME YEAR TO FRACTION(2),C9 DATETIME YEAR TO FRACTION(3),C10 DATETIME YEAR TO FRACTION(4),C11 DATETIME YEAR TO FRACTION(5), C12 DATETIME YEAR TO FRACTION(6))");
	TCHAR	*InsTabYYTO = _T("INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLYYTO(C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)");
	TCHAR	*SelTabYYTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12 FROM TRAFODION.ODBC_SCHEMA.CSQLYYTO");
	
	//MMTO...
	TCHAR	*DrpTabMMTO = _T("DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLMMTO");
	TCHAR	*DelTabMMTO = _T("DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLMMTO");
	TCHAR	*CrtTabMMTO = _T("CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLMMTO(C1 DATETIME MONTH,C2 DATETIME MONTH TO DAY,C3 DATETIME MONTH TO HOUR,C4 DATETIME MONTH TO MINUTE,C5 DATETIME MONTH TO SECOND,C6 DATETIME MONTH TO FRACTION(1),C7 DATETIME MONTH TO FRACTION(2),C8 DATETIME MONTH TO FRACTION(3),C9 DATETIME MONTH TO FRACTION(4),C10 DATETIME MONTH TO FRACTION(5), C11 DATETIME MONTH TO FRACTION(6))");
	TCHAR	*InsTabMMTO = _T("INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLMMTO(C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11) VALUES (?,?,?,?,?,?,?,?,?,?,?)");
	TCHAR	*SelTabMMTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11 FROM TRAFODION.ODBC_SCHEMA.CSQLMMTO");
	
	//DDTO...
	TCHAR	*DrpTabDDTO = _T("DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLDDTO");
	TCHAR	*DelTabDDTO = _T("DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLDDTO");
	TCHAR	*CrtTabDDTO = _T("CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLDDTO(C1 DATETIME DAY,C2 DATETIME DAY TO HOUR,C3 DATETIME DAY TO MINUTE,C4 DATETIME DAY TO SECOND,C5 DATETIME DAY TO FRACTION(1),C6 DATETIME DAY TO FRACTION(2),C7 DATETIME DAY TO FRACTION(3),C8 DATETIME DAY TO FRACTION(4),C9 DATETIME DAY TO FRACTION(5), C10 DATETIME DAY TO FRACTION(6))");
	TCHAR	*InsTabDDTO = _T("INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLDDTO(C1,C2,C3,C4,C5,C6,C7,C8,C9,C10) VALUES (?,?,?,?,?,?,?,?,?,?)");	
	TCHAR	*SelTabDDTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10 FROM TRAFODION.ODBC_SCHEMA.CSQLDDTO");
	
	//HHTO...
	TCHAR	*DrpTabHHTO = _T("DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLHHTO");
	TCHAR	*DelTabHHTO = _T("DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLHHTO");
	TCHAR	*CrtTabHHTO = _T("CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLHHTO(C1 DATETIME HOUR,C2 DATETIME HOUR TO MINUTE,C3 DATETIME HOUR TO SECOND,C4 DATETIME HOUR TO FRACTION(1),C5 DATETIME HOUR TO FRACTION(2),C6 DATETIME HOUR TO FRACTION(3),C7 DATETIME HOUR TO FRACTION(4),C8 DATETIME HOUR TO FRACTION(5), C9 DATETIME HOUR TO FRACTION(6))");
	TCHAR	*InsTabHHTO = _T("INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLHHTO(C1,C2,C3,C4,C5,C6,C7,C8,C9) VALUES (?,?,?,?,?,?,?,?,?)");
	TCHAR	*SelTabHHTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9 FROM TRAFODION.ODBC_SCHEMA.CSQLHHTO");
	
	//MNTO...
	TCHAR	*DrpTabMNTO = _T("DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLMNTO");
	TCHAR	*DelTabMNTO = _T("DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLMNTO");
	TCHAR	*CrtTabMNTO = _T("CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLMNTO(C1 DATETIME MINUTE,C2 DATETIME MINUTE TO SECOND,C3 DATETIME MINUTE TO FRACTION(1),C4 DATETIME MINUTE TO FRACTION(2),C5 DATETIME MINUTE TO FRACTION(3),C6 DATETIME MINUTE TO FRACTION(4),C7 DATETIME MINUTE TO FRACTION(5), C8 DATETIME MINUTE TO FRACTION(6))");
	TCHAR	*InsTabMNTO = _T("INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLMNTO(C1,C2,C3,C4,C5,C6,C7,C8) VALUES (?,?,?,?,?,?,?,?)");
	TCHAR	*SelTabMNTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8 FROM TRAFODION.ODBC_SCHEMA.CSQLMNTO");
	
	//SSTO...
	TCHAR	*DrpTabSSTO = _T("DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLSSTO");
	TCHAR	*DelTabSSTO = _T("DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLSSTO");
	TCHAR	*CrtTabSSTO = _T("CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLSSTO(C1 DATETIME SECOND,C2 DATETIME SECOND TO FRACTION(1),C3 DATETIME SECOND TO FRACTION(2),C4 DATETIME SECOND TO FRACTION(3),C5 DATETIME SECOND TO FRACTION(4),C6 DATETIME SECOND TO FRACTION(5), C7 DATETIME SECOND TO FRACTION(6))");
	TCHAR	*InsTabSSTO = _T("INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLSSTO(C1,C2,C3,C4,C5,C6,C7) VALUES (?,?,?,?,?,?,?)");
	TCHAR	*SelTabSSTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7 FROM TRAFODION.ODBC_SCHEMA.CSQLSSTO");
	

	SQLLEN			InValue = SQL_NTS;
	TCHAR			OutValue[NAME_LEN];
	SQLLEN		OutValueLen;
	time_t now;
	struct tm *timeArray;
	static TCHAR dateBuffer[12];
	TCHAR	State[STATE_SIZE];
	SDWORD	NativeError;
	TCHAR	buf[MAX_STRING_SIZE];
	

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing => Partial DateTime Input Conversions.\n"));
	LogMsg(NONE, _T(""));
	TEST_INIT;

	TESTCASE_BEGIN("Connection for partial datetime input conversion tests\n");

	if(!FullConnect(pTestInfo)){
		LogMsg(NONE,_T("Unable to connect\n"));
//		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
//		TEST_FAILED;
		TEST_RETURN;
	}
//	TESTCASE_END; 

	//set up the current date
	now=time(NULL);
	timeArray = localtime(&now);
	_tcsftime (dateBuffer,12,_T("%Y-%m-%d"),timeArray);

//====================================================================================================
// converting from YYTO
	
				
	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table:\n %s.\n"),CrtTabYYTO);
		TESTCASE_BEGINW(Heading);
	
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabYYTO,SQL_NTS);				//RS: Create/drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabYYTO,SQL_NTS);
		if(returncode != SQL_SUCCESS)
		{
			returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, hstmt, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
			if (NativeError == -3195)
			{
				LogMsg(NONE, _T("DATETIME datatype not supported\n"));
				_gTestCount--;
				FullDisconnect(pTestInfo);
				LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing => Partial DateTime Input Conversions.\n"));
			}
			else
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TEST_RETURN;
		}
		/*
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLTCHAR*) DelTabYYTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueYYTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueYYTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTabYYTO,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END;
			}

			for (j = 0; j < MAX_PartialYYTO; j++)
			
			{
				_stprintf(Heading,_T("Set up SQLBindParameter to convert from %s to %s\n"),CDataValueYYTO[i].TestCType, CDataArgYYTO.TestSQLType[j]);
				TESTCASE_BEGINW(Heading);

                switch (CDataValueYYTO[i].CType)
				{
					case SQL_C_TCHAR:
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueYYTO[i].CType,
									CDataArgYYTO.SQLType[j],CDataArgYYTO.ColPrec[j],
									CDataArgYYTO.ColScale[j],CDataValueYYTO[i].InputValue[j],NAME_LEN,&InValue);
									
									
						break;

					case SQL_C_DATE:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueYYTO[i].CType,
									CDataArgYYTO.SQLType[j],CDataArgYYTO.ColPrec[j],
									CDataArgYYTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
									
									
						break;

					case SQL_C_TIME:
						if (CDataArgYYTO.SQLType[j]==SQL_DATE) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_DATE,
									CDataArgYYTO.SQLType[j],CDataArgYYTO.ColPrec[j],
									CDataArgYYTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueYYTO[i].CType,
									CDataArgYYTO.SQLType[j],CDataArgYYTO.ColPrec[j],
									CDataArgYYTO.ColScale[j],&CTIMETOSQL,NAME_LEN,&InValue);
						};
						
					// Since we are giving only time as input the current date is inserted for date part. 
					// Hence we will change the date part of expected output to current date.
						if ( j > 2) 
						{	_tcsncpy(CDataValueYYTO[i].OutputValue[j],dateBuffer,10);
								
						}
					
						break;

					case SQL_C_TIMESTAMP:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueYYTO[i].CType,
									CDataArgYYTO.SQLType[j],CDataArgYYTO.ColPrec[j],
									CDataArgYYTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
									
						break;

					case SQL_C_DEFAULT:
						if (CDataArgYYTO.SQLType[j]==SQL_DATE) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueYYTO[i].CType,
									CDataArgYYTO.SQLType[j],CDataArgYYTO.ColPrec[j],
									CDataArgYYTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueYYTO[i].CType,
									CDataArgYYTO.SQLType[j],CDataArgYYTO.ColPrec[j],
									CDataArgYYTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
						};
						break;

		
					default: ;
				}

				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueYYTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueYYTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabYYTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				_stprintf(Heading,_T("Setup for checking SQLBindParameter tests %s.\n"),CDataValueYYTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabYYTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_PartialYYTO; j++)
						{
							//LogMsg(NONE,_T("SQLBindParameter test: checking data for column c%d\n"),j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueYYTO[i].OutputValue[j],OutValue,_tcslen(CDataValueYYTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueYYTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueYYTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			_stprintf(Heading,_T("Setup for SQLBindParameter tests for delete table %s.\n"),CDataValueYYTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTabYYTO,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END;
			i++;
			
 			
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabYYTO,SQL_NTS);


//=================================================================================================================
//====================================================================================================
// converting from MMTO

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table:\n %s.\n"),CrtTabMMTO);
		TESTCASE_BEGINW(Heading);

/*		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMMTO,SQL_NTS);				// RS: Create/drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabMMTO,SQL_NTS);
		
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLTCHAR*) DelTabMMTO,SQL_NTS);				// RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueMMTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueMMTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTabMMTO,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END;
			}

			for (j = 0; j < MAX_PartialMMTO; j++)
			
			{
				_stprintf(Heading,_T("Set up SQLBindParameter to convert from %s to %s\n"),CDataValueMMTO[i].TestCType, CDataArgMMTO.TestSQLType[j]);
				TESTCASE_BEGINW(Heading);
				

				switch (CDataValueMMTO[i].CType)
				{
					case SQL_C_TCHAR:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMMTO[i].CType,
									CDataArgMMTO.SQLType[j],CDataArgMMTO.ColPrec[j],
									CDataArgMMTO.ColScale[j],CDataValueMMTO[i].InputValue[j],NAME_LEN,&InValue);
									
									
						break;
					case SQL_C_DATE:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMMTO[i].CType,
									CDataArgMMTO.SQLType[j],CDataArgMMTO.ColPrec[j],
									CDataArgMMTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
									
									
						break;
					case SQL_C_TIME:
						if (CDataArgMMTO.SQLType[j]==SQL_DATE) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_DATE,
									CDataArgMMTO.SQLType[j],CDataArgMMTO.ColPrec[j],
									CDataArgMMTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMMTO[i].CType,
									CDataArgMMTO.SQLType[j],CDataArgMMTO.ColPrec[j],
									CDataArgMMTO.ColScale[j],&CTIMETOSQL,NAME_LEN,&InValue);
						};
						// Since we are giving only time as input the current date is inserted for date part. 
						// Hence we will change the date part of expected output to current date.
						if ( j > 1) 
						{	_tcsncpy(CDataValueMMTO[i].OutputValue[j],&dateBuffer[5],5);
								
						}
						break;
					case SQL_C_TIMESTAMP:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMMTO[i].CType,
									CDataArgMMTO.SQLType[j],CDataArgMMTO.ColPrec[j],
									CDataArgMMTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
									
									
						break;
		
					case SQL_C_DEFAULT:
						if (CDataArgMMTO.SQLType[j]==SQL_DATE) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMMTO[i].CType,
									CDataArgMMTO.SQLType[j],CDataArgMMTO.ColPrec[j],
									CDataArgMMTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMMTO[i].CType,
									CDataArgMMTO.SQLType[j],CDataArgMMTO.ColPrec[j],
									CDataArgMMTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
						};
						break;
					default: ;
				}

				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueMMTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueMMTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabMMTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				_stprintf(Heading,_T("Setup for checking SQLBindParameter tests %s.\n"),CDataValueMMTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabMMTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_PartialMMTO; j++)
						{
							//LogMsg(NONE,_T("SQLBindParameter test: checking data for column c%d\n"),j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueMMTO[i].OutputValue[j],OutValue,_tcslen(CDataValueMMTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMMTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMMTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			_stprintf(Heading,_T("Setup for SQLBindParameter tests for delete table %s.\n"),CDataValueMMTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTabMMTO,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END;
			i++;
			
 			
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMMTO,SQL_NTS);

//=================================================================================================================
//====================================================================================================
// converting from DDTO

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table:\n %s.\n"),CrtTabDDTO);
		TESTCASE_BEGINW(Heading);

/*		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDDTO,SQL_NTS);				// RS: Create/drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabDDTO,SQL_NTS);
		
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLTCHAR*) DelTabDDTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueDDTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueDDTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTabDDTO,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END;
			}

			for (j = 0; j < MAX_PartialDDTO; j++)
			
			{
				_stprintf(Heading,_T("Set up SQLBindParameter to convert from %s to %s\n"),CDataValueDDTO[i].TestCType, CDataArgDDTO.TestSQLType[j]);
				TESTCASE_BEGINW(Heading);
				
				switch (CDataValueDDTO[i].CType)
				{
					case SQL_C_TCHAR:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueDDTO[i].CType,
									CDataArgDDTO.SQLType[j],CDataArgDDTO.ColPrec[j],
									CDataArgDDTO.ColScale[j],CDataValueDDTO[i].InputValue[j],NAME_LEN,&InValue);
									
									
						break;
					case SQL_C_DATE:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueDDTO[i].CType,
									CDataArgDDTO.SQLType[j],CDataArgDDTO.ColPrec[j],
									CDataArgDDTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
									
									
						break;
					case SQL_C_TIME:
						if (CDataArgDDTO.SQLType[j]==SQL_DATE) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_DATE,
									CDataArgDDTO.SQLType[j],CDataArgDDTO.ColPrec[j],
									CDataArgDDTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueDDTO[i].CType,
									CDataArgDDTO.SQLType[j],CDataArgDDTO.ColPrec[j],
									CDataArgDDTO.ColScale[j],&CTIMETOSQL,NAME_LEN,&InValue);
						};
						// Since we are giving only time as input the current date is inserted for date part. 
						// Hence we will change the date part of expected output to current date.
						if ( j > 0) 
						{	_tcsncpy(CDataValueDDTO[i].OutputValue[j],&dateBuffer[8],2);
								
						}
						break;
					case SQL_C_TIMESTAMP:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueDDTO[i].CType,
									CDataArgDDTO.SQLType[j],CDataArgDDTO.ColPrec[j],
									CDataArgDDTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
									
									
						break;
		
					case SQL_C_DEFAULT:
						if (CDataArgDDTO.SQLType[j]==SQL_DATE) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueDDTO[i].CType,
									CDataArgDDTO.SQLType[j],CDataArgDDTO.ColPrec[j],
									CDataArgDDTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueDDTO[i].CType,
									CDataArgDDTO.SQLType[j],CDataArgDDTO.ColPrec[j],
									CDataArgDDTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
						};
						break;
					default: ;
				}

				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueDDTO[i].TestCType);
				TESTCASE_BEGINW(Heading);

				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueDDTO[i].TestCType);
				TESTCASE_BEGINW(Heading);

				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabDDTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				_stprintf(Heading,_T("Setup for checking SQLBindParameter tests %s.\n"),CDataValueDDTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabDDTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_PartialDDTO; j++)
						{
							//LogMsg(NONE,_T("SQLBindParameter test: checking data for column c%d\n"),j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueDDTO[i].OutputValue[j],OutValue,_tcslen(CDataValueDDTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueDDTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueDDTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			_stprintf(Heading,_T("Setup for SQLBindParameter tests for delete table %s.\n"),CDataValueDDTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTabDDTO,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END;
			i++;
			
 			
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDDTO,SQL_NTS);

//=================================================================================================================
//====================================================================================================
// converting from HHTO

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table:\n %s.\n"),CrtTabHHTO);
		TESTCASE_BEGINW(Heading);
		
/*		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabHHTO,SQL_NTS);				//RS: Create/drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabHHTO,SQL_NTS);
		
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLTCHAR*) DelTabHHTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueHHTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueHHTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
								
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTabHHTO,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END;
			}

			for (j = 0; j < MAX_PartialHHTO; j++)
			
			{
				_stprintf(Heading,_T("Set up SQLBindParameter to convert from %s to %s\n"),CDataValueHHTO[i].TestCType, CDataArgHHTO.TestSQLType[j]);
				TESTCASE_BEGINW(Heading);
								
				switch (CDataValueHHTO[i].CType)
				{
					case SQL_C_TCHAR:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueHHTO[i].CType,
									CDataArgHHTO.SQLType[j],CDataArgHHTO.ColPrec[j],
									CDataArgHHTO.ColScale[j],CDataValueHHTO[i].InputValue[j],NAME_LEN,&InValue);
									
									
						break;
				
					case SQL_C_TIME:
						if (CDataArgHHTO.SQLType[j]==SQL_DATE) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_DATE,
									CDataArgHHTO.SQLType[j],CDataArgHHTO.ColPrec[j],
									CDataArgHHTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueHHTO[i].CType,
									CDataArgHHTO.SQLType[j],CDataArgHHTO.ColPrec[j],
									CDataArgHHTO.ColScale[j],&CTIMETOSQL,NAME_LEN,&InValue);
						};
						
						break;
					case SQL_C_TIMESTAMP:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueHHTO[i].CType,
									CDataArgHHTO.SQLType[j],CDataArgHHTO.ColPrec[j],
									CDataArgHHTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
									
									
						break;
		
					case SQL_C_DEFAULT:
						if (CDataArgHHTO.SQLType[j]==SQL_TIME) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueHHTO[i].CType,
									CDataArgHHTO.SQLType[j],CDataArgHHTO.ColPrec[j],
									CDataArgHHTO.ColScale[j],&CTIMETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueHHTO[i].CType,
									CDataArgHHTO.SQLType[j],CDataArgHHTO.ColPrec[j],
									CDataArgHHTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
						};
						break;
					default: ;
				}

				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueHHTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueHHTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabHHTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				_stprintf(Heading,_T("Setup for checking SQLBindParameter tests %s.\n"),CDataValueHHTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabHHTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_PartialHHTO; j++)
						{
							//LogMsg(NONE,_T("SQLBindParameter test: checking data for column c%d\n"),j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueHHTO[i].OutputValue[j],OutValue,_tcslen(CDataValueHHTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueHHTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueHHTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			_stprintf(Heading,_T("Setup for SQLBindParameter tests for delete table %s.\n"),CDataValueHHTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTabHHTO,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END;
			i++;
			
 			
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabHHTO,SQL_NTS);

//=================================================================================================================
//====================================================================================================
// converting from MNTO

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table:\n %s.\n"),CrtTabMNTO);
		TESTCASE_BEGINW(Heading);
		
		
/*		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMNTO,SQL_NTS);				// RS: Create/drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabMNTO,SQL_NTS);
		
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLTCHAR*) DelTabMNTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueMNTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueMNTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTabMNTO,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END;
			}

			for (j = 0; j < MAX_PartialMNTO; j++)
			
			{
				_stprintf(Heading,_T("Set up SQLBindParameter to convert from %s to %s\n"),CDataValueMNTO[i].TestCType, CDataArgMNTO.TestSQLType[j]);
				TESTCASE_BEGINW(Heading);
				
				
				switch (CDataValueMNTO[i].CType)
				{
					case SQL_C_TCHAR:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMNTO[i].CType,
									CDataArgMNTO.SQLType[j],CDataArgMNTO.ColPrec[j],
									CDataArgMNTO.ColScale[j],CDataValueMNTO[i].InputValue[j],NAME_LEN,&InValue);
									
									
						break;
				
					case SQL_C_TIME:
						if (CDataArgMNTO.SQLType[j]==SQL_DATE) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_DATE,
									CDataArgMNTO.SQLType[j],CDataArgMNTO.ColPrec[j],
									CDataArgMNTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMNTO[i].CType,
									CDataArgMNTO.SQLType[j],CDataArgMNTO.ColPrec[j],
									CDataArgMNTO.ColScale[j],&CTIMETOSQL,NAME_LEN,&InValue);
						};
						
						break;
					case SQL_C_TIMESTAMP:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMNTO[i].CType,
									CDataArgMNTO.SQLType[j],CDataArgMNTO.ColPrec[j],
									CDataArgMNTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
									
									
						break;
					case SQL_C_DEFAULT:
						if (CDataArgMNTO.SQLType[j]==SQL_TIME) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMNTO[i].CType,
									CDataArgMNTO.SQLType[j],CDataArgMNTO.ColPrec[j],
									CDataArgMNTO.ColScale[j],&CTIMETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueMNTO[i].CType,
									CDataArgMNTO.SQLType[j],CDataArgMNTO.ColPrec[j],
									CDataArgMNTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
						};
						break;
					default: ;
				}

				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueMNTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueMNTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabMNTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				_stprintf(Heading,_T("Setup for checking SQLBindParameter tests %s.\n"),CDataValueMNTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabMNTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_PartialMNTO; j++)
						{
							//LogMsg(NONE,_T("SQLBindParameter test: checking data for column c%d\n"),j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueMNTO[i].OutputValue[j],OutValue,_tcslen(CDataValueMNTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMNTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMNTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			_stprintf(Heading,_T("Setup for SQLBindParameter tests for delete table %s.\n"),CDataValueMNTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTabMNTO,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END;
			i++;
			
 			
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMNTO,SQL_NTS);

//=================================================================================================================
//====================================================================================================
// converting from SSTO

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table:\n %s.\n"),CrtTabSSTO);
		TESTCASE_BEGINW(Heading);
		

/*		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabSSTO,SQL_NTS);				// RS: Create/Drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabSSTO,SQL_NTS);
		
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLTCHAR*) DelTabSSTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueSSTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for prepare %s.\n"),CDataValueSSTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTabSSTO,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END;
			}

			for (j = 0; j < MAX_PartialSSTO; j++)
			
			{
				_stprintf(Heading,_T("Set up SQLBindParameter to convert from %s to %s\n"),CDataValueSSTO[i].TestCType, CDataArgSSTO.TestSQLType[j]);
				TESTCASE_BEGINW(Heading);
				
				
				switch (CDataValueSSTO[i].CType)
				{
					case SQL_C_TCHAR:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueSSTO[i].CType,
									CDataArgSSTO.SQLType[j],CDataArgSSTO.ColPrec[j],
									CDataArgSSTO.ColScale[j],CDataValueSSTO[i].InputValue[j],NAME_LEN,&InValue);
									
									
						break;
				
					case SQL_C_TIME:
						if (CDataArgSSTO.SQLType[j]==SQL_DATE) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_DATE,
									CDataArgSSTO.SQLType[j],CDataArgSSTO.ColPrec[j],
									CDataArgSSTO.ColScale[j],&CDATETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueSSTO[i].CType,
									CDataArgSSTO.SQLType[j],CDataArgSSTO.ColPrec[j],
									CDataArgSSTO.ColScale[j],&CTIMETOSQL,NAME_LEN,&InValue);
						};
						
						break;
					case SQL_C_TIMESTAMP:			
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueSSTO[i].CType,
									CDataArgSSTO.SQLType[j],CDataArgSSTO.ColPrec[j],
									CDataArgSSTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
																	
						break;
					case SQL_C_DEFAULT:
						if (CDataArgSSTO.SQLType[j]==SQL_TIME) 
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueSSTO[i].CType,
									CDataArgSSTO.SQLType[j],CDataArgSSTO.ColPrec[j],
									CDataArgSSTO.ColScale[j],&CTIMETOSQL,NAME_LEN,&InValue);
						}
						else
						{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueSSTO[i].CType,
									CDataArgSSTO.SQLType[j],CDataArgSSTO.ColPrec[j],
									CDataArgSSTO.ColScale[j],&CTIMESTAMPTOSQL,NAME_LEN,&InValue);
						};
						break;
					default: ;
				}

				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
		
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for Execute %s.\n"),CDataValueSSTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for SQLBindParameter tests for ExecDirect %s.\n"),CDataValueSSTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabSSTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				_stprintf(Heading,_T("Setup for checking SQLBindParameter tests %s.\n"),CDataValueSSTO[i].TestCType);
				TESTCASE_BEGINW(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabSSTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_PartialSSTO; j++)
						{
							//LogMsg(NONE,_T("SQLBindParameter test: checking data for column c%d\n"),j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_tcsnicmp(CDataValueSSTO[i].OutputValue[j],OutValue,_tcslen(CDataValueSSTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueSSTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueSSTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			_stprintf(Heading,_T("Setup for SQLBindParameter tests for delete table %s.\n"),CDataValueSSTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTabSSTO,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END;
			i++;
			
 			
		}
	}
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabSSTO,SQL_NTS);

//=================================================================================================================

	
	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing => Partial DateTime Input Conversions.\n"));
	TEST_RETURN;
}

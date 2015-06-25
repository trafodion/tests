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

int ConvertTimeToString(SQL_TIME_STRUCT * t, char * strTime)
{
sprintf(strTime, "%d:%d:%d",t->hour,t->minute,t->second);
	return 8;
}

int ConvertDateToString( SQL_DATE_STRUCT * d, char * strDate)
{
	sprintf(strDate, "%d-%d-%d",d->year,d->month,d->day);
	return 8;
}
int ConvertTimestampToString(SQL_TIMESTAMP_STRUCT * ts, char * strTS)
{
	sprintf(strTS, "%d-%.2d-%.2d %d:%d:%d.%u",ts->year,ts->month,ts->day,ts->hour,ts->minute,ts->second,(unsigned int)ts->fraction);
	return 29;
}

PassFail TestMXPartialDateTimeOutputConversions(TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	char				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	int					i, j, k;
	SQLSMALLINT			ParamType = SQL_PARAM_INPUT;
	
	
	struct // SQL field types for Datetime "Year To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialYYTO];
		char		*TestSQLType[MAX_PartialYYTO];
		SQLUINTEGER	ColPrec[MAX_PartialYYTO];
		SQLSMALLINT	ColScale[MAX_PartialYYTO];
	} CDataArgYYTO = {
			 SQL_DATE,SQL_DATE,SQL_DATE,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			"SQL_DATE","SQL_DATE","SQL_DATE","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP",
		 	0,0,0,26,26,26,26,26,26,26,26,26,
			0,0,0,6,6,6,6,6,6,6,6,6};

	struct // SQL field types for Datetime "Month To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialMMTO];
		char		*TestSQLType[MAX_PartialMMTO];
		SQLUINTEGER	ColPrec[MAX_PartialMMTO];
		SQLSMALLINT	ColScale[MAX_PartialMMTO];
	} CDataArgMMTO = {
			 SQL_DATE,SQL_DATE,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			"SQL_DATE","SQL_DATE","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP",
		 	0,0,26,26,26,26,26,26,26,26,26,
			0,0,6,6,6,6,6,6,6,6,6};

	struct // SQL field types for Datetime "Day To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialDDTO];
		char		*TestSQLType[MAX_PartialDDTO];
		SQLUINTEGER	ColPrec[MAX_PartialDDTO];
		SQLSMALLINT	ColScale[MAX_PartialDDTO];
	} CDataArgDDTO = {
			 SQL_DATE,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			"SQL_DATE","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP",
		 	0,26,26,26,26,26,26,26,26,26,
			0,6,6,6,6,6,6,6,6,6};

	struct // SQL field types for Datetime "Hour To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialHHTO];
		char		*TestSQLType[MAX_PartialHHTO];
		SQLUINTEGER	ColPrec[MAX_PartialHHTO];
		SQLSMALLINT	ColScale[MAX_PartialHHTO];
	} CDataArgHHTO = {
			 SQL_TIME,SQL_TIME,SQL_TIME,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			"SQL_TIME","SQL_TIME","SQL_TIME","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP",
		 	0,0,0,26,26,26,26,26,26,
			0,0,0,6,6,6,6,6,6};

	struct // SQL field types for Datetime "Minute To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialMNTO];
		char		*TestSQLType[MAX_PartialMNTO];
		SQLUINTEGER	ColPrec[MAX_PartialMNTO];
		SQLSMALLINT	ColScale[MAX_PartialMNTO];
	} CDataArgMNTO = {
			SQL_TIME,SQL_TIME,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			"SQL_TIME","SQL_TIME","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP",
		 	0,0,26,26,26,26,26,26,
			0,0,6,6,6,6,6,6};
			
	struct // SQL field types for Datetime "Second To..." datatypes
	{
		SQLSMALLINT	SQLType[MAX_PartialSSTO];
		char		*TestSQLType[MAX_PartialSSTO];
		SQLUINTEGER	ColPrec[MAX_PartialSSTO];
		SQLSMALLINT	ColScale[MAX_PartialSSTO];
	} CDataArgSSTO = {
			SQL_TIME,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,SQL_TIMESTAMP,
			"SQL_TIME","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP","SQL_TIMESTAMP",
		 	0,26,26,26,26,26,26,
			0,6,6,6,6,6,6};		 


	struct
	{
		SQLSMALLINT	CType;
		char		*TestCType;
		char		InputValue[MAX_PartialYYTO][35];
		char		OutputValue[MAX_PartialYYTO][35];
	} CDataValueYYTO[] = {
		{SQL_C_CHAR,
		"SQL_C_CHAR",
		"1997-10-12","1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997","1997-10","1997-10-12","1997-10-12 11","1997-10-12 11:33","1997-10-12 11:33:41","1997-10-12 11:33:41.1","1997-10-12 11:33:41.12","1997-10-12 11:33:41.123","1997-10-12 11:33:41.1234","1997-10-12 11:33:41.12345","1997-10-12 11:33:41.123456",
		},
		{SQL_C_DATE,
		"SQL_C_DATE",
		"1997-10-12","1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997-1-1","1997-10-1","1997-10-12","1997-10-12","1997-10-12","1997-10-12","1997-10-12","1997-10-12","1997-10-12","1997-10-12","1997-10-12","1997-10-12",
		},
		{SQL_C_TIME,
		"SQL_C_TIME",
		"1997-10-12","1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997-1-1","1997-10-1","1997-10-12","11:0:0","11:33:0","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12","1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997-01-01 0:0:0.0","1997-10-01 0:0:0.0","1997-10-12 0:0:0.0","1997-10-12 11:0:0.0","1997-10-12 11:33:0.0","1997-10-12 11:33:41.0","1997-10-12 11:33:41.1000","1997-10-12 11:33:41.12000","1997-10-12 11:33:41.123000","1997-10-12 11:33:41.1234000","1997-10-12 11:33:41.12345000","1997-10-12 11:33:41.123456000",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997-10-12","1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997-1-1","1997-10-1","1997-10-12","1997-10-12 11:0:0.0","1997-10-12 11:33:0.0","1997-10-12 11:33:41.0","1997-10-12 11:33:41.1000","1997-10-12 11:33:41.12000","1997-10-12 11:33:41.123000","1997-10-12 11:33:41.1234000","1997-10-12 11:33:41.12345000","1997-10-12 11:33:41.123456000",
		},
		{999,}
		};
	
	char		*CCharOutput[MAX_PartialYYTO];
	SQLLEN	OutputLen1[MAX_PartialYYTO];
	SQL_DATE_STRUCT	CDateOutput[MAX_PartialYYTO];
	SQL_TIMESTAMP_STRUCT	CTimeStampOutput[MAX_PartialYYTO];
	SQL_TIME_STRUCT	CTimeOutput[MAX_PartialYYTO];
	struct
	{
		SQLSMALLINT	CType;
		char		*TestCType;
		char		InputValue[MAX_PartialMMTO][35];
		char		OutputValue[MAX_PartialMMTO][35];
	} CDataValueMMTO[] = {
		{SQL_C_CHAR,
		"SQL_C_CHAR",
		"1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"10","10-12","10-12 11","10-12 11:33","10-12 11:33:41","10-12 11:33:41.1","10-12 11:33:41.12","10-12 11:33:41.123","10-12 11:33:41.1234","10-12 11:33:41.12345","10-12 11:33:41.123456",
		},
		{SQL_C_DATE,
		"SQL_C_DATE",
		"1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1-10-1","1-10-12","1-10-12","1-10-12","1-10-12","1-10-12","1-10-12","1-10-12","1-10-12","1-10-12","1-10-12",
		},
		{SQL_C_TIME,
		"SQL_C_TIME",
		"1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1-10-1","1-10-12","11:0:0","11:33:0","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1-10-01 0:0:0.0","1-10-12 0:0:0.0","1-10-12 11:0:0.0","1-10-12 11:33:0.0","1-10-12 11:33:41.0","1-10-12 11:33:41.1000","1-10-12 11:33:41.12000","1-10-12 11:33:41.123000","1-10-12 11:33:41.1234000","1-10-12 11:33:41.12345000","1-10-12 11:33:41.123456000",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1-10-1","1-10-12","1-10-12 11:0:0.0","1-10-12 11:33:0.0","1-10-12 11:33:41.0","1-10-12 11:33:41.1000","1-10-12 11:33:41.12000","1-10-12 11:33:41.123000","1-10-12 11:33:41.1234000","1-10-12 11:33:41.12345000","1-10-12 11:33:41.123456000",
		},
		{999,}
		};

	struct
	{
		SQLSMALLINT	CType;
		char		*TestCType;
		char		InputValue[MAX_PartialDDTO][35];
		char		OutputValue[MAX_PartialDDTO][35];
	} CDataValueDDTO[] = {
		{SQL_C_CHAR,
		"SQL_C_CHAR",
		"1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"12","12 11","12 11:33","12 11:33:41","12 11:33:41.1","12 11:33:41.12","12 11:33:41.123","12 11:33:41.1234","12 11:33:41.12345","12 11:33:41.123456",
		},
		{SQL_C_DATE,
		"SQL_C_DATE",
		"1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1-1-12","1-1-12","1-1-12","1-1-12","1-1-12","1-1-12","1-1-12","1-1-12","1-1-12","1-1-12",
		},
		{SQL_C_TIME,
		"SQL_C_TIME",
		"1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1-1-12","11:0:0","11:33:0","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1-01-12 0:0:0.0","1-01-12 11:0:0.0","1-01-12 11:33:0.0","1-01-12 11:33:41.0","1-01-12 11:33:41.1000","1-01-12 11:33:41.12000","1-01-12 11:33:41.123000","1-01-12 11:33:41.1234000","1-01-12 11:33:41.12345000","1-01-12 11:33:41.123456000",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1-1-12","1-01-12 11:0:0.0","1-01-12 11:33:0.0","1-01-12 11:33:41.0","1-01-12 11:33:41.1000","1-01-12 11:33:41.12000","1-01-12 11:33:41.123000","1-01-12 11:33:41.1234000","1-01-12 11:33:41.12345000","1-01-12 11:33:41.123456000",
		},
		{999,}
		};

	struct
	{
		SQLSMALLINT	CType;
		char		*TestCType;
		char		InputValue[MAX_PartialHHTO][35];
		char		OutputValue[MAX_PartialHHTO][35];
	} CDataValueHHTO[] = {
		{SQL_C_CHAR,
		"SQL_C_CHAR",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"11","11:33","11:33:41","11:33:41.1","11:33:41.12","11:33:41.123","11:33:41.1234","11:33:41.12345","11:33:41.123456",
		},
		{SQL_C_TIME,
		"SQL_C_TIME",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"11:0:0","11:33:0","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997-10-12 11:0:0.0","1997-10-12 11:33:0.0","1997-10-12 11:33:41.0","1-01-01 11:33:41.1000","1-01-01 11:33:41.12000","1-01-01 11:33:41.123000","1-01-01 11:33:41.1234000","1-01-01 11:33:41.12345000","1-01-01 11:33:41.123456000",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"11:0:0","11:33:0","11:33:41","1-01-01 11:33:41.1000","1-01-01 11:33:41.12000","1-01-01 11:33:41.123000","1-01-01 11:33:41.1234000","1-01-01 11:33:41.12345000","1-01-01 11:33:41.123456000",
		},
		{999,}
		};

	struct
	{
		SQLSMALLINT	CType;
		char		*TestCType;
		char		InputValue[MAX_PartialMNTO][35];
		char		OutputValue[MAX_PartialMNTO][35];
	} CDataValueMNTO[] = {
		{SQL_C_CHAR,
		"SQL_C_CHAR",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"33","33:41","33:41.1","33:41.12","33:41.123","33:41.1234","33:41.12345","33:41.123456",
		},
		{SQL_C_TIME,
		"SQL_C_TIME",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"0:33:0","0:33:41:0","0:33:41","0:33:41","0:33:41","0:33:41","0:33:41","0:33:41",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997-10-12 0:33:0.0","1997-10-12 0:33:41.0","1-01-01 0:33:41.1000","1-01-01 0:33:41.12000","1-01-01 0:33:41.123000","1-01-01 0:33:41.1234000","1-01-01 0:33:41.12345000","1-01-01 0:33:41.123456000",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEAULT",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"0:33:0","0:33:41","1-01-01 0:33:41.1000","1-01-01 0:33:41.12000","1-01-01 0:33:41.123000","1-01-01 0:33:41.1234000","1-01-01 0:33:41.12345000","1-01-01 0:33:41.123456000",
		},
		{999,}
		};

	struct
	{
		SQLSMALLINT	CType;
		char		*TestCType;
		char		InputValue[MAX_PartialSSTO][35];
		char		OutputValue[MAX_PartialSSTO][35];
	} CDataValueSSTO[] = {
		{SQL_C_CHAR,
		"SQL_C_CHAR",
		"1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"41","41.1","41.12","41.123","41.1234","41.12345","41.123456",
		},
		{SQL_C_TIME,
		"SQL_C_TIME",
		"1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"0:0:41","0:0:41","0:0:41","0:0:41","0:0:41","0:0:41","0:0:41",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997-10-12 0:0:41.0","1-01-01 0:0:41.1000","1-01-01 0:0:41.12000","1-01-01 0:0:41.123000","1-01-01 0:0:41.1234000","1-01-01 0:0:41.12345000","1-01-01 0:0:41.123456000",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"0:0:41","1-01-01 0:0:41.1000","1-01-01 0:0:41.12000","1-01-01 0:0:41.123000","1-01-01 0:0:41.1234000","1-01-01 0:0:41.12345000","1-01-01 0:0:41.123456000",
		},
		{999,}
		};

	//YYTO...
	char	*DrpTabYYTO = "DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLYYTO";
	char	*DelTabYYTO = "DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLYYTO";
	char	*CrtTabYYTO = "CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLYYTO(C1 DATETIME YEAR ,C2 DATETIME YEAR TO MONTH,C3 DATETIME YEAR TO DAY,C4 DATETIME YEAR TO HOUR,C5 DATETIME YEAR TO MINUTE,C6 DATETIME YEAR TO SECOND,C7 DATETIME YEAR TO FRACTION(1),C8 DATETIME YEAR TO FRACTION(2),C9 DATETIME YEAR TO FRACTION(3),C10 DATETIME YEAR TO FRACTION(4),C11 DATETIME YEAR TO FRACTION(5), C12 DATETIME YEAR TO FRACTION(6))";
	char	*InsTabYYTO = "INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLYYTO(C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)";
	char	*SelTabYYTO = "SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12 FROM TRAFODION.ODBC_SCHEMA.CSQLYYTO";
	
	//MMTO...
	char	*DrpTabMMTO = "DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLMMTO";
	char	*DelTabMMTO = "DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLMMTO";
	char	*CrtTabMMTO = "CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLMMTO(C1 DATETIME MONTH,C2 DATETIME MONTH TO DAY,C3 DATETIME MONTH TO HOUR,C4 DATETIME MONTH TO MINUTE,C5 DATETIME MONTH TO SECOND,C6 DATETIME MONTH TO FRACTION(1),C7 DATETIME MONTH TO FRACTION(2),C8 DATETIME MONTH TO FRACTION(3),C9 DATETIME MONTH TO FRACTION(4),C10 DATETIME MONTH TO FRACTION(5), C11 DATETIME MONTH TO FRACTION(6))";
	char	*InsTabMMTO = "INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLMMTO(C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11) VALUES (?,?,?,?,?,?,?,?,?,?,?)";
	char	*SelTabMMTO = "SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11 FROM TRAFODION.ODBC_SCHEMA.CSQLMMTO";
	
	//DDTO...
	char	*DrpTabDDTO = "DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLDDTO";
	char	*DelTabDDTO = "DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLDDTO";
	char	*CrtTabDDTO = "CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLDDTO(C1 DATETIME DAY,C2 DATETIME DAY TO HOUR,C3 DATETIME DAY TO MINUTE,C4 DATETIME DAY TO SECOND,C5 DATETIME DAY TO FRACTION(1),C6 DATETIME DAY TO FRACTION(2),C7 DATETIME DAY TO FRACTION(3),C8 DATETIME DAY TO FRACTION(4),C9 DATETIME DAY TO FRACTION(5), C10 DATETIME DAY TO FRACTION(6))";
	char	*InsTabDDTO = "INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLDDTO(C1,C2,C3,C4,C5,C6,C7,C8,C9,C10) VALUES (?,?,?,?,?,?,?,?,?,?)";	
	char	*SelTabDDTO = "SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10 FROM TRAFODION.ODBC_SCHEMA.CSQLDDTO";
	
	//HHTO...
	char	*DrpTabHHTO = "DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLHHTO";
	char	*DelTabHHTO = "DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLHHTO";
	char	*CrtTabHHTO = "CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLHHTO(C1 DATETIME HOUR,C2 DATETIME HOUR TO MINUTE,C3 DATETIME HOUR TO SECOND,C4 DATETIME HOUR TO FRACTION(1),C5 DATETIME HOUR TO FRACTION(2),C6 DATETIME HOUR TO FRACTION(3),C7 DATETIME HOUR TO FRACTION(4),C8 DATETIME HOUR TO FRACTION(5), C9 DATETIME HOUR TO FRACTION(6))";
	char	*InsTabHHTO = "INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLHHTO(C1,C2,C3,C4,C5,C6,C7,C8,C9) VALUES (?,?,?,?,?,?,?,?,?)";
	char	*SelTabHHTO = "SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9 FROM TRAFODION.ODBC_SCHEMA.CSQLHHTO";
	
	//MNTO...
	char	*DrpTabMNTO = "DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLMNTO";
	char	*DelTabMNTO = "DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLMNTO";
	char	*CrtTabMNTO = "CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLMNTO(C1 DATETIME MINUTE,C2 DATETIME MINUTE TO SECOND,C3 DATETIME MINUTE TO FRACTION(1),C4 DATETIME MINUTE TO FRACTION(2),C5 DATETIME MINUTE TO FRACTION(3),C6 DATETIME MINUTE TO FRACTION(4),C7 DATETIME MINUTE TO FRACTION(5), C8 DATETIME MINUTE TO FRACTION(6))";
	char	*InsTabMNTO = "INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLMNTO(C1,C2,C3,C4,C5,C6,C7,C8) VALUES (?,?,?,?,?,?,?,?)";
	char	*SelTabMNTO = "SELECT C1,C2,C3,C4,C5,C6,C7,C8 FROM TRAFODION.ODBC_SCHEMA.CSQLMNTO";
	
	//SSTO...
	char	*DrpTabSSTO = "DROP TABLE TRAFODION.ODBC_SCHEMA.CSQLSSTO";
	char	*DelTabSSTO = "DELETE FROM TRAFODION.ODBC_SCHEMA.CSQLSSTO";
	char	*CrtTabSSTO = "CREATE TABLE TRAFODION.ODBC_SCHEMA.CSQLSSTO(C1 DATETIME SECOND,C2 DATETIME SECOND TO FRACTION(1),C3 DATETIME SECOND TO FRACTION(2),C4 DATETIME SECOND TO FRACTION(3),C5 DATETIME SECOND TO FRACTION(4),C6 DATETIME SECOND TO FRACTION(5), C7 DATETIME SECOND TO FRACTION(6))";
	char	*InsTabSSTO = "INSERT INTO TRAFODION.ODBC_SCHEMA.CSQLSSTO(C1,C2,C3,C4,C5,C6,C7) VALUES (?,?,?,?,?,?,?)";
	char	*SelTabSSTO = "SELECT C1,C2,C3,C4,C5,C6,C7 FROM TRAFODION.ODBC_SCHEMA.CSQLSSTO";
	

	SQLLEN			InValue = SQL_NTS;
	time_t now;
	struct tm *timeArray;
	static char dateBuffer[12];
	
	char	State[STATE_SIZE];
	SDWORD	NativeError;
	char	buf[MAX_STRING_SIZE];

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing => Partial DateTime Output Conversions.\n");
	LogMsg(NONE, "");
	TEST_INIT;

	TESTCASE_BEGIN("Connection for partial datetime output conversion tests\n");

	if(!FullConnect(pTestInfo)){
		LogMsg(NONE,"Unable to connect\n");
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
	strftime (dateBuffer,12,"%Y-%m-%d",timeArray);

//====================================================================================================
// converting from YYTO
					
	sprintf(Heading,"Setup for SQLBindParameter tests for create table. \n %s\n",CrtTabYYTO);
	TESTCASE_BEGIN(Heading);
	
	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabYYTO,SQL_NTS);					//RS, create table disabled
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabYYTO,SQL_NTS);

	if (returncode != SQL_SUCCESS)
		{
			returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, hstmt, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
			if (NativeError == -3195)
			{
				LogMsg(NONE, "DATETIME datatype not supported\n");
				_gTestCount--;
				FullDisconnect(pTestInfo);
				LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing => Partial DateTime Output Conversions.\n");
			}
			else
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TEST_RETURN;
		}
	SQLExecDirect(hstmt,(SQLCHAR*) DelTabYYTO,SQL_NTS);	//RS: Since table is not created, delete any rows
//	TESTCASE_END;

	i = 0;
	while (CDataValueYYTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialYYTO; j++)
		{
			sprintf(Heading,"Set up SQLBindParameter to convert from SQL_C_CHAR to %s\n",CDataArgYYTO.TestSQLType[j]);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_CHAR,
								CDataArgYYTO.SQLType[j],CDataArgYYTO.ColPrec[j],
								CDataArgYYTO.ColScale[j],CDataValueYYTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		sprintf(Heading,"Inserting the data from SQL_C_CHAR.\n");
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabYYTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			sprintf(Heading,"Setup for select to %s.\n",CDataValueYYTO[i].TestCType);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabYYTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueYYTO[i].CType)
				{
				case SQL_C_CHAR:

				for (k = 0; k < MAX_PartialYYTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgYYTO.TestSQLType[k],CDataValueYYTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueYYTO[i].CType,CCharOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialYYTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking data for column c%d\n",k+1);
			
						if (_strnicmp(CDataValueYYTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialYYTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgYYTO.TestSQLType[k],CDataValueYYTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueYYTO[i].CType,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialYYTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n",k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						if (_strnicmp(CDataValueYYTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialYYTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgYYTO.TestSQLType[k],CDataValueYYTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueYYTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialYYTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n",k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueYYTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialYYTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgYYTO.TestSQLType[k],CDataValueYYTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					if (CDataArgYYTO.SQLType[k] == SQL_DATE)
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),SQL_C_DATE,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					else
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueYYTO[i].CType,&CTimeOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialYYTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						if (CDataArgYYTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueYYTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialYYTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgYYTO.TestSQLType[k],CDataValueYYTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					if (CDataArgYYTO.SQLType[k] == SQL_DATE)
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueYYTO[i].CType,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					else
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueYYTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialYYTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						if (CDataArgYYTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueYYTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				default:;

				}//switch
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLFreeStmt(hstmt,SQL_UNBIND);

		sprintf(Heading,"Setup for SQLBindParameter tests for delete table %s.\n",CDataValueYYTO[i].TestCType);
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)DelTabYYTO,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		i++;
		
 		
	}

	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabYYTO,SQL_NTS);

//====================================================================================================
// converting from MMTO
					
	sprintf(Heading,"Setup for SQLBindParameter tests for create table. \n %s\n",CrtTabMMTO);
	TESTCASE_BEGIN(Heading);
	
/*	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMMTO,SQL_NTS);				// RS: drop table disabled
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabMMTO,SQL_NTS);
	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	*/
	SQLExecDirect(hstmt,(SQLCHAR*) DelTabMMTO,SQL_NTS);				//RS: Since we do not create table, we delete al rows
	TESTCASE_END;

	i = 0;
	while (CDataValueMMTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialMMTO; j++)
		{
			sprintf(Heading,"Set up SQLBindParameter to convert from SQL_C_CHAR to %s\n",CDataArgMMTO.TestSQLType[j]);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_CHAR,
								CDataArgMMTO.SQLType[j],CDataArgMMTO.ColPrec[j],
								CDataArgMMTO.ColScale[j],CDataValueMMTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		sprintf(Heading,"Inserting the data from SQL_C_CHAR.\n");
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabMMTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			sprintf(Heading,"Setup for select to %s.\n",CDataValueMMTO[i].TestCType);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabMMTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueMMTO[i].CType)
				{
				case SQL_C_CHAR:

				for (k = 0; k < MAX_PartialMMTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgMMTO.TestSQLType[k],CDataValueMMTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMMTO[i].CType,CCharOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialMMTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking data for column c%d\n",k+1);
			
						if (_strnicmp(CDataValueMMTO[i].OutputValue[k],CCharOutput[k],strlen(CDataValueMMTO[i].OutputValue[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialMMTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgMMTO.TestSQLType[k],CDataValueMMTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMMTO[i].CType,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialMMTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n",k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						if (_strnicmp(CDataValueMMTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialMMTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgMMTO.TestSQLType[k],CDataValueMMTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMMTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialMMTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n",k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueMMTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialMMTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgMMTO.TestSQLType[k],CDataValueMMTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					if (CDataArgMMTO.SQLType[k] == SQL_DATE)
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),SQL_C_DATE,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					else
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMMTO[i].CType,&CTimeOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialMMTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						if (CDataArgMMTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueMMTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialMMTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgMMTO.TestSQLType[k],CDataValueMMTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					if (CDataArgMMTO.SQLType[k] == SQL_DATE)
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMMTO[i].CType,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					else
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMMTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialMMTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						if (CDataArgMMTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueMMTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				default:;

				}//switch
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		sprintf(Heading,"Setup for SQLBindParameter tests for delete table %s.\n",CDataValueMMTO[i].TestCType);
		TESTCASE_BEGIN(Heading);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)DelTabMMTO,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			//TEST_FAILED;
			TEST_RETURN;
		}
		//TESTCASE_END;
		i++;
		
 		
	}

	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMMTO,SQL_NTS);

//====================================================================================================
// converting from DDTO
					
	sprintf(Heading,"Setup for SQLBindParameter tests for create table. \n %s\n",CrtTabDDTO);
	TESTCASE_BEGIN(Heading);
/*	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDDTO,SQL_NTS);				// RS: drop table disabled
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabDDTO,SQL_NTS);
	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	*/
	SQLExecDirect(hstmt,(SQLCHAR*) DelTabDDTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
	//TESTCASE_END;

	i = 0;
	while (CDataValueDDTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialDDTO; j++)
		{
			sprintf(Heading,"Set up SQLBindParameter to convert from SQL_C_CHAR to %s\n",CDataArgDDTO.TestSQLType[j]);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_CHAR,
								CDataArgDDTO.SQLType[j],CDataArgDDTO.ColPrec[j],
								CDataArgDDTO.ColScale[j],CDataValueDDTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		sprintf(Heading,"Inserting the data from SQL_C_CHAR.\n");
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabDDTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			sprintf(Heading,"Setup for select to %s.\n",CDataValueDDTO[i].TestCType);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabDDTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueDDTO[i].CType)
				{
				case SQL_C_CHAR:

				for (k = 0; k < MAX_PartialDDTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgDDTO.TestSQLType[k],CDataValueDDTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueDDTO[i].CType,CCharOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialDDTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking data for column c%d\n",k+1);
			
						if (_strnicmp(CDataValueDDTO[i].OutputValue[k],CCharOutput[k],strlen(CDataValueDDTO[i].OutputValue[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialDDTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgDDTO.TestSQLType[k],CDataValueDDTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueDDTO[i].CType,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialDDTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n",k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						if (_strnicmp(CDataValueDDTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialDDTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgDDTO.TestSQLType[k],CDataValueDDTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueDDTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialDDTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n",k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueDDTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialDDTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgDDTO.TestSQLType[k],CDataValueDDTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					if (CDataArgDDTO.SQLType[k] == SQL_DATE)
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),SQL_C_DATE,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					else
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueDDTO[i].CType,&CTimeOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialDDTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						if (CDataArgDDTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueDDTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialDDTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgDDTO.TestSQLType[k],CDataValueDDTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					if (CDataArgDDTO.SQLType[k] == SQL_DATE)
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueDDTO[i].CType,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					else
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueDDTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialDDTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						if (CDataArgDDTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueDDTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				default:;

				}//switch
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		sprintf(Heading,"Setup for SQLBindParameter tests for delete table %s.\n",CDataValueDDTO[i].TestCType);
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)DelTabDDTO,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		i++;
		
 		
	}

	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDDTO,SQL_NTS);

//====================================================================================================
// converting from HHTO
					
	sprintf(Heading,"Setup for SQLBindParameter tests for create table. \n %s\n",CrtTabHHTO);
	TESTCASE_BEGIN(Heading);
/*	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabHHTO,SQL_NTS);				//RS: Drop table disabled
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabHHTO,SQL_NTS);
	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	*/
	SQLExecDirect(hstmt,(SQLCHAR*) DelTabHHTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
//	TESTCASE_END;

	i = 0;
	while (CDataValueHHTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialHHTO; j++)
		{
			sprintf(Heading,"Set up SQLBindParameter to convert from SQL_C_CHAR to %s\n",CDataArgHHTO.TestSQLType[j]);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_CHAR,
								CDataArgHHTO.SQLType[j],CDataArgHHTO.ColPrec[j],
								CDataArgHHTO.ColScale[j],CDataValueHHTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		sprintf(Heading,"Inserting the data from SQL_C_CHAR.\n");
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabHHTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			sprintf(Heading,"Setup for select to %s.\n",CDataValueHHTO[i].TestCType);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabHHTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueHHTO[i].CType)
				{
				case SQL_C_CHAR:

				for (k = 0; k < MAX_PartialHHTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgHHTO.TestSQLType[k],CDataValueHHTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueHHTO[i].CType,CCharOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialHHTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking data for column c%d\n",k+1);
			
						if (_strnicmp(CDataValueHHTO[i].OutputValue[k],CCharOutput[k],strlen(CDataValueHHTO[i].OutputValue[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialHHTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgHHTO.TestSQLType[k],CDataValueHHTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueHHTO[i].CType,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialHHTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n",k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueHHTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialHHTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgHHTO.TestSQLType[k],CDataValueHHTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueHHTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialHHTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n",k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						// Since we are giving only time as input the current date is inserted for date part. 
						// Hence we will change the date part of expected output to current date.
						if ( k <= 2) 
						{	strncpy(CDataValueHHTO[i].OutputValue[k],dateBuffer,10);
								
						}
						if (_strnicmp(CDataValueHHTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialHHTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgHHTO.TestSQLType[k],CDataValueHHTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueHHTO[i].CType,&CTimeOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialHHTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						//LogMsg(NONE,"Time[%d]:%d:%d:%d\n",k+1,CTimeOutput[k].hour,CTimeOutput[k].minute,CTimeOutput[k].second);
						
						if (_strnicmp(CDataValueHHTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialHHTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgHHTO.TestSQLType[k],CDataValueHHTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					if (CDataArgHHTO.SQLType[k] == SQL_TIME)
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueHHTO[i].CType,&CTimeOutput[k],NAME_LEN,&OutputLen1[k]);
					else
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueHHTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialHHTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						if (CDataArgHHTO.SQLType[k] == SQL_TIME)
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueHHTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				default:;

				}//switch
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		sprintf(Heading,"Setup for SQLBindParameter tests for delete table %s.\n",CDataValueHHTO[i].TestCType);
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)DelTabHHTO,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		i++;
		
 		
	}

	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabHHTO,SQL_NTS);

//====================================================================================================
// converting from MNTO
					
	sprintf(Heading,"Setup for SQLBindParameter tests for create table. \n %s\n",CrtTabMNTO);
	TESTCASE_BEGIN(Heading);
/*	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMNTO,SQL_NTS);				// RS: Drop table disabled
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabMNTO,SQL_NTS);
	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	*/
	SQLExecDirect(hstmt,(SQLCHAR*) DelTabMNTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
//	TESTCASE_END;

	i = 0;
	while (CDataValueMNTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialMNTO; j++)
		{
			sprintf(Heading,"Set up SQLBindParameter to convert from SQL_C_CHAR to %s\n",CDataArgMNTO.TestSQLType[j]);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_CHAR,
								CDataArgMNTO.SQLType[j],CDataArgMNTO.ColPrec[j],
								CDataArgMNTO.ColScale[j],CDataValueMNTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		sprintf(Heading,"Inserting the data from SQL_C_CHAR.\n");
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabMNTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			sprintf(Heading,"Setup for select to %s.\n",CDataValueMNTO[i].TestCType);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabMNTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueMNTO[i].CType)
				{
				case SQL_C_CHAR:

				for (k = 0; k < MAX_PartialMNTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgMNTO.TestSQLType[k],CDataValueMNTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMNTO[i].CType,CCharOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialMNTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking data for column c%d\n",k+1);
			
						if (_strnicmp(CDataValueMNTO[i].OutputValue[k],CCharOutput[k],strlen(CDataValueMNTO[i].OutputValue[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialMNTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgMNTO.TestSQLType[k],CDataValueMNTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMNTO[i].CType,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialMNTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n",k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						if (_strnicmp(CDataValueMNTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialMNTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgMNTO.TestSQLType[k],CDataValueMNTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMNTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialMNTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n",k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						// Since we are giving only time as input the current date is inserted for date part. 
						// Hence we will change the date part of expected output to current date.
						if ( k <= 1) 
						{	strncpy(CDataValueMNTO[i].OutputValue[k],dateBuffer,10);
								
						}
						if (_strnicmp(CDataValueMNTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialMNTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgMNTO.TestSQLType[k],CDataValueMNTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMNTO[i].CType,&CTimeOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialMNTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueMNTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialMNTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgMNTO.TestSQLType[k],CDataValueMNTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					if (CDataArgMNTO.SQLType[k] == SQL_TIME)
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMNTO[i].CType,&CTimeOutput[k],NAME_LEN,&OutputLen1[k]);
					else
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueMNTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialMNTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						if (CDataArgMNTO.SQLType[k] == SQL_TIME)
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueMNTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				default:;

				}//switch
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		sprintf(Heading,"Setup for SQLBindParameter tests for delete table %s.\n",CDataValueMNTO[i].TestCType);
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)DelTabMNTO,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		i++;
		
 		
	}

SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMNTO,SQL_NTS);

//====================================================================================================
// converting from SSTO
					
	sprintf(Heading,"Setup for SQLBindParameter tests for create table. \n %s\n",CrtTabSSTO);
	TESTCASE_BEGIN(Heading);
/*	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabSSTO,SQL_NTS);				//RS: drop table disabled
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabSSTO,SQL_NTS);
	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	*/
	SQLExecDirect(hstmt,(SQLCHAR*) DelTabSSTO,SQL_NTS);				//RS: since we do not create the table, we delete all rows
//	TESTCASE_END;

	i = 0;
	while (CDataValueSSTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialSSTO; j++)
		{
			sprintf(Heading,"Set up SQLBindParameter to convert from SQL_C_CHAR to %s\n",CDataArgSSTO.TestSQLType[j]);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_CHAR,
								CDataArgSSTO.SQLType[j],CDataArgSSTO.ColPrec[j],
								CDataArgSSTO.ColScale[j],CDataValueSSTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		sprintf(Heading,"Inserting the data from SQL_C_CHAR.\n");
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabSSTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			sprintf(Heading,"Setup for select to %s.\n",CDataValueSSTO[i].TestCType);
			TESTCASE_BEGIN(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabSSTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueSSTO[i].CType)
				{
				case SQL_C_CHAR:

				for (k = 0; k < MAX_PartialSSTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgSSTO.TestSQLType[k],CDataValueSSTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueSSTO[i].CType,CCharOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialSSTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking data for column c%d\n",k+1);
			
						if (_strnicmp(CDataValueSSTO[i].OutputValue[k],CCharOutput[k],strlen(CDataValueSSTO[i].OutputValue[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialSSTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgSSTO.TestSQLType[k],CDataValueSSTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueSSTO[i].CType,&CDateOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialSSTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n",k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						if (_strnicmp(CDataValueSSTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialSSTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgSSTO.TestSQLType[k],CDataValueSSTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					
					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueSSTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialSSTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n",k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						// Since we are giving only time as input the current date is inserted for date part. 
						// Hence we will change the date part of expected output to current date.
						if ( k == 0) 
						{	strncpy(CDataValueSSTO[i].OutputValue[k],dateBuffer,10);
								
						}
						if (_strnicmp(CDataValueSSTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialSSTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgSSTO.TestSQLType[k],CDataValueSSTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueSSTO[i].CType,&CTimeOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialSSTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueSSTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialSSTO; k++)
				{  
					sprintf(Heading,"SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n",k+1,CDataArgSSTO.TestSQLType[k],CDataValueSSTO[i].TestCType);
					TESTCASE_BEGIN(Heading);
					

					CCharOutput[k] = (char *)malloc(NAME_LEN);
					memset(CCharOutput[k],0,NAME_LEN);
					if (CDataArgSSTO.SQLType[k] == SQL_TIME)
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueSSTO[i].CType,&CTimeOutput[k],NAME_LEN,&OutputLen1[k]);
					else
						returncode = SQLBindCol(hstmt,(SWORD)(k+1),CDataValueSSTO[i].CType,&CTimeStampOutput[k],NAME_LEN,&OutputLen1[k]);
					
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					TESTCASE_END;  
				}
				
				returncode = SQLFetch(hstmt);
				if((!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")) && (!CHECKRC(SQL_SUCCESS_WITH_INFO,returncode,"SQLFetch")))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (k = 0; k < MAX_PartialSSTO; k++)
					{
						//LogMsg(NONE,"SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n",k+1);
						
						if (CDataArgSSTO.SQLType[k] == SQL_TIME)
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_strnicmp(CDataValueSSTO[i].OutputValue[k],CCharOutput[k],strlen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				default:;

				}//switch
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		sprintf(Heading,"Setup for SQLBindParameter tests for delete table %s.\n",CDataValueSSTO[i].TestCType);
		TESTCASE_BEGIN(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)DelTabSSTO,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		i++;
		
 		
	}

SQLExecDirect(hstmt,(SQLCHAR*) DrpTabSSTO,SQL_NTS);

FullDisconnect(pTestInfo);
LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing => Partial DateTime Output Conversions.\n");
TEST_RETURN;

}

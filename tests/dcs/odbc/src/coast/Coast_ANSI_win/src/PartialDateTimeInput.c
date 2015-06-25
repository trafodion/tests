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
 	char				Heading[MAX_STRING_SIZE];
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
		"1997","1997-10","1997-10-12","1997-10-12 00","1997-10-12 00:00","1997-10-12 00:00:00","1997-10-12 00:00:00.0","1997-10-12 00:00:00.00","1997-10-12 00:00:00.000","1997-10-12 00:00:00.0000","1997-10-12 00:00:00.00000","1997-10-12 00:00:00.000000",
		},
		{SQL_C_TIME,
		"SQL_C_TIME",
		"1997-10-12","1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997","1997-10","1997-10-12","1997-10-12 11","1997-10-12 11:33","1997-10-12 11:33:41","1997-10-12 11:33:41.0","1997-10-12 11:33:41.00","1997-10-12 11:33:41.000","1997-10-12 11:33:41.0000","1997-10-12 11:33:41.00000","1997-10-12 11:33:41.000000",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12","1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997","1997-10","1997-10-12","1997-10-12 11","1997-10-12 11:33","1997-10-12 11:33:41","1997-10-12 11:33:41.3","1997-10-12 11:33:41.23","1997-10-12 11:33:41.123","1997-10-12 11:33:41.0123","1997-10-12 11:33:41.00123","1997-10-12 11:33:41.000123",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997","1997-10","1997-10-12","1997-10-12 11","1997-10-12 11:33","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"1997","1997-10","1997-10-12","1997-10-12 11","1997-10-12 11:33","1997-10-12 11:33:41","1997-10-12 11:33:41.3","1997-10-12 11:33:41.23","1997-10-12 11:33:41.123","1997-10-12 11:33:41.0123","1997-10-12 11:33:41.00123","1997-10-12 11:33:41.000123",
		},
		
		{999,}
		};

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
		"10","10-12","10-12 00","10-12 00:00","10-12 00:00:00","10-12 00:00:00.0","10-12 00:00:00.00","10-12 00:00:00.000","10-12 00:00:00.0000","10-12 00:00:00.00000","10-12 00:00:00.000000",
		},
		{SQL_C_TIME,
		"SQL_C_TIME",
		"1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"10","10-12","10-12 11","10-12 11:33","10-12 11:33:41","10-12 11:33:41.0","10-12 11:33:41.00","10-12 11:33:41.000","10-12 11:33:41.0000","10-12 11:33:41.00000","10-12 11:33:41.000000",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"10","10-12","10-12 11","10-12 11:33","10-12 11:33:41","10-12 11:33:41.3","10-12 11:33:41.23","10-12 11:33:41.123","10-12 11:33:41.0123","10-12 11:33:41.00123","10-12 11:33:41.000123",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997-10-12","1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"10","10-12","10-12 11","10-12 11:33","10-12 11:33:41","10-12 11:33:41.3","10-12 11:33:41.23","10-12 11:33:41.123","10-12 11:33:41.0123","10-12 11:33:41.00123","10-12 11:33:41.000123",
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
		"12","12 00","12 00:00","12 00:00:00","12 00:00:00.0","12 00:00:00.00","12 00:00:00.000","12 00:00:00.0000","12 00:00:00.00000","12 00:00:00.000000",
		},
		{SQL_C_TIME,
		"SQL_C_TIME",
		"1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"12","12 11","12 11:33","12 11:33:41","12 11:33:41.0","12 11:33:41.00","12 11:33:41.000","12 11:33:41.0000","12 11:33:41.00000","12 11:33:41.000000",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"12","12 11","12 11:33","12 11:33:41","12 11:33:41.3","12 11:33:41.23","12 11:33:41.123","12 11:33:41.0123","12 11:33:41.00123","12 11:33:41.000123",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997-10-12","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"12","12 11","12 11:33","12 11:33:41","12 11:33:41.3","12 11:33:41.23","12 11:33:41.123","12 11:33:41.0123","12 11:33:41.00123","12 11:33:41.000123",
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
		"11","11:33","11:33:41","11:33:41.0","11:33:41.00","11:33:41.000","11:33:41.0000","11:33:41.00000","11:33:41.000000",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"11","11:33","11:33:41","11:33:41.3","11:33:41.23","11:33:41.123","11:33:41.0123","11:33:41.00123","11:33:41.000123",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"11","11:33","11:33:41","11:33:41.3","11:33:41.23","11:33:41.123","11:33:41.0123","11:33:41.00123","11:33:41.000123",
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
		"33","33:41","33:41.0","33:41.00","33:41.000","33:41.0000","33:41.00000","33:41.000000",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"33","33:41","33:41.3","33:41.23","33:41.123","33:41.0123","33:41.00123","33:41.000123",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997-10-12 11:33:41","1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"33","33:41","33:41.3","33:41.23","33:41.123","33:41.0123","33:41.00123","33:41.000123",
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
		"41","41.0","41.00","41.000","41.0000","41.00000","41.000000",
		},
		{SQL_C_TIMESTAMP,
		"SQL_C_TIMESTAMP",
		"1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"41","41.3","41.23","41.123","41.0123","41.00123","41.000123",
		},
		{SQL_C_DEFAULT,
		"SQL_C_DEFAULT",
		"1997-10-12 11:33:41","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789","1997-10-12 11:33:41.123456789",
		"41","41.3","41.23","41.123","41.0123","41.00123","41.000123",
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
	char			OutValue[NAME_LEN];
	SQLLEN		OutValueLen;
	time_t now;
	struct tm *timeArray;
	static char dateBuffer[12];
	char	State[STATE_SIZE];
	SDWORD	NativeError;
	char	buf[MAX_STRING_SIZE];
	

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing => Partial DateTime Input Conversions.\n");
	LogMsg(NONE, "");
	TEST_INIT;

	TESTCASE_BEGIN("Connection for partial datetime input conversion tests\n");

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
	
				
	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		sprintf(Heading,"Setup for SQLBindParameter tests for create table:\n %s.\n",CrtTabYYTO);
		TESTCASE_BEGIN(Heading);
	
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabYYTO,SQL_NTS);				//RS: Create/drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabYYTO,SQL_NTS);
		if(returncode != SQL_SUCCESS)
		{
			returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, hstmt, (SQLCHAR*)State, &NativeError, (SQLCHAR*)buf, MAX_STRING_SIZE, NULL);
			if (NativeError == -3195)
			{
				LogMsg(NONE, "DATETIME datatype not supported\n");
				_gTestCount--;
				FullDisconnect(pTestInfo);
				LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing => Partial DateTime Input Conversions.\n");
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
		SQLExecDirect(hstmt,(SQLCHAR*) DelTabYYTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueYYTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare %s.\n",CDataValueYYTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTabYYTO,SQL_NTS);
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
				sprintf(Heading,"Set up SQLBindParameter to convert from %s to %s\n",CDataValueYYTO[i].TestCType, CDataArgYYTO.TestSQLType[j]);
				TESTCASE_BEGIN(Heading);

                switch (CDataValueYYTO[i].CType)
				{
					case SQL_C_CHAR:
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
						{	strncpy(CDataValueYYTO[i].OutputValue[j],dateBuffer,10);
								
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
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute %s.\n",CDataValueYYTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
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
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect %s.\n",CDataValueYYTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabYYTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests %s.\n",CDataValueYYTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabYYTO,SQL_NTS);
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
							//LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_strnicmp(CDataValueYYTO[i].OutputValue[j],OutValue,strlen(CDataValueYYTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueYYTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueYYTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
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
	}
	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabYYTO,SQL_NTS);


//=================================================================================================================
//====================================================================================================
// converting from MMTO

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		sprintf(Heading,"Setup for SQLBindParameter tests for create table:\n %s.\n",CrtTabMMTO);
		TESTCASE_BEGIN(Heading);

/*		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMMTO,SQL_NTS);				// RS: Create/drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabMMTO,SQL_NTS);
		
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLCHAR*) DelTabMMTO,SQL_NTS);				// RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueMMTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare %s.\n",CDataValueMMTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				
				returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTabMMTO,SQL_NTS);
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
				sprintf(Heading,"Set up SQLBindParameter to convert from %s to %s\n",CDataValueMMTO[i].TestCType, CDataArgMMTO.TestSQLType[j]);
				TESTCASE_BEGIN(Heading);
				

				switch (CDataValueMMTO[i].CType)
				{
					case SQL_C_CHAR:			
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
						{	strncpy(CDataValueMMTO[i].OutputValue[j],&dateBuffer[5],5);
								
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
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute %s.\n",CDataValueMMTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
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
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect %s.\n",CDataValueMMTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabMMTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests %s.\n",CDataValueMMTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabMMTO,SQL_NTS);
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
							//LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_strnicmp(CDataValueMMTO[i].OutputValue[j],OutValue,strlen(CDataValueMMTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMMTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMMTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			sprintf(Heading,"Setup for SQLBindParameter tests for delete table %s.\n",CDataValueMMTO[i].TestCType);
			TESTCASE_BEGIN(Heading);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)DelTabMMTO,SQL_NTS);
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
	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMMTO,SQL_NTS);

//=================================================================================================================
//====================================================================================================
// converting from DDTO

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		sprintf(Heading,"Setup for SQLBindParameter tests for create table:\n %s.\n",CrtTabDDTO);
		TESTCASE_BEGIN(Heading);

/*		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDDTO,SQL_NTS);				// RS: Create/drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabDDTO,SQL_NTS);
		
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLCHAR*) DelTabDDTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueDDTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare %s.\n",CDataValueDDTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTabDDTO,SQL_NTS);
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
				sprintf(Heading,"Set up SQLBindParameter to convert from %s to %s\n",CDataValueDDTO[i].TestCType, CDataArgDDTO.TestSQLType[j]);
				TESTCASE_BEGIN(Heading);
				
				switch (CDataValueDDTO[i].CType)
				{
					case SQL_C_CHAR:			
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
						{	strncpy(CDataValueDDTO[i].OutputValue[j],&dateBuffer[8],2);
								
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
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute %s.\n",CDataValueDDTO[i].TestCType);
				TESTCASE_BEGIN(Heading);

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
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect %s.\n",CDataValueDDTO[i].TestCType);
				TESTCASE_BEGIN(Heading);

				returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabDDTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests %s.\n",CDataValueDDTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabDDTO,SQL_NTS);
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
							//LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_strnicmp(CDataValueDDTO[i].OutputValue[j],OutValue,strlen(CDataValueDDTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueDDTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueDDTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
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
	}
	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDDTO,SQL_NTS);

//=================================================================================================================
//====================================================================================================
// converting from HHTO

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		sprintf(Heading,"Setup for SQLBindParameter tests for create table:\n %s.\n",CrtTabHHTO);
		TESTCASE_BEGIN(Heading);
		
/*		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabHHTO,SQL_NTS);				//RS: Create/drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabHHTO,SQL_NTS);
		
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLCHAR*) DelTabHHTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueHHTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare %s.\n",CDataValueHHTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
								
				returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTabHHTO,SQL_NTS);
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
				sprintf(Heading,"Set up SQLBindParameter to convert from %s to %s\n",CDataValueHHTO[i].TestCType, CDataArgHHTO.TestSQLType[j]);
				TESTCASE_BEGIN(Heading);
								
				switch (CDataValueHHTO[i].CType)
				{
					case SQL_C_CHAR:			
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
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute %s.\n",CDataValueHHTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
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
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect %s.\n",CDataValueHHTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabHHTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests %s.\n",CDataValueHHTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabHHTO,SQL_NTS);
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
							//LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_strnicmp(CDataValueHHTO[i].OutputValue[j],OutValue,strlen(CDataValueHHTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueHHTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueHHTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
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
	}
	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabHHTO,SQL_NTS);

//=================================================================================================================
//====================================================================================================
// converting from MNTO

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		sprintf(Heading,"Setup for SQLBindParameter tests for create table:\n %s.\n",CrtTabMNTO);
		TESTCASE_BEGIN(Heading);
		
		
/*		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMNTO,SQL_NTS);				// RS: Create/drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabMNTO,SQL_NTS);
		
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLCHAR*) DelTabMNTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueMNTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare %s.\n",CDataValueMNTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				
				returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTabMNTO,SQL_NTS);
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
				sprintf(Heading,"Set up SQLBindParameter to convert from %s to %s\n",CDataValueMNTO[i].TestCType, CDataArgMNTO.TestSQLType[j]);
				TESTCASE_BEGIN(Heading);
				
				
				switch (CDataValueMNTO[i].CType)
				{
					case SQL_C_CHAR:			
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
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute %s.\n",CDataValueMNTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
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
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect %s.\n",CDataValueMNTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabMNTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests %s.\n",CDataValueMNTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabMNTO,SQL_NTS);
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
							//LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_strnicmp(CDataValueMNTO[i].OutputValue[j],OutValue,strlen(CDataValueMNTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueMNTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueMNTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
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
	}
	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMNTO,SQL_NTS);

//=================================================================================================================
//====================================================================================================
// converting from SSTO

	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		sprintf(Heading,"Setup for SQLBindParameter tests for create table:\n %s.\n",CrtTabSSTO);
		TESTCASE_BEGIN(Heading);
		

/*		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabSSTO,SQL_NTS);				// RS: Create/Drop table disabled
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabSSTO,SQL_NTS);
		
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		*/
		SQLExecDirect(hstmt,(SQLCHAR*) DelTabSSTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
		TESTCASE_END;

		i = 0;TS_iteration=0;
		while (CDataValueSSTO[i].CType != 999)
		{
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				sprintf(Heading,"Setup for SQLBindParameter tests for prepare %s.\n",CDataValueSSTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				
				returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTabSSTO,SQL_NTS);
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
				sprintf(Heading,"Set up SQLBindParameter to convert from %s to %s\n",CDataValueSSTO[i].TestCType, CDataArgSSTO.TestSQLType[j]);
				TESTCASE_BEGIN(Heading);
				
				
				switch (CDataValueSSTO[i].CType)
				{
					case SQL_C_CHAR:			
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
				sprintf(Heading,"Setup for SQLBindParameter tests for Execute %s.\n",CDataValueSSTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
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
				sprintf(Heading,"Setup for SQLBindParameter tests for ExecDirect %s.\n",CDataValueSSTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsTabSSTO,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
			{
				sprintf(Heading,"Setup for checking SQLBindParameter tests %s.\n",CDataValueSSTO[i].TestCType);
				TESTCASE_BEGIN(Heading);
				
				returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabSSTO,SQL_NTS);
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
							//LogMsg(NONE,"SQLBindParameter test: checking data for column c%d\n",j+1);
				
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							else
							{
								if (_strnicmp(CDataValueSSTO[i].OutputValue[j],OutValue,strlen(CDataValueSSTO[i].OutputValue[j])) == 0)
								{
									//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueSSTO[i].OutputValue[j],OutValue);
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched\n",CDataValueSSTO[i].OutputValue[j],OutValue);
								}
							}
						} // end for loop
					}
				}
			}
			TESTCASE_END;
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
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
	}
	SQLExecDirect(hstmt,(SQLCHAR*) DrpTabSSTO,SQL_NTS);

//=================================================================================================================

	
	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing => Partial DateTime Input Conversions.\n");
	TEST_RETURN;
}

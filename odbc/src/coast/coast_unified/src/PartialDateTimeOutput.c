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

int ConvertTimeToString(SQL_TIME_STRUCT * t, TCHAR * strTime)
{
_stprintf(strTime, _T("%d:%d:%d"),t->hour,t->minute,t->second);
	return 8;
}

int ConvertDateToString( SQL_DATE_STRUCT * d, TCHAR * strDate)
{
	_stprintf(strDate, _T("%d-%d-%d"),d->year,d->month,d->day);
	return 8;
}
int ConvertTimestampToString(SQL_TIMESTAMP_STRUCT * ts, TCHAR * strTS)
{
	_stprintf(strTS, _T("%d-%.2d-%.2d %d:%d:%d.%u"),ts->year,ts->month,ts->day,ts->hour,ts->minute,ts->second,(unsigned int)ts->fraction);
	return 29;
}

PassFail TestMXPartialDateTimeOutputConversions(TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	TCHAR				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	int					i, j, k;
	SQLSMALLINT			ParamType = SQL_PARAM_INPUT;
	
	
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
		_T("1997-1-1"),_T("1997-10-1"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),
		},
		{SQL_C_TIME,
		_T("SQL_C_TIME"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997-1-1"),_T("1997-10-1"),_T("1997-10-12"),_T("11:0:0"),_T("11:33:0"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997-01-01 0:0:0.0"),_T("1997-10-01 0:0:0.0"),_T("1997-10-12 0:0:0.0"),_T("1997-10-12 11:0:0.0"),_T("1997-10-12 11:33:0.0"),_T("1997-10-12 11:33:41.0"),_T("1997-10-12 11:33:41.1000"),_T("1997-10-12 11:33:41.12000"),_T("1997-10-12 11:33:41.123000"),_T("1997-10-12 11:33:41.1234000"),_T("1997-10-12 11:33:41.12345000"),_T("1997-10-12 11:33:41.123456000"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997-1-1"),_T("1997-10-1"),_T("1997-10-12"),_T("1997-10-12 11:0:0.0"),_T("1997-10-12 11:33:0.0"),_T("1997-10-12 11:33:41.0"),_T("1997-10-12 11:33:41.1000"),_T("1997-10-12 11:33:41.12000"),_T("1997-10-12 11:33:41.123000"),_T("1997-10-12 11:33:41.1234000"),_T("1997-10-12 11:33:41.12345000"),_T("1997-10-12 11:33:41.123456000"),
		},
		{999,}
#endif
	};
	
	TCHAR		*CCharOutput[MAX_PartialYYTO];
	SQLLEN	OutputLen1[MAX_PartialYYTO];
	SQL_DATE_STRUCT	CDateOutput[MAX_PartialYYTO];
	SQL_TIMESTAMP_STRUCT	CTimeStampOutput[MAX_PartialYYTO];
	SQL_TIME_STRUCT	CTimeOutput[MAX_PartialYYTO];
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
		_T("1-10-1"),_T("1-10-12"),_T("1-10-12"),_T("1-10-12"),_T("1-10-12"),_T("1-10-12"),_T("1-10-12"),_T("1-10-12"),_T("1-10-12"),_T("1-10-12"),_T("1-10-12"),
		},
		{SQL_C_TIME,
		_T("SQL_C_TIME"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1-10-1"),_T("1-10-12"),_T("11:0:0"),_T("11:33:0"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1-10-01 0:0:0.0"),_T("1-10-12 0:0:0.0"),_T("1-10-12 11:0:0.0"),_T("1-10-12 11:33:0.0"),_T("1-10-12 11:33:41.0"),_T("1-10-12 11:33:41.1000"),_T("1-10-12 11:33:41.12000"),_T("1-10-12 11:33:41.123000"),_T("1-10-12 11:33:41.1234000"),_T("1-10-12 11:33:41.12345000"),_T("1-10-12 11:33:41.123456000"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997-10-12"),_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1-10-1"),_T("1-10-12"),_T("1-10-12 11:0:0.0"),_T("1-10-12 11:33:0.0"),_T("1-10-12 11:33:41.0"),_T("1-10-12 11:33:41.1000"),_T("1-10-12 11:33:41.12000"),_T("1-10-12 11:33:41.123000"),_T("1-10-12 11:33:41.1234000"),_T("1-10-12 11:33:41.12345000"),_T("1-10-12 11:33:41.123456000"),
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
		_T("1-1-12"),_T("1-1-12"),_T("1-1-12"),_T("1-1-12"),_T("1-1-12"),_T("1-1-12"),_T("1-1-12"),_T("1-1-12"),_T("1-1-12"),_T("1-1-12"),
		},
		{SQL_C_TIME,
		_T("SQL_C_TIME"),
		_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1-1-12"),_T("11:0:0"),_T("11:33:0"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1-01-12 0:0:0.0"),_T("1-01-12 11:0:0.0"),_T("1-01-12 11:33:0.0"),_T("1-01-12 11:33:41.0"),_T("1-01-12 11:33:41.1000"),_T("1-01-12 11:33:41.12000"),_T("1-01-12 11:33:41.123000"),_T("1-01-12 11:33:41.1234000"),_T("1-01-12 11:33:41.12345000"),_T("1-01-12 11:33:41.123456000"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997-10-12"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1-1-12"),_T("1-01-12 11:0:0.0"),_T("1-01-12 11:33:0.0"),_T("1-01-12 11:33:41.0"),_T("1-01-12 11:33:41.1000"),_T("1-01-12 11:33:41.12000"),_T("1-01-12 11:33:41.123000"),_T("1-01-12 11:33:41.1234000"),_T("1-01-12 11:33:41.12345000"),_T("1-01-12 11:33:41.123456000"),
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
	} CDataValueHHTO[5] = {
#ifndef unixcli
	  {SQL_C_TCHAR,
		_T("SQL_C_TCHAR"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("11"),_T("11:33"),_T("11:33:41"),_T("11:33:41.1"),_T("11:33:41.12"),_T("11:33:41.123"),_T("11:33:41.1234"),_T("11:33:41.12345"),_T("11:33:41.123456"),
		},
		{SQL_C_TIME,
		_T("SQL_C_TIME"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("11:0:0"),_T("11:33:0"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),_T("11:33:41"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997-10-12 11:0:0.0"),_T("1997-10-12 11:33:0.0"),_T("1997-10-12 11:33:41.0"),_T("1-01-01 11:33:41.1000"),_T("1-01-01 11:33:41.12000"),_T("1-01-01 11:33:41.123000"),_T("1-01-01 11:33:41.1234000"),_T("1-01-01 11:33:41.12345000"),_T("1-01-01 11:33:41.123456000"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("11:0:0"),_T("11:33:0"),_T("11:33:41"),_T("1-01-01 11:33:41.1000"),_T("1-01-01 11:33:41.12000"),_T("1-01-01 11:33:41.123000"),_T("1-01-01 11:33:41.1234000"),_T("1-01-01 11:33:41.12345000"),_T("1-01-01 11:33:41.123456000"),
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
		_T("0:33:0"),_T("0:33:41:0"),_T("0:33:41"),_T("0:33:41"),_T("0:33:41"),_T("0:33:41"),_T("0:33:41"),_T("0:33:41"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997-10-12 0:33:0.0"),_T("1997-10-12 0:33:41.0"),_T("1-01-01 0:33:41.1000"),_T("1-01-01 0:33:41.12000"),_T("1-01-01 0:33:41.123000"),_T("1-01-01 0:33:41.1234000"),_T("1-01-01 0:33:41.12345000"),_T("1-01-01 0:33:41.123456000"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEAULT"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("0:33:0"),_T("0:33:41"),_T("1-01-01 0:33:41.1000"),_T("1-01-01 0:33:41.12000"),_T("1-01-01 0:33:41.123000"),_T("1-01-01 0:33:41.1234000"),_T("1-01-01 0:33:41.12345000"),_T("1-01-01 0:33:41.123456000"),
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
		_T("0:0:41"),_T("0:0:41"),_T("0:0:41"),_T("0:0:41"),_T("0:0:41"),_T("0:0:41"),_T("0:0:41"),
		},
		{SQL_C_TIMESTAMP,
		_T("SQL_C_TIMESTAMP"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("1997-10-12 0:0:41.0"),_T("1-01-01 0:0:41.1000"),_T("1-01-01 0:0:41.12000"),_T("1-01-01 0:0:41.123000"),_T("1-01-01 0:0:41.1234000"),_T("1-01-01 0:0:41.12345000"),_T("1-01-01 0:0:41.123456000"),
		},
		{SQL_C_DEFAULT,
		_T("SQL_C_DEFAULT"),
		_T("1997-10-12 11:33:41"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),_T("1997-10-12 11:33:41.123456789"),
		_T("0:0:41"),_T("1-01-01 0:0:41.1000"),_T("1-01-01 0:0:41.12000"),_T("1-01-01 0:0:41.123000"),_T("1-01-01 0:0:41.1234000"),_T("1-01-01 0:0:41.12345000"),_T("1-01-01 0:0:41.123456000"),
		},
		{999,}
#endif
	};

	//YYTO...
	TCHAR	*DrpTabYYTO = _T("DROP TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLYYTO");
	TCHAR	*DelTabYYTO = _T("DELETE FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLYYTO");
	TCHAR	*CrtTabYYTO = _T("CREATE TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLYYTO(C1 DATETIME YEAR ,C2 DATETIME YEAR TO MONTH,C3 DATETIME YEAR TO DAY,C4 DATETIME YEAR TO HOUR,C5 DATETIME YEAR TO MINUTE,C6 DATETIME YEAR TO SECOND,C7 DATETIME YEAR TO FRACTION(1),C8 DATETIME YEAR TO FRACTION(2),C9 DATETIME YEAR TO FRACTION(3),C10 DATETIME YEAR TO FRACTION(4),C11 DATETIME YEAR TO FRACTION(5), C12 DATETIME YEAR TO FRACTION(6))");
	TCHAR	*InsTabYYTO = _T("INSERT INTO TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLYYTO(C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)");
	TCHAR	*SelTabYYTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12 FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLYYTO");
	
	//MMTO...
	TCHAR	*DrpTabMMTO = _T("DROP TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLMMTO");
	TCHAR	*DelTabMMTO = _T("DELETE FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLMMTO");
	TCHAR	*CrtTabMMTO = _T("CREATE TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLMMTO(C1 DATETIME MONTH,C2 DATETIME MONTH TO DAY,C3 DATETIME MONTH TO HOUR,C4 DATETIME MONTH TO MINUTE,C5 DATETIME MONTH TO SECOND,C6 DATETIME MONTH TO FRACTION(1),C7 DATETIME MONTH TO FRACTION(2),C8 DATETIME MONTH TO FRACTION(3),C9 DATETIME MONTH TO FRACTION(4),C10 DATETIME MONTH TO FRACTION(5), C11 DATETIME MONTH TO FRACTION(6))");
	TCHAR	*InsTabMMTO = _T("INSERT INTO TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLMMTO(C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11) VALUES (?,?,?,?,?,?,?,?,?,?,?)");
	TCHAR	*SelTabMMTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11 FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLMMTO");
	
	//DDTO...
	TCHAR	*DrpTabDDTO = _T("DROP TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLDDTO");
	TCHAR	*DelTabDDTO = _T("DELETE FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLDDTO");
	TCHAR	*CrtTabDDTO = _T("CREATE TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLDDTO(C1 DATETIME DAY,C2 DATETIME DAY TO HOUR,C3 DATETIME DAY TO MINUTE,C4 DATETIME DAY TO SECOND,C5 DATETIME DAY TO FRACTION(1),C6 DATETIME DAY TO FRACTION(2),C7 DATETIME DAY TO FRACTION(3),C8 DATETIME DAY TO FRACTION(4),C9 DATETIME DAY TO FRACTION(5), C10 DATETIME DAY TO FRACTION(6))");
	TCHAR	*InsTabDDTO = _T("INSERT INTO TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLDDTO(C1,C2,C3,C4,C5,C6,C7,C8,C9,C10) VALUES (?,?,?,?,?,?,?,?,?,?)");	
	TCHAR	*SelTabDDTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10 FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLDDTO");
	
	//HHTO...
	TCHAR	*DrpTabHHTO = _T("DROP TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLHHTO");
	TCHAR	*DelTabHHTO = _T("DELETE FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLHHTO");
	TCHAR	*CrtTabHHTO = _T("CREATE TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLHHTO(C1 DATETIME HOUR,C2 DATETIME HOUR TO MINUTE,C3 DATETIME HOUR TO SECOND,C4 DATETIME HOUR TO FRACTION(1),C5 DATETIME HOUR TO FRACTION(2),C6 DATETIME HOUR TO FRACTION(3),C7 DATETIME HOUR TO FRACTION(4),C8 DATETIME HOUR TO FRACTION(5), C9 DATETIME HOUR TO FRACTION(6))");
	TCHAR	*InsTabHHTO = _T("INSERT INTO TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLHHTO(C1,C2,C3,C4,C5,C6,C7,C8,C9) VALUES (?,?,?,?,?,?,?,?,?)");
	TCHAR	*SelTabHHTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9 FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLHHTO");
	
	//MNTO...
	TCHAR	*DrpTabMNTO = _T("DROP TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLMNTO");
	TCHAR	*DelTabMNTO = _T("DELETE FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLMNTO");
	TCHAR	*CrtTabMNTO = _T("CREATE TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLMNTO(C1 DATETIME MINUTE,C2 DATETIME MINUTE TO SECOND,C3 DATETIME MINUTE TO FRACTION(1),C4 DATETIME MINUTE TO FRACTION(2),C5 DATETIME MINUTE TO FRACTION(3),C6 DATETIME MINUTE TO FRACTION(4),C7 DATETIME MINUTE TO FRACTION(5), C8 DATETIME MINUTE TO FRACTION(6))");
	TCHAR	*InsTabMNTO = _T("INSERT INTO TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLMNTO(C1,C2,C3,C4,C5,C6,C7,C8) VALUES (?,?,?,?,?,?,?,?)");
	TCHAR	*SelTabMNTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8 FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLMNTO");
	
	//SSTO...
	TCHAR	*DrpTabSSTO = _T("DROP TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLSSTO");
	TCHAR	*DelTabSSTO = _T("DELETE FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLSSTO");
	TCHAR	*CrtTabSSTO = _T("CREATE TABLE TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLSSTO(C1 DATETIME SECOND,C2 DATETIME SECOND TO FRACTION(1),C3 DATETIME SECOND TO FRACTION(2),C4 DATETIME SECOND TO FRACTION(3),C5 DATETIME SECOND TO FRACTION(4),C6 DATETIME SECOND TO FRACTION(5), C7 DATETIME SECOND TO FRACTION(6))");
	TCHAR	*InsTabSSTO = _T("INSERT INTO TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLSSTO(C1,C2,C3,C4,C5,C6,C7) VALUES (?,?,?,?,?,?,?)");
	TCHAR	*SelTabSSTO = _T("SELECT C1,C2,C3,C4,C5,C6,C7 FROM TANDEM_SYSTEM_NSK.ODBC_SCHEMA.CSQLSSTO");
	

	SQLLEN			InValue = SQL_NTS;
	time_t now;
	struct tm *timeArray;
	static TCHAR dateBuffer[12];
	
	TCHAR	State[STATE_SIZE];
	SDWORD	NativeError;
	TCHAR	buf[MAX_STRING_SIZE];

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing => Partial DateTime Output Conversions.\n"));
	LogMsg(NONE, _T(""));
	TEST_INIT;

	TESTCASE_BEGIN("Connection for partial datetime output conversion tests\n");

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
					
	_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table. \n %s\n"),CrtTabYYTO);
	TESTCASE_BEGINW(Heading);
	
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabYYTO,SQL_NTS);					//RS, create table disabled
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabYYTO,SQL_NTS);

	if (returncode != SQL_SUCCESS)
		{
			returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, hstmt, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
			if (NativeError == -3195)
			{
				LogMsg(NONE, _T("DATETIME datatype not supported\n"));
				_gTestCount--;
				FullDisconnect(pTestInfo);
				LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing => Partial DateTime Output Conversions.\n"));
			}
			else
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TEST_RETURN;
		}
	SQLExecDirect(hstmt,(SQLTCHAR*) DelTabYYTO,SQL_NTS);	//RS: Since table is not created, delete any rows
//	TESTCASE_END;

	i = 0;
	while (CDataValueYYTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialYYTO; j++)
		{
			_stprintf(Heading,_T("Set up SQLBindParameter to convert from SQL_C_TCHAR to %s\n"),CDataArgYYTO.TestSQLType[j]);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_TCHAR,
								CDataArgYYTO.SQLType[j],CDataArgYYTO.ColPrec[j],
								CDataArgYYTO.ColScale[j],CDataValueYYTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		_stprintf(Heading,_T("Inserting the data from SQL_C_TCHAR.\n"));
		TESTCASE_BEGINW(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabYYTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			_stprintf(Heading,_T("Setup for select to %s.\n"),CDataValueYYTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabYYTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueYYTO[i].CType)
				{
				case SQL_C_TCHAR:

				for (k = 0; k < MAX_PartialYYTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgYYTO.TestSQLType[k],CDataValueYYTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking data for column c%d\n"),k+1);
			
						if (_tcsnicmp(CDataValueYYTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialYYTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgYYTO.TestSQLType[k],CDataValueYYTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n"),k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						if (_tcsnicmp(CDataValueYYTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialYYTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgYYTO.TestSQLType[k],CDataValueYYTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n"),k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueYYTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialYYTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgYYTO.TestSQLType[k],CDataValueYYTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						if (CDataArgYYTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueYYTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialYYTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgYYTO.TestSQLType[k],CDataValueYYTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						if (CDataArgYYTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueYYTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueYYTO[i].OutputValue[k],CCharOutput[k]);
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

	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabYYTO,SQL_NTS);

//====================================================================================================
// converting from MMTO
					
	_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table. \n %s\n"),CrtTabMMTO);
	TESTCASE_BEGINW(Heading);
	
/*	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMMTO,SQL_NTS);				// RS: drop table disabled
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabMMTO,SQL_NTS);
	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	*/
	SQLExecDirect(hstmt,(SQLTCHAR*) DelTabMMTO,SQL_NTS);				//RS: Since we do not create table, we delete al rows
	TESTCASE_END;

	i = 0;
	while (CDataValueMMTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialMMTO; j++)
		{
			_stprintf(Heading,_T("Set up SQLBindParameter to convert from SQL_C_TCHAR to %s\n"),CDataArgMMTO.TestSQLType[j]);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_TCHAR,
								CDataArgMMTO.SQLType[j],CDataArgMMTO.ColPrec[j],
								CDataArgMMTO.ColScale[j],CDataValueMMTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		_stprintf(Heading,_T("Inserting the data from SQL_C_TCHAR.\n"));
		TESTCASE_BEGINW(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabMMTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			_stprintf(Heading,_T("Setup for select to %s.\n"),CDataValueMMTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabMMTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueMMTO[i].CType)
				{
				case SQL_C_TCHAR:

				for (k = 0; k < MAX_PartialMMTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgMMTO.TestSQLType[k],CDataValueMMTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking data for column c%d\n"),k+1);
			
						if (_tcsnicmp(CDataValueMMTO[i].OutputValue[k],CCharOutput[k],_tcslen(CDataValueMMTO[i].OutputValue[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialMMTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgMMTO.TestSQLType[k],CDataValueMMTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n"),k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						if (_tcsnicmp(CDataValueMMTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialMMTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgMMTO.TestSQLType[k],CDataValueMMTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n"),k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueMMTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialMMTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgMMTO.TestSQLType[k],CDataValueMMTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						if (CDataArgMMTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueMMTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialMMTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgMMTO.TestSQLType[k],CDataValueMMTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						if (CDataArgMMTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueMMTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMMTO[i].OutputValue[k],CCharOutput[k]);
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
		_stprintf(Heading,_T("Setup for SQLBindParameter tests for delete table %s.\n"),CDataValueMMTO[i].TestCType);
		TESTCASE_BEGINW(Heading);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTabMMTO,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			//TEST_FAILED;
			TEST_RETURN;
		}
		//TESTCASE_END;
		i++;
		
 		
	}

	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMMTO,SQL_NTS);

//====================================================================================================
// converting from DDTO
					
	_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table. \n %s\n"),CrtTabDDTO);
	TESTCASE_BEGINW(Heading);
/*	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDDTO,SQL_NTS);				// RS: drop table disabled
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabDDTO,SQL_NTS);
	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	*/
	SQLExecDirect(hstmt,(SQLTCHAR*) DelTabDDTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
	//TESTCASE_END;

	i = 0;
	while (CDataValueDDTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialDDTO; j++)
		{
			_stprintf(Heading,_T("Set up SQLBindParameter to convert from SQL_C_TCHAR to %s\n"),CDataArgDDTO.TestSQLType[j]);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_TCHAR,
								CDataArgDDTO.SQLType[j],CDataArgDDTO.ColPrec[j],
								CDataArgDDTO.ColScale[j],CDataValueDDTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		_stprintf(Heading,_T("Inserting the data from SQL_C_TCHAR.\n"));
		TESTCASE_BEGINW(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabDDTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			_stprintf(Heading,_T("Setup for select to %s.\n"),CDataValueDDTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabDDTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueDDTO[i].CType)
				{
				case SQL_C_TCHAR:

				for (k = 0; k < MAX_PartialDDTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgDDTO.TestSQLType[k],CDataValueDDTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking data for column c%d\n"),k+1);
			
						if (_tcsnicmp(CDataValueDDTO[i].OutputValue[k],CCharOutput[k],_tcslen(CDataValueDDTO[i].OutputValue[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialDDTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgDDTO.TestSQLType[k],CDataValueDDTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n"),k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						if (_tcsnicmp(CDataValueDDTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialDDTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgDDTO.TestSQLType[k],CDataValueDDTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n"),k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueDDTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialDDTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgDDTO.TestSQLType[k],CDataValueDDTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						if (CDataArgDDTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueDDTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialDDTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgDDTO.TestSQLType[k],CDataValueDDTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						if (CDataArgDDTO.SQLType[k] == SQL_DATE)
							ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueDDTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueDDTO[i].OutputValue[k],CCharOutput[k]);
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

	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDDTO,SQL_NTS);

//====================================================================================================
// converting from HHTO
					
	_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table. \n %s\n"),CrtTabHHTO);
	TESTCASE_BEGINW(Heading);
/*	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabHHTO,SQL_NTS);				//RS: Drop table disabled
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabHHTO,SQL_NTS);
	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	*/
	SQLExecDirect(hstmt,(SQLTCHAR*) DelTabHHTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
//	TESTCASE_END;

	i = 0;
	while (CDataValueHHTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialHHTO; j++)
		{
			_stprintf(Heading,_T("Set up SQLBindParameter to convert from SQL_C_TCHAR to %s\n"),CDataArgHHTO.TestSQLType[j]);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_TCHAR,
								CDataArgHHTO.SQLType[j],CDataArgHHTO.ColPrec[j],
								CDataArgHHTO.ColScale[j],CDataValueHHTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		_stprintf(Heading,_T("Inserting the data from SQL_C_TCHAR.\n"));
		TESTCASE_BEGINW(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabHHTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			_stprintf(Heading,_T("Setup for select to %s.\n"),CDataValueHHTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabHHTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueHHTO[i].CType)
				{
				case SQL_C_TCHAR:

				for (k = 0; k < MAX_PartialHHTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgHHTO.TestSQLType[k],CDataValueHHTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking data for column c%d\n"),k+1);
			
						if (_tcsnicmp(CDataValueHHTO[i].OutputValue[k],CCharOutput[k],_tcslen(CDataValueHHTO[i].OutputValue[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialHHTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgHHTO.TestSQLType[k],CDataValueHHTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n"),k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueHHTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialHHTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgHHTO.TestSQLType[k],CDataValueHHTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n"),k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						// Since we are giving only time as input the current date is inserted for date part. 
						// Hence we will change the date part of expected output to current date.
						if ( k <= 2) 
						{	_tcsncpy(CDataValueHHTO[i].OutputValue[k],dateBuffer,10);
								
						}
						if (_tcsnicmp(CDataValueHHTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialHHTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgHHTO.TestSQLType[k],CDataValueHHTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						//LogMsg(NONE,_T("Time[%d]:%d:%d:%d\n"),k+1,CTimeOutput[k].hour,CTimeOutput[k].minute,CTimeOutput[k].second);
						
						if (_tcsnicmp(CDataValueHHTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialHHTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgHHTO.TestSQLType[k],CDataValueHHTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						if (CDataArgHHTO.SQLType[k] == SQL_TIME)
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueHHTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueHHTO[i].OutputValue[k],CCharOutput[k]);
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

	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabHHTO,SQL_NTS);

//====================================================================================================
// converting from MNTO
					
	_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table. \n %s\n"),CrtTabMNTO);
	TESTCASE_BEGINW(Heading);
/*	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMNTO,SQL_NTS);				// RS: Drop table disabled
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabMNTO,SQL_NTS);
	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	*/
	SQLExecDirect(hstmt,(SQLTCHAR*) DelTabMNTO,SQL_NTS);				//RS: Since we do not create the table, we delete all rows
//	TESTCASE_END;

	i = 0;
	while (CDataValueMNTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialMNTO; j++)
		{
			_stprintf(Heading,_T("Set up SQLBindParameter to convert from SQL_C_TCHAR to %s\n"),CDataArgMNTO.TestSQLType[j]);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_TCHAR,
								CDataArgMNTO.SQLType[j],CDataArgMNTO.ColPrec[j],
								CDataArgMNTO.ColScale[j],CDataValueMNTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		_stprintf(Heading,_T("Inserting the data from SQL_C_TCHAR.\n"));
		TESTCASE_BEGINW(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabMNTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			_stprintf(Heading,_T("Setup for select to %s.\n"),CDataValueMNTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabMNTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueMNTO[i].CType)
				{
				case SQL_C_TCHAR:

				for (k = 0; k < MAX_PartialMNTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgMNTO.TestSQLType[k],CDataValueMNTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking data for column c%d\n"),k+1);
			
						if (_tcsnicmp(CDataValueMNTO[i].OutputValue[k],CCharOutput[k],_tcslen(CDataValueMNTO[i].OutputValue[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialMNTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgMNTO.TestSQLType[k],CDataValueMNTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n"),k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						if (_tcsnicmp(CDataValueMNTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialMNTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgMNTO.TestSQLType[k],CDataValueMNTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n"),k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						// Since we are giving only time as input the current date is inserted for date part. 
						// Hence we will change the date part of expected output to current date.
						if ( k <= 1) 
						{	_tcsncpy(CDataValueMNTO[i].OutputValue[k],dateBuffer,10);
								
						}
						if (_tcsnicmp(CDataValueMNTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialMNTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgMNTO.TestSQLType[k],CDataValueMNTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueMNTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialMNTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgMNTO.TestSQLType[k],CDataValueMNTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						if (CDataArgMNTO.SQLType[k] == SQL_TIME)
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueMNTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueMNTO[i].OutputValue[k],CCharOutput[k]);
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

SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMNTO,SQL_NTS);

//====================================================================================================
// converting from SSTO
					
	_stprintf(Heading,_T("Setup for SQLBindParameter tests for create table. \n %s\n"),CrtTabSSTO);
	TESTCASE_BEGINW(Heading);
/*	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabSSTO,SQL_NTS);				//RS: drop table disabled
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabSSTO,SQL_NTS);
	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	*/
	SQLExecDirect(hstmt,(SQLTCHAR*) DelTabSSTO,SQL_NTS);				//RS: since we do not create the table, we delete all rows
//	TESTCASE_END;

	i = 0;
	while (CDataValueSSTO[i].CType != 999)
	{
		for (j = 0; j < MAX_PartialSSTO; j++)
		{
			_stprintf(Heading,_T("Set up SQLBindParameter to convert from SQL_C_TCHAR to %s\n"),CDataArgSSTO.TestSQLType[j]);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_TCHAR,
								CDataArgSSTO.SQLType[j],CDataArgSSTO.ColPrec[j],
								CDataArgSSTO.ColScale[j],CDataValueSSTO[i].InputValue[j],NAME_LEN,&InValue);
			
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		}
	
		_stprintf(Heading,_T("Inserting the data from SQL_C_TCHAR.\n"));
		TESTCASE_BEGINW(Heading);
		
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTabSSTO,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		if ((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO))
		{
			_stprintf(Heading,_T("Setup for select to %s.\n"),CDataValueSSTO[i].TestCType);
			TESTCASE_BEGINW(Heading);
			
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabSSTO,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{	
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				switch (CDataValueSSTO[i].CType)
				{
				case SQL_C_TCHAR:

				for (k = 0; k < MAX_PartialSSTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgSSTO.TestSQLType[k],CDataValueSSTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking data for column c%d\n"),k+1);
			
						if (_tcsnicmp(CDataValueSSTO[i].OutputValue[k],CCharOutput[k],_tcslen(CDataValueSSTO[i].OutputValue[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_DATE:
				for (k = 0; k < MAX_PartialSSTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgSSTO.TestSQLType[k],CDataValueSSTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_DATE ctype data for column c%d\n"),k+1);
			
						ConvertDateToString(&CDateOutput[k],CCharOutput[k]);
						if (_tcsnicmp(CDataValueSSTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIMESTAMP:
				for (k = 0; k < MAX_PartialSSTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgSSTO.TestSQLType[k],CDataValueSSTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					
					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIMESTAMP ctype data for column c%d\n"),k+1);
						ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						// Since we are giving only time as input the current date is inserted for date part. 
						// Hence we will change the date part of expected output to current date.
						if ( k == 0) 
						{	_tcsncpy(CDataValueSSTO[i].OutputValue[k],dateBuffer,10);
								
						}
						if (_tcsnicmp(CDataValueSSTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;

				case SQL_C_TIME:
				for (k = 0; k < MAX_PartialSSTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgSSTO.TestSQLType[k],CDataValueSSTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueSSTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}
						free(CCharOutput[k]);
					} // end for loop
				}
				break;
				case SQL_C_DEFAULT:
				for (k = 0; k < MAX_PartialSSTO; k++)
				{  
					_stprintf(Heading,_T("SQLBindCol: Positive test #%d for converting %s to %s before fetch.\n"),k+1,CDataArgSSTO.TestSQLType[k],CDataValueSSTO[i].TestCType);
					TESTCASE_BEGINW(Heading);
					

					CCharOutput[k] = (TCHAR *)malloc(NAME_LEN);
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
						//LogMsg(NONE,_T("SQLBindCol test: checking SQL_C_TIME ctype data for column c%d\n"),k+1);
						
						if (CDataArgSSTO.SQLType[k] == SQL_TIME)
							ConvertTimeToString(&CTimeOutput[k],CCharOutput[k]);
						else
							ConvertTimestampToString(&CTimeStampOutput[k],CCharOutput[k]);
						
						if (_tcsnicmp(CDataValueSSTO[i].OutputValue[k],CCharOutput[k],_tcslen(CCharOutput[k])) == 0)
						{
							//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %s	and actual: %s are not matched\n"),CDataValueSSTO[i].OutputValue[k],CCharOutput[k]);
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

SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabSSTO,SQL_NTS);

FullDisconnect(pTestInfo);
LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing => Partial DateTime Output Conversions.\n"));
TEST_RETURN;

}

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

#define NAME_LEN		300

#ifdef UNICODE
	#define	MAX_BINDPARAM1	28
#else
	#define	MAX_BINDPARAM1	25
#endif

#define MAX_PUTPARAM2	14
#define	MAX_PUTPARAM3	14
#define MAX_PUTPARAM4	9
#define MAX_PUTPARAM5   14
#define BIG_NUM_PARAM	8

#ifndef _WM
	#define DATE_FORMAT			_T("1993-12-30")
	#define FLOAT_FORMAT		_T("0.123456")
	#define FLOAT_FORMAT_N		_T("-0.123456")
	#define FLOAT_FORMAT_E		_T("0.12345678")
	#define DOUBLE_FORMAT		_T("0.123456789123456")
	#define DOUBLE_FORMAT_N		_T("-0.123456789123456")
	#define DOUBLE_FORMAT_L		_T("0.1234567891")
	#define DOUBLE_FORMAT_LN	_T("-0.1234567891")
#else
	#define DATE_FORMAT			_T("93/12/30")
	#define FLOAT_FORMAT		_T(".123456")
	#define FLOAT_FORMAT_N		_T("-.123456")
	#define FLOAT_FORMAT_E		_T(".12345678")
	#define DOUBLE_FORMAT		_T(".123456789123456")
	#define DOUBLE_FORMAT_N		_T("-.123456789123456")
	#define DOUBLE_FORMAT_L		_T(".1234567891")
	#define DOUBLE_FORMAT_LN	_T("-.1234567891")
#endif

PassFail TestMXSQLPutData(TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	TCHAR				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode, rc;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	short				i, j, k, h, maxloop;
	short				TestId;
	SQLSMALLINT			ParamType = SQL_PARAM_INPUT;

	struct // We have to support bit, tinyint, binary, varbinary, long varbinary
	{
		SQLSMALLINT	SQLType[MAX_BINDPARAM1];
	} CDataArgToSQL1 = 
		{
			SQL_CHAR, SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT, SQL_INTEGER,    SQL_REAL,
			SQL_FLOAT,SQL_DOUBLE, SQL_DATE,   SQL_TIME,   SQL_TIMESTAMP,SQL_LONGVARCHAR,SQL_BIGINT,
			#ifndef UNICODE
			SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			#endif
			SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC
			#ifdef UNICODE
			,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR
			#endif
		};

	struct
	{
		SQLSMALLINT			CType;
		TCHAR				*CrtCol;
		SQLUINTEGER			ColPrec[MAX_BINDPARAM1];
		SQLSMALLINT			ColScale[MAX_BINDPARAM1];
		int					PutLoop;
		TCHAR				*OutputValue[MAX_BINDPARAM1];
		TCHAR				*expectedValue[MAX_BINDPARAM1];
	} CDataValueTOSQL1[] = 
		{			// real, float and double precision to TCHAR has problem it returns 12345.0 values as 12345.
#ifdef UNICODE
			{	SQL_C_TCHAR,
				_T("--"),
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,19,19,128,128,128,10,18,30,254,254,2000,254,254,2000,
				0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,6,0,128,64,5,5,10,0,0,0,0,0,0,
				1,
				_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("123456"),_T("1234567890123456789"),_T("1234567890123.456789"),_T("1234567890123456789012345678901234567890"),_T("0.123456789012345678901234567890123456789"),_T("1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),
	#ifndef _WM
				_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("123456"),_T("1234567890123456789"),_T("1234567890123.456789"),_T("1234567890123456789012345678901234567890"),_T("0.123456789012345678901234567890123456789"),_T("1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
	#else
				_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),_T("93/12/30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("123456"),_T("1234567890123456789"),_T("1234567890123.456789"),_T("1234567890123456789012345678901234567890"),_T(".123456789012345678901234567890123456789"),_T("1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
	#endif
			},
			{	SQL_C_TCHAR,
				_T("--"),
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,19,19,128,128,128,10,18,30,254,254,2000,254,254,2000,
				0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,6,0,128,64,5,5,10,0,0,0,0,0,0,
				4,
				_T("--"),_T("--"),_T("-1234.56789"),_T("-5678.12345"),_T("-1234"),_T("-12345"),_T("-12340.0"),_T("-12300.0"),_T("-12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("-123456"),_T("-1234567890123456789"),_T("-1234567890123.456789"),_T("-1234567890123456789012345678901234567890"),_T("-0.123456789012345678901234567890123456789"),_T("-1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),
	#ifndef _WM
				_T("--"),_T("--"),_T("-1234.56789"),_T("-5678.12345"),_T("-1234"),_T("-12345"),_T("-12340.0"),_T("-12300.0"),_T("-12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("-123456"),_T("-1234567890123456789"),_T("-1234567890123.456789"),_T("-1234567890123456789012345678901234567890"),_T("-0.123456789012345678901234567890123456789"),_T("-1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
	#else
				_T("--"),_T("--"),_T("-1234.56789"),_T("-5678.12345"),_T("-1234"),_T("-12345"),_T("-12340.0"),_T("-12300.0"),_T("-12345670.0"),_T("93/12/30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("-123456"),_T("-1234567890123456789"),_T("-1234567890123.456789"),_T("-1234567890123456789012345678901234567890"),_T("-.123456789012345678901234567890123456789"),_T("-1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
	#endif
			},
#else
			{	SQL_C_TCHAR,
				_T("--"),
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,254,254,2000,19,19,128,128,128,10,18,30,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,0,0,   0,0,  0,  0, 0, 6, 0,  128,64, 5, 5, 10,
				1,
				_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("123456"),_T("--"),_T("--"),_T("--"),_T("1234567890123456789"),_T("1234567890123.456789"),_T("1234567890123456789012345678901234567890"),_T("0.123456789012345678901234567890123456789"),_T("1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),
	#ifndef _WM
				_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("123456"),_T("--"),_T("--"),_T("--"),_T("1234567890123456789"),_T("1234567890123.456789"),_T("1234567890123456789012345678901234567890"),_T("0.123456789012345678901234567890123456789"),_T("1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789")
	#else
				_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),_T("93/12/30"),  _T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("123456"),_T("--"),_T("--"),_T("--"),_T("1234567890123456789"),_T("1234567890123.456789"),_T("1234567890123456789012345678901234567890"),_T(".123456789012345678901234567890123456789"), _T("1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789")
	#endif
			},
			{	SQL_C_TCHAR,
				_T("--"),
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,254,254,2000,19,19,128,128,128,10,18,30,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,0,0,   0,0,  0,  0,   0, 6, 0,  128,64, 5,  5,10,
				4,
				_T("--"),_T("--"),_T("-1234.56789"),_T("-5678.12345"),_T("-1234"),_T("-12345"),_T("-12340.0"),_T("-12300.0"),_T("-12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("-123456"),_T("--"),_T("--"),_T("--"),_T("-1234567890123456789"),_T("-1234567890123.456789"),_T("-1234567890123456789012345678901234567890"),_T("-0.123456789012345678901234567890123456789"),_T("-1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),
	#ifndef _WM
				_T("--"),_T("--"),_T("-1234.56789"),_T("-5678.12345"),_T("-1234"),_T("-12345"),_T("-12340.0"),_T("-12300.0"),_T("-12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("-123456"),_T("--"),_T("--"),_T("--"),_T("-1234567890123456789"),_T("-1234567890123.456789"),_T("-1234567890123456789012345678901234567890"),_T("-0.123456789012345678901234567890123456789"),_T("-1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789")
	#else
				_T("--"),_T("--"),_T("-1234.56789"),_T("-5678.12345"),_T("-1234"),_T("-12345"),_T("-12340.0"),_T("-12300.0"),_T("-12345670.0"),_T("93/12/30"),  _T("11:45:23"),_T("1992-12-31 23:45:23.123456"),_T("--"),_T("-123456"),_T("--"),_T("--"),_T("--"),_T("-1234567890123456789"),_T("-1234567890123.456789"),_T("-1234567890123456789012345678901234567890"),_T("-.123456789012345678901234567890123456789"), _T("-1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789")
	#endif
			},
#endif
			{	999,
			}
		};

	TCHAR	*DrpTab1;
	TCHAR	*CrtTab1;
	TCHAR	*InsTab1;
	TCHAR	*SelTab1;

	//=====================================================================================
	struct // We have to support bit, tinyint
	{
		TCHAR		*TestSQLType[MAX_PUTPARAM2];
		SQLSMALLINT	SQLType[MAX_PUTPARAM2];
		SQLUINTEGER	ColPrec[MAX_PUTPARAM2];
		SQLSMALLINT	ColScale[MAX_PUTPARAM2];
	} CDataArgToSQL2 = {
#ifdef UNICODE
			_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_REAL"),_T("SQL_FLOAT"),_T("SQL_DOUBLE"),_T("SQL_WLONGVARCHAR"),_T("SQL_BIGINT"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_WCHAR,SQL_WVARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_WLONGVARCHAR,SQL_BIGINT,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
#else
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_REAL"),_T("SQL_FLOAT"),_T("SQL_DOUBLE"),_T("SQL_LONGVARCHAR"),_T("SQL_BIGINT"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_LONGVARCHAR,SQL_BIGINT,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
#endif
			254,254,10,10,5,10,7,15,15,2000,19,254,254,2000,
			0,0,5,5,0,0,0,0,0,0,0,0,0,0};
	
	struct
	{
		SCHAR		CSTINTTOSQL[MAX_PUTPARAM2];
		UCHAR		CUTINTTOSQL[MAX_PUTPARAM2];
		SCHAR		CTINTTOSQL[MAX_PUTPARAM2];
		SWORD		CSSHORTTOSQL[MAX_PUTPARAM2];
		UWORD		CUSHORTTOSQL[MAX_PUTPARAM2];
		SWORD		CSHORTTOSQL[MAX_PUTPARAM2];
		SDWORD		CSLONGTOSQL[MAX_PUTPARAM2];
		UDWORD		CULONGTOSQL[MAX_PUTPARAM2];
		SDWORD		CLONGTOSQL[MAX_PUTPARAM2];
	} CDataTypeTOSQL2 = {
				{-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123},
				{ 123,123,123,123,123,123,123,123,123,123,123,123,123,123},
				{-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123},
				{-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234},
				{ 1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234},
				{-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234},
				{-12345,-12345,-12345,-12345,-1234,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345},
				{ 12345,12345,12345,12345,1234,12345,12345,12345,12345,12345,12345,12345,12345,12345},
				{-12345,-12345,-12345,-12345,-1234,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345}
			};

	//TCHAR		CUTINTTOSQL[MAX_PUTPARAM2] =  { 123,123,123,123,123,123,123,123,123,123,123,123,123,123};
	int		CUTINTTOSQL[MAX_PUTPARAM2] =  { 123,123,123,123,123,123,123,123,123,123,123,123,123,123};

	int temp;

	struct
	{
		SQLSMALLINT			CType;
		TCHAR				*TestCType;
		TCHAR				*OutputValue[MAX_PUTPARAM2];
	} CDataValueTOSQL2[] = {
		{SQL_C_STINYINT,_T("SQL_C_STINYINT"),_T("-123"),_T("-123"),_T("-123.0"),_T("-123.0"),_T("-123"),_T("-123"),_T("-123.0"),_T("-123.0"),_T("-123.0"),_T("-123"),_T("-123"),_T("-123"),_T("-123"),_T("-123")},
		{SQL_C_UTINYINT,_T("SQL_C_UTINYINT"),_T("123"),_T("123"),_T("123.0"),_T("123.0"),_T("123"),_T("123"),_T("123.0"),_T("123.0"),_T("123.0"),_T("123"),_T("123"),_T("123"),_T("123"),_T("123")},
		{SQL_C_TINYINT,_T("SQL_C_TINYINT"),_T("-123"),_T("-123"),_T("-123.0"),_T("-123.0"),_T("-123"),_T("-123"),_T("-123.0"),_T("-123.0"),_T("-123.0"),_T("-123"),_T("-123"),_T("-123"),_T("-123"),_T("-123")},
		{SQL_C_SSHORT,_T("SQL_C_SSHORT"),_T("-1234"),_T("-1234"),_T("-1234.0"),_T("-1234.0"),_T("-1234"),_T("-1234"),_T("-1234.0"),_T("-1234.0"),_T("-1234.0"),_T("-1234"),_T("-1234"),_T("-1234"),_T("-1234"),_T("-1234")},
		{SQL_C_USHORT,_T("SQL_C_USHORT"),_T("1234"),_T("1234"),_T("1234.0"),_T("1234.0"),_T("1234"),_T("1234"),_T("1234.0"),_T("1234.0"),_T("1234.0"),_T("1234"),_T("1234"),_T("1234"),_T("1234"),_T("1234")},
		{SQL_C_SHORT,_T("SQL_C_SHORT"),_T("-1234"),_T("-1234"),_T("-1234.0"),_T("-1234.0"),_T("-1234"),_T("-1234"),_T("-1234.0"),_T("-1234.0"),_T("-1234.0"),_T("-1234"),_T("-1234"),_T("-1234"),_T("-1234"),_T("-1234")},
		{SQL_C_SLONG,_T("SQL_C_SLONG"),_T("-12345"),_T("-12345"),_T("-12345.0"),_T("-12345.0"),_T("-1234"),_T("-12345"),_T("-12345.0"),_T("-12345.0"),_T("-12345.0"),_T("-12345"),_T("-12345"),_T("-12345"),_T("-12345"),_T("-12345")},
		{SQL_C_ULONG,_T("SQL_C_ULONG"),_T("12345"),_T("12345"),_T("12345.0"),_T("12345.0"),_T("1234"),_T("12345"),_T("12345.0"),_T("12345.0"),_T("12345.0"),_T("12345"),_T("12345"),_T("12345"),_T("12345"),_T("12345")},
		{SQL_C_LONG,_T("SQL_C_LONG"),_T("-12345"),_T("-12345"),_T("-12345.0"),_T("-12345.0"),_T("-1234"),_T("-12345"),_T("-12345.0"),_T("-12345.0"),_T("-12345.0"),_T("-12345"),_T("-12345"),_T("-12345"),_T("-12345"),_T("-12345")},
		{999,}
		};

	TCHAR	*DrpTab2;
	TCHAR	*DelTab2;
	TCHAR	*CrtTab2;
	TCHAR	*InsTab2;
	TCHAR	*SelTab2;
	
	//=======================================================================================
	struct // We have to support bit, tinyint
	{
		TCHAR				*TestSQLType[MAX_PUTPARAM3];
		SQLSMALLINT	SQLType[MAX_PUTPARAM3];
		SQLUINTEGER	ColPrec[MAX_PUTPARAM3];
		SQLSMALLINT	ColScale[MAX_PUTPARAM3];
	} CDataArgToSQL3 = {
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_REAL"),_T("SQL_FLOAT"),_T("SQL_DOUBLE"),_T("SQL_LONGVARCHAR"),_T("SQL_BIGINT"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_LONGVARCHAR,SQL_BIGINT,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,10,10,5,10,7,15,15,2000,19,254,127,2000,
			0,0,5,5,0,0,0,0,0,0,0,0,0,0};

	struct
	{
		SFLOAT	CFLOATTOSQL[MAX_PUTPARAM3];
		SDOUBLE	CDOUBLETOSQL[MAX_PUTPARAM3];
	} CDataTypeTOSQL3 = {
		{(float)12345.67,(float)12345.67,(float)12345.67,(float)12345.67,(float)1234,(float)12345,(float)12345.67,(float)12345.67,(float)123456.78,(float)12345.67,(float)123456,(float)12345.67,(float)12345.67,(float)12345.67},
		{12345.67,12345.67,12345.67,12345.67,1234,12345,12345.67,12345.67,123456.78,12345.67,1234567,12345.67,12345.67,12345.67}
		};

	struct
	{
		SQLSMALLINT			CType;
		TCHAR				*TestCType;
		TCHAR				*OutputValue[MAX_PUTPARAM3];
	} CDataValueTOSQL3[] = {
		{SQL_C_FLOAT,_T("SQL_C_FLOAT"),_T("12345.67"),_T("12345.67"),_T("12345.67"),_T("12345.67"),_T("1234"),_T("12345"),_T("12345.67"),_T("12345.67"),_T("123456.78"),_T("12345.67"),_T("123456"),_T("12345.67"),_T("12345.67"),_T("12345.67")},
		{SQL_C_DOUBLE,_T("SQL_C_DOUBLE"),_T("12345.67"),_T("12345.67"),_T("12345.67"),_T("12345.67"),_T("1234"),_T("12345"),_T("12345.67"),_T("12345.67"),_T("123456.78"),_T("12345.67"),_T("1234567"),_T("12345.67"),_T("12345.67"),_T("12345.67")},
		{999,}
		};

	TCHAR	*DrpTab3;
	TCHAR	*DelTab3;
	TCHAR	*CrtTab3;
	TCHAR	*InsTab3;
	TCHAR	*SelTab3;

	//=========================================================================================
	struct // We have to support longvarchar
	{
		TCHAR				*TestSQLType[MAX_PUTPARAM4];
		SQLSMALLINT	SQLType[MAX_PUTPARAM4];
		SQLUINTEGER	ColPrec[MAX_PUTPARAM4];
		SQLSMALLINT	ColScale[MAX_PUTPARAM4];
	} CDataArgToSQL4 = {
			_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DATE"),_T("SQL_TIME"),_T("SQL_TIMESTAMP"),_T("SQL_LONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
			SQL_CHAR,SQL_VARCHAR,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_LONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			254,254,0,0,0,2000,254,254,2000,
			0,0,0,0,0,0,0,0,0};

	struct
	{
		short int	year;
		unsigned short int	month;
		unsigned short int	day;
	} CDATETOSQL = {1993,12,30};

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
		unsigned int		fraction;
	} CTIMESTAMPTOSQL = {1993,12,30,11,33,41,123456000};

	struct
	{
		SQLSMALLINT	CType;
		TCHAR				*TestCType;
		TCHAR				*OutputValue[MAX_PUTPARAM4];
//		TCHAR				OutputValue[MAX_PUTPARAM4][30];
	} CDataValueTOSQL4[4] = {
//#ifndef unixcli
		{SQL_C_DATE,		_T("SQL_C_DATE"),		_T("1993-12-30"),					_T("1993-12-30"),					DATE_FORMAT,	_T("11:33:41"),_T("1993-12-30"),				_T("1993-12-30"),					_T("1993-12-30"),					_T("1993-12-30"),					_T("1993-12-30")},
		{SQL_C_TIME,		_T("SQL_C_TIME"),		_T("11:33:41"),						_T("11:33:41"),						DATE_FORMAT,	_T("11:33:41"),_T("11:33:41"),					_T("11:33:41"),						_T("11:33:41"),						_T("11:33:41"),						_T("11:33:41")},
		{SQL_C_TIMESTAMP,	_T("SQL_C_TIMESTAMP"),	_T("1993-12-30 11:33:41.123456"),	_T("1993-12-30 11:33:41.123456"),	DATE_FORMAT,	_T("11:33:41"),_T("1993-12-30 11:33:41.123456"),_T("1993-12-30 11:33:41.123456"),	_T("1993-12-30 11:33:41.123456"),	_T("1993-12-30 11:33:41.123456"),	_T("1993-12-30 11:33:41.123456")},
		{999,}
//#endif
		};

	TCHAR	*DrpTab4;
	TCHAR	*DelTab4;
	TCHAR	*CrtTab4;
	TCHAR	*InsTab4;
	TCHAR	*SelTab4;

	TCHAR	tmpbuf[30], tmpbuf1[30];

	//===============================================================================
	struct // We have to support bit, tinyint, binary, varbinary, long varbinary
	{
		SQLSMALLINT	SQLType[MAX_BINDPARAM1];
	} CDataArgToSQL5 = 
		{
#ifdef UNICODE
			SQL_WCHAR, SQL_WVARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT, SQL_INTEGER,    SQL_REAL,
			SQL_FLOAT,SQL_DOUBLE, SQL_DATE,   SQL_TIME,   SQL_TIMESTAMP,SQL_WLONGVARCHAR,SQL_BIGINT,
			SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,
			SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR
#else
			SQL_CHAR, SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT, SQL_INTEGER,    SQL_REAL,
			SQL_FLOAT,SQL_DOUBLE, SQL_DATE,   SQL_TIME,   SQL_TIMESTAMP,SQL_LONGVARCHAR,SQL_BIGINT,
			SQL_WCHAR,SQL_WVARCHAR,SQL_WLONGVARCHAR,
			SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC
#endif
		};

	struct
	{
		SQLSMALLINT			CType;
		TCHAR				*CrtCol;
		SQLUINTEGER			ColPrec[MAX_BINDPARAM1];
		SQLSMALLINT			ColScale[MAX_BINDPARAM1];
		TCHAR				*CharValue;
		TCHAR				*VarCharValue;
		char				*DecimalValue;
		char				*NumericValue;
		SWORD				ShortValue;
		SDWORD				LongValue;
		SFLOAT				RealValue;
		SDOUBLE				FloatValue;
		SDOUBLE				DoubleValue;
		struct
		{
			short int	year;
			unsigned short int	month;
			unsigned short int	day;
		} DateValue;
		struct
		{
			unsigned short int	hour;
			unsigned short int	minute;
			unsigned short int	second;
		} TimeValue;

		struct
		{
			short int	year;
			unsigned short int	month;
			unsigned short int	day;
			unsigned short int	hour;
			unsigned short int	minute;
			unsigned short int	second;
			unsigned int		fraction;
		} TimestampValue;
		TCHAR				*LongVarCharValue;
		char				*BigintValue;

#ifndef UNICODE
		TCHAR				*NChar;
		TCHAR				*NCharVarying;
		TCHAR				*NLongCharVarying;
#endif
		char				*BigNumValue[BIG_NUM_PARAM];
#ifdef UNICODE
		TCHAR				*NChar;
		TCHAR				*NCharVarying;
		TCHAR				*NLongCharVarying;
        TCHAR               *UTF8CharValue;
        TCHAR               *UTF8VarCharValue;
        TCHAR               *UTF8LongVarCharValue;
#endif
		TCHAR				*OutputValue[MAX_BINDPARAM1];
	} CDataValueTOSQL5[] = 
		{			// real, float and double precision to TCHAR has problem it returns 12345.0 values as 12345.
#ifdef UNICODE
			{	SQL_C_DEFAULT,
				_T("--"),
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,19,19,128,128,128,10,18,30,254,254,2000,254,254,2000,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,0,0,   0,0, 6, 0,  128,64, 5,  5,10,0,0,0,0,0,0,
				_T("--"),
				_T("--"),
				"1234.56789",
				"5678.12345",
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,123456},
				_T("--"),
				"123456",
				"1234567890123456789","1234567890123.456789","1234567890123456789012345678901234567890","0.123456789012345678901234567890123456789","1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789",
				_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),
#ifndef _WM
				_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1997-10-12 11:33:41.000123"),_T("--"),_T("123456"),_T("1234567890123456789"),_T("1234567890123.456789"),_T("1234567890123456789012345678901234567890"),_T("0.123456789012345678901234567890123456789"),_T("1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
#else
				_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),"93/12/30",_T("11:45:23"),_T("1997-10-12 11:33:41.000123"),_T("--"),_T("123456"),_T("1234567890123456789"),_T("1234567890123.456789"),_T("1234567890123456789012345678901234567890"),".123456789012345678901234567890123456789",_T("1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
#endif
			},
			{	SQL_C_DEFAULT,
				_T("--"),
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,19,19,128,128,128,10,18,30,254,254,2000,254,254,2000,
				0,0,5,5,0,0,0,0,0,0,0,0,0,0,0,6,0,128,64,5,5,10,0,0,0,0,0,0,
				_T("--"),
				_T("--"),
				"-1234.56789",
				"-5678.12345",
				-1234,
				-12345,
				-12340.0,
				-12300.0,
				-12345670.0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,123456789},
				_T("--"),
				"-123456",
				"-1234567890123456789","-1234567890123.456789","-1234567890123456789012345678901234567890","-0.123456789012345678901234567890123456789","-1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789",
				_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),
#ifndef _WM
				_T("--"),_T("--"),_T("-1234.56789"),_T("-5678.12345"),_T("-1234"),_T("-12345"),_T("-12340.0"),_T("-12300.0"),_T("-12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1997-10-12 11:33:41.123456"),_T("--"),_T("-123456"),_T("-1234567890123456789"),_T("-1234567890123.456789"),_T("-1234567890123456789012345678901234567890"),_T("-0.123456789012345678901234567890123456789"),_T("-1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
#else
				_T("--"),_T("--"),_T("-1234.56789"),_T("-5678.12345"),_T("-1234"),_T("-12345"),_T("-12340.0"),_T("-12300.0"),_T("-12345670.0"),"93/12/30",_T("11:45:23"),_T("1997-10-12 11:33:41.123456"),_T("--"),_T("-123456"),_T("-1234567890123456789"),_T("-1234567890123.456789"),_T("-1234567890123456789012345678901234567890"),"-.123456789012345678901234567890123456789",_T("-1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")
#endif
			},
#else
			{	SQL_C_DEFAULT,
				_T("--"),
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,254,254,2000,19,19,128,128,128,10,18,30,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,0,0,   0,0,  0,  0,   0, 6, 0,  128,64, 5, 5, 10,
				_T("--"),
				_T("--"),
				"1234.56789",
				"5678.12345",
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,123456},
				_T("--"),
				"123456",
				_T("--"),_T("--"),_T("--"),
				"1234567890123456789","1234567890123.456789","1234567890123456789012345678901234567890","0.123456789012345678901234567890123456789","1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789",
	#ifndef _WM
				_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1997-10-12 11:33:41.000123"),_T("--"),_T("123456"),_T("--"),_T("--"),_T("--"),_T("1234567890123456789"),_T("1234567890123.456789"),_T("1234567890123456789012345678901234567890"),_T("0.123456789012345678901234567890123456789"),_T("1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789")
	#else
				_T("--"),_T("--"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340.0"),_T("12300.0"),_T("12345670.0"),"93/12/30",_T("11:45:23"),_T("1997-10-12 11:33:41.000123"),_T("--"),_T("123456"),_T("--"),_T("--"),_T("--"),_T("1234567890123456789"),_T("1234567890123.456789"),_T("1234567890123456789012345678901234567890"),".123456789012345678901234567890123456789",_T("1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789")
	#endif
			},
			{	SQL_C_DEFAULT,
				_T("--"),
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,254,254,2000, 19,19,128,128,128,10,18,30,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,0,0,   0,0,  0,  0,    0, 6, 0,  128,64, 5, 5, 10,
				_T("--"),
				_T("--"),
				"-1234.56789",
				"-5678.12345",
				-1234,
				-12345,
				-12340.0,
				-12300.0,
				-12345670.0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,123456789},
				_T("--"),
				"-123456",
				_T("--"),_T("--"),_T("--"),				
				"-1234567890123456789","-1234567890123.456789","-1234567890123456789012345678901234567890","-0.123456789012345678901234567890123456789","-1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789",
	#ifndef _WM
				_T("--"),_T("--"),_T("-1234.56789"),_T("-5678.12345"),_T("-1234"),_T("-12345"),_T("-12340.0"),_T("-12300.0"),_T("-12345670.0"),_T("1993-12-30"),_T("11:45:23"),_T("1997-10-12 11:33:41.123456"),_T("--"),_T("-123456"),_T("--"),_T("--"),_T("--"),_T("-1234567890123456789"),_T("-1234567890123.456789"),_T("-1234567890123456789012345678901234567890"),_T("-0.123456789012345678901234567890123456789"),_T("-1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789")
	#else
				_T("--"),_T("--"),_T("-1234.56789"),_T("-5678.12345"),_T("-1234"),_T("-12345"),_T("-12340.0"),_T("-12300.0"),_T("-12345670.0"),"93/12/30",_T("11:45:23"),_T("1997-10-12 11:33:41.123456"),_T("--"),_T("-123456"),_T("--"),_T("--"),_T("--"),_T("-1234567890123456789"),_T("-1234567890123.456789"),_T("-1234567890123456789012345678901234567890"),"-.123456789012345678901234567890123456789",_T("-1234567890.123456789012345678901234567890123456789"),_T("12345.56789"),_T("1234567890123.56789"),_T("12345678901234567890.0123456789")
	#endif
			},
#endif
			{	999,
			}
		};

	TCHAR	*DrpTab5;
	TCHAR	*CrtTab5;
	TCHAR	*InsTab5;
	TCHAR	*SelTab5;

//	wchar_t			mbchar[256], mbvarchar[256], mblongvarchar[256];
	TCHAR			mbchar[256], mbvarchar[256], mblongvarchar[256];
#ifdef UNICODE
	wchar_t			widechar[256], widevarchar[256], widelongvarchar[256];
#else
	char			widechar[256], widevarchar[256], widelongvarchar[256];
#endif
	SQLLEN			InValue = SQL_DATA_AT_EXEC, InValue1 = SQL_DATA_AT_EXEC;
	TCHAR			OutValue[NAME_LEN];
	SQLLEN			OutValueLen;
	TCHAR			*InsStr;
	TCHAR			*TempType1,*TempType2;
	SQLPOINTER		pToken;
	
	int TIMtemp;

//************************************************
// Data structures for Testing Section #6

    TCHAR    *DrpTab6;
    TCHAR    *CrtTab6;
    TCHAR    *InsTab6;
    TCHAR    *SelTab6;

    struct {
		RETCODE		PassFail;
		TCHAR		*CrtCol;
		SQLUINTEGER	ColPrec[MAX_PUTPARAM5];
		SQLSMALLINT	ColScale[MAX_PUTPARAM5];
		SFLOAT		FloatValue[MAX_PUTPARAM5];
        TCHAR        *OutputValue[MAX_PUTPARAM5];
    } CFloatToNumeric[] = {
        {SQL_SUCCESS, 
			_T("--"),
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(float)12345678.0, (float)0.123456, (float)12.345678, (float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)12345678,
            (float)0.123456, (float)1.234567, (float)12345678.0, (float)0.123456, (float)12345678.0,(float)0.123456},
            {_T("12345678"), FLOAT_FORMAT, _T("12.345678"), _T("12345678"), FLOAT_FORMAT, _T("1.234567"), _T("12345678"), _T("12345678"),
            FLOAT_FORMAT, _T("1.234567"), _T("12345678"), FLOAT_FORMAT, _T("12345678"), FLOAT_FORMAT}
        },
        {SQL_SUCCESS, 
            _T("--"),
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {(float)12345678.0, (float)0.123456, (float)12.345678, (float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)12345678,
            (float)0.123456, (float)1.234567, (float)12345678.0, (float)0.123456, (float)12345678.0,(float)0.123456},
            {_T("12345678"), FLOAT_FORMAT, _T("12.345678"), _T("12345678"), FLOAT_FORMAT, _T("1.234567"), _T("12345678"), _T("12345678"),
            FLOAT_FORMAT, _T("1.234567"), _T("12345678"), FLOAT_FORMAT, _T("12345678"), FLOAT_FORMAT}
        },
        {SQL_SUCCESS, 
            _T("--"),
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {(float)(-123456.0), (float)(-0.123456), (float)(-12.345678), (float)(-123456.0), (float)(-0.123456), (float)(-1.234567), (float)(-123456.0), (float)(-123456),
            (float)(-0.123456), (float)(-1.234567), (float)(-123456.0), (float)(-0.123456), (float)(-123456.0),(float)(-0.123456)},
            {_T("-123456"), FLOAT_FORMAT_N, _T("-12.345678"), _T("-123456"), FLOAT_FORMAT_N, _T("-1.234567"), _T("-123456"), _T("-123456"),
            FLOAT_FORMAT_N, _T("-1.234567"), _T("-123456"), FLOAT_FORMAT_N, _T("-123456"), FLOAT_FORMAT_N}
        },
        {SQL_SUCCESS, 
            _T("--"),
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(float)(+123456.0), (float)(+0.123456), (float)(+12.345678), (float)(123456.0), (float)(0.123456), (float)(1.234567), (float)(123456.0), (float)(+123456),
            (float)(+0.123456), (float)(+1.234567), (float)(+123456.0), (float)(0.123456), (float)(123456.0), (float)(0.123456)},
            {_T("123456"), FLOAT_FORMAT, _T("12.345678"), _T("123456"), _T("0.123456"), _T("1.234567"), _T("123456"), _T("123456"),
            FLOAT_FORMAT, _T("1.234567"), _T("123456"), FLOAT_FORMAT, _T("123456"), FLOAT_FORMAT}
        },
        {SQL_SUCCESS, 
			_T("--"),
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(float)12345678.0, (float)0.12345678, (float)12.345678, (float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)12345678,
            (float)0.123456, (float)1.234567, (float)12345678.0, (float)0.123456, (float)12345678.0,(float)0.123456},
            {_T("12345678"), FLOAT_FORMAT_E, _T("12.345678"), _T("12345678"), FLOAT_FORMAT, _T("1.234567"), _T("12345678"), _T("12345678"),
            FLOAT_FORMAT, _T("1.234567"), _T("12345678"), FLOAT_FORMAT, _T("12345678"), FLOAT_FORMAT}
        },
        {999,
        }
    };

//************************************************
// Data structures for Testing Section #7

    struct {
		RETCODE		PassFail;
		TCHAR		*CrtCol;
		SQLUINTEGER	ColPrec[MAX_PUTPARAM5];
		SQLSMALLINT	ColScale[MAX_PUTPARAM5];
		SDOUBLE		DoubleValue[MAX_PUTPARAM5];
        TCHAR        *OutputValue[MAX_PUTPARAM5];
    } CDoubleToNumeric[] = {
        {SQL_SUCCESS, 
            _T("--"),
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)123456789123456.0, (double)0.123456789123456, (double)12.3456789123456, (double)123456789123456.0, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)123456789123456.0,
            (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)0.1234567891, (double)123456789123456.0,(double)0.123456789123456},
            {_T("123456789123456"), DOUBLE_FORMAT, _T("12.3456789123456"), _T("123456789123456"), DOUBLE_FORMAT, _T("1.23456789123456"), _T("123456789123456"), _T("123456789123456"),
            DOUBLE_FORMAT, _T("1.23456789123456"), _T("123456789123456"), DOUBLE_FORMAT_L, _T("123456789123456"), DOUBLE_FORMAT}
        },
        {SQL_SUCCESS, 
            _T("--"),
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {(double)123456789123456.0, (double)0.123456789123456, (double)12.3456789123456, (double)123456789123456.0, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)123456789123456.0,
            (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)0.12345678916, (double)123456789123456.0,(double)0.123456789123456},
            {_T("123456789123456"), DOUBLE_FORMAT, _T("12.3456789123456"), _T("123456789123456"), DOUBLE_FORMAT, _T("1.23456789123456"), _T("123456789123456"), _T("123456789123456"),
            DOUBLE_FORMAT, _T("1.23456789123456"), _T("123456789123456"), DOUBLE_FORMAT_L, _T("123456789123456"), DOUBLE_FORMAT}
        },
        {SQL_SUCCESS, 
            _T("--"),
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {(double)-123456789123456.0, (double)-0.123456789123456, (double)-12.3456789123456, (double)-123456789123456.0, (double)-0.123456789123456, (double)-1.23456789123456, (double)-123456789123456.0, (double)-123456789123456.0,
            (double)-0.123456789123456, (double)-1.23456789123456, (double)-123456789123456.0, (double)-0.1234567891, (double)-123456789123456.0,(double)-0.123456789123456},
            {_T("-123456789123456"), DOUBLE_FORMAT_N, _T("-12.3456789123456"), _T("-123456789123456"), DOUBLE_FORMAT_N, _T("-1.23456789123456"), _T("-123456789123456"), _T("-123456789123456"),
            DOUBLE_FORMAT_N, _T("-1.23456789123456"), _T("-123456789123456"), DOUBLE_FORMAT_LN, _T("-123456789123456"), DOUBLE_FORMAT_N}
        },
        {SQL_SUCCESS, 
            _T("--"),
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)+123456789123456.0, (double)+0.123456789123456, (double)+12.3456789123456, (double)+123456789123456.0, (double)+0.123456789123456, (double)+1.23456789123456, (double)+123456789123456.0, (double)+123456789123456.0,
            (double)+0.123456789123456, (double)+1.23456789123456, (double)+123456789123456.0, (double)+0.1234567891, (double)+123456789123456.0,(double)+0.123456789123456},
            {_T("123456789123456"), DOUBLE_FORMAT, _T("12.3456789123456"), _T("123456789123456"), DOUBLE_FORMAT, _T("1.23456789123456"), _T("123456789123456"), _T("123456789123456"),
            DOUBLE_FORMAT, _T("1.23456789123456"), _T("123456789123456"), DOUBLE_FORMAT_L, _T("123456789123456"), DOUBLE_FORMAT}

        },
        {SQL_SUCCESS, 
            _T("--"),
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)12345678.0, (double)0.12345678, (double)12.345678, (double)12345678.0, (double)0.123456, (double)1.234567, (double)12345678.0, (double)12345678,
            (double)0.123456, (double)1.234567, (double)12345678.0, (double)0.123456, (double)12345678.0,(double)0.123456},
            {_T("12345678"), FLOAT_FORMAT_E, _T("12.345678"), _T("12345678"), FLOAT_FORMAT, _T("1.234567"), _T("12345678"), _T("12345678"),
            FLOAT_FORMAT, _T("1.234567"), _T("12345678"), FLOAT_FORMAT, _T("12345678"), FLOAT_FORMAT}
        },
        {999,
        }
    };

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLPutData"), charset_file);
	if (var_list == NULL) return FAILED;

	DrpTab1 = var_mapping(_T("SQLPutData_DrpTab_1"), var_list);
	CrtTab1 = var_mapping(_T("SQLPutData_CrtTab_1"), var_list);
	InsTab1 = var_mapping(_T("SQLPutData_InsTab_1"), var_list);
	SelTab1 = var_mapping(_T("SQLPutData_SelTab_1"), var_list);

	DrpTab2 = var_mapping(_T("SQLPutData_DrpTab_2"), var_list);
	CrtTab2 = var_mapping(_T("SQLPutData_CrtTab_2"), var_list);
	InsTab2 = var_mapping(_T("SQLPutData_InsTab_2"), var_list);
	SelTab2 = var_mapping(_T("SQLPutData_SelTab_2"), var_list);
	DelTab2 = var_mapping(_T("SQLPutData_DelTab_2"), var_list);

	DrpTab3 = var_mapping(_T("SQLPutData_DrpTab_3"), var_list);
	CrtTab3 = var_mapping(_T("SQLPutData_CrtTab_3"), var_list);
	InsTab3 = var_mapping(_T("SQLPutData_InsTab_3"), var_list);
	SelTab3 = var_mapping(_T("SQLPutData_SelTab_3"), var_list);
	DelTab3 = var_mapping(_T("SQLPutData_DelTab_3"), var_list);

	DrpTab4 = var_mapping(_T("SQLPutData_DrpTab_4"), var_list);
	CrtTab4 = var_mapping(_T("SQLPutData_CrtTab_4"), var_list);
	InsTab4 = var_mapping(_T("SQLPutData_InsTab_4"), var_list);
	SelTab4 = var_mapping(_T("SQLPutData_SelTab_4"), var_list);
	DelTab4 = var_mapping(_T("SQLPutData_DelTab_4"), var_list);

	DrpTab5 = var_mapping(_T("SQLPutData_DrpTab_5"), var_list);
	CrtTab5 = var_mapping(_T("SQLPutData_CrtTab_5"), var_list);
	InsTab5 = var_mapping(_T("SQLPutData_InsTab_5"), var_list);
	SelTab5 = var_mapping(_T("SQLPutData_SelTab_5"), var_list);

	DrpTab6 = var_mapping(_T("SQLPutData_DrpTab_6"), var_list);
	CrtTab6 = var_mapping(_T("SQLPutData_CrtTab_6"), var_list);
	InsTab6 = var_mapping(_T("SQLPutData_InsTab_6"), var_list);
	SelTab6 = var_mapping(_T("SQLPutData_SelTab_6"), var_list);

	CDataValueTOSQL1[0].CrtCol = var_mapping(_T("SQLPutData_CDataValueTOSQL1_CrtCol_0"), var_list);
	CDataValueTOSQL1[0].OutputValue[0] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue0_0"), var_list);
	CDataValueTOSQL1[0].OutputValue[1] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue1_0"), var_list);
	CDataValueTOSQL1[0].OutputValue[12] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue12_0"), var_list);

#ifdef UNICODE
	CDataValueTOSQL1[0].OutputValue[22] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue22_0"), var_list);
	CDataValueTOSQL1[0].OutputValue[23] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue23_0"), var_list);
	CDataValueTOSQL1[0].OutputValue[24] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue24_0"), var_list);
	CDataValueTOSQL1[0].OutputValue[25] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue25_0"), var_list);
	CDataValueTOSQL1[0].OutputValue[26] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue26_0"), var_list);
	CDataValueTOSQL1[0].OutputValue[27] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue27_0"), var_list);
#else
	CDataValueTOSQL1[0].OutputValue[14] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue14_0"), var_list);
	CDataValueTOSQL1[0].OutputValue[15] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue15_0"), var_list);
	CDataValueTOSQL1[0].OutputValue[16] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue16_0"), var_list);
#endif

	CDataValueTOSQL1[0].expectedValue[0] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue0_0"), var_list);
	CDataValueTOSQL1[0].expectedValue[1] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue1_0"), var_list);
	CDataValueTOSQL1[0].expectedValue[12] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue12_0"), var_list);

#ifdef UNICODE
	CDataValueTOSQL1[0].expectedValue[22] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue22_0"), var_list);
	CDataValueTOSQL1[0].expectedValue[23] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue23_0"), var_list);
	CDataValueTOSQL1[0].expectedValue[24] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue24_0"), var_list);
	CDataValueTOSQL1[0].expectedValue[25] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue25_0"), var_list);
	CDataValueTOSQL1[0].expectedValue[26] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue26_0"), var_list);
	CDataValueTOSQL1[0].expectedValue[27] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue27_0"), var_list);
#else
	CDataValueTOSQL1[0].expectedValue[14] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue14_0"), var_list);
	CDataValueTOSQL1[0].expectedValue[15] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue15_0"), var_list);
	CDataValueTOSQL1[0].expectedValue[16] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue16_0"), var_list);
#endif

	CDataValueTOSQL1[1].CrtCol = var_mapping(_T("SQLPutData_CDataValueTOSQL1_CrtCol_1"), var_list);
	CDataValueTOSQL1[1].OutputValue[0] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue0_1"), var_list);
	CDataValueTOSQL1[1].OutputValue[1] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue1_1"), var_list);
	CDataValueTOSQL1[1].OutputValue[12] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue12_1"), var_list);

#ifdef UNICODE
	CDataValueTOSQL1[1].OutputValue[22] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue22_1"), var_list);
	CDataValueTOSQL1[1].OutputValue[23] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue23_1"), var_list);
	CDataValueTOSQL1[1].OutputValue[24] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue24_1"), var_list);
	CDataValueTOSQL1[1].OutputValue[25] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue25_1"), var_list);
	CDataValueTOSQL1[1].OutputValue[26] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue26_1"), var_list);
	CDataValueTOSQL1[1].OutputValue[27] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue27_1"), var_list);
#else
	CDataValueTOSQL1[1].OutputValue[14] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue14_1"), var_list);
	CDataValueTOSQL1[1].OutputValue[15] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue15_1"), var_list);
	CDataValueTOSQL1[1].OutputValue[16] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue16_1"), var_list);	
#endif

	CDataValueTOSQL1[1].expectedValue[0] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue0_1"), var_list);
	CDataValueTOSQL1[1].expectedValue[1] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue1_1"), var_list);
	CDataValueTOSQL1[1].expectedValue[12] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue12_1"), var_list);
	
#ifdef UNICODE
	CDataValueTOSQL1[1].expectedValue[22] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue22_1"), var_list);
	CDataValueTOSQL1[1].expectedValue[23] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue23_1"), var_list);
	CDataValueTOSQL1[1].expectedValue[24] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue24_1"), var_list);
	CDataValueTOSQL1[1].expectedValue[25] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue25_1"), var_list);
	CDataValueTOSQL1[1].expectedValue[26] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue26_1"), var_list);
	CDataValueTOSQL1[1].expectedValue[27] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue27_1"), var_list);
#else
	CDataValueTOSQL1[1].expectedValue[14] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue14_1"), var_list);
	CDataValueTOSQL1[1].expectedValue[15] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue15_1"), var_list);
	CDataValueTOSQL1[1].expectedValue[16] = var_mapping(_T("SQLPutData_CDataValueTOSQL1_OutputValue16_1"), var_list);
#endif
	////////////////////////////////////////////////////////////////

	CDataValueTOSQL5[0].CrtCol = var_mapping(_T("SQLPutData_CDataValueTOSQL5_CrtCol_0"), var_list);

	CDataValueTOSQL5[0].CharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_CharValue_0"), var_list);
	CDataValueTOSQL5[0].VarCharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_VarCharValue_0"), var_list);
	CDataValueTOSQL5[0].LongVarCharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_LongVarCharValue_0"), var_list);
	CDataValueTOSQL5[0].NChar = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NChar_0"), var_list);
	CDataValueTOSQL5[0].NCharVarying = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NCharVarying_0"), var_list);
	CDataValueTOSQL5[0].NLongCharVarying = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NLongCharVarying_0"), var_list);
	
	CDataValueTOSQL5[0].OutputValue[0]  = var_mapping(_T("SQLPutData_CDataValueTOSQL5_CharValue_0"), var_list);
	CDataValueTOSQL5[0].OutputValue[1]  = var_mapping(_T("SQLPutData_CDataValueTOSQL5_VarCharValue_0"), var_list);
	CDataValueTOSQL5[0].OutputValue[12] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_LongVarCharValue_0"), var_list);
	
#ifdef UNICODE
	CDataValueTOSQL5[0].UTF8CharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8CharValue_0"), var_list);
	CDataValueTOSQL5[0].UTF8VarCharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8VarCharValue_0"), var_list);
	CDataValueTOSQL5[0].UTF8LongVarCharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8LongVarCharValue_0"), var_list);

	CDataValueTOSQL5[0].OutputValue[22] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NChar_0"), var_list);
	CDataValueTOSQL5[0].OutputValue[23] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NCharVarying_0"), var_list);
	CDataValueTOSQL5[0].OutputValue[24] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NLongCharVarying_0"), var_list);
	CDataValueTOSQL5[0].OutputValue[25] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8CharValue_0"), var_list);
	CDataValueTOSQL5[0].OutputValue[26] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8VarCharValue_0"), var_list);
	CDataValueTOSQL5[0].OutputValue[27] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8LongVarCharValue_0"), var_list);	
#else
	CDataValueTOSQL5[0].OutputValue[14] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_OutputValue14_0"), var_list);
	CDataValueTOSQL5[0].OutputValue[15] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_OutputValue15_0"), var_list);
	CDataValueTOSQL5[0].OutputValue[16] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_OutputValue16_0"), var_list);	
#endif

	CDataValueTOSQL5[1].CrtCol = var_mapping(_T("SQLPutData_CDataValueTOSQL5_CrtCol_1"), var_list);

	CDataValueTOSQL5[1].CharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_CharValue_1"), var_list);
	CDataValueTOSQL5[1].VarCharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_VarCharValue_1"), var_list);
	CDataValueTOSQL5[1].LongVarCharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_LongVarCharValue_1"), var_list);

	CDataValueTOSQL5[1].NChar = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NChar_1"), var_list);
	CDataValueTOSQL5[1].NCharVarying = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NCharVarying_1"), var_list);
	CDataValueTOSQL5[1].NLongCharVarying = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NLongCharVarying_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[0]  = var_mapping(_T("SQLPutData_CDataValueTOSQL5_CharValue_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[1]  = var_mapping(_T("SQLPutData_CDataValueTOSQL5_VarCharValue_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[12] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_LongVarCharValue_1"), var_list);

#ifdef UNICODE
	CDataValueTOSQL5[1].UTF8CharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8CharValue_1"), var_list);
	CDataValueTOSQL5[1].UTF8VarCharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8VarCharValue_1"), var_list);
	CDataValueTOSQL5[1].UTF8LongVarCharValue = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8LongVarCharValue_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[22] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NChar_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[23] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NCharVarying_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[24] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_NLongCharVarying_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[25] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8CharValue_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[26] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8VarCharValue_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[27] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_UTF8LongVarCharValue_1"), var_list);
#else
	CDataValueTOSQL5[1].OutputValue[14] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_OutputValue14_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[15] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_OutputValue15_1"), var_list);
	CDataValueTOSQL5[1].OutputValue[16] = var_mapping(_T("SQLPutData_CDataValueTOSQL5_OutputValue16_1"), var_list);	

#endif


	//////////////////////////////////////////////////////////
	CFloatToNumeric[0].CrtCol = var_mapping(_T("SQLPutData_CFloatToNumeric_0"), var_list);
	CFloatToNumeric[1].CrtCol = var_mapping(_T("SQLPutData_CFloatToNumeric_1"), var_list);
	CFloatToNumeric[2].CrtCol = var_mapping(_T("SQLPutData_CFloatToNumeric_2"), var_list);
	CFloatToNumeric[3].CrtCol = var_mapping(_T("SQLPutData_CFloatToNumeric_3"), var_list);
	CFloatToNumeric[4].CrtCol = var_mapping(_T("SQLPutData_CFloatToNumeric_4"), var_list);

	CDoubleToNumeric[0].CrtCol = var_mapping(_T("SQLPutData_CDoubleToNumeric_0"), var_list);
	CDoubleToNumeric[1].CrtCol = var_mapping(_T("SQLPutData_CDoubleToNumeric_1"), var_list);
	CDoubleToNumeric[2].CrtCol = var_mapping(_T("SQLPutData_CDoubleToNumeric_2"), var_list);
	CDoubleToNumeric[3].CrtCol = var_mapping(_T("SQLPutData_CDoubleToNumeric_3"), var_list);
	CDoubleToNumeric[4].CrtCol = var_mapping(_T("SQLPutData_CDoubleToNumeric_4"), var_list);

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => MX Specific SQLParamData/SQLPutData.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLParamData/SQLPutData tests\n");

	if(!FullConnect(pTestInfo)){
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = pTestInfo->hstmt;
   	
	returncode = SQLAllocStmt(hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END; // end of setup

	TempType1 = (TCHAR *)malloc(NAME_LEN);	_tcscpy(TempType1,_T(""));
	TempType2 = (TCHAR *)malloc(NAME_LEN);	_tcscpy(TempType2,_T(""));
	InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);

//====================================================================================================
// converting from c TCHAR to all data types

	TestId=1;
	i = 0;
	while (CDataValueTOSQL1[i].CType != 999)
	{
		_stprintf(Heading,_T("Setup for SQLParamData/SQLPutData tests #%d for SQL_C_TCHAR.\n"),TestId);
		TESTCASE_BEGINW(Heading);

		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab1,SQL_NTS);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,CrtTab1);
		_tcscat(InsStr,CDataValueTOSQL1[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTab1,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		
		for (j = 0; j < MAX_BINDPARAM1; j++)
		{
			LogMsg(NONE,_T("SQLBindParameter, Column #%d, SQL_C_TCHAR to %s.\n"),j+1,SQLTypeToChar(CDataArgToSQL1.SQLType[j],TempType1));
			InValue = SQL_DATA_AT_EXEC;
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL1[i].CType,
																		CDataArgToSQL1.SQLType[j],CDataValueTOSQL1[i].ColPrec[j],
																		CDataValueTOSQL1[i].ColScale[j],NULL,NAME_LEN,
																		&InValue);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				LogAllErrors(henv,hdbc,hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
		}
	

		returncode = SQLExecute(hstmt);         // Execute statement with 
		if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
			TESTCASE_END;	// end setup
		}
		else
		{
			TESTCASE_END;	// end setup

			_stprintf(Heading,_T("Test #%d: Positive Functionality of SQLParamData/SQLPutData.\n"),TestId);
			TESTCASE_BEGINW(Heading);

			j = 0;
			while (returncode == SQL_NEED_DATA)
			{
				returncode = SQLParamData(hstmt,&pToken);
				if (returncode == SQL_NEED_DATA)
				{
					if (CDataArgToSQL1.SQLType[j] == SQL_LONGVARCHAR)
					{
						_tcscpy(TempType1,_T(""));
						maxloop = CDataValueTOSQL1[i].PutLoop;
					}
					else if (CDataArgToSQL1.SQLType[j] == SQL_WLONGVARCHAR)
					{
						_tcscpy(TempType2,_T(""));
						maxloop = CDataValueTOSQL1[i].PutLoop;
					}
					else
					{
						maxloop = 1;
					}

					for (k = 0; k < maxloop; k++)
					{
						if (CDataArgToSQL1.SQLType[j] == SQL_LONGVARCHAR)
						{
							_tcscat(TempType1,CDataValueTOSQL1[i].OutputValue[j]);
						}
						else if (CDataArgToSQL1.SQLType[j] == SQL_WLONGVARCHAR)
						{
							_tcscat(TempType2,CDataValueTOSQL1[i].OutputValue[j]);
						}
						else {}

						rc = SQLPutData(hstmt,CDataValueTOSQL1[i].OutputValue[j],SQL_NTS);//_tcslen(CDataValueTOSQL1[i].OutputValue[j])*sizeof(TCHAR));
						if(!CHECKRC(SQL_SUCCESS,rc,"SQLPutData"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
					}
					j++;
				}
				else if (returncode != SQL_SUCCESS) {
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else {}
			}

			LogMsg(NONE,_T("Getting and verifying data.\n"));
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab1,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				returncode = SQLFetch(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (j = 0; j < MAX_BINDPARAM1; j++)
					{
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (CDataArgToSQL1.SQLType[j] == SQL_LONGVARCHAR)
							{
								if (_tcscmp(TempType1,OutValue) == 0)
								{
									if(g_Trace){
										LogMsg(NONE,_T("Column %d: expect: %s and actual: %s are matched\n"),j+1,TempType1,OutValue);
										}
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("Column %d: expect: %s and actual: %s are not matched at line: %d\n"),j+1,TempType1,OutValue, __LINE__);
								}
							}
							else if (CDataArgToSQL1.SQLType[j] == SQL_WLONGVARCHAR)
							{
								if (_tcscmp(TempType2,OutValue) == 0)
								{
									if(g_Trace){
										LogMsg(NONE,_T("Column %d: expect: %s and actual: %s are matched\n"),j+1,TempType2,OutValue);
										}
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("Column %d: expect: %s and actual: %s are not matched at line: %d\n"),j+1,TempType2,OutValue, __LINE__);
								}
							}
							else
							{
								if (_tcsnicmp(CDataValueTOSQL1[i].expectedValue[j],OutValue,_tcslen(CDataValueTOSQL1[i].expectedValue[j])) == 0)
								{
									if(g_Trace){
										LogMsg(NONE,_T("Column %d: expect: %s and actual: %s are matched\n"),j+1,CDataValueTOSQL1[i].expectedValue[j],OutValue);
										}
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,_T("Column %d: expect: %s and actual: %s are not matched at line: %d\n"),j+1,CDataValueTOSQL1[i].expectedValue[j],OutValue, __LINE__);
								}
							}
						}
					} // end for loop
				}
			}
			TESTCASE_END;
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab1,SQL_NTS);
		i++;
		TestId++;
	}

//====================================================================================================
	// converting from ctinyint, cshort and clong to sql 

	_stprintf(Heading,_T("General setup for SQLParamData/SQLPutData tests for ctinyint, cshort and clong.\n"));
	TESTCASE_BEGINW(Heading);
	SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab2,SQL_NTS);
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTab2,SQL_NTS);
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;

	i = 0;
	while (CDataValueTOSQL2[i].CType != 999)
	{
		_stprintf(Heading,_T("Setup for SQLParamData/SQLPutData tests #%d for ctinyint, cshort and clong.\n"),TestId);
		TESTCASE_BEGINW(Heading);
		returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTab2,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		for (j = 0; j < MAX_PUTPARAM2; j++)
		{
			LogMsg(NONE,_T("SQLBindParameter from %s to %s\n"),CDataValueTOSQL2[i].TestCType, CDataArgToSQL2.TestSQLType[j]);
			InValue1 = SQL_DATA_AT_EXEC;
			switch (CDataValueTOSQL2[i].CType)
			{
				case SQL_C_STINYINT:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																			CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																			CDataArgToSQL2.ColScale[j],NULL,0,&InValue1);
					break;
				case SQL_C_UTINYINT:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																			CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																			CDataArgToSQL2.ColScale[j],NULL,0,&InValue1);
					break;
				case SQL_C_TINYINT:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																			CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																			CDataArgToSQL2.ColScale[j],NULL,0,&InValue1);
					break;
				case SQL_C_SSHORT:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																			CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																			CDataArgToSQL2.ColScale[j],NULL,0,&InValue1);
					break;
				case SQL_C_USHORT:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																		CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																		CDataArgToSQL2.ColScale[j],NULL,0,&InValue1);
					break;
				case SQL_C_SHORT:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																		CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																		CDataArgToSQL2.ColScale[j],NULL,0,&InValue1);
					break;
				case SQL_C_SLONG:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																		CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																		CDataArgToSQL2.ColScale[j],NULL,0,&InValue1);
					break;
				case SQL_C_ULONG:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																		CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																		CDataArgToSQL2.ColScale[j],NULL,0,&InValue1);
					break;
				case SQL_C_LONG:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																		CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																		CDataArgToSQL2.ColScale[j],NULL,0,&InValue1);
					break;
				default: ;
			}

			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
	
//		LogMsg(NONE,_T("Getting and verifying data for %s.\n"),CDataValueTOSQL2[i].TestCType);

		returncode = SQLExecute(hstmt);         // Execute statement with 
		if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecute"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TESTCASE_END;	// end setup
		}
		else
		{
			TESTCASE_END;	// end setup

			_stprintf(Heading,_T("Test #%d: Positive Functionality of SQLParamData/SQLPutData.\n"),TestId);
			TESTCASE_BEGINW(Heading);
			j = 0;
			while (returncode == SQL_NEED_DATA)
			{
				returncode = SQLParamData(hstmt,&pToken);
				if (returncode == SQL_NEED_DATA)
				{
					switch (CDataValueTOSQL2[i].CType)
					{
						case SQL_C_STINYINT:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL2.CSTINTTOSQL[j]),0);
							break;
						case SQL_C_UTINYINT:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL2.CUTINTTOSQL[j]),0);
							break;
						case SQL_C_TINYINT:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL2.CTINTTOSQL[j]),0);
							break;
						case SQL_C_SSHORT:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL2.CSSHORTTOSQL[j]),0);
							break;
						case SQL_C_USHORT:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL2.CUSHORTTOSQL[j]),0);
							break;
						case SQL_C_SHORT:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL2.CSHORTTOSQL[j]),0);
							break;
						case SQL_C_SLONG:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL2.CSLONGTOSQL[j]),0);
							break;
						case SQL_C_ULONG:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL2.CULONGTOSQL[j]),0);
							break;
						case SQL_C_LONG:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL2.CLONGTOSQL[j]),0);
							break;
						default: ;
					}
					if(!CHECKRC(SQL_SUCCESS,rc,"SQLPutData"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					j++;
				}
			}

			LogMsg(NONE,_T("Getting and verifying data for %s.\n"),CDataValueTOSQL2[i].TestCType);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab2,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				returncode = SQLFetch(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (j = 0; j < MAX_PUTPARAM2; j++)
					{
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (_tcsnicmp(CDataValueTOSQL2[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL2[i].OutputValue[j])) == 0)
							{
								if(g_Trace){
									LogMsg(NONE,_T("Column %d: expect: %s and actual: %s are matched\n"),j+1,CDataValueTOSQL2[i].OutputValue[j],OutValue);
									}
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,_T("Column %d: expect: %s and actual: %s are not matched at line: %d\n"),j+1,CDataValueTOSQL2[i].OutputValue[j],OutValue,__LINE__);
							}
						}
					} // end for loop
				}
			}
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTab2,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		i++;
		TestId++;
	}
	
//====================================================================================================
	// converting from cfloat and cdouble to sql 

	i = 0;
	while (CDataValueTOSQL3[i].CType != 999)
	{
		_stprintf(Heading,_T("Setup for SQLParamData/SQLPutData tests #%d for cfloat and cdouble\n"),TestId);
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab3,SQL_NTS);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTab3,SQL_NTS);
	 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		LogMsg(NONE,_T("Prepare for %s.\n"),CDataValueTOSQL3[i].TestCType);
		returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTab3,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		for (j = 0; j < MAX_PUTPARAM3; j++)
		{
			LogMsg(NONE,_T("SQLBindParameter to convert from %s to %s\n"),CDataValueTOSQL3[i].TestCType, CDataArgToSQL3.TestSQLType[j]);
			InValue1 = SQL_DATA_AT_EXEC;
			returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL3[i].CType,
															CDataArgToSQL3.SQLType[j],CDataArgToSQL3.ColPrec[j],
															CDataArgToSQL3.ColScale[j],NULL,0,&InValue1);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
	
		returncode = SQLExecute(hstmt);         // Execute statement with 
		if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
			TESTCASE_END;	// end of setup
		}
		else
		{
			TESTCASE_END;	// end of setup

			_stprintf(Heading,_T("Test #%d: (SQLParamData/SQLPutData) checking %s tests \n"),TestId,CDataValueTOSQL3[i].TestCType);
			TESTCASE_BEGINW(Heading);
			j = 0;
			while (returncode == SQL_NEED_DATA)
			{
				returncode = SQLParamData(hstmt,&pToken);
				if (returncode == SQL_NEED_DATA)
				{
					switch (CDataValueTOSQL3[i].CType)
					{
						case SQL_C_FLOAT:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL3.CFLOATTOSQL[j]),0);
							break;
						case SQL_C_DOUBLE:
							rc = SQLPutData(hstmt,&(CDataTypeTOSQL3.CDOUBLETOSQL[j]),0);
							break;
						default: ;
					}
					if(!CHECKRC(SQL_SUCCESS,rc,"SQLPutData"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					j++;
				}
			}

			if (returncode != SQL_SUCCESS) {
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}

			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab3,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				returncode = SQLFetch(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (j = 0; j < MAX_PUTPARAM3; j++)
					{
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (_tcsnicmp(CDataValueTOSQL3[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL3[i].OutputValue[j])) == 0)
							{
								if(g_Trace){
									LogMsg(NONE,_T("Column #%d: expect: %s and actual: %s are matched\n"),
										j+1,CDataValueTOSQL3[i].OutputValue[j],OutValue);
								}
							}	
							else if (_tcsnicmp(CDataValueTOSQL3[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL3[i].OutputValue[j])-1) == 0)
							{
								TIMtemp = _tcslen(CDataValueTOSQL3[i].OutputValue[j])-1;
								if ((CDataValueTOSQL3[i].OutputValue[j][TIMtemp]) == (OutValue[TIMtemp] + 1))
									LogMsg(NONE,_T("Column #%d: expect: %s and actual: %s are matched\n"),
										j+1,CDataValueTOSQL3[i].OutputValue[j],OutValue);
								else
									LogMsg(ERRMSG,_T("Column #%d: expect: %s and actual: %s are not matched at line: %d\n"),
										j+1,CDataValueTOSQL3[i].OutputValue[j],OutValue,__LINE__);
							}
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,_T("Column #%d: expect: %s	and actual: %s are not matched at line: %d\n"),
									j+1,CDataValueTOSQL3[i].OutputValue[j],OutValue,__LINE__);
							}
						}
					} // end for loop
				}
			}
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTab3,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		i++;
		TestId++;
	}

//====================================================================================================
	// converting from cdate, ctime and ctimestamp to sql 
	i = 0;
	while (CDataValueTOSQL4[i].CType != 999)
	{
		_stprintf(Heading,_T("Setup for SQLParamData/SQLPutData tests #%d for cdate, ctime and ctimestamp\n"),TestId);
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab4,SQL_NTS);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTab4,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		LogMsg(NONE,_T("SQLPrepare for %s.\n"),CDataValueTOSQL4[i].TestCType);
		returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTab4,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		for (j = 0; j < MAX_PUTPARAM4; j++)
		{
			LogMsg(NONE,_T("SQLBindParameter for Column %d to convert from %s to %s\n"),j+1,CDataValueTOSQL4[i].TestCType, CDataArgToSQL4.TestSQLType[j]);
			InValue1 = SQL_DATA_AT_EXEC;
			switch (CDataValueTOSQL4[i].CType)
			{
				case SQL_C_DATE:
					if (CDataArgToSQL4.SQLType[j] != SQL_TIME)
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL4[i].CType,
																			CDataArgToSQL4.SQLType[j],CDataArgToSQL4.ColPrec[j],
																			CDataArgToSQL4.ColScale[j],NULL,0,&InValue1);
					else
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_TIME,
																			SQL_TIME,CDataArgToSQL4.ColPrec[j],
																			CDataArgToSQL4.ColScale[j],NULL,0,&InValue1);
					break;
				case SQL_C_TIME:
					if (CDataArgToSQL4.SQLType[j] != SQL_DATE)
					{
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL4[i].CType,
																			CDataArgToSQL4.SQLType[j],CDataArgToSQL4.ColPrec[j],
																			CDataArgToSQL4.ColScale[j],NULL,0,&InValue1);
					}
					else
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,SQL_C_DATE,
																			SQL_DATE,CDataArgToSQL4.ColPrec[j],
																			CDataArgToSQL4.ColScale[j],NULL,0,&InValue1);
					break;
				case SQL_C_TIMESTAMP:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL4[i].CType,
																			CDataArgToSQL4.SQLType[j],CDataArgToSQL4.ColPrec[j],
																			CDataArgToSQL4.ColScale[j],NULL,0,&InValue1);
					break;
				default: ;
			}

			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
	
		LogMsg(NONE,_T("Setup for checking SQLParamData/SQLPutData tests %s.\n"),CDataValueTOSQL4[i].TestCType);

		returncode = SQLExecute(hstmt);         // Execute statement with 
		if (!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
			TESTCASE_END;	//end of setup
		}
		else
		{
			TESTCASE_END;// end of setup

			_stprintf(Heading,_T("Test #%d: (SQLParamData/SQLPutData) checking %s tests \n"),TestId,CDataValueTOSQL4[i].TestCType);
			TESTCASE_BEGINW(Heading);
			j = 0;
			while (returncode == SQL_NEED_DATA)
			{
				returncode = SQLParamData(hstmt,&pToken);
				if (returncode == SQL_NEED_DATA)
				{
					switch (CDataValueTOSQL4[i].CType)
					{
						case SQL_C_DATE:
							if (CDataArgToSQL4.SQLType[j] != SQL_TIME)
								rc = SQLPutData(hstmt,&CDATETOSQL,0);
							else
								rc = SQLPutData(hstmt,&CTIMETOSQL,0);
							break;
						case SQL_C_TIME:
							if (CDataArgToSQL4.SQLType[j] != SQL_DATE)
							{
								rc = SQLPutData(hstmt,&CTIMETOSQL,0);
								if (CDataArgToSQL4.SQLType[j] == SQL_TIMESTAMP)
								{
									struct tm *newtime;
									time_t long_time;

									time( &long_time );
									newtime = localtime( &long_time );
									_tcscpy(tmpbuf,_T(""));
									_tcscpy(tmpbuf1,_T(""));
									_itot(newtime->tm_year+1900,tmpbuf1,10);
									_tcscpy(tmpbuf,tmpbuf1);
									_tcscat(tmpbuf,_T("-"));
									_tcscpy(tmpbuf1,_T(""));
									_stprintf(tmpbuf1,_T("%02d"),newtime->tm_mon+1);
									_tcscat(tmpbuf,tmpbuf1);
									_tcscat(tmpbuf,_T("-"));
									_tcscpy(tmpbuf1,_T(""));
									_stprintf(tmpbuf1,_T("%02d"),newtime->tm_mday);
									_tcscat(tmpbuf,tmpbuf1);
									_tcscat(tmpbuf,_T(" "));
									_tcscat(tmpbuf,CDataValueTOSQL4[i].OutputValue[j]);
								 // _tcscpy(CDataValueTOSQL4[i].OutputValue[j],_T(""));

									CDataValueTOSQL4[i].OutputValue[j] = (TCHAR *)malloc(sizeof(TCHAR)*(_tcslen(tmpbuf)+1));

									_tcscpy(CDataValueTOSQL4[i].OutputValue[j],_T(""));
									_tcscpy(CDataValueTOSQL4[i].OutputValue[j],tmpbuf);
									_tcscpy(tmpbuf,_T(""));
									_tcscpy(tmpbuf1,_T(""));
								}
							}
							else
								rc = SQLPutData(hstmt,&CDATETOSQL,0);
							break;
						case SQL_C_TIMESTAMP:
							rc = SQLPutData(hstmt,&CTIMESTAMPTOSQL,0);
							break;
						default: ;
					}
					if(!CHECKRC(SQL_SUCCESS,rc,"SQLPutData"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					j++;
				}
			}
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab4,SQL_NTS);
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
					for (j = 0; j < MAX_PUTPARAM4; j++)
					{
						LogMsg(NONE,_T("SQLParamData/SQLPutData test: checking data for column c%d\n"),j+1);
			
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (_tcsnicmp(CDataValueTOSQL4[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL4[i].OutputValue[j])) == 0)
							{
								if(g_Trace){
									LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),
										CDataValueTOSQL4[i].OutputValue[j],OutValue);
									}	
								}
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched at line: %d\n"),
									CDataValueTOSQL4[i].OutputValue[j],OutValue,__LINE__);
							}
						}
					} // end for loop
				}
			}
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)DelTab4,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		TESTCASE_END;
		i++;
		TestId++;
	}

//====================================================================================================

	i = 0;
	while (CDataValueTOSQL5[i].CType != 999)
	{
		_stprintf(Heading,_T("Setup for SQLParamData/SQLPutData tests #%d for SQL_C_DEFAULT.\n"),TestId);
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab5,SQL_NTS);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,CrtTab5);
		_tcscat(InsStr,CDataValueTOSQL5[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTab5,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		
		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_CHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[0],CDataValueTOSQL5[i].ColPrec[0],
																		CDataValueTOSQL5[i].ColScale[0],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
	
		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_VARCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[1],CDataValueTOSQL5[i].ColPrec[1],
																		CDataValueTOSQL5[i].ColScale[1],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_DECIMAL.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[2],CDataValueTOSQL5[i].ColPrec[2],
																		CDataValueTOSQL5[i].ColScale[2],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_NUMERIC.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[3],CDataValueTOSQL5[i].ColPrec[3],
																		CDataValueTOSQL5[i].ColScale[3],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_SMALLINT.\n"));
		InValue1 = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(5),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[4],CDataValueTOSQL5[i].ColPrec[4],
																		CDataValueTOSQL5[i].ColScale[4],NULL,0,&InValue1);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_INTEGER.\n"));
		InValue1 = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(6),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[5],CDataValueTOSQL5[i].ColPrec[5],
																		CDataValueTOSQL5[i].ColScale[5],NULL,0,&InValue1);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_REAL.\n"));
		InValue1 = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(7),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[6],CDataValueTOSQL5[i].ColPrec[6],
																		CDataValueTOSQL5[i].ColScale[6],NULL,0,&InValue1);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_FLOAT.\n"));
		InValue1 = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(8),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[7],CDataValueTOSQL5[i].ColPrec[7],
																		CDataValueTOSQL5[i].ColScale[7],NULL,0,&InValue1);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_DOUBLE.\n"));
		InValue1 = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(9),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[8],CDataValueTOSQL5[i].ColPrec[8],
																		CDataValueTOSQL5[i].ColScale[8],NULL,0,&InValue1);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_DATE.\n"));
		InValue1 = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(10),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[9],CDataValueTOSQL5[i].ColPrec[9],
																		CDataValueTOSQL5[i].ColScale[9],NULL,0,&InValue1);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_TIME.\n"));
		InValue1 = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(11),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[10],CDataValueTOSQL5[i].ColPrec[10],
																		CDataValueTOSQL5[i].ColScale[10],NULL,0,&InValue1);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_TIMESTAMP.\n"));
		InValue1 = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(12),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[11],CDataValueTOSQL5[i].ColPrec[11],
																		CDataValueTOSQL5[i].ColScale[11],NULL,0,&InValue1);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_LONGVARCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(13),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[12],CDataValueTOSQL5[i].ColPrec[12],
																		CDataValueTOSQL5[i].ColScale[12],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_BIGINT.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(14),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[13],CDataValueTOSQL5[i].ColPrec[13],
																		CDataValueTOSQL5[i].ColScale[13],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

/// ============================================================================================================
#ifndef UNICODE
		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_WCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(15),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[14],CDataValueTOSQL5[i].ColPrec[14],
																		CDataValueTOSQL5[i].ColScale[14],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_WVARCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(16),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[15],CDataValueTOSQL5[i].ColPrec[15],
																		CDataValueTOSQL5[i].ColScale[15],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_WLONGVARCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(17),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[16],CDataValueTOSQL5[i].ColPrec[16],
																		CDataValueTOSQL5[i].ColScale[16],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		for (h=0; h<BIG_NUM_PARAM; h++) {
			LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_BIGNUM. Columns #%d\n"), h+18);
			InValue = SQL_DATA_AT_EXEC;
			returncode = SQLBindParameter(hstmt,(SWORD)(h+18),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[h+17],CDataValueTOSQL5[i].ColPrec[h+17],
																			CDataValueTOSQL5[i].ColScale[h+17],NULL,NAME_LEN,&InValue);
		}
#else
		for (h=0; h<BIG_NUM_PARAM; h++) {
			LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_BIGNUM. Columns #%d\n"), h+15);
			InValue = SQL_DATA_AT_EXEC;
			returncode = SQLBindParameter(hstmt,(SWORD)(h+15),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[h+14],CDataValueTOSQL5[i].ColPrec[h+14],
																			CDataValueTOSQL5[i].ColScale[h+14],NULL,NAME_LEN,&InValue);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_WCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(23),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[22],CDataValueTOSQL5[i].ColPrec[22],
																		CDataValueTOSQL5[i].ColScale[22],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_WVARCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(24),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[23],CDataValueTOSQL5[i].ColPrec[23],
																		CDataValueTOSQL5[i].ColScale[23],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_WLONGVARCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(25),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[24],CDataValueTOSQL5[i].ColPrec[24],
																		CDataValueTOSQL5[i].ColScale[24],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_WCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(26),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[25],CDataValueTOSQL5[i].ColPrec[25],
																		CDataValueTOSQL5[i].ColScale[25],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_WVARCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(27),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[26],CDataValueTOSQL5[i].ColPrec[26],
																		CDataValueTOSQL5[i].ColScale[26],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}

		LogMsg(NONE,_T("SQLBindParameter from SQL_C_DEFAULT to SQL_WLONGVARCHAR.\n"));
		InValue = SQL_DATA_AT_EXEC;
		returncode = SQLBindParameter(hstmt,(SWORD)(28),ParamType,CDataValueTOSQL5[i].CType,
																		CDataArgToSQL5.SQLType[27],CDataValueTOSQL5[i].ColPrec[27],
																		CDataValueTOSQL5[i].ColScale[27],NULL,NAME_LEN,&InValue);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
#endif

		returncode = SQLExecute(hstmt);         // Execute statement with 
		if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
			TESTCASE_END;		// end of setup
		}
		else
		{
			TESTCASE_END;		// end of setup
/*
			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
#ifdef UNICODE
//				wcstombs(mbchar, (wchar_t*)CDataValueTOSQL5[i].CharValue, sizeof(mbchar));
				_tcscpy((TCHAR *)mbchar, CDataValueTOSQL5[i].CharValue);
#else
				mbstowcs(mbchar, CDataValueTOSQL5[i].CharValue, _tcslen(CDataValueTOSQL5[i].CharValue)+1);
#endif
				returncode = SQLPutData(hstmt,mbchar,wcslen(mbchar)*sizeof(wchar_t)*2);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
*/


			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				_tcscpy((TCHAR *)mbchar, CDataValueTOSQL5[i].CharValue);
				returncode = SQLPutData(hstmt,mbchar,_tcslen(mbchar)*sizeof(TCHAR));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
/*
#ifdef UNICODE
				_tcscpy((TCHAR *)mbvarchar, CDataValueTOSQL5[i].VarCharValue);
#else
				mbstowcs(mbvarchar, CDataValueTOSQL5[i].VarCharValue, _tcslen(CDataValueTOSQL5[i].VarCharValue)+1);
#endif
				returncode = SQLPutData(hstmt,mbvarchar, wcslen(mbvarchar)*sizeof(wchar_t)*2);
*/
                                _tcscpy((TCHAR *)mbvarchar, CDataValueTOSQL5[i].VarCharValue);
                                returncode = SQLPutData(hstmt,mbvarchar, _tcslen(mbvarchar)*sizeof(TCHAR));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,CDataValueTOSQL5[i].DecimalValue,strlen(CDataValueTOSQL5[i].DecimalValue));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			else {
				LogAllErrors(henv,hdbc,hstmt);			
			}
			
			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,CDataValueTOSQL5[i].NumericValue,strlen(CDataValueTOSQL5[i].NumericValue));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,&(CDataValueTOSQL5[i].ShortValue),0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,&(CDataValueTOSQL5[i].LongValue),0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,&(CDataValueTOSQL5[i].RealValue),0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,&(CDataValueTOSQL5[i].FloatValue),0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,&(CDataValueTOSQL5[i].DoubleValue),0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,&(CDataValueTOSQL5[i].DateValue),0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,&(CDataValueTOSQL5[i].TimeValue),0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,&(CDataValueTOSQL5[i].TimestampValue),0);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
/*
#ifdef UNICODE
//			        wcstombs(mblongvarchar, (wchar_t*)CDataValueTOSQL5[i].LongVarCharValue, sizeof(mblongvarchar));
				_tcscpy((TCHAR *)mblongvarchar, CDataValueTOSQL5[i].LongVarCharValue);
#else
			        mbstowcs(mblongvarchar, CDataValueTOSQL5[i].LongVarCharValue, _tcslen(CDataValueTOSQL5[i].LongVarCharValue)+1);				
#endif
				returncode = SQLPutData(hstmt,mblongvarchar, wcslen(mblongvarchar)*sizeof(wchar_t)*2);
*/
                                _tcscpy((TCHAR *)mblongvarchar, CDataValueTOSQL5[i].LongVarCharValue);
                                returncode = SQLPutData(hstmt,mblongvarchar,_tcslen(mblongvarchar)*sizeof(TCHAR));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,CDataValueTOSQL5[i].BigintValue,strlen(CDataValueTOSQL5[i].BigintValue));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

#ifndef UNICODE
			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				strcpy(widechar, CDataValueTOSQL5[i].NChar);
//				returncode = SQLPutData(hstmt,widechar,SQL_NTS);
				returncode = SQLPutData(hstmt,widechar,strlen(widechar)*sizeof(char));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			else
				LogAllErrors(henv,hdbc,hstmt);

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				strcpy(widevarchar, CDataValueTOSQL5[i].NCharVarying);
//				returncode = SQLPutData(hstmt,widevarchar,SQL_NTS);
				returncode = SQLPutData(hstmt,widevarchar,strlen(widevarchar)*sizeof(char));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				_tcscpy(widelongvarchar, CDataValueTOSQL5[i].NLongCharVarying);
//				returncode = SQLPutData(hstmt,widelongvarchar,SQL_NTS);
				returncode = SQLPutData(hstmt,widelongvarchar,strlen(widelongvarchar)*sizeof(char));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
#endif

			for (h=0; h<BIG_NUM_PARAM; h++) {
				returncode = SQLParamData(hstmt,&pToken);
				if (returncode == SQL_NEED_DATA)
				{
					returncode = SQLPutData(hstmt,CDataValueTOSQL5[i].BigNumValue[h],strlen(CDataValueTOSQL5[i].BigNumValue[h]));
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
				}
			}

#ifdef UNICODE

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				_tcscpy(widechar, CDataValueTOSQL5[i].NChar);
			//	returncode = SQLPutData(hstmt,widechar,wcslen(widechar)*2*sizeof(wchar_t));
				returncode = SQLPutData(hstmt,widechar,_tcslen(widechar)*sizeof(TCHAR));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			else
				LogAllErrors(henv,hdbc,hstmt);

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				_tcscpy(widevarchar, CDataValueTOSQL5[i].NCharVarying);
			//	returncode = SQLPutData(hstmt,widevarchar,wcslen(widevarchar)*2*sizeof(wchar_t));
				returncode = SQLPutData(hstmt,widevarchar,_tcslen(widevarchar)*sizeof(TCHAR));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				_tcscpy(widelongvarchar, CDataValueTOSQL5[i].NLongCharVarying);
			//	returncode = SQLPutData(hstmt,widelongvarchar,wcslen(widelongvarchar)*2*sizeof(wchar_t));
				returncode = SQLPutData(hstmt,widelongvarchar,_tcslen(widelongvarchar)*sizeof(TCHAR));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				_tcscpy(widechar, CDataValueTOSQL5[i].UTF8CharValue);
			//	returncode = SQLPutData(hstmt,widechar,wcslen(widechar)*2*sizeof(wchar_t));
				returncode = SQLPutData(hstmt,widechar,_tcslen(widechar)*sizeof(TCHAR));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				_tcscpy(widevarchar, CDataValueTOSQL5[i].UTF8VarCharValue);
			//	returncode = SQLPutData(hstmt,widevarchar,wcslen(widevarchar)*2*sizeof(wchar_t));
				returncode = SQLPutData(hstmt,widevarchar,_tcslen(widevarchar)*sizeof(TCHAR));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				_tcscpy(widelongvarchar, CDataValueTOSQL5[i].UTF8LongVarCharValue);
			//	returncode = SQLPutData(hstmt,widelongvarchar,wcslen(widelongvarchar)*2*sizeof(wchar_t));
				returncode = SQLPutData(hstmt,widelongvarchar,_tcslen(widelongvarchar)*sizeof(TCHAR));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
#endif

			returncode = SQLParamData(hstmt,&pToken);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLParamData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
//#endif

			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab5,SQL_NTS);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				returncode = SQLFetch(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				else
				{
					for (j = 0; j < MAX_BINDPARAM1; j++)
					{
						LogMsg(LINEBEFORE,_T("SQLParamData/SQLPutData test:checking data for column c%d\n"),j+1);
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (_tcsnicmp(CDataValueTOSQL5[i].OutputValue[j],OutValue,_tcslen(CDataValueTOSQL5[i].OutputValue[j])) == 0)
							{
								if(g_Trace){
									LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueTOSQL5[i].OutputValue[j],OutValue);
									}
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched at line: %d\n"),CDataValueTOSQL5[i].OutputValue[j],OutValue,__LINE__);
							}
						}
					} // end for loop
				}
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab5,SQL_NTS);
		i++;
		TestId++;
	}

//=================================================================================================================
// Section #6: convert SQL_C_FLOAT to SQL_NUMERIC
    i = 0;
	while (CFloatToNumeric[i].PassFail != 999)
	{
		TESTCASE_BEGIN("SQLPutData tests to bind from SQL_C_FLOAT to SQL_NUMERIC.\n");
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab6,SQL_NTS);
        _stprintf(InsStr, _T("%s %s"), CrtTab6, CFloatToNumeric[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTab6,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

        for(j = 0; j < MAX_PUTPARAM5; j++) {
            InValue = SQL_DATA_AT_EXEC;
		    returncode = SQLBindParameter(hstmt,(SWORD)(j+1),SQL_PARAM_INPUT,SQL_C_FLOAT,SQL_NUMERIC,
								    CFloatToNumeric[i].ColPrec[j],CFloatToNumeric[i].ColScale[j],NULL,0,&InValue);
		    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		    {
			    TEST_FAILED;
			    LogAllErrors(henv,hdbc,hstmt);
		    }
        }

        returncode = SQLExecute(hstmt);
		if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
        else 
        {
			j = 0;
			while(returncode == SQL_NEED_DATA)
			{
				returncode = SQLParamData(hstmt,&pToken);
				if (returncode == SQL_NEED_DATA)
				{
					rc = SQLPutData(hstmt,&(CFloatToNumeric[i].FloatValue[j]),0);
					if(!CHECKRC(SQL_SUCCESS,rc,"SQLPutData"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					j++;
				} 
				else if(returncode == SQL_ERROR ) {
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
		}

        returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab6,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
		{
			returncode = SQLFetch(hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				for (j = 0; j < MAX_PUTPARAM5; j++)
				{
					LogMsg(NONE,_T("SQLBindParameter test:checking data for column c%d\n"),j+1);
					returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						if (fabsf(_tstof(CFloatToNumeric[i].OutputValue[j]) - _tstof(OutValue)) < 0.000001)
						//if (_tcsncmp(CFloatToNumeric[i].OutputValue[j],OutValue,_tcslen(CFloatToNumeric[i].OutputValue[j])) == 0)
						{
							LogMsg(NONE,_T("expect: %f and actual: %f are matched\n"),_tstof(CFloatToNumeric[i].OutputValue[j]),_tstof(OutValue));
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %f and actual: %f are not matched at line %d\n"),_tstof(CFloatToNumeric[i].OutputValue[j]),_tstof(OutValue),__LINE__);
						}
					}
				} // end for loop
			}
		}

		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab6,SQL_NTS);
		i++;
	}

////=================================================================================================================
// Section #7: convert SQL_C_DOUBLE to SQL_NUMERIC

    i = 0;
	while (CDoubleToNumeric[i].PassFail != 999)
	{
		TESTCASE_BEGIN("SQLPutData tests to bind from SQL_C_DOUBLE to SQL_NUMERIC.\n");
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab6,SQL_NTS);
        _stprintf(InsStr, _T("%s %s"), CrtTab6, CDoubleToNumeric[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTab6,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

        for(j = 0; j < MAX_PUTPARAM5; j++) {
            InValue = SQL_DATA_AT_EXEC;
		    returncode = SQLBindParameter(hstmt,(SWORD)(j+1),SQL_PARAM_INPUT,SQL_C_DOUBLE,SQL_NUMERIC,
								    CDoubleToNumeric[i].ColPrec[j],CDoubleToNumeric[i].ColScale[j],NULL,0,&InValue);
		    if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
		    {
			    TEST_FAILED;
			    LogAllErrors(henv,hdbc,hstmt);
		    }
        }

        returncode = SQLExecute(hstmt);
		if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLExecute"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
        else 
        {
			j = 0;
			while(returncode == SQL_NEED_DATA)
			{
				returncode = SQLParamData(hstmt,&pToken);
				if (returncode == SQL_NEED_DATA)
				{
					rc = SQLPutData(hstmt,&(CDoubleToNumeric[i].DoubleValue[j]),0);
					if(!CHECKRC(SQL_SUCCESS,rc,"SQLPutData"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					j++;
				} 
				else if(returncode == SQL_ERROR) {
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
		}

        returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab6,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		else
		{
			returncode = SQLFetch(hstmt);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			else
			{
				for (j = 0; j < MAX_PUTPARAM5; j++)
				{
					LogMsg(NONE,_T("SQLPutData test:checking data for column c%d\n"),j+1);
					returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						if (fabs(_tstof(CDoubleToNumeric[i].OutputValue[j]) - _tstof(OutValue)) < 0.000001)
						//if (_tcsncmp(CDoubleToNumeric[i].OutputValue[j],OutValue,_tcslen(CDoubleToNumeric[i].OutputValue[j])) == 0)
						{
							LogMsg(NONE,_T("expect: %lf and actual: %lf are matched\n"),_tstof(CDoubleToNumeric[i].OutputValue[j]),_tstof(OutValue));
						}	
						else
						{
							TEST_FAILED;	
							LogMsg(ERRMSG,_T("expect: %lf and actual: %lf are not matched at line %d\n"),_tstof(CDoubleToNumeric[i].OutputValue[j]),_tstof(OutValue),__LINE__);
						}
					}
				} // end for loop
			}
		}

		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTab6,SQL_NTS);
		i++;
	}

//=================================================================================================================

	free(TempType1);
	free(TempType2);
	free(InsStr);
	FullDisconnect(pTestInfo);
	free_list(var_list);
	LogMsg(SHORTTIMESTAMP+LINEBEFORE+LINEAFTER,_T("End testing API => MX Specific SQLSQLParamData/SQLPutData.\n"));
	TEST_RETURN;
}

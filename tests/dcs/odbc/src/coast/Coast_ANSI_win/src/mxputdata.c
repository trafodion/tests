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
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/timeb.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define NAME_LEN		300
#define	MAX_PUTPARAM1	25
#define MAX_PUTPARAM2	14
#define	MAX_PUTPARAM3	14
#define MAX_PUTPARAM4	9 
#define MAX_PUTPARAM5   14
#define BIG_NUM_PARAM	8

#ifndef _WM
	#define DATE_FORMAT			"1993-12-30"
	#define FLOAT_FORMAT		"0.123456"
	#define FLOAT_FORMAT_N		"-0.123456"
	#define FLOAT_FORMAT_E		"0.12345678"
/* SEAQUSET */ #define FLOAT_FORMAT_F          "0.123457"
	#define DOUBLE_FORMAT		"0.123456789123456"
	#define DOUBLE_FORMAT_N		"-0.123456789123456"
	#define DOUBLE_FORMAT_L		"0.1234567891"
	#define DOUBLE_FORMAT_LN	"-0.1234567891"
#else
	#define DATE_FORMAT			"93/12/30"
	#define FLOAT_FORMAT		".123456"
	#define FLOAT_FORMAT_N		"-.123456"
	#define FLOAT_FORMAT_E		".12345678"
/* sq */ #define FLOAT_FORMAT_F          ".123457"
	#define DOUBLE_FORMAT		".123456789123456"
	#define DOUBLE_FORMAT_N		"-.123456789123456"
	#define DOUBLE_FORMAT_L		".1234567891"
	#define DOUBLE_FORMAT_LN	"-.1234567891"
#endif

PassFail TestMXSQLPutData(TestInfo *pTestInfo)
{
	TEST_DECLARE;
 	char				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode, rc;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	short				i, j, k, h, maxloop;
	short				TestId;
    SQLINTEGER          BuffLen;
	SQLSMALLINT			ParamType = SQL_PARAM_INPUT;

	struct // We have to support bit, tinyint, binary, varbinary, long varbinary
	{
		SQLSMALLINT	SQLType[MAX_PUTPARAM1];
	} CDataArgToSQL1 = 
		{
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,
			SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_LONGVARCHAR,SQL_BIGINT,
			SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,
            SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR
		};

	struct
	{
		SQLSMALLINT			CType;
		char				*CrtCol;
		SQLUINTEGER			ColPrec[MAX_PUTPARAM1];
		SQLSMALLINT			ColScale[MAX_PUTPARAM1];
		int					PutLoop;
		char				*expectedValue[MAX_PUTPARAM1];
	} CDataValueTOSQL1[] = 
		{			// real, float and double precision to char has problem it returns 12345.0 values as 12345.
			{	SQL_C_CHAR,
				"--",
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,19,19,128,128,128,10,18,30,254,254,2000,
				0,  0,  5, 5, 0,0, 0, 0, 0,0,0,0,0,   0,0, 6, 0,  128,64, 5, 5, 10,0,  0,  0,
				1,
#ifndef _WM
				"--","--","1234.56789","5678.12345","1234","12345","12340.0","12300.0","12345670.0","1993-12-30","11:45:23","1992-12-31 23:45:23.123456","--","123456","1234567890123456789","1234567890123.456789","1234567890123456789012345678901234567890","0.123456789012345678901234567890123456789","1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789","--","--","--"
#else
				"--","--","1234.56789","5678.12345","1234","12345","12340.0","12300.0","12345670.0","93/12/30","11:45:23","1992-12-31 23:45:23.123456","--","123456","1234567890123456789","1234567890123.456789","1234567890123456789012345678901234567890",".123456789012345678901234567890123456789","1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789","--","--","--"
#endif
			},
			{	SQL_C_CHAR,
				"--",
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,19,19,128,128,128,10,18,30,254,254,2000,
				0,  0,  5, 5, 0,0, 0, 0, 0,0,0,0,0,   0,0, 6, 0,  128,64, 5, 5, 10,0,  0,  0,
				4,
#ifndef _WM
				"--","--","-1234.56789","-5678.12345","-1234","-12345","-12340.0","-12300.0","-12345670.0","1993-12-30","11:45:23","1992-12-31 23:45:23.123456","--","-123456","-1234567890123456789","-1234567890123.456789","-1234567890123456789012345678901234567890","-0.123456789012345678901234567890123456789","-1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789","--","--","--"
#else
				"--","--","-1234.56789","-5678.12345","-1234","-12345","-12340.0","-12300.0","-12345670.0","93/12/30","11:45:23","1992-12-31 23:45:23.123456","--","-123456","-1234567890123456789","-1234567890123.456789","-1234567890123456789012345678901234567890","-.123456789012345678901234567890123456789","-1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789","--","--","--"
#endif
			},
			{	999,
			}
		};

	char	*DrpTab1;
	char	*CrtTab1;
	char	*InsTab1;
	char	*SelTab1;

	struct // We have to support bit, tinyint
	{
		char		*TestSQLType[MAX_PUTPARAM2];
		SQLSMALLINT	SQLType[MAX_PUTPARAM2];
		SQLUINTEGER	ColPrec[MAX_PUTPARAM2];
		SQLSMALLINT	ColScale[MAX_PUTPARAM2];
	} CDataArgToSQL2 = {
			"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_REAL","SQL_FLOAT","SQL_DOUBLE","SQL_LONGVARCHAR","SQL_BIGINT","SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR",
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_LONGVARCHAR,SQL_BIGINT,SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR,
			254,254,10,10,5,10,7,15,15,2000,19,254,254,2000,
			0,0,5,5,0,0,0,0,0,0,0,0,0,0};
	
	struct
	{
		SCHAR		CSTINTTOSQL[MAX_PUTPARAM2];
		char		CUTINTTOSQL[MAX_PUTPARAM2];
		SCHAR		CTINTTOSQL[MAX_PUTPARAM2];
		SWORD		CSSHORTTOSQL[MAX_PUTPARAM2];
		UWORD		CUSHORTTOSQL[MAX_PUTPARAM2];
		SWORD		CSHORTTOSQL[MAX_PUTPARAM2];
		SDWORD		CSLONGTOSQL[MAX_PUTPARAM2];
		UDWORD		CULONGTOSQL[MAX_PUTPARAM2];
		SDWORD		CLONGTOSQL[MAX_PUTPARAM2];
	} CDataTypeTOSQL2 = {-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,
						123,123,123,123,123,123,123,123,123,123,123,123,123,123,
						-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,-123,
						-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,
						1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,1234,
						-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,-1234,
						-12345,-12345,-12345,-12345,-1234,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345,
						12345,12345,12345,12345,1234,12345,12345,12345,12345,12345,12345,12345,12345,12345,
						-12345,-12345,-12345,-12345,-1234,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345,-12345};

	struct
	{
		SQLSMALLINT			CType;
		char				*TestCType;
		char				*OutputValue[MAX_PUTPARAM2];
	} CDataValueTOSQL2[] = {
		{SQL_C_STINYINT,"SQL_C_STINYINT","-123","-123","-123.0","-123.0","-123","-123","-123.0","-123.0","-123.0","-123","-123","-123","-123","-123"},
		{SQL_C_UTINYINT,"SQL_C_UTINYINT","123","123","123.0","123.0","123","123","123.0","123.0","123.0","123","123","123","123","123"},
		{SQL_C_TINYINT,"SQL_C_TINYINT","-123","-123","-123.0","-123.0","-123","-123","-123.0","-123.0","-123.0","-123","-123","-123","-123","-123"},
		{SQL_C_SSHORT,"SQL_C_SSHORT","-1234","-1234","-1234.0","-1234.0","-1234","-1234","-1234.0","-1234.0","-1234.0","-1234","-1234","-1234","-1234","-1234"},
		{SQL_C_USHORT,"SQL_C_USHORT","1234","1234","1234.0","1234.0","1234","1234","1234.0","1234.0","1234.0","1234","1234","1234","1234","1234"},
		{SQL_C_SHORT,"SQL_C_SHORT","-1234","-1234","-1234.0","-1234.0","-1234","-1234","-1234.0","-1234.0","-1234.0","-1234","-1234","-1234","-1234","-1234"},
		{SQL_C_SLONG,"SQL_C_SLONG","-12345","-12345","-12345.0","-12345.0","-1234","-12345","-12345.0","-12345.0","-12345.0","-12345","-12345","-12345","-12345","-12345"},
		{SQL_C_ULONG,"SQL_C_ULONG","12345","12345","12345.0","12345.0","1234","12345","12345.0","12345.0","12345.0","12345","12345","12345","12345","12345"},
		{SQL_C_LONG,"SQL_C_LONG","-12345","-12345","-12345.0","-12345.0","-1234","-12345","-12345.0","-12345.0","-12345.0","-12345","-12345","-12345","-12345","-12345"},
		{999,}
		};

	char	*DrpTab2;
	char	*DelTab2;
	char	*CrtTab2;
	char	*InsTab2;
	char	*SelTab2;
	
	struct // We have to support bit, tinyint
	{
		char	    *TestSQLType[MAX_PUTPARAM3];
		SQLSMALLINT	SQLType[MAX_PUTPARAM3];
		SQLUINTEGER	ColPrec[MAX_PUTPARAM3];
		SQLSMALLINT	ColScale[MAX_PUTPARAM3];
	} CDataArgToSQL3 = {
			"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_REAL","SQL_FLOAT","SQL_DOUBLE","SQL_LONGVARCHAR","SQL_BIGINT","SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR",
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,SQL_FLOAT,SQL_DOUBLE,SQL_LONGVARCHAR,SQL_BIGINT,SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR,
			254,254,10,10,5,10,7,15,15,2000,19,254,254,2000,
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
		char				*TestCType;
		char				*OutputValue[MAX_PUTPARAM3];
	} CDataValueTOSQL3[] = {
		{SQL_C_FLOAT,"SQL_C_FLOAT","12345.67","12345.67","12345.67","12345.67","1234","12345","12345.67","12345.67","123456.78","12345.67","123456","12345.67","12345.67","12345.67"},
		{SQL_C_DOUBLE,"SQL_C_DOUBLE","12345.67","12345.67","12345.67","12345.67","1234","12345","12345.67","12345.67","123456.78","12345.67","1234567","12345.67","12345.67","12345.67"},
		{999,}
		};

	char	*DrpTab3;
	char	*DelTab3;
	char	*CrtTab3;
	char	*InsTab3;
	char	*SelTab3;

	struct // We have to support longvarchar
	{
		char				*TestSQLType[MAX_PUTPARAM4];
		SQLSMALLINT	SQLType[MAX_PUTPARAM4];
		SQLUINTEGER	ColPrec[MAX_PUTPARAM4];
		SQLSMALLINT	ColScale[MAX_PUTPARAM4];
	} CDataArgToSQL4 = {
			"SQL_CHAR","SQL_VARCHAR","SQL_DATE","SQL_TIME","SQL_TIMESTAMP","SQL_LONGVARCHAR","SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR",
			SQL_CHAR,SQL_VARCHAR,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_LONGVARCHAR,SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR,
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
		char				*TestCType;
		char				*OutputValue[MAX_PUTPARAM4];
	} CDataValueTOSQL4[] = {
		{SQL_C_DATE,"SQL_C_DATE","1993-12-30","1993-12-30",DATE_FORMAT,"11:33:41","1993-12-30","1993-12-30","1993-12-30","1993-12-30","1993-12-30"},
		{SQL_C_TIME,"SQL_C_TIME","11:33:41","11:33:41",DATE_FORMAT,"11:33:41","11:33:41","11:33:41","11:33:41","11:33:41","11:33:41"},
		{SQL_C_TIMESTAMP,"SQL_C_TIMESTAMP","1993-12-30 11:33:41.123456","1993-12-30 11:33:41.123456",DATE_FORMAT,"11:33:41","1993-12-30 11:33:41.123456","1993-12-30 11:33:41.123456","1993-12-30 11:33:41.123456","1993-12-30 11:33:41.123456","1993-12-30 11:33:41.123456"},
		{999,}
		};

	char	*DrpTab4;
	char	*DelTab4;
	char	*CrtTab4;
	char	*InsTab4;
	char	*SelTab4;
// sq	char tmpbuf[30],tmpbuf1[8];
/* sq new */ char tmpbuf[70];

	struct // We have to support bit, tinyint, binary, varbinary, long varbinary
	{
		SQLSMALLINT	SQLType[MAX_PUTPARAM1];
	} CDataArgToSQL5 = 
		{
			SQL_CHAR,SQL_VARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,
			SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_LONGVARCHAR,SQL_BIGINT,
			SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,SQL_NUMERIC,
            SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR
		};

	struct
	{
		SQLSMALLINT			CType;
		char				*CrtCol;
		SQLUINTEGER			ColPrec[MAX_PUTPARAM1];
		SQLSMALLINT			ColScale[MAX_PUTPARAM1];
		char				*CharValue;
		char				*VarCharValue;
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
		char				*LongVarCharValue;
		char				*BigintValue;
		char			    *BigNumValue[BIG_NUM_PARAM];
        char                *NChar;
        char                *NCharVarying;
        char                *NLongCharVarying;
		char				*OutputValue[MAX_PUTPARAM1];
	} CDataValueTOSQL5[] = 
		{			// real, float and double precision to char has problem it returns 12345.0 values as 12345.
			{	SQL_C_DEFAULT,
				"--",
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,19,19,128,128,128,10,18,30,254,254,2000,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,0,0,   0,0, 6, 0,  128,64, 5, 5, 10,0,  0,  0,
				"--",
				"--",
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
				"--",
				"123456",
				"1234567890123456789","1234567890123.456789","1234567890123456789012345678901234567890","0.123456789012345678901234567890123456789","1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789",
                "--","--","--",
#ifndef _WM
				"--","--","1234.56789","5678.12345","1234","12345","12340.0","12300.0","12345670.0","1993-12-30","11:45:23","1997-10-12 11:33:41.000123","--","123456","1234567890123456789","1234567890123.456789","1234567890123456789012345678901234567890","0.123456789012345678901234567890123456789","1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789","--","--","--"
#else
				"--","--","1234.56789","5678.12345","1234","12345","12340.0","12300.0","12345670.0","93/12/30","11:45:23","1997-10-12 11:33:41.000123","--","123456","1234567890123456789","1234567890123.456789","1234567890123456789012345678901234567890",".123456789012345678901234567890123456789","1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789","--","--","--"
#endif
			},
			{	SQL_C_DEFAULT,
				"--",
				254,254,10,10,5,10,7,15,15,0,0,0,2000,0,19,19,128,128,128,10,18,30,254,254,2000,
				0,  0,  5, 5, 0,0, 0,0, 0, 0,0,0,0,   0,0, 6, 0,  128,64, 5, 5, 10,0,  0,  0,
				"--",
				"--",
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
				"--",
				"-123456",
				"-1234567890123456789","-1234567890123.456789","-1234567890123456789012345678901234567890","-0.123456789012345678901234567890123456789","-1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789",
                "--","--","--",
#ifndef _WM
				"--","--","-1234.56789","-5678.12345","-1234","-12345","-12340.0","-12300.0","-12345670.0","1993-12-30","11:45:23","1997-10-12 11:33:41.123456","--","-123456","-1234567890123456789","-1234567890123.456789","-1234567890123456789012345678901234567890","-0.123456789012345678901234567890123456789","-1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789","--","--","--"
#else
				"--","--","-1234.56789","-5678.12345","-1234","-12345","-12340.0","-12300.0","-12345670.0","93/12/30","11:45:23","1997-10-12 11:33:41.123456","--","-123456","-1234567890123456789","-1234567890123.456789","-1234567890123456789012345678901234567890","-.123456789012345678901234567890123456789","-1234567890.123456789012345678901234567890123456789","12345.56789","1234567890123.56789","12345678901234567890.0123456789","--","--","--"
#endif
			},
			{	999,
			}
		};

	char	*DrpTab5;
	char	*CrtTab5;
	char	*InsTab5;
	char	*SelTab5;

	SQLLEN			InValue = SQL_DATA_AT_EXEC, InValue1 = SQL_DATA_AT_EXEC;
	char			OutValue[NAME_LEN];
	SQLLEN			OutValueLen;
	char			*InsStr;
	char			*TempType1;
	SQLPOINTER		pToken;
	
	int TIMtemp;

//************************************************
// Data structures for Testing Section #6

    char    *DrpTab6;
    char    *CrtTab6;
    char    *InsTab6;
    char    *SelTab6;

    struct {
		RETCODE		PassFail;
		char		*CrtCol;
		SQLUINTEGER	ColPrec[MAX_PUTPARAM5];
		SQLSMALLINT	ColScale[MAX_PUTPARAM5];
		SFLOAT		FloatValue[MAX_PUTPARAM5];
        char        *OutputValue[MAX_PUTPARAM5];
    } CFloatToNumeric[] = {
        {SQL_SUCCESS, 
			"--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(float)12345678.0, (float)0.123456, (float)12.345678, (float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)12345678,
            (float)0.123456, (float)1.234567, (float)12345678.0, (float)0.123456, (float)12345678.0,(float)0.123456},
            {"12345678", FLOAT_FORMAT, "12.345678", "12345678", FLOAT_FORMAT, "1.234567", "12345678", "12345678",
            FLOAT_FORMAT, "1.234567", "12345678", FLOAT_FORMAT, "12345678", FLOAT_FORMAT}
        },
        {SQL_SUCCESS, 
            "--",
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {(float)12345678.0, (float)0.123456, (float)12.345678, (float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)12345678,
            (float)0.123456, (float)1.234567, (float)12345678.0, (float)0.123456, (float)12345678.0,(float)0.123456},
            {"12345678", FLOAT_FORMAT, "12.345678", "12345678", FLOAT_FORMAT, "1.234567", "12345678", "12345678",
            FLOAT_FORMAT, "1.234567", "12345678", FLOAT_FORMAT, "12345678", FLOAT_FORMAT}
        },
        {SQL_SUCCESS, 
            "--",
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {0,0,0,0,0,0,0,0,0,0,0,0,0,0},
            {(float)(-123456.0), (float)(-0.123456), (float)(-12.345678), (float)(-123456.0), (float)(-0.123456), (float)(-1.234567), (float)(-123456.0), (float)(-123456),
            (float)(-0.123456), (float)(-1.234567), (float)(-123456.0), (float)(-0.123456), (float)(-123456.0),(float)(-0.123456)},
            {"-123456", FLOAT_FORMAT_N, "-12.345678", "-123456", FLOAT_FORMAT_N, "-1.234567", "-123456", "-123456",
            FLOAT_FORMAT_N, "-1.234567", "-123456", FLOAT_FORMAT_N, "-123456", FLOAT_FORMAT_N}
        },
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(float)(+123456.0), (float)(+0.123456), (float)(+12.345678), (float)(123456.0), (float)(0.123456), (float)(1.234567), (float)(123456.0), (float)(+123456),
            (float)(+0.123456), (float)(+1.234567), (float)(+123456.0), (float)(0.123456), (float)(123456.0), (float)(0.123456)},
            {"123456", FLOAT_FORMAT, "12.345678", "123456", "0.123456", "1.234567", "123456", "123456",
            FLOAT_FORMAT, "1.234567", "123456", FLOAT_FORMAT, "123456", FLOAT_FORMAT}
        },
        {SQL_SUCCESS, 
			"--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(float)12345678.0, (float)0.12345678, (float)12.345678, (float)12345678.0, (float)0.123456, (float)1.234567, (float)12345678.0, (float)12345678,
            (float)0.123456, (float)1.234567, (float)12345678.0, (float)0.123456, (float)12345678.0,(float)0.123456},
            {"12345678", /* sq FLOAT_FORMAT_E */ FLOAT_FORMAT_F, "12.345678", "12345678", FLOAT_FORMAT, "1.234567", "12345678", "123456",
            FLOAT_FORMAT, "1.234567", "12345678", FLOAT_FORMAT, "12345678", FLOAT_FORMAT}
        },
        {999,
        }
    };

//************************************************
// Data structures for Testing Section #7

    struct {
		RETCODE		PassFail;
		char		*CrtCol;
		SQLUINTEGER	ColPrec[MAX_PUTPARAM5];
		SQLSMALLINT	ColScale[MAX_PUTPARAM5];
		SDOUBLE		DoubleValue[MAX_PUTPARAM5];
        char        *OutputValue[MAX_PUTPARAM5];
    } CDoubleToNumeric[] = {
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)123456789123456.0, (double)0.123456789123456, (double)12.3456789123456, (double)123456789123456.0, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)123456789123456,
            (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)0.1234567891, (double)123456789123456.0,(double)0.123456789123456},
            {"123456789123456", DOUBLE_FORMAT, "12.3456789123456", "123456789123456", DOUBLE_FORMAT, "1.23456789123456", "123456789123456", "123456789123456",
            DOUBLE_FORMAT, "1.23456789123456", "123456789123456", DOUBLE_FORMAT_L, "123456789123456", DOUBLE_FORMAT}
        },
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)123456789123456.0, (double)0.123456789123456, (double)12.3456789123456, (double)123456789123456.0, (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)123456789123456,
            (double)0.123456789123456, (double)1.23456789123456, (double)123456789123456.0, (double)0.1234567891, (double)123456789123456.0,(double)0.123456789123456},
            {"123456789123456", DOUBLE_FORMAT, "12.3456789123456", "123456789123456", DOUBLE_FORMAT, "1.23456789123456", "123456789123456", "123456789123456",
            DOUBLE_FORMAT, "1.23456789123456", "123456789123456", DOUBLE_FORMAT_L, "123456789123456", DOUBLE_FORMAT}
        },
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)-123456789123456.0, (double)-0.123456789123456, (double)-12.3456789123456, (double)-123456789123456.0, (double)-0.123456789123456, (double)-1.23456789123456, (double)-123456789123456.0, (double)-123456789123456,
            (double)-0.123456789123456, (double)-1.23456789123456, (double)-123456789123456.0, (double)-0.1234567891, (double)-123456789123456.0,(double)-0.123456789123456},
            {"-123456789123456", DOUBLE_FORMAT_N, "-12.3456789123456", "-123456789123456", DOUBLE_FORMAT_N, "-1.23456789123456", "-123456789123456", "-123456789123456",
            DOUBLE_FORMAT_N, "-1.23456789123456", "-123456789123456", DOUBLE_FORMAT_LN, "-123456789123456", DOUBLE_FORMAT_N}
        },
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)+123456789123456.0, (double)+0.123456789123456, (double)+12.3456789123456, (double)+123456789123456.0, (double)+0.123456789123456, (double)+1.23456789123456, (double)+123456789123456.0, (double)+123456789123456,
            (double)+0.123456789123456, (double)+1.23456789123456, (double)+123456789123456.0, (double)+0.1234567891, (double)+123456789123456.0,(double)+0.123456789123456},
            {"123456789123456", DOUBLE_FORMAT, "12.3456789123456", "123456789123456", DOUBLE_FORMAT, "1.23456789123456", "123456789123456", "123456789123456",
            DOUBLE_FORMAT, "1.23456789123456", "123456789123456", DOUBLE_FORMAT_L, "123456789123456", DOUBLE_FORMAT}

        },
        {SQL_SUCCESS, 
            "--",
            {18,18,18,19,19,19,128,64,128,128,18,19,128,64},
            {0,18,17,0,19,18,0,0,128,127,0,10,0,32},
            {(double)12345678.0, (double)0.12345678, (double)12.345678, (double)12345678.0, (double)0.123456, (double)1.234567, (double)12345678.0, (double)12345678,
            (double)0.123456, (double)1.234567, (double)12345678.0, (double)0.123456, (double)12345678.0,(double)0.123456},
            {"12345678", FLOAT_FORMAT_E, "12.345678", "12345678", FLOAT_FORMAT, "1.234567", "12345678", "123456",
            FLOAT_FORMAT, "1.234567", "12345678", FLOAT_FORMAT, "12345678", FLOAT_FORMAT}
        },
        {999,
        }
    };

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLPutData", charset_file);
	if (var_list == NULL) return FAILED;

	DrpTab1 = var_mapping("SQLPutData_DrpTab_1", var_list);
	CrtTab1 = var_mapping("SQLPutData_CrtTab_1", var_list);
	InsTab1 = var_mapping("SQLPutData_InsTab_1", var_list);
	SelTab1 = var_mapping("SQLPutData_SelTab_1", var_list);

	DrpTab2 = var_mapping("SQLPutData_DrpTab_2", var_list);
	CrtTab2 = var_mapping("SQLPutData_CrtTab_2", var_list);
	InsTab2 = var_mapping("SQLPutData_InsTab_2", var_list);
	SelTab2 = var_mapping("SQLPutData_SelTab_2", var_list);
	DelTab2 = var_mapping("SQLPutData_DelTab_2", var_list);

	DrpTab3 = var_mapping("SQLPutData_DrpTab_3", var_list);
	CrtTab3 = var_mapping("SQLPutData_CrtTab_3", var_list);
	InsTab3 = var_mapping("SQLPutData_InsTab_3", var_list);
	SelTab3 = var_mapping("SQLPutData_SelTab_3", var_list);
	DelTab3 = var_mapping("SQLPutData_DelTab_3", var_list);

	DrpTab4 = var_mapping("SQLPutData_DrpTab_4", var_list);
	CrtTab4 = var_mapping("SQLPutData_CrtTab_4", var_list);
	InsTab4 = var_mapping("SQLPutData_InsTab_4", var_list);
	SelTab4 = var_mapping("SQLPutData_SelTab_4", var_list);
	DelTab4 = var_mapping("SQLPutData_DelTab_4", var_list);

	DrpTab5 = var_mapping("SQLPutData_DrpTab_5", var_list);
	CrtTab5 = var_mapping("SQLPutData_CrtTab_5", var_list);
	InsTab5 = var_mapping("SQLPutData_InsTab_5", var_list);
	SelTab5 = var_mapping("SQLPutData_SelTab_5", var_list);

	DrpTab6 = var_mapping("SQLPutData_DrpTab_6", var_list);
	CrtTab6 = var_mapping("SQLPutData_CrtTab_6", var_list);
	InsTab6 = var_mapping("SQLPutData_InsTab_6", var_list);
	SelTab6 = var_mapping("SQLPutData_SelTab_6", var_list);

	CDataValueTOSQL1[0].CrtCol = var_mapping("SQLPutData_CDataValueTOSQL1_CrtCol_0", var_list);
	CDataValueTOSQL1[0].expectedValue[0] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue0_0", var_list);
	CDataValueTOSQL1[0].expectedValue[1] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue1_0", var_list);
	CDataValueTOSQL1[0].expectedValue[12] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue12_0", var_list);
    CDataValueTOSQL1[0].expectedValue[22] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue22_0", var_list);
    CDataValueTOSQL1[0].expectedValue[23] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue23_0", var_list);
    CDataValueTOSQL1[0].expectedValue[24] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue24_0", var_list);

	CDataValueTOSQL1[1].CrtCol = var_mapping("SQLPutData_CDataValueTOSQL1_CrtCol_1", var_list);
	CDataValueTOSQL1[1].expectedValue[0] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue0_1", var_list);
	CDataValueTOSQL1[1].expectedValue[1] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue1_1", var_list);
	CDataValueTOSQL1[1].expectedValue[12] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue12_1", var_list);
    CDataValueTOSQL1[1].expectedValue[22] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue22_1", var_list);
    CDataValueTOSQL1[1].expectedValue[23] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue23_1", var_list);
    CDataValueTOSQL1[1].expectedValue[24] = var_mapping("SQLPutData_CDataValueTOSQL1_OutputValue24_1", var_list);

	CDataValueTOSQL5[0].CrtCol = var_mapping("SQLPutData_CDataValueTOSQL5_CrtCol_0", var_list);
	CDataValueTOSQL5[0].CharValue = var_mapping("SQLPutData_CDataValueTOSQL5_CharValue_0", var_list);
	CDataValueTOSQL5[0].VarCharValue = var_mapping("SQLPutData_CDataValueTOSQL5_VarCharValue_0", var_list);
	CDataValueTOSQL5[0].LongVarCharValue = var_mapping("SQLPutData_CDataValueTOSQL5_LongVarCharValue_0", var_list);
    CDataValueTOSQL5[0].NChar = var_mapping("SQLPutData_CDataValueTOSQL5_NChar_0", var_list);
	CDataValueTOSQL5[0].NCharVarying = var_mapping("SQLPutData_CDataValueTOSQL5_NCharVarying_0", var_list);
	CDataValueTOSQL5[0].NLongCharVarying = var_mapping("SQLPutData_CDataValueTOSQL5_NLongCharVarying_0", var_list);
	CDataValueTOSQL5[0].OutputValue[0] = var_mapping("SQLPutData_CDataValueTOSQL5_CharValue_0", var_list);
	CDataValueTOSQL5[0].OutputValue[1] = var_mapping("SQLPutData_CDataValueTOSQL5_VarCharValue_0", var_list);
	CDataValueTOSQL5[0].OutputValue[12] = var_mapping("SQLPutData_CDataValueTOSQL5_LongVarCharValue_0", var_list);
    CDataValueTOSQL5[0].OutputValue[22] = var_mapping("SQLPutData_CDataValueTOSQL5_NChar_0", var_list);
	CDataValueTOSQL5[0].OutputValue[23] = var_mapping("SQLPutData_CDataValueTOSQL5_NCharVarying_0", var_list);
	CDataValueTOSQL5[0].OutputValue[24] = var_mapping("SQLPutData_CDataValueTOSQL5_NLongCharVarying_0", var_list);

	CDataValueTOSQL5[1].CrtCol = var_mapping("SQLPutData_CDataValueTOSQL5_CrtCol_1", var_list);
	CDataValueTOSQL5[1].CharValue = var_mapping("SQLPutData_CDataValueTOSQL5_CharValue_1", var_list);
	CDataValueTOSQL5[1].VarCharValue = var_mapping("SQLPutData_CDataValueTOSQL5_VarCharValue_1", var_list);
	CDataValueTOSQL5[1].LongVarCharValue = var_mapping("SQLPutData_CDataValueTOSQL5_LongVarCharValue_1", var_list);
    CDataValueTOSQL5[1].NChar = var_mapping("SQLPutData_CDataValueTOSQL5_NChar_1", var_list);
	CDataValueTOSQL5[1].NCharVarying = var_mapping("SQLPutData_CDataValueTOSQL5_NCharVarying_1", var_list);
	CDataValueTOSQL5[1].NLongCharVarying = var_mapping("SQLPutData_CDataValueTOSQL5_NLongCharVarying_1", var_list);
	CDataValueTOSQL5[1].OutputValue[0] = var_mapping("SQLPutData_CDataValueTOSQL5_CharValue_1", var_list);
	CDataValueTOSQL5[1].OutputValue[1] = var_mapping("SQLPutData_CDataValueTOSQL5_VarCharValue_1", var_list);
	CDataValueTOSQL5[1].OutputValue[12] = var_mapping("SQLPutData_CDataValueTOSQL5_LongVarCharValue_1", var_list);
    CDataValueTOSQL5[1].OutputValue[22] = var_mapping("SQLPutData_CDataValueTOSQL5_NChar_1", var_list);
	CDataValueTOSQL5[1].OutputValue[23] = var_mapping("SQLPutData_CDataValueTOSQL5_NCharVarying_1", var_list);
	CDataValueTOSQL5[1].OutputValue[24] = var_mapping("SQLPutData_CDataValueTOSQL5_NLongCharVarying_1", var_list);

	CFloatToNumeric[0].CrtCol = var_mapping("SQLPutData_CFloatToNumeric_0", var_list);
	CFloatToNumeric[1].CrtCol = var_mapping("SQLPutData_CFloatToNumeric_1", var_list);
	CFloatToNumeric[2].CrtCol = var_mapping("SQLPutData_CFloatToNumeric_2", var_list);
	CFloatToNumeric[3].CrtCol = var_mapping("SQLPutData_CFloatToNumeric_3", var_list);
	CFloatToNumeric[4].CrtCol = var_mapping("SQLPutData_CFloatToNumeric_4", var_list);

	CDoubleToNumeric[0].CrtCol = var_mapping("SQLPutData_CDoubleToNumeric_0", var_list);
	CDoubleToNumeric[1].CrtCol = var_mapping("SQLPutData_CDoubleToNumeric_1", var_list);
	CDoubleToNumeric[2].CrtCol = var_mapping("SQLPutData_CDoubleToNumeric_2", var_list);
	CDoubleToNumeric[3].CrtCol = var_mapping("SQLPutData_CDoubleToNumeric_3", var_list);
	CDoubleToNumeric[4].CrtCol = var_mapping("SQLPutData_CDoubleToNumeric_4", var_list);

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API => MX Specific SQLParamData/SQLPutData | SQLPutData | mxputdata.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLParamData/SQLPutData tests\n");

	if(!FullConnect(pTestInfo)){
		LogMsg(NONE,"Unable to connect\n");
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

	TempType1 = (char *)malloc(NAME_LEN);
	strcpy(TempType1,"");
	InsStr = (char *)malloc(MAX_NOS_SIZE);

//====================================================================================================
// converting from c char to all data types

	TestId=1;
	i = 0;
	while (CDataValueTOSQL1[i].CType != 999)
	{
		sprintf(Heading,"Setup for SQLParamData/SQLPutData tests #%d for SQL_C_CHAR.\n",TestId);
		TESTCASE_BEGIN(Heading);

		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab1,SQL_NTS);
		strcpy(InsStr,"");
		strcat(InsStr,CrtTab1);
		strcat(InsStr,CDataValueTOSQL1[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab1,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		
		for (j = 0; j < MAX_PUTPARAM1; j++)
		{
			LogMsg(NONE,"SQLBindParameter, Column #%d, SQL_C_CHAR to %s.\n",j+1,SQLTypeToChar(CDataArgToSQL1.SQLType[j],TempType1));
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

			sprintf(Heading,"Test #%d: Positive Functionality of SQLParamData/SQLPutData.\n",TestId);
			TESTCASE_BEGIN(Heading);

			j = 0;
			while (returncode == SQL_NEED_DATA)
			{
				returncode = SQLParamData(hstmt,&pToken);
				if (returncode == SQL_NEED_DATA)
				{
					if (CDataArgToSQL1.SQLType[j] == SQL_LONGVARCHAR)
					{
                        strcpy(TempType1,(char*)"");
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
							strcat(TempType1,CDataValueTOSQL1[i].expectedValue[j]);
						}
						rc = SQLPutData(hstmt,CDataValueTOSQL1[i].expectedValue[j],strlen(CDataValueTOSQL1[i].expectedValue[j]));
						if(!CHECKRC(SQL_SUCCESS,rc,"SQLPutData"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
					}
					j++;
				}
			}

			LogMsg(NONE,"Getting and verifying data.\n");
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab1,SQL_NTS);
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
					for (j = 0; j < MAX_PUTPARAM1; j++)
					{
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (CDataArgToSQL1.SQLType[j] == SQL_LONGVARCHAR)
							{
								if (_strnicmp(CDataValueTOSQL1[i].expectedValue[j],OutValue,strlen(CDataValueTOSQL1[i].expectedValue[j])) == 0)
								{
									if(g_Trace){
										LogMsg(NONE,"Column %d: expect: %s and actual: %s are matched\n",j+1,TempType1,OutValue);
										}
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,"Column %d: expect: %s and actual: %s are not matched at line: %d\n",j+1,TempType1,OutValue, __LINE__);
								}
							}
							else
							{
								if (_strnicmp(CDataValueTOSQL1[i].expectedValue[j],OutValue,strlen(CDataValueTOSQL1[i].expectedValue[j])) == 0)
								{
									if(g_Trace){
										LogMsg(NONE,"Column %d: expect: %s and actual: %s are matched\n",j+1,CDataValueTOSQL1[i].expectedValue[j],OutValue);
										}
								}	
								else
								{
									TEST_FAILED;	
									LogMsg(ERRMSG,"Column %d: expect: %s and actual: %s are not matched at line: %d\n",j+1,CDataValueTOSQL1[i].expectedValue[j],OutValue, __LINE__);
								}
							}
						}
					} // end for loop
				}
			}
			TESTCASE_END;
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab1,SQL_NTS);
		i++;
		TestId++;
	}

//====================================================================================================
	// converting from ctinyint, cshort and clong to sql 

	sprintf(Heading,"General setup for SQLParamData/SQLPutData tests for ctinyint, cshort and clong.\n");
	TESTCASE_BEGIN(Heading);
	SQLExecDirect(hstmt,(SQLCHAR*) DrpTab2,SQL_NTS);
	returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab2,SQL_NTS);
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
		sprintf(Heading,"Setup for SQLParamData/SQLPutData tests #%d for ctinyint, cshort and clong.\n",TestId);
		TESTCASE_BEGIN(Heading);
		returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab2,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		for (j = 0; j < MAX_PUTPARAM2; j++)
		{
			LogMsg(NONE,"SQLBindParameter from %s to %s\n",CDataValueTOSQL2[i].TestCType, CDataArgToSQL2.TestSQLType[j]);
			InValue1 = SQL_DATA_AT_EXEC;
			switch (CDataValueTOSQL2[i].CType)
			{
				case SQL_C_STINYINT:
				case SQL_C_UTINYINT:
				case SQL_C_TINYINT:
				case SQL_C_SSHORT:
				case SQL_C_USHORT:
				case SQL_C_SHORT:
				case SQL_C_SLONG:
				case SQL_C_ULONG:
				case SQL_C_LONG:
					returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL2[i].CType,
																		CDataArgToSQL2.SQLType[j],CDataArgToSQL2.ColPrec[j],
																		CDataArgToSQL2.ColScale[j],NULL,0,&InValue1);
					break;
				default: 
                    LogMsg(ERRMSG,"UNEXPECTED Bind type\n");
                    break;
			}

			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
	
//		LogMsg(NONE,"Getting and verifying data for %s.\n",CDataValueTOSQL2[i].TestCType);

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

			sprintf(Heading,"Test #%d: Positive Functionality of SQLParamData/SQLPutData.\n",TestId);
			TESTCASE_BEGIN(Heading);
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

			LogMsg(NONE,"Getting and verifying data for %s.\n",CDataValueTOSQL2[i].TestCType);
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab2,SQL_NTS);
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
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (_strnicmp(CDataValueTOSQL2[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL2[i].OutputValue[j])) == 0)
							{
								if(g_Trace){
									LogMsg(NONE,"Column %d: expect: %s and actual: %s are matched\n",j+1,CDataValueTOSQL2[i].OutputValue[j],OutValue);
									}
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"Column %d: expect: %s and actual: %s are not matched at line: %d\n",j+1,CDataValueTOSQL2[i].OutputValue[j],OutValue,__LINE__);
							}
						}
					} // end for loop
				}
			}
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)DelTab2,SQL_NTS);
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
		sprintf(Heading,"Setup for SQLParamData/SQLPutData tests #%d for cfloat and cdouble\n",TestId);
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab3,SQL_NTS);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab3,SQL_NTS);
	 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		LogMsg(NONE,"Prepare for %s.\n",CDataValueTOSQL3[i].TestCType);
		returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab3,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		for (j = 0; j < MAX_PUTPARAM3; j++)
		{
			LogMsg(NONE,"SQLBindParameter to convert from %s to %s\n",CDataValueTOSQL3[i].TestCType, CDataArgToSQL3.TestSQLType[j]);
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

			sprintf(Heading,"Test #%d: (SQLParamData/SQLPutData) checking %s tests \n",TestId,CDataValueTOSQL3[i].TestCType);
			TESTCASE_BEGIN(Heading);
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

			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab3,SQL_NTS);
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
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (_strnicmp(CDataValueTOSQL3[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL3[i].OutputValue[j])) == 0)
							{
								if(g_Trace){
									//LogMsg(NONE,"Column #%d: expect: %s and actual: %s are matched\n",
									//	j+1,CDataValueTOSQL3[i].OutputValue[j],OutValue);
								}
							}	
							else if (_strnicmp(CDataValueTOSQL3[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL3[i].OutputValue[j])-1) == 0)
							{
								TIMtemp = strlen(CDataValueTOSQL3[i].OutputValue[j])-1;
								if ((CDataValueTOSQL3[i].OutputValue[j][TIMtemp]) == (OutValue[TIMtemp] + 1))
									LogMsg(NONE,"Column #%d: expect: %s and actual: %s are matched\n",
										j+1,CDataValueTOSQL3[i].OutputValue[j],OutValue);
								else
									LogMsg(ERRMSG,"Column #%d: expect: %s and actual: %s are not matched at line: %d\n",
										j+1,CDataValueTOSQL3[i].OutputValue[j],OutValue,__LINE__);
							}
							else
							{
								TEST_FAILED;	
								LogMsg(ERRMSG,"Column #%d: expect: %s	and actual: %s are not matched at line: %d\n",
									j+1,CDataValueTOSQL3[i].OutputValue[j],OutValue,__LINE__);
							}
						}
					} // end for loop
				}
			}
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)DelTab3,SQL_NTS);
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
		sprintf(Heading,"Setup for SQLParamData/SQLPutData tests #%d for cdate, ctime and ctimestamp\n",TestId);
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab4,SQL_NTS);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTab4,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		LogMsg(NONE,"SQLPrepare for %s.\n",CDataValueTOSQL4[i].TestCType);
		returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab4,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		for (j = 0; j < MAX_PUTPARAM4; j++)
		{
			LogMsg(NONE,"SQLBindParameter for Column %d to convert from %s to %s\n",j+1,CDataValueTOSQL4[i].TestCType, CDataArgToSQL4.TestSQLType[j]);
			InValue1 = SQL_DATA_AT_EXEC;
			switch (CDataValueTOSQL4[i].CType)
			{
				case SQL_C_DATE:
                    if (CDataArgToSQL4.SQLType[j] != SQL_TIME) {
						returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL4[i].CType,
																			CDataArgToSQL4.SQLType[j],CDataArgToSQL4.ColPrec[j],
																			CDataArgToSQL4.ColScale[j],NULL,0,&InValue1);
                    }
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
				default: 
                    LogMsg(ERRMSG,"Unexpected Bind type\n");
                    break;
			}

			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
		}
	
		LogMsg(NONE,"Setup for checking SQLParamData/SQLPutData tests %s.\n",CDataValueTOSQL4[i].TestCType);

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

			sprintf(Heading,"Test #%d: (SQLParamData/SQLPutData) checking %s tests \n",TestId,CDataValueTOSQL4[i].TestCType);
			TESTCASE_BEGIN(Heading);
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
/* sq new */
								if (CDataArgToSQL4.SQLType[j] == SQL_TIMESTAMP)
								{
									struct tm *newtime;
									time_t long_time;

									time( &long_time );
									newtime = localtime( &long_time );
									strftime (tmpbuf, 60, "%Y-%m-%d ", newtime);
									strcat(tmpbuf,CDataValueTOSQL4[i].OutputValue[j]);
									CDataValueTOSQL4[i].OutputValue[j]=strdup(tmpbuf);
									strcpy(tmpbuf,"");
								}
/* end of sq new */
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
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab4,SQL_NTS);
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
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
                            LogMsg(NONE,"SQLParamData/SQLPutData test: checking data for column c%d\n",j+1);
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (_strnicmp(CDataValueTOSQL4[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL4[i].OutputValue[j])) == 0)
							{
								if(g_Trace){
									LogMsg(NONE,"expect: %s and actual: %s are matched\n",
										CDataValueTOSQL4[i].OutputValue[j],OutValue);
									}	
								}
							else
							{
                                LogMsg(NONE,"SQLParamData/SQLPutData test: checking data for column c%d\n",j+1);
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %s	and actual: %s are not matched at line: %d\n",
									CDataValueTOSQL4[i].OutputValue[j],OutValue,__LINE__);
							}
						}
					} // end for loop
				}
			}
		}
		SQLFreeStmt(hstmt,SQL_CLOSE);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)DelTab4,SQL_NTS);
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
		sprintf(Heading,"Setup for SQLParamData/SQLPutData tests #%d for SQL_C_DEFAULT.\n",TestId);
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab5,SQL_NTS);
		strcpy(InsStr,"");
		strcat(InsStr,CrtTab5);
		strcat(InsStr,CDataValueTOSQL5[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab5,SQL_NTS);
 		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

        for(j=0;j<MAX_PUTPARAM1;j++) {
            LogMsg(NONE,"SQLBindParameter from SQL_C_DEFAULT to %s\n", SQLTypeToChar(CDataArgToSQL5.SQLType[j],TempType1));
            InValue = SQL_DATA_AT_EXEC;
            if(CDataArgToSQL5.SQLType[j] == SQL_TIMESTAMP ||
               CDataArgToSQL5.SQLType[j] == SQL_TIME ||
               CDataArgToSQL5.SQLType[j] == SQL_DATE ||
               CDataArgToSQL5.SQLType[j] == SQL_DOUBLE ||
               CDataArgToSQL5.SQLType[j] == SQL_FLOAT ||
               CDataArgToSQL5.SQLType[j] == SQL_REAL || 
               CDataArgToSQL5.SQLType[j] == SQL_INTEGER || 
               CDataArgToSQL5.SQLType[j] == SQL_SMALLINT ) 
            {
                BuffLen = ZERO_LEN;
            } else {
                BuffLen = NAME_LEN;
            }
		    returncode = SQLBindParameter(hstmt,(SWORD)(j+1),ParamType,CDataValueTOSQL5[i].CType,
																	    CDataArgToSQL5.SQLType[j],
																	    CDataValueTOSQL5[i].ColPrec[j],
																	    CDataValueTOSQL5[i].ColScale[j],
																	    NULL,BuffLen,&InValue);
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
			TESTCASE_END;		// end of setup
		}
		else
		{
			TESTCASE_END;		// end of setup

			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,CDataValueTOSQL5[i].CharValue,strlen(CDataValueTOSQL5[i].CharValue));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,CDataValueTOSQL5[i].VarCharValue,strlen(CDataValueTOSQL5[i].VarCharValue));
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
				returncode = SQLPutData(hstmt,CDataValueTOSQL5[i].LongVarCharValue,strlen(CDataValueTOSQL5[i].LongVarCharValue));
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

            returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,CDataValueTOSQL5[i].NChar,strlen(CDataValueTOSQL5[i].NChar));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
            returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,CDataValueTOSQL5[i].NCharVarying,strlen(CDataValueTOSQL5[i].NCharVarying));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
            returncode = SQLParamData(hstmt,&pToken);
			if (returncode == SQL_NEED_DATA)
			{
				returncode = SQLPutData(hstmt,CDataValueTOSQL5[i].NLongCharVarying,strlen(CDataValueTOSQL5[i].NLongCharVarying));
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPutData"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
			}
			returncode = SQLParamData(hstmt,&pToken);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLParamData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab5,SQL_NTS);
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
					for (j = 0; j < MAX_PUTPARAM1; j++)
					{
						returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
						if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
						{
                            LogMsg(LINEBEFORE,"SQLParamData/SQLPutData test:checking data for column c%d\n",j+1);
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
						else
						{
							if (_strnicmp(CDataValueTOSQL5[i].OutputValue[j],OutValue,strlen(CDataValueTOSQL5[i].OutputValue[j])) == 0)
							{
								if(g_Trace){
									LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDataValueTOSQL5[i].OutputValue[j],OutValue);
									}
							}	
							else
							{
                                LogMsg(LINEBEFORE,"SQLParamData/SQLPutData test:checking data for column c%d\n",j+1);
								TEST_FAILED;	
								LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line: %d\n",CDataValueTOSQL5[i].OutputValue[j],OutValue,__LINE__);
							}
						}
					} // end for loop
				}
			}
		}
		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab5,SQL_NTS);
		i++;
		TestId++;
	}

//=================================================================================================================
// Section #6: convert SQL_C_FLOAT to SQL_NUMERIC
    i = 0;
	while (CFloatToNumeric[i].PassFail != 999)
	{
		TESTCASE_BEGIN("SQLPutData tests to bind from SQL_C_FLOAT to SQL_NUMERIC.\n");
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab6,SQL_NTS);
        sprintf(InsStr, "%s %s", CrtTab6, CFloatToNumeric[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab6,SQL_NTS);
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

        returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab6,SQL_NTS);
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
					returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
					{
                        LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						if (strncmp(CFloatToNumeric[i].OutputValue[j],OutValue,strlen(CFloatToNumeric[i].OutputValue[j])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CFloatToNumeric[i].OutputValue[j],OutValue);
						}	
						else
						{
                            LogMsg(NONE,"SQLBindParameter test:checking data for column c%d\n",j+1);
							TEST_FAILED;	
                            //LogMsg(NONE,"Float input value: %f\n", CFloatToNumeric[i].FloatValue[j]);
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line %d\n",CFloatToNumeric[i].OutputValue[j],OutValue,__LINE__);
						}
					}
				} // end for loop
			}
		}

		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab6,SQL_NTS);
		i++;
	}

//=================================================================================================================
// Section #7: convert SQL_C_DOUBLE to SQL_NUMERIC

    i = 0;
	while (CDoubleToNumeric[i].PassFail != 999)
	{
		TESTCASE_BEGIN("SQLPutData tests to bind from SQL_C_DOUBLE to SQL_NUMERIC.\n");
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab6,SQL_NTS);
        sprintf(InsStr, "%s %s", CrtTab6, CDoubleToNumeric[i].CrtCol);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}

		returncode = SQLPrepare(hstmt,(SQLCHAR*)InsTab6,SQL_NTS);
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

        returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTab6,SQL_NTS);
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
					returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_CHAR,OutValue,NAME_LEN,&OutValueLen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
					{
                        LogMsg(NONE,"SQLPutData test:checking data for column c%d\n",j+1);
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
					else
					{
						if (strncmp(CDoubleToNumeric[i].OutputValue[j],OutValue,strlen(CDoubleToNumeric[i].OutputValue[j])) == 0)
						{
							//LogMsg(NONE,"expect: %s and actual: %s are matched\n",CDoubleToNumeric[i].OutputValue[j],OutValue);
						}	
						else
						{
/* sq NEW */                                if (labs((long)(atof(CDoubleToNumeric[i].OutputValue[j]) - atof(OutValue)) > 0.001)) {
                            LogMsg(NONE,"SQLPutData test:checking data for column c%d\n",j+1);
							TEST_FAILED;	
                            //LogMsg(NONE,"Float input value: %f\n", CDoubleToNumeric[i].FloatValue[j]);
							LogMsg(ERRMSG,"expect: %s and actual: %s are not matched at line %d\n",CDoubleToNumeric[i].OutputValue[j],OutValue,__LINE__);
/* sq */					     }
						}
					}
				} // end for loop
			}
		}

		TESTCASE_END;
		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTab6,SQL_NTS);
		i++;
	}

//=================================================================================================================

	free(TempType1);
	free(InsStr);
	FullDisconnect(pTestInfo);
	free_list(var_list);
	LogMsg(SHORTTIMESTAMP+LINEBEFORE+LINEAFTER,
		"End testing API => MX Specific SQLSQLParamData/SQLPutData.\n");
	TEST_RETURN;
}

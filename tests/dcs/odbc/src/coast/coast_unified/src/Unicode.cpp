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


#include <wchar.h>
#include <stdio.h>
#include <time.h>
#include <windows.h>
#include "basedef.h"
#include "common.h"
#include "log.h"
#include "apitests.h"

#define NAME_LEN		300
#define	MAX_BINDPARAM1	14

SQLRETURN		retcode;
SQLINTEGER		BufferLength;
SQLLEN	 		Strlen_or_IndPtr;

SQLTCHAR *drpsql = (SQLTCHAR *) _T("DROP TABLE ZING_NCHAR");
SQLTCHAR *crtsql = (SQLTCHAR *) _T("CREATE TABLE ZING_NCHAR (C1 NCHAR(10), C2 INTEGER, C3 NCHAR (10), C4 NCHAR VARYING(10), C5 NCHAR(1), C6 REAL, C7 CHAR(10), C8 NCHAR(1)) NO PARTITION");
SQLTCHAR *inssql = (SQLTCHAR *) _T("insert into zing_nchar values (?,?,?,?,?,?,?,?)");
SQLTCHAR *selsql = (SQLTCHAR *) _T("select {fn RTRIM(C1)},C2,{fn RTRIM(C3)},C4,{fn RTRIM(C5)},C6,{fn RTRIM(C7)},{fn RTRIM(C8)} from zing_nchar");

//BufferLength should be 0 in all bindparams
TCHAR buffer1[100] = _T("ABCDEF");
TCHAR buffer2[100] = _T("123");
TCHAR buffer3[100] = _T("PQR");
TCHAR buffer4[100] = _T("XYZ!@@#@$!");
TCHAR buffer5[100] = _T("A");
TCHAR buffer6[100] = _T("123.567");
TCHAR buffer7[100] = _T("MNOPQ");
TCHAR buffer8[100] = _T("*");

TCHAR *OutputValue[100] = {_T("ABCDEF"), _T("123"), _T("PQR"), _T("XYZ!@@#@$!"), _T("A"), _T("123.5670013"), _T("MNOPQ"), _T("*")};

SQLWCHAR lbuffer1[100] = L"ABCDEF";
SQLWCHAR lbuffer2[100] = L"123";
SQLWCHAR lbuffer3[100] = L"PQR";
SQLWCHAR lbuffer4[100] = L"XYZ!@@#@$!";
SQLWCHAR lbuffer5[100] = L"A";
SQLWCHAR lbuffer6[100] = L"123.567";
SQLWCHAR lbuffer7[100] = L"MNOPQ";
SQLWCHAR lbuffer8[100] = L"*";

struct{
	SQLWCHAR lbuffer[100];
}lOutputValue[] = 
{
	{
		L"ABCDEF"
	},
	{
		L"123"
	},
	{
		L"PQR"
	},
	{
		L"XYZ!@@#@$!"
	},
	{
		L"A"
	},
	{
		L"123.567"
	},
	{
		L"MNOPQ"
	},
	{
		L"*"
	}
};

PassFail TestMXSQLBindParameterUnicode(TestInfo *);

PassFail TestUnicodeSetup (TestInfo *);
PassFail TestUnicodeTest1 (TestInfo *);
PassFail TestUnicodeTest2 (TestInfo *);
PassFail TestUnicodeTest3 (TestInfo *);
PassFail TestUnicodeTest4 (TestInfo *);
PassFail TestUnicodeTest5 (TestInfo *);
PassFail TestUnicodeTest6 (TestInfo *);
PassFail TestUnicodeTest7 (TestInfo *);
PassFail TestUnicodeTest8 (TestInfo *);

PassFail TestMXSQLUnicode(TestInfo *pTestInfo)
{
	PassFail ret; 
	ret = TestMXSQLBindParameterUnicode(pTestInfo);
	return ret;
}

PassFail TestMXSQLBindParameterUnicode(TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TCHAR		*InsStr;
	TCHAR		*TempType1;

	TCHAR		Heading[MAX_STRING_SIZE];
	RETCODE		returncode;
	SQLHANDLE 	henv;
	SQLHANDLE 	hdbc;
	SQLHANDLE	hstmt;
	int			i, j;
	int			loop_bindparam;
	SQLSMALLINT	ParamType = SQL_PARAM_INPUT;
	SQLLEN		InValue = SQL_NTS, InValue1 = 0, InValueNullData = SQL_NULL_DATA;
	TCHAR		OutValue[NAME_LEN];
	SQLLEN		OutValueLen;

//************************************************
// Data structures for Testing Section #5

	struct // We have to support bit, tinyint, binary, varbinary, long varbinary
	{
		SQLSMALLINT	SQLType[MAX_BINDPARAM1];
	} CDataArgToSQL5 = 
		{
			SQL_WCHAR, SQL_WVARCHAR,SQL_DECIMAL,SQL_NUMERIC,SQL_SMALLINT,SQL_INTEGER,SQL_REAL,
			SQL_FLOAT,SQL_DOUBLE,SQL_DATE,SQL_TIME,SQL_TIMESTAMP,SQL_WVARCHAR,SQL_BIGINT
		};

	struct
	{
		SQLSMALLINT		CType;
		RETCODE			PassFail;
		BOOL			NullData;
		TCHAR			*CrtCol;
		SQLUINTEGER		ColPrec[MAX_BINDPARAM1];
		SQLSMALLINT		ColScale[MAX_BINDPARAM1];
		wchar_t			*CharValue;
		wchar_t			*VarCharValue;
		char			*DecimalValue;
		char			*NumericValue;
		SWORD			ShortValue;
		SDWORD			LongValue;
		SFLOAT			RealValue;
		SDOUBLE			FloatValue;
		SDOUBLE			DoubleValue;
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
			unsigned long int	fraction;
		} TimestampValue;
		wchar_t			*LongVarCharValue;
		#if !defined(PLATFORM)
			_int64	  			BigintValue;
		#else
			long long  			BigintValue;
		#endif
		TCHAR				*OutputValue[MAX_BINDPARAM1];
	} CDataValueTOSQL5[] = 
		{		// real, float and double precision to TCHAR has problem it returns 12345.0 values as 12345.
			{	SQL_C_DEFAULT,
				SQL_SUCCESS,
				FALSE,
				_T("(C1 NCHAR(10),C2 NCHAR VARYING (10),C3 DECIMAL(10,5),C4 NUMERIC(10,5),C5 SMALLINT,C6 INTEGER,C7 REAL,C8 FLOAT,C9 DOUBLE PRECISION,C10 DATE,C11 TIME,C12 TIMESTAMP,C13 LONG VARCHAR character set ucs2,C14 BIGINT) NO PARTITION"),
				254,254,10,10,5,10,7,15,15,0,0,26,2000,19,
				0,0,5,5,0,0,0,0,0,0,0,6,0,0,
				L"0123456789",
				L"0123456789",
				"1234.56789",
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,0},
				L"0123456789",
				123456,
#ifndef _WM
				_T("0123456789"),_T("0123456789"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340"),_T("12300"),_T("12345670"),_T("1993-12-30"),_T("11:45:23"),_T("1997-10-12 11:33:41.000000"),_T("0123456789"),_T("123456")
#else
				_T("0123456789"),_T("0123456789"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340"),_T("12300"),_T("12345670"),_T("93/12/30"),_T("11:45:23"),_T("1997-10-12 11:33:41.000000"),_T("0123456789"),_T("123456")
#endif
			},
			//5/9/06: For bad data testing
			{
				SQL_C_DEFAULT,
				SQL_ERROR, 
				FALSE,
				_T("(C1 NCHAR(10),C2 NCHAR VARYING (10),C3 DECIMAL(10,5),C4 NUMERIC(10,5),C5 SMALLINT,C6 INTEGER,C7 REAL,C8 FLOAT,C9 DOUBLE PRECISION,C10 DATE,C11 TIME,C12 TIMESTAMP,C13 LONG VARCHAR,C14 BIGINT) NO PARTITION"),
				254,254,10,10,5,10,7,15,15,0,0,26,2000,19,
				0,0,5,5,0,0,0,0,0,0,0,6,0,0,
				L"01234567890ABCDE",//error
				L"01234567890abcde",//error
				"123",
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,15,60},
				{11,85,93},
				{1997,15,42,11,33,41,123456},
				L"0123456789",
				123456,
				_T("0123456789"),_T("0123456789"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340"),_T("12300"),_T("12345670"),_T("1993-12-30"),_T("11:45:23"),_T("1997-10-12 11:33:41.000123"),_T("0123456789"),_T("123456")
			},
			{	
				SQL_C_DEFAULT,
				SQL_ERROR,
				FALSE,
				_T("(C1 NCHAR(10),C2 NCHAR VARYING (10),C3 DECIMAL(10,5),C4 NUMERIC(10,5),C5 SMALLINT,C6 INTEGER,C7 REAL,C8 FLOAT,C9 DOUBLE PRECISION,C10 DATE,C11 TIME,C12 TIMESTAMP,C13 LONG VARCHAR character set ucs2,C14 BIGINT) NO PARTITION"),
				254,254,10,10,5,10,7,15,15,0,0,26,2000,19,
				0,0,5,5,0,0,0,0,0,0,0,6,0,0,
				L"0123456789",
				L"0123456789",
				"123-",//error
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,15,60},
				{11,85,93},
				{1997,15,42,11,33,41,123456},
				L"01234567890",
				123456,
				_T("0123456789"),_T("0123456789"),_T("123"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340"),_T("12300"),_T("12345670"),_T("1993-12-30"),_T("11:45:23"),_T("1997-10-12 11:33:41.000123"),_T("0123456789"),_T("123456")
			},
			{	//*******************************err
				SQL_C_DEFAULT,//c_numeric
				SQL_ERROR,
				FALSE,
				_T("(C1 NCHAR(10),C2 NCHAR VARYING (10),C3 DECIMAL(10,5),C4 NUMERIC(10,5),C5 SMALLINT,C6 INTEGER,C7 REAL,C8 FLOAT,C9 DOUBLE PRECISION,C10 DATE,C11 TIME,C12 TIMESTAMP,C13 LONG VARCHAR,C14 BIGINT) NO PARTITION"),
				254,254,10,10,5,10,7,15,15,0,0,26,2000,19,
				0,0,5,5,0,0,0,0,0,0,0,6,0,0,
				L"0123456789",
				L"0123456789",
				"1234.56789-", //error
				"5678.12345",//{10,5,1,0xF9,0x20,0xD8,0x21,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00},
				1234,
				12345,
				12340.0,
				12300.0,
				12345670.0,
				{1993,12,30},
				{11,45,23},
				{1997,10,12,11,33,41,123456},
				L"0123456789",
				123456,
				_T("0123456789"),_T("0123456789"),_T("1234.56789"),_T("5678.12345"),_T("1234"),_T("12345"),_T("12340"),_T("12300"),_T("12345670"),_T("1993-12-30"),_T("11:45:23"),_T("1997-10-12 11:33:41.000123"),_T("0123456789"),_T("123456")
			},
			{	999,}
		};
	TCHAR	*DrpTab5 = _T("DROP TABLE SQLCDEFAULTTOSQL");
	TCHAR	*CrtTab5 = _T("CREATE TABLE SQLCDEFAULTTOSQL");
	TCHAR	*InsTab5 = _T("INSERT INTO SQLCDEFAULTTOSQL (C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)");
	TCHAR	*SelTab5 = _T("SELECT C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,C13,C14 FROM SQLCDEFAULTTOSQL");

//**********************************	

	struct // We have to support bit, tinyint, binary, varbinary, long varbinary
	{
		SQLSMALLINT	SQLType[4];
	} CDataArgToSQL9 = 
		{
			SQL_WCHAR,SQL_INTEGER,SQL_WVARCHAR,SQL_WLONGVARCHAR
		};
	struct
	{
		SQLSMALLINT		CType;
		RETCODE			PassFail;
		BOOL			NullData;
		TCHAR			*CrtCol;
		SQLUINTEGER		ColPrec[4];
		SQLSMALLINT		ColScale[4];
		SQLWCHAR	CharValue[100];
		SQLWCHAR	IntegerValue[100];
		SQLWCHAR	VarCharValue[100];
		SQLWCHAR	LongVarCharValue[100];
		SQLWCHAR	*OutputValue[4];
	} CDataValueTOSQL9[] = 
		{
			{	SQL_C_WCHAR,
				SQL_SUCCESS,
				FALSE,
				_T("(C1 NCHAR(10), C2 INTEGER, C3 NCHAR (10), C4 NCHAR VARYING(10)) NO PARTITION"),
				100,100,100,100,
				0,0,0,0,
				L"ABC", 
				L"123",
				L"PQR",
				L"XYZ",
				L"ABC",L"123",L"PQR",L"XYZ"
			},
			{	SQL_C_WCHAR,
				SQL_ERROR,
				FALSE,
				_T("(C1 NCHAR(10), C2 INTEGER, C3 NCHAR (10), C4 NCHAR VARYING(10)) NO PARTITION"),
				100,100,100,100,
				0,0,0,0,
				L"ABC", 
				L"123-",
				L"PQR",
				L"XYZ",
				L"ABC",L"123",L"PQR",L"XYZ"
			},
			{	999,}
		};
	TCHAR	*DrpTab9 = _T("DROP TABLE SQLCCHARTOSQL1");
	TCHAR	*CrtTab9 = _T("CREATE TABLE SQLCCHARTOSQL1");
	TCHAR	*InsTab9 = _T("INSERT INTO SQLCCHARTOSQL1 (C1,C2,C3,C4) VALUES (?,?,?,?)");
	TCHAR	*SelTab9 = _T("SELECT C1,C2,C3,C4 FROM SQLCCHARTOSQL1");
//=============================================================================================
// Initialization Test Case

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => Unicode.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("SQLBindParameter/SQLGetData/SQLBindCol\n");

	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;

	returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(henv,hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END; 

	TempType1 = (TCHAR *)malloc(NAME_LEN);
	_tcscpy(TempType1,_T(""));
	InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);

//=================================================================================================================
// Testing Section #5
// converting from cdefault to sql
	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL5[i].CType != 999)
		{
			// Creating the table
			//TESTCASE_BEGIN("Setup for SQLBindParameter tests to create table for SQL_C_DEFAULT.\n");
			TESTCASE_BEGIN("");
			SQLExecDirect(hstmt, (SQLTCHAR*)DrpTab5,SQL_NTS);
			_tcscpy(InsStr,_T(""));
			_tcscat(InsStr,CrtTab5);
			_tcscat(InsStr,CDataValueTOSQL5[i].CrtCol);
            LogMsg(NONE,_T("%s\n"),InsStr);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
				//TestMXSQLBindParamaterVer3_Cleanup(hstmt,"",TempType1,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END;

			// Preparing for an insert into the table.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for Unicode SQLBindParameter tests for prepare SQL_C_DEFAULT.\n"));
				//TESTCASE_BEGINW(Heading);
				TESTCASE_BEGIN("");
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTab5,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					//TestMXSQLBindParamaterVer3_Cleanup(hstmt,DrpTab5,TempType1,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}

			// Binding with all of the columns in the table.... this goes on for awhile.
			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_WCHAR.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[0],CDataValueTOSQL5[i].ColPrec[0],
																			CDataValueTOSQL5[i].ColScale[0],CDataValueTOSQL5[i].CharValue,NAME_LEN,
																			&InValue);
                /*LogMsg(NONE,_T("SQLBindParamter(hstmt,%d,%d,%d,%d,%d,%d,%s,%d,%d)\n"),(SWORD)(1),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[0],CDataValueTOSQL5[i].ColPrec[0],
																			CDataValueTOSQL5[i].ColScale[0],CDataValueTOSQL5[i].CharValue,NAME_LEN,
																			InValue);*/
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[0],CDataValueTOSQL5[i].ColPrec[0],
																			CDataValueTOSQL5[i].ColScale[0],NULL,NAME_LEN,
																			&InValueNullData);
                /*LogMsg(NONE,_T("SQLBindParamter(hstmt,%d,%d,%d,%d,%d,%d,%s,%d,%d)\n"),(SWORD)(1),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[0],CDataValueTOSQL5[i].ColPrec[0],
																			CDataValueTOSQL5[i].ColScale[0],NULL,NAME_LEN,
																			InValueNullData);*/
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
		
			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_WVARCHAR.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[1],CDataValueTOSQL5[i].ColPrec[1],
																			CDataValueTOSQL5[i].ColScale[1],CDataValueTOSQL5[i].VarCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[1],CDataValueTOSQL5[i].ColPrec[1],
																			CDataValueTOSQL5[i].ColScale[1],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_DECIMAL.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[2],CDataValueTOSQL5[i].ColPrec[2],
																			CDataValueTOSQL5[i].ColScale[2],CDataValueTOSQL5[i].DecimalValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[2],CDataValueTOSQL5[i].ColPrec[2],
																			CDataValueTOSQL5[i].ColScale[2],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_NUMERIC.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[3],CDataValueTOSQL5[i].ColPrec[3],
																			CDataValueTOSQL5[i].ColScale[3],CDataValueTOSQL5[i].NumericValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[3],CDataValueTOSQL5[i].ColPrec[3],
																			CDataValueTOSQL5[i].ColScale[3],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_SMALLINT.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(5),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[4],CDataValueTOSQL5[i].ColPrec[4],
																			CDataValueTOSQL5[i].ColScale[4],&(CDataValueTOSQL5[i].ShortValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(5),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[4],CDataValueTOSQL5[i].ColPrec[4],
																			CDataValueTOSQL5[i].ColScale[4],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_INTEGER.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(6),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[5],CDataValueTOSQL5[i].ColPrec[5],
																			CDataValueTOSQL5[i].ColScale[5],&(CDataValueTOSQL5[i].LongValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(6),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[5],CDataValueTOSQL5[i].ColPrec[5],
																			CDataValueTOSQL5[i].ColScale[5],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_REAL.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(7),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[6],CDataValueTOSQL5[i].ColPrec[6],
																			CDataValueTOSQL5[i].ColScale[6],&(CDataValueTOSQL5[i].RealValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(7),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[6],CDataValueTOSQL5[i].ColPrec[6],
																			CDataValueTOSQL5[i].ColScale[6],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_FLOAT.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(8),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[7],CDataValueTOSQL5[i].ColPrec[7],
																			CDataValueTOSQL5[i].ColScale[7],&(CDataValueTOSQL5[i].FloatValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(8),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[7],CDataValueTOSQL5[i].ColPrec[7],
																			CDataValueTOSQL5[i].ColScale[7],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_DOUBLE.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(9),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[8],CDataValueTOSQL5[i].ColPrec[8],
																			CDataValueTOSQL5[i].ColScale[8],&(CDataValueTOSQL5[i].DoubleValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(9),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[8],CDataValueTOSQL5[i].ColPrec[8],
																			CDataValueTOSQL5[i].ColScale[8],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_DATE.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(10),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[9],CDataValueTOSQL5[i].ColPrec[9],
																			CDataValueTOSQL5[i].ColScale[9],&(CDataValueTOSQL5[i].DateValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(10),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[9],CDataValueTOSQL5[i].ColPrec[9],
																			CDataValueTOSQL5[i].ColScale[9],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_TIME.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(11),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[10],CDataValueTOSQL5[i].ColPrec[10],
																			CDataValueTOSQL5[i].ColScale[10],&(CDataValueTOSQL5[i].TimeValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(11),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[10],CDataValueTOSQL5[i].ColPrec[10],
																			CDataValueTOSQL5[i].ColScale[10],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_TIMESTAMP.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(12),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[11],CDataValueTOSQL5[i].ColPrec[11],
																			CDataValueTOSQL5[i].ColScale[11],&(CDataValueTOSQL5[i].TimestampValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(12),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[11],CDataValueTOSQL5[i].ColPrec[11],
																			CDataValueTOSQL5[i].ColScale[11],NULL,0,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_WLONGVARCHAR.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(13),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[12],CDataValueTOSQL5[i].ColPrec[12],
																			CDataValueTOSQL5[i].ColScale[12],CDataValueTOSQL5[i].LongVarCharValue,NAME_LEN,
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(13),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[12],CDataValueTOSQL5[i].ColPrec[12],
																			CDataValueTOSQL5[i].ColScale[12],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;

			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_DEFAULT to SQL_BIGINT.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL5[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(14),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[13],CDataValueTOSQL5[i].ColPrec[13],
																			CDataValueTOSQL5[i].ColScale[13],&(CDataValueTOSQL5[i].BigintValue),0,
																			&InValue1);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(14),ParamType,CDataValueTOSQL5[i].CType,
																			CDataArgToSQL5.SQLType[13],CDataValueTOSQL5[i].ColPrec[13],
																			CDataValueTOSQL5[i].ColScale[13],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
			// Finished binding.....

			// Now executing the insert statement.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for Unicode SQLBindParameter tests for Execute SQL_C_DEFAULT.\n"));
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(CDataValueTOSQL5[i].PassFail,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for Unicode SQLBindParameter tests for ExecDirect SQL_C_DEFAULT.\n"));
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTab5,SQL_NTS);
				if(!CHECKRC(CDataValueTOSQL5[i].PassFail,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if(returncode == SQL_SUCCESS)
			{
				_stprintf(Heading,_T("Setup for checking Unicode SQLBindParameter tests SQL_C_DEFAULT.\n"));
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab5,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						for (j = 0; j < MAX_BINDPARAM1; j++)
						{
							LogMsg(NONE,_T("Unicode SQLBindParameter test:checking data for column c%d\n"),j+1);
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (!CDataValueTOSQL5[i].NullData)
								{
									if (_tcsnicmp(CDataValueTOSQL5[i].OutputValue[j],(const TCHAR*)OutValue,_tcslen(CDataValueTOSQL5[i].OutputValue[j])) == 0)
									{
										//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueTOSQL5[i].OutputValue[j],OutValue);
									}	
									else
									{
										TEST_FAILED;	
										LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched %d\n"),CDataValueTOSQL5[i].OutputValue[j],OutValue,__LINE__);
									}
								}
								else
								{
									if (OutValueLen == SQL_NULL_DATA)
									{
										//LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQL_NULL_DATA,OutValueLen);
									}	
									else
									{
										TEST_FAILED;	
										LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched %d\n"),SQL_NULL_DATA,OutValueLen, __LINE__);
									}
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt, (SQLTCHAR*)DrpTab5,SQL_NTS);

//=================================================================================================================
// Testing Section #9
// converting from TCHAR to sql
	for (loop_bindparam = 0; loop_bindparam < BINDPARAM_FOR_PREPEXEC_EXECDIRECT; loop_bindparam++)
	{
		i = 0;
		while (CDataValueTOSQL9[i].CType != 999)
		{
			// Creating the table
			TESTCASE_BEGIN("Setup for SQLBindParameter tests to create table for SQL_C_TCHAR.\n");
			SQLExecDirect(hstmt, (SQLTCHAR*)DrpTab9,SQL_NTS);
			_tcscpy(InsStr,_T(""));
			_tcscat(InsStr,CrtTab9);
			_tcscat(InsStr,CDataValueTOSQL9[i].CrtCol);
			returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
 			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
			{
				LogAllErrorsVer3(henv,hdbc,hstmt);
                //TestMXSQLBindParamaterVer3_Cleanup(hstmt,"",TempType1,InsStr,pTestInfo);
				TEST_FAILED;
				TEST_RETURN;
			}
			TESTCASE_END; 

			// Preparing for an insert into the table.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for Unicode SQLBindParameter tests for prepare SQL_C_TCHAR.\n"));
				TESTCASE_BEGINW(Heading);
				returncode = SQLPrepare(hstmt,(SQLTCHAR*)InsTab9,SQL_NTS);
 				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare"))
				{
					LogAllErrorsVer3(henv,hdbc,hstmt);
					//TestMXSQLBindParamaterVer3_Cleanup(hstmt,DrpTab9,TempType1,InsStr,pTestInfo);
					TEST_FAILED;
					TEST_RETURN;
				}
				TESTCASE_END; 
			}
			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_TCHAR to SQL_WCHAR.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL9[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL9[i].CType,
																			CDataArgToSQL9.SQLType[0],wcslen(CDataValueTOSQL9[i].CharValue) * sizeof(SQLWCHAR),
																			0,&(CDataValueTOSQL9[i].CharValue),wcslen(CDataValueTOSQL9[i].CharValue) * sizeof(SQLWCHAR),
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(1),ParamType,CDataValueTOSQL9[i].CType,
																			CDataArgToSQL9.SQLType[0],CDataValueTOSQL9[i].ColPrec[0],
																			CDataValueTOSQL9[i].ColScale[0],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
			_stprintf(Heading,_T("Unicode SQLBindParameter from SQL_C_TCHAR to SQL_WVARCHAR.\n"));
			TESTCASE_BEGINW(Heading);
			if (!CDataValueTOSQL9[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL9[i].CType,
																			CDataArgToSQL9.SQLType[1],wcslen(CDataValueTOSQL9[i].IntegerValue) * sizeof(SQLWCHAR),
																			0,&(CDataValueTOSQL9[i].IntegerValue),wcslen(CDataValueTOSQL9[i].IntegerValue) * sizeof(SQLWCHAR),
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(2),ParamType,CDataValueTOSQL9[i].CType,
																			CDataArgToSQL9.SQLType[1],CDataValueTOSQL9[i].ColPrec[1],
																			CDataValueTOSQL9[i].ColScale[1],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
			TESTCASE_BEGIN("");
			if (!CDataValueTOSQL9[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL9[i].CType,
																			CDataArgToSQL9.SQLType[2],wcslen(CDataValueTOSQL9[i].VarCharValue) * sizeof(SQLWCHAR),
																			0,&(CDataValueTOSQL9[i].VarCharValue),wcslen(CDataValueTOSQL9[i].VarCharValue) * sizeof(SQLWCHAR),
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(3),ParamType,CDataValueTOSQL9[i].CType,
																			CDataArgToSQL9.SQLType[2],CDataValueTOSQL9[i].ColPrec[2],
																			CDataValueTOSQL9[i].ColScale[2],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
			TESTCASE_BEGIN("");
			if (!CDataValueTOSQL9[i].NullData)
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL9[i].CType,
																			CDataArgToSQL9.SQLType[3],wcslen(CDataValueTOSQL9[i].LongVarCharValue) * sizeof(SQLWCHAR),
																			0,&(CDataValueTOSQL9[i].LongVarCharValue),wcslen(CDataValueTOSQL9[i].LongVarCharValue) * sizeof(SQLWCHAR),
																			&InValue);
			}
			else
			{
				returncode = SQLBindParameter(hstmt,(SWORD)(4),ParamType,CDataValueTOSQL9[i].CType,
																			CDataArgToSQL9.SQLType[3],CDataValueTOSQL9[i].ColPrec[3],
																			CDataValueTOSQL9[i].ColScale[3],NULL,NAME_LEN,
																			&InValueNullData);
			}
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindParameter"))
			{
				TEST_FAILED;
				LogAllErrorsVer3(henv,hdbc,hstmt);
			}
			TESTCASE_END;
			// Finished binding.....

			// Now executing the insert statement.
			if (loop_bindparam == BINDPARAM_PREPARE_EXECUTE)
			{
				_stprintf(Heading,_T("Setup for Unicode SQLBindParameter tests for Execute SQL_C_TCHAR.\n"));
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecute(hstmt);         // Execute statement with 
				if(!CHECKRC(CDataValueTOSQL9[i].PassFail,returncode,"SQLExecute"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if (loop_bindparam == BINDPARAM_EXECDIRECT)
			{
				_stprintf(Heading,_T("Setup for Unicode SQLBindParameter tests for ExecDirect SQL_C_TCHAR.\n"));
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsTab9,SQL_NTS);
				if(!CHECKRC(CDataValueTOSQL9[i].PassFail,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				TESTCASE_END;
			}
			if(returncode == SQL_SUCCESS)
			{
				_stprintf(Heading,_T("Setup for checking Unicode SQLBindParameter tests SQL_C_TCHAR.\n"));
				TESTCASE_BEGINW(Heading);
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTab9,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
				{
					TEST_FAILED;
					LogAllErrorsVer3(henv,hdbc,hstmt);
				}
				else
				{
					returncode = SQLFetch(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
					{
						TEST_FAILED;
						LogAllErrorsVer3(henv,hdbc,hstmt);
					}
					else
					{
						short numrescols = 0;
						SQLNumResultCols(hstmt,&numrescols);
						for (j = 0; j < numrescols; j++)
						{
							LogMsg(NONE,_T("Unicode SQLBindParameter test:checking data for column c%d\n"),j+1);
							returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_WCHAR,OutValue,NAME_LEN,&OutValueLen);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
							{
								TEST_FAILED;
								LogAllErrorsVer3(henv,hdbc,hstmt);
							}
							else
							{
								if (!CDataValueTOSQL9[i].NullData)
								{
									if (wcsncmp(CDataValueTOSQL9[i].OutputValue[j],(const SQLWCHAR *)OutValue,strlen((const char *)CDataValueTOSQL9[i].OutputValue[j])) == 0)
									{
										//LogMsg(NONE,_T("expect: %s and actual: %s are matched\n"),CDataValueTOSQL8[i].OutputValue[j],OutValue);
									}	
									else
									{
										TEST_FAILED;	
										LogMsg(ERRMSG,_T("expect: %s and actual: %s are not matched %d \n"),CDataValueTOSQL9[i].OutputValue[j],OutValue, __LINE__);
									}
								}
								else
								{
									if (OutValueLen == SQL_NULL_DATA)
									{
										//LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQL_NULL_DATA,OutValueLen);
									}	
									else
									{
										TEST_FAILED;	
										LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched %d \n"),SQL_NULL_DATA,OutValueLen, __LINE__);
									}
								}
							}
						} // end for loop
					}
				}
				TESTCASE_END;
			}
			SQLFreeStmt(hstmt,SQL_CLOSE);
			SQLFreeStmt(hstmt,SQL_RESET_PARAMS);
			i++;
		}
	}
	SQLExecDirect(hstmt, (SQLTCHAR*)DrpTab9,SQL_NTS);

	LogMsg(NONE, _T("START OF TEST#1 TO #8\n"));

//=================================================================================================================
//May 20, 2006: These tests need to be changed to COAST structure
	if (!TestUnicodeSetup (pTestInfo))
	{
		TestUnicodeTest1 (pTestInfo);
		TestUnicodeTest2 (pTestInfo);
		TestUnicodeTest3 (pTestInfo);
		TestUnicodeTest4 (pTestInfo);
		TestUnicodeTest5 (pTestInfo); //Fetch GetData sql_c_char
		TestUnicodeTest6 (pTestInfo); //Fetch GetData sql_c_wchar
		TestUnicodeTest7 (pTestInfo); //Fetch BindCol sql_c_char
		TestUnicodeTest8 (pTestInfo); //Fetch BindCol sql_c_wchar
	}

//================================================================
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	free(TempType1);
	free(InsStr);
	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => Unicode.\n"));
	TEST_RETURN;
}

PassFail TestUnicodeTest1 (TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TEST_INIT;
	TESTCASE_BEGIN("");
	SQLHANDLE hstmt;
	retcode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)pTestInfo->hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED((retcode = SQLPrepare(hstmt, inssql, SQL_NTS))))
	{
		LogMsg (ERRMSG, _T("Test1: SQLPrepare insert stmt failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	Strlen_or_IndPtr = SQL_NULL_DATA;

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 1,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_TCHAR,
		 0,
		 0,
		 &buffer1,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test1: SQLBindParameter #1 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	Strlen_or_IndPtr = SQL_NTS;

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 2,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_INTEGER,
		 0,
		 0,
		 &buffer2,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test1: SQLBindParameter #2 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 3,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_TVARCHAR,
		 0,
		 0,
		 &buffer3,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test1: SQLBindParameter #3 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 4,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_TLONGVARCHAR,
		 0,
		 0,
		 &buffer4,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test1: SQLBindParameter #4 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 5,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_TCHAR,
		 0,
		 0,
		 &buffer5,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test1: SQLBindParameter #5 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	Strlen_or_IndPtr = SQL_NTS;
	BufferLength = 4;

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 6,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_REAL,
		 0,
		 0,
		 &buffer6,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test1: SQLBindParameter #6 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 7,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_TCHAR,
		 0,
		 0,
		 &buffer7,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test1: SQLBindParameter #7 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 8,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_TCHAR,
		 0,
		 0,
		 &buffer8,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test1: SQLBindParameter #8 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED(retcode = SQLExecute(hstmt)))
	{
		LogMsg (ERRMSG, _T("Test1: SQLExecute failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	TESTCASE_END;
	TEST_RETURN;
}

PassFail TestUnicodeTest2 (TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TEST_INIT;
	TESTCASE_BEGIN("");
	SQLHANDLE hstmt;
	retcode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)pTestInfo->hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED((retcode = SQLPrepare(hstmt, inssql, SQL_NTS))))
	{
		LogMsg (ERRMSG, _T("Test2: SQLPrepare ins stmt failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	Strlen_or_IndPtr = SQL_NTS;

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 1,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_TCHAR,
		 0,
		 0,
		 &lbuffer1,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test2: SQLBindParameter #1 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 2,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_INTEGER,
		 0,
		 0,
		 &lbuffer2,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test2: SQLBindParameter #2 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 3,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_TVARCHAR,
		 0,
		 0,
		 &lbuffer3,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test2: SQLBindParameter #3 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 4,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_TLONGVARCHAR,
		 0,
		 0,
		 &lbuffer4,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test2: SQLBindParameter #4 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 5,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_TCHAR,
		 0,
		 0,
		 &lbuffer5,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test2: SQLBindParameter #5 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	Strlen_or_IndPtr = SQL_NTS;
	BufferLength = 4;

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 6,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_REAL,
		 0,
		 0,
		 &lbuffer6,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test2: SQLBindParameter #6 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 7,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_TCHAR,
		 0,
		 0,
		 &lbuffer7,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test2: SQLBindParameter #7 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 8,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_TCHAR,
		 0,
		 0,
		 &lbuffer8,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test2: SQLBindParameter #8 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLExecute(hstmt)))
	{
		LogMsg (ERRMSG, _T("Test2: SQLExecute failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	TESTCASE_END;
	TEST_RETURN;
}

PassFail TestUnicodeTest3 (TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TEST_INIT;
	TESTCASE_BEGIN("");
	SQLHANDLE hstmt;
	retcode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)pTestInfo->hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED((retcode = SQLPrepare(hstmt, inssql, SQL_NTS))))
	{
		LogMsg (ERRMSG, _T("Test3: SQLPrepare is stmt failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 1,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_WCHAR,
		 0,
		 0,
		 &lbuffer1,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test3: SQLBindParameter #1 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 2,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_INTEGER,
		 0,
		 0,
		 &lbuffer2,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test3: SQLBindParameter #2 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 3,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_WVARCHAR,
		 0,
		 0,
		 &lbuffer3,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test3: SQLBindParameter #3 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 4,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_WLONGVARCHAR,
		 0,
		 0,
		 &lbuffer4,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test3: SQLBindParameter #4 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 5,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_WCHAR,
		 0,
		 0,
		 &lbuffer5,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test3: SQLBindParameter #5 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 6,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_REAL,
		 0,
		 0,
		 &lbuffer6,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test3: SQLBindParameter #6 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 7,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_WCHAR,
		 0,
		 0,
		 &lbuffer7,
		 0,
		 &Strlen_or_IndPtr))))
	{ 
		LogMsg (ERRMSG, _T("Test3: SQLBindParameter #7 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 8,
		 SQL_PARAM_INPUT,
		 SQL_C_WCHAR,
		 SQL_WCHAR,
		 0,
		 0,
		 &lbuffer8,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test3: SQLBindParameter #8 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED(retcode = SQLExecute(hstmt)))
	{
		LogMsg (ERRMSG, _T("Test3: SQLExecute failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	TESTCASE_END;
	TEST_RETURN;
}

PassFail TestUnicodeTest4 (TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TEST_INIT;
	TESTCASE_BEGIN("");
	SQLHANDLE hstmt;
	retcode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)pTestInfo->hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED((retcode = SQLPrepare(hstmt, inssql, SQL_NTS))))
	{
		LogMsg (ERRMSG, _T("Test4: SQLPrepare is stmt failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	BufferLength = 4;
	Strlen_or_IndPtr = SQL_NULL_DATA;

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 1,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_WCHAR,
		 0,
		 0,
		 &buffer1,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test4: SQLBindParameter #1 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	Strlen_or_IndPtr = SQL_NTS;
	BufferLength = 4;

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 2,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_INTEGER,
		 0,
		 0,
		 &buffer2,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test4: SQLBindParameter #2 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 3,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_WVARCHAR,
		 0,
		 0,
		 &buffer3,
		 0,
		 &Strlen_or_IndPtr))))
	{ 
		LogMsg (ERRMSG, _T("Test4: SQLBindParameter #3 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 4,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_WLONGVARCHAR,
		 0,
		 0,
		 &buffer4,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test4: SQLBindParameter #4 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 5,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_WCHAR,
		 0,
		 0,
		 &buffer5,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test4: SQLBindParameter #5 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	Strlen_or_IndPtr = SQL_NTS;
	BufferLength = 4;

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 6,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_REAL,
		 0,
		 0,
		 &buffer6,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test4: SQLBindParameter #6 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 7,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_WCHAR,
		 0,
		 0,
		 &buffer7,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test4: SQLBindParameter #7 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED((retcode = SQLBindParameter(
		 hstmt,
		 8,
		 SQL_PARAM_INPUT,
		 SQL_C_TCHAR,
		 SQL_WCHAR,
		 0,
		 0,
		 &buffer8,
		 0,
		 &Strlen_or_IndPtr))))
	{
		LogMsg (ERRMSG, _T("Test4: SQLBindParameter #8 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLExecute(hstmt)))
	{
		LogMsg (ERRMSG, _T("Test4: SQLExecute failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	TESTCASE_END;
	TEST_RETURN;
}

PassFail TestUnicodeTest5 (TestInfo *pTestInfo)
{
	BOOL berr = FALSE;
	int numrows = 0;
	short numrescols = 0;
	TEST_DECLARE;
	TEST_INIT;
	TESTCASE_BEGIN("");
	SQLHANDLE hstmt;
	retcode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)pTestInfo->hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLExecDirect(hstmt,selsql,SQL_NTS)))
	{
		LogMsg (ERRMSG, _T("Test5: SQLExecDirect Select stmt failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	while(TRUE)
	{
		if ((retcode = SQLFetch(hstmt)) == SQL_ERROR)
		{
			LogMsg (ERRMSG, _T("Test5: SQLFetch failed \n"));
			LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
			TEST_FAILED;
			TEST_RETURN;
		}
		if (retcode == SQL_NO_DATA_FOUND)
		{
			break;
		}
		numrows++;
		numrescols = 0;
		SQLNumResultCols(hstmt,&numrescols);
		for (int j = 0; j < numrescols; j++)
		{
			UCHAR		OutValue[100];
			SQLLEN		OutValueLen;

			if (!SQL_SUCCEEDED(retcode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR,OutValue,100,&OutValueLen)))
			{
				LogMsg (ERRMSG, _T("Test5: SQLGetData failed for column %d\n"), j+1);
				LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
				TEST_FAILED;
				TEST_RETURN;
			}
			else
			{
				if (_tcsicmp(OutputValue[j],(const TCHAR *)OutValue) != 0)
				{
					LogMsg (ERRMSG, _T("Oops! expect: %s and actual: %s are not matched %d\n"),OutputValue[j],OutValue, __LINE__);
					berr = true;
					TEST_FAILED;
				}
				//else
					//_tprintf(_T("expect: %s and actual: %s are matched\n"),OutputValue[j],OutValue);
			}
		}
	}
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	if (berr)
		LogMsg (ERRMSG, _T("There were some errors.\n"));
	TESTCASE_END;
	TEST_RETURN;
}

PassFail TestUnicodeTest6 (TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TEST_INIT;
	TESTCASE_BEGIN("");
	bool berr = false;
	int numrows = 0;
	SQLHANDLE hstmt;
	retcode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)pTestInfo->hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLExecDirect(hstmt,selsql,SQL_NTS)))
	{
		LogMsg (ERRMSG, _T("Test6: SQLExecDirect Select stmt failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	while(true)
	{
		if ((retcode = SQLFetch(hstmt)) == SQL_ERROR)
		{
			LogMsg (ERRMSG, _T("Test6: SQLFetch failed \n"));
			LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
			TEST_FAILED;
			TEST_RETURN;
		}
		if (retcode == SQL_NO_DATA_FOUND)
		{
			break;
		}
		numrows++;
		short numrescols = 0;
		SQLNumResultCols(hstmt,&numrescols);
		for (int j = 0; j < numrescols; j++)
		{
			SQLWCHAR	lOutValue[100];
			SQLLEN		OutValueLen;

			if (!SQL_SUCCEEDED(retcode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_WCHAR,lOutValue,100,&OutValueLen)))
			{
				LogMsg (ERRMSG, _T("Test6: SQLGetData failed for column %d \n"), j+1);
				LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
				TEST_FAILED;
				TEST_RETURN;
			}
			else
			{
				if (wcsncmp((const SQLWCHAR *)&(lOutputValue[j].lbuffer),(const SQLWCHAR *)lOutValue, wcslen((const SQLWCHAR *)(lOutputValue[j].lbuffer))) != 0)
				{
					LogMsg (ERRMSG, _T("Test6: data mismatch for column %d \n"), j+1);
					TEST_FAILED;
					berr = true;
				}
			}
		}
	}
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	if (berr)
	{
		LogMsg (ERRMSG, _T("There were some errors. \n"));
	}
	TESTCASE_END;
	TEST_RETURN;
}

PassFail TestUnicodeTest7 (TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TEST_INIT;
	TESTCASE_BEGIN("");
	SQLTCHAR obuffer1[100]; 
	SQLTCHAR obuffer2[100]; 
	SQLTCHAR obuffer3[100]; 
	SQLTCHAR obuffer4[100]; 
	SQLTCHAR obuffer5[100]; 
	SQLTCHAR obuffer6[100]; 
	SQLTCHAR obuffer7[100]; 
	SQLTCHAR obuffer8[100]; 
	SQLLEN obuflen1,obuflen2,obuflen3,obuflen4,obuflen5,obuflen6,obuflen7,obuflen8; 

	SQLHANDLE hstmt;
	retcode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)pTestInfo->hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLExecDirect(hstmt,selsql,SQL_NTS)))
	{
		LogMsg (ERRMSG, _T("Test7: SQLExecDirect Select stmt failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											1, 
											SQL_C_TCHAR, 
											obuffer1, 
											sizeof(obuffer1), 
											&obuflen1)))
	{
		LogMsg (ERRMSG, _T("Test7: SQLBindCol #1 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											2, 
											SQL_C_TCHAR, 
											obuffer2, 
											sizeof(obuffer2), 
											&obuflen2)))
	{
		LogMsg (ERRMSG, _T("Test7: SQLBindCol #2 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											3, 
											SQL_C_TCHAR, 
											obuffer3, 
											sizeof(obuffer3), 
											&obuflen3)))
	{
		LogMsg (ERRMSG, _T("Test7: SQLBindCol #3 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											4, 
											SQL_C_TCHAR, 
											obuffer4, 
											sizeof(obuffer4), 
											&obuflen4)))
	{
		LogMsg (ERRMSG, _T("Test7: SQLBindCol #4 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											5, 
											SQL_C_TCHAR, 
											obuffer5, 
											sizeof(obuffer5), 
											&obuflen5)))
	{
		LogMsg (ERRMSG, _T("Test7: SQLBindCol #5 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											6, 
											SQL_C_TCHAR, 
											obuffer6, 
											sizeof(obuffer6), 
											&obuflen6)))
	{
		LogMsg (ERRMSG, _T("Test7: SQLBindCol #6 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											7, 
											SQL_C_TCHAR, 
											obuffer7, 
											sizeof(obuffer7), 
											&obuflen7)))
	{
		LogMsg (ERRMSG, _T("Test7: SQLBindCol #7 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											8, 
											SQL_C_TCHAR, 
											obuffer8, 
											sizeof(obuffer8), 
											&obuflen8)))
	{
		LogMsg (ERRMSG, _T("Test7: SQLBindCol #8 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	do 
	{ 
		retcode = SQLFetch(hstmt); 
		if (retcode == SQL_NO_DATA) 
			break; 
		if (retcode != SQL_SUCCESS)
		{
			LogMsg (ERRMSG, _T("Test7: SQLFetch failed \n"));
			LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
			TEST_FAILED;
			TEST_RETURN;
		}
		//_tprintf(_T("%s %s %s %s %s %s %s %s\r\n"), obuffer1,obuffer2,obuffer3,obuffer4,obuffer5,obuffer6,obuffer7,obuffer8); 
		//compare obuffern and buffern
		{
			int cmp = 0;
			int failed = 0;
			cmp = _tcsncmp(buffer1,(const TCHAR *)obuffer1, _tcslen(buffer1));
			if (cmp != 0) { LogMsg (ERRMSG, _T("Test7: Data mismatch for colume1\n")); failed = 1;}
			cmp = _tcsncmp(buffer2,(const TCHAR *)obuffer2, _tcslen(buffer2));
			if (cmp != 0) { LogMsg (ERRMSG, _T("Test7: Data mismatch for colume2\n")); failed = 1;}
			cmp = _tcsncmp(buffer3,(const TCHAR *)obuffer3, _tcslen(buffer3));
			if (cmp != 0) { LogMsg (ERRMSG, _T("Test7: Data mismatch for colume3\n")); failed = 1;}
			cmp = _tcsncmp(buffer4,(const TCHAR *)obuffer4, _tcslen(buffer4));
			if (cmp != 0) { LogMsg (ERRMSG, _T("Test7: Data mismatch for colume4\n")); failed = 1;}
			cmp = _tcsncmp(buffer5,(const TCHAR *)obuffer5, _tcslen(buffer5));
			if (cmp != 0) { LogMsg (ERRMSG, _T("Test7: Data mismatch for colume5\n")); failed = 1;}
			cmp = _tcsncmp(buffer6,(const TCHAR *)obuffer6, _tcslen(buffer6));
			if (cmp != 0) { LogMsg (ERRMSG, _T("Test7: Data mismatch for colume6\n")); failed = 1;}
			cmp = _tcsncmp(buffer7,(const TCHAR *)obuffer7, _tcslen(buffer7));
			if (cmp != 0) { LogMsg (ERRMSG, _T("Test7: Data mismatch for colume7\n")); failed = 1;}
			cmp = _tcsncmp(buffer8,(const TCHAR *)obuffer8, _tcslen(buffer8));
			if (cmp != 0) { LogMsg (ERRMSG, _T("Test7: Data mismatch for colume8\n")); failed = 1;}
			if (failed == 1)
			{
				TEST_FAILED;
			}
		}
	} while (1); 
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	TESTCASE_END;
	TEST_RETURN;
}

PassFail TestUnicodeTest8 (TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TEST_INIT;
	TESTCASE_BEGIN("");
	SQLWCHAR obuffer1[100]; 
	SQLWCHAR obuffer2[100]; 
	SQLWCHAR obuffer3[100]; 
	SQLWCHAR obuffer4[100]; 
	SQLWCHAR obuffer5[100]; 
	SQLWCHAR obuffer6[100]; 
	SQLWCHAR obuffer7[100]; 
	SQLWCHAR obuffer8[100]; 
	SQLLEN obuflen1,obuflen2,obuflen3,obuflen4,obuflen5,obuflen6,obuflen7,obuflen8; 

	SQLHANDLE hstmt;
	retcode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)pTestInfo->hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLExecDirect(hstmt,selsql,SQL_NTS)))
	{
		LogMsg (ERRMSG, _T("Test8: SQLExecDirect Select stmt failed v"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											1, 
											SQL_C_WCHAR, 
											obuffer1, 
											sizeof(obuffer1), 
											&obuflen1)))
	{
		LogMsg (ERRMSG, _T("Test8: SQLBindCol #1 failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											2, 
											SQL_C_WCHAR, 
											obuffer2, 
											sizeof(obuffer2), 
											&obuflen2)))
	{
		LogMsg (ERRMSG, _T("Test8: SQLBindCol #2  failed \n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											3, 
											SQL_C_WCHAR, 
											obuffer3, 
											sizeof(obuffer3), 
											&obuflen3)))
	{
		LogMsg (ERRMSG, _T("Test8: SQLBindCol #3  failed\n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											4, 
											SQL_C_WCHAR, 
											obuffer4, 
											sizeof(obuffer4), 
											&obuflen4)))
	{
		LogMsg (ERRMSG, _T("Test8: SQLBindCol #4  failed\n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											5, 
											SQL_C_WCHAR, 
											obuffer5, 
											sizeof(obuffer5), 
											&obuflen5)))
	{
		LogMsg (ERRMSG, _T("Test8: SQLBindCol #5  failed\n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											6, 
											SQL_C_WCHAR, 
											obuffer6, 
											sizeof(obuffer6), 
											&obuflen6)))
	{
		LogMsg (ERRMSG, _T("Test8: SQLBindCol #6  failed"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											7, 
											SQL_C_WCHAR, 
											obuffer7, 
											sizeof(obuffer7), 
											&obuflen7)))
	{
		LogMsg (ERRMSG, _T("Test8: SQLBindCol #7  failed\n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	if (!SQL_SUCCEEDED(retcode = SQLBindCol(hstmt, 
											8, 
											SQL_C_WCHAR, 
											obuffer8, 
											sizeof(obuffer8), 
											&obuflen8)))
	{
		LogMsg (ERRMSG, _T("Test8: SQLBindCol #8  failed\n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}

	do 
	{ 
		retcode = SQLFetch(hstmt); 
		if (retcode == SQL_NO_DATA) 
			break; 
		if (retcode != SQL_SUCCESS)
		{
			LogMsg (ERRMSG, _T("Test8: SQLFetch failed\n"));
			LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
			TEST_FAILED;
			TEST_RETURN;
		}
		//wprintf(L"%s %s %s %s %s %s %s %s\r\n", obuffer1,obuffer2,obuffer3,obuffer4,obuffer5,obuffer6,obuffer7,obuffer8); 
		{
			int cmp = 0, failed = 0;
			cmp = wcsncmp((const SQLWCHAR *)lbuffer1,obuffer1,wcslen((const SQLWCHAR *)lbuffer1));
			if(cmp != 0) {failed = 1; LogMsg (ERRMSG, _T("Test8: Data mismatch for colume1\n"));}
			cmp = wcsncmp((const SQLWCHAR *)lbuffer2,obuffer2,wcslen((const SQLWCHAR *)lbuffer2));
			if(cmp != 0) {failed = 1; LogMsg (ERRMSG, _T("Test8: Data mismatch for colume2\n"));}
			cmp = wcsncmp((const SQLWCHAR *)lbuffer3,obuffer3,wcslen((const SQLWCHAR *)lbuffer3));
			if(cmp != 0) {failed = 1; LogMsg (ERRMSG, _T("Test8: Data mismatch for colume3\n"));}
			cmp = wcsncmp((const SQLWCHAR *)lbuffer4,obuffer4,wcslen((const SQLWCHAR *)lbuffer4));
			if(cmp != 0) {failed = 1; LogMsg (ERRMSG, _T("Test8: Data mismatch for colume4\n"));}
			cmp = wcsncmp((const SQLWCHAR *)lbuffer5,obuffer5,wcslen((const SQLWCHAR *)lbuffer5));
			if(cmp != 0) {failed = 1; LogMsg (ERRMSG, _T("Test8: Data mismatch for colume5\n"));}
			cmp = wcsncmp((const SQLWCHAR *)lbuffer6,obuffer6,wcslen((const SQLWCHAR *)lbuffer6));
			if(cmp != 0) {failed = 1; LogMsg (ERRMSG, _T("Test8: Data mismatch for colume6\n"));}
			cmp = wcsncmp((const SQLWCHAR *)lbuffer7,obuffer7,wcslen((const SQLWCHAR *)lbuffer7));
			if(cmp != 0) {failed = 1; LogMsg (ERRMSG, _T("Test8: Data mismatch for colume7\n"));}
			cmp = wcsncmp((const SQLWCHAR *)lbuffer8,obuffer8,wcslen((const SQLWCHAR *)lbuffer8));
			if(cmp != 0) {failed = 1; LogMsg (ERRMSG, _T("Test8: Data mismatch for colume8\n"));}
			if (failed != 0) TEST_FAILED;
		}
	} while (1); 
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	TESTCASE_END;
	TEST_RETURN;
}

PassFail TestUnicodeSetup (TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TEST_INIT;
	TESTCASE_BEGIN("");
	SQLHANDLE hstmt;	
	retcode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)pTestInfo->hdbc, &hstmt);	
 	if(!CHECKRC(SQL_SUCCESS,retcode,"SQLAllocHandle"))
	{
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);
		FullDisconnect3(pTestInfo);
		TEST_FAILED;
		TEST_RETURN;
	}
	SQLExecDirect(hstmt, drpsql, SQL_NTS);

	if (!SQL_SUCCEEDED((retcode = SQLExecDirect(hstmt, crtsql, SQL_NTS))))
	{
		LogMsg (ERRMSG, _T("SQLExecDirect (create table) failed\n"));
		LogAllErrorsVer3(pTestInfo->henv,pTestInfo->hdbc,hstmt);	
		TEST_FAILED;
		TEST_RETURN;
	}
	SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
	TESTCASE_END;
	TEST_RETURN;
}

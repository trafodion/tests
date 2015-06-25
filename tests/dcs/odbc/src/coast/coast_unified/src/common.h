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


#ifndef __COMMONH      /* this prevents multiple copies of this... */
#define __COMMONH      /* ...include file from being #included... */

#include <sql.h>
#include <sqlext.h>
#include <math.h>
#include <locale.h> 
#include "basedef.h"

#ifdef unixcli
	#include "hpsqlext.h"
	#include "utchar.h"
	// FILE relative usage replacement
	#ifdef UNICODE
	#define TFILE		UFILE
	#define _tfclose	u_fclose
	
	#ifndef _TCS_MEMSET_DEFINED
	#define _tmemset       u_memset
	#define _TCS_MEMSET_DEFINED
	#endif // end def _TCS_MEMSET_DEFINED

	#else // ndef UNICODE
	#define TFILE		FILE
	#define _tfclose	fclose
	
	#ifndef _TCS_MEMSET_DEFINED
	#define _tmemset       memset
	#define _TCS_MEMSET_DEFINED
	#endif // end def _TCS_MEMSET_DEFINED

	#endif
#else
	#include <tchar.h>
	#define TFILE		FILE
	#define _tfclose	fclose
	
	#ifndef _TCS_MEMSET_DEFINED
	#define _tmemset       memset
	#define _TCS_MEMSET_DEFINED
	#endif // end def _TCS_MEMSET_DEFINED

	// Session Name connection attribute
	#define SQL_ATTR_SESSIONNAME            5000
	/* Max Session Name length including terminating null */
	#define SQL_MAX_SESSIONNAME_LEN 25
	// Attribute to get the 64bit rowcount when using the 32-bit ODBC driver
	#define SQL_ATTR_ROWCOUNT64_PTR         5001
	// Attribute to set fetchahead connection attribute
	#define SQL_ATTR_FETCHAHEAD             5003	
#endif

#ifdef UNICODE
#define SQL_TCHAR				SQL_WCHAR
#define SQL_TVARCHAR			SQL_WVARCHAR
#define SQL_TLONGVARCHAR		SQL_WLONGVARCHAR
#else
#define SQL_TCHAR				SQL_CHAR
#define SQL_TVARCHAR			SQL_VARCHAR
#define SQL_TLONGVARCHAR		SQL_LONGVARCHAR
#endif 

/**************************************
** Constants, Structures, and Typedefs 
**************************************/
#define MAX_TESTS_PER_FUNCTION	100
#define MAX_CONNECT_STRING      1024
#define STATE_SIZE				6
#define MAX_STRING_SIZE			500
#define MAX_NOS_SIZE			4050
#define MAX_HEADING_SIZE		4000
#define MAXLEN					100
#define MAX_COLUMNS				100
#define MAX_ROW_LEN				1000
#define MAX_COLUMN_NAME			128
#define MAX_DB_NAME_LEN			60
#define	NUM_ENV_HND				10
#define	NUM_CONN_HND			10
#define	MAX_TABLE_NAME			128
#define MAX_SCHEMA_NAME			128
#define MAX_CATALOG_NAME		128
#define MAX_USER_NAME			128+1

#define	DROP_TABLE				0
#define	CREATE_TABLE			1
#define	INSERT_TABLE			2
#define	SELECT_TABLE			3
#define	UPDATE_TABLE			4
#define	DELETE_TABLE			5
#define	INSERT_TABLE_WITH_PARAM	6

#define BINDPARAM_PREPARE_EXECUTE			0
#define BINDPARAM_EXECDIRECT				1
#define BINDPARAM_FOR_PREPEXEC_EXECDIRECT	2

#define TEST_GLOBALS  short _gTestCount=0,_gTestFailedCount=0,_gTestPassedCount=0,_gTestIndvCount=0,_gTestFailedIndvCount=0
#define TEST_GLOBALS_RESET  _gTestCount=0,_gTestFailedCount=0,_gTestPassedCount=0
#define TEST_GLOBALS_EXTERN extern short _gTestCount,_gTestFailedCount,_gTestPassedCount
#define TEST_DECLARE  PassFail _TestSuiteResult;  PassFail _TestCase
#define TEST_INIT  {_TestSuiteResult=PASSED;}
#define TESTCASE_BEGIN(x) {if (x) LogSetMark(); _TestCase=PASSED; _gTestCount++; if (x) LogMsg(SHORTTIMESTAMP+LINEBEFORE,_T(x));} 
#define TESTCASE_BEGINW(x) {if (x) LogSetMark(); _TestCase=PASSED; _gTestCount++; if (x) LogMsg(SHORTTIMESTAMP+LINEBEFORE,x);} 
#define TEST_FAILED  {_TestSuiteResult=FAILED;  _TestCase=FAILED; _gTestFailedCount++;}
#define TESTCASE_END  {if ((_TestCase==PASSED)&&(!g_Trace)){LogSetEofAtMark(); _gTestPassedCount++;}}
#define TEST_RETURN  return(_TestSuiteResult)

#define TESTCASE_LOG(x) {LogSetMark(); LogMsg(SHORTTIMESTAMP+LINEBEFORE,x);} 

#define MX_SPECIFIC	0
#define MP_SPECIFIC 1

#define MX_DT_ALL				0
#define MP_DT_ALL				1
#define MX_DT_EXCEPT_DATETIME	2
#define MP_DT_EXCEPT_DATETIME	3
#define MX_DT_DATE				4
#define MP_DT_DATE				5
#define MX_DT_TIME				6
#define MP_DT_TIME				7
#define MX_DT_TIMESTAMP			8
#define MP_DT_TIMESTAMP			9
// The below value comes from the SERVER string:
// TCP:xxx.xxx.xxx.xxx/nnnnn
// 1234567890123456789012345
//          1         2
// Where xxx is the TCP/IP address and nnnnn is the port number.
#define MAX_SERVER_NAME_LENGTH		128

#define MX_2_VERSION 210
#define MX_3_VERSION 351

#define CONNECT_AUTOCOMMIT_OFF		0x01	// Default is on.
#define CONNECT_ODBC_VERSION_2		0x02
#define CONNECT_ODBC_VERSION_3		0x04

/** *Constraints for locale and character set settings **/
#define CS_ASCII	1
#define CS_GBK		2
#define CS_SJIS		3

#define LC_EN		"en_US"
#define LC_CN		"zh_CN"
#define LC_JP		"ja_JP"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct var_list_tt {
	int last;
	TCHAR *var_name;
	TCHAR *value;
} var_list_t;

struct TestInfo {
   TCHAR DataSource[SQL_MAX_DSN_LENGTH*2];
   TCHAR Server[MAX_SERVER_NAME_LENGTH*2];
   TCHAR Port[10*2];
   TCHAR UserID[MAX_USER_NAME*2];
   TCHAR Password[MAX_USER_NAME*2];
   /*
   char DataSource[SQL_MAX_DSN_LENGTH*2];
   char Server[MAX_SERVER_NAME_LENGTH*2];
   char Port[10*2];
   char UserID[MAX_USER_NAME*2];
   char Password[MAX_USER_NAME*2];
	*/
   TCHAR Database[MAX_DB_NAME_LEN*2]; 
   TCHAR Catalog[MAX_CATALOG_NAME*2];
   TCHAR Schema[MAX_SCHEMA_NAME*2];

   SQLHANDLE henv;
   SQLHANDLE hdbc;
   SQLHANDLE hstmt;
   short Trace;              
   TCHAR Matrix[MAX_TESTS_PER_FUNCTION];
   };

struct ColumnInfo	{
	SQLTCHAR	Name[MAX_COLUMN_NAME];
	SWORD	SqlType;
	SQLULEN	Prec; 
	SWORD	Scale;
	SWORD	Nullable;
	SQLULEN	DisplaySize;
	};

struct ConnectInfo	{
	unsigned int	Duration;
	unsigned int	EnvHndl;
	unsigned int	ConnHndl;
	unsigned int	StmtHndl;
	int						Operas;
	};

struct PerformInfo {
	BOOL	measure_connection;
	BOOL	measure_query;		
	};

#if defined(UNICODE) && defined(unixcli)
struct SICUConverter {
	UConverter *converter;
	UConverter *utf8;
	UErrorCode err;
	
	char locale[20];
	char *codepage;
	unsigned int charset;
};

typedef struct SICUConverter ICUConverter;
extern ICUConverter* icu_conv;
#endif

typedef struct TestInfo TestInfo;
typedef struct ColumnInfo ColumnInfo;
typedef struct ConnectInfo ConnectInfo;
typedef struct PerformInfo PerformInfo;

/*************************
** External declarations 
*************************/
extern BOOL g_Trace;
extern BOOL g_MPSyntax;

TEST_GLOBALS_EXTERN;

/* new stuff */
extern CRITICAL_SECTION error_process_mutex;
/* a counter to make sure no thread tries to enter the
	 critical section twice at a time (the system will let
	 it do this with no error and no blocking) */
extern int critical_count;
/* end new stuff */

extern TCHAR charset_file[256];
extern int	myLogID;

extern char *inputLocale;

extern BOOL isCharSet;
extern BOOL isUCS2;

extern TCHAR	column_string[1000];
extern TCHAR	ColumnDefinition[100];

extern void blank_pad( TCHAR *s,int  len);
extern VOID FormatHexOutput( TCHAR *In, TCHAR *Out, int Length );
extern VOID BufferToHex( TCHAR *In, TCHAR *Out, int Length );

/* NOTE: Always use CHECKRC and never call CheckReturnCode directly */
#define CHECKRC(expected,actual,FunctionName) (CheckReturnCode((expected),(actual),(_T(FunctionName)),_T(__FILE__),(short)__LINE__))

extern TrueFalse CheckReturnCode(
   RETCODE expected,
   RETCODE actual,
   TCHAR *comment,
   TCHAR *SourceFile,
   short LineNum);
   
// Functions for converting ODBC values into more meaningful character strings
extern TCHAR *ReturncodeToChar(RETCODE returncode,TCHAR *buffer);
extern TCHAR *SQLTypeToChar(SWORD SQLType,TCHAR *buffer);
extern TCHAR *SQLNullToChar(SWORD NullState,TCHAR *buffer);
extern TCHAR *CatalogLocationToString(SWORD CatLoc, TCHAR *buf);
extern TCHAR *SQLDescToChar(SWORD Desc,TCHAR *buffer);
extern TCHAR *SQLDescAttrToChar(SWORD Desc,TCHAR *buffer);
extern TCHAR *StatementOptionToChar( long Option, TCHAR *buf );
extern TCHAR *StatementParamToChar( long Option, long Param, TCHAR *buf );
extern TCHAR *ConnectionOptionToChar( long Option, TCHAR *buf );
extern TCHAR *ConnectionParamToChar( long Option, long Param, TCHAR *buf );
extern SQLTCHAR *StmtQueries(long QueryType, TCHAR *name, TCHAR *buf );
extern TCHAR *CreateTableForConversion(int SQLDataType, TCHAR *TableName, TCHAR *cprec, TCHAR *vcprec, TCHAR *lvcprc,TCHAR *decprec, TCHAR *numprec, TCHAR *buf );
extern TCHAR *SQLCTypeToChar(SWORD CType, TCHAR *buf);
extern TCHAR *InfoTypeToChar( long InfoType, TCHAR *buf );
extern TCHAR *CatalogUsageToString(long CatUsage, TCHAR *buf);
extern TCHAR *ConcatNullToString(SWORD ConcatNull, TCHAR *buf);
extern TCHAR *ConvertValueToString(long ConvertValue, TCHAR *buf);
extern TCHAR *CA1ToString(long CAValue, TCHAR *buf);
extern TCHAR *CA2ToString(long CAValue, TCHAR *buf);
extern TCHAR *CvtFunctionToString(long CvtFunction, TCHAR *buf);
extern TCHAR *CorrelationToString(SWORD Correl, TCHAR *buf);
extern TCHAR *CursorBehaviorToString(SWORD CursorB, TCHAR *buf);
extern TCHAR *TxnIsolationToString(SDWORD TxnIsolation, TCHAR *buf);
extern TCHAR *FileUsageToString(SDWORD FileUsage, TCHAR *buf);
extern TCHAR *AggregateToString(long AggregateOption, TCHAR *buf);
extern TCHAR *AlterTableToString(long AlterOption, TCHAR *buf);
extern TCHAR *NumFunctionToString(long NumFunction, TCHAR *buf);
extern TCHAR *StrFunctionToString(long StrFunction, TCHAR *buf);
extern TCHAR *TimeIntToString(long TimeInt, TCHAR *buf);
extern TCHAR *TimeFunctionToString(long TimeFunction, TCHAR *buf);
extern TCHAR *OJToString(long OJ, TCHAR *buf);
extern TCHAR *GDExtToString(long GDExt, TCHAR *buf);
extern TCHAR *GroupByToString(SWORD GroupBy, TCHAR *buf);
extern TCHAR *CaseToString(SWORD CaseValue, TCHAR *buf);
extern TCHAR *SchemaUsageToString(long SchemaUsage, TCHAR *buf);
extern int cwcscmp(TCHAR* str1, TCHAR* str2, BOOL ignoreCase);
extern int cstrncmp(TCHAR* expect, TCHAR* actual, BOOL ignoreCase, int size);
extern TCHAR* printSymbol(TCHAR* in, TCHAR* output);
extern TCHAR* removeQuotes(TCHAR* in, TCHAR* output);
extern BOOL specialMode(SQLHANDLE hstmt, TCHAR* cqd, TCHAR* mode);
extern void get_time_std(TCHAR* tmpbuf);
extern void get_time_special(TCHAR* tmpbuf);
extern int mbs_truncate(TCHAR* in_mbsstr, TCHAR* out_mbsstr, int len, int type);

extern SWORD	CharToSQLType(TCHAR *buffer);
extern SWORD	CharToSQLCType(TCHAR *buffer);

extern TCHAR *PerformanceQueries(long QueryType, TCHAR *name, TCHAR *buf );

extern void ErrorMessageBox (
	TestInfo* ti,
	RETCODE   retcode,
	TCHAR*	  Label);

extern TrueFalse FindError(
   TCHAR *FindMsg,
   SQLHANDLE henv,
   SQLHANDLE hdbc,
   SQLHANDLE hstmt);
   
extern void LogAllErrors(
   SQLHANDLE henv,
   SQLHANDLE hdbc,
   SQLHANDLE hstmt);
   
extern void LogAllErrorsVer3(
   SQLHANDLE henv,
   SQLHANDLE hdbc,
   SQLHANDLE hstmt);

extern void DisplaySqlErr(
	SQLHANDLE hdl,
	SQLSMALLINT HdlType);

extern void LogResults(void);
extern void LogResultsTest(TCHAR *);

extern TrueFalse FullConnectPromptUserVer(
   TestInfo *pTestInfo,
   int		iODBCVer);

extern TrueFalse FullConnectPromptUser(
   TestInfo	*pTestInfo);
   
extern TrueFalse FullConnectPromptUser3(
   TestInfo	*pTestInfo);

extern TrueFalse FullConnect(
   TestInfo *pTestInfo);

extern TrueFalse FullConnectWithOptions(
   TestInfo *pTestInfo,
   int Options);

extern TrueFalse DriverConnectNoPrompt(TestInfo *pTestInfo);

extern TrueFalse FullDisconnectVer(
   TestInfo *pTestInfo,
   int		iODBCVer);

extern TrueFalse FullDisconnect(
   TestInfo *pTestInfo); 

extern TrueFalse FullDisconnect3(
   TestInfo *pTestInfo); 

extern TrueFalse GetDataAll( 
	TestInfo*	ti,
	void*		buffer,
	SQLULEN		cbBuf,
	SQLULEN*		cbAvail,
	RETCODE*	pRetCode,
	SQLULEN		cbMaxCol);

extern TrueFalse LogDataAll(
	TestInfo*	ti,
	HLOGT		hlog);

extern TrueFalse LogDataAll(
	TestInfo*	ti,
	HLOGT		hlog);

extern TCHAR *ReturnColumnDefinition(TCHAR *CrtCol, short ColNum);
extern void LogInfo(TestInfo *pTestInfo);

/*For Character Set*/
//extern int next_line(TCHAR *lineOut, FILE *scriptFD);
extern var_list_t* load_api_vars(TCHAR *api, TCHAR *textFile);
extern void print_list (var_list_t *var_list);
extern void free_list (var_list_t *var_list);
extern TCHAR* var_mapping(TCHAR *var_name, var_list_t *var_list);
#ifdef __cplusplus
}
#endif

#endif

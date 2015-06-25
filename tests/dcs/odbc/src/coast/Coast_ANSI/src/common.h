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
#include "basedef.h"

#ifdef unixcli
	#include <hpsqlext.h>
#else
    // Session Name connection attribute
    #define SQL_ATTR_SESSIONNAME		5000
    // Session Name length
    #define SQL_MAX_SESSIONNAME_LEN		25

    // Attribute to get the 64bit rowcount when using the 32-bit ODBC driver
    #define SQL_ATTR_ROWCOUNT64_PTR		5001

    // Attribute to set fetchahead connection attribute
    #define SQL_ATTR_FETCHAHEAD			5003

    // Application Name connection attribute
    #define SQL_ATTR_ROLENAME			5002
    // Application Name length
    #define SQL_MAX_ROLENAME_LEN		128
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
#define ZERO_LEN                0
#define BUFF300                 300
#define BUFF600                 600

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
#define TESTCASE_BEGIN(x) {if (x) LogSetMark(); _TestCase=PASSED; _gTestCount++; if (x) LogMsg(SHORTTIMESTAMP+LINEBEFORE,x);} 
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

typedef struct var_list_tt {
	int last;
	char *var_name;
	char *value;
} var_list_t;

struct TestInfo {
   char DataSource[SQL_MAX_DSN_LENGTH];
   char Server[MAX_SERVER_NAME_LENGTH];
   char Port[10];
   char UserID[MAX_USER_NAME];
   char Password[MAX_USER_NAME];
   char Database[MAX_DB_NAME_LEN]; 
   char Catalog[MAX_CATALOG_NAME];
   char Schema[MAX_SCHEMA_NAME];

   BOOL bLongOn;  //Modified for Longvarchar changes
   SQLHANDLE henv;
   SQLHANDLE hdbc;
   SQLHANDLE hstmt;
   short Trace;              
   char Matrix[MAX_TESTS_PER_FUNCTION];
   };

struct ColumnInfo	{
	SQLCHAR	Name[MAX_COLUMN_NAME];
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

#ifdef __cplusplus
extern "C" {
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

extern char charset_file[256];
extern int	myLogID;

extern BOOL isCharSet;
extern BOOL isUCS2;
extern char *secondaryRole;

//extern char secondaryRole[SQL_MAX_ROLENAME_LEN];

extern char	column_string[1000];
extern char	ColumnDefinition[100];

extern void blank_pad( char *s,int  len);
extern VOID FormatHexOutput( char *In, char *Out, int Length );
extern VOID BufferToHex( char *In, char *Out, int Length );

/* NOTE: Always use CHECKRC and never call CheckReturnCode directly */
#define CHECKRC(expected,actual,FunctionName) (CheckReturnCode((expected),(actual),(FunctionName),(char*)__FILE__,(short)__LINE__))

extern TrueFalse CheckReturnCode(
   RETCODE expected,
   RETCODE actual,
   char *comment,
   char *SourceFile,
   short LineNum);
   
// Functions for converting ODBC values into more meaningful character strings
extern char *ReturncodeToChar(RETCODE returncode,char *buffer);
extern char *SQLTypeToChar(SWORD SQLType,char *buffer);
extern char *SQLNullToChar(SWORD NullState,char *buffer);
extern char *CatalogLocationToString(SWORD CatLoc, char *buf);
extern char *SQLDescToChar(SWORD Desc,char *buffer);
extern char *SQLDescAttrToChar(SWORD Desc,char *buffer);
extern char *StatementOptionToChar( long Option, char *buf );
extern char *StatementParamToChar( long Option, long Param, char *buf );
extern char *ConnectionOptionToChar( long Option, char *buf );
extern char *ConnectionParamToChar( long Option, long Param, char *buf );
extern SQLCHAR *StmtQueries(long QueryType, char *name, char *buf );
extern char *CreateTableForConversion(int SQLDataType, char *TableName, char *cprec, char *vcprec, char *lvcprc,char *decprec, char *numprec, char *buf );
extern char *SQLCTypeToChar(SWORD CType, char *buf);
extern char *InfoTypeToChar( long InfoType, char *buf );
extern char *CatalogUsageToString(long CatUsage, char *buf);
extern char *ConcatNullToString(SWORD ConcatNull, char *buf);
extern char *ConvertValueToString(long ConvertValue, char *buf);
extern char *CA1ToString(long CAValue, char *buf);
extern char *CA2ToString(long CAValue, char *buf);
extern char *CvtFunctionToString(long CvtFunction, char *buf);
extern char *CorrelationToString(SWORD Correl, char *buf);
extern char *CursorBehaviorToString(SWORD CursorB, char *buf);
extern char *TxnIsolationToString(SDWORD TxnIsolation, char *buf);
extern char *FileUsageToString(SDWORD FileUsage, char *buf);
extern char *AggregateToString(long AggregateOption, char *buf);
extern char *AlterTableToString(long AlterOption, char *buf);
extern char *NumFunctionToString(long NumFunction, char *buf);
extern char *StrFunctionToString(long StrFunction, char *buf);
extern char *TimeIntToString(long TimeInt, char *buf);
extern char *TimeFunctionToString(long TimeFunction, char *buf);
extern char *OJToString(long OJ, char *buf);
extern char *GDExtToString(long GDExt, char *buf);
extern char *GroupByToString(SWORD GroupBy, char *buf);
extern char *CaseToString(SWORD CaseValue, char *buf);
extern char *SchemaUsageToString(long SchemaUsage, char *buf);
extern int cstrcmp(char* str1, char* str2, BOOL ignoreCase, BOOL isCS);
extern int cstrncmp(char* expect, char* actual, BOOL ignoreCase, BOOL isCS, int size);
extern char* printSymbol(char* in, char* output);
extern char* removeQuotes(char* in, char* output);
//extern BOOL specialMode(SQLHANDLE hstmt, char* cqd, char* mode);
extern void get_time_std(char* tmpbuf);
extern void get_time_special(char* tmpbuf);

extern SWORD	CharToSQLType(char *buffer);
extern SWORD	CharToSQLCType(char *buffer);

extern char *PerformanceQueries(long QueryType, char *name, char *buf );

extern void ErrorMessageBox (
	TestInfo* ti,
	RETCODE   retcode,
	char*	  Label);

extern TrueFalse FindError(
   char *FindMsg,
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

extern void LogResults(void);
extern void LogResultsTest(char *);

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

extern char *ReturnColumnDefinition(char *CrtCol, short ColNum);
extern void LogInfo(TestInfo *pTestInfo);

/*For Character Set*/
//extern int next_line(char *lineOut, FILE *scriptFD);
extern var_list_t* load_api_vars(char *api, char *textFile);
extern void print_list (var_list_t *var_list);
extern void free_list (var_list_t *var_list);
extern char* var_mapping(char *var_name, var_list_t *var_list);

extern char *replace_str(char *str, char *orig, char *rep);

#ifdef __cplusplus
}
#endif

#endif

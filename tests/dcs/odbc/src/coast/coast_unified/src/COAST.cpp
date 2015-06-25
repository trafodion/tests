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


// COAST.cpp : Defines the entry point for the console application.
//
#include <stdlib.h>    
#include <stdio.h> 
#include <string.h>
#include <windows.h>
#include <sqlext.h>
#include <assert.h>
#include <time.h>
#include "common.h"
#include "log.h"
#include "apitests.h"
#include "getoptw.h"

#define RUNALL	1
#define RUNFILE	2
#define RUNAPI	3
#define	ARGS	_T("d:u:p:l:c:f:m:r:")

TestInfo		*pTestInfo;
TCHAR *DSN;//[100];
TCHAR *USR;//[100];
TCHAR *PWD;//[100];
TCHAR *charset;
TCHAR *strapi;//[100];
TCHAR *strOption;//[100];
TCHAR *inputfile;//[100];
TFILE *scriptFD = NULL;
TCHAR *machine = _T("local");

TCHAR *charset_filenames[] = {_T("charset_auto_generated_ascii.char"),
							 _T("charset_auto_generated_sjis.char"),
							 _T("charset_auto_generated_big5.char"),
							 _T("charset_auto_generated_gb2.char"),
							 _T("charset_auto_generated_gb1.char"),
							 _T("charset_auto_generated_ksc.char"),
							 _T("charset_auto_generated_eucjp.char"),
							 _T("charset_auto_generated_latin1.char"),
				 _T("charset_auto_generated_gbk.char")
						 };

TCHAR fileout_dir[1024];

#if defined(unixcli)&& defined(UNICODE)
ICUConverter *icu_conv;
#endif

int m_Charset;
bool m_AllApi				= FALSE;

// ODBC 2.x APIs
bool m_AllocEnv				= FALSE;
bool m_AllocConnect			= FALSE;
bool m_BindParameter		= FALSE;
bool m_BrowseConnect		= FALSE;
bool m_Cancel				= FALSE;
bool m_ColAttrib			= FALSE;
bool m_Connect				= FALSE;
bool m_DataSources			= FALSE;
bool m_DesCols 				= FALSE;
bool m_DriverConnect		= FALSE;
bool m_Drivers				= FALSE;
bool m_Error				= FALSE;
bool m_ExecDirect			= FALSE;
bool m_Execute				= FALSE;
bool m_ExtendedFetch		= FALSE;
bool m_Fetch 				= FALSE;
bool m_GetData				= FALSE;
bool m_PutData				= FALSE;
bool m_GetFunctions			= FALSE;
bool m_GetInfo				= FALSE;
bool m_MoreResults			= FALSE;
bool m_AllocStmt			= FALSE;
bool m_BindCol				= FALSE;
bool m_Columns				= FALSE;
bool m_DescribeParam		= FALSE;
bool m_GetTypeInfo			= FALSE;
bool m_PrimaryKeys			= FALSE;
bool m_ResGovern			= FALSE;
bool m_SetConnectOption		= FALSE;
bool m_SetCursorName		= FALSE;
bool m_SetStmtOption		= FALSE;
bool m_SpecialColumns		= FALSE;
bool m_Statistics			= FALSE;
bool m_Tables				= FALSE;
bool m_NativeSql			= FALSE;
bool m_NumParams			= FALSE;
bool m_NumResultCols		= FALSE;
bool m_Prepare				= FALSE;
bool m_RowCount				= FALSE;
bool m_Transact				= FALSE;

//ODBC 3.0 APIs

bool m_AllocHandle30			= FALSE;
bool m_BindCol30				= FALSE;
bool m_BindParameter30			= FALSE;
bool m_CloseCursor30			= FALSE;
bool m_ColAttributes30			= FALSE;
bool m_CopyDesc30				= FALSE;
bool m_DescribeCol30			= FALSE;
bool m_EndTran30				= FALSE;
bool m_GetConnectAttr30			= FALSE;
bool m_GetData30				= FALSE;
bool m_SetGetDescFields30		= FALSE;
bool m_GetDescRec30				= FALSE;
bool m_GetDiagField30			= FALSE;
bool m_GetDiagRec30				= FALSE;
bool m_GetEnvAttr30				= FALSE;
bool m_GetInfo30				= FALSE;
bool m_GetStmtAttr30			= FALSE;
bool m_MoreResults30			= FALSE;
//bool m_PartialDateTimeInput	= FALSE;
//bool m_PartialDateTimeOutput	= FALSE;
bool m_BindParamInterval30		= FALSE;
bool m_GetTypeInfo30R18			= FALSE;
bool m_ProcedureColumns30		= FALSE;
bool m_Procedures30				= FALSE;
bool m_FetchScroll30			= FALSE;
bool m_ForeignKeys30			= FALSE;
bool m_BindColInterval30		= FALSE;
bool m_GetDataInterval30		= FALSE;
bool m_ColumnPrivileges30		= FALSE;
bool m_TablePrivileges30		= FALSE;
bool m_Unicode30				= FALSE;

// Features
bool m_QueryID					= FALSE;
bool m_Hash2					= FALSE;
bool m_LargeBlock				= FALSE;
bool m_InfoStats                = FALSE;

int iRunOption = 0;

int Run20Tests ();
int Run21Tests ();
int	Run30Tests ();
void MapApiNameToFlag(TCHAR *);
void ReadSelectedTests(TCHAR *);

#ifdef unixcli
int _tmain(int argc, char* argv[]) // 
#else
int _tmain(int argc, TCHAR* argv[])
#endif
{
	//process command line params
	int c, errflag = 0;
	inputLocale = (char*)malloc(20 * sizeof(char));
	TCHAR temp[2048];

#if defined(unixcli)&&defined(UNICODE)
	icu_conv = (ICUConverter*)malloc(sizeof(ICUConverter));
	char* plang;
	char* plocale = getenv("LANG");
	if(plocale)
	{
		char* temp = strtok(plocale, ".");
		if(temp == NULL)
		{
			printf("LANG is invalid.");
			exit(1);
		}

		plang = strtok(NULL, ".");
		if(!plang)
		{
			printf("LANG is invalid.");
			exit(1);
		}
	}

	UErrorCode errvalue = U_ZERO_ERROR;
	UConverter *m_conv = ucnv_open(plang, &errvalue);

	icu_conv->converter = m_conv;
#endif

	int *arg_length=(int*)malloc(sizeof(int)*argc);

	TCHAR** tcs_argv=(TCHAR**)malloc(sizeof(TCHAR*)*argc);
	for(int i=0;i<argc;i++)
	{
#ifdef unixcli
		arg_length[i]=strlen(argv[i])+1;
#else
		arg_length[i]=_tcslen(argv[i])+1;
#endif
		tcs_argv[i]=(TCHAR*)malloc(sizeof(TCHAR)*arg_length[i]);
	}
	
	tcs_optarg = NULL;

	if (argc < 2 || argc > 14)
		errflag++;

#if defined(unixcli)&&defined(UNICODE)
	for(int i=0;i<argc;i++)
	{
		/* For unix,standard libraries process all wchar_t 
		 * as 4 bytes character. The code here convert the 
		 * input arguments to wide strings * to pass to getopt_c
		 * function, and before that all strings are converted to 
		 * 2 bytes to comply with short-wchar macro switch.
		 * */
		mbstowcs(tcs_argv[i],argv[i],arg_length[i]);
		//mbstowcs((wchar_t*)temp,argv[i],arg_length[i]);
		//for(int j=0;j<4*arg_length[i];j+=2)
		//	tcs_argv[i][j/2]=temp[j];
	}
#else
	for(int i=0;i<argc;i++)
		_tcscpy(tcs_argv[i],argv[i]);
#endif

	// Parse input options and arguments
	while (!errflag && (c = getopt_c(argc, tcs_argv, ARGS)) != -1)
		switch (c) {
			case 'd':
				DSN = tcs_optarg;	
				break;
			case 'u':
				USR = tcs_optarg;
				break;
			case 'p':
				PWD = tcs_optarg;
				break;
			case 'f':
				strOption = tcs_optarg;
				if (!_tcsicmp(strOption,_T("FILE")))
				{
					iRunOption = RUNFILE;
					inputfile = secondarg;
                    strapi = (TCHAR*)_T("FILE");
				}
				else if (!_tcsicmp(strOption,_T("API")))
				{
					iRunOption = RUNAPI;
					strapi = secondarg;
				}
				else if (!_tcsicmp(strOption,_T("ALL")))
				{
					strapi = strOption;
					iRunOption = RUNALL;
				}
				break;
			case 'c':
				charset = tcs_optarg;	

#if defined(unixcli)&&defined(UNICODE)
				strcpy(inputLocale, argv[optind-1]);
				icu_conv->codepage = (char*)malloc(20 * sizeof(char));
				icu_conv->codepage = NULL;
#endif
				if (!_tcsicmp(charset,_T("ASCII"))) {
					_tcscpy(charset_file,charset_filenames[0]);
#if defined(unixcli)&&defined(UNICODE)
					strcpy(icu_conv->locale, LC_EN);
#endif
				} else {
					isCharSet = TRUE;
					if (!_tcsicmp(charset,_T("SJIS"))) {
						_tcscpy(charset_file,charset_filenames[1]);
#if defined(unixcli)&&defined(UNICODE)
						strcpy(icu_conv->locale, LC_JP);
						icu_conv->codepage = "SJIS";
#endif
					}
					else if (!_tcsicmp(charset,_T("BIG5"))) {
						_tcscpy(charset_file,charset_filenames[2]);
					}
					else if (!_tcsicmp(charset,_T("GB2"))) {
						_tcscpy(charset_file,charset_filenames[3]);
#if defined(unixcli)&&defined(UNICODE)
						strcpy(icu_conv->locale, LC_CN);
#endif
					}
					else if (!_tcsicmp(charset,_T("GB1"))) {
						_tcscpy(charset_file,charset_filenames[4]);
#if defined(unixcli)&&defined(UNICODE)
						strcpy(icu_conv->locale, LC_CN);
#endif
					}
					else if (!_tcsicmp(charset,_T("KSC"))) {
						_tcscpy(charset_file,charset_filenames[5]);
					}
					else if (!_tcsicmp(charset,_T("EUCJP"))) {
						_tcscpy(charset_file,charset_filenames[6]);
#if defined(unixcli)&&defined(UNICODE)
						strcpy(icu_conv->locale, LC_JP);
#endif
					}
					else if (!_tcsicmp(charset,_T("LATIN1"))) {
						_tcscpy(charset_file,charset_filenames[7]);
					}

					else if (!_tcsicmp(charset,_T("GBK"))) {
						_tcscpy(charset_file,charset_filenames[8]);
#if defined(unixcli)&&defined(UNICODE)
						strcpy(icu_conv->locale, LC_CN);
//#ifdef HPUXCLI
						icu_conv->codepage = "gb18030";
//#endif
#endif
					}
					else 
						errflag++;
				}
				break;
			case 'm':
				machine = tcs_optarg;
				break;
			default :
				errflag++;
		}
	if (errflag) {
		_tprintf(_T("Usage: %s [-d <datasource>] [-u <userid>] [-p <password>] [-c <ASCII|SJIS|BIG5|GB1|GB2|KSC|EJCJP|LATIN1>] [-f <ALL|API api_name|FILE file_name>]\nOr:   %s [-d <datasource>]\n   where default userID is 'odbcqa' and default password is 'odbcqa' with default character set is 'ASCII'\n"), tcs_argv[0], tcs_argv[0] );
		return FALSE;
	}

	if(!USR)
		USR = (TCHAR*)_T("odbcqa");
	if(!PWD)
		PWD = (TCHAR*)_T("odbcqa");
	if(!charset) {
		charset = (TCHAR*)_T("ASCII");
		_tcscpy(charset_file,charset_filenames[0]);
	}
	if(!strOption) {
		iRunOption = RUNALL;
		strapi = (TCHAR*)_T("ALL");
	}

#ifndef unixcli
	if ((scriptFD = _tfopen(charset_file, _T("r"))) == NULL) {
		_tcscpy(temp, _T("..\\..\\..\\src\\"));
		_tcscat(temp, charset_file);
		_tcscpy(charset_file, temp);

		if ((scriptFD = _tfopen(charset_file, _T("r"))) == NULL) {
			_tprintf(_T("Error open textfile %s\n"), charset_file);
			return FALSE;
		}
	}
	_tfclose(scriptFD);
	_tprintf(_T("Loading data from: %s\n"), charset_file);
#endif

#ifndef unixcli
	_tsetlocale(LC_ALL, _T(""));
//#else
//	setlocale(LC_ALL, inputLocale);
#endif
	
	_stprintf(fileout_dir, _T("."));
	pTestInfo	= new TestInfo;

	_tcscpy (pTestInfo->DataSource,(const TCHAR *)DSN);
	_tcscpy (pTestInfo->UserID,(const TCHAR *)USR);
	_tcscpy (pTestInfo->Password,(const TCHAR *)PWD);
	//ADDING FOR TRAFODION
	_tcscpy (pTestInfo->Catalog,(const TCHAR *)"TRAFODION");

	switch (iRunOption)
	{
	case RUNALL:
		m_AllApi = true;
		break;
	case RUNAPI:
		MapApiNameToFlag((TCHAR *)strapi);
		break;
	case RUNFILE:
		ReadSelectedTests((TCHAR *)inputfile);
		break;
	}

	// initialization added (RS) to prevent some runtime errors with the debug version
	pTestInfo->henv = (SQLHANDLE) NULL;
	pTestInfo->hstmt =(SQLHANDLE) NULL;
	pTestInfo->hdbc = (SQLHANDLE) NULL;
	  
	// Initialize the log file
	TCHAR buff[4000];
	TCHAR timebuf[1024];

	time_t my_clock = time( NULL);
    _tcsftime( timebuf, 1024, _T("%Y-%m-%d_%H.%M.%S"), localtime( &my_clock ) );
	TFILE *myFile;
	
	while (true) {
#ifdef UNICODE
		TCHAR *cs = _T("UNICODE");
#else
		TCHAR *cs = _T("ANSI");
#endif
		_stprintf(buff, _T("coast_%s.%s.%s.%s.%s.%s.log"), timebuf, cs, charset, strapi, machine, DSN);

		myFile = _tfopen (buff,_T("r"));
		if (myFile == NULL)
			break;
		_tfclose (myFile);
	}

	LogInit(buff,3,_T("***ERROR: "));

#if defined(unixcli) && defined(UNICODE)
	// Initiate Unicode converter objects.
//	icu_conv->err = U_ZERO_ERROR;
//	icu_conv->converter= ucnv_open(inputLocale, &icu_conv->err);

	ucnv_setFallback(icu_conv->converter, TRUE);
#endif

	// need to get initial values for DSN, UID, and Password and set
	// the values in the Testinfo structure so all tests can use these
	if(!DriverConnectNoPrompt(pTestInfo)){
		LogMsg(ERRMSG+LINEBEFORE+LINEAFTER,
			_T("Unable to establish an initial connection.  No tests can be executed.\n"));
		delete pTestInfo;
		return 0;
	}

	LogInfo (pTestInfo);
       
	FullDisconnect(pTestInfo);

	g_Trace=TRUE;
	pTestInfo->Trace=TRUE;

	Run20Tests();
	Run21Tests();
	Run30Tests();

	LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,_T("Total Tests=%d  Failed=%d\n"),_gTestCount,_gTestFailedCount);
	_tprintf (_T("Total Tests=%d  Failed=%d\r\n"),_gTestCount,_gTestFailedCount);
	//_putts(_T("Results logged in file: "));
	//_putts(buff);
	_putts(_T("\r\nHave a good day! \r\n"));

	delete pTestInfo;

	return 0;
}

int Run20Tests()
{
	// Execute the selected tests
	// (as you add 'if' statements for each procedure to be tested
	//  try and keep them in alphabetical order so it is a bit 
	//  easier to find things)
	pTestInfo->Trace=FALSE;

	if (m_AllApi)
	{
		m_AllocEnv		= TRUE;
		m_AllocConnect	= TRUE;
		m_BrowseConnect = TRUE;
		m_Connect		= TRUE;
		m_DataSources	= TRUE;
		m_DriverConnect	= TRUE;
		m_Drivers		= TRUE;
		m_Error			= TRUE;
		m_ExecDirect	= TRUE;
		m_ExtendedFetch	= TRUE;
		m_Fetch			= TRUE;
		m_GetFunctions	= TRUE;
		m_MoreResults	= TRUE;
		m_NativeSql		= TRUE;
		m_NumParams		= TRUE;
		m_NumResultCols	= TRUE;
		m_Prepare		= TRUE;
		m_RowCount		= TRUE;
		m_Transact		= TRUE;
	}
	
	LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,_T("Starting ODBC 2.0 tests...\n"));
	_putts(_T("Starting ODBC 2.0 tests...\n"));
	if (m_AllocEnv)
	{
		_putts(_T("Running AllocEnv API.\r\n"));
		TestSQLAllocEnv(pTestInfo);
		LogResultsTest(_T("SQLAllocEnv (2.0)"));
	}
	if (m_AllocConnect)
	{
		_putts(_T("Running AllocConnect API.\r\n"));
		TestSQLAllocConnect(pTestInfo);
		LogResultsTest(_T("SQLAllocConnect (2.0)"));
	}
	if (m_BrowseConnect)
	{
		_putts(_T("Running BrowseConnect API.\r\n"));
		TestSQLBrowseConnect(pTestInfo);
		LogResultsTest(_T("SQLBrowseConnect (2.0)"));
	}
	if (m_Connect)				
	{
		_putts(_T("Running Connect API.\r\n"));
		TestSQLConnect(pTestInfo);
		LogResultsTest(_T("SQLConnect (2.0)"));
	}
	if (m_DataSources)
	{
		_putts(_T("Running DataSources API.\r\n"));
		TestSQLDataSources(pTestInfo);
		LogResultsTest(_T("SQLDataSources (2.0)"));
	}
	if (m_DriverConnect)
	{
		_putts(_T("Running DriveConnect API.\r\n"));
		TestSQLDriverConnect(pTestInfo);
		LogResultsTest(_T("SQLDriverConnect (2.0)"));
	}
	if (m_Drivers)
	{
		_putts(_T("Running Drivers API.\r\n"));
		TestSQLDrivers(pTestInfo);
		LogResultsTest(_T("SQLDrivers (2.0)"));
	}
	if (m_Error)
	{
		_putts(_T("Running Error API.\r\n"));
		TestSQLError(pTestInfo);
		LogResultsTest(_T("SQLError (2.0)"));
	}
	if (m_ExecDirect)			
	{
		_putts(_T("Running ExecDirect API.\r\n"));
		TestSQLExecDirect(pTestInfo);
		LogResultsTest(_T("SQLExecDirect (2.0)"));
	}
	if (m_ExtendedFetch)				
	{
		_putts(_T("Running ExtendedFetch API.\r\n"));
		TestSQLExtendedFetch(pTestInfo);
		LogResultsTest(_T("SQLExtendedFetch (2.0)"));
	}
	if (m_Fetch)				
	{
		_putts(_T("Running Fetch API.\r\n"));
		TestSQLFetch(pTestInfo);
		LogResultsTest(_T("SQLFetch (2.0)"));
	}
	if (m_GetFunctions)		
	{
		_putts(_T("Running GetFunctions API.\r\n"));
		TestSQLGetFunctions(pTestInfo);
		LogResultsTest(_T("SQLGetFunctions (2.0)"));
	}
	if (m_MoreResults)		
	{
		_putts(_T("Running MoreResults API.\r\n"));
		TestSQLMoreResults(pTestInfo);
		LogResultsTest(_T("SQLMoreResults (2.0)"));
	}
	if (m_NativeSql)			
	{
		_putts(_T("Running NativeSql API.\r\n"));
		TestSQLNativeSql(pTestInfo);
		LogResultsTest(_T("SQLNativeSql (2.0)"));
	}
	if (m_NumParams)			
	{
		_putts(_T("Running NumParams API.\r\n"));
		TestSQLNumParams(pTestInfo);
		LogResultsTest(_T("SQLNumParams (2.0)"));
	}
	if (m_NumResultCols)		
	{
		_putts(_T("Running NumResultCols API.\r\n"));
		TestSQLNumResultCols(pTestInfo);
		LogResultsTest(_T("SQLNumResultCols (2.0)"));
	}
	if (m_Prepare)				
	{
		_putts(_T("Running Prepare API.\r\n"));
		TestSQLPrepare(pTestInfo);
		LogResultsTest(_T("SQLPrepare (2.0)"));
	}
	if (m_RowCount)			
	{
		_putts(_T("Running RowCount API.\r\n"));
		TestSQLRowCount(pTestInfo);
		LogResultsTest(_T("SQLRowCount (2.0)"));
	}
	if (m_Transact)			
	{
		_putts(_T("Running Transact API.\r\n"));
		TestSQLTransact(pTestInfo);
		LogResultsTest(_T("SQLTransact (2.0)"));
	}

	// Display statistics for tests ran
	//LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,"Total Tests=%d  Failed=%d\n",_gTestCount,_gTestFailedCount);

	return 0;
}

int Run21Tests ()
{
	pTestInfo->Trace = FALSE;
	g_Trace=FALSE;

	if (m_AllApi)
	{
		m_AllocStmt			= TRUE;
		m_BindCol			= TRUE;
		m_BindParameter		= TRUE;
		m_Cancel			= TRUE;
		m_ColAttrib			= TRUE;
		m_Columns			= TRUE;
		m_DesCols			= TRUE;
		m_DescribeParam		= TRUE;
		m_Execute			= TRUE;
		m_GetData			= TRUE;
		m_PutData			= TRUE;
		m_GetInfo			= TRUE;
		m_GetTypeInfo		= TRUE;
		m_PrimaryKeys		= TRUE;
		m_SetConnectOption	= TRUE;
		m_SetCursorName		= TRUE;
		m_SetStmtOption		= TRUE;
		m_SpecialColumns	= TRUE;
		m_Statistics		= TRUE;
		m_Tables			= TRUE;
		m_ResGovern			= TRUE;
	}

	LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,_T("Starting ODBC 2.1 tests...\n"));
	_putts(_T("Starting ODBC 2.1 tests...\n"));
	if (m_AllocStmt)
	{
		_putts(_T("Running MX 2.10 AllocStmt API.\r\n"));
		TestSQLAllocStmt(pTestInfo, MX_SPECIFIC);
		LogResultsTest(_T("SQLAllocStmt (2.1)"));
	}

	if (m_BindCol)			
	{
		_putts(_T("Running MX 2.10 SQLBindCol API.\r\n"));
		TestMXSQLBindCol(pTestInfo);
		LogResultsTest(_T("SQLBindCol (2.1)"));
	}
	if (m_BindParameter)			
	{
		_putts(_T("Running MX 2.10 SQLBindParameter API.\r\n"));
		TestMXSQLBindParameter(pTestInfo);
		LogResultsTest(_T("SQLBindParameter (2.1)"));
	}
	
	if (m_Cancel)			
	{
		_putts(_T("Running MX 2.10 SQLCancel API.\r\n"));
		TestMXSQLCancel(pTestInfo);
		LogResultsTest(_T("SQLCancel (2.1)"));
	}
	
	if (m_ColAttrib)			
	{
		_putts(_T("Running MX 2.10 SQLColumnAttributes API.\r\n"));
		TestMXSQLColAttributes(pTestInfo);
		LogResultsTest(_T("SQLColumnAttributes (2.1)"));
	}
	if (m_Columns)			
	{
		_putts(_T("Running MX 2.10 SQLColumns API.\r\n"));
		TestMXSQLColumns(pTestInfo);
		LogResultsTest(_T("SQLColumns (2.1)"));
	}
	if (m_DesCols)			
	{
		_putts(_T("Running MX 2.10 SQLDescribeColumns API.\r\n"));
		TestMXSQLDescribeCol(pTestInfo);
		LogResultsTest(_T("SQLDescribeColumns (2.1)"));
	}
	if (m_DescribeParam)			
	{
		_putts(_T("Running MX 2.10 SQLDescribeParam API.\r\n"));
		TestSQLDescribeParam(pTestInfo,MX_SPECIFIC);
		LogResultsTest(_T("SQLDescribeParam (2.1)"));
	}
	if (m_Execute)			
	{
		_putts(_T("Running MX 2.10 SQLExecute API.\r\n"));
		TestSQLExecute(pTestInfo,MX_SPECIFIC);
		LogResultsTest(_T("SQLExecute (2.1)"));
	}
	if (m_GetData)			
	{
		_putts(_T("Running MX 2.10 SQLGetData API.\r\n"));
		TestMXSQLGetData(pTestInfo);
		LogResultsTest(_T("SQLGetData (2.1)"));
	}
	if (m_PutData)			
	{
		_putts(_T("Running MX 2.10 SQLPutData API.\r\n"));
		TestMXSQLPutData(pTestInfo);
		LogResultsTest(_T("SQLPutData (2.1)"));
	}
	if (m_GetInfo)			
	{
		_putts(_T("Running MX 2.10 SQLGetInfo API.\r\n"));
		TestMXSQLGetInfo(pTestInfo);
		LogResultsTest(_T("SQLGetInfo (2.1)"));
	}
	if (m_GetTypeInfo)			
	{
		_putts(_T("Running MX 2.10 SQLGetTypeInfo API.\r\n"));
		TestSQLGetTypeInfo(pTestInfo,MX_SPECIFIC);
		LogResultsTest(_T("SQLGetTypeInfo (2.1)"));
	}
	if (m_PrimaryKeys)
	{
		_putts(_T("Running MX 2.10 SQLPrimaryKeys API.\r\n"));
		TestSQLPrimaryKeys(pTestInfo,MX_SPECIFIC);
		LogResultsTest(_T("SQLPrimaryKeys (2.1)"));
	}
	if (m_SetConnectOption)
	{
		_putts(_T("Running MX 2.10 SQLSet/GetConnectOption API.\r\n"));
		TestSQLSetConnectOption(pTestInfo, MX_SPECIFIC);
		LogResultsTest(_T("SQLSet/GetConnectOption (2.1)"));
	}
	if (m_SetCursorName)
	{
		_putts(_T("Running MX 2.10 SQLSet/GetCursorName API.\r\n"));
		TestSQLSetCursorName(pTestInfo, MX_SPECIFIC);
		LogResultsTest(_T("SQLSet/GetCursorName (2.1)"));
	}
	if (m_SetStmtOption)
	{
		_putts(_T("Running MX 2.10 SQLSet/GetStmtOption API.\r\n"));
		TestSQLSetStmtOption(pTestInfo, MX_SPECIFIC);
		LogResultsTest(_T("SQLSet/GetStmtOption (2.1)"));
	}
	if (m_SpecialColumns)	
	{
		_putts(_T("Running MX 2.10 SQLSpecialColumns API.\r\n"));
		TestSQLSpecialColumns(pTestInfo, MX_SPECIFIC);
		LogResultsTest(_T("SQLSpecialColumns (2.1)"));
	}
	if (m_Statistics)			
	{
		_putts(_T("Running MX 2.10 SQLStatistics API.\r\n"));
		TestSQLStatistics(pTestInfo, MX_SPECIFIC);
		LogResultsTest(_T("SQLStatistics (2.1)"));
	}
	if (m_Tables)			
	{
		_putts(_T("Running MX 2.10 SQLTables API.\r\n"));
		TestMXSQLTables(pTestInfo);
		LogResultsTest(_T("SQLTables (2.1)"));
	}
	if (m_ResGovern)			
	{
		_putts(_T("Running MX 2.10 Resource Governing.\r\n"));
		TestMXResourceGovern(pTestInfo);
		LogResultsTest(_T("Resource Governing (2.1)"));
	}
	
	// Display statistics for tests ran
	//LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,"Total Tests=%d  Failed=%d\n",_gTestCount,_gTestFailedCount);
	return 0;
}

int	Run30Tests ()
{
	g_Trace=FALSE;
	pTestInfo->Trace=FALSE;

	if (m_AllApi)
	{
		m_AllocHandle30 = TRUE;
		m_BindCol30 = TRUE;
		m_GetConnectAttr30 = TRUE;
		m_EndTran30 = TRUE;
		m_CloseCursor30 = TRUE;
		m_CopyDesc30 = TRUE;
		m_GetDescRec30 = TRUE;	//also tests SQLSetDescRec
		m_GetEnvAttr30 = TRUE;
		m_GetData30 = TRUE;
		m_GetDiagRec30 = TRUE;
		m_GetDiagField30 = TRUE;
		m_BindParameter30 = TRUE;
		m_DescribeCol30 = TRUE;
		m_GetInfo30 = TRUE;
		m_MoreResults30 = TRUE;
		m_SetGetDescFields30 = TRUE;
		m_GetStmtAttr30 = TRUE;
		m_ColAttributes30 = TRUE;
		m_GetTypeInfo30R18 = TRUE;
		m_FetchScroll30 = TRUE;
		m_ForeignKeys30 = TRUE;
		m_ColumnPrivileges30 = TRUE;
		m_TablePrivileges30 = TRUE;

		// Interval Data Type Tests
		m_BindColInterval30 = TRUE;
		m_GetDataInterval30 = TRUE;
		m_BindParamInterval30 = TRUE;
		m_Unicode30 = TRUE;

		// Stored Procedures
		m_ProcedureColumns30 = TRUE;
		m_Procedures30 = TRUE;

		// Partial Date Time Conversions
		//m_PartialDateTimeInput30 = TRUE;
		//m_PartialDateTimeOutput30 = TRUE;

		// Features
		m_QueryID = TRUE;
		m_Hash2 = TRUE;
		m_LargeBlock = TRUE;
	        m_InfoStats = TRUE;
	}

	LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,_T("Starting ODBC 3.0 tests...\n"));
	_putts(_T("Starting ODBC 3.0 tests...\n"));

	if (m_AllocHandle30)
	{
		_putts(_T("Running MX 3.0 AllocHandle API.\r\n"));
		TestMXSQLAllocHandle(pTestInfo);
		LogResultsTest(_T("SQLAllocHandle (3.0)"));
	}
	if (m_BindCol30)			
	{
		_putts(_T("Running MX 3.0 SQLBindCol API.\r\n"));
		TestMXSQLBindColVer3(pTestInfo);
		LogResultsTest(_T("SQLBindCol (3.0)"));
	}
	if (m_GetConnectAttr30)
	{
		_putts(_T("Running MX 3.0 SetConnectAttr/GetConnectAttr API.\r\n"));
		TestMXSQLSetConnectAttr(pTestInfo);
		LogResultsTest(_T("SQLSet/GetConnectAttr (3.0)"));
	}
	if (m_EndTran30)
	{
		_putts(_T("Running MX 3.0 EndTran API.\r\n"));
		TestMXSQLEndTran(pTestInfo);
		LogResultsTest(_T("SQLEndTran (3.0)"));
	}
	if (m_CloseCursor30)
	{
		_putts(_T("Running MX 3.0 CloseCursor API.\r\n"));
		TestMXSQLCloseCursor(pTestInfo);
		LogResultsTest(_T("SQLCloseCursor (3.0)"));
	}
	if (m_CopyDesc30)
	{
		_putts(_T("Running MX 3.0 CopyDesc API.\r\n"));
		TestMXSQLCopyDesc(pTestInfo);
		LogResultsTest(_T("SQLCopyDesc (3.0)"));
	}
	if (m_GetData30)			
	{
		_putts(_T("Running MX 3.0 SQLGetData API.\r\n"));
		TestMXSQLGetDataVer3(pTestInfo);
		LogResultsTest(_T("SQLGetData (3.0)"));
	}
	if (m_GetDescRec30)
	{
		_putts(_T("Running MX 3.0 GetDescRec API.\r\n"));
		TestMXSQLGetDescRec(pTestInfo);
		LogResultsTest(_T("SQLGetDescRec (3.0)"));
	}
	if (m_GetEnvAttr30)
	{
		_putts(_T("Running MX 3.0 Set/GetEnvAttr API.\r\n"));
		TestMXSQLSetEnvAttr(pTestInfo);
		LogResultsTest(_T("SQLSet/GetEnvAttr (3.0)"));
	}
	if (m_GetDiagRec30)
	{
		_putts(_T("Running MX 3.0 GetDiagRec API.\r\n"));
		TestMXSQLGetDiagRec(pTestInfo);
		LogResultsTest(_T("SQLGetDiagRec (3.0)"));
	}
	if (m_GetDiagField30)
	{
		_putts(_T("Running MX 3.0 GetDiagField API.\r\n"));
		TestMXSQLGetDiagField(pTestInfo);
		LogResultsTest(_T("SQLGetDiagField (3.0)"));
	}
	if (m_GetStmtAttr30)
	{
		_putts(_T("Running MX 3.0 Set/GetStmtAttr API.\r\n"));
		TestMXSQLSetStmtAttr(pTestInfo);
		LogResultsTest(_T("SQLSet/GetStmtAttr (3.0)"));
	}
	if (m_ColAttributes30)
	{
		_putts(_T("Running MX 3.0 ColAttribute API.\r\n"));
		TestMXSQLColAttributeVer3(pTestInfo);
		LogResultsTest(_T("SQLColAttribute (3.0)"));
	}

	if (m_BindParameter30)
	{
		_putts(_T("Running MX 3.0 BindParameter API.\r\n"));
		TestMXSQLBindParameterVer3(pTestInfo);
		LogResultsTest(_T("SQLBindParameter (3.0)"));
	}
	if (m_DescribeCol30)
	{
		_putts(_T("Running MX 3.0 DescribeCol API.\r\n"));
		TestMXSQLDescribeColVer3(pTestInfo);
		LogResultsTest(_T("SQLDescribeCol (3.0)"));
	}
	if (m_FetchScroll30)			
	{
		_putts(_T("Running MX 3.0 SQLFetchScroll API.\r\n"));
		TestMXSQLFetchScroll(pTestInfo);
		LogResultsTest(_T("SQLFetchScroll (3.0)"));
	}
	if (m_GetInfo30)
	{
		_putts(_T("Running MX 3.0 GetInfo API.\r\n"));
		TestMXSQLGetInfoVer3(pTestInfo);
		LogResultsTest(_T("SQLGetInfo (3.0)"));
	}
	if (m_MoreResults30)
	{
		_putts(_T("Running MX 3.0 MoreResults API.\r\n"));
		TestSQLMoreResultsVer3(pTestInfo);
		LogResultsTest(_T("SQLMoreResults (3.0)"));
	}
	if (m_SetGetDescFields30)
	{
		_putts(_T("Running MX 3.0 Set and Get DescFields APIs.\r\n"));
		TestMXSQLSetGetDescFields(pTestInfo);
		LogResultsTest(_T("SQLSet/GetDescFields (3.0)"));
	}
	if (m_GetTypeInfo30R18)			
	{
		_putts(_T("Running MX 3.0 SQLGetTypeInfo API for R1.8.\r\n"));
		TestSQLGetTypeInfoR18(pTestInfo);
		LogResultsTest(_T("SQLGetTypeInfo (3.0)"));
	}
	if (m_ColumnPrivileges30)			
	{
		_putts(_T("Running MX 3.0 SQLColumnPrivileges API.\r\n"));
		TestMXSQLColumnPrivileges(pTestInfo);
		LogResultsTest(_T("SQLColumnPrivileges (3.0)"));
    }
	
	// Interval Data Type Tests
	if (m_BindParamInterval30)
	{
		_putts(_T("Running MX 3.0 Interval BindParam API.\r\n"));
		TestMXSQLBindParameterInterval(pTestInfo);
		LogResultsTest(_T("SQLBindParameter - Interval (3.0)"));
	}
	if (m_BindColInterval30)
	{
		_putts(_T("Running MX 3.0 Interval BindCol API.\r\n"));
		TestMXSQLBindColInterval(pTestInfo);
		LogResultsTest(_T("SQLBindCol - Interval (3.0)"));
	}
	if (m_GetDataInterval30)
	{
		_putts(_T("Running MX 3.0 Interval GetData API.\r\n"));
		TestMXSQLGetDataInterval(pTestInfo);
		LogResultsTest(_T("SQLGetData - interval (3.0)"));
	}
	if (m_ProcedureColumns30)	
	{
		_putts(_T("Running MX 3.0 ProcedureColumns API.\r\n"));
		TestMXSQLProcedureColumns(pTestInfo);
		LogResultsTest(_T("SQLProcedureColumns (3.0)"));
	}
	if (m_Procedures30)			
	{
		_putts(_T("Running MX 3.0 Procedures API.\r\n"));
		TestMXSQLProcedures(pTestInfo);
		LogResultsTest(_T("SQLProcedures (3.0)"));
	}
	if (m_Unicode30)
	{
		#ifdef unixcli
			_putts(_T("Running MX 3.0 Unicode tests.\r\n"));
			_putts(_T("Driver doesn't support Unicode yet!\r\n"));
		#else
			_putts(_T("Running MX 3.0 Unicode tests.\r\n"));
			TestMXSQLUnicode(pTestInfo);
			LogResultsTest(_T("Unicode (3.0)"));
		#endif
	}
	if (m_LargeBlock)
	{
		_putts(_T("Running LargeBlock feature tests.\r\n"));
		TestLargeBlock(pTestInfo);
		LogResultsTest(_T("LargeBlock"));
	}
	if (m_ForeignKeys30)			
	{
		_putts(_T("Running MX 3.0 SQLForeignKeys API.\r\n"));
		TestMXSQLForeignKeys(pTestInfo);
		LogResultsTest(_T("SQLForeignKeys (3.0)"));
	}
	if (m_QueryID)
	{
		_putts(_T("Running QueryID feature tests.\r\n"));
		TestQueryID(pTestInfo);
		LogResultsTest(_T("Query ID"));
	}
	if (m_Hash2)
	{
		#ifdef _HASH2
			_putts(_T("Running Hash2 feature tests.\r\n"));
			TestHash2(pTestInfo);
			LogResultsTest(_T("Hash2"));
		#else
			_putts(_T("Running Hash2 feature tests.\r\n"));
			_putts(_T("Hash2 feature is only supported by Linux and Solaris drivers\r\n"));
		#endif
	}
	if (m_InfoStats)
    {
        _putts(_T("Running InfoStats tests\r\n"));
		TestInfoStats(pTestInfo);
		LogResultsTest(_T("InfoStats"));
    }
    if (m_TablePrivileges30)			
	{
		_putts(_T("Running MX 3.0 SQLTablePrivileges API.\r\n"));
		TestMXSQLTablePrivileges(pTestInfo);
		LogResultsTest(_T("SQLTablePrivileges (3.0)"));
	}
/*
	// Partial DateTime Conversions
	if (m_PartialDateTimeInput30)	
	{
		_putts(_T("Running MX 3.0 Partial DateTime Input Conversion tests\r\n"));
		TestMXPartialDateTimeInputConversions(pTestInfo);
		LogResultsTest(_T("Partial Date/time - input conversion (3.0)"));
	}

	if (m_PartialDateTimeOutput30)	
	{
		_putts(_T("Running MX 3.0 Partial DateTime Output Conversion tests\r\n"));
		TestMXPartialDateTimeOutputConversions(pTestInfo);
		LogResultsTest(_T("Partial Date/time - output conversion (3.0)"));
	}
*/
	// Display statistics for tests ran

	return 0;
}

void ReadSelectedTests(TCHAR* filename) 
{
	TCHAR line[100];
    TCHAR *ret;
	TCHAR *seps  = _T(" \t");
	TCHAR *token;
	TFILE *input_file;
	
	input_file = _tfopen(filename, _T("r"));
	_tprintf(_T("%s\n"), filename);
	if (input_file == NULL)
	{
		_tprintf(_T("Error opening file %s\n"), filename);
		_tperror(_T("Unable to open file"));
		exit(-1);
	}

	ret = _fgetts(line, 80, input_file);

	while (ret != NULL)
	{
		line[_tcslen(line)-1] = '\0';
		token = _tcstok(line, seps);

		if (_tcsicmp(token,_T("SQLAllocEnv")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_AllocEnv = TRUE;
			else
				m_AllocEnv = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLAllocConnect")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_AllocConnect = TRUE;
			else
				m_AllocConnect = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLBindParameter")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_BindParameter = TRUE;
			else
				m_BindParameter = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLBrowseConnect")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_BrowseConnect = TRUE;
			else
				m_BrowseConnect = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLColumnAttribute")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_ColAttrib = TRUE;
			else
				m_ColAttrib = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLConnectDisconnect")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Connect = TRUE;
			else
				m_Connect = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLDataSources")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_DataSources = TRUE;
			else
				m_DataSources = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLDescribeColumns")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_DesCols = TRUE;
			else
				m_DesCols = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLDriverConnect")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_DriverConnect = TRUE;
			else
				m_DriverConnect = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLDrivers")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Drivers = TRUE;
			else
				m_Drivers = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLError")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Error = TRUE;
			else
				m_Error = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLExecuteDirect")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_ExecDirect = TRUE;
			else
				m_ExecDirect = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLExecute")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Execute = TRUE;
			else
				m_Execute = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLExtendedFetch")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_ExtendedFetch = TRUE;
			else
				m_ExtendedFetch = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLFetch")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Fetch = TRUE;
			else
				m_Fetch = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetData")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetData = TRUE;
			else
				m_GetData = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLPutData")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_PutData = TRUE;
			else
				m_PutData = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetFunctions")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetFunctions = TRUE;
			else
				m_GetFunctions = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetInfo")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetInfo = TRUE;
			else
				m_GetInfo = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLMoreResults")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_MoreResults = TRUE;
			else
				m_MoreResults = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLAllocStmt")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_AllocStmt = TRUE;
			else
				m_AllocStmt = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLBindColumn")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_BindCol = TRUE;
			else
				m_BindCol = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLColumns")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Columns = TRUE;
			else
				m_Columns = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLDescribeParam")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_DescribeParam = TRUE;
			else
				m_DescribeParam = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetTypeInfo")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetTypeInfo = TRUE;
			else
				m_GetTypeInfo = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLPrimaryKeys")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_PrimaryKeys = TRUE;
			else
				m_PrimaryKeys = FALSE;
			}
		else if (_tcsicmp(token,_T("ResourceGoverning")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_ResGovern = TRUE;
			else
				m_ResGovern = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLSetConnectOption")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_SetConnectOption = TRUE;
			else
				m_SetConnectOption = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLSetCursorName")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_SetCursorName = TRUE;
			else
				m_SetCursorName = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLSetStatementOption")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_SetStmtOption = TRUE;
			else
				m_SetStmtOption = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLSpecialColumns")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_SpecialColumns = TRUE;
			else
				m_SpecialColumns = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLStatistics")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Statistics = TRUE;
			else
				m_Statistics = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLTables")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Tables = TRUE;
			else
				m_Tables = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLNativeSql")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_NativeSql = TRUE;
			else
				m_NativeSql = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLNumParams")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_NumParams = TRUE;
			else
				m_NumParams = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLNumResultCols")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_NumResultCols = TRUE;
			else
				m_NumResultCols = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLPrepare")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Prepare = TRUE;
			else
				m_Prepare = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLRowCount")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_RowCount = TRUE;
			else
				m_RowCount = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLTransact")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Transact = TRUE;
			else
				m_Transact = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLAllocHandle")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_AllocHandle30= TRUE;
			else
				m_AllocHandle30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLBindParameter30")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_BindParameter30 = TRUE;
			else
				m_BindParameter30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLCloseCursor")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_CloseCursor30 = TRUE;
			else
				m_CloseCursor30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLColumnAttributes30")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_ColAttributes30 = TRUE;
			else
				m_ColAttributes30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLCopyDescriptor")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_CopyDesc30 = TRUE;
			else
				m_CopyDesc30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLDescribeColumns30")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_DescribeCol30 = TRUE;
			else
				m_DescribeCol30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLEndTran")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_EndTran30 = TRUE;
			else
				m_EndTran30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetConnectAttr")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetConnectAttr30 = TRUE;
			else
				m_GetConnectAttr30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetDescField")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_SetGetDescFields30 = TRUE;
			else
				m_SetGetDescFields30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetDescRec")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetDescRec30 = TRUE;
			else
				m_GetDescRec30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetDiagField")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetDiagField30 = TRUE;
			else
				m_GetDiagField30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetDiagRec")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetDiagRec30 = TRUE;
			else
				m_GetDiagRec30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetEnvAttr")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetEnvAttr30 = TRUE;
			else
				m_GetEnvAttr30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetInfo30")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetInfo30 = TRUE;
			else
				m_GetInfo30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetStmtAttr")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetStmtAttr30 = TRUE;
			else
				m_GetStmtAttr30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLMoreResults30")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_MoreResults30 = TRUE;
			else
				m_MoreResults30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLBindCol30")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_BindCol30 = TRUE;
			else
				m_BindCol30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetData30")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetData30 = TRUE;
			else
				m_GetData30 = FALSE;
			}
/*		else if (_tcsicmp(token,_T("SQLPartialDateTimeInput")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_PartialDateTimeInput = TRUE;
			else
				m_PartialDateTimeInput = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLPartialDateTimeOutput")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_PartialDateTimeOutput = TRUE;
			else
				m_PartialDateTimeOutput = FALSE;
			}
*/		else if (_tcsicmp(token,_T("SQLBindColInterval")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_BindColInterval30 = TRUE;
			else
				m_BindColInterval30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetDataInterval")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetDataInterval30 = TRUE;
			else
				m_GetDataInterval30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLBindParamInterval")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_BindParamInterval30 = TRUE;
			else
				m_BindParamInterval30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLForeignKeys")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_ForeignKeys30 = TRUE;
			else
				m_ForeignKeys30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLColumnPriv")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_ColumnPrivileges30 = TRUE;
			else
				m_ColumnPrivileges30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLTablePriv")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_TablePrivileges30 = TRUE;
			else
				m_TablePrivileges30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLGetTypeInfo3")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_GetTypeInfo30R18 = TRUE;
			else
				m_GetTypeInfo30R18 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLProcedures")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Procedures30 = TRUE;
			else
				m_Procedures30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLProcedureColumns")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_ProcedureColumns30 = TRUE;
			else
				m_ProcedureColumns30 = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLFetchScroll")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_FetchScroll30 = TRUE;
			else
				m_FetchScroll30 = FALSE;
			}
		else if (_tcsicmp(token,_T("Unicode")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Unicode30 = TRUE;
			else
				m_Unicode30 = FALSE;
			}
		else if (_tcsicmp(token,_T("QueryID")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_QueryID = TRUE;
			else
				m_QueryID = FALSE;
			}
		else if (_tcsicmp(token,_T("Hash2")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Hash2 = TRUE;
			else
				m_Hash2 = FALSE;
			}
		else if (_tcsicmp(token,_T("LargeBlock")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_LargeBlock = TRUE;
			else
				m_LargeBlock = FALSE;
			}
        else if (_tcsicmp(token,_T("InfoStats")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_InfoStats = TRUE;
			else
				m_InfoStats = FALSE;
			}
		else if (_tcsicmp(token,_T("SQLCancel")) == 0)
			{
			token = _tcstok(NULL, seps);
			if (_tcsicmp(token,_T("YES")) == 0)
				m_Cancel = TRUE;
			else
				m_Cancel = FALSE;
			}
		else _tprintf(_T("***ERROR: %s does not match any of the expected API names or known tokens.\n"),token);

		ret = _fgetts(line, 80, input_file);
	}
}

void MapApiNameToFlag(TCHAR *token)
{
	if (_tcsicmp(token,_T("SQLAllocEnv")) == 0)
		m_AllocEnv = TRUE;
	else if (_tcsicmp(token,_T("SQLAllocConnect")) == 0)
		m_AllocConnect = TRUE;
	else if (_tcsicmp(token,_T("SQLBindParameter")) == 0)
		m_BindParameter = TRUE;
	else if (_tcsicmp(token,_T("SQLBrowseConnect")) == 0)
		m_BrowseConnect = TRUE;
	else if (_tcsicmp(token,_T("SQLColumnAttribute")) == 0)
		m_ColAttrib = TRUE;
	else if (_tcsicmp(token,_T("SQLConnectDisconnect")) == 0)
		m_Connect = TRUE;
	else if (_tcsicmp(token,_T("SQLDataSources")) == 0)
		m_DataSources = TRUE;
	else if (_tcsicmp(token,_T("SQLDescribeColumns")) == 0)
		m_DesCols = TRUE;
	else if (_tcsicmp(token,_T("SQLDriverConnect")) == 0)
		m_DriverConnect = TRUE;
	else if (_tcsicmp(token,_T("SQLDrivers")) == 0)
		m_Drivers = TRUE;
	else if (_tcsicmp(token,_T("SQLError")) == 0)
		m_Error = TRUE;
	else if (_tcsicmp(token,_T("SQLExecuteDirect")) == 0)
		m_ExecDirect = TRUE;
	else if (_tcsicmp(token,_T("SQLExecute")) == 0)
		m_Execute = TRUE;
	else if (_tcsicmp(token,_T("SQLExtendedFetch")) == 0)
		m_ExtendedFetch = TRUE;
	else if (_tcsicmp(token,_T("SQLFetch")) == 0)
		m_Fetch = TRUE;
	else if (_tcsicmp(token,_T("SQLGetData")) == 0)
		m_GetData = TRUE;
	else if (_tcsicmp(token,_T("SQLPutData")) == 0)
		m_PutData = TRUE;
	else if (_tcsicmp(token,_T("SQLGetFunctions")) == 0)
		m_GetFunctions = TRUE;
	else if (_tcsicmp(token,_T("SQLGetInfo")) == 0)
		m_GetInfo = TRUE;
	else if (_tcsicmp(token,_T("SQLMoreResults")) == 0)
		m_MoreResults = TRUE;
	else if (_tcsicmp(token,_T("SQLAllocStmt")) == 0)
		m_AllocStmt = TRUE;
	else if (_tcsicmp(token,_T("SQLBindColumn")) == 0)
		m_BindCol = TRUE;
	else if (_tcsicmp(token,_T("SQLColumns")) == 0)
		m_Columns = TRUE;
	else if (_tcsicmp(token,_T("SQLDescribeParam")) == 0)
		m_DescribeParam = TRUE;
	else if (_tcsicmp(token,_T("SQLGetTypeInfo")) == 0)
		m_GetTypeInfo = TRUE;
	else if (_tcsicmp(token,_T("SQLPrimaryKeys")) == 0)
		m_PrimaryKeys = TRUE;
	else if (_tcsicmp(token,_T("ResourceGoverning")) == 0)
		m_ResGovern = TRUE;
	else if (_tcsicmp(token,_T("SQLSetConnectOption")) == 0)
		m_SetConnectOption = TRUE;
	else if (_tcsicmp(token,_T("SQLSetCursorName")) == 0)
		m_SetCursorName = TRUE;
	else if (_tcsicmp(token,_T("SQLSetStatementOption")) == 0)
		m_SetStmtOption = TRUE;
	else if (_tcsicmp(token,_T("SQLSpecialColumns")) == 0)
		m_SpecialColumns = TRUE;
	else if (_tcsicmp(token,_T("SQLStatistics")) == 0)
		m_Statistics = TRUE;
	else if (_tcsicmp(token,_T("SQLTables")) == 0)
		m_Tables = TRUE;
	else if (_tcsicmp(token,_T("SQLNativeSql")) == 0)
		m_NativeSql = TRUE;
	else if (_tcsicmp(token,_T("SQLNumParams")) == 0)
		m_NumParams = TRUE;
	else if (_tcsicmp(token,_T("SQLNumResultCols")) == 0)
		m_NumResultCols = TRUE;
	else if (_tcsicmp(token,_T("SQLPrepare")) == 0)
		m_Prepare = TRUE;
	else if (_tcsicmp(token,_T("SQLRowCount")) == 0)
		m_RowCount = TRUE;
	else if (_tcsicmp(token,_T("SQLTransact")) == 0)
		m_Transact = TRUE;
	else if (_tcsicmp(token,_T("SQLAllocHandle")) == 0)
		m_AllocHandle30 = TRUE;
	else if (_tcsicmp(token,_T("SQLBindParameter30")) == 0)
		m_BindParameter30 = TRUE;
	else if (_tcsicmp(token,_T("SQLCloseCursor")) == 0)
		m_CloseCursor30 = TRUE;
	else if (_tcsicmp(token,_T("SQLColumnAttributes30")) == 0)
		m_ColAttributes30 = TRUE;
	else if (_tcsicmp(token,_T("SQLCopyDescriptor")) == 0)
		m_CopyDesc30 = TRUE;
	else if (_tcsicmp(token,_T("SQLDescribeColumns30")) == 0)
		m_DescribeCol30 = TRUE;
	else if (_tcsicmp(token,_T("SQLEndTran")) == 0)
		m_EndTran30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetConnectAttr")) == 0)
		m_GetConnectAttr30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetDescField")) == 0)
		m_SetGetDescFields30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetDescRec")) == 0)
		m_GetDescRec30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetDiagField")) == 0)
		m_GetDiagField30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetDiagRec")) == 0)
		m_GetDiagRec30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetEnvAttr")) == 0)
		m_GetEnvAttr30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetInfo30")) == 0)
		m_GetInfo30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetStmtAttr")) == 0)
		m_GetStmtAttr30 = TRUE;
	else if (_tcsicmp(token,_T("SQLMoreResults30")) == 0)
		m_MoreResults30 = TRUE;
	else if (_tcsicmp(token,_T("SQLBindCol30")) == 0)
		m_BindCol30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetData30")) == 0)
		m_GetData30 = TRUE;
/*	else if (_tcsicmp(token,_T("SQLPartialDateTimeInput")) == 0)
		m_PartialDateTimeInput = TRUE;
	else if (_tcsicmp(token,_T("SQLPartialDateTimeOutput")) == 0)
		m_PartialDateTimeOutput = TRUE;
*/
	else if (_tcsicmp(token,_T("SQLBindColInterval")) == 0)
		m_BindColInterval30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetDataInterval")) == 0)
		m_GetDataInterval30 = TRUE;
	else if (_tcsicmp(token,_T("SQLBindParamInterval")) == 0)
		m_BindParamInterval30 = TRUE;
	else if (_tcsicmp(token,_T("SQLForeignKeys")) == 0)
		m_ForeignKeys30 = TRUE;
	else if (_tcsicmp(token,_T("SQLColumnPriv")) == 0)
		m_ColumnPrivileges30 = TRUE;
	else if (_tcsicmp(token,_T("SQLTablePriv")) == 0)
		m_TablePrivileges30 = TRUE;
	else if (_tcsicmp(token,_T("SQLGetTypeInfo3")) == 0)
		m_GetTypeInfo30R18 = TRUE;
	else if (_tcsicmp(token,_T("SQLProcedures")) == 0)
		m_Procedures30 = TRUE;
	else if (_tcsicmp(token,_T("SQLProcedureColumns")) == 0)
		m_ProcedureColumns30 = TRUE;
	else if (_tcsicmp(token,_T("SQLFetchScroll")) == 0)
		m_FetchScroll30 = TRUE;
	else if (_tcsicmp(token,_T("Unicode")) == 0)
		m_Unicode30 = TRUE;
	else if (_tcsicmp(token,_T("QueryID")) == 0)
		m_QueryID = TRUE;
	else if (_tcsicmp(token,_T("Hash2")) == 0)
		m_Hash2 = TRUE;
	else if (_tcsicmp(token,_T("SQLCancel")) == 0)
		m_Cancel = TRUE;
	else if (_tcsicmp(token,_T("LargeBlock")) == 0)
		m_LargeBlock = TRUE;
    else if (_tcsicmp(token,_T("InfoStats")) == 0)
		m_InfoStats = TRUE;
	else _tprintf(_T("***ERROR: %s does not match any of the expected API names or known tokens.\n"),token);
}

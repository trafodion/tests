#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"
#include "apitests.h"

#define isUCS2 1

#define MAX_SIZE_KEY				2048
#define	MAX_SIZE_KEY_UCS2			1024
#define MAX_SIZE_COL				32708
#define MAX_COL		 				20
#define MAX_FILENAME_LENGTH			256
#define MAX_SERVER_NAME_LENGTH		128
#define SQL_MAX_DB_NAME_LEN			60
#define MAX_STRING_SIZE				500
#define STATE_SIZE					6
#define OUT_CONN_STR				1024

#define EXEC_DIRECT					0
#define PREPARE_EXEC_FETCH			1
#define PREPARE_EXEC_EXNENDEDFETCH	2

#define T_SQLConnect				0
#define T_SQLDriverConnect			1

#ifndef _WM
#define DATE_FORMAT1 _T("2007-12-30")
#define DATE_FORMAT2 _T("2007-10-30")
#else
#define DATE_FORMAT1 _T("07/12/30")
#define DATE_FORMAT2 _T("07/10/30")
#endif

PassFail TestLargeBlock(TestInfo *pTestInfo)
{
	TEST_DECLARE;
	TCHAR				temp[MAX_SIZE_KEY];
	TCHAR				sqlStmt[MAX_SIZE_COL];
	TCHAR				outValue[MAX_SIZE_KEY];
	TCHAR				keysize[18];
 	TCHAR				Heading[MAX_STRING_SIZE];
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	SQLUSMALLINT		FetchStatus;
	SQLULEN				FetchProcessed;
	SQLLEN				OutConn_tcslen;
	int					loop, totalLen = 0, i, j=0, k,n;
	bool				failed = false;

	TCHAR				ld_input[MAX_SIZE_KEY+3];
    TCHAR				ld_input_half[MAX_SIZE_KEY+3];
	TCHAR				ld_output[MAX_SIZE_KEY+3];
    TCHAR				ld_output_half[MAX_SIZE_KEY+3];
    TCHAR				datastr1_input[MAX_SIZE_KEY+3], datastr1_output[MAX_SIZE_KEY+3];      //"abcdefghij"
    TCHAR				datastr2_input[MAX_SIZE_KEY+3], datastr2_output[MAX_SIZE_KEY+3];      //"'abcdefghijklmnopqrstuvwxyz1234567890'"
    TCHAR				datastr3_input[MAX_SIZE_KEY+3], datastr3_output[MAX_SIZE_KEY+3];      //"abcdefghijk123432"
    TCHAR				datastr4_input[MAX_SIZE_KEY+3], datastr4_output[MAX_SIZE_KEY+3];      //"13453aabea__DEJKD"

	TCHAR				*DrpTable,*CrtTable,*InsTable,*SelTable,*UpdTable,*DelTable,*whereClause;

	struct _Row {
		TCHAR		A[MAX_COL][MAX_SIZE_KEY*4+2];
		SQLLEN		AInd[MAX_COL];
	} aRow;

	struct
	{
		int			size;
		TCHAR		*cols;
		TCHAR		*input[MAX_COL];
		TCHAR		*updatecols;
		TCHAR		*output[MAX_COL];
	} dataTypesMatrix[] = {
		{2, _T("--"),	{ld_input,_T("'0123456789'")},		                _T("--"),		{ld_output,datastr1_output}},
		{2, _T("--"),	{ld_input,_T("'0123456789'")},		                _T("--"),		{ld_output,datastr1_output}},
		{2, _T("--"),	{ld_input,_T("1234.56789")},		                _T("--"),		{ld_output,_T("9876.54321")}},
		{2, _T("--"),	{ld_input,_T("5678.12345")},		                _T("--"),		{ld_output,_T("1234.56785")}},
		{2, _T("--"),	{ld_input,_T("5678.12345")},		                _T("--"),		{ld_output,_T("1234.56785")}},
		{2, _T("--"),	{ld_input,_T("-1234")},				                _T("--"),		{ld_output,_T("-4321")}},
		{2, _T("--"),	{ld_input,_T("6789")},				                _T("--"),		{ld_output,_T("9876")}},
		{2, _T("--"),	{ld_input,_T("-12345")},			                _T("--"),		{ld_output,_T("-54321")}},
		{2, _T("--"),	{ld_input,_T("56789")},				                _T("--"),		{ld_output,_T("98765")}},
		{2, _T("--"),	{ld_input,_T("12340")},				                _T("--"),		{ld_output,_T("54321.0")}},
		{2, _T("--"),	{ld_input,_T("12300")},				                _T("--"),		{ld_output,_T("32100.0")}},
		{2, _T("--"),	{ld_input,_T("12345670")},			                _T("--"),		{ld_output,_T("76543210.0")}},
		{2, _T("--"),	{ld_input,_T("{d '1993-12-30'}")},	                _T("--"),		{ld_output,DATE_FORMAT1}},
		{2, _T("--"),	{ld_input,_T("-9876543")},			                _T("--"),		{ld_output,_T("-1234567")}},
		{2, _T("--"),	{ld_input,_T("{t '11:45:23'}")},	                _T("--"),		{ld_output,_T("12:15:20")}},
		{2, _T("--"),	{ld_input,_T("{ts '1992-12-31 23:45:23.123456'}")}, _T("--"),     {ld_output,_T("2007-12-30 12:15:20.123456")}},
		{3, _T("--"),	{ld_input,ld_input,_T("123456.001")},	            _T("--"),     {ld_output,ld_output,_T("654321.001")}},
		{4, _T("--"),	{_T("123450"),ld_input,_T("123456.001"),ld_input},  _T("--"),     {_T("123450"),ld_output,_T("654321.001"),ld_output}},
		{18,_T("--"),	{ld_input,_T("'0123456789'"),_T("'0123456789'"),ld_input,_T("1234.56789"),_T("5678.12345"),_T("-1234"),_T("6789"),_T("-12345"),_T("56789"),_T("12340"),_T("12300"),_T("12345670"),_T("{d '1993-12-30'}"),_T("{t '11:45:23'}"),_T("{ts '1992-12-31 23:45:23.123456'}"),_T("-9876543"),_T("12345678.9012345678901234567890")},_T("--"),{ld_output,datastr1_output,datastr1_output,ld_output,_T("9876.54321"),_T("8765.12345"),_T("-4321"),_T("9876"),_T("-54321"),_T("98765"),_T("43210.0"),_T("32100.0"),_T("76543210.0"),DATE_FORMAT2,_T("12:25:21"),_T("2007-10-30 12:25:21.123456"),_T("-6563455"),/* SEAQUEST _T("-12345678.1234567890000000000000") */ _T("-12345678.123456789")}},
        //This section is for Bignum testing
		{2, _T("--"),	{ld_input,_T("1234567890.12345678")},               _T("--"),		{ld_output,_T("123456789.12345678")}},
		{2, _T("--"),	{ld_input,_T("12345678901234567890.12345678901234567890123456789012345678901")},_T("--"),{ld_output,_T("-123456789012345678901234567890.123456789012345678901234567890123456789012345678901000")}},
		{2, _T("--"),	{_T("-1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678"),_T("'1234567890'")},_T("--"),{_T("-1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678"),_T("0123456")}},
		{2, _T("--"),	{_T("1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678"),_T("'1234567890'")}, _T("--"),{_T("1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678"),_T("0123456")}},
		{2, _T("--"),	{_T("'1234567890'"),_T("1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678")}, _T("--"),{_T("1234567890"),_T("1234567890123456789012345678901234567890.1234567890123456789012345678901234567890123456789012345678901234")}},
		{2, _T("--"),   {_T("'1234567890'"),_T("-1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678")},_T("--"),{_T("1234567890"),_T("-1234567890123456789012345678901234567890.1234567890123456789012345678901234567890123456789012345678901234")}},
		{2, _T("--"),   {_T("'1234567890'"),_T("1234567890123456789012345678901234567890123456789012345678901234.5678901234567890123456789012345678901234567890123456789012345678")}, _T("--"),{_T("1234567890"),_T("1234567890123456789012345678901234567890.1234567890123456789012345678901234567890123456789012345678901234")}},
		{7, _T("--"),	{_T("1234567"),_T("12345678.1234567899"),_T("1234567890123456789"),_T("1234567890123456789012345678901234567890"),_T("1234567890123456789012345678901234567890.123456789012345678901234567890123456789"),_T("0.12345678901234567890123456789012345678901234567890123456789012345678901234567890"),_T("1234567.8901234567")},_T("--"),{_T("1234567"),_T("12345678.1234500000"),_T("1234567890"),_T("123456789012345678901234567890123456789012345678901234.5678901234"),_T("12345678901234567890.1234567890000000000000000000000000000000000000000000000000000000"),
        #ifndef _WM
			_T("0.12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000"),_T("0.1234567890")}},
        #else
			_T(".12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000"),_T(".1234567890")}},
        #endif			
		{7, _T("--"),{_T("-1234567.1234567899"),_T("-12345678.1234567899"),_T("-1234567890123456789"),_T("-1234567890123456789012345678901234567890"),_T("-1234567890123456789012345678901234567890.123456789012345678901234567890123456789"),_T("-0.12345678901234567890123456789012345678901"),_T("-1234567.8901234567")},_T("--"),{_T("-1234567.1234567899000000000000000000000000000000000000000000000000000000"),_T("-12345678.1234500000"),_T("-1234567890"),_T("-12345678901234567890123456789012345678901234567890123456789012345678901234567890"),_T("-12345678901234567890.1234567890000000000000000000000000000000000000000000000000000000"),
        
		#ifndef _WM
			_T("-0.12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000"),_T("-0.1234567890")}},
        #else
			_T("-.12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000"),_T("-.1234567890")}},
        #endif

		{7, _T("--"),{_T("0.12345678901234567899"),_T("-12345678.1234567899"),_T("1234567890123456789"),_T("-1234567890123456789012345678901234567890"),_T("1234567890123456789012345678901234567890.123456789012345678901234567890123456789"),_T("-0.12345678901234567890123456789012345678901"),_T("1234567.8901234567")},_T("--"),

		#ifndef _WM
			{_T("0.12345678901234567899000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),_T("12345678.1234500000"),_T("-1234567890"),_T("12345678901234567890123456789012345678901234567890123456789012345678901234567890"),_T("-12345678901234567890.1234567890000000000000000000000000000000000000000000000000000000"),_T("0.12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000"),_T("-0.1234567890")}},
        #else
			{_T(".12345678901234567899000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),_T("12345678.1234500000"),_T("-1234567890"),_T("12345678901234567890123456789012345678901234567890123456789012345678901234567890"),_T("-12345678901234567890.1234567890000000000000000000000000000000000000000000000000000000"),_T(".12345678901234567890123456789012345678901234567890123456789000000000000000000000000000000000000000000000000000000000000000000000"),_T("-.1234567890")}},
        #endif		

//#ifdef UNICODE  
		{10,_T("--"),{_T("0.12345678901234567890"),_T("123.456789"),_T("1234567890"),_T("1234.567890"),_T("0.123456789"),_T("12345.6789012345"),_T("123456789012345600"),_T("123456789.012345600"),_T("0.123456789012345678"),_T("12.12345678901234567890")},_T("--"),

		#ifndef _WM
			{_T("0.12345678901234567890000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),_T("123.456780"),_T("1234567899"),_T("1234.567899"),_T("0.1234567890"),_T("1234.6789012345"),_T("1234567890123456"),_T("12345678.012345600"),_T("0.123456789012345670"),_T("12.12345678901234567800")}},
        #else
			{_T(".12345678901234567890000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"),_T("123.456780"),_T("1234567899"),_T("1234.567899"),_T(".1234567890"),_T("1234.6789012345"),_T("1234567890123456"),_T("12345678.012345600"),_T(".123456789012345670"),_T("12.12345678901234567800")}},
        #endif
		{6, _T("--"),{ld_input,ld_input_half,ld_input,ld_input_half,datastr2_input,datastr2_input},_T("--"),{ld_output,datastr3_output,datastr3_output,datastr3_output,datastr3_output,datastr3_output}},
		{6, _T("--"),{ld_input,ld_input_half,ld_input,ld_input_half,datastr2_input,datastr2_input},_T("--"),{ld_output,ld_output_half,datastr4_output,ld_output_half,datastr4_output,datastr2_output}},
		{6, _T("--"),{ld_input,ld_input_half,ld_input,ld_input_half,datastr2_input,datastr2_input},_T("--"),{ld_output,datastr3_output,ld_output,datastr3_output,datastr2_output,datastr3_output}},
//#endif
		{9999}
	};

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("LargeBlock"), charset_file);
	if (var_list == NULL) return FAILED;

	DrpTable = var_mapping(_T("LargeBlock_DrpTable"), var_list);
	CrtTable = var_mapping(_T("LargeBlock_CrtTable"), var_list);
	InsTable = var_mapping(_T("LargeBlock_InsTable"), var_list);
	SelTable = var_mapping(_T("LargeBlock_SelTable"), var_list);
	UpdTable = var_mapping(_T("LargeBlock_UpdTable"), var_list);
	DelTable = var_mapping(_T("LargeBlock_DelTable"), var_list);
	
	if(isUCS2) {
		_stprintf(keysize, _T("%d"), MAX_SIZE_KEY_UCS2);
	} else {
		_stprintf(keysize, _T("%d"), MAX_SIZE_KEY);
	}

    i = 0;
    while(dataTypesMatrix[i].size != 9999) {
		if((i==16 || i==17) && isUCS2) {
			_stprintf(temp,_T("LargeBlock_dataTypesMatrix_cols_%d_UCS2"), i);
			dataTypesMatrix[i].cols = var_mapping(temp, var_list);
        } else {
			_stprintf(temp,_T("LargeBlock_dataTypesMatrix_cols_%d"), i);
			dataTypesMatrix[i].cols = var_mapping(temp, var_list);
        }
		_stprintf(temp,_T("LargeBlock_dataTypesMatrix_updatecols_%d"), i);
		dataTypesMatrix[i].updatecols = var_mapping(temp, var_list);
        i++;
    }

    whereClause = var_mapping(_T("LargeBlock_UpdTable_w"), var_list);

    _stprintf(datastr1_input,_T("'%s'"),var_mapping(_T("LargeBlock_datastr1"), var_list));
    _stprintf(datastr2_input,_T("'%s'"),var_mapping(_T("LargeBlock_datastr2"), var_list));
    _stprintf(datastr3_input,_T("'%s'"),var_mapping(_T("LargeBlock_datastr3"), var_list));
    _stprintf(datastr4_input,_T("'%s'"),var_mapping(_T("LargeBlock_datastr4"), var_list));
	_stprintf(datastr1_output,_T("%s"),var_mapping(_T("LargeBlock_datastr1"), var_list));
    _stprintf(datastr2_output,_T("%s"),var_mapping(_T("LargeBlock_datastr2"), var_list));
    _stprintf(datastr3_output,_T("%s"),var_mapping(_T("LargeBlock_datastr3"), var_list));
    _stprintf(datastr4_output,_T("%s"),var_mapping(_T("LargeBlock_datastr4"), var_list));

//=============================================================================================================================
	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing feature =>LargeBlock | LargeBlock | largeblock.cpp\n"));
	TEST_INIT;

	TESTCASE_BEGINW(_T("Setup for LargeBlock tests\n"));
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
		TEST_FAILED;
		TEST_RETURN;
	}
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;

	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}

	//Generate large data
	j=0;
	if(isUCS2) j = MAX_SIZE_KEY_UCS2;
	else       j = MAX_SIZE_KEY;
	ld_input[0] = '\'';
	for (i=0; i<j; i++) {
		ld_input[i+1] = (char)(i%10 + 48);
		ld_output[i] = (char)(i%10 + 48);
	}
	ld_input[i+1] = '\'';
	ld_input[i+2] = '\0';
	ld_output[i] = '\0';

    if(isUCS2) {
        _tcsncpy(ld_input_half,ld_input,i+3);
        _tcsncpy(ld_output_half,ld_output,i+1);
    } else {
        _tcsncpy(ld_input_half,ld_input,MAX_SIZE_KEY_UCS2+1);
        ld_input_half[MAX_SIZE_KEY_UCS2+1] = '\'';
        ld_input_half[MAX_SIZE_KEY_UCS2+2] = '\0';
        _tcsncpy(ld_output_half,ld_output,MAX_SIZE_KEY_UCS2);
        ld_output_half[MAX_SIZE_KEY_UCS2] = '\0';
    }

    //LogMsg(NONE,_T("String in is %s\n"),ld_input_half);
    //LogMsg(NONE,_T("String out is %s\n"),ld_output_half);

	TESTCASE_END; // end of setup

//=============================================================================================================================

	i=0;
	while (dataTypesMatrix[i].size != 9999) {
		SQLExecDirect(hstmt, (SQLTCHAR*)DrpTable,SQL_NTS); //clean up

		for (loop=0; loop<=PREPARE_EXEC_EXNENDEDFETCH; loop++) {
			if (loop == EXEC_DIRECT)
				_stprintf(Heading,_T("Test %d.a Positive functionality of LargeBlock by doing ExecDirect\n"),i+1);
			else if (loop == PREPARE_EXEC_FETCH)
				_stprintf(Heading,_T("Test %d.b Positive functionality of LargeBlock by doing Prepare/Execute/Fetch\n"),i+1);
			else 
				_stprintf(Heading,_T("Test %d.c Positive functionality of LargeBlock by doing Prepare/Execute/ExtendedFetch\n"),i+1);
            TESTCASE_BEGINW(Heading);

			//Create table
			_stprintf(sqlStmt, _T("%s %s"), CrtTable,dataTypesMatrix[i].cols);
			// replace_str(sqlStmt,"$$$$",keysize);
			// _stprintf(temp,"%d",MAX_SIZE_KEY_UCS2);
			// replace_str(sqlStmt,"****",temp);
			LogMsg(NONE, _T("Create table: %s\n"), sqlStmt);
			if (loop ==  EXEC_DIRECT) {
				returncode = SQLExecDirect(hstmt, (SQLTCHAR*)sqlStmt,SQL_NTS);
                if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")) {
					LogMsg(NONE,_T("The string is: %s\n"),sqlStmt);
                    LogAllErrors(henv,hdbc,hstmt);				
                    TEST_FAILED;
                }
			}
			else {
				returncode = SQLPrepare(hstmt, (SQLTCHAR*)sqlStmt,SQL_NTS);
                if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")) {
					LogMsg(NONE,_T("The string is: %s\n"),sqlStmt);
					TEST_FAILED;
                    LogAllErrors(henv,hdbc,hstmt);
                }
				returncode = SQLExecute(hstmt);			
                if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")) {
					LogMsg(NONE,_T("The string is: %s\n"),sqlStmt);
					TEST_FAILED;
                    LogAllErrors(henv,hdbc,hstmt);
                }
			}

			/**********************************************************************************/
			// Susan: Before insert the table, initiate the ld_input  
                        if ( _tcscmp(ld_input,_T("")) == 0 ) { //Susan: check if the ld_input is flooded 

                                j=0;
                                if(isUCS2) j = MAX_SIZE_KEY_UCS2;
                                else       j = MAX_SIZE_KEY;

                                ld_input[0] = '\'';
                                for ( n=0; n<j; n++) {
                                        ld_input[n+1] = (char)(n%10 + 48);
                                }

                                ld_input[n+1] = '\'';
                                ld_input[n+2] = '\0';
                        }			

			//Insert table
			if (dataTypesMatrix[i].size != 1) {
				for (j=0; j<dataTypesMatrix[i].size; j++) {
					totalLen += _tcslen(dataTypesMatrix[i].input[j]);
				}
				_stprintf(sqlStmt, _T("%s ( "), InsTable);
				for (j=0; j<dataTypesMatrix[i].size; j++) {
					_tcscat(sqlStmt,dataTypesMatrix[i].input[j]);
        			        if (j<dataTypesMatrix[i].size-1) {
						_tcscat(sqlStmt,_T(","));
                        			if(i>= 30 && i <= 32 && (j == 0 || j == 2 || j == 4))
						_tcscat (sqlStmt,_T("_UCS2"));
                    			}
				}
				_tcscat(sqlStmt,_T(" )"));
			}
			else {
				_stprintf(sqlStmt, _T("%s ( %s )"), InsTable, dataTypesMatrix[i].input[0]);
			}

			LogMsg(LINEBEFORE, _T("INSERT ONTO TABLE ...:%s\n"), sqlStmt);
			if (loop ==  EXEC_DIRECT) {
				returncode = SQLExecDirect(hstmt, (SQLTCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
					LogMsg(NONE,_T("(i:%d) The string is: %s\n"), i,sqlStmt);
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}
			}
			else {
				returncode = SQLPrepare(hstmt, (SQLTCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
					LogMsg(NONE,_T("The string is: %s\n"),sqlStmt);
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}
				returncode = SQLExecute(hstmt);			
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute"))
				{
					LogMsg(NONE,_T("The string is: %s\n"),sqlStmt);
					LogMsg(ERRMSG,_T("SQLExecute. Expected: SQL_SUCCESS, actual: %d at line %d\n"), returncode, __LINE__);
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
				}
			}

			/**********************************************************************************/
			//Update table
			_stprintf(sqlStmt, _T("%s %s %s%s"), UpdTable, dataTypesMatrix[i].updatecols, whereClause, dataTypesMatrix[i].input[0]);
			LogMsg(LINEBEFORE,_T("UPDATE TABLE ...%s\n"), sqlStmt);

			if (loop ==  EXEC_DIRECT) {
				returncode = SQLExecDirect(hstmt, (SQLTCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
					LogMsg(NONE,_T("The string is: %s\n"),sqlStmt);
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}
			}
			else {
				returncode = SQLPrepare(hstmt, (SQLTCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
					LogMsg(NONE,_T("The string is: %s\n"),sqlStmt);
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}

				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
					LogMsg(NONE,_T("The string is: %s\n"),sqlStmt);
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}
			}
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);

			/**********************************************************************************/
			//Select table using different types of APIs
			if (loop != PREPARE_EXEC_EXNENDEDFETCH)
			{
				if (loop ==  EXEC_DIRECT) {
					LogMsg(LINEBEFORE,_T("Using EXEC_DIRECT, Test id=%d\n"), i+1);
					returncode = SQLExecDirect(hstmt, (SQLTCHAR*)SelTable,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
                        			LogMsg(NONE,_T("The string is: %s\n"),SelTable);
                        			LogAllErrors(henv,hdbc,hstmt);				
                        			TEST_FAILED;
                    			}
				}
				else {
					LogMsg(LINEBEFORE,_T("Using PREPARE_EXEC, Test id=%d\n"), i+1);
					returncode = SQLPrepare(hstmt, (SQLTCHAR*)SelTable,SQL_NTS);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
                        			LogMsg(NONE,_T("The string is: %s\n"),SelTable);
                        			LogAllErrors(henv,hdbc,hstmt);				
                        			TEST_FAILED;
                    			}

					returncode = SQLExecute(hstmt);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
                        			LogMsg(NONE,_T("The string is: %s\n"),SelTable);
                        			LogAllErrors(henv,hdbc,hstmt);				
                        			TEST_FAILED;
                    			}
				}

		                //LogMsg(LINEBEFORE,_T("%s\n"), SelTable);

				returncode = SQLFetch(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch")){
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}	

				if (returncode == SQL_SUCCESS_WITH_INFO) {
					LogAllErrors(henv,hdbc,hstmt);
				}

				failed = false;
				for (j = 0; j < dataTypesMatrix[i].size; j++)
				{  
					returncode = SQLGetData(hstmt,(SWORD)(j+1),SQL_C_TCHAR, outValue, (MAX_SIZE_KEY+1)*sizeof(TCHAR),&OutConn_tcslen);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
					{
						LogAllErrors(henv,hdbc,hstmt);
						failed = true;
					}
					else
					{
						if(_tcsncmp(outValue,dataTypesMatrix[i].output[j],_tcslen(dataTypesMatrix[i].output[j]))!=0 &&
						   _tcsnicmp(outValue,dataTypesMatrix[i].output[j],_tcslen(dataTypesMatrix[i].output[j]))!=0) 
						{
								failed = true;
								LogMsg(ERRMSG,_T("(i:%d j:%d) expect: %s and actual: %s values of column %d are not matched at %d\n"),i, j, dataTypesMatrix[i].output[j],outValue, j+1,__LINE__);
						}
						//else {
                            //LogMsg(NONE,_T("expect: %s and actual: %s values of column %d\n"),dataTypesMatrix[i].output[j],outValue);
                        //}
					}
				}
				if (failed) {
					TEST_FAILED;
				}
			}
			else {
				SQLSetStmtOption(hstmt, SQL_CONCURRENCY, SQL_CONCUR_READ_ONLY);
				SQLSetStmtOption(hstmt, SQL_CURSOR_TYPE, SQL_CURSOR_FORWARD_ONLY);
				SQLSetStmtOption(hstmt, SQL_ROWSET_SIZE, 1);
				SQLSetStmtOption(hstmt, SQL_BIND_TYPE, sizeof(aRow));

				// Bind the parameters in row-wise fashion.
				for (j=0; j<dataTypesMatrix[i].size; j++) {
					returncode = SQLBindCol(hstmt, j+1, SQL_C_TCHAR, &aRow.A[j], /* MAX_SIZE_KEY*4 */(MAX_SIZE_KEY+1)*sizeof(TCHAR), &aRow.AInd[j]);
					if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBindCol"))
						TEST_FAILED;
				}

				// Execute the select statement.
				LogMsg(LINEBEFORE,_T("Using PREPARE_EXEC_EXNENDEDFETCH, Test id=%d\n"), i+1);
				returncode = SQLExecDirect(hstmt, (SQLTCHAR*)SelTable,SQL_NTS);
				LogMsg(NONE, _T("Select table:%s\n"), SelTable);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}

				returncode = SQL_SUCCESS;
				while (returncode != SQL_NO_DATA_FOUND || returncode == SQL_ERROR)
				{
					returncode = SQLExtendedFetch(hstmt, SQL_FETCH_NEXT, 1, &FetchProcessed, &FetchStatus);
					if (returncode == SQL_ERROR)
					{
                        			LogMsg(ERRMSG,_T("SQLExtendedFetch, select table: %s\n"),SelTable);
						LogAllErrors(henv,hdbc,hstmt);
						TEST_FAILED;
					}
					if (returncode == SQL_NO_DATA_FOUND || returncode == SQL_ERROR) break;

					//Check to see which sets of parameters were processed successfully.
					for (k = 0; k < (int)FetchProcessed; k++) 
					{
						returncode = SQLSetPos(hstmt, k+1, SQL_POSITION, SQL_LOCK_UNLOCK);
						if (returncode == SQL_ERROR)
						{
							LogMsg(ERRMSG,_T("SQLSetPos, expected SQL_SUCCESS, actual : %d\n"), returncode);
							LogAllErrors(henv,hdbc,hstmt);
							TEST_FAILED;
						}
						if (FetchStatus == SQL_ROW_SUCCESS || FetchStatus == SQL_ROW_SUCCESS_WITH_INFO) 
						{
							failed = false;
							for (j=0; j<dataTypesMatrix[i].size; j++) {
								if (aRow.AInd[j] == SQL_NULL_DATA) {
									LogMsg(ERRMSG,_T("Col SQL_NULL_DATA\n"));
									failed = true;
									continue;
								}

								if(_tcsncmp(aRow.A[j],dataTypesMatrix[i].output[j],_tcslen(dataTypesMatrix[i].output[j]))!=0 &&
								   _tcsnicmp(aRow.A[j],dataTypesMatrix[i].output[j],_tcslen(dataTypesMatrix[i].output[j]))!=0)
								{
										failed = true;
										LogMsg(ERRMSG,_T("(i:%d j:%d k:%d) expect: %s and actual: %s values of column %d are not matched at %d\n"),i, j, k, dataTypesMatrix[i].output[j],aRow.A[j], j+1,__LINE__);
								}
								else
								{
									//LogMsg(NONE,_T("expect: %s and actual: %s values of column %d are matched\n"), dataTypesMatrix[i].output[j],aRow.A[j],j+1);
								}
							}

							if (failed) {
								TEST_FAILED;
							}
						}
					}//End For loop
				}//End while loop
			}//End else
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);

			/**********************************************************************************/
			//Delete a row using Prepare/Execute
			//Susan: Modify the code
			// _stprintf(sqlStmt, _T("%s%s"), DelTable,dataTypesMatrix[i].input[0]);
			_stprintf(sqlStmt, _T("%s"), DelTable);

			LogMsg(LINEBEFORE,_T("DELETE FROM TABLE ...\n"));
			if (loop ==  EXEC_DIRECT) {
				returncode = SQLExecDirect(hstmt, (SQLTCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
                   	 		LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}
			}
			else {
				returncode = SQLPrepare(hstmt, (SQLTCHAR*)sqlStmt,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}

				returncode = SQLExecute(hstmt);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}
			}
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);

			/**********************************************************************************/
			//Drop table
			if (loop ==  EXEC_DIRECT) {
				returncode = SQLExecDirect(hstmt, (SQLTCHAR*)DrpTable,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect")){
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}
			}
			else {
				returncode = SQLPrepare(hstmt, (SQLTCHAR*)DrpTable,SQL_NTS);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLPrepare")){
                    			LogAllErrors(henv,hdbc,hstmt);				
                    			TEST_FAILED;
                		}

				returncode = SQLExecute(hstmt);			
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecute")){
                    		LogAllErrors(henv,hdbc,hstmt);				
                    		TEST_FAILED;
                		}
			}
			SQLFreeStmt(hstmt,SQL_UNBIND);
			SQLFreeStmt(hstmt,SQL_CLOSE);
			TESTCASE_END;
		}//End for loop

		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLFreeStmt(hstmt,SQL_CLOSE);

		i++;
	}

//============================================================================================
	FullDisconnect3(pTestInfo);
	free_list(var_list);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => LargeBlock.\n"));
	TEST_RETURN;
}

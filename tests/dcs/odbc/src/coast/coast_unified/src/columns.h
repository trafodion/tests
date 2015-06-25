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


extern PassFail CreateMouseDB( TestInfo *);

/*
---------------------------------------------------------
TestSQLColumns()                      
Tests the SQLColumns function in ODBC, also tests wildcard 
syntax of parser.

TestSQLColumns loops through the test cases and generates the
calls to 'TestSQLColumnsExec' which actually does the work and
analyzes the return values
*/

#define NUM_CALLS	16
#define RESULT_DIR	"\\results\\SQLColumns"

typedef struct COLPARAMSTRUCTtag	{
	TCHAR	*szQualifier;
	TCHAR	*szOwner;
	TCHAR	*szName;
	TCHAR	*szCol;	
}  COLPARAMSTRUCT;

 /* Parameter Arrays for testing */
 COLPARAMSTRUCT cps[NUM_CALLS] = {
	NULL,		NULL,				_T("mice"),			NULL,
	NULL,		_T("%"),				NULL,				(_T("%e"),			
	NULL,       _T("CAT_SYLVESTR"),	NULL,				NULL,
	NULL,		NULL,				_T("%1"),				NULL,
	NULL,		_T("MOUSE_MINNIE"),	NULL,				_T("H%"),
	NULL,		_T("MOUSE_%"),			_T("_tab_"),			NULL,
	NULL,		_T("%.s%"),			_T("d%"),				_T("%"),
	NULL,		_T("%"),				_T("_tab%"),			NULL,
	NULL,		_T("______M%"),		_T("%b_"),				NULL,
	NULL,		_T("dbo"),				_T("_tab"),			_T("%t%"),
	NULL,		_T("dbo"),				_T("_tab"),			_T("s%"),
	NULL,		_T("C%"),				_T("%tab%"),			_T("%"),
	NULL,		_T("_at_%"),			_T("%"),				NULL,
	NULL,		NULL,				_T("ATAB"),			NULL,
	NULL,		_T("MOUSE_%"),			_T("A%B1"),			_T("%FLD_"),
	NULL,		NULL,				NULL,				_T("NAMEFLD_"),
 };

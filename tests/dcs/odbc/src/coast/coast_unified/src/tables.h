/* tables.h
   Defininitions and declaration for tables.c, functions for testing
   SQLTables functionality.
*/
#define NUM_CALLS   15
#define RESULT_DIR  _T("\\results\\SQLTables")

typedef struct TABPARAMSTRUCTtag   {
    TCHAR   *szQualifier;
    TCHAR   *szOwner;
    TCHAR   *szName;
    TCHAR   *szType;
}  TABPARAMSTRUCT;


PassFail TestSQLTablesExec( TestInfo *pTestInfo, TABPARAMSTRUCT * );

 /* Parameter Arrays for testing */
 TABPARAMSTRUCT tps[NUM_CALLS] = {
    NULL,       NULL,					NULL,               NULL,
    NULL,       _T("%"),				NULL,               NULL,
    _T("%") ,NULL,					NULL,               NULL,
    NULL,       NULL,					_T("%1"),		NULL,
    NULL,       _T("MOUSE_MINNIE"),	NULL,				_T("TABLE"),
    NULL,       _T("MOUSE_%"),		_T("_tab_"),		_T("VIEW"),
    NULL,       _T("%_s%"),			_T("d%"),		NULL,
    NULL,       _T("%"),				_T("_tab%"),		_T("TABLE"),
    NULL,       _T("______M%"),		_T("%b_"),		NULL,
    NULL,       _T("dbo"),			_T("_tab"),		_T("TABLE"),
    NULL,       _T("dbo"),			_T("_tab"),		_T("VIEW"),
    NULL,       _T("C%"),			_T("%tab%"),		_T("VIEW"),
    NULL,       _T("_at%"),			_T("%"),			_T("TABLE"),
    NULL,       NULL,					_T("A%B"),		_T("TABLE"),
    NULL,       _T("MOUSE_%"),		_T("A%B1"),		_T("VIEW")
 };

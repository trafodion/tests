#ifndef __SQLUTILH
#define __SQLUTILH

#define SQL_COLUMN_NOT_FOUND          "S0022"
#define SQL_DUPLICATE_KEY_ERROR       -8102

extern short AllocateValueBuffer(ColumnInfo *pColumn);
extern short ScanTableColumns(TableInfo *pTable,
                       short ODBCDataType,
                       short start_column);
extern short ScanTableColumnsForNondatetime(TableInfo *pTable,short start_column);
extern short ScanTableColumnsForNumber(TableInfo *pTable,short start_column);
extern ColumnInfo *GetColumnInfo(HSTMT hstmt,
                           short ColumnPosition,
                           ColumnInfo *pColumn,
                           ReturnStatus **RSPtr);
extern TableInfo *GetTableInfo(HDBC hdbc,
			                  char *table_name,
				               Boolean syskey,
					            ReturnStatus **RSPtr);
extern ReturnStatus *BindAndFillAllParams(HSTMT hstmt,TableInfo *pTable);
extern ReturnStatus *BuildReturnStatusODBC(short ODBCReturnCode,
                                    HENV henv,
                                    HDBC hdbc,
                                    HSTMT hstmt,
                                    ReturnStatus *RS_Ptr);

#endif

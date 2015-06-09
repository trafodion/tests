#ifndef __TABLEH      /* this prevents multiple copies of this... */
#define __TABLEH      /* ...include file from being #included... */


/*********************************************************
** TABLE.H  : Header file for all functions in TABLE.C
**********************************************************/

/* Some limits */
#define SQL_MAX_COL_NAME       30
#define SQL_MAX_COLUMNS        255   /* not a real SQL limit, just one I picked */
#define SQL_MAX_SELECT_STAT    255
#define SQL_MAX_HEADING_LEN    30
#define SQL_MAX_ROW_LENGTH     4059
#define ODBC_MAX_CHAR_COLUMN_LENGTH    254
#define SQL_MAX_CHAR_COLUMN_LENGTH     SQL_MAX_ROW_LENGTH
#define SQL_MAX_KEY_COLUMNS		255

#define DP2_BLOCK_HEADER_SIZE  32    /* >>>>just another guess */

/* SQL data types */
#define TYPE_UNKNOWN           -3232
#define TYPE_CHAR              1
#define TYPE_NUMERIC           2
#define TYPE_DECIMAL           3
#define TYPE_INT               4
#define TYPE_SMALLINT          5
#define TYPE_FLOAT             6
#define TYPE_REAL              7
#define TYPE_DOUBLE            8
#define TYPE_VARCHAR           9
#define TYPE_LONGVARCHAR       10
#define TYPE_BIGINT            11

#define TYPE_DATE              12
#define TYPE_TIME              13
#define TYPE_TIMESTAMP         14

#define TYPE_BINARY            15
#define TYPE_VARBINARY         16
#define TYPE_LONGVARBINARY     17
#define TYPE_TINYINT           18
#define TYPE_BIT               19

#define MAX_TYPES              14	// only the first 14 types are supported by SQL/MX

/* SQL Date and Time defines */
#define TYPE_FRACTION          1
#define TYPE_SECOND            2
#define TYPE_MINUTE            3
#define TYPE_HOUR              4
#define TYPE_DAY               5
#define TYPE_MONTH             6
#define TYPE_YEAR              7


/* Sort order for key fields */
#define KEY_ASC   1
#define KEY_DESC  2

/* Column defaults */
#define COL_DEFAULT_NULL        1
#define COL_DEFAULT_NONE        2
#define COL_DEFAULT_LITERAL     3
#define COL_DEFAULT_USER        4

/* SQL Key types */
#define SYSTEM_KEY          0
#define PRIMARY_KEY         1
#define CLUSTERING_KEY      2

/**************************************************************************
** The following UNION is defined for pointers to buffers of different
** (SQL) data types.
**************************************************************************/
union AllDataTypes {
   char           *pChar;
   short          *pSmallint;
   unsigned short *pUsmallint;
   long           *pInteger;
   unsigned long  *pUinteger;
   float          *pReal;
   double         *pDouble;
   };
typedef union AllDataTypes AllDataTypes;

/**********************************************************************
** Date and Time Field Definition Structure
**********************************************************************/
struct DateAndTime {
  short Year;
  short Month;
  short Day;
  short Hour;
  short Min;
  short Sec;
  short MilliSec;
  short MicroSec;
  };
typedef struct DateAndTime DateAndTime;

/**********************************************************************
** Key Structure (also used to define index columns)
**********************************************************************/
struct KeyDef {
  short ColNum;     /* Column field, Default = -1 */
  short AscDesc;    /* Default = -1,0 (Ascending order),1 (Descending order) */
};
typedef struct KeyDef KeyDef;

/**********************************************************************
** SQL Data Types Definition Structure
**********************************************************************/
struct SQLTypeInfo {
	char	TypeName[SQL_MAX_COL_NAME+1];
	short	SQLDataType;
	short	ColumnSize;
	char	LiteralPrefix[SQL_MAX_COL_NAME+1];
	char	LiteralSuffix[SQL_MAX_COL_NAME+1];
	char	CreateParams[SQL_MAX_COL_NAME+1];
	short	Nullable;
	short CaseSensitive;
	short	Searchable;
	short	UnsignedAttr;
	short FixedPrecScale;
	short	AutoIncrement;
	char	LocalTypeName[(SQL_MAX_COL_NAME+1)*2];
	short MinScale;
	short MaxScale;
	short	SQLDataType2;		// ODBC 3.0 only
	short	SQLDatetimeSub;	// ODBC 3.0 only
	long	NumPrecRadix;		// ODBC 3.0 only
	short	IntervalPrecision;// ODBC 3.0 only
	struct SQLTypeInfo *pNext;
	};
typedef struct SQLTypeInfo SQLTypeInfo;


/**********************************************************************
** Column Definition Structure
**********************************************************************/
struct ColumnInfo {
	char	CName[SQL_MAX_COL_NAME+1];  /* Column name */
	Boolean	AutoIncrement;
	Boolean	CaseSensitive;
	Boolean	FixedPrecScale;
	long	DisplaySize;                /* Max number of characters to display value */
	char	*Label;
	short	DataType;                   // Data Type values as defined at the front of this file
												 // do not confuse these data type values with the actual
												 // ODBC data types as defined in SQL.H

	long	DataTypeLen;                /* Length (or Precision) of data type */
	short	DataTypePrecision;
	short	DataTypeScale;              /* Scale of data type */
	SQLTypeInfo	*pTypeInfo;				// pointer to generic info about this SQL data type
	AllDataTypes Value;				// pointer to buffer containing the actual value
	short	Nullable;
	short	Searchable;
	Boolean	UnsignedColumn;
	short	Updatable;

	// additional parameters used in CREATE
	short  DefaultType;                /* None, Literal, NULL, or USER */
	char   *Literal;                   /* Literal value of default (except for date/time) */
	Boolean UniqueColumn;
	Boolean PrimaryKey;
	char *ReferenceTable;
	char *ReferencedColumns;
	char *Constraint;
	char CHeading[SQL_MAX_HEADING_LEN];        /* Heading string */
	Boolean  Money;

	// ODBC 3.0 column attributes
	char	*BaseColName;		// ODBC 3.0 only
	char	*BaseTableName;	// ODBC 3.0 only
	long	ConciseType;		// ODBC 3.0 only
	char	*LiteralPrefix;	// ODBC 3.0 only
	char	*LiteralSuffix;	// ODBC 3.0 only
	char	*LocalTypeName;	// ODBC 3.0 only
	long	NumPrecRadix;		// ODBC 3.0 only
	long	OctetLength;		// ODBC 3.0 only


  };
typedef struct ColumnInfo ColumnInfo;

/**********************************************************************
** Index Information Structure
** >>>> Indexes are not implemented yet, this is just a place holder
**********************************************************************/
struct IndexInfo {
  short JustAPlaceHolder;
  };
typedef struct IndexInfo IndexInfo;

/**********************************************************************
** Table Information Structure
**********************************************************************/
struct TableInfo {
  char TableName[SQL_MAX_TABLE_NAME_LEN]; /* Table Name (fully qualified) */
  char ShortTableName[SQL_MAX_DSN_LENGTH];// just the Table Name (not fully qualified)
  char TCatalog[SQL_MAX_TABLE_NAME_LEN]; /* Table Catalog */
                                         /* Default = System Catalog */
  char SchemaName[SQL_MAX_TABLE_NAME_LEN];

  short  Organization;                   /* Key Sequenced   = 1 */
                                         /* Entry Sequenced = 2 */	// SQL/MP only
                                         /* Relative        = 3 */	// SQL/MP only

  short  NumOfCol;                       /* Number of Columns */
  ColumnInfo *ColPtr;                    // Pointer to first Column Structure...
														// ...(the beginning of an array of structures)

  short KeyType;                         /* 0 (system key), */
                                         /* 1 (Primary key)*/
													  // 2 (Clustering Key)
  short KeyColCount;                     /* number of Key Columns */
  KeyDef *KeyPtr;                        /* Pointer to first Key Structure */
                                         /* NOTE: KeyDefs are stored in sequence order */
													  // ...(the beginning of an array of structures)

  short IndexCount;                      /* number of indexes */
  IndexInfo *IndexPtr;                   /* pointer to first Index */

  long  RowLength;                      /* Default = -1, Total bytes of rows */
  };
typedef struct TableInfo TableInfo;


/*************************************************************************
** Function Declarations
*************************************************************************/
extern SQLTypeInfo *GetSQLTypeInfo(char *DataSource,char *UserID, char *Password);
extern SQLTypeInfo *FindSQLTypeInfo(short DataType);
extern short FindODBCType(short DataType);
extern TableInfo *InitializeTableInfo(short NCol,short NKeyCol);
extern void CopyTableInfo(TableInfo *ToPtr,TableInfo *FromPtr);
extern void FillTableInfo (TableInfo *TP);
extern void FillColumnInfo (ColumnInfo *ColumnPtr);
extern ColumnInfo *GetColumnInfoByName(ColumnInfo *ColumnListPtr,short ColumnCount,
                                       char *ColumnNameToSearchFor);
extern short GetColumnNumber(TableInfo *pTable,char *ColumnNameToSearchFor);
extern char *BuildColumnString( ColumnInfo *colstr );
extern char *BuildCreateTableString (TableInfo *TP);
extern void FreeTableInfo(TableInfo *TP);
extern char *RandomODBCDateTimeString(short DateTimeType);
extern char *RandomDecimalString(short Precision,short Scale);

#endif

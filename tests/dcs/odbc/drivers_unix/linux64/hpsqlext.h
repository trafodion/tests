/*
// @@@ START COPYRIGHT @@@
//
// Copyright 2006-2007
// Hewlett Packard Development Company, L.P.
// Protected as an unpublished work.
// All rights reserved.
//
// The computer program listings, specifications and
// documentation herein are the property of Compaq Computer
// Corporation and successor entities such as Hewlett Packard
// Development Company, L.P., or a third party supplier and
// shall not be reproduced, copied, disclosed, or used in whole
// or in part for any reason without the prior express written
// permission of Hewlett Packard Development Company, L.P.
//
// @@@ END COPYRIGHT @@@
*/

#ifndef __HPSQLEXTH
#define __HPSQLEXTH

// Attribute to turn non atomic rowset behaviour OFF or ON
// default is non atomic rowsets (SQL_ATTR_ROWSET_RECOVERY_ON)
// for Atomic rowsets set this attribute to SQL_ATTR_ROWSET_RECOVERY_OFF
#define SQL_ATTR_ROWSET_RECOVERY        2000
#define SQL_ATTR_ROWSET_RECOVERY_OFF    0
#define SQL_ATTR_ROWSET_RECOVERY_ON     1

// HP Session Name connection attribute
#define SQL_ATTR_SESSIONNAME		5000
// Attribute to get the 64bit rowcount when using the 32-bit ODBC driver
#define SQL_ATTR_ROWCOUNT64_PTR		5001
// HP rolename attribute
#define SQL_ATTR_ROLENAME 			5002
// Attribute to set fetchahead connection attribute
#define SQL_ATTR_FETCHAHEAD			5003

/* Max Session Name length including terminating null */
#define SQL_MAX_SESSIONNAME_LEN		25
/* Max rolename Name length including terminating null */
#define SQL_MAX_ROLENAME_LEN		128

//wms_mapping 
#define SQL_ATTR_APPLNAME			5100
#define SQL_MAX_APPLNAME_LEN		128

// HP Security
#define SQL_ATTR_CERTIFICATE_DIR			5200
#define SQL_ATTR_CERTIFICATE_FILE			5201
#define SQL_ATTR_CERTIFICATE_FILE_ACTIVE	5202
#ifdef HOLDABLE
#define SQL_ATTR_CURSOR_HOLDABLE	-3  // 
#define SQL_NONHOLDABLE			0
#define SQL_HOLDABLE			1
#endif

#endif /* __HPSQLEXTH */

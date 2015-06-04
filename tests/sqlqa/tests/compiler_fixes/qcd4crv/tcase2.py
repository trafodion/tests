# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@

from ...lib import hpdci
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""INFER_CHARSET compiler abend"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """control query default pos 'OFF';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default odbc_process 'ON';"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default infer_charset 'ON';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table tval
(
C_VAL                          CHAR(12) NO DEFAULT NOT NULL
HEADING 'CODE VALEUR'
, Y_D_VALI                       CHAR(1) NO DEFAULT NOT NULL
HEADING 'TYPE DATE VALIDITE'
, C_SGR_RLC                      CHAR(2) NO DEFAULT NOT NULL
HEADING 'CODE SOUS GROUPE RLC'
, Q_LOT_NG                       NUMERIC( 18, 0) NO DEFAULT NOT NULL
HEADING 'QUANTITE LOT NEGOCIATION'
, L_VAL                          CHAR(30) NO DEFAULT NOT NULL
HEADING 'LIBELLE VALEUR'
, C_GR_RLC                       CHAR(2) NO DEFAULT NOT NULL
HEADING 'CODE GROUPE RLC'
, C_VAL_MNE                      CHAR(10) DEFAULT ' ' NOT NULL
HEADING 'CODE MNEMONIQUE VALEUR'
, I_AJ_VAL                       NUMERIC( 1, 0) NO DEFAULT NOT NULL
HEADING 'INDICATEUR AJUSTEMENT VALEUR'
, P_DR_COT_V_AJ                  NUMERIC( 18, 7) NOT NULL
HEADING 'COURS (DERNIER) COTE VEILLE AJUSTE'
, C_GD_S_VAL                     CHAR(1) NO DEFAULT NOT NULL
HEADING 'CODE GRANDE CATEGORIE VALEUR'
, Y_EXP_P_VAL                    CHAR(1) NO DEFAULT NOT NULL
HEADING 'TYPE EXPRESSION COURS VALEUR'
, YUNIPVAL                       CHAR(1) DEFAULT ' ' NOT NULL
HEADING 'TYPE D''UNITE DES COURS VALEUR'
, P_DR_COT_VAL                   NUMERIC( 18, 7) NOT NULL
HEADING 'COURS (DERNIER) COTE VALEUR'
, P_PB_COT_VAL                   NUMERIC( 18, 7) NOT NULL
HEADING 'COURS (PLUS BAS) COTE VALEUR'
, P_PH_COT_VAL                   NUMERIC( 18, 7) NOT NULL
HEADING 'COURS (PLUS HAUT) COTE VALEUR'
, P_TEO_OV                       NUMERIC( 18, 7) NOT NULL
HEADING 'COURS THEORIQUE OUVERTURE'
, Q_LIM_SIM_AC                   NUMERIC( 18, 7) NOT NULL
HEADING 'MONTANT LIMITE SIMULE ACHAT'
, Q_LIM_SIM_VT                   NUMERIC( 18, 7) NOT NULL
HEADING 'MONTANT LIMITE SIMULE VENTE'
, Z_TRAN                         NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE TRANSACTION'
, Z_TRAN_PB                      NUMERIC( 7, 0) NOT NULL
HEADING 'NOMBRE TRANSACTION (PLUS BAS)'
, Z_TRAN_PH                      NUMERIC( 7, 0) NOT NULL
HEADING 'NOMBRE TRANSACTION (PLUS HAUT)'
, Q_SOM_LIM_SIM_AC               NUMERIC( 18, 0) NOT NULL
HEADING 'QUANTITE CUMUL LIMITE SIMULE ACHAT'
, Q_SOM_LIM_SIM_VT               NUMERIC( 18, 0) NOT NULL
HEADING 'QUANTITE CUMUL LIMITE SIMULE VENTE'
, Q_NG_SOM                       NUMERIC( 18, 0) NOT NULL
HEADING 'QUANTITE NEGOCIEE CUMUL'
, Q_NREP_OV                      NUMERIC( 18, 0) NOT NULL
HEADING 'QUANTITE NON REPONDUE OUVERTURE'
, Q_TOT_NG_OV                    NUMERIC( 18, 0) NOT NULL
HEADING 'QUANTITE TOTALE NEGOCIEE OUVERTURE'
, Q_FMP                          NUMERIC( 18, 0) NOT NULL
HEADING 'QUANTITE FOURCHETTE MOYENNE PONDEREE'
, I_RES                          CHAR(1) DEFAULT ' ' NOT NULL
HEADING 'INDICATEUR RESERVATION'
, I_SENS_Q_NREP_OV               CHAR(1) DEFAULT ' ' NOT NULL
HEADING 'INDICATEUR SENS QUANTITE NON REPONDUE OUVERTURE'
, H_OV_PGM_VAL                   timestamp(0) NO DEFAULT NOT NULL
HEADING 'HEURE OUVERTURE PROGRAMME VALEUR'
, D_VALI_P_EXT                   DATE
HEADING 'DATE VALIDITE COURS EXTREME'
, S_INTE_PB                      NUMERIC( 18, 7) NOT NULL
HEADING 'SEUIL INTERMEDIAIRE BAS'
, S_INTE_PH                      NUMERIC( 18, 7) NOT NULL
HEADING 'SEUIL INTERMEDIARE HAUT'
, P_AVT_DR_COT_VAL               NUMERIC( 18, 7) NOT NULL
HEADING 'COURS (AVANT DERNIER) COTE VALEUR'
, P_RF                           NUMERIC( 18, 7) NOT NULL
HEADING 'COURS REFERENCE'
, X_TICK_VAL                     NUMERIC( 18, 7) NOT NULL
HEADING '% TICK_LIMIT VALEUR - LIMITE DE FLUCTUATION'
, C_PL_COT                       NUMERIC( 3, 0) NO DEFAULT NOT NULL
HEADING 'CODE PLACE COTATION VALEUR'
, Z_OM_CRN                       NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE EN CARNET'
, C_DEV_COT                      CHAR(3) NO DEFAULT NOT NULL
HEADING 'CODE DEVISE COTATION'
, C_ETA_VAL                      CHAR(2) NO DEFAULT NOT NULL
HEADING 'CODE ETAT VALEUR'
, C_ID_GRC                       CHAR(2) NO DEFAULT NOT NULL
HEADING 'CODE IDENTIFIANT GROUPE VALEUR'
, D_J_CALD                       DATE  NO DEFAULT
HEADING 'DATE JOUR CALENDRIER'
, NOM_LOG_FIC                    CHAR(8) NO DEFAULT NOT NULL
HEADING 'NOM LOGIQUE FICHIER'
, NOM_SERV_CALC                  CHAR(15) NO DEFAULT NOT NULL
HEADING 'NOM SERVEUR CALC'
, NOM_SERV_FMP                   CHAR(15) NO DEFAULT NOT NULL
HEADING 'NOM SERVEUR FOURCHETTE MOYENNE PONDEREE'
, Z_TRAN_VAL_OV                  NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE TRANSACTION VALEUR OUVERTURE'
, Z_TRAN_VAL_SEA                 NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE TRANSACTION VALEUR SEANCE'
, Z_OM_ATN_AC                    NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE ACHAT EN FILE D''ATTENTE'
, Z_OM_ATN_VT                    NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE VENTE EN FILE D''ATTENTE'
, Z_OM_TOR_DCH_NON_XTE           NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE TOR DECL. NON-EXECUTE'
, Z_OM_SAI_POV                   NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE SAISI PREOUVERTURE'
, Z_OM_SAI_SEA                   NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE SAISI SEANCE'
, Z_OM_SUP_SMA_POV               NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE PURGE SURVEILLANCE PREOUVERTURE'
, Z_OM_SUP_SMA_SEA               NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE PURGE SURVEILLANCE SEANCE'
, Z_OM_XTE_PATL_OV               NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE EXECUTE PARTIEL OUVERTURE'
, Z_OM_XTE_PATL_SEA              NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE EXECUTE PARTIEL SEANCE'
, Z_OM_XTE_ETIE_OV               NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE EXECUTE ENTIER OUVERTURE'
, Z_OM_XTE_ETIE_SEA              NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE EXECUTE ENTIER SEANCE'
, Z_OM_SUP_POV                   NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE ELIMINE PREOUVERTURE'
, Z_OM_SUP_SEA                   NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE ELIMINE SEANCE'
, Z_OM_SUP_GEL_SEA               NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE ELIMINE GEL SEANCE'
, Z_OM_STOP_DCH                  NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE STOP ATTN DECLENCH.'
, Z_OM_TOR_CRN                   NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE ORDRE TOR  EN CARNET'
, N_DR_TRAN                      NUMERIC( 7, 0) NO DEFAULT NOT NULL
HEADING 'NUMERO DERNIERE TRANSACTION'
, H_IN_DR_OM                     timestamp(0) NO DEFAULT NOT NULL
HEADING 'HEURE ENTREE DERNIER ORDRE'
, I_SENS_OM_AMX_NREP             CHAR(1) NO DEFAULT NOT NULL
HEADING 'INDICATEUR SENS ORDRE AU MIEUX NON REPONDU'
, I_DIF_MAJ_FDM                  NUMERIC( 1, 0) NO DEFAULT NOT NULL
HEADING 'INDICATEUR DIFFUSION TOUTES MAJ FEUILLE DE MARCHE'
, P_PR_COT_VAL                   NUMERIC( 18, 7) NO DEFAULT NOT NULL
HEADING 'COURS PREMIER COTE VALEUR'
, I_PRS_TOR_DCH                  NUMERIC( 1, 0) NO DEFAULT NOT NULL
HEADING 'INDICATEUR PRESENCE TOR DECLENCHABLES'
, I_MAJ_P_COMP                   CHAR(1) NO DEFAULT NOT NULL
HEADING 'INDICATEUR MISE A JOUR COURS DE COMPENSATION'
, D_SETTLE                       DATE NO DEFAULT NOT NULL
HEADING 'SETTLE DATE'
, I_CA_VAR                       CHAR(1) NO DEFAULT NOT NULL
HEADING 'INDICATEUR CALCUL VARIATION'
, Q_MAX                          NUMERIC( 18, 0) NO DEFAULT NOT NULL
HEADING 'QUANTITE MAXIMALE'
, Q_MIN                          NUMERIC( 18, 0) NO DEFAULT NOT NULL
HEADING 'QUANTITE MINIMALE'
, Q_PAS_COT                      NUMERIC( 18, 7) NO DEFAULT NOT NULL
HEADING 'MONTANT PAS DE COTATION (MONTANT DU TICK)'
, I_ECH_COT                      CHAR(2) NO DEFAULT NOT NULL
HEADING 'INDEX ECHELON DE COTATION'
, FT_P_AFF                       CHAR(2) NO DEFAULT NOT NULL
HEADING 'FORMAT DU PRIX AFFICHE'
, Z_DEL_P_AFF                    NUMERIC( 2, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE DE DECIMALE DU PRIX AFFICHE'
, Z_INCR_MIN                     NUMERIC( 4, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE D''INCREMENT MINIMUN'
, D_EXPI                         timestamp(0) NO DEFAULT NOT NULL
HEADING 'DATE D''EXPIRATION'
, D_ACTIV                        timestamp(0) NO DEFAULT NOT NULL
HEADING 'DATE D''ACTIVATION'
, I_NB_OV_GRC                    NUMERIC( 2, 0) NO DEFAULT NOT NULL
HEADING 'NOMBRE D''OUVERTURE GROUPE'
, C_VAL_SPT                      CHAR(12) NO DEFAULT NOT NULL
HEADING 'CODE VALEUR SUPPORT'
, H_DR_COT_VAL                   timestamp NO DEFAULT
NOT NULL
HEADING 'HORAIRE DERNIER COTE VALEUR'
, PH_LAST_OM                     NUMERIC( 18, 7) NO DEFAULT NOT NULL
HEADING 'PLUS HAUT LAST ORDRE MARCHE'
, I_PH_LAST_OM                   CHAR(1) NO DEFAULT NOT NULL
HEADING 'INDICATEUR PLUS HAUT LAST ORDRE MARCHE'
, PB_LAST_OM                     NUMERIC( 18, 7) NO DEFAULT NOT NULL
HEADING 'PLUS BAS LAST ORDRE MARCHE'
, I_PB_LAST_OM                   CHAR(1) NO DEFAULT NOT NULL
HEADING 'INDICATEUR PLUS BAS LAST ORDRE MARCHE'
, P_DR_LAST_OM                   NUMERIC( 18, 7) NO DEFAULT NOT NULL
HEADING 'PRIX DERNIER LAST ORDRE MARCHE'
, I_P_DR_LAST_OM                 CHAR(1) NO DEFAULT NOT NULL
HEADING 'INDICATEUR PRIX DERNIER LAST ORDRE MARCHE'
, H_DR_LAST_OM                   timestamp NO DEFAULT
NOT NULL
HEADING 'HORAIRE DERNIER LAST ORDRE MARCHE'
, Y_ALGO_APPA_ORD                CHAR(1) DEFAULT 'F' NOT NULL
HEADING 'TYPE ALGORITHME APPARIEMENT ORDRE'
, I_FL_MAR                       CHAR(2) DEFAULT '  ' NOT NULL
HEADING 'INDICATEUR FLUX DE MARCHE'
, I_TOP_AC                       timestamp DEFAULT NULL
HEADING 'Buy TOP ORDER            '
, I_TOP_VT                       timestamp DEFAULT NULL
HEADING 'Sell TOP ORDER           '
, QTOTNGSEAVAL                   NUMERIC( 18, 7) NOT NULL
HEADING 'MONTANT TOTAL ECHANGE JOUR'
, NOMSERVLIM                     CHAR(15) NO DEFAULT NOT NULL
HEADING 'NOM SERVEUR LIMITES'
, QNMVMO                         NUMERIC( 18, 7) NOT NULL
HEADING 'MONTANT NOMINAL DE LA VALEUR MOBILIERE'
, AMUVALDRVWSE                   NUMERIC( 18, 7) NOT NULL
HEADING 'MULTIPLICATEUR VALEUR DERIVEE VARSOVIE'
, I_SPREAD_DST                   CHAR(1) DEFAULT '0' NOT NULL
HEADING 'INDICATEUR SPREAD DESINTERESSABLE'
, Y_ALGO_CA_P_LEG                CHAR(2) NOT NULL
HEADING 'TYPE ALGORITHME POUR CALCUL PRIX DEPATTES'
, I_DST_ACTIF                    CHAR(1) DEFAULT '0' NOT NULL
HEADING 'INDICATEUR  DESINTERESSEMENT ACTIF'
, Y_STG                          CHAR(2) DEFAULT '  ' NOT NULL
HEADING 'TYPE DE STRATEGIE'
, C_ID_ADC                       CHAR(8) DEFAULT ' ' NOT NULL
HEADING 'CODE IDENTIFIANT ADHERENT'
, C_ID_NG                        CHAR(8) DEFAULT ' ' NOT NULL
HEADING 'CODE NEGOCIATEUR'
, NSEQOMDR                       NUMERIC( 9, 0) NO DEFAULT NOT NULL
HEADING 'NUMERO SEQUENTIEL ORDRE (DERNIER)'
, QMAJB                          CHAR(8) NO DEFAULT NOT NULL
HEADING 'NOM LOGIQUE QUEUE MISE A JOUR BASE'
, P_BAND_VAR                     NUMERIC( 18, 7) NOT NULL
HEADING 'PRICE BANDING VARIATION'
, A_DR_MSG_LIM                   CHAR(216) NO DEFAULT NOT NULL
HEADING 'AGREGAT DERNIER MESSAGE LIMITE'
, NSEQOMDR1                      NUMERIC( 9, 0) NOT NULL
HEADING 'Host Order Number column 1'
, NSEQOMDR2                      NUMERIC( 9, 0) NOT NULL
HEADING 'Host Order Number column 2'
, NSEQOMDR3                      NUMERIC( 9, 0) NOT NULL
HEADING 'Host Order Number column 3'
, NSEQOMDR4                      NUMERIC( 9, 0) NOT NULL
HEADING 'Host Order Number column 4'
, NSEQOMDR5                      NUMERIC( 9, 0) NOT NULL
HEADING 'Host Order Number column 5'
, NSEQOMDR6                      NUMERIC( 9, 0) NOT NULL
HEADING 'Host Order Number column 6'
, NSEQOMDR7                      NUMERIC( 9, 0) NOT NULL
HEADING 'Host Order Number column 7'
, NSEQOMDR8                      NUMERIC( 9, 0) NOT NULL
HEADING 'Host Order Number column 8'
, NSEQOMDR9                      NUMERIC( 9, 0) NOT NULL
HEADING 'Host Order Number column 9'
, PRT_POINTS                     NUMERIC( 18, 7) NOT NULL
HEADING 'Protection Points'
, FALCON_PRT                     NUMERIC( 18, 7) NOT NULL
HEADING 'Falcon Protection Points'
, NO_BUST_RANGE                  NUMERIC( 18, 7) NOT NULL
HEADING 'No Bust Range'
, SPIKE_SECONDS                  NUMERIC( 7, 0) NOT NULL
HEADING 'Spike Seconds'
, SPIKE_COUNT                    NUMERIC( 7, 0) NOT NULL
HEADING 'Spike Reopen Count'
, SPARROW_FLAG                   CHAR(1) NOT NULL
HEADING 'Sparrow Flag'
) attributes extent (16,64);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """SELECT l_val ContractName,
c_val IntrumentID,
d_activ FirstTradeDate,
d_expi LastTradeDate,
p_rf SettlementPrice,
s_inte_pb LimitDownPrice,
s_inte_ph LimitUpPrice,
c_id_grc ProductCategory
FROM tval
ORDER BY l_val browse access;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """assertion""")
    #unexpect purge
    
    stmt = """control query default pos  reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default odbc_process reset;"""
    output = _dci.cmdexec(stmt)
    stmt = """control query default infer_charset reset;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)


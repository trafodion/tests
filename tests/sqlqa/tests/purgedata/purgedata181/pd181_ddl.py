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
    
    stmt = """create table pd181 ( C1 char(2) default '&' not null primary key, C2 char(1), C3  char(1), C4 char(1), C5 char(1), C6 char(1), C7 char(1), C8 char(1),
C9   char(1), C10  char(1), C11  char(1), C12  char(1), C13  char(1), C14  char(1), C15  char(1), C16  char(1), C17  char(1), C18  char(1), C19  char(1),
C20  char(1), C21  char(1), C22  char(1), C23  char(1), C24  char(1), C25  char(1), C26  char(1), C27  char(1), C28  char(1), C29  char(1), C30  char(1),
C31  char(1), C32  char(1), C33  char(1), C34  char(1), C35  char(1), C36  char(1), C37  char(1), C38  char(1), C39  char(1), C40  char(1), C41  char(1),
C42  char(1), C43  char(1), C44  char(1), C45  char(1), C46  char(1), C47  char(1), C48  char(1), C49  char(1), C50  char(1), C51  char(1), C52  char(1),
C53  char(1), C54  char(1), C55  char(1), C56  char(1), C57  char(1), C58  char(1), C59  char(1), C60  char(1), C61  char(1), C62  char(1), C63  char(1),
C64  char(1), C65  char(1), C66  char(1), C67  char(1), C68  char(1), C69  char(1), C70  char(1), C71  char(1), C72  char(1), C73  char(1), C74  char(1),
C75  char(1), C76  char(1), C77  char(1), C78  char(1), C79  char(1), C80  char(1), C81  char(1), C82  char(1), C83  char(1), C84  char(1), C85  char(1),
C86  char(1), C87  char(1), C88  char(1), C89  char(1), C90  char(1), C91  char(1), C92  char(1), C93  char(1), C94  char(1), C95  char(1), C96  char(1),
C97  char(1), C98  char(1), C99  char(1), C100  char(1), C101  char(1), C102  char(1), C103  char(1), C104  char(1), C105  char(1), C106  char(1),
C107  char(1), C108  char(1), C109  char(1), C110  char(1), C111  char(1), C112  char(1), C113  char(1), C114  char(1), C115  char(1), C116  char(1),
C117  char(1), C118  char(1), C119  char(1), C120  char(1), C121  char(1), C122  char(1), C123  char(1), C124  char(1), C125  char(1), C126  char(1),
C127  char(1), C128  char(1), C129  char(1), C130  char(1), C131  char(1), C132  char(1), C133  char(1), C134  char(1), C135  char(1), C136  char(1),
C137  char(1), C138  char(1), C139  char(1), C140  char(1), C141  char(1), C142  char(1), C143  char(1), C144  char(1), C145  char(1), C146  char(1),
C147  char(1), C148  char(1), C149  char(1), C150  char(1), C151  char(1), C152  char(1), C153  char(1), C154  char(1), C155  char(1), C156  char(1),
C157  char(1), C158  char(1), C159  char(1), C160  char(1), C161  char(1), C162  char(1), C163  char(1), C164  char(1), C165  char(1), C166  char(1),
C167  char(1), C168  char(1), C169  char(1), C170  char(1), C171  char(1), C172  char(1), C173  char(1), C174  char(1), C175  char(1), C176  char(1),
C177  char(1), C178  char(1), C179  char(1), C180  char(1), C181  char(1), C182  char(1), C183  char(1), C184  char(1), C185  char(1), C186  char(1),
C187  char(1), C188  char(1), C189  char(1), C190  char(1), C191  char(1), C192  char(1), C193  char(1), C194  char(1), C195  char(1), C196  char(1),
C197  char(1), C198  char(1), C199  char(1), C200  char(1), C201  char(1), C202  char(1), C203  char(1), C204  char(1), C205  char(1), C206  char(1),
C207  char(1), C208  char(1), C209  char(1), C210  char(1), C211  char(1), C212  char(1), C213  char(1), C214  char(1), C215  char(1), C216  char(1),
C217  char(1), C218  char(1), C219  char(1), C220  char(1), C221  char(1), C222  char(1), C223  char(1), C224  char(1), C225  char(1), C226  char(1),
C227  char(1), C228  char(1), C229  char(1), C230  char(1), C231  char(1), C232  char(1), C233  char(1), C234  char(1), C235  char(1), C236  char(1),
C237  char(1), C238  char(1), C239  char(1), C240  char(1), C241  char(1), C242  char(1), C243  char(1), C244  char(1), C245  char(1), C246  char(1),
C247  char(1), C248  char(1), C249  char(1), C250  char(1), C251  char(1), C252  char(1), C253  char(1), C254  char(1), C255  char(1), C256  char(1),
C257  char(1), C258  char(1), C259  char(1), C260  char(1), C261  char(1), C262  char(1), C263  char(1), C264  char(1), C265  char(1), C266  char(1),
C267  char(1), C268  char(1), C269  char(1), C270  char(1), C271  char(1), C272  char(1), C273  char(1), C274  char(1), C275  char(1), C276  char(1),
C277  char(1), C278  char(1), C279  char(1), C280  char(1), C281  char(1), C282  char(1), C283  char(1), C284  char(1), C285  char(1), C286  char(1),
C287  char(1), C288  char(1), C289  char(1), C290  char(1), C291  char(1), C292  char(1), C293  char(1), C294  char(1), C295  char(1), C296  char(1),
C297  char(1), C298  char(1), C299  char(1), C300  char(1), C301  char(1), C302  char(1), C303  char(1), C304  char(1), C305  char(1), C306  char(1),
C307  char(1), C308  char(1), C309  char(1), C310  char(1), C311  char(1), C312  char(1), C313  char(1), C314  char(1), C315  char(1), C316  char(1),
C317  char(1), C318  char(1), C319  char(1), C320  char(1), C321  char(1), C322  char(1), C323  char(1), C324  char(1), C325  char(1), C326  char(1),
C327  char(1), C328  char(1), C329  char(1), C330  char(1), C331  char(1), C332  char(1), C333  char(1), C334  char(1), C335  char(1), C336  char(1),
C337  char(1), C338  char(1), C339  char(1), C340  char(1), C341  char(1), C342  char(1), C343  char(1), C344  char(1), C345  char(1), C346  char(1),
C347  char(1), C348  char(1), C349  char(1), C350  char(1), C351  char(1), C352  char(1), C353  char(1), C354  char(1), C355  char(1), C356  char(1),
C357  char(1), C358  char(1), C359  char(1), C360  char(1), C361  char(1), C362  char(1), C363  char(1), C364  char(1), C365  char(1), C366  char(1),
C367  char(1), C368  char(1), C369  char(1), C370  char(1), C371  char(1), C372  char(1), C373  char(1), C374  char(1), C375  char(1), C376  char(1),
C377  char(1), C378  char(1), C379  char(1), C380  char(1), C381  char(1), C382  char(1), C383  char(1), C384  char(1), C385  char(1), C386  char(1),
C387  char(1), C388  char(1), C389  char(1), C390  char(1), C391  char(1), C392  char(1), C393  char(1), C394  char(1), C395  char(1), C396  char(1),
C397  char(1), C398  char(1), C399  char(1), C400  char(1), C401  char(1), C402  char(1), C403  char(1), C404  char(1), C405  char(1), C406  char(1),
C407  char(1), C408  char(1), C409  char(1), C410  char(1), C411  char(1), C412  char(1), C413  char(1), C414  char(1), C415  char(1), C416  char(1),
C417  char(1), C418  char(1), C419  char(1), C420  char(1), C421  char(1), C422  char(1), C423  char(1), C424  char(1), C425  char(1), C426  char(1),
C427  char(1), C428  char(1), C429  char(1), C430  char(1), C431  char(1), C432  char(1), C433  char(1), C434  char(1), C435  char(1), C436  char(1),
C437  char(1), C438  char(1), C439  char(1), C440  char(1), C441  char(1), C442  char(1), C443  char(1), C444  char(1), C445  char(1), C446  char(1),
C447  char(1), C448  char(1), C449  char(1), C450  char(1), C451  char(1), C452  char(1), C453  char(1), C454  char(1), C455  char(1), C456  char(1),
C457  char(1), C458  char(1), C459  char(1), C460  char(1), C461  char(1), C462  char(1), C463  char(1), C464  char(1), C465  char(1), C466  char(1),
C467  char(1), C468  char(1), C469  char(1), C470  char(1), C471  char(1), C472  char(1), C473  char(1), C474  char(1), C475  char(1), C476  char(1),
C477  char(1), C478  char(1), C479  char(1), C480  char(1), C481  char(1), C482  char(1), C483  char(1), C484  char(1), C485  char(1), C486  char(1),
C487  char(1), C488  char(1), C489  char(1), C490  char(1), C491  char(1), C492  char(1), C493  char(1), C494  char(1), C495  char(1), C496  char(1),
C497  char(1), C498  char(1), C499  char(1), C500  char(1));"""
    output = _dci.cmdexec(stmt)

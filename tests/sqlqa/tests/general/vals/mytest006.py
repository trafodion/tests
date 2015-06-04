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

# test006
# JClear
# 1999-04-14
# VALUES tests: 100 rows in a values statement
#
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
    stmt = """values
(923.65, 'Fxmvocr', timestamp '2024-06-19 13:17:41'),
(11795.43, 'Uwvv', timestamp '1957-08-25 16:29:53'),
(7171.04, 'Vwqacxkwxg', timestamp '1951-12-25 14:46:51'),
(11873.74, 'Xqrqhi', timestamp '1991-04-21 13:16:15'),
(3692.46, 'Sxkgsyerw', timestamp '1977-01-15 06:32:36'),
(26522.12, 'Zbyajnobt', timestamp '1964-01-03 07:31:22'),
(21008.20, 'Sfikn', timestamp '2038-05-15 09:34:04'),
(28353.61, 'Pnquefgpt', timestamp '1986-01-28 19:01:17'),
(22875.70, 'Xmfkhagnqa', timestamp '1985-07-29 00:48:37'),
(12550.63, 'Gesdsmnhsn', timestamp '1996-07-16 16:38:52'),
(1614.22, 'Zhoklxqjx', timestamp '1985-03-07 15:51:43'),
(16555.42, 'Llhdubrwo', timestamp '2003-11-24 13:31:10'),
(17903.77, 'Xsfxkyif', timestamp '1970-05-27 12:46:12'),
(6851.81, 'Lyjxi', timestamp '2022-02-17 20:31:53'),
(18819.34, 'Oxvoc', timestamp '1971-04-11 01:17:21'),
(15091.25, 'Wwbuseltha', timestamp '1991-08-15 22:35:47'),
(1656.74, 'Eqhtauac', timestamp '1957-04-02 12:23:27'),
(23388.89, 'Bhwsbdouxm', timestamp '2038-10-26 08:00:04'),
(23526.24, 'Qtg', timestamp '2015-10-18 20:51:54'),
(9331.45, 'Ria', timestamp '2037-06-25 17:01:40'),
(19552.22, 'Twgpgu', timestamp '2017-08-17 17:24:54'),
(29185.31, 'Qgwxah', timestamp '2037-08-26 08:47:57'),
(31841.19, 'Kw', timestamp '1999-01-16 01:36:35'),
(25349.98, 'Mqnnah', timestamp '1998-03-24 13:01:47'),
(25179.84, 'Emkpkkjvl', timestamp '1989-10-01 21:01:16'),
(1335.08, 'Iamlmoe', timestamp '2032-12-03 04:01:59'),
(21911.17, 'Tfkmdkdma', timestamp '1975-11-25 20:00:48'),
(20092.42, 'Mbbtp', timestamp '1969-08-18 13:54:24'),
(8313.29, 'Ipjulups', timestamp '1965-12-30 19:40:35'),
(3708.44, 'Crxwgu', timestamp '1990-02-21 09:57:44'),
(10518.48, 'Xicrhe', timestamp '1963-03-03 04:32:59'),
(1187.69, 'Wblh', timestamp '2036-01-11 16:02:50'),
(9872.18, 'Dvhkr', timestamp '1999-11-21 18:32:22'),
(28956.98, 'Pen', timestamp '2008-05-25 00:11:36'),
(16661.45, 'Bkrurn', timestamp '1995-09-29 07:40:58'),
(12541.05, 'Cjh', timestamp '1982-02-08 03:02:49'),
(16350.82, 'Ajqvv', timestamp '2015-10-10 22:51:26'),
(16782.09, 'Vinatbjoob', timestamp '1992-12-24 08:20:01'),
(2529.14, 'Cwyfp', timestamp '1977-08-06 03:59:05'),
(14813.69, 'Mfysneq', timestamp '2007-05-04 11:36:38'),
(26602.03, 'Dwvrbtg', timestamp '1988-09-24 13:27:30'),
(17162.08, 'Knwputml', timestamp '1976-11-28 19:26:11'),
(12200.94, 'Bmpi', timestamp '2011-11-06 05:49:23'),
(2385.07, 'Xnx', timestamp '1984-09-14 07:10:26'),
(4722.22, 'Kvdi', timestamp '1971-08-12 21:40:46'),
(8912.03, 'Mjefjmo', timestamp '1982-10-15 17:02:23'),
(23061.13, 'Abgcqob', timestamp '1986-07-05 13:04:52'),
(8449.28, 'Yaei', timestamp '2007-03-18 09:00:19'),
(24096.71, 'Whnjxxowdf', timestamp '1969-08-22 04:58:45'),
(437.40, 'Hqclx', timestamp '1981-11-15 05:40:56'),
(18853.29, 'Jqyowmkg', timestamp '2002-07-24 17:37:57'),
(291.71, 'Wbasvgs', timestamp '2017-12-06 05:32:17'),
(4146.27, 'Gkj', timestamp '1974-04-22 11:59:53'),
(4472.27, 'Wyqny', timestamp '1995-04-08 21:28:27'),
(16952.76, 'Lljfanwbuh', timestamp '2029-12-06 02:44:28'),
(9267.43, 'Efwhuin', timestamp '2036-09-10 21:53:45'),
(26072.17, 'Wfwcypyima', timestamp '1976-08-12 13:50:54'),
(10857.49, 'Cqujymlpb', timestamp '2011-02-28 22:58:07'),
(15503.48, 'Mtmcx', timestamp '2021-03-26 06:54:13'),
(10882.22, 'Zmd', timestamp '2010-01-10 19:26:32'),
(12905.56, 'Vhf', timestamp '1995-03-01 21:13:10'),
(30888.26, 'Dlgpooqj', timestamp '1962-04-18 20:18:30'),
(12416.93, 'Ifpcjnnwuv', timestamp '1987-04-18 12:59:13'),
(16403.94, 'Tmurodtxua', timestamp '2026-07-09 18:51:18'),
(13932.74, 'Vipfie', timestamp '1975-05-28 07:04:38'),
(6996.09, 'Fxyhvqm', timestamp '1990-07-05 15:01:32'),
(32384.50, 'Ylatgitor', timestamp '1960-02-22 21:55:17'),
(24550.23, 'Gqqy', timestamp '2035-06-14 01:51:33'),
(1954.05, 'Uhdhb', timestamp '2026-10-02 08:10:52'),
(20474.84, 'Mucoswsna', timestamp '2026-06-17 05:46:40'),
(11184.05, 'Vfhigtqc', timestamp '2025-01-30 03:32:37'),
(5860.11, 'Ayvbjool', timestamp '1989-10-25 21:55:27'),
(27016.23, 'Fcilpg', timestamp '2008-05-27 00:45:52'),
(8471.82, 'Agdygpnlu', timestamp '1959-02-20 21:14:27'),
(9594.86, 'Clijxy', timestamp '2005-03-27 14:48:54'),
(13697.48, 'Rl', timestamp '1972-04-30 08:27:30'),
(16564.36, 'Ixqvif', timestamp '1971-03-31 06:35:31'),
(5087.14, 'Nswvyrdit', timestamp '1971-10-31 22:41:48'),
(18355.58, 'Ocbht', timestamp '1966-11-28 03:15:29'),
(23164.98, 'Of', timestamp '1993-01-06 19:54:13'),
(17819.62, 'Zpa', timestamp '2026-10-14 15:59:42'),
(19488.32, 'Yy', timestamp '1998-10-22 13:34:51'),
(17864.71, 'Fncjqbqg', timestamp '1955-04-26 06:01:46'),
(14127.12, 'Uqxddhewg', timestamp '2016-06-23 14:51:54'),
(10711.66, 'Eocltisy', timestamp '1978-04-20 13:08:31'),
(9282.65, 'Lpx', timestamp '1987-01-25 10:43:03'),
(30200.78, 'Hnnau', timestamp '1980-08-06 01:26:42'),
(10975.56, 'Ygjfia', timestamp '1966-07-20 14:59:01'),
(7749.79, 'Zrrc', timestamp '1962-07-23 19:43:49'),
(32151.52, 'Ehxolx', timestamp '1994-12-29 07:35:58'),
(4730.84, 'Vfjxj', timestamp '2032-08-18 19:38:26'),
(18947.78, 'Dkxdvvfsn', timestamp '2025-09-29 12:33:04'),
(10291.98, 'Tcoyaji', timestamp '2038-03-24 10:50:06'),
(846.70, 'Wddnaj', timestamp '1997-09-04 05:25:34'),
(11463.49, 'Qwejs', timestamp '1957-10-13 09:43:49'),
(22949.36, 'Ehui', timestamp '1959-11-11 09:17:23'),
(24008.33, 'Lq', timestamp '1993-12-27 02:32:16'),
(26728.22, 'Pv', timestamp '1982-08-02 14:01:21'),
(21758.47, 'Ycptpwaw', timestamp '1975-04-04 20:27:06'),
(9382.26, 'Jsw', timestamp '2033-11-01 06:12:24');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/test006.exp""", """test006a""")
    
    # expect 100 rows selected
    

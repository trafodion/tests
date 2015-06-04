# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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

import sys
import re
import inspect
import os
import fcntl
import subprocess 
import datetime
import time
import signal
import optparse
import multiprocessing
import gvars
import copy_reg
import types
import threading
import shutil
import ConfigParser

#----------------------------------------------------------------------------
# The following code is necessary for multiprocess to work in a class like
# HPTestMgr.  Otherwise when you start multiple processes, you will run into
# 'pickle' error due to the mingled class function name.  In order for
# __mro__ (Method Resolution Order) to work in the following code, HPTestMgr
# also needs to inherit from object.
#----------------------------------------------------------------------------
def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    if func_name.startswith('__') and not func_name.endswith('__'):
        #deal with mangled names
        cls_name = cls.__name__.lstrip('_')
        func_name = '_%s%s' % (cls_name, func_name)
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    if obj and func_name in obj.__dict__:
        cls, obj = obj, None # if func_name is classmethod
    for cls in cls.__mro__:
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
    return func.__get__(obj, cls)

copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)

#----------------------------------------------------------------------------
# A function (or a structure in C's sense) that contains all variables
# recording user's command-line parameters.
#----------------------------------------------------------------------------
def ArgList():
    _target = None
    _user = None
    _pw = None
    _role = None
    _dbroot_user = None
    _dbroot_pw = None
    _dbroot_role = None
    _dsn = None
    _java = None
    _jdbc_classpath = None
    _hpdci_classpath = None
    _results_dir = None
    _qalib_dir = None
    _use_sqlci = None
    _target_type = None

#----------------------------------------------------------------------------
# A class that implements all HPDCI process related functions, including
# some of the DFM-style helper functions.
#----------------------------------------------------------------------------
class HPDci:
    """Implmentation for hpdci related functions"""

    _proc_name = ''
    _testmgr = None
    _target = ''
    _dsn = ''
    _user = ''
    _pw = ''
    _role = ''
    _dbroot_user = ''
    _dbroot_pw = ''
    _dbroot_role = ''
    _hpipe = None
    _prompt_str = None
    _sqlci_prompt_str = '>>'
    _hpdci_prompt_str = 'SQL>'

    def __init__(self, name, testmgr):
       self._proc_name = name
       self._testmgr = testmgr

    #------------------------------------------------------------------------
    # Basic HPDCI functions, such as connect/disconnect/issue stmt and read
    # the results back.
    #------------------------------------------------------------------------
    # Make an HPDCI connection
    def connect(self, target, dsn, user, pw, role=''):
        self._target = target
        self._dsn = dsn
        self._user = user
        self._pw = pw
        self._role = role
        sqlci_unreg_user_str1 = 'ERROR[8732] User'
        sqlci_unreg_user_str2 = 'is not a registered database user'

        if ArgList._use_sqlci:
            # use sqlci

            # Make sure $MY_SQROOT is set.
            output = self._testmgr.shell_call('echo $MY_SQROOT').strip()
            if not output:
                raise RuntimeError('$MY_SQROOT is not set, run sqenv.sh from your installation root first.')

            self._prompt_str = self._sqlci_prompt_str
            cmd = 'sqlci'
            if self._user != None:
                cmd += (' -u ' + self._user)
        else:
            # use hpdci
            self._prompt_str = self._hpdci_prompt_str
            classpath = '.:' + ArgList._jdbc_classpath + ':' + ArgList._hpdci_classpath
            if tgtSQ():
                cmd = ArgList._java + ' -classpath ' + classpath + ' com.hp.hpdci.UserInterface -h ' + self._target + ' -dsn ' + self._dsn + ' -u ' + self._user + ' -p ' + self._pw
            elif tgtTR():
                cmd = ArgList._java + ' -classpath ' + classpath + ' org.trafodion.ci.UserInterface -h ' + self._target + ' -u ' + self._user + ' -p ' + self._pw
            if self._role == '':
                cmd += ' -r \'\''
            else:
                cmd = cmd + ' -r ' + self._role

        ON_POSIX = 'posix' in sys.builtin_module_names
        self._hpipe = subprocess.Popen(cmd, stdin=subprocess.PIPE,
          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          bufsize=1, close_fds=ON_POSIX, shell=True)

        # Change to non-blocking mode, so read returns even if there is no data.
        # this happens after the prompt SQL> shows up.
        fcntl.fcntl(self._hpipe.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

        # consume header message
        out = self.read_until_next_prompt()
        # Check the unregistered user error from sqlci.  Even though
        # sqlci continues if -u <user> is not a registered user.  The test
        # should error out so that it is not run under the wrong user.
        # We can't check this error condition in read_until_next_prompt()
        # as some tests may test this as a negative test, so do this right
        # after the header message is displayed.
        if ArgList._use_sqlci and \
           sqlci_unreg_user_str1 in out and \
           sqlci_unreg_user_str2 in out:
           raise RuntimeError('unregistered user ' + self._user)

    # Disconnect from HPDCI
    def disconnect(self):
        if not self._hpipe:
            return

        # issue an exit command
        self.issue_stmt('exit;')
        self._hpipe.kill()

    # Issue a statement to hpdci
    def issue_stmt(self, stmt):
        # self._tstmgr.log_write(self._prompt_str + stmt)
        if ArgList._use_sqlci and self._proc_name == 'SQL':
            self._testmgr.log_write('>>' + stmt)
        else:       
            self._testmgr.log_write(self._proc_name + '>' + stmt)
        # strip trailing whitespace
        stmt = stmt.lstrip()
        stmt += '\n'
        # print ">>>", stmt
        self._hpipe.stdin.write(stmt)
        self._hpipe.stdin.flush()

    # Keep reading until the next prompt. Data returned does not include the
    # prompt.
    def read_until_next_prompt(self):
        buf_flush_threshold = 5 # sec
        buf = ''
        log_buf = ''
        same_buf = False
        # when a cmd like 'connect <usr id>/<pass>' failed, this is the 
        # prompt for you to retry.  We will send a ^C when seeing this.
        user_authen_str = 'User Name:'
        # when ^C is issued to a command, this is the prompt for you to hit 
        # <Enter> and go back to the DCI prompt.
        cmd_interrupted_str = 'Command Interrupted - Please hit <Enter> ...'
        # hpdci connection refused message (often happens with wrong port 
        # number)
        conn_refused_str = 'ERROR[29113] error while opening socket. Cause: Connection refused'
        # hpdci connection timeout message (often happens with wrong IP addr)
        conn_timeout_str = 'ERROR[29113] error while opening socket. Cause: Connection timed out'
        # hpdci connection reset message
        conn_reset_str = ' ERROR[29115] error while reading from socket. Cause: Connection reset' 
        # The following 2 are seen together for wrong user id or password for
        # HPDCI connection.  We basically issue a ^C when asked about 
        # 'User Name:' and then
        # 'Existing HP Database Command Interface - Please hit <Enter> ...' 
        # shows up.
        authen_err_str = 'ERROR[8837] CLI Authentication'
        hpdci_exit_str = 'Exiting HP Database Command Interface'

        start_time = time.time()

        while True:
            try:
                thisbuf = self._hpipe.stdout.read()
            except IOError: # there is no data
                # this is the regular "SQL>" prompt, we are done and return.
                if len(buf) >= len(self._prompt_str) and \
                   buf[len(buf)-len(self._prompt_str):] == self._prompt_str:
                       buf = buf[:len(buf)-len(self._prompt_str)]
                       log_buf = log_buf[:len(log_buf)-len(self._prompt_str)]
                       self._testmgr.log_write(log_buf)
                       log_buf = ''
                       return buf
                elif not same_buf:
                    # deal with other special prompts.
                    s = buf.strip()

                    # send a CTRL^C over when being asked about user name,
                    # password, etc.
                    if len(s) >= len(user_authen_str) and \
                       s[len(s)-len(user_authen_str):] \
                       == user_authen_str:
                        self._hpipe.send_signal(signal.SIGINT)
                        same_buf = True

                    # send a newline over when the command has been ^C'ed and
                    # HPDci is asking the user to hit <enter> to go back to
                    # the HPDci prompt.
                    elif len(s) >= len(cmd_interrupted_str) and \
                         s[len(s)-len(cmd_interrupted_str):] \
                         == cmd_interrupted_str:
                        self._hpipe.stdin.write('\n')
                        self._hpipe.stdin.flush()
                        # For some reaon, the prompt gets all screwed-up
                        # if we don't wait for a little bit here.  Sleep
                        # for 10 secs.
                        time.sleep(10)
                        same_buf = True

                    elif conn_refused_str in buf:
                        self._testmgr.log_write(log_buf)
                        log_buf = ''
                        raise RuntimeError('connection refused')
                    elif conn_timeout_str in buf:
                        self._testmgr.log_write(log_buf)
                        log_buf = ''
                        raise RuntimeError('connection time out')
                    elif conn_reset_str in buf:
                        self._testmgr.log_write(log_buf)
                        log_buf = ''
                        raise RuntimeError('connection reset')
                    elif authen_err_str in buf and \
                         hpdci_exit_str in buf:
                        self._testmgr.log_write(log_buf)
                        log_buf = '' 
                        raise RuntimeError('CLI authentication error')
                    else:
                        # flush out the buffer once we reach the threadhold.
                        # This way we can at least tell what the last message
                        # is even when it hangs.
                        elapsed_sec = time.time() - start_time
                        if elapsed_sec > buf_flush_threshold and log_buf != '':
                            self._testmgr.log_write(log_buf)
                            log_buf = ''
                            same_buf = True
            else:
                # there is data
                # strip all of the leading '+>'s.
                #  ^ leadning
                # (\+>) the string '+>' to strip. + is a special char, hence \
                # + 1 or more times
                if (len(thisbuf) > 0):
                    # print '<<<' + thisbuf + '<<<'
                    buf += re.sub('^(\+>)+','', thisbuf)
                    log_buf += re.sub('^(\+>)+','', thisbuf)
                    same_buf = False

    # Execute a statement and return the output in string form
    def cmdexec(self, stmt):
        if tgtTR():
            # Any unsupported statements that would cause damange go here.
            # They will be skipped.
            stmts_to_skip = []
            for s in stmts_to_skip:
                if stmt.lower().strip().startswith(s):
                    return '\n--- SQL operation complete. [Test engine did not issue this unsupported stmt in TRAF]\n\n'

        # TODO: This is temp workaround.  "create trigger" hangs if run
        # from hpdci, unless you add / to the next line after the command.
        # address this workaound here so that we don't have to deal with
        # changing them in the test.
        tokens = stmt.split()
        if len(tokens) >= 2 and tokens[0].lower() == 'create' and tokens[1].lower() == 'trigger':
            stmt += '\n/'
        retry_tmf_err97 = 0
        retry_tmf_err73 = 0
        while (True):
            self.issue_stmt(stmt)
            buf = self.read_until_next_prompt()
            # See if the error needs to be retried.
            if 'ERROR' in buf and 'TMF' in buf and 'error 97' in buf:
                # retry up to 10 times for TMF error 97.
                retry_tmf_err97 += 1
                if (retry_tmf_err97 < 10):
                    self._testmgr.log_write('INFO: Retrying the stmt for TMF error 97: ' + str(retry_tmf_err97) + ' time(s).\n')
                    continue
                else:
                    self._testmgr.log_write('INFO: Retrying TMF error 97 for 10 times with no luck.  Give up.\n')
                    return buf
            elif 'ERROR' in buf and 'TMF' in buf and 'error 73' in buf:
                # retry up to 10 times for TMF error 97.
                retry_tmf_err73 += 1
                if (retry_tmf_err73 < 10):
                    self._testmgr.log_write('INFO: Retrying the stmt for TMF error 73: ' + str(retry_tmf_err73) + ' time(s).\n')
                    continue
                else:
                    self._testmgr.log_write('INFO: Retrying TMF error 73 for 10 times with no luck.  Give up.\n')
                    return buf

            # If there is need to retry, return here. 
            return buf
                

    #------------------------------------------------------------------------
    # DFM-style functions to support legacy DFM tests
    #------------------------------------------------------------------------
    # Prepare a Python regex string using a DFM style regex string.
    def convert_dfm_regex(self, string):
        # DFM supports 3 special characters:
        # "*" was    '[a-zA-Z0-9]*' any number of alphanumeric chars
        #     is now '.*'           the rule is relaxed to any number of chars
        # "?" was    '[a-zA-Z0-9]'  one alphanumeric character
        #     new    '.{1}'         the rule is relaxed to any 1 char
        # "%" -> [0-9]              one numeric char
        # "\\" -> "\\"              this really is \, but we need to keep \\
        #                           for regex as well.  No change needed
        s = string
        s = re.escape(s) #escape everything but alpha numeric chacaters

        # these were originally escaped DFM special chars \*, \?, and \?, 
        # emporary rename them to known strings so that they don't get
        # replaced by the next step.
        esc_star = 'this_is_my_dfm_temp_escaped_star'
        esc_question_mark =  'this_is_my_dfm_temp_escaped_question_mark'
        esc_percent_sign = 'this_is_my_dfm_temp_escaped_percent_sign'
        s = s.replace(re.escape('\*'), esc_star)
        s = s.replace(re.escape('\?'), esc_question_mark)
        s = s.replace(re.escape('\%'), esc_percent_sign)

        # replace the non-espcaed DFM special chars
        # s = s.replace(re.escape('*'), '[_a-zA-Z0-9]*')
        s = s.replace(re.escape('*'), r'.*')
        # s = s.replace(re.escape('?'), '[_a-zA-Z0-9]')
        s = s.replace(re.escape('?'), r'.{1}')
        s = s.replace(re.escape('%'), '[0-9]')

        # replace the escaped ones back
        s = s.replace(esc_star, re.escape('\*'))
        s = s.replace(esc_question_mark, re.escape('\?'))
        s = s.replace(esc_percent_sign, re.escape('\%'))

        return s

    # Similar to DFM #expectfile
    def expect_file(self, output, filename, section):
        recording = False
        found = False
        exp_content = ''
        # Append the target type to the exp file as different target type
        # often has different spaces, etc.       
        filename = filename + '.' + ArgList._target_type

        # if file does not exist, create one, otherwise open it
        fd = open(filename, 'a+')
        for line in fd:
            if recording:
                if line.startswith("<section_end>"):
                    break
                else:
                    exp_content += line      
            if line.startswith("<section_begin>"):
                list = line.split()
                if list[1] == section: 
                    recording = True
                    found = True

        # section exists 
        if found:
            output_list = output.splitlines()
            expect_list = exp_content.splitlines()
            group_output = []
            group_expect = []
            group_recording = False
            output_idx = 0
            expect_idx = 0
            while output_idx < len(output_list) and \
                  expect_idx < len(expect_list):
                output_line = output_list[output_idx]
                expect_line = expect_list[expect_idx]
                if group_recording:
                    if expect_line.startswith('<group_end>'):
                        group_recording = False
                        expect_idx += 1
                        for i in group_output:
                            found_group_match_line = False
                            idx = 0
                            for j in group_expect:
                                if i == j or \
                                    re.compile(self.convert_dfm_regex(\
                                      j)).match(i):
                                    found_group_match_line = True
                                    # delete this line so that we don't 
                                    # double match it for another line
                                    del group_expect[idx]
                                    break
                                idx += 1
                            if not found_group_match_line:
                                self._testmgr.mismatch_record('expect file: ' + \
                                os.path.basename(filename) + \
                                ' \"<section_begin>  ' + section + \
                                '\" <group_begin> \n  line: ' + i + \
                                '\n  not found in the group.')
                    else:
                        group_output.append(output_line)
                        group_expect.append(expect_line)
                        output_idx += 1
                        expect_idx += 1
                elif expect_line.startswith("<group_begin>"):
                    group_recording = True
                    expect_idx += 1
                else:
                    if output_line != expect_line and \
                       not re.compile(self.convert_dfm_regex(\
                           expect_line)).match(output_line):
                        self._testmgr.mismatch_record('expect file: ' + \
                            os.path.basename(filename) + \
                            ' \"<section_begin>  ' + section + \
                            '\"\n    expected: ' + expect_line + \
                            '\n    found   : ' + output_line)
                    output_idx += 1
                    expect_idx += 1
        else:
            self._testmgr.log_write('INFO: Section ' + section + \
                ' not found in ' + filename + '. New one created.\n')
            self._testmgr.local_deferred_count_increase()
            # DFM has two white spaces between <section_begin> and name
            fd.write('<section_begin>  ' + section + '\n')
            fd.write(output)
            fd.write('<section_end>\n')

        fd.close()

    # Well, using #expectplan in DFM is just a test badly written.  You 
    # should look for a certain operator in the plan if you need to.  But
    # if you absolutely needs to use it.  Here you have it, it is the same
    # as expect_file() and a plan mismatch is counted as a failed test 
    # instead of failed plan (we don't have such a thing) now.
    def expect_plan(self, output, filename, section):
       return self.expect_file(output, filename, section)

    # Expect a token.  A token is a string bracketed by 'white space(s)'
    def expect_str_token(self, output, token):
        items = output.split()
        found = False
        for t in items:
            if t == token:
                found = True
                break
        if not found:
            self._testmgr.mismatch_record(token)

    # Similar to DFM #expect any
    def expect_any_substr(self, output, msg, caseInsensitive=False):
        if caseInsensitive:
            msg1 = msg.lower()
            output1 = output.lower()
        else:
            msg1 = msg
            output1 = output

        if msg1 not in output1 and \
           not re.compile(self.convert_dfm_regex(msg1)).search(output1):
            self._testmgr.mismatch_record(msg)

    # Similar to DFM #unexpect any
    def unexpect_any_substr(self, output, msg, caseInsensitive=False):
        if caseInsensitive:
            msg1 = msg.lower()
            output1 = output.lower()
        else:
            msg1 = msg
            output1 = output

        if msg1 in output1 or \
           re.compile(self.convert_dfm_regex(msg1)).search(output1):
            self._testmgr.mismatch_record(msg, True)

    # Unexpecting error msg.
    def unexpect_error_msg(self, output, numstr=None):
        # For now, count the unsupported feature passed
        if self.ignore_unsupported_cmd(output):
            return

        if numstr == None:
            msg = '*** ERROR'
        else:
            msg = '*** ERROR[' + numstr + ']'
        if msg in output:
            self._testmgr.mismatch_record(msg, True)

    # Unexpecting warning msg.
    def unexpect_warning_msg(self, output, numstr=None):
        if numstr == None:
            msg = '*** WARNING'
        else:
            msg = '*** WARNING[' + numstr + ']'
        if msg in output:
            self._testmgr.mismatch_record(msg, True)

    # temporary ignoring unsupported commands
    def ignore_unsupported_cmd(self, output):
        # For now, count the unsupported feature passed
        if tgtTR():
            if 'ERROR[4222]' in output:
                return True
        return False

    # Similar to DFM $SQL_complete_msg()
    def expect_complete_msg(self, output):
        # For now, count the unsupported feature passed
        if self.ignore_unsupported_cmd(output):
            return
 
        msg = '--- SQL operation complete.'
        if msg not in output:
            self._testmgr.mismatch_record(msg)

    # Similar to DFM $SQL_prepared_msg()
    def expect_prepared_msg(self, output):
        msg = '--- SQL command prepared.'
        if msg not in output:
            self._testmgr.mismatch_record(msg)

    # Similar to DFM $SQL_inserted_msg()
    def expect_inserted_msg(self, output, num=None):
        if num == None:
            msg = ' row(s) inserted.'
        else:
            msg = '--- ' + str(num) + ' row(s) inserted.'
        if msg not in output:
            self._testmgr.mismatch_record(msg)

    # Similar to DFM $SQL_deleted_msg()
    def expect_deleted_msg(self, output, num=None):
        if num == None:
            msg = ' row(s) deleted.'
        else:
            msg = '--- ' + str(num) + ' row(s) deleted.'
        if msg not in output:
            self._testmgr.mismatch_record(msg)

    # Similar to DFM $SQL_updated_msg()
    def expect_updated_msg(self, output, num=None):
        if num == None:
            msg = ' row(s) updated.'
        else:
            msg = '--- ' + str(num) + ' row(s) updated.'
        if msg not in output:
            self._testmgr.mismatch_record(msg)

    # Similar to DFM $SQL_selected_msg() 
    def expect_selected_msg(self, output, num=None):
        if num == None:
            msg = ' row(s) selected.'
        else:
            msg = '--- ' + str(num) + ' row(s) selected.'
        if msg not in output:
            self._testmgr.mismatch_record(msg)

    # Similar to DFM $SQL_purged_msg()
    def expect_purged_msg(self, output):
        msg = 'OBJECT(S) PURGED'
        if msg not in output: 
            self._testmgr.mismatch_record(msg)

    # Similar to DFM $SQL_duplicated_msg()
    def expect_duplicated_msg(self, output):
        msg = 'OBJET(S) DUPLICATED'
        if msg not in output:
            self._testmgr.mismatch_record(msg)

    # New message for data loader written in python
    def expect_loaded_msg(self, output):
        msg = 'Status: Table loaded'
        if msg not in output:
            self._testmgr.mismatch_record(msg)

    # Expecting any error msg.
    def expect_error_msg(self, output, numstr=None):
        # For now, count the unsupported feature passed
        if self.ignore_unsupported_cmd(output):
            return

        if numstr == None:
            msg = '*** ERROR'
        else:
            msg = '*** ERROR[' + numstr + ']'
        if msg not in output:
            self._testmgr.mismatch_record(msg)

    # Expecting any error msg.
    def expect_warning_msg(self, output, numstr=None):
        # For now, count the unsupported feature passed
        if self.ignore_unsupported_cmd(output):
            return

        if numstr == None:
            msg = '*** WARNING'
        else:
            msg = '*** WARNING[' + numstr + ']'
        if msg not in output:
            self._testmgr.mismatch_record(msg)

    #------------------------------------------------------------------------
    # Misc helper functions
    #------------------------------------------------------------------------
    # Turn on the CQD that shows all external/internal CQDs
    def showcontrol_showall_on(self):
        if tgtSQ():
            output = self.cmdexec("""control query default showcontrol_unexternalized_attrs 'on';""")
        elif tgtTR():
            output = self.cmdexec("""control query default showcontrol_show_all 'on';""")

    # Reset (off) the CQD that shows all external/internal CQDs
    def showcontrol_showall_reset(self):
        if tgtSQ():
            output = self.cmdexec("""control query default showcontrol_unexternalized_attrs reset;""")
        elif tgtTR():
            output = self.cmdexec("""control query default showcontrol_show_all reset;""")

    # Get a CQD value.  The return value is a string.
    def get_cqd_value(self, name):
        # don't know if this CQD is an external one or an external one, 
        # just show all internal ones as well.
        self.showcontrol_showall_on()
        output = self.cmdexec('showcontrol query default ' + name + ';')
        lines = output.splitlines() 
        value = None
        for l in lines:
            tokens = l.split()
            if len(tokens) > 0 and tokens[0].lower() == name.lower():
                if len(tokens) >= 2:
                    value = tokens[1]
                    break
        self.showcontrol_showall_reset()
        return value

    # get the proper stat missing error numbers
    def get_ustat_error_numbers(self):
        self.showcontrol_showall_on()
        stmt = """showcontrol query default ustat_automation_interval;"""
        output = self.cmdexec(stmt)

        # When the USAS CQD is 0, USAS is off, error code should be 6007/6008.
        # When the USAS CQD >0, USAS is on, error code should be 6010/6011.
        ustat_auto = False
        for line in output.splitlines():
            if line.startswith('  USTAT_AUTOMATION_INTERVAL'):
                tokens = line.split()
                if len(tokens) > 1:
                    if int(tokens[1]) > 0:
                        ustat_auto = True

        self.showcontrol_showall_reset()

        if ustat_auto:
            return ['6010', '6011']
        else:
            return ['6007', '6008']

    # get the current query ID
    def get_current_qid(self):
        output = self.cmdexec("""get statistics for qid current;""")
        lines = output.splitlines()
        for l in lines:
            if l.strip() == '':
                continue
            tokens = l.strip().split()
            if tokens[0] == 'Qid':
                return tokens[1]
        return None

    # Set up the schema according to the target type
    def setup_schema(self, schema):
        # create schema does not have any effect on the TF target right now,
        # but it will be implemented soon.  It does not hurt to do it even 
        # there is no effect.
        output = self.cmdexec('create schema ' + schema + ';')
        output = self.cmdexec('set schema ' + schema + ';')

 
    # drop all objects in the schema
    def cleanup_schema(self, schema):
        output = self.cmdexec('drop schema ' + schema + ' cascade;')

#----------------------------------------------------------------------------
# A class that implements all HBase shell process related functions
#----------------------------------------------------------------------------
class HBase:
    """Implmentation for hbase shell related functions"""

    _proc_name = ''
    _testmgr = None
    _hpipe = None
    _prompt_str1 = 'hbase(main):'
    _last_prompt = None

    def __init__(self, name, testmgr):
       self._proc_name = name
       self._testmgr = testmgr

    #------------------------------------------------------------------------
    # Basic hbase functions, such as connect/disconnect/issue stmt and read
    # the results back.
    #------------------------------------------------------------------------
    # Make an hbase shell connection
    def connect(self):
        # Make sure $MY_SQROOT is set.
        output = self._testmgr.shell_call('echo $MY_SQROOT').strip()
        if not output:
            raise RuntimeError('$MY_SQROOT is not set, run sqenv.sh from your installation root first.')

        cmd = '$MY_SQROOT/sql/local_hadoop/hbase/bin/hbase shell'

        ON_POSIX = 'posix' in sys.builtin_module_names
        self._hpipe = subprocess.Popen(cmd, stdin=subprocess.PIPE,
          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          bufsize=1, close_fds=ON_POSIX, shell=True)

        # Change to non-blocking mode, so read returns even if there is no data.
        # this happens after the prompt shows up.
        fcntl.fcntl(self._hpipe.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

        # hbase shell by default set the prompt to NULL if stdout is not
        # TTY.  The code is like this:
        # lib/ruby/1.x/irb/init.rb has this line:
        #   @CONF[:PROMPT_MODE] = (STDIN.tty? ? :DEFAULT : :NULL)
        # If you type 'conf' from the shell prompt, you can see all these
        # configurations.  It means that if we start it from python, the
        # prompt is set to :NULL and it won't show up.  But we still need
        # the prompt to parse.  So we have to set it back to :DEFAULT
        self._hpipe.stdin.write('conf.prompt_mode=:DEFAULT\n')
        self._hpipe.stdin.flush()

        # consume header message
        out = self.read_until_next_prompt()

    # Disconnect from hbase shell
    def disconnect(self):
        # issue an exit command
        self.issue_stmt('exit')
        self._testmgr.log_write('\n')
        self._hpipe.kill()

    # Issue a statement to hbase shell
    def issue_stmt(self, stmt):
        # hbase's result output  includes the stmt as well.  
        # There is no need to log the stmt, just the prompt.
        # self._testmgr.log_write(self._last_prompt + stmt)
        self._testmgr.log_write(self._last_prompt)
        # strip trailing whitespace
        stmt = stmt.lstrip()
        stmt += '\n'
        # print ">>>", stmt
        self._hpipe.stdin.write(stmt)
        self._hpipe.stdin.flush()

    # Keep reading until the next prompt. Data returned does not include the
    # prompt.
    def read_until_next_prompt(self):
        buf_flush_threshold = 5 # sec
        buf = ''
        log_buf = ''
        same_buf = False

        start_time = time.time()

        while True:
            try:
                thisbuf = self._hpipe.stdout.read()
            except IOError: # there is no data
                # this is the prompt, we are done and return.
                if self._prompt_str1 in buf:
                    self._last_prompt = buf[buf.rfind(self._prompt_str1):]
                    buf = buf[:buf.rfind(self._prompt_str1)]
                    log_buf = log_buf[:log_buf.rfind(self._prompt_str1)]
                    self._testmgr.log_write(log_buf)
                    log_buf = ''
                    return buf
                elif not same_buf:
                    # deal with other special prompts.
                    s = buf.strip()
                    # flush out the buffer once we reach the threadhold.
                    # This way we can at least tell what the last message
                    # is even when it hangs.
                    elapsed_sec = time.time() - start_time
                    if elapsed_sec > buf_flush_threshold and log_buf != '':
                        self._testmgr.log_write(log_buf)
                        log_buf = ''
                        same_buf = True

            else:
                # there is data
                # strip all of the leading '+>'s.
                #  ^ leadning
                # (\+>) the string '+>' to strip. + is a special char, hence \
                # + 1 or more times
                if (len(thisbuf) > 0):
                    # print '{{{' + thisbuf + '}}}'
                    buf += re.sub('^(\+>)+','', thisbuf)
                    log_buf += re.sub('^(\+>)+','', thisbuf)
                    same_buf = False

    # Execute a statement and return the output in string form
    def cmdexec(self, stmt):
        self.issue_stmt(stmt)
        return self.read_until_next_prompt()

    # Unexpecting any error msg.
    def unexpect_error_msg(self, output):
        msg = 'ERROR:'
        if msg in output:
            self._testmgr.mismatch_record(msg, True)


#----------------------------------------------------------------------------
# A class that implements all Hive shell process related functions
#----------------------------------------------------------------------------
class Hive:
    """Implmentation for Hive shell related functions"""

    _proc_name = ''
    _testmgr = None
    _hpipe = None
    _prompt_str = 'hive> '

    def __init__(self, name, testmgr):
       self._proc_name = name
       self._testmgr = testmgr

    #------------------------------------------------------------------------
    # Basic Hive functions, such as connect/disconnect/issue stmt and read
    # the results back.
    #------------------------------------------------------------------------
    # Make an hive shell connection
    def connect(self):
        # Make sure $MY_SQROOT is set.
        output = self._testmgr.shell_call('echo $MY_SQROOT').strip()
        if not output:
            raise RuntimeError('$MY_SQROOT is not set, run sqenv.sh from your installation root first.')

        cmd = 'export HADOOP_HOME=$MY_SQROOT/sql/local_hadoop/hadoop && $MY_SQROOT/sql/local_hadoop/hive/bin/hive'

        ON_POSIX = 'posix' in sys.builtin_module_names
        self._hpipe = subprocess.Popen(cmd, stdin=subprocess.PIPE,
          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          bufsize=1, close_fds=ON_POSIX, shell=True)

        # Change to non-blocking mode, so read returns even if there is no data.
        # this happens after the prompt shows up.
        fcntl.fcntl(self._hpipe.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

        # consume header message
        out = self.read_until_next_prompt()

    # Disconnect from hive
    def disconnect(self):
        # issue an exit command
        self.issue_stmt('exit;')
        self._testmgr.log_write('\n')
        self._hpipe.kill()

    # Issue a statement to hive
    def issue_stmt(self, stmt):
        # hive's result output  includes the stmt as well.
        # There is no need to log the stmt, just the prompt.
        # self._testmgr.log_write(self._prompt_str + stmt)
        self._testmgr.log_write(self._prompt_str)
        # strip trailing whitespace
        stmt = stmt.lstrip()
        stmt += '\n'
        # print ">>>", stmt
        self._hpipe.stdin.write(stmt)
        self._hpipe.stdin.flush()

    # Keep reading until the next prompt. Data returned does not include the
    # prompt.
    def read_until_next_prompt(self):
        buf_flush_threshold = 5 # sec
        buf = ''
        log_buf = ''
        same_buf = False

        start_time = time.time()

        while True:
            try:
                thisbuf = self._hpipe.stdout.read()
            except IOError: # there is no data
                # this is the prompt, we are done and return.
                if len(buf) >= len(self._prompt_str) and \
                   buf[len(buf)-len(self._prompt_str):] == self._prompt_str:
                    buf = buf[:buf.rfind(self._prompt_str)]
                    log_buf = log_buf[:log_buf.rfind(self._prompt_str)]
                    self._testmgr.log_write(log_buf)
                    log_buf = ''
                    return buf
                elif not same_buf:
                    # deal with other special prompts.
                    s = buf.strip()
                    # flush out the buffer once we reach the threadhold.
                    # This way we can at least tell what the last message
                    # is even when it hangs.
                    elapsed_sec = time.time() - start_time
                    if elapsed_sec > buf_flush_threshold and log_buf != '':
                        self._testmgr.log_write(log_buf)
                        log_buf = ''
                        same_buf = True

            else:
                # there is data
                # strip all of the leading '>'s.
                #  ^ leadning
                # (\>) the string '>' to strip. + is a special char, hence \
                # + 1 or more times
                if (len(thisbuf) > 0):
                    # print '{{{' + thisbuf + '}}}'
                    buf += re.sub('^(\>)+','', thisbuf)
                    log_buf += re.sub('^(\>)+','', thisbuf)
                    same_buf = False

    # Execute a statement and return the output in string form
    def cmdexec(self, stmt):
        self.issue_stmt(stmt)
        return self.read_until_next_prompt()

    # Unexpecting any error msg.
    def unexpect_failed_msg(self, output):
        msg = 'FAILED:'
        if msg in output:
            self._testmgr.mismatch_record(msg, True)

#----------------------------------------------------------------------------
# A class that implements the main test driver.
# In order for multiprocess to work for a class, we need to run the picle
# method first:
#   copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)
# and in order to run that, we need HPTestMgr to inherit from object to
# get __mro__ (Method Resolution Order)
#----------------------------------------------------------------------------
class HPTestMgr(object):
    _dci_proc_list = {} 
    _hbase_proc_list = {}
    _hive_proc_list = {}
    _test_status_list = []
    _logfile_name = None
    _sumfile_name = None
    _logfd = None
    _silent_mode = False
    _echo = True
    _mismatch_list = []
    _local_mismatch_count = 0
    _local_deferred_count = 0
    _sep_line = '-'.rjust(79, '-') + '\n'
    _num_testcase_planned = 0 
    _test_start_time = None 
    _total_elapsed_time = 0
    _status_passed_str = 'Passed'
    _status_failed_str = 'Failed'
    _status_deferred_str = 'Deferred'
    _data_loader = 'data_import'

    def __init__(self):
        pass

    #------------------------------------------------------------------------
    # HPDCI process management related functions
    #------------------------------------------------------------------------
    # Create a new DCI process, make the connection.
    def create_dci_proc(self, name, target, dsn, user, pw, role=''):

        if self.dci_proc_name_exist(name):
            raise RuntimeError('proc name: ' + name + ' already exists.')

        dci = HPDci(name, self)
        # record it first before connect.  So if the connection fails, we can
        # still call delete_all_dci_procs() to kill the java processes
        self.record_dci_proc(name, dci)
        dci.connect(target, dsn, user, pw, role)
        if not ArgList._use_sqlci:
            # set hpdci idle timeout to infinite.
            output = dci.cmdexec('set idletimeout 0;')

        # Target specific settings go here.
        if tgtSQ():
            gvars.histograms = 'HISTOGRAMS'
            gvars.histogram_intervals = 'HISTOGRAM_INTERVALS'
            gvars.definition_schema = 'HP_DEFINITION_SCHEMA'
            gvars.current_schema_version = gvars.definition_schema
            gvars.sys_definition_schema = gvars.definition_schema
            gvars.inscmd = 'insert into'
        elif tgtTR():
            gvars.histograms = 'SB_HISTOGRAMS'
            gvars.histogram_intervals = 'SB_HISTOGRAM_INTERVALS'
            gvars.definition_schema = '"_MD_"'
            gvars.current_schema_version = gvars.definition_schema
            gvars.sys_definition_schema = gvars.definition_schema
            gvars.inscmd = 'upsert using load into'

        return dci 

    # Clone a new DCI process using a know DCI session's target and dsn, 
    # with new user, password, and role.
    def clone_dci_proc_with_id(self, name, dci, user, pw, role=''):
        return self.create_dci_proc(name, dci._target, dci._dsn, user, pw, role)

    # Clone a new DCI process using the current user, password, and role.
    def clone_dci_proc(self, name, dci):
        return self.create_dci_proc(name, dci._target, dci._dsn, dci._user, dci._pw, dci._role)

    # Disconnect and delete a dci process using its registered name.
    def delete_dci_proc(self, name):
        if not self.dci_proc_name_exist(name):
            raise RuntimeError('proc name: ' + name + ' does not exist.')
        obj = self._dci_proc_list[name]
        obj.disconnect()
        del self._dci_proc_list[name]
   
    # Disconnect and delete all registered DCI processes. 
    def delete_all_dci_procs(self):
        for k in self._dci_proc_list.keys():
            self.delete_dci_proc(k)        

    # Get a DCI object using its registered name. 
    def get_dci_proc(self, name):
        if not self.dci_proc_name_exist(name):
            raise RuntimeError('proc name: ' + name + ' does not exist.')
        return self._dci_proc_list[name]    
     
    # Get the default DCI process (whose name is 'SQL') that was created
    # automatically at the beginning of the test. 
    def get_default_dci_proc(self):
        return self.get_dci_proc('SQL')

    # Get the dbroot DCI process (whose name is 'SUPERSQL') that was created
    # automatically at the beginning of the test.
    def get_dbroot_dci_proc(self):
        return self.get_dci_proc('DBROOT')

    # Register a DCI process with its name. 
    def record_dci_proc(self, name, obj):
        if self.dci_proc_name_exist(name):
            raise RuntimeError('proc name: ' + name + ' already exists.')
        self._dci_proc_list[name] = obj 

    # Check to see if a DCI process with the name is registered.
    def dci_proc_name_exist(self, name):
        return self._dci_proc_list.has_key(name)

    #------------------------------------------------------------------------
    # HBase shell process management related functions
    #------------------------------------------------------------------------
    # Create a new hbase shell process, make the connection. This only
    # works when the tests are run locally with the instance installation
    # where you have direct access to the installed hbase shell.
    def create_hbase_proc(self, name):
        self.check_hbase_proc_name_not_exist(name)
        hbase = HBase(name, self)
        # record it first before connect.  So if the connection fails, we can
        # still call delete_all_hbase_procs() to kill the java processes
        self.record_hbase_proc(name, hbase)
        hbase.connect()
        return hbase

    # Disconnect and delete a hbase process using its registered name.
    def delete_hbase_proc(self, name):
        self.check_hbase_proc_name_exist(name)
        obj = self._hbase_proc_list[name]
        obj.disconnect()
        del self._hbase_proc_list[name]

    # Disconnect and delete all registered hbase processes.
    def delete_all_hbase_procs(self):
        for k in self._hbase_proc_list.keys():
            self.delete_hbase_proc(k)

    # Get a hbase object using its registered name.
    def get_hbase_proc(self, name):
        self.check_hbase_proc_name_exist(name)
        return self._hbase_proc_list[name]

    # Get the default hbase process (whose name is 'main') that was created
    # automatically at the beginning of the test.
    def get_default_hbase_proc(self):
        return self.get_hbase_proc('SQL')

    # Register a hbase process with its name.
    def record_hbase_proc(self, name, obj):
        self.check_hbase_proc_name_not_exist(name)
        self._hbase_proc_list[name] = obj

    # Check to make sure that a hbase process with the same name is not
    # already registered.  An exception will be raised if it is.
    def check_hbase_proc_name_not_exist(self, name):
        if (self._hbase_proc_list.has_key(name)):
            raise RuntimeError('proc name: ' + name + ' already exists.')

    # Check to make sure that a hbase process with the name is registered.
    # An exception will be raised if it is not.
    def check_hbase_proc_name_exist(self, name):
        if (not self._hbase_proc_list.has_key(name)):
            raise RuntimeError('proc name: ' + name + ' does not exist.')

    #------------------------------------------------------------------------
    # hive shell process management related functions
    #------------------------------------------------------------------------
    # Create a new hive shell process, make the connection. This only
    # works when the tests are run locally with the instance installation
    # where you have direct access to the installed hive shell.
    def create_hive_proc(self, name):
        self.check_hive_proc_name_not_exist(name)
        hive = Hive(name, self)
        # record it first before connect.  So if the connection fails, we can
        # still call delete_all_hive_procs() to kill the java processes
        self.record_hive_proc(name, hive)
        hive.connect()
        return hive

    # Disconnect and delete a hive process using its registered name.
    def delete_hive_proc(self, name):
        self.check_hive_proc_name_exist(name)
        obj = self._hive_proc_list[name]
        obj.disconnect()
        del self._hive_proc_list[name]

    # Disconnect and delete all registered hive processes.
    def delete_all_hive_procs(self):
        for k in self._hive_proc_list.keys():
            self.delete_hive_proc(k)

    # Get a hive object using its registered name.
    def get_hive_proc(self, name):
        self.check_hive_proc_name_exist(name)
        return self._hive_proc_list[name]

    # Get the default hive process (whose name is 'main') that was created
    # automatically at the beginning of the test.
    def get_default_hive_proc(self):
        return self.get_hive_proc('SQL')

    # Register a hive process with its name.
    def record_hive_proc(self, name, obj):
        self.check_hive_proc_name_not_exist(name)
        self._hive_proc_list[name] = obj

    # Check to make sure that a hive process with the same name is not
    # already registered.  An exception will be raised if it is.
    def check_hive_proc_name_not_exist(self, name):
        if (self._hive_proc_list.has_key(name)):
            raise RuntimeError('proc name: ' + name + ' already exists.')

    # Check to make sure that a hive process with the name is registered.
    # An exception will be raised if it is not.
    def check_hive_proc_name_exist(self, name):
        if (not self._hive_proc_list.has_key(name)):
            raise RuntimeError('proc name: ' + name + ' does not exist.')

    #------------------------------------------------------------------------
    # Shell command line related functions
    #------------------------------------------------------------------------
    # call the shell to run a shell command or program.
    def shell_call(self, cmd):
        # subprocess.call(cmd)
        ON_POSIX = 'posix' in sys.builtin_module_names
        self.log_write('SHELL>' + cmd + '\n')
        hpipe = subprocess.Popen(cmd, stdin=subprocess.PIPE,
          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
          bufsize=1, close_fds=ON_POSIX, shell=True)
        # Change to non-blocking mode, so read returns even if there is no data.
        # fcntl.fcntl(self._hpipe.stdout, fcntl.F_SETFL, os.O_NONBLOCK)
        output = hpipe.stdout.read()
        self.log_write(output)
        return output 

    #------------------------------------------------------------------------
    # Invoke HPDCI one time and feed it an obey file.
    # WARNING: This obey file must end with 'exit;' otherwise this command
    # sits in a prompt and won't return.
    #------------------------------------------------------------------------
    def exec_dci_with_obeyfile(self, file):
        classpath = '.:' + ArgList._jdbc_classpath + ':' + ArgList._hpdci_classpath
        if tgtSQ():
            cmd = ArgList._java + ' -classpath ' + classpath + ' com.hp.hpdci.UserInterface -h ' + ArgList._target + ' -dsn ' + ArgList._dsn + ' -u ' + ArgList._user + ' -p ' + ArgList._pw
        elif tgtTR():
            cmd = ArgList._java + ' -classpath ' + classpath + ' org.trafodion.ci.UserInterface -h ' + ArgList._target + ' -u ' + ArgList._user + ' -p ' + ArgList._pw

        if ArgList._role == '':
            cmd += ' -r \'\''
        else:
            cmd = cmd + ' -r ' + ArgList._role
        cmd = cmd + ' -s ' + file
        return self.shell_call(cmd)

    def exec_dbroot_dci_with_obeyfile(self, file):
        classpath = '.:' + ArgList._jdbc_classpath + ':' + ArgList._hpdci_classpath
        if tgtSQ():
            cmd = ArgList._java + ' -classpath ' + classpath + ' com.hp.hpdci.UserInterface -h ' + ArgList._target + ' -dsn ' + ArgList._dsn + ' -u ' + ArgList._dbroot_user + ' -p ' + ArgList._dbroot_pw
        elif tgtTR():
            cmd = ArgList._java + ' -classpath ' + classpath + ' org.trafodion.ci.UserInterface -h ' + ArgList._target + ' -u ' + ArgList._dbroot_user + ' -p ' + ArgList._dbroot_pw

        if ArgList._dbroot_role == '':
            cmd += ' -r \'\''
        else:
            cmd = cmd + ' -r ' + ArgList._dbroot_role
        cmd = cmd + ' -s ' + file
        return self.shell_call(cmd)

    #------------------------------------------------------------------------
    # Invoke HPDCI one time and feed it with one statement.
    #------------------------------------------------------------------------
    def exec_dci_with_one_stmt(self, stmt):
        classpath = '.:' + ArgList._jdbc_classpath + ':' + ArgList._hpdci_classpath
        if tgtSQ():
            cmd = ArgList._java + ' -classpath ' + classpath + ' com.hp.hpdci.UserInterface -h ' + ArgList._target + ' -dsn ' + ArgList._dsn + ' -u ' + ArgList._user + ' -p ' + ArgList._pw
        elif tgtTR():
            cmd = ArgList._java + ' -classpath ' + classpath + ' org.trafodion.ci.UserInterface -h ' + ArgList._target + ' -u ' + ArgList._user + ' -p ' + ArgList._pw

        if ArgList._role == '':
            cmd += ' -r \'\''
        else:
            cmd = cmd + ' -r ' + ArgList._role
        cmd = cmd + ' -q ' + '"' + stmt + '"'
        return self.shell_call(cmd)

    def exec_dbroot_dci_with_one_stmt(self, stmt):
        classpath = '.:' + ArgList._jdbc_classpath + ':' + ArgList._hpdci_classpath
        if tgtSQ():
            cmd = ArgList._java + ' -classpath ' + classpath + ' com.hp.hpdci.UserInterface -h ' + ArgList._target + ' -dsn ' + ArgList._dsn + ' -u ' + ArgList._dbroot_user + ' -p ' + ArgList._dbroot_pw
        elif tgtTR():
            cmd = ArgList._java + ' -classpath ' + classpath + ' org.trafodion.ci.UserInterface -h ' + ArgList._target + ' -u ' + ArgList._dbroot_user + ' -p ' + ArgList._dbroot_pw

        if ArgList._dbroot_role == '':
            cmd += ' -r \'\''
        else:
            cmd = cmd + ' -r ' + ArgList._dbroot_role
        cmd = cmd + ' -q ' + '"' + stmt + '"'
        return self.shell_call(cmd)

    #------------------------------------------------------------------------
    # Log files related functions
    #------------------------------------------------------------------------
    # open a test log file
    def log_open(self, name, echo=True):
        if self._logfd:
            self._logfd.close()
        self._logfd = open(name, 'a+')
        self._echo = echo

    # write to the log file and stdout
    def log_write(self, string):
        if not self._silent_mode:
            if self._logfd:
                self._logfd.write(string)
                self._logfd.flush()
            if self._echo:
                sys.stdout.write(string)
                sys.stdout.flush()

    # write to the log file only
    def log_write_log_only(self, string):
        if not self._silent_mode:
            if self._logfd:
                self._logfd.write(string)
                self._logfd.flush()

    # close the log file
    def log_close(self):
        if self._logfd:
           self._logfd.close()
           self._logfd = None

    # turn on silent mode
    def silent_mode_on(self):
        self._silent_mode = True

    # turn off silent mode
    def silent_mode_off(self):
        self._silent_mode = False

    #------------------------------------------------------------------------
    # Mismatch and deferred management related functions
    #------------------------------------------------------------------------
    # clear all recorded mismatch info.
    def mismatch_clear(self):
        self._mismatch_list[:] = []
        self.local_mismatch_count_reset()

    # record a mismatch
    def mismatch_record(self, msg, unexpect=False):
        rec = inspect.stack()[2] # 0 reprents this line,
                                 # 1 reprents line at caller,
                                 # 2 reprents line at caller's caller,
                                 # ... and so on ...
        frame = rec[0]
        info = inspect.getframeinfo(frame)
        name = inspect.getmodulename(info.filename) + '.' + info.function
        if unexpect:
            s = '*** MISMATCH *** unexpecting: \'' + msg + '\''
        else:
            s = '*** MISMATCH *** expecting: \'' + msg + '\''
        # s = info.filename + ':' + str(info.lineno) + ' ' + info.function + '():\n*** MISMATCH *** expecting: \'' + msg + '\''
        self.log_write(s + '\n\n')
        self._mismatch_list.append(name + '():\n' + s)
        self.local_mismatch_count_increase()

    # Enter the recorded mismatch info.
    def log_mismatch_summary(self):
        for item in self._mismatch_list:
            self.log_write(item + '\n\n')

        list_len = len(self._mismatch_list)
        if list_len > 0:
            s = '---  ' + str(list_len) + ' *** MISMATCH(es) *** found   ---\n'
            self.log_write(s)
            return True
        else:
            return False

    # Reset the mismatch count.
    def local_mismatch_count_reset(self):
        self._local_mismatch_count = 0

    # Increase the mismatch count.
    def local_mismatch_count_increase(self):
        self._local_mismatch_count += 1

    # Return the mismatch count.
    def local_mismatch_count(self):
        return self._local_mismatch_count

    # Reset the deferred count.
    def local_deferred_count_reset(self):
        self._local_deferred_count = 0

    # Incrase the deferred count.
    def local_deferred_count_increase(self):
        self._local_deferred_count += 1 

    # Return the deferred count.
    def local_deferred_count(self):
        return self._local_deferred_count

    #------------------------------------------------------------------------
    # Execution management related functions
    #------------------------------------------------------------------------
    # Clear the testing status list
    def test_status_list_clear(self):
        self._test_status_list[:] = [] 

    # Append a new status to the testing status list
    def test_status_list_append(self, name, desc, status, time):
        self._test_status_list.append([name, desc, status, time])

    # Prepare the output for a DFM style test summary.  Return a tuple of
    # test status (True: all success or deferred, False: some failed), and
    # the summary output
    def dfm_style_summary(self):
        n_len=22
        d_len=32
        s_len=8
        t_len=12

        output = ('DATE : ' + datetime.datetime.now().strftime('%c') + '\n\n')
        n = 'Testcase'
        d = ''
        s = 'Status'
        t = 'Elapsed Time'
        output += (n[:n_len].ljust(n_len) + ' ' + \
                   d[:d_len].ljust(d_len) + '  ' + \
                   s[:s_len].ljust(s_len) + '  ' + \
                   t[:t_len].ljust(t_len) + '\n')
        output += self._sep_line

        passed_count = 0
        failed_count = 0
        deferred_count = 0
        for [n, d, s, t] in self._test_status_list:
            output += (n[:n_len].ljust(n_len) + ' ' + \
                       d[:d_len].ljust(d_len) + '  ' + \
                       s[:s_len].ljust(s_len) + '  ' + \
                       t[:t_len].ljust(t_len) + '\n')
            if s == self._status_passed_str:
                passed_count += 1
            elif s == self._status_failed_str:
                failed_count += 1
            else:
                deferred_count += 1

        output += '\n'
        output += ('Number of testcase planed'.ljust(39) + str(self._num_testcase_planned) + '\n')
        output += ('Number of testcase run:'.ljust(39) + str(passed_count+failed_count+deferred_count) + '\n')
        if passed_count:
            output += ('Number of testcase passed:'.ljust(39) + str(passed_count) + '\n')
        if failed_count:
            output += ('Number of testcase failed:'.ljust(39) + str(failed_count) + '\n')
        if deferred_count:
            output += ('Number of testcase deferred:'.ljust(39) + str(deferred_count) + '\n')
        output += '\nCOMPLETE RUN\n\n'

        min, sec = divmod(self._total_elapsed_time, 60)
        hr, min = divmod(min, 60)
        t = '%02d:%02d:%02d' % (hr, min, sec)
        output += ('TOTAL ELAPSED TIME:  ' + t + '\n\n')

        return [(failed_count == 0), output]

    # Should be called before a testcase starts.
    def testcase_begin(self, testlist):
        self._test_start_time = time.time() 
        rec = inspect.stack()[1] # 0 reprents this line,
                                 # 1 reprents line at caller,
                                 # 2 reprents line at caller's caller,
                                 # ... and so on ...
        frame = rec[0]
        info = inspect.getframeinfo(frame)
        name = inspect.getmodulename(info.filename) + '.' + info.function

        self._num_testcase_planned += 1

        if testlist:
            if testlist[0] == '~': # this list is to be excluded
                if name in testlist:
                    return False
            else:                  # this list is to be included
                if name not in testlist:
                    return False

        self.local_mismatch_count_reset()
        self.local_deferred_count_reset()
        s = '== TEST: ' + name + '\n'
        self.log_write(self._sep_line + s + self._sep_line)
        return True

    # Should be called after a testcase ends.
    def testcase_end(self, desc):
        rec = inspect.stack()[1] # 0 reprents this line,
                                 # 1 reprents line at caller,
                                 # 2 reprents line at caller's caller,
                                 # ... and so on ...
        frame = rec[0]
        info = inspect.getframeinfo(frame)
        name = inspect.getmodulename(info.filename) + '.' + info.function

        # When expect file creates a new file or section, it's considered 
        # 'Deferred', even when there are other mismtches.
        if self.local_deferred_count():
            status = self._status_deferred_str
        elif self.local_mismatch_count():
            status = self._status_failed_str
        else: 
            status = self._status_passed_str

        if self._test_start_time:
           elapsed_sec = time.time() - self._test_start_time
           self._total_elapsed_time += elapsed_sec
           min, sec = divmod(elapsed_sec, 60)
           hr, min = divmod(min, 60)
           exec_time = '%02d:%02d:%02d' % (hr, min, sec)
        else:
           exec_time = '--------' 
        self.test_status_list_append(name, desc, status, exec_time)

    # Should be called before a testunit starts.
    def testunit_begin(self, module):
        result_dir_create(module) 
        # this remove does nothing if the work_dir does not exist.
        work_dir_remove(module)
        work_dir_create(module)
        self._logfile_name = my_logfile(module)
        self._sumfile_name = my_sumfile(module)
        # remove the files if they exist
        if os.path.isfile(self._logfile_name):
            os.remove(self._logfile_name)
        if os.path.isfile(self._sumfile_name):
            os.remove(self._sumfile_name)
        self.log_open(self._logfile_name)
        self.mismatch_clear()
        self.test_status_list_clear()
        self._num_testcase_planned = 0
        self._total_elapsed_time = 0
        self._no_test_case = 0
        # create the default hpdci process
        self.create_dci_proc('SQL', ArgList._target, ArgList._dsn, ArgList._user, ArgList._pw, ArgList._role)
        # create the dbroot hpdci process
        self.create_dci_proc('DBROOT', ArgList._target, ArgList._dsn, ArgList._dbroot_user, ArgList._dbroot_pw, ArgList._dbroot_role)


    # Should be called after a testunit ends.
    def testunit_end(self, module):
        self.log_write('List of mismatches\n')
        self.log_write(self._sep_line)
        self.log_mismatch_summary()
        self.log_write('\n')

        status, output = self.dfm_style_summary()
        self.log_write(output)
        self.log_close()

        # create a sum file and write this to the sum file too
        fd = open(self._sumfile_name, 'w+')
        fd.write(output)
        fd.close()
       
        # summary has been reported, clear the mismatch list now
        self.mismatch_clear()
   
        # remote the temporary work dir
        work_dir_remove(module)

        # kill all hpdci processes
        self.delete_all_dci_procs()

        return status

    #------------------------------------------------------------------------
    # Data loading related functions
    #------------------------------------------------------------------------
    def subproc_loader_using_jdbc(self, x):
        work_dir = x[0]
        proc_no = x[1]
        prop_file = x[2]
        table = x[3]
        data_file = x[4]
        separator = x[5]
        start_line = x[6]
        line_count = x[7]
        logfile_name = x[8]
        proc_name = 'subproc[' + str(proc_no) + ']'

        self.log_open(logfile_name)
        self.log_write(proc_name + ' started to load lines: ' + str(start_line) + '..' + str(start_line+line_count-1) + '\n')

        # the java loader class file should have been built in work_dir
        # of this program.  
        jdbc_loader_path = os.path.dirname(sys.modules[__name__].__file__)
        classpath = work_dir + ':' + ArgList._jdbc_classpath 
        cmd = ArgList._java + ' -classpath ' + classpath + ' -Dhpt4jdbc.properties=' + prop_file + ' ' + self._data_loader + ' ' + table + ' ' + data_file + ' ' + str(start_line) + ' ' + str(line_count) + ' ' + '"' + separator + '"' + ' ' + work_dir + ' ' + ArgList._target_type
        out = self.shell_call(cmd)
        # Java already prints this, writes to log file only, no stdout write.
        self.log_write_log_only(out)
        self.log_close()

        if str(line_count) + ' row(s) imported.' not in out:
            return [proc_name, False, start_line, line_count, out]
        else:
            return [proc_name, True, -1, -1, 'success']

    def data_loader(self, work_dir, prop_file, table, data_file, separator=',',
                    max_streams=6):

        if tgtTR():
            max_streams=1

        min_rows_per_stream = 10000

        failure_msg = 'Status: Table loading failed.\n\n'
        success_msg = 'Status: Table loaded.\n\n'

        # To avoid mismatched Java versions, the class file is always
        # rebuild into the work_dir.  It checks to see if there is one
        # in work_dir.  If the file does not exist, whichever test in the
        # same testsuite (i.e. using the same work_dir) calls this function
        # first gets to build it.  The source code .jar is always in the
        # same directory as this python module file.
        lib_dir = os.path.dirname(sys.modules[__name__].__file__)
        class_file = work_dir + '/' + self._data_loader + '.class'
        if not os.path.isfile(class_file):
            # we want to use the javac in the same directory as java.
            # simpily append 'c' to it.
            cmd = ArgList._java + 'c -classpath ' + lib_dir + ':' + ArgList._jdbc_classpath + ' -d ' + work_dir + ' ' + lib_dir + '/' + self._data_loader + '.java'
            out = self.shell_call(cmd)   
            self.log_write(out)
            # if we still don't have the file, something is wrong. 
            if not os.path.isfile(class_file):
                self.log_write('ERROR: Failed to compile ' + self._data_loader + '.class. shell command: ' + cmd + '\n')
                self.log_write(failure_msg)
                return failure_msg

        self.log_write('Loading data to ' + table + ' from ' + data_file + '\n')
        # Get the total line count from the file.
        fd = open(data_file, 'r')
        for total_line_count, line in enumerate(fd):
            pass
        # line count starts from 0
        total_line_count += 1
        fd.close()

        # Calculate how many streams are needed, and how many lines each
        # streams have to process.
        if max_streams < 1:
            self.log_write('ERROR: Invalid max_streams: ' + max_streams)
            self.log_write(failure_msg)
            return failure_msg

        num_streams = max_streams
        while True:
            num_lines_per_proc = total_line_count / num_streams;
            # if there is not enough data to fill even one insert, decress
            # the num_streams, but the minimun is 1 stream.
            if num_streams > 1 and num_lines_per_proc < min_rows_per_stream:
               num_streams -= 1
            else:
               # we are done
               break

        # compose the argument list to pass to each subprocess.
        arglist = []
        proc_no = 0
        start_line = 0
        while proc_no < num_streams:
            start_line = num_lines_per_proc * proc_no
            # last stream
            if proc_no == (num_streams - 1):
                line_count = total_line_count - start_line
            else:
                line_count = num_lines_per_proc
            arglist.append([work_dir, proc_no, prop_file, table, data_file, separator, start_line, line_count, self._logfile_name])
            proc_no += 1

        pool = multiprocessing.Pool(processes=proc_no)
        res_list = pool.map(self.subproc_loader_using_jdbc, arglist)
        pool.close()
        pool.join()
        failure_status = ''
        for r in res_list:
            proc_name = r[0]
            status = r[1]
            start_row = r[2]
            line_count = r[3]
            output = r[4]
            if not status:
                failure_status += (proc_name + ' reports failure at line ' + str(start_row) + '..' + str(start_row + line_count - 1) + '.\n')
                # already written by subproc failure_status += output

        if failure_status:
            self.log_write('ERROR: failured reported by subprocess loader.\n')
            self.log_write(failure_status)
            self.log_write(failure_msg)
            return failure_msg

        self.log_write(success_msg)
        return success_msg

#----------------------------------------------------------------------------
# Useful helper functions
#----------------------------------------------------------------------------

# Get additional test environment information
def get_test_env_setting(what):
    if what == 'TEST_ENV_QALIB_DIR':
        return ArgList._qalib_dir;
    elif what == 'TEST_ENV_QALIB_SPJ_DIR':
        return os.path.join(ArgList._qalib_dir, 'SPJ') 
    elif what == 'TEST_ENV_QALIB_UDF_DIR':
        return os.path.join(ArgList._qalib_dir, 'UDF')
    else:
        raise RuntimeError('UnKNOWN request for get_test_env_setting(): ' + what)

# Get the test directory according to the module
def my_test_dir(module_name):
    module = sys.modules[module_name]
    return os.path.dirname(module.__file__)

# Return the temporary work dir that a test can use.  This is pre-created
# by the test manager and will be purged afterwards.
def my_work_dir(module_name):
    module = sys.modules[module_name]
    d, f = my_result_dir_and_filename(module)
    return os.path.join(d, f+'_work')

# Calculate and create the result directory if it does not exist.  It
# returns a tuple of the result directory and the filename that should
# be used without the file extension part.
def my_result_dir_and_filename(module):
    path = os.path.dirname(module.__file__)
    path, s1 = os.path.split(path)
    path, s2 = os.path.split(path)
    path, s3 = os.path.split(path)
 
    path = ArgList._results_dir
    path = os.path.abspath(os.path.join(path, s2))
    return [path, s1]

# Create the result directory.
def result_dir_create(module):
    d, f = my_result_dir_and_filename(module)
    folders=[]
    while True:
        d, f = os.path.split(d) 
        if f:
            folders.insert(0, f)
        else: # f is empty
           if d:
               folders.insert(0, d)
           break
    # my_result_dir_and_filename() should always return abosulte name.
    path = ''
    for f in folders:
        path = os.path.join(path, f)
        if not os.path.isdir(path):
            os.mkdir(path)

# Create the temporary work directory for a test.
def work_dir_create(module):
    work_dir = my_work_dir(module.__name__)
    if not os.path.isdir(work_dir):
       os.mkdir(work_dir)

# Remove the temporary work directory for a test.
def work_dir_remove(module):
    work_dir = my_work_dir(module.__name__)
    if os.path.isdir(work_dir):
        for root, dirs, files in os.walk(work_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        # os.rmdir(work_dir)
        shutil.rmtree(work_dir)

# Return the logfile name in full path for the test.  The directory will
# also be created if it does not exist.
def my_logfile(module):
    d, f = my_result_dir_and_filename(module)
    return os.path.join(d, f+'.log')

# Return the sumfile name in full path for the test.  The directory will
# also be created if it does not exist.
def my_sumfile(module):
    d, f = my_result_dir_and_filename(module)
    return os.path.join(d, f+'.sum')

# Return the schema name that the test is supposed to use.
def my_schema(module_name):
    module = sys.modules[module_name]
    path = os.path.dirname(module.__file__)
    path, s1 = os.path.split(path)
    path, s2 = os.path.split(path)
    # If the test ever needs to append the user id to the schema name,
    # uncomment the following:
    # if ArgList._user == None:
    #   user = 'sql_usser'
    # else:
    #  user = ArgList._user
    # return user + '_' + s2 + '_' + s1
    return s2 + '_' + s1 

# Executes _init() + all testXXX() in the module (dir() lists them in the 
# order of the appearance in the file.)
# Only use this function if the tests in your module are named testXXX(),
# and only if you want to run them in the same order as they appear in the
# file.  Otherwise, list them manually instead.
def auto_execute_module_tests(module, hpdcimgr, testlist):
    # always run _init() first
    getattr(module, '_init')(hpdcimgr, testlist)
    for func in dir(module):
        if func.startswith('test'):
            try:
                getattr(module, func)()
            except TypeError as e:
                raise RuntimeError('Failed to invoke ' + func + ' reason: ' + str(e))


# Parse the argument list for main
# This is used when running the tests from myunit.py as a directory unitest
# program.
def prog_parse_args_from_main():
    hpdci_required_args = ['target', 'user', 'pw', 'dbrootuser', 'dbrootpw']

    rec = inspect.stack()[1] # 0 reprents this line,
                             # 1 reprents line at caller,
                             # 2 reprents line at caller's caller,
                             # ... and so on ...
    frame = rec[0]
    info = inspect.getframeinfo(frame)
    default_results_dir= os.path.dirname(os.path.abspath(info.filename)) + '/results'

    # alas, the more powerful argparse module only exists in >= 2.7 and >= 3.2,
    # use optparse instead.
    option_list = [
        # No need to add '-h' or '-help', optparse automatically adds one.

        # we do not use short options, hence the first ''.
        # required args
        optparse.make_option('', '--target', action='store', type='string',
          dest='target',
          help='target \'<IP>:<port>\', required argument with no default. This is still needed for jdbc loader even when using sqlci.'),
        optparse.make_option('', '--user', action='store', type='string',
          dest='user',
          help='user id for the target, required argument with no default. It can be any non-empty string if using sqlci.'),
        optparse.make_option('', '--pw', action='store', type='string',
          dest='pw',
          help='password for the target, required argument with no default. It can be any non-empty string if using sqlci.'),
        optparse.make_option('', '--dbrootuser', action='store', type='string',
          dest='dbrootuser',
          help='dbroot user id for the target, required argument with no default. It can be any non-empty string if using sqlci.'),
        optparse.make_option('', '--dbrootpw', action='store', type='string',
          dest='dbrootpw',
          help='dbroot password for the target, required argument with no default. It can be any non-empty string if using sqlci.'),
        # optional args
        optparse.make_option('', '--role', action='store', type='string',
          dest='role', default='',
          help='role for the target, defaulted to \'\''),
        optparse.make_option('', '--dbrootrole', action='store', type='string',
          dest='dbrootrole', default='',
          help='dbroot role for the target, defaulted to \'\''),
        optparse.make_option('', '--dsn', action='store', type='string',
          dest='dsn', default='TDM_Default_DataSource',
          help='data source for the target, defaulted to \'TDM_Default_DataSource\''),
        optparse.make_option('', '--java', action='store', type='string',
          dest='java', default='java',
          help='java program location, defaulted to \'java\''),
        optparse.make_option('', '--jdbccp', action='store', type='string',
          dest='jdbccp', default=gvars.DEFAULT_JDBC_CLASSPATH,
          help='jdbc classpath, defaulted to \'DEFAULT_JDBC_CLASSPATH\' set in \'lib/gvars.py\''),
        optparse.make_option('', '--hpdcicp', action='store', type='string',
          dest='hpdcicp', default=gvars.DEFAULT_HPDCI_CLASSPATH,
          help='hpdci classpath, defaulted to \'DEFAULT_HPDCI_CLASSPATH\' set in \'lib/gvars.py\''),
        optparse.make_option('', '--resultdir', action='store', type='string',
          dest='resultdir', default=default_results_dir,
          help='results directory, defaulted to \'<test root>/results\', <test root> is where the test program is.'),
        optparse.make_option('', '--qalibdir', action='store', type='string',
          dest='qalibdir', default='/opt/home/trafodion/QALibs',
          help='QA library directory (for UDFs, SPJs, etc) on target machine, defaulted to \'/opt/home/trafodion/QALibs\' '),
        optparse.make_option('', '--sqlci', action='store_true',
          dest='usesqlci', default=False,
          help='use sqlci on a local node instead of hpdci'),
        optparse.make_option('', '--targettype', action='store', type='string',
          dest='targettype', default='TR',
          help='target type, defaulted to TR for Trafodion')
    ]

    usage = 'usage: %prog [-h|--help|<options>]'
    parser = optparse.OptionParser(usage=usage, option_list=option_list)
    # OptionParser gets the options out, whatever is not preceeded by
    # an option is considered args.
    (options, args) = parser.parse_args()

    # we are not expecting any args right now.  In the future, if we do,
    # make a list of the known args and check against it.
    if args:
        parser.error('Invalid argment(s) found: ' + str(args))

    # check for the required args for certain conditions
    not_found = []
    if not options.usesqlci:
        for r in hpdci_required_args:
            if options.__dict__[r] == None:
                not_found.append('--' + r)
    if not_found:
        parser.error('Required option(s) not found: ' + str(not_found))

    if options.targettype != 'SQ' and options.targettype != 'TR':
        parser.error('Invalid --targettype.  Only SQ aor TR is supported: ' +
                     options.targettype);

    ArgList._target = options.target
    ArgList._user = options.user
    ArgList._pw = options.pw
    ArgList._role = options.role
    ArgList._dbroot_user = options.dbrootuser
    ArgList._dbroot_pw = options.dbrootpw
    ArgList._dbroot_role = options.dbrootrole
    ArgList._dsn = options.dsn
    ArgList._java = options.java
    ArgList._jdbc_classpath = options.jdbccp
    ArgList._hpdci_classpath = options.hpdcicp
    ArgList._results_dir = options.resultdir
    ArgList._qalib_dir = options.qalibdir
    ArgList._use_sqlci = options.usesqlci
    ArgList._target_type = options.targettype

    print 'target:            ', ArgList._target
    print 'user:              ', ArgList._user
    print 'pw:                ', ArgList._pw
    print 'role:              ', ArgList._role
    print 'dbroot user:       ', ArgList._dbroot_user
    print 'dbroot pw:         ', ArgList._dbroot_pw
    print 'dbroot role:       ', ArgList._dbroot_role
    print 'dsn:               ', ArgList._dsn
    print 'java program:      ', ArgList._java
    print 'jdbc classpath:    ', ArgList._jdbc_classpath
    print 'hpdci classpath:   ', ArgList._hpdci_classpath
    print 'results directory: ', ArgList._results_dir
    print 'qalib directory:   ', ArgList._qalib_dir
    print 'use sqlci:         ', ArgList._use_sqlci
    print 'target type:       ', ArgList._target_type

    # Once we are done with our arguments, clear the sys.argv ecept for
    # the program name, so that they don't get passed into unittest.main()
    del sys.argv[1:]

# Parse the argument list from the config.init 
# This is used when running the tests from tox
def prog_parse_args_from_initfile():

    scriptPath = os.path.dirname(os.path.realpath(__file__))
    Config = ConfigParser.ConfigParser()
    Config.read(os.path.abspath(scriptPath + '../../../config.ini'))

    ArgList._target = Config.get("pytest","tcp").lstrip('TCP:')
    ArgList._user = Config.get("pytest","usr")
    ArgList._pw = Config.get("pytest","pwd") 
    ArgList._role = Config.get("pytest","usr_role")
    ArgList._dbroot_user = Config.get("pytest","dbrootusr")
    ArgList._dbroot_pw = Config.get("pytest","dbrootpwd")
    ArgList._dbroot_role = Config.get("pytest","dbrootusr_role")
    ArgList._dsn = Config.get("pytest","dsn")
    ArgList._java = 'java'
    ArgList._jdbc_classpath = Config.get("pytest","t4jdbc_classpath")
    ArgList._hpdci_classpath = Config.get("pytest","hpdci_classpath")
    ArgList._results_dir = Config.get("pytest","log_directory")
    ArgList._qalib_dir = Config.get("pytest","libroot")
    ArgList._use_sqlci = False

    hpdci_class = Config.get("pytest","hpdci_class")
    if hpdci_class == 'org.trafodion.ci.UserInterface':
        ArgList._target_type = 'TR'
    else:
        ArgList._target_type = 'SQ'

    # print does not show up when running from tox
    # turn off when not actually running any tests
    # and only print this once if running tests
    try:
        if os.environ['PY_FWK_PRINT_CFG_INI'] == "yes" and  str(sys.argv[1]) == 'discover' and str(sys.argv[3]) != '--list':
            #sys.stderr.write('Arguments:         ' + str(sys.argv) + '\n')
            sys.stderr.write('target:            ' + ArgList._target + '\n')
            sys.stderr.write('user:              ' + ArgList._user + '\n')
            sys.stderr.write('pw:                ' + ArgList._pw + '\n')
            sys.stderr.write('role:              ' + ArgList._role + '\n')
            sys.stderr.write('dbroot user:       ' + ArgList._dbroot_user + '\n')
            sys.stderr.write('dbroot pw:         ' + ArgList._dbroot_pw + '\n')
            sys.stderr.write('dbroot role:       ' + ArgList._dbroot_role + '\n')
            sys.stderr.write('dsn:               ' + ArgList._dsn + '\n')
            sys.stderr.write('java program:      ' + ArgList._java + '\n')
            sys.stderr.write('jdbc classpath:    ' + ArgList._jdbc_classpath + '\n')
            sys.stderr.write('hpdci classpath:   ' + ArgList._hpdci_classpath + '\n')
            sys.stderr.write('results directory: ' + ArgList._results_dir + '\n')
            sys.stderr.write('qalib directory:   ' + ArgList._qalib_dir + '\n')
            sys.stderr.write('use sqlci:         ' + str(ArgList._use_sqlci) + '\n')
            sys.stderr.write('target type:       ' + ArgList._target_type + '\n\n')

            # set to no so will not print previous block again
            os.environ['PY_FWK_PRINT_CFG_INI'] = "no"
        else:
            pass
    except:
        pass

# create a JDBC prop file using templatefile.  It replaces all str1 in
# templatefile with str2, where multiple [str1, str2]s can be listed in
# replacelist.  templatefile and newfile both are full path file names
#
# If replacelist is empty, this function expects the template file to
# contain:
#   REPLACE_JDBC_HOST
#   REPLACE_JDBC_USER
#   REPLACE_JDBC_PW
#   REPLACE_JDBC_ROLE
# It replaces them with the values passed into the program and saved in
# ArgList
def create_jdbc_propfile(templatefile, newfile, catalog, schema, replacelist=[]):
    if replacelist == []:
        replacelist = [['REPLACE_JDBC_HOST', ArgList._target],
                       ['REPLACE_JDBC_USER', ArgList._user],
                       ['REPLACE_JDBC_PW', ArgList._pw],
                       ['REPLACE_JDBC_ROLE', ArgList._role],
                       ['REPLACE_JDBC_CATALOG', catalog],
                       ['REPLACE_JDBC_SCHEMA', schema]]
    fd1 = open(templatefile, 'r')
    fd2 = open(newfile, 'w+')

    for line in fd1:
        for r in replacelist:
            line = line.replace(r[0], r[1])
        fd2.write(line)
    fd1.close()
    fd2.close()

def create_dbroot_jdbc_propfile(templatefile, newfile, catalog, schema, replacelist=[]):
    if replacelist == []:
        replacelist = [['REPLACE_JDBC_HOST', ArgList._target],
                       ['REPLACE_JDBC_USER', ArgList._dbroot_user],
                       ['REPLACE_JDBC_PW', ArgList._dbroot_pw],
                       ['REPLACE_JDBC_ROLE', ArgList._dbroot_role],
                       ['REPLACE_JDBC_CATALOG', catalog],
                       ['REPLACE_JDBC_SCHEMA', schema]]
    fd1 = open(templatefile, 'r')
    fd2 = open(newfile, 'w+')

    for line in fd1:
        for r in replacelist:
            line = line.replace(r[0], r[1])
        fd2.write(line)
    fd1.close()
    fd2.close()

# find the token after s2 in s1
def get_token_after_string(s1, s2):
    if s2 not in s1:
        return None
    else:
        return s1[s1.find(s2)+len(s2):].split()[0]

# Convert time string to second.  The time string is in the format of
# 00:01:00.12345. The .12345 part will be discarded
def convert_timestring_to_second(s):
    x = time.strptime(s.split('.')[0],'%H:%M:%S')
    return x.tm_hour * 60 * 60 + x.tm_min * 60 + x.tm_sec; 

def tgtTR():
    if ArgList._target_type == 'TR':
        return True
    else:
        return False

def tgtSQ():
    if ArgList._target_type == 'SQ':
        return True
    else:
        return False
 

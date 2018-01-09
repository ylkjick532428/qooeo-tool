# -*- coding: utf-8 -*-
'''

'''

import sys
import os
import json
import re
import tempfile
import platform

from subprocess import Popen, PIPE
from plan.commands import Echo
from plan._compat import get_binary_content

class CrontabUtils(object):
    '''
    classdocs
    '''
    def __init__(self, ):
        '''
        Constructor
        '''
        self.name = "vastio"
        self.user = None
        self.crons = []
        self.envs = {}
        
    #===========================================================================
    # add_cron
    #===========================================================================
    def add_cron(self, tmp_cron):
        self.crons.append(tmp_cron)
        
    #===============================================================================
    # communicate_process
    #===============================================================================
    def communicate_process(self, command, stdin=None, *args, **kwargs):
        """Run the command described by command, then interact with process.
    
        :param stdin: the data you want to send to stdin.
        :return: a tuple of stdout, stderr and returncode
        """
        p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, *args, **kwargs)
        output, error = p.communicate(stdin)
        returncode = p.returncode
        return output, error, returncode

    #===========================================================================
    # read_crontab
    #===========================================================================
    def read_crontab(self):
            """Get the current working crontab cronfile content."""
            command = ['crontab', '-l']
            if self.user:
                command.extend(["-u", str(self.user)])
            try:
                r = self.communicate_process(command, universal_newlines=True)
                output, error, returncode = r
                if returncode != 0:
                    raise ("couldn't read crontab")
            except OSError:
                raise ("couldn't read crontab; please make sure you "
                            "have crontab installed")
            return output
    
    #===========================================================================
    # comment_begin
    #===========================================================================
    @property
    def comment_begin(self):
            """Comment begin content for this object, this will be added before
            the actual cron syntax jobs content.  Different name is used to
            distinguish different Plan object, so we can locate the cronfile
            content corresponding to this object.
            """
            return "# Begin Plan generated jobs for: %s" % self.name
    
    #===========================================================================
    # comment_end
    #===========================================================================
    @property
    def comment_end(self):
        return "# End Plan generated jobs for: %s" % self.name
    
    #===========================================================================
    # _write_to_crontab
    #===========================================================================
    def _write_to_crontab(self, action, content):
        """The inside method used to modify the current crontab cronfile.
        This will write the content into current crontab cronfile.

        :param action: the action that is done, could be written, updated or
                       cleared.
        :param content: the content that is written to the crontab cronfile.
        """
        # make sure at most 3 '\n' in a row
        content = re.sub(r'\n{4,}', r'\n\n\n', content)
        # strip
        content = content.strip()
        if content:
            content += "\n"

        tmp_cronfile = tempfile.NamedTemporaryFile()
        tmp_cronfile.write(get_binary_content(content))
        tmp_cronfile.flush()

        # command used to write crontab
        # $ crontab -u username cronfile
        command = ['crontab']
        if self.user:
            command.extend(["-u", str(self.user)])
        command.append(tmp_cronfile.name)

        try:
            output, error, returncode = self.communicate_process(command)
            if returncode != 0:
                raise ("couldn't write crontab; try running check to "
                                "ensure your cronfile is valid.")
        except OSError:
            raise ("couldn't write crontab; please make sure you "
                            "have crontab installed")
        else:
            if action:
                Echo.write("crontab file %s" % action)
        finally:
            tmp_cronfile.close()

    #===========================================================================
    # environment_variables
    #===========================================================================
    @property
    def environment_variables(self):
        """Return a list of crontab environment settings's cron syntax
        content.

        .. versionadded:: 0.5
        """
        variables = []
        for variable, value in self.envs.items():
            if value is not None:
                value = '"%s"' % str(value)
                variables.append("%s=%s" % (str(variable), value))
        return variables
    
    #===========================================================================
    # cron_content
    #===========================================================================
    @property
    def cron_content(self):
        """Your schedule jobs converted to cron syntax."""
        return "\n".join([self.comment_begin] + self.environment_variables +
                         self.crons + [self.comment_end]) + "\n"

    #===========================================================================
    # env
    #===========================================================================
    def env(self, variable, value):
        """Add one environment variable for this Plan object in the crontab.
    
        .. versionadded:: 0.5
    
        :param variable: environment variable name.
        :param value: environment variable value.
        """
        self.envs[variable] = value
                                 
    #===========================================================================
    # update_crontab
    #===========================================================================
    def update_crontab(self):
        """Update the current cronfile, used by run_type `update` or `clear`.
        This will find the block inside cronfile corresponding to this Plan
        object and replace it.

        :param update_type: update or clear, if you choose update, the block
                            corresponding to this plan object will be replaced
                            with the new cron job entries, otherwise, they
                            will be wiped.
        """
        if platform.system() == "Linux":
            current_crontab = self.read_crontab()
        else:
            #Windows用于测试
            current_crontab = "\n".join([self.comment_begin, "", self.comment_end]) + "\n"
            
        action = "updated"
        crontab_content = self.cron_content
        # Check for unbegined or unended block
        comment_begin_re = re.compile(r"^%s$" % self.comment_begin, re.M)
        comment_end_re = re.compile(r"^%s$" % self.comment_end, re.M)
        cron_block_re = re.compile(r"^%s$.+^%s$" %
                                   (self.comment_begin, self.comment_end),
                                   re.M | re.S)

        comment_begin_match = comment_begin_re.search(current_crontab)
        comment_end_match = comment_end_re.search(current_crontab)

        if comment_begin_match and not comment_end_match:
            raise ("Your crontab file is not ended, it contains "
                            "'%s', but no '%s'" % (self.comment_begin,
                                                   self.comment_end))
        elif not comment_begin_match and comment_end_match:
            raise ("Your crontab file has no begining, it contains "
                            "'%s', but no '%s'" % (self.comment_end,
                                                   self.comment_begin))

        # Found our existing block and replace it with the new one
        # Otherwise, append out new cron jobs after others
        if comment_begin_match and comment_end_match:
            updated_content = cron_block_re.sub(crontab_content,
                                                current_crontab)
        else:
            updated_content = "\n\n".join((current_crontab, crontab_content))

        # Write the updated cronfile back to crontab
        print (updated_content)
        if platform.system() == "Linux":
            self._write_to_crontab(action, updated_content)
        
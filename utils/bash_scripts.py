import subprocess
from .log import write_to_log


def get_pid_by_name(name):
    bash_command = "ps -eaf | grep -v grep | grep %s " \
                   "| grep -v $$ | awk '{ print $2 }'" % name
    output = subprocess.check_output(['bash', '-c', bash_command])
    write_to_log('Getting PID for %s' % name)
    return output


def kill_process(pid):
    bash_command = "kill -SIGKILL %s" % int(pid)
    subprocess.Popen(bash_command.split())
    write_to_log('Process %s was killed' % pid)


def run_phantomjs():
    bash_command = 'nohup $OPENSHIFT_DATA_DIR/phantomjs/bin/phantomjs ' \
                   '--webdriver=$OPENSHIFT_PYTHON_IP:15005 > ' \
                   '$OPENSHIFT_PYTHON_LOG_DIR/nohup_for_scheduler.out 2>&1&'
    subprocess.Popen(bash_command.split())
    write_to_log('Phantomjs was started with PID %s' % get_pid_by_name('pahntomjs'))


def kill_phantom_js():
    kill_process(get_pid_by_name('phantomjs'))
    write_to_log('Phantomjs was killed')

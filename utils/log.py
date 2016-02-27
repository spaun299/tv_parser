import os
from .date_and_time import get_date_and_time_with_timezone
import sys
import traceback


def write_to_log(message=None, error=None):
    if os.environ.get('OPENSHIFT_PYTHON_LOG_DIR'):
        date_time = get_date_and_time_with_timezone(time=True)
        file = open(os.environ.get('OPENSHIFT_PYTHON_LOG_DIR') + 'python_log.log', 'a')
        text = '[%s] :   ' % date_time
        if error:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb)
            tb_info = traceback.extract_tb(tb)
            filename_, line_, func_, text_ = tb_info[-1]
            message = 'Error. ' \
                      'An error occurred on File "{file}" line {line}\n {assert_message}'.\
                format(line=line_, assert_message=error.args, file=filename_)
        text += message
        file.write(text + '\n')
        file.close()
    else:
        return

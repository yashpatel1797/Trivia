#!"d:\app\fsnd\trivia api\trivia-api\backend\env\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'migrate==0.3.7','console_scripts','migrate'
__requires__ = 'migrate==0.3.7'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('migrate==0.3.7', 'console_scripts', 'migrate')()
    )

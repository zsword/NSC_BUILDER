#!/bin/bash

print_logo() {
echo "                                        __          _ __    __         "
echo "                  ____  _____ ____     / /_  __  __(_) /___/ /__  _____"
echo "                 / __ \/ ___/ ___/    / __ \/ / / / / / __  / _ \/ ___/"
echo "                / / / (__  ) /__     / /_/ / /_/ / / / /_/ /  __/ /    "
echo "               /_/ /_/____/\___/____/_.___/\__,_/_/_/\__,_/\___/_/     "
echo "                              /_____/                                   "
echo "-------------------------------------------------------------------------------------"
echo "                         NINTENDO SWITCH CLEANER AND BUILDER"
echo "                      (THE XCI MULTI CONTENT BUILDER AND MORE)"
echo "-------------------------------------------------------------------------------------"
echo "=============================     BY JULESONTHEROAD     ============================="
echo "-------------------------------------------------------------------------------------"

exit 0
}

alias pycommand=python3
if command -v python >/dev/null 2>&1; then
  alias pycommand=python
fi
op_file="$(dirname "$0")/zconfig/NSCB_options.sh"

echo "pycommand"

if [ -f "$op_file" ]; then
    source "$op_file"
fi

echo
echo "Installing dependencies"
echo
pip install --upgrade pip
pip install wheel
pip install urllib3 unidecode tqdm bs4 requests pillow pycryptodome pykakasi googletrans==4.0.0-rc1 chardet eel bottle zstandard colorama google-auth-httplib2 google-auth-oauthlib oauth2client comtypes
pip install pywin32 windows-curses
pip install --upgrade google-api-python-client
echo
echo "**********************************************************************************"
echo "---IMPORTANT: Check if dependencies were installed correctly before continuing---"
echo "**********************************************************************************"
echo
read -p "Press [Enter] key to continue..."

exit 0

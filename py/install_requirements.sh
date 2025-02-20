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

#!/bin/bash

pycommand="python3"
op_file="$(dirname "$0")/zconfig/NSCB_options.sh"


if [ -f "$op_file" ]; then
    source "$op_file"
fi

echo
echo "Installing dependencies"
echo
$pycommand -m pip install --upgrade pip
$pycommand -m pip install wheel
$pycommand -m pip install urllib3 unidecode tqdm bs4 requests pillow pywin32 pycryptodome pykakasi googletrans==4.0.0-rc1 chardet eel bottle zstandard colorama google-auth-httplib2 google-auth-oauthlib windows-curses oauth2client comtypes
$pycommand -m pip install --upgrade google-api-python-client
echo
echo "**********************************************************************************"
echo "---IMPORTANT: Check if dependencies were installed correctly before continuing---"
echo "**********************************************************************************"
echo
read -p "Press [Enter] key to continue..."

exit 0

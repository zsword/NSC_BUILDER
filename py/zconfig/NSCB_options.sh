# SET CUSTOM COLOR FOR THE BATCH FILES
# color 1F  # This is for Windows, ignoring in macOS

# -----------------------------------------------
# OPTION 1: FOLDERS
# -----------------------------------------------
w_folder="NSCB_temp"
fold_output="NSCB_output"
zip_Fold="NSCB_zips"  # Original variable name was "zip Fold"

# -----------------------------------------------
# OPTION 2: PROGRAM ROUTES
# -----------------------------------------------
nut="ztools/squirrel.py"
xci_lib="ztools/XCI.sh"
nsp_lib="ztools/NSP.sh"
zip="ztools/squirrel.py"
listmanager="ztools/squirrel.py"
batconfig="ztools/NSCB_config.sh"
batdepend="ztools/install_dependencies.sh"
infobat="ztools/info.sh"

# -----------------------------------------------
# OPTION 3: SQUIRREL OPTIONS
# -----------------------------------------------
pycommand="py -3"  # In macOS, this might need to be "python3"
buffer="-b 65536"
nf_cleaner="--C_clean_ND"
skdelta="-ND true"
patchRSV="-pv false"
capRSV="--RSVcap 268435656"

# -----------------------------------------------
# OPTION 4: IMPORTANT FILES
# -----------------------------------------------
uinput="ztools/uinput"
dec_keys="ztools/keys.txt"

# -----------------------------------------------
# OPTION 5: REPACK OPTIONS
# -----------------------------------------------
vrepack="both"
fi_rep="multi"

# -----------------------------------------------
# OPTION 6: MANUAL MODE INTRO
# -----------------------------------------------
manual_Intro="choose"  # Original variable name was "manual Intro"

# -----------------------------------------------
# OPTION 7: Zip files
# -----------------------------------------------
zip_restore="false"

# -----------------------------------------------
# OPTION 8: PATCH IF KEYGENERATION IS BIGGER THAN
# -----------------------------------------------
vkey="-kp false"

# -----------------------------------------------
# OPTION 10: AUTO-EXIT
# -----------------------------------------------
va_exit="false"

# -----------------------------------------------
# OPTION 11: SKIP RSV AND KEYGENERATION CHANGE PROPMT
# -----------------------------------------------
skipRSVprompt="false"

# -----------------------------------------------
# OPTION 12: SD FORMAT
# -----------------------------------------------
fatype="-fat exfat"
fexport="-fx files"

# -----------------------------------------------
# OPTION 13: END FOLDER ORGANIZATION
# -----------------------------------------------
oforg="inline"

# -----------------------------------------------
# OPTION 14: NEW OR LEGACY
# -----------------------------------------------
NSBMODE="new"

# -----------------------------------------------
# OPTION 15: ROMANIZE JAPANESE AND CHINESE TITLES
# -----------------------------------------------
romaji="TRUE"

# -----------------------------------------------
# OPTION 16: TRANSLATE NUTDB DESCRIPTIONS FROM ASIAN REGIONS
# -----------------------------------------------
transnutdb="FALSE"

# -----------------------------------------------
# OPTION 17: WORKERS FOR MULTI-THREADING
# -----------------------------------------------
workers="-threads 1"

# -----------------------------------------------
# OPTION 18: NSZ user options
# -----------------------------------------------
compression_lv="17"
compression_threads="0"
xci_export="xcz"

# -----------------------------------------------
# MTP
# -----------------------------------------------
MTP="ztools bin/nscb_mtp.exe"
MTP_verification="True"
MTP_prioritize_NSZ="True"
MTP_exclude_xci_autinst="True"
MTP_aut_ch_medium="True"
MTP_chk_fw="False"
MTP_prepatch_kg="False"
MTP_prechk_Base="True"
MTP_prechk_Upd="False"
MTP_saves_Inline="False"
MTP_saves_AddTIDandVer="False"
MTP_pdrive_truecopy="True"
MTP_stc_installs="False"
MTP_ptch_inst_spec="spec1"

# -----------------------------------------------
# Lib_call
# -----------------------------------------------
squirrel_lb="ztools/squirrel_lib_call.py"
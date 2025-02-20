Below is the shell script equivalent of the provided BAT script, designed to configure options for the Nintendo Switch Cleaner and Builder (NSCB) program. This conversion replaces BAT-specific constructs (like goto and set /p) with shell script equivalents (such as functions, read, and case statements), while maintaining the menu-driven interface and functionality.
Shell Script Conversion
bash
#!/bin/bash

# Define variables from command-line arguments
op_file="$1"
listmanager="$2"
batdepend="$3"
pycommand="python"  # Adjust to your Python interpreter path
squirrel="ztools/squirrel.py"  # Example path; adjust as needed
squirrel_lb="ztools/squirrel_lb.py"  # Example path; adjust as needed
dec_keys="zconfig/dec_keys.txt"  # Example path; adjust as needed
opt_interface="zconfig/interface_options.txt"  # Example path; adjust as needed
opt_server="zconfig/server_options.txt"  # Example path; adjust as needed

# Function to display the logo
logo() {
    echo "                                        __          _ __    __"
    echo "                  ____  _____ ____     / /_  __  __(_) /___/ /__  _____"
    echo "                 / __ \/ ___/ ___/    / __ \/ / / / / / __  / _ \/ ___/"
    echo "                / / / (__  ) /__     / /_/ / /_/ / / / /_/ /  __/ /"
    echo "               /_/ /_/____/\___/____/_.___/\__,_/_/_/\__,_/\___/_/"
    echo "                              /_____/"
    echo "-------------------------------------------------------------------------------------"
    echo "                         NINTENDO SWITCH CLEANER AND BUILDER"
    echo "                      (THE XCI MULTI CONTENT BUILDER AND MORE)"
    echo "-------------------------------------------------------------------------------------"
    echo "=============================     BY JULESONTHEROAD     ============================="
    echo "-------------------------------------------------------------------------------------"
    echo "\"                                POWERED BY SQUIRREL                                \""
    echo "\"                    BASED ON THE WORK OF BLAWAR AND LUCA FRAGA                     \""
    echo "                                    VERSION 1.01"
    echo "-------------------------------------------------------------------------------------"
    echo "Program's github: https://github.com/julesontheroad/NSC_BUILDER"
    echo "Blawar's github:  https://github.com/blawar"
    echo "Luca Fraga's github: https://github.com/LucaFraga"
    echo "-------------------------------------------------------------------------------------"
}

# Main menu function
main_menu() {
    while true; do
        clear
        logo
        echo "********************************************************"
        echo "OPTION - CONFIGURATION"
        echo "********************************************************"
        echo "Input \"1\" for AUTO-MODE OPTIONS"
        echo "Input \"2\" for GLOBAL AND MANUAL OPTIONS"
        echo "Input \"3\" to VERIFY KEYS.TXT"
        echo "Input \"4\" to UPDATE NUTDB"
        echo "Input \"5\" for INTERFACE OPTIONS"
        echo "Input \"6\" for SERVER OPTIONS"
        echo "Input \"7\" for GOOGLE DRIVE OPTIONS"
        echo "Input \"8\" for MTP OPTIONS"
        echo ""
        echo "Input \"c\" to read CURRENT PROFILE"
        echo "Input \"d\" to set DEFAULT SETTINGS"
        echo "Input \"0\" to go back to the MAIN PROGRAM"
        echo "......................................................."
        echo ""
        read -p "Enter your choice: " choice
        case "$choice" in
            1) auto_mode_options ;;
            2) global_options ;;
            3) verify_keys ;;
            4) update_nutdb ;;
            5) interface_options ;;
            6) server_options ;;
            7) google_drive_options ;;
            8) mtp_options ;;
            c|C) 
                curr_set1
                curr_set2
                echo ""
                read -p "Press Enter to continue"
                ;;
            d|D) 
                def_set1
                def_set2
                echo ""
                read -p "Press Enter to continue"
                ;;
            0) return ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                ;;
        esac
    done
}

# Auto-mode options menu
auto_mode_options() {
    while true; do
        clear
        logo
        echo "********************************************************"
        echo "AUTO-MODE - CONFIGURATION"
        echo "********************************************************"
        echo "Input \"1\" to change REPACK configuration"
        echo "Input \"2\" to change FOLDER'S TREATMENT"
        echo "Input \"3\" to change RSV patching configuration"
        echo "Input \"4\" to change KEYGENERATION configuration"
        echo ""
        echo "Input \"c\" to read CURRENT AUTO-MODE SETTINGS"
        echo "Input \"d\" to set DEFAULT AUTO-MODE SETTINGS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "......................................................."
        echo ""
        read -p "Enter your choice: " choice
        case "$choice" in
            1) op_repack ;;
            2) op_pfolder ;;
            3) op_RSV ;;
            4) op_KGEN ;;
            c|C) 
                curr_set1
                echo ""
                read -p "Press Enter to continue"
                ;;
            d|D) 
                def_set1
                echo ""
                read -p "Press Enter to continue"
                return
                ;;
            0) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                ;;
        esac
    done
}

# Repack configuration
op_repack() {
    while true; do
        clear
        logo
        echo "*******************************************************"
        echo "REPACK configuration"
        echo "*******************************************************"
        echo "REPACK OPTION FOR AUTO-MODE"
        echo "......................................................."
        echo "Input \"1\" to repack as NSP"
        echo "Input \"2\" to repack as XCI"
        echo "Input \"3\" to repack as BOTH"
        echo "Input \"4\" to remove DELTAS from updates"
        echo "Input \"5\" to REBUILD NSPS by cnmt order"
        echo ""
        echo "Input \"b\" to return to AUTO-MODE - CONFIGURATION"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "......................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_rep="none"
        case "$choice" in
            1) v_rep="nsp" ;;
            2) v_rep="xci" ;;
            3) v_rep="both" ;;
            4) v_rep="nodelta" ;;
            5) v_rep="rebuild" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_rep" != "none" ]; then
            v_rep="vrepack=$v_rep"
            $pycommand "$listmanager" -cl "$op_file" -ln "57" -nl "set \"$v_rep\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "57" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Folder treatment configuration
op_pfolder() {
    while true; do
        clear
        logo
        echo "**********************************************************************"
        echo "FOLDER'S TREATMENT"
        echo "**********************************************************************"
        echo "HOW TO TREAT FOLDER'S IN AUTO-MODE"
        echo "......................................................................"
        echo "Input \"1\" to repack folder's files individually (single-content file)"
        echo "Input \"2\" to repack folder's files together (multi-content file)"
        echo "Input \"3\" to repack folder's files by BASE ID"
        echo ""
        echo "Input \"b\" to return to AUTO-MODE - CONFIGURATION"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "......................................................................"
        echo ""
        read -p "Enter your choice: " choice
        v_fold="none"
        case "$choice" in
            1) v_fold="indiv" ;;
            2) v_fold="multi" ;;
            3) v_fold="baseid" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_fold" != "none" ]; then
            v_fold="fi_rep=$v_fold"
            $pycommand "$listmanager" -cl "$op_file" -ln "61" -nl "set \"$v_fold\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "61" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# RSV patching configuration
op_RSV() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "REQUIRED SYSTEM VERSION PATCHING"
        echo "***************************************************************************"
        echo "PATCH REQUIRED_SYSTEM_VERSION IN THE META NCA (AUTO-MODE)"
        echo "..........................................................................."
        echo "Patches the RequiredSystemVersion so console doesn't ask for updates bigger"
        echo "the required FW to decipher the crypto"
        echo ""
        echo "Input \"1\" to PATCH Required System Version in the meta nca"
        echo "Input \"2\" to leave Required System Version UNCHANGED"
        echo ""
        echo "Input \"b\" to return to AUTO-MODE - CONFIGURATION"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_RSV="none"
        case "$choice" in
            1) v_RSV="-pv true" ;;
            2) v_RSV="-pv false" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_RSV" != "none" ]; then
            v_RSV="patchRSV=$v_RSV"
            $pycommand "$listmanager" -cl "$op_file" -ln "41" -nl "set \"$v_RSV\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "41" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Keygeneration configuration
op_KGEN() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "PATCH IF KEYGENERATION IS BIGGER THAN"
        echo "***************************************************************************"
        echo "CHANGE KEYGENERATION IF BIGGER THAN THE SET NUMBER (AUTO-MODE)"
        echo "..........................................................................."
        echo "Changes the keygeneration and recalculates the keyblock to use a lower"
        echo "masterkey to decrypt the nca."
        echo ""
        echo "Input \"f\" to not change the keygeneration"
        echo "Input \"0\" to change top keygeneration to 0 (FW 1.0)"
        echo "Input \"1\" to change top keygeneration to 1 (FW 2.0-2.3)"
        echo "Input \"2\" to change top keygeneration to 2 (FW 3.0)"
        echo "Input \"3\" to change top keygeneration to 3 (FW 3.0.1-3.02)"
        echo "Input \"4\" to change top keygeneration to 4 (FW 4.0.0-4.1.0)"
        echo "Input \"5\" to change top keygeneration to 5 (FW 5.0.0-5.1.0)"
        echo "Input \"6\" to change top keygeneration to 6 (FW 6.0.0-6.1.0)"
        echo "Input \"7\" to change top keygeneration to 7 (FW 6.2.0)"
        echo "Input \"8\" to change top keygeneration to 8 (FW 7.0.0-8.0.1)"
        echo "Input \"9\" to change top keygeneration to 9 (FW 8.1.0)"
        echo "Input \"10\" to change top keygeneration to 10 (FW 9.0.0-9.01)"
        echo "Input \"11\" to change top keygeneration to 11 (FW 9.1.0-11.0.3)"
        echo "Input \"12\" to change top keygeneration to 12 (FW 12.1.0)"
        echo "Input \"13\" to change top keygeneration to 13 (>FW 13.0.0)"
        echo ""
        echo "Input \"b\" to return to AUTO-MODE - CONFIGURATION"
        echo "Input \"c\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_KGEN="none"
        v_CAPRSV=""
        case "$choice" in
            f|F) v_KGEN="-kp false" ;;
            0) v_KGEN="-kp 0"; v_CAPRSV="--RSVcap 0" ;;
            1) v_KGEN="-kp 1"; v_CAPRSV="--RSVcap 65796" ;;
            2) v_KGEN="-kp 2"; v_CAPRSV="--RSVcap 201327002" ;;
            3) v_KGEN="-kp 3"; v_CAPRSV="--RSVcap 201392178" ;;
            4) v_KGEN="-kp 4"; v_CAPRSV="--RSVcap 268435656" ;;
            5) v_KGEN="-kp 5"; v_CAPRSV="--RSVcap 335544750" ;;
            6) v_KGEN="-kp 6"; v_CAPRSV="--RSVcap 402653494" ;;
            7) v_KGEN="-kp 7"; v_CAPRSV="--RSVcap 404750336" ;;
            8) v_KGEN="-kp 8"; v_CAPRSV="--RSVcap 469762048" ;;
            9) v_KGEN="-kp 9"; v_CAPRSV="--RSVcap 537919488" ;;
            10) v_KGEN="-kp 10"; v_CAPRSV="--RSVcap 603979776" ;;
            11) v_KGEN="-kp 11"; v_CAPRSV="--RSVcap 605028352" ;;
            12) v_KGEN="-kp 12"; v_CAPRSV="--RSVcap 806354944" ;;
            13) v_KGEN="-kp 13"; v_CAPRSV="--RSVcap 872415232" ;;
            b|B) return ;;
            c|C) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_KGEN" != "none" ]; then
            v_KGEN="vkey=$v_KGEN"
            v_CAPRSV="capRSV=$v_CAPRSV"
            $pycommand "$listmanager" -cl "$op_file" -ln "95" -nl "set \"$v_KGEN\""
            $pycommand "$listmanager" -cl "$op_file" -ln "42" -nl "set \"$v_CAPRSV\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "95" -nl "Line in config was changed to: "
            $pycommand "$listmanager" -rl "$op_file" -ln "42" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Global options menu
global_options() {
    while true; do
        clear
        logo
        echo "**********************************************"
        echo "GLOBAL OPTIONS - CONFIGURATION"
        echo "**********************************************"
        echo "Input \"1\" to change text and background COLOR"
        echo "Input \"2\" to change WORK FOLDER's name"
        echo "Input \"3\" to change OUTPUT FOLDER's name"
        echo "Input \"4\" to change DELTA files treatment"
        echo "Input \"5\" to change ZIP configuration (LEGACY)"
        echo "Input \"6\" to change AUTO-EXIT configuration"
        echo "Input \"7\" to skip KEY-GENERATION PROMPT"
        echo "Input \"8\" to set file stream BUFFER"
        echo "Input \"9\" to set file FAT32\\EXFAT options"
        echo "Input \"10\" to how to ORGANIZE output files"
        echo "Input \"11\" to set NEW MODE OR LEGACY MODE"
        echo "Input \"12\" to ROMANIZE names when using direct-multi"
        echo "Input \"13\" to TRANSLATE game description lines in file info"
        echo "Input \"14\" to change number of WORKERS IN THREADED OPERATIONS (TEMPORARILY DISABLED)"
        echo "Input \"15\" to setup NSZ COMPRESSION USER PRESET"
        echo "Input \"16\" to setup COMPRESSED XCI EXPORT FORMAT"
        echo ""
        echo "Input \"c\" to read CURRENT GLOBAL SETTINGS"
        echo "Input \"d\" to set DEFAULT GLOBAL SETTINGS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        case "$choice" in
            1) op_color ;;
            2) op_wfolder ;;
            3) op_ofolder ;;
            4) op_delta ;;
            5) op_zip ;;
            6) op_aexit ;;
            7) op_kgprompt ;;
            8) op_buffer ;;
            9) op_fat ;;
            10) op_oforg ;;
            11) op_nscbmode ;;
            12) op_romanize ;;
            13) op_translate ;;
            14) op_threads ;;
            15) op_NSZ1 ;;
            16) op_NSZ3 ;;
            c|C) 
                curr_set2
                echo ""
                read -p "Press Enter to continue"
                ;;
            d|D) 
                def_set2
                echo ""
                read -p "Press Enter to continue"
                return
                ;;
            0) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                ;;
        esac
    done
}

# Color configuration
op_color() {
    clear
    logo
    echo "********************************************************"
    echo "COLOR - CONFIGURATION"
    echo "********************************************************"
    echo "--------------------------------------------------------"
    echo "FOREGROUND COLOR (TEXT COLOR)"
    echo "--------------------------------------------------------"
    echo "Input \"1\" to change text color to BRIGHT WHITE (DEFAULT)"
    echo "Input \"2\" to change text color to BLACK"
    echo "Input \"3\" to change text color to BLUE"
    echo "Input \"4\" to change text color to GREEN"
    echo "Input \"5\" to change text color to AQUA"
    echo "Input \"6\" to change text color to RED"
    echo "Input \"7\" to change text color to PURPLE"
    echo "Input \"8\" to change text color to YELLOW"
    echo "Input \"9\" to change text color to WHITE"
    echo "Input \"10\" to change text color to GRAY"
    echo "Input \"11\" to change text color to LIGHT BLUE"
    echo "Input \"12\" to change text color to LIGHT GREEN"
    echo "Input \"13\" to change text color to LIGHT AQUA"
    echo "Input \"14\" to change text color to LIGHT RED"
    echo "Input \"15\" to change text color to LIGHT PURPLE"
    echo "Input \"16\" to change text color to LIGHT YELLOW"
    echo ""
    echo "Input \"d\" to set default color configuration"
    echo "Input \"b\" to return to GLOBAL OPTIONS"
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " choice_fg
    v_colF="F"
    case "$choice_fg" in
        1) v_colF="F" ;;
        2) v_colF="0" ;;
        3) v_colF="3" ;;
        4) v_colF="1" ;;
        5) v_colF="2" ;;
        6) v_colF="4" ;;
        7) v_colF="5" ;;
        8) v_colF="6" ;;
        9) v_colF="7" ;;
        10) v_colF="8" ;;
        11) v_colF="9" ;;
        12) v_colF="A" ;;
        13) v_colF="B" ;;
        14) v_colF="C" ;;
        15) v_colF="D" ;;
        16) v_colF="E" ;;
        d|D) 
            v_colF="F"
            v_colB="1"
            v_col="${v_colB}${v_colF}"
            $pycommand "$listmanager" -cl "$op_file" -ln "3" -nl "color $v_col"
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "3" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
            ;;
        b|B) return ;;
        0) main_menu ;;
        e|E) exit 0 ;;
        *) ;;
    esac

    echo "-----------------------------------------------------"
    echo "BACKGROUND COLOR"
    echo "-----------------------------------------------------"
    echo "Input \"1\" to change background color to BLUE (DEFAULT)"
    echo "Input \"2\" to change background color to BLACK"
    echo "Input \"3\" to change background color to GREEN"
    echo "Input \"4\" to change background color to AQUA"
    echo "Input \"5\" to change background color to RED"
    echo "Input \"6\" to change background color to PURPLE"
    echo "Input \"7\" to change background color to YELLOW"
    echo "Input \"8\" to change background color to WHITE"
    echo "Input \"9\" to change background color to GRAY"
    echo "Input \"10\" to change background color to BRIGHT WHITE"
    echo "Input \"11\" to change background color to LIGHT BLUE"
    echo "Input \"12\" to change background color to LIGHT GREEN"
    echo "Input \"13\" to change background color to LIGHT AQUA"
    echo "Input \"14\" to change background color to LIGHT RED"
    echo "Input \"15\" to change background color to LIGHT PURPLE"
    echo "Input \"16\" to change background color to LIGHT YELLOW"
    echo ""
    echo "Input \"d\" to set default color configuration"
    echo "Input \"b\" to return to GLOBAL OPTIONS"
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " choice_bg
    v_colB="1"
    case "$choice_bg" in
        1) v_colB="1" ;;
        2) v_colB="0" ;;
        3) v_colB="2" ;;
        4) v_colB="3" ;;
        5) v_colB="4" ;;
        6) v_colB="5" ;;
        7) v_colB="6" ;;
        8) v_colB="7" ;;
        9) v_colB="8" ;;
        10) v_colB="F" ;;
        11) v_colB="9" ;;
        12) v_colB="A" ;;
        13) v_colB="B" ;;
        14) v_colB="C" ;;
        15) v_colB="D" ;;
        16) v_colB="E" ;;
        d|D) 
            v_colF="F"
            v_colB="1"
            ;;
        b|B) return ;;
        0) main_menu ;;
        e|E) exit 0 ;;
        *) ;;
    esac

    v_col="${v_colB}${v_colF}"
    $pycommand "$listmanager" -cl "$op_file" -ln "3" -nl "color $v_col"
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "3" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
}

# Work folder configuration
op_wfolder() {
    clear
    logo
    echo "***********************************"
    echo "WORK FOLDER's name - CONFIGURATION"
    echo "***********************************"
    echo "Input \"1\" to set default work folder's name"
    echo ""
    echo "Input \"b\" to return to GLOBAL OPTIONS"
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Or type a new name: " choice
    v_wf="$choice"
    case "$choice" in
        1) v_wf="NSCB_temp" ;;
        b|B) return ;;
        0) main_menu ;;
        e|E) exit 0 ;;
        *) ;;
    esac

    v_wf="w_folder=$v_wf"
    $pycommand "$listmanager" -cl "$op_file" -ln "8" -nl "set \"$v_wf\""
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "8" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
}

# Output folder configuration
op_ofolder() {
    clear
    logo
    echo "*************************************"
    echo "OUTPUT FOLDER's name - CONFIGURATION"
    echo "*************************************"
    echo "Input \"1\" to set default output folder's name"
    echo ""
    echo "Input \"b\" to return to GLOBAL OPTIONS"
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Or type a new name: " choice
    v_of="$choice"
    case "$choice" in
        1) v_of="NSCB_output" ;;
        b|B) return ;;
        0) main_menu ;;
        e|E) exit 0 ;;
        *) ;;
    esac

    v_of="fold_output=$v_of"
    $pycommand "$listmanager" -cl "$op_file" -ln "10" -nl "set \"$v_of\""
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "10" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
}

# Delta files treatment configuration
op_delta() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "DELTA files treatment - CONFIGURATION"
        echo "***************************************************************************"
        echo "SKIP DELTA NCA FILES WHEN EXTRACTING UPDATES"
        echo "..........................................................................."
        echo "The deltas serve to convert previous updates into new ones, updates can"
        echo "incorporate the full update + deltas. Deltas are nocive and unnecessary"
        echo "for xci, while they serve to install faster nsp and convert previous"
        echo "updates to the new one. Without deltas your old update will stay in the"
        echo "system and you'll need to uninstall it."
        echo ""
        echo "Input \"1\" to skip deltas (default configuration)"
        echo "Input \"2\" to repack deltas"
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_delta="none"
        v_delta2_=""
        case "$choice" in
            1) 
                v_delta="--C_clean_ND"
                v_delta2_="-ND true"
                ;;
            2) 
                v_delta="--C_clean"
                v_delta2_="-ND false"
                ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_delta" != "none" ]; then
            v_delta="nf_cleaner=$v_delta"
            v_delta2_="skdelta=$v_delta2_"
            $pycommand "$listmanager" -cl "$op_file" -ln "36" -nl "set \"$v_delta\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "36" -nl "Line in config was changed to: "
            $pycommand "$listmanager" -cl "$op_file" -ln "37" -nl "set \"$v_delta2_\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "37" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Zip configuration
op_zip() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "ZIP FILES GENERATION"
        echo "***************************************************************************"
        echo "GENERATE ZIP FILES WITH KEYBLOCK AND FILE INFORMATION"
        echo "..........................................................................."
        echo ""
        echo "Input \"1\" to generate zip files"
        echo "Input \"2\" to not generate zip files (default configuration)"
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_gzip="none"
        case "$choice" in
            1) v_gzip="true" ;;
            2) v_gzip="false" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_gzip" != "none" ]; then
            v_gzip="zip_restore=$v_gzip"
            $pycommand "$listmanager" -cl "$op_file" -ln "78" -nl "set \"$v_gzip\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "78" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Auto-exit configuration
op_aexit() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "AUTO-EXIT CONFIGURATION (MANUAL MODES)"
        echo "***************************************************************************"
        echo "Auto exit after processing files or ask to process next."
        echo "..........................................................................."
        echo ""
        echo "Input \"1\" to set off auto-exit (default configuration)"
        echo "Input \"2\" to set on auto-exit"
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_exit="none"
        case "$choice" in
            1) v_exit="false" ;;
            2) v_exit="true" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_exit" != "none" ]; then
            v_exit="va_exit=$v_exit"
            $pycommand "$listmanager" -cl "$op_file" -ln "101" -nl "set \"$v_exit\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "101" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Key-generation prompt configuration
op_kgprompt() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "SHOW\\SKIP REQUIRED_SYSTEM_VERSION AND KEYGENERATION CHANGE PROMPT"
        echo "***************************************************************************"
        echo ""
        echo "Input \"1\" to show RSV prompt (default configuration)"
        echo "Input \"2\" to not show RSV prompt"
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        skipRSVprompt="none"
        case "$choice" in
            1) skipRSVprompt="false" ;;
            2) skipRSVprompt="true" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$skipRSVprompt" != "none" ]; then
            skipRSVprompt="skipRSVprompt=$skipRSVprompt"
            $pycommand "$listmanager" -cl "$op_file" -ln "108" -nl "set \"$skipRSVprompt\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "108" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Buffer configuration
op_buffer() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "SET BUFFER FOR COPY AND APPENDING FILES FROM\\TO NSP\\XCI"
        echo "***************************************************************************"
        echo "This option affects the speed of the process. The ideal buffer depends on"
        echo "your system. Default is set at 64kB"
        echo ""
        echo "Input \"1\"  to change BUFFER to 80kB"
        echo "Input \"2\"  to change BUFFER to 72kB"
        echo "Input \"3\"  to change BUFFER to 64kB (Default)"
        echo "Input \"4\"  to change BUFFER to 56kB"
        echo "Input \"5\"  to change BUFFER to 48kB"
        echo "Input \"6\"  to change BUFFER to 40kB"
        echo "Input \"7\"  to change BUFFER to 32kB"
        echo "Input \"8\"  to change BUFFER to 24kB"
        echo "Input \"9\"  to change BUFFER to 16kB"
        echo "Input \"10\" to change BUFFER to  8kB"
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_buffer="none"
        case "$choice" in
            1) v_buffer="-b 81920" ;;
            2) v_buffer="-b 73728" ;;
            3) v_buffer="-b 65536" ;;
            4) v_buffer="-b 57344" ;;
            5) v_buffer="-b 49152" ;;
            6) v_buffer="-b 40960" ;;
            7) v_buffer="-b 32768" ;;
            8) v_buffer="-b 24576" ;;
            9) v_buffer="-b 16384" ;;
            10) v_buffer="-b 8192" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_buffer" != "none" ]; then
            v_buffer="buffer=$v_buffer"
            $pycommand "$listmanager" -cl "$op_file" -ln "32" -nl "set \"$v_buffer\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "32" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# FAT32/EXFAT options configuration
op_fat() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "SET FAT32 FROM YOUR SD CARD TO GENERATE SPLIT FILES IF NEEDED"
        echo "***************************************************************************"
        echo "SX OS rommenu supports ns0, ns1,... files for split nsp files as well"
        echo "as 00, 01 files in an archived folder, to reflect this 2 options are given."
        echo ""
        echo "Input \"1\" to change CARD FORMAT to exfat (Default)"
        echo "Input \"2\" to change CARD FORMAT to fat32 for SX OS (xc0 and ns0 files)"
        echo "Input \"3\" to change CARD FORMAT to fat32 for all CFW (archive folder)"
        echo ""
        echo "Note: Archive folder option exports nsp files as folders and xci files"
        echo "split files."
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_fat1="none"
        v_fat2="none"
        case "$choice" in
            1) 
                v_fat1="-fat exfat"
                v_fat2="-fx files"
                ;;
            2) 
                v_fat1="-fat fat32"
                v_fat2="-fx files"
                ;;
            3) 
                v_fat1="-fat fat32"
                v_fat2="-fx folder"
                ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_fat1" != "none" ]; then
            v_fat1="fatype=$v_fat1"
            v_fat2="fexport=$v_fat2"
            $pycommand "$listmanager" -cl "$op_file" -ln "116" -nl "set \"$v_fat1\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "116" -nl "Line in config was changed to: "
            $pycommand "$listmanager" -cl "$op_file" -ln "117" -nl "set \"$v_fat2\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "117" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Output organization configuration
op_oforg() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "ORGANIZATION FORMAT FOR OUTPUT ITEMS IN OUTPUT FOLDER"
        echo "***************************************************************************"
        echo ""
        echo "Input \"1\" to organize files separately (default)"
        echo "Input \"2\" to organize files in folders set by content"
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_oforg="none"
        case "$choice" in
            1) v_oforg="inline" ;;
            2) v_oforg="subfolder" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_oforg" != "none" ]; then
            v_oforg="oforg=$v_oforg"
            $pycommand "$listmanager" -cl "$op_file" -ln "125" -nl "set \"$v_oforg\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "125" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# NSCB mode configuration
op_nscbmode() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "START PROGRAM WITH NEW MODE OR LEGACY MODE"
        echo "***************************************************************************"
        echo ""
        echo "Input \"1\" to start with NEW MODE (default)"
        echo "Input \"2\" to start with LEGACY MODE"
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_nscbmode="none"
        case "$choice" in
            1) v_nscbmode="new" ;;
            2) v_nscbmode="legacy" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_nscbmode" != "none" ]; then
            v_nscbmode="NSBMODE=$v_nscbmode"
            $pycommand "$listmanager" -cl "$op_file" -ln "132" -nl "set \"$v_nscbmode\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "132" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Romanize configuration
op_romanize() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "ROMANIZE RESULTING NAMES FOR DIRECT MULTI FUNCTION"
        echo "***************************************************************************"
        echo ""
        echo "Input \"1\" to convert Japanese\\Asian names to ROMAJI (default)"
        echo "Input \"2\" to keep names as read on PREVALENT BASEFILE"
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_roma="none"
        case "$choice" in
            1) v_roma="TRUE" ;;
            2) v_roma="FALSE" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_roma" != "none" ]; then
            v_roma="romaji=$v_roma"
            $pycommand "$listmanager" -cl "$op_file" -ln "139" -nl "set \"$v_roma\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "139" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Translate configuration
op_translate() {
    while true; do
        clear
        logo
        echo "*****************************************************************************"
        echo "TRANSLATE GAME DESCRIPTION LINES TO ENGLISH FROM JAPANESE, CHINESE, KOREAN"
        echo "*****************************************************************************"
        echo ""
        echo "NOTE: Unlike romaji for translations NSCB makes API calls to GOOGLE TRANSLATE"
        echo ""
        echo "Input \"1\" to translate descriptions (default)"
        echo "Input \"2\" to keep descriptions as read on nutdb files"
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_trans="none"
        case "$choice" in
            1) v_trans="TRUE" ;;
            2) v_trans="FALSE" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_trans" != "none" ]; then
            v_trans="transnutdb=$v_trans"
            $pycommand "$listmanager" -cl "$op_file" -ln "147" -nl "set \"$v_trans\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "147" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Workers configuration
op_threads() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "SET NUMBER OF WORKERS FOR THREADED OPERATIONS"
        echo "***************************************************************************"
        echo "Currently used in the renamer and database building modes"
        echo "For more values edit NSCB_options.cmd with a text editor"
        echo ""
        echo "Input \"1\"  to USE 1 worker (default\\deactivated)"
        echo "Input \"2\"  to USE 5 workers"
        echo "Input \"3\"  to USE 10 workers"
        echo "Input \"4\"  to USE 20 workers"
        echo "Input \"5\"  to USE 30 workers"
        echo "Input \"6\"  to USE 40 workers"
        echo "Input \"7\"  to USE 50 workers"
        echo "Input \"8\"  to USE 60 workers"
        echo "Input \"9\"  to USE 70 workers"
        echo "Input \"10\" to USE 80 workers"
        echo "Input \"11\" to USE 90 workers"
        echo "Input \"12\" to USE 100 workers"
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_workers="none"
        case "$choice" in
            1) v_workers="-threads 1" ;;
            2) v_workers="-threads 5" ;;
            3) v_workers="-threads 10" ;;
            4) v_workers="-threads 20" ;;
            5) v_workers="-threads 30" ;;
            6) v_workers="-threads 40" ;;
            7) v_workers="-threads 50" ;;
            8) v_workers="-threads 60" ;;
            9) v_workers="-threads 70" ;;
            10) v_workers="-threads 80" ;;
            11) v_workers="-threads 90" ;;
            12) v_workers="-threads 100" ;;
            b|B) return ;;
            0) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_workers" != "none" ]; then
            v_workers="workers=$v_workers"
            $pycommand "$listmanager" -cl "$op_file" -ln "153" -nl "set \"$v_workers\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "153" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# NSZ compression preset configuration
op_NSZ1() {
    clear
    logo
    echo "***************************************************************************"
    echo "USER COMPRESSION OPTIONS"
    echo "***************************************************************************"
    echo "************************"
    echo "INPUT COMPRESSION LEVEL"
    echo "************************"
    echo "Input a compression level between 1 and 22"
    echo "Notes:"
    echo "  + Level 1 - Fast and smaller compression ratio"
    echo "  + Level 22 - Slow but better compression ratio"
    echo "  Levels 10-17 are recommended in the spec"
    echo ""
    echo "Input \"b\" to return to GLOBAL OPTIONS"
    echo "Input \"x\" to return to CONFIG MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo "..........................................................................."
    echo ""
    read -p "Enter your choice: " choice
    v_nszlevels="$choice"
    case "$choice" in
        b|B) return ;;
        x|X) main_menu ;;
        e|E) exit 0 ;;
        *) ;;
    esac

    v_nszlevels="compression_lv=$v_nszlevels"
    $pycommand "$listmanager" -cl "$op_file" -ln "158" -nl "set \"$v_nszlevels\""
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "158" -nl "Line in config was changed to: "

    echo ""
    echo "*******************************************************"
    echo "INPUT NUMBER OF THREADS TO USE"
    echo "*******************************************************"
    echo "Input a number of threads to use between 0 and 4"
    echo "Notes:"
    echo "  + By using threads you may gain a little speed bump"
    echo "    but you'll lose compression ratio"
    echo "  + Level 22 and 4 threads may run you out of memory"
    echo "  + For maximum threads level 17 compression is advised"
    echo "    but you'll lose compression ratio"
    echo ""
    echo "Input \"b\" to return to GLOBAL OPTIONS"
    echo "Input \"x\" to return to CONFIG MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo "..........................................................................."
    echo ""
    read -p "Enter your choice: " choice_threads
    v_nszthreads="$choice_threads"
    case "$choice_threads" in
        b|B) return ;;
        x|X) main_menu ;;
        e|E) exit 0 ;;
        *) ;;
    esac

    v_nszthreads="compression_threads=$v_nszthreads"
    $pycommand "$listmanager" -cl "$op_file" -ln "159" -nl "set \"$v_nszthreads\""
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "159" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
}

# Compressed XCI export format configuration
op_NSZ3() {
    while true; do
        clear
        logo
        echo "*******************************************************"
        echo "FORMAT TO EXPORT XCI"
        echo "*******************************************************"
        echo ""
        echo "Input \"1\"  to export as xcz -supertrimmed- (default)"
        echo "Input \"2\"  to export as nsz"
        echo ""
        echo "Remember, tinfoil can install both formats so it is not"
        echo "advised to export as nsz. If you really want to have"
        echo "them as nsz please do it this way to make the nca"
        echo "files from the game restorable."
        echo "Note: Currently this restoration needs to uncompress"
        echo "the file into nsp first; a direct restoration will be"
        echo "included soon."
        echo ""
        echo "Input \"b\" to return to GLOBAL OPTIONS"
        echo "Input \"x\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "..........................................................................."
        echo ""
        read -p "Enter your choice: " choice
        v_xcz_export="none"
        case "$choice" in
            1) v_xcz_export="xcz" ;;
            2) v_xcz_export="nsz" ;;
            b|B) return ;;
            x|X) main_menu ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_xcz_export" != "none" ]; then
            v_xcz_export="xci_export=$v_xcz_export"
            $pycommand "$listmanager" -cl "$op_file" -ln "160" -nl "set \"$v_xcz_export\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "160" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# Default auto-mode settings
def_set1() {
    echo ""
    echo "**AUTO-MODE OPTIONS**"
    # vrepack
    v_rep="vrepack=both"
    $pycommand "$listmanager" -cl "$op_file" -ln "57" -nl "set \"$v_rep\""
    $pycommand "$listmanager" -rl "$op_file" -ln "57" -nl "Line in config was changed to: "

    # fi_rep
    v_fold="fi_rep=multi"
    $pycommand "$listmanager" -cl "$op_file" -ln "61" -nl "set \"$v_fold\""
    $pycommand "$listmanager" -rl "$op_file" -ln "61" -nl "Line in config was changed to: "

    # v_RSV
    v_RSV="patchRSV=-pv false"
    $pycommand "$listmanager" -cl "$op_file" -ln "41" -nl "set \"$v_RSV\""
    $pycommand "$listmanager" -rl "$op_file" -ln "41" -nl "Line in config was changed to: "

    # vkey
    v_KGEN="vkey=-kp false"
    $pycommand "$listmanager" -cl "$op_file" -ln "95" -nl "set \"$v_KGEN\""
    $pycommand "$listmanager" -rl "$op_file" -ln "95" -nl "Line in config was changed to: "
}

# Default global settings
def_set2() {
    echo ""
    echo "**GLOBAL OPTIONS**"
    # OP_COLOR
    v_col="1F"
    $pycommand "$listmanager" -cl "$op_file" -ln "3" -nl "color $v_col"
    $pycommand "$listmanager" -rl "$op_file" -ln "3" -nl "Line in config was changed to: "

    # w_folder
    v_wf="w_folder=NSCB_temp"
    $pycommand "$listmanager" -cl "$op_file" -ln "8" -nl "set \"$v_wf\""
    $pycommand "$listmanager" -rl "$op_file" -ln "8" -nl "Line in config was changed to: "

    # v_of
    v_of="fold_output=NSCB_output"
    $pycommand "$listmanager" -cl "$op_file" -ln "10" -nl "set \"$v_of\""
    $pycommand "$listmanager" -rl "$op_file" -ln "10" -nl "Line in config was changed to: "

    # v_delta
    v_delta="nf_cleaner=--C_clean_ND"
    $pycommand "$listmanager" -cl "$op_file" -ln "36" -nl "set \"$v_delta\""
    $pycommand "$listmanager" -rl "$op_file" -ln "36" -nl "Line in config was changed to: "

    # v_delta2
    v_delta2_="skdelta=-ND true"
    $pycommand "$listmanager" -cl "$op_file" -ln "37" -nl "set \"$v_delta2_\""
    $pycommand "$listmanager" -rl "$op_file" -ln "37" -nl "Line in config was changed to: "

    # zip_restore
    v_gzip="zip_restore=false"
    $pycommand "$listmanager" -cl "$op_file" -ln "78" -nl "set \"$v_gzip\""
    $pycommand "$listmanager" -rl "$op_file" -ln "78" -nl "Line in config was changed to: "

    # AUTO-EXIT
    v_exit="va_exit=false"
    $pycommand "$listmanager" -cl "$op_file" -ln "101" -nl "set \"$v_exit\""
    $pycommand "$listmanager" -rl "$op_file" -ln "101" -nl "Line in config was changed to: "

    # skipRSVprompt
    skipRSVprompt="skipRSVprompt=false"
    $pycommand "$listmanager" -cl "$op_file" -ln "108" -nl "set \"$skipRSVprompt\""
    $pycommand "$listmanager" -rl "$op_file" -ln "108" -nl "Line in config was changed to: "

    # buffer
    v_buffer="buffer=-b 65536"
    $pycommand "$listmanager" -cl "$op_file" -ln "32" -nl "set \"$v_buffer\""
    $pycommand "$listmanager" -rl "$op_file" -ln "32" -nl "Line in config was changed to: "

    # FAT format
    v_fat1="fatype=-fat exfat"
    $pycommand "$listmanager" -cl "$op_file" -ln "116" -nl "set \"$v_fat1\""
    $pycommand "$listmanager" -rl "$op_file" -ln "116" -nl "Line in config was changed to: "
    v_fat2="fexport=-fx files"
    $pycommand "$listmanager" -cl "$op_file" -ln "117" -nl "set \"$v_fat2\""
    $pycommand "$listmanager" -rl "$op_file" -ln "117" -nl "Line in config was changed to: "

    # OUTPUT ORGANIZING format
    v_oforg="oforg=inline"
    $pycommand "$listmanager" -cl "$op_file" -ln "125" -nl "set \"$v_oforg\""
    $pycommand "$listmanager" -rl "$op_file" -ln "125" -nl "Line in config was changed to: "

    # NSCB MODE
    v_nscbmode="NSBMODE=new"
    $pycommand "$listmanager" -cl "$op_file" -ln "132" -nl "set \"$v_nscbmode\""
    $pycommand "$listmanager" -rl "$op_file" -ln "132" -nl "Line in config was changed to: "

    # ROMAJI
    v_roma="romaji=TRUE"
    $pycommand "$listmanager" -cl "$op_file" -ln "139" -nl "set \"$v_roma\""
    $pycommand "$listmanager" -rl "$op_file" -ln "139" -nl "Line in config was changed to: "

    # TRANSLATE
    v_trans="transnutdb=FALSE"
    $pycommand "$listmanager" -cl "$op_file" -ln "147" -nl "set \"$v_trans\""
    $pycommand "$listmanager" -rl "$op_file" -ln "147" -nl "Line in config was changed to: "

    # WORKERS
    v_workers="workers=-threads 1"
    $pycommand "$listmanager" -cl "$op_file" -ln "153" -nl "set \"$v_workers\""
    $pycommand "$listmanager" -rl "$op_file" -ln "153" -nl "Line in config was changed to: "

    # COMPRESSION
    v_nszlevels="compression_lv=17"
    $pycommand "$listmanager" -cl "$op_file" -ln "158" -nl "set \"$v_nszlevels\""
    $pycommand "$listmanager" -rl "$op_file" -ln "158" -nl "Line in config was changed to: "
    v_nszthreads="compression_threads=0"
    $pycommand "$listmanager" -cl "$op_file" -ln "159" -nl "set \"$v_nszthreads\""
    $pycommand "$listmanager" -rl "$op_file" -ln "159" -nl "Line in config was changed to: "
    v_xcz_export="xci_export=xcz"
    $pycommand "$listmanager" -cl "$op_file" -ln "160" -nl "set \"$v_xcz_export\""
    $pycommand "$listmanager" -rl "$op_file" -ln "160" -nl "Line in config was changed to: "
}

# Current auto-mode settings
curr_set1() {
    echo ""
    echo "**CURRENT AUTO-MODE OPTIONS**"
    $pycommand "$listmanager" -rl "$op_file" -ln "57" -nl "File repack is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "61" -nl "Folder processing is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "41" -nl "RequiredSystemVersion patching is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "95" -nl "Keygeneration variable is set to: "
}

# Current global settings
curr_set2() {
    echo ""
    echo "**CURRENT GLOBAL OPTIONS**"
    $pycommand "$listmanager" -rl "$op_file" -ln "3" -nl "Color is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "8" -nl "Work Folder is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "10" -nl "Output Folder is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "36" -nl "Delta Skipping is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "37" -nl "Delta Skipping (direct functions) is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "78" -nl "Zip generation is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "101" -nl "Auto-exit is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "108" -nl "Skip RSV selection is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "32" -nl "Buffer is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "116" -nl "SD File Format is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "117" -nl "Split nsp format is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "125" -nl "Output organization is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "132" -nl "NSCB mode is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "139" -nl "ROMANIZE option is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "147" -nl "TRANSLATE option is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "153" -nl "WORKERS option is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "158" -nl "COMPRESSION LEVELS option is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "159" -nl "COMPRESSION THREADS option is set to: "
    $pycommand "$listmanager" -rl "$op_file" -ln "160" -nl "COMPRESSED XCIS EXPORT option is set to: "
}

# Verify keys
verify_keys() {
    clear
    logo
    echo "***************************************************************************"
    echo "VERIFY KEYS IN KEYS.TXT AGAINST SHA256 HASHES FROM THE CORRECT KEYS"
    echo "***************************************************************************"
    $pycommand "$squirrel" -nint_keys "$dec_keys"
    echo "..........................................................................."
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo "..........................................................................."
    echo ""
    read -p "Enter your choice: " choice
    case "$choice" in
        0) main_menu ;;
        e|E) exit 0 ;;
        *) ;;
    esac
}

# Update nutdb
update_nutdb() {
    clear
    logo
    echo "***************************************************************************"
    echo "FORCING NUT_DB UPDATE"
    echo "***************************************************************************"
    $pycommand "$squirrel_lb" -lib_call nutdb force_refresh
    echo "..........................................................................."
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo "..........................................................................."
    echo ""
    read -p "Enter your choice: " choice
    case "$choice" in
        0) main_menu ;;
        e|E) exit 0 ;;
        *) ;;
    esac
}

# Google Drive options
google_drive_options() {
    while true; do
        clear
        logo
        echo "********************************************************"
        echo "GOOGLE-DRIVE - CONFIGURATION"
        echo "********************************************************"
        echo "Input \"1\" to register account"
        echo "Input \"2\" to refresh cache for remote libraries"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "......................................................."
        echo ""
        read -p "Enter your choice: " choice
        case "$choice" in
            1) op_google_drive_account ;;
            2) 
                $pycommand "$squirrel_lb" -lib_call workers concurrent_cache
                ;;
            0) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                ;;
        esac
    done
}

op_google_drive_account() {
    clear
    logo
    echo "***************************************************************************"
    echo "Register a google drive account"
    echo "***************************************************************************"
    echo "You need a credentials.json, this can be called credentials.json or name of"
    echo "token you'll generate.json. A credentials.json can be used with many accounts"
    echo "to generate tokens but if it's used with a different account than the one that"
    echo "generated it you'll get a warning."
    echo "A system is implemented to have many credentials json in the credentials folder"
    echo "read the document distributed with NSCB to learn how to get the file."
    echo ""
    echo "Note: The name you input in this step will be used to save the token and for"
    echo "paths."
    echo ""
    echo "Example: A token named \"drive\" will use paths like drive:/folder/file.nsp"
    echo ""
    read -p "Enter the drive name: " token
    echo ""
    $pycommand "$squirrel_lb" -lib_call Drive.Private create_token -xarg "$token" headless="False"
    read -p "Press Enter to continue"
}

# Interface options
interface_options() {
    while true; do
        clear
        logo
        echo "********************************************************"
        echo "INTERFACE - CONFIGURATION"
        echo "********************************************************"
        echo "Input \"1\" to change STARTUP VISIBILITY configuration"
        echo "Input \"2\" to choose a BROWSER for the interface"
        echo "Input \"3\" to deactivate VIDEO PLAYBACK"
        echo "Input \"4\" to setup PORT"
        echo "Input \"5\" to setup HOST"
        echo "Input \"6\" to setup the NOCONSOLE parameter"
        echo ""
        echo "Input \"d\" to restore INTERFACE DEFAULTS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "......................................................."
        echo ""
        read -p "Enter your choice: " choice
        case "$choice" in
            1) op_interface_consolevisibility ;;
            2) op_interface_browser ;;
            3) op_interface_video_playback ;;
            4) op_interface_port ;;
            5) op_interface_host ;;
            6) op_interface_noconsole ;;
            d|D) op_interface_defaults ;;
            0) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                ;;
        esac
    done
}

op_interface_consolevisibility() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "START INTERFACE.BAT MINIMIZED?"
        echo "***************************************************************************"
        echo "Controls if the debugging console starts minimized together with the web"
        echo "interface"
        echo ""
        echo "Input \"1\"  to start MINIMIZED"
        echo "Input \"2\"  to NOT start MINIMIZED"
        echo "Input \"D\"  for default (NOT MINIMIZED)"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to INTERFACE MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_interface="none"
        case "$choice" in
            1) v_interface="yes" ;;
            2) v_interface="no" ;;
            d|D) v_interface="no" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_interface" != "none" ]; then
            v_interface="start_minimized=$v_interface"
            $pycommand "$listmanager" -cl "$opt_interface" -ln "17" -nl "set \"$v_interface\""
            echo ""
            $pycommand "$listmanager" -rl "$opt_interface" -ln "17" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_interface_browser() {
    clear
    logo
    echo "***************************************************************************"
    echo "CHOOSE BROWSER TO STARTUP INTERFACE"
    echo "***************************************************************************"
    echo "Selects the browser used to startup the interface:"
    echo "Options:"
    echo "1. Auto. Order is set in base of ztools\\chromium or browser installed in"
    echo "system. This is autoset by squirrel in the following order:"
    echo "   I.   ztools\\chromium (Chromium portable\\Slimjet portable)"
    echo "   II.  Chrome or Chromium installed on system"
    echo "   III. Microsoft Edge (Not recommended)"
    echo "2. System Default. Uses default system browser (low compatibility)"
    echo "3. Set a raw path to a pure chromium browser by one of the following methods."
    echo "   I.   Absolute path to your browser, ending by .exe"
    echo "   II.  Absolute path to a .lnk file (windows shortcut)"
    echo "   III. Name of a .lnk file in ztools\\chromium (ending by .lnk)"
    echo "        Example: brave.lnk"
    echo "        This will read ztools\\chromium\\brave.lnk and redirect to the exe"
    echo "        path launching brave browser"
    echo ""
    echo "Input \"1\" or \"d\" to set variable to AUTO"
    echo "Input \"2\" to set variable to SYSTEM DEFAULT"
    echo "Input shortcut.lnk name to 3.III methods"
    echo "Input absolute route to browser or shortcut for 3.I or 3.II method"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to INTERFACE MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " choice
    v_interface_browser="$choice"
    case "$choice" in
        1|d|D) v_interface_browser="auto" ;;
        2) v_interface_browser="default" ;;
        0) main_menu ;;
        b|B) return ;;
        e|E) exit 0 ;;
        *) ;;
    esac

    v_interface_browser="browserpath=$v_interface_browser"
    $pycommand "$listmanager" -cl "$opt_interface" -ln "31" -nl "set \"$v_interface_browser\""
    echo ""
    $pycommand "$listmanager" -rl "$opt_interface" -ln "31" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
}

op_interface_video_playback() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "DEACTIVATE VIDEO PLAYBACK"
        echo "***************************************************************************"
        echo "Deactivates HLS player for Nintendo.com videos."
        echo "This is meant for old computers that may freeze with the HLS javascript"
        echo "player"
        echo ""
        echo "Input \"1\"  to ENABLE video playback"
        echo "Input \"2\"  to DISABLE video playback"
        echo "Input \"D\"  for default (ENABLED)"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to INTERFACE MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_video_playback="none"
        case "$choice" in
            1) v_video_playback="true" ;;
            2) v_video_playback="false" ;;
            d|D) v_video_playback="true" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_video_playback" != "none" ]; then
            v_video_playback="videoplayback=$v_video_playback"
            $pycommand "$listmanager" -cl "$opt_interface" -ln "35" -nl "set \"$v_video_playback\""
            echo ""
            $pycommand "$listmanager" -rl "$opt_interface" -ln "35" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_interface_port() {
    clear
    logo
    echo "***************************************************************************"
    echo "CHOOSE PORT FOR INTERFACE"
    echo "***************************************************************************"
    echo ""
    echo "Note \"rg8000\" locates an open port between 8000 and 8999, it allows to open"
    echo "several interface windows at the same time. This is the default parameter"
    echo ""
    echo "Input \"1\" or \"d\" to set variable to rg8000"
    echo "or input a PORT NUMBER"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to INTERFACE MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " choice
    v_interface_port="$choice"
    case "$choice" in
        1|d|D) v_interface_port="rg8000" ;;
        0) main_menu ;;
        b|B) return ;;
        e|E) exit 0 ;;
        *) ;;
    esac

    v_interface_port="port=$v_interface_port"
    $pycommand "$listmanager" -cl "$opt_interface" -ln "48" -nl "set \"$v_interface_port\""
    echo ""
    $pycommand "$listmanager" -rl "$opt_interface" -ln "48" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
}

op_interface_host() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "CHOOSE HOST FOR INTERFACE"
        echo "***************************************************************************"
        echo "Localhost. Interface is only visible locally (default)"
        echo "0.0.0.0. Interface can be visible on the same network"
        echo ""
        echo "Input \"1\" or \"D\" to setup host as LOCALHOST"
        echo "Input \"2\" to setup host as 0.0.0.0"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to INTERFACE MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_interface_host="none"
        case "$choice" in
            1|d|D) v_interface_host="localhost" ;;
            2) v_interface_host="0.0.0.0" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_interface_host" != "none" ]; then
            v_interface_host="host=$v_interface_host"
            $pycommand "$listmanager" -cl "$opt_interface" -ln "55" -nl "set \"$v_interface_host\""
            echo ""
            $pycommand "$listmanager" -rl "$opt_interface" -ln "55" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_interface_noconsole() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "HIDDEN CONSOLE FOR INTERFACE"
        echo "***************************************************************************"
        echo "NoConsole=True. Hides cmd console and redirects console prints to interface"
        echo "this is the default parameter."
        echo "NoConsole=False. Shows cmd console"
        echo ""
        echo "Input \"1\" or \"D\" to setup NOCONSOLE as TRUE"
        echo "Input \"2\" to setup NOCONSOLE as FALSE"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to INTERFACE MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_interface_noconsole="none"
        case "$choice" in
            1|d|D) v_interface_noconsole="true" ;;
            2) v_interface_noconsole="false" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_interface_noconsole" != "none" ]; then
            v_interface_noconsole="noconsole=$v_interface_noconsole"
            $pycommand "$listmanager" -cl "$opt_interface" -ln "61" -nl "set \"$v_interface_noconsole\""
            echo ""
            $pycommand "$listmanager" -rl "$opt_interface" -ln "61" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_interface_defaults() {
    clear
    logo
    v_interface="start_minimized=no"
    $pycommand "$listmanager" -cl "$opt_interface" -ln "17" -nl "set \"$v_interface\""
    $pycommand "$listmanager" -rl "$opt_interface" -ln "17" -nl "Line in config was changed to: "
    echo ""
    v_interface_browser="browserpath=auto"
    $pycommand "$listmanager" -cl "$opt_interface" -ln "31" -nl "set \"$v_interface_browser\""
    $pycommand "$listmanager" -rl "$opt_interface" -ln "31" -nl "Line in config was changed to: "
    echo ""
    v_video_playback="videoplayback=true"
    $pycommand "$listmanager" -cl "$opt_interface" -ln "35" -nl "set \"$v_video_playback\""
    $pycommand "$listmanager" -rl "$opt_interface" -ln "35" -nl "Line in config was changed to: "
    v_interface_port="port=rg8000"
    $pycommand "$listmanager" -cl "$opt_interface" -ln "48" -nl "set \"$v_interface_port\""
    $pycommand "$listmanager" -rl "$opt_interface" -ln "48" -nl "Line in config was changed to: "
    v_interface_host="host=localhost"
    $pycommand "$listmanager" -cl "$opt_interface" -ln "55" -nl "set \"$v_interface_host\""
    $pycommand "$listmanager" -rl "$opt_interface" -ln "55" -nl "Line in config was changed to: "
    v_interface_noconsole="noconsole=true"
    $pycommand "$listmanager" -cl "$opt_interface" -ln "61" -nl "set \"$v_interface_noconsole\""
    $pycommand "$listmanager" -rl "$opt_interface" -ln "61" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    main_menu
}

# Server options
server_options() {
    while true; do
        clear
        logo
        echo "********************************************************"
        echo "SERVER - CONFIGURATION"
        echo "********************************************************"
        echo "Input \"1\" to change STARTUP VISIBILITY configuration"
        echo "Input \"2\" to deactivate VIDEO PLAYBACK"
        echo "Input \"3\" to setup port number"
        echo "Input \"4\" to setup host"
        echo "Input \"5\" to setup the noconsole parameter"
        echo "Input \"6\" to setup the ssl parameter"
        echo ""
        echo "Input \"d\" to restore SERVER DEFAULTS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "......................................................."
        echo ""
        read -p "Enter your choice: " choice
        case "$choice" in
            1) op_server_consolevisibility ;;
            2) op_server_video_playback ;;
            3) op_server_port ;;
            4) op_server_host ;;
            5) op_server_noconsole ;;
            6) op_server_ssl ;;
            d|D) op_server_defaults ;;
            0) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                ;;
        esac
    done
}

op_server_consolevisibility() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "START SERVER.BAT MINIMIZED?"
        echo "***************************************************************************"
        echo "Controls if the debugging console starts minimized together with the web"
        echo "interface"
        echo ""
        echo "Input \"1\"  to start MINIMIZED"
        echo "Input \"2\"  to NOT start MINIMIZED"
        echo "Input \"D\"  for default (NOT MINIMIZED)"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to SERVER MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_server_vis="none"
        case "$choice" in
            1) v_server_vis="yes" ;;
            2) v_server_vis="no" ;;
            d|D) v_server_vis="no" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_server_vis" != "none" ]; then
            v_server_vis="start_minimized=$v_server_vis"
            $pycommand "$listmanager" -cl "$opt_server" -ln "17" -nl "set \"$v_server_vis\""
            echo ""
            $pycommand "$listmanager" -rl "$opt_server" -ln "17" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_server_video_playback() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "DEACTIVATE VIDEO PLAYBACK"
        echo "***************************************************************************"
        echo "Deactivates HLS player for Nintendo.com videos."
        echo "This is meant for old computers that may freeze with the HLS javascript"
        echo "player"
        echo ""
        echo "Input \"1\"  to ENABLE video playback"
        echo "Input \"2\"  to DISABLE video playback"
        echo "Input \"D\"  for default (ENABLED)"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to SERVER MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_video_playback="none"
        case "$choice" in
            1) v_video_playback="true" ;;
            2) v_video_playback="false" ;;
            d|D) v_video_playback="true" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_video_playback" != "none" ]; then
            v_video_playback="videoplayback=$v_video_playback"
            $pycommand "$listmanager" -cl "$opt_server" -ln "21" -nl "set \"$v_video_playback\""
            echo ""
            $pycommand "$listmanager" -rl "$opt_server" -ln "21" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_server_port() {
    clear
    logo
    echo "***************************************************************************"
    echo "CHOOSE PORT FOR SERVER"
    echo "***************************************************************************"
    echo ""
    echo "Note \"rg8000\" locates an open port between 8000 and 8999, it allows to open"
    echo "several interface windows at the same time. This is the default parameter"
    echo ""
    echo "Input \"1\" or \"d\" to set variable to rg8000"
    echo "or input a PORT NUMBER"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to SERVER MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " choice
    v_server_port="$choice"
    case "$choice" in
        1|d|D) v_server_port="rg8000" ;;
        0) main_menu ;;
        b|B) return ;;
        e|E) exit 0 ;;
        *) ;;
    esac

    v_server_port="port=$v_server_port"
    $pycommand "$listmanager" -cl "$opt_server" -ln "29" -nl "set \"$v_server_port\""
    echo ""
    $pycommand "$listmanager" -rl "$opt_server" -ln "29" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
}

op_server_host() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "CHOOSE HOST FOR SERVER"
        echo "***************************************************************************"
        echo "Localhost. Server is only visible locally (default)"
        echo "0.0.0.0. Interface can be visible on the same network"
        echo ""
        echo "Input \"1\" or \"D\" to setup host as LOCALHOST"
        echo "Input \"2\" to setup host as 0.0.0.0"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to SERVER MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_server_host="none"
        case "$choice" in
            1|d|D) v_server_host="localhost" ;;
            2) v_server_host="0.0.0.0" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_server_host" != "none" ]; then
            v_server_host="host=$v_server_host"
            $pycommand "$listmanager" -cl "$opt_server" -ln "36" -nl "set \"$v_server_host\""
            echo ""
            $pycommand "$listmanager" -rl "$opt_server" -ln "36" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_server_noconsole() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "HIDDEN CONSOLE FOR SERVER"
        echo "***************************************************************************"
        echo "NoConsole=True. Hides cmd console and redirects console prints to server"
        echo "this is the default parameter."
        echo "NoConsole=False. Shows cmd console"
        echo ""
        echo "Input \"1\" or \"D\" to setup NOCONSOLE as TRUE"
        echo "Input \"2\" to setup NOCONSOLE as FALSE"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to SERVER MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_server_noconsole="none"
        case "$choice" in
            1|d|D) v_server_noconsole="true" ;;
            2) v_server_noconsole="false" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_server_noconsole" != "none" ]; then
            v_server_noconsole="noconsole=$v_server_noconsole"
            $pycommand "$listmanager" -cl "$opt_server" -ln "42" -nl "set \"$v_server_noconsole\""
            echo ""
            $pycommand "$listmanager" -rl "$opt_server" -ln "42" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_server_ssl() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "SSL PROTOCOL"
        echo "***************************************************************************"
        echo "If true the server will be served via https: if there's a properly signed"
        echo "certificate.pem and key.pem file in zconfig. If those files are not found"
        echo "squirrel will fallback to http:"
        echo ""
        echo "Input \"1\" or \"D\" to SSL OFF (DEFAULT)"
        echo "Input \"2\" to setup SSL ON"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to SERVER MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_server_SSL="none"
        case "$choice" in
            1|d|D) v_server_SSL="false" ;;
            2) v_server_SSL="true" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_server_SSL" != "none" ]; then
            v_server_SSL="ssl=$v_server_SSL"
            $pycommand "$listmanager" -cl "$opt_server" -ln "48" -nl "set \"$v_server_SSL\""
            echo ""
            $pycommand "$listmanager" -rl "$opt_server" -ln "48" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_server_defaults() {
    clear
    logo
    v_interface="start_minimized=no"
    $pycommand "$listmanager" -cl "$opt_server" -ln "17" -nl "set \"$v_interface\""
    $pycommand "$listmanager" -rl "$opt_server" -ln "17" -nl "Line in config was changed to: "
    echo ""
    v_video_playback="videoplayback=true"
    $pycommand "$listmanager" -cl "$opt_server" -ln "21" -nl "set \"$v_video_playback\""
    $pycommand "$listmanager" -rl "$opt_server" -ln "21" -nl "Line in config was changed to: "
    v_interface_port="port=rg8000"
    $pycommand "$listmanager" -cl "$opt_server" -ln "29" -nl "set \"$v_interface_port\""
    $pycommand "$listmanager" -rl "$opt_server" -ln "29" -nl "Line in config was changed to: "
    v_interface_host="host=localhost"
    $pycommand "$listmanager" -cl "$opt_server" -ln "36" -nl "set \"$v_interface_host\""
    $pycommand "$listmanager" -rl "$opt_server" -ln "36" -nl "Line in config was changed to: "
    v_interface_noconsole="noconsole=true"
    $pycommand "$listmanager" -cl "$opt_server" -ln "42" -nl "set \"$v_interface_noconsole\""
    $pycommand "$listmanager" -rl "$opt_server" -ln "42" -nl "Line in config was changed to: "
    v_server_SSL="ssl=false"
    $pycommand "$listmanager" -cl "$opt_server" -ln "48" -nl "set \"$v_server_SSL\""
    $pycommand "$listmanager" -rl "$opt_server" -ln "48" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    main_menu
}

# MTP options
mtp_options() {
    while true; do
        clear
        logo
        echo "********************************************************"
        echo "MTP - CONFIGURATION"
        echo "********************************************************"
        echo "Input \"1\" to setup VERIFICATION pre-installation"
        echo "Input \"2\" to PRIORITIZE NSZ when autoupdating the device"
        echo "Input \"3\" to activate STANDARD CRYPTO INSTALLATIONS"
        echo "Input \"4\" to EXCLUDE XCI when installing updates in AUTOUPDATE"
        echo "Input \"5\" to change between SD and EMMC depending on free space"
        echo "Input \"6\" to check firmware on console before doing installations"
        echo "Input \"7\" to patch keygeneration of files if needed"
        echo "Input \"8\" to check if base content is installed before installation"
        echo "Input \"9\" to check if old updates or dlcs are installed before installation"
        echo "Input \"10\" to choose folder setup when dumping saves"
        echo "Input \"11\" to choose if adding titleid and version to save dumps"
        echo "Input \"12\" to choose how to add files to the cache remote for public links"
        echo "Input \"13\" to change PATCHED FILES AND XCI INSTALLATION SPECIFICATION"
        echo ""
        echo "Input \"d\" to restore MTP DEFAULTS"
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo "......................................................."
        echo ""
        read -p "Enter your choice: " choice
        case "$choice" in
            1) op_MTP_verification ;;
            2) op_MTP_prioritize_NSZ ;;
            3) op_MTP_standard_crypto ;;
            4) op_MTP_exclude_xci_autinst ;;
            5) op_MTP_aut_ch_medium ;;
            6) op_MTP_chk_fw ;;
            7) op_MTP_prepatch_kg ;;
            8) op_MTP_prechk_Base ;;
            9) op_MTP_prechk_Upd ;;
            10) op_MTP_saves_Inline ;;
            11) op_MTP_saves_AddTIDandVer ;;
            12) op_MTP_pdrive_truecopy ;;
            13) op_MTP_ptch_install_spec ;;
            d|D) op_mtp_defaults ;;
            0) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                ;;
        esac
    done
}

op_MTP_verification() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "ACTIVATE FILE VERIFICATION PRE-INSTALLATION"
        echo "***************************************************************************"
        echo "False: Verification deactivated"
        echo "Level 2 verification: Nca are readable, no files missing, titlekey is"
        echo "correct and signature 1 is from a legit VERIFIABLE origin. (default)"
        echo "Hash: Level 2 verification + Hash verification"
        echo ""
        echo "Input \"1\" or \"D\" to setup VERIFICATION to LEVEL2"
        echo "Input \"2\" to setup VERIFICATION to HASH"
        echo "Input \"3\" to DEACTIVATE VERIFICATION"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to MTP MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_mtp_verification="none"
        case "$choice" in
            1|d|D) v_mtp_verification="True" ;;
            2) v_mtp_verification="Hash" ;;
            3) v_mtp_verification="False" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_mtp_verification" != "none" ]; then
            v_mtp_verification="MTP_verification=$v_mtp_verification"
            $pycommand "$listmanager" -cl "$op_file" -ln "166" -nl "set \"$v_mtp_verification\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "166" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_MTP_prioritize_NSZ() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "PRIORITIZE NSZ OVER NSP WHEN CHECKING FOR NEW UPDATES AND DLC IN LIBRARY"
        echo "***************************************************************************"
        echo ""
        echo "Input \"1\" or \"D\" to PRIORITIZE nsz"
        echo "Input \"2\" to NOT prioritize nsz"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to MTP MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_MTP_prioritize_NSZ="none"
        case "$choice" in
            1|d|D) v_MTP_prioritize_NSZ="True" ;;
            2) v_MTP_prioritize_NSZ="False" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_MTP_prioritize_NSZ" != "none" ]; then
            v_MTP_prioritize_NSZ="MTP_prioritize_NSZ=$v_MTP_prioritize_NSZ"
            $pycommand "$listmanager" -cl "$op_file" -ln "167" -nl "set \"$v_MTP_prioritize_NSZ\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "167" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_MTP_standard_crypto() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "INSTALL ALL NSP FILES AS STANDARD CRYPTO"
        echo "***************************************************************************"
        echo "This means nsp files are installed without tickets and titlerights, this"
        echo "to keep the ticketblob in the console clean."
        echo ""
        echo "Input \"1\" or \"D\" to INSTALL WITH TITLERIGHTS (default)"
        echo "Input \"2\" to INSTALL AS STANDARD CRYPTO"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to MTP MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_MTP_standard_crypto="none"
        case "$choice" in
            1|d|D) v_MTP_standard_crypto="False" ;;
            2) v_MTP_standard_crypto="True" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_MTP_standard_crypto" != "none" ]; then
            v_MTP_standard_crypto="MTP_stc_installs=$v_MTP_standard_crypto"
            $pycommand "$listmanager" -cl "$op_file" -ln "181" -nl "set \"$v_MTP_standard_crypto\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "181" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_MTP_exclude_xci_autinst() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "EXCLUDE XCI FROM AUTOUPDATER CHECKS FOR NEW CONTENT"
        echo "***************************************************************************"
        echo ""
        echo "Input \"1\" or \"D\" to EXCLUDE xci from checks"
        echo "Input \"2\" to NOT EXCLUDE xci from checks"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to MTP MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_MTP_exclude_xci_autinst="none"
        case "$choice" in
            1|d|D) v_MTP_exclude_xci_autinst="True" ;;
            2) v_MTP_exclude_xci_autinst="False" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_MTP_exclude_xci_autinst" != "none" ]; then
            v_MTP_exclude_xci_autinst="MTP_exclude_xci_autinst=$v_MTP_exclude_xci_autinst"
            $pycommand "$listmanager" -cl "$op_file" -ln "168" -nl "set \"$v_MTP_exclude_xci_autinst\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "168" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

op_MTP_aut_ch_medium() {
    while true; do
        clear
        logo
        echo "***************************************************************************"
        echo "AUTOCHANGE MEDIUM ACCORDING TO SPACE ON DEVICE"
        echo "***************************************************************************"
        echo "If true changes between SD and EMMC when the space is low in the selected"
        echo "medium. If false skips the installation."
        echo ""
        echo "Input \"1\" or \"D\" to CHANGE MEDIUM according to space on device"
        echo "Input \"2\" to NOT CHANGE MEDIUM according to space on device"
        echo ""
        echo "Input \"0\" to return to CONFIG MENU"
        echo "Input \"b\" to return to MTP MENU"
        echo "Input \"e\" to go back to the MAIN PROGRAM"
        echo ""
        read -p "Enter your choice: " choice
        v_MTP_aut_ch_medium="none"
        case "$choice" in
            1|d|D) v_MTP_aut_ch_medium="True" ;;
            2) v_MTP_aut_ch_medium="False" ;;
            0) main_menu ;;
            b|B) return ;;
            e|E) exit 0 ;;
            *) 
                echo "WRONG CHOICE"
                echo ""
                continue
                ;;
        esac

        if [ "$v_MTP_aut_ch_medium" != "none" ]; then
            v_MTP_aut_ch_medium="MTP_aut_ch_medium=$v_MTP_aut_ch_medium"
            $pycommand "$listmanager" -cl "$op_file" -ln "169" -nl "set \"$v_MTP_aut_ch_medium\""
            echo ""
            $pycommand "$listmanager" -rl "$op_file" -ln "169" -nl "Line in config was changed to: "
            echo ""
            read -p "Press Enter to continue"
            return
        fi
    done
}

# 函数定义：显示 logo
logo() {
    echo "                                        __          _ __    __"
    echo "                  ____  _____ ____     / /_  __  __(_) /___/ /__  _____"  
    echo "                 / __ \/ ___/ ___/    / __ \/ / / / / / __  / _ \/ ___/" 
    echo "                / / / (__  ) /__     / /_/ / /_/ / / / /_/ /  __/ /"    
    echo "               /_/ /_/____/\___/____/_.___/\__,_/_/_/\__,_/\___/_/"     
    echo "                              /_____/"                                  
    echo "-------------------------------------------------------------------------------------"
    echo "                         NINTENDO SWITCH CLEANER AND BUILDER"                        
    echo "                      (THE XCI MULTI CONTENT BUILDER AND MORE)"                      
    echo "-------------------------------------------------------------------------------------"
    echo "=============================     BY JULESONTHEROAD     =============================="
    echo "-------------------------------------------------------------------------------------"
    echo "                                POWERED BY SQUIRREL                                 "
    echo "                    BASED IN THE WORK OF BLAWAR AND LUCA FRAGA                     "
    echo "                                    VERSION 1.01"                                   
    echo "-------------------------------------------------------------------------------------"
    echo "Program's github: https://github.com/julesontheroad/NSC_BUILDER"                   
    echo "Blawar's github:  https://github.com/blawar"                                       
    echo "Luca Fraga's github: https://github.com/LucaFraga"                                 
    echo "-------------------------------------------------------------------------------------"
}

# 函数：op_MTP_chk_fw
op_MTP_chk_fw() {
    clear
    logo
    echo "***************************************************************************"
    echo "CHECK FIRMWARE ON DEVICE AND ON FILE BEING PROCESSED"
    echo "***************************************************************************"
    echo ""
    echo "Input \"1\" or \"D\" to NOT CHECK FIRMWARE (default)"
    echo "Input \"2\" to CHECK FIRMWARE"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to MTP MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " bs

    v_MTP_chk_fw="none"
    if [[ "${bs^^}" == "1" || "${bs^^}" == "D" ]]; then v_MTP_chk_fw="False"; fi
    if [[ "${bs^^}" == "2" ]]; then v_MTP_chk_fw="True"; fi
    if [[ "${bs^^}" == "0" ]]; then sc1; return; fi
    if [[ "${bs^^}" == "B" ]]; then MTP; return; fi
    if [[ "${bs^^}" == "E" ]]; then salida; return; fi

    if [ "$v_MTP_chk_fw" == "none" ]; then
        echo "WRONG CHOICE"
        echo ""
        op_MTP_chk_fw
        return
    fi

    v_MTP_chk_fw="MTP_chk_fw=$v_MTP_chk_fw"
    $pycommand "$listmanager" -cl "$op_file" -ln "170" -nl "set $v_MTP_chk_fw"
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "170" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    MTP
}

# 函数：op_MTP_prepatch_kg
op_MTP_prepatch_kg() {
    clear
    logo
    echo "***************************************************************************"
    echo "CHECK FIRMWARE ON DEVICE AND ON FILE BEING PROCESSED"
    echo "***************************************************************************"
    echo "After a firmware check on the console and the files the program will decide"
    echo "if it should patch or skip the file based on this option"
    echo "Note: Currently it's needed to generate a new file before pushing it via MTP"
    echo "since the ability of patching streams on the fly is not implemented yet on"
    echo "the mtp hook."
    echo ""
    echo "Input \"1\" or \"D\" to NOT PATCH FILES (default)"
    echo "Input \"2\" to PATCH FILES"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to MTP MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " bs

    v_MTP_prepatch_kg="none"
    if [[ "${bs^^}" == "1" || "${bs^^}" == "D" ]]; then v_MTP_prepatch_kg="False"; fi
    if [[ "${bs^^}" == "2" ]]; then v_MTP_prepatch_kg="True"; fi
    if [[ "${bs^^}" == "0" ]]; then sc1; return; fi
    if [[ "${bs^^}" == "B" ]]; then MTP; return; fi
    if [[ "${bs^^}" == "E" ]]; then salida; return; fi

    if [ "$v_MTP_prepatch_kg" == "none" ]; then
        echo "WRONG CHOICE"
        echo ""
        op_MTP_prepatch_kg
        return
    fi

    v_MTP_prepatch_kg="MTP_chk_fw=$v_MTP_prepatch_kg"
    $pycommand "$listmanager" -cl "$op_file" -ln "171" -nl "set $v_MTP_prepatch_kg"
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "171" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    MTP
}

# 函数：op_MTP_prechk_Base
op_MTP_prechk_Base() {
    clear
    logo
    echo "***************************************************************************"
    echo "CHECK IF BASEGAMES ARE ALREADY INSTALLED IN DEVICE"
    echo "***************************************************************************"
    echo "If activated if a base game is in the device the installation will be skipped"
    echo "If deactivated the installation will be overwritten."
    echo ""
    echo "Input \"1\" or \"D\" to CHECK AND SKIP GAMES ALREADY INSTALLED (default)"
    echo "Input \"2\" to NOT check and skip games already installed"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to MTP MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " bs

    v_MTP_prechk_Base="none"
    if [[ "${bs^^}" == "1" || "${bs^^}" == "D" ]]; then v_MTP_prechk_Base="True"; fi
    if [[ "${bs^^}" == "2" ]]; then v_MTP_prechk_Base="False"; fi
    if [[ "${bs^^}" == "0" ]]; then sc1; return; fi
    if [[ "${bs^^}" == "B" ]]; then MTP; return; fi
    if [[ "${bs^^}" == "E" ]]; then salida; return; fi

    if [ "$v_MTP_prechk_Base" == "none" ]; then
        echo "WRONG CHOICE"
        echo ""
        op_MTP_prechk_Base
        return
    fi

    v_MTP_prechk_Base="MTP_prechk_Base=$v_MTP_prechk_Base"
    $pycommand "$listmanager" -cl "$op_file" -ln "173" -nl "set $v_MTP_prechk_Base"
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "173" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    MTP
}

# 函数：op_MTP_prechk_Upd
op_MTP_prechk_Upd() {
    clear
    logo
    echo "***************************************************************************"
    echo "CHECK IF UPDATES AND ARE ALREADY INSTALLED IN DEVICE"
    echo "***************************************************************************"
    echo "If activated checks if an update or dlc is already in the device if the"
    echo "version is lower to the one pushed it deletes the old one pre-installation"
    echo "to reclaim space before the installation process, if the version in the"
    echo "device is equal or higher installation is skipped."
    echo "If deactivated it allows to install older updates or dlc as well as overwrite"
    echo "updates with the same version number."
    echo ""
    echo "Input \"1\" or \"D\" to NOT CHECK AND SKIP updates or dlc already installed (default)"
    echo "Input \"2\" to CHECK AND SKIP updates or dlc already installed"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to MTP MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " bs

    v_MTP_prechk_Upd="none"
    if [[ "${bs^^}" == "1" || "${bs^^}" == "D" ]]; then v_MTP_prechk_Upd="False"; fi
    if [[ "${bs^^}" == "2" ]]; then v_MTP_prechk_Upd="True"; fi
    if [[ "${bs^^}" == "0" ]]; then sc1; return; fi
    if [[ "${bs^^}" == "B" ]]; then MTP; return; fi
    if [[ "${bs^^}" == "E" ]]; then salida; return; fi

    if [ "$v_MTP_prechk_Upd" == "none" ]; then
        echo "WRONG CHOICE"
        echo ""
        op_MTP_prechk_Upd
        return
    fi

    v_MTP_prechk_Upd="MTP_prechk_Upd=$v_MTP_prechk_Upd"
    $pycommand "$listmanager" -cl "$op_file" -ln "174" -nl "set $v_MTP_prechk_Upd"
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "174" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    MTP
}

# 函数：op_MTP_saves_Inline
op_MTP_saves_Inline() {
    clear
    logo
    echo "***************************************************************************"
    echo "STORE SAVEGAMES DUMPS IN FOLDERS OR INLINE"
    echo "***************************************************************************"
    echo ""
    echo "Input \"1\" or \"D\" to store savegames in FOLDERS (default)"
    echo "Input \"2\" to store savegames in INLINE"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to MTP MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " bs

    v_MTP_saves_Inline="none"
    if [[ "${bs^^}" == "1" || "${bs^^}" == "D" ]]; then v_MTP_saves_Inline="False"; fi
    if [[ "${bs^^}" == "2" ]]; then v_MTP_saves_Inline="True"; fi
    if [[ "${bs^^}" == "0" ]]; then sc1; return; fi
    if [[ "${bs^^}" == "B" ]]; then MTP; return; fi
    if [[ "${bs^^}" == "E" ]]; then salida; return; fi

    if [ "$v_MTP_saves_Inline" == "none" ]; then
        echo "WRONG CHOICE"
        echo ""
        op_MTP_saves_Inline
        return
    fi

    v_MTP_saves_Inline="MTP_saves_Inline=$v_MTP_saves_Inline"
    $pycommand "$listmanager" -cl "$op_file" -ln "176" -nl "set $v_MTP_saves_Inline"
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "176" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    MTP
}

# 函数：op_MTP_saves_AddTIDandVer
op_MTP_saves_AddTIDandVer() {
    clear
    logo
    echo "***************************************************************************"
    echo "ADD TITLEID AND VERSION TAGS TO SAVEGAMES"
    echo "***************************************************************************"
    echo "This is meant to know the game version on device when the savedump was made"
    echo "to avoid compatibility issues."
    echo ""
    echo "Input \"1\" or \"D\" to ADD titleid and version tags to file (default)"
    echo "Input \"2\" to NOT ADD titleid and version tags to file"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to MTP MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " bs

    v_MTP_saves_AddTIDandVer="none"
    if [[ "${bs^^}" == "1" || "${bs^^}" == "D" ]]; then v_MTP_saves_AddTIDandVer="False"; fi
    if [[ "${bs^^}" == "2" ]]; then v_MTP_saves_AddTIDandVer="True"; fi
    if [[ "${bs^^}" == "0" ]]; then sc1; return; fi
    if [[ "${bs^^}" == "B" ]]; then MTP; return; fi
    if [[ "${bs^^}" == "E" ]]; then salida; return; fi

    if [ "$v_MTP_saves_AddTIDandVer" == "none" ]; then
        echo "WRONG CHOICE"
        echo ""
        op_MTP_saves_AddTIDandVer
        return
    fi

    v_MTP_saves_AddTIDandVer="MTP_saves_AddTIDandVer=$v_MTP_saves_AddTIDandVer"
    $pycommand "$listmanager" -cl "$op_file" -ln "177" -nl "set $v_MTP_saves_AddTIDandVer"
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "177" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    MTP
}

# 函数：op_MTP_pdrive_truecopy
op_MTP_pdrive_truecopy() {
    clear
    logo
    echo "***************************************************************************"
    echo "ADD TITLEID AND VERSION TAGS TO SAVEGAMES"
    echo "***************************************************************************"
    echo "When installing or transferring a game from a google drive public link NSCB"
    echo "requires a token auth and cache folder setup in a google drive account for"
    echo "better compatibility."
    echo ""
    echo "The game is copied gaining ownership to the cache folder, which also avoids"
    echo "quota issues if TRUECOPY is enabled."
    echo "If TRUECOPY is disabled the game is added to the cache folder as symlink,"
    echo "this allows the file to be called with the auth token but can present quota"
    echo "issues if the link was shared."
    echo ""
    echo "Input \"1\" or \"D\" to ACTIVATE TRUECOPY (default)"
    echo "Input \"2\" to NOT activate TRUECOPY"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to MTP MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " bs

    v_op_MTP_pdrive_truecopy="none"
    if [[ "${bs^^}" == "1" || "${bs^^}" == "D" ]]; then v_op_MTP_pdrive_truecopy="True"; fi
    if [[ "${bs^^}" == "2" ]]; then v_op_MTP_pdrive_truecopy="False"; fi
    if [[ "${bs^^}" == "0" ]]; then sc1; return; fi
    if [[ "${bs^^}" == "B" ]]; then MTP; return; fi
    if [[ "${bs^^}" == "E" ]]; then salida; return; fi

    if [ "$v_op_MTP_pdrive_truecopy" == "none" ]; then
        echo "WRONG CHOICE"
        echo ""
        op_MTP_pdrive_truecopy
        return
    fi

    v_op_MTP_pdrive_truecopy="MTP_pdrive_truecopy=$v_op_MTP_pdrive_truecopy"
    $pycommand "$listmanager" -cl "$op_file" -ln "179" -nl "set $v_op_MTP_pdrive_truecopy"
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "179" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    MTP
}

# 函数：op_MTP_standard_crypto
op_MTP_standard_crypto() {
    clear
    logo
    echo "***************************************************************************"
    echo "INSTALL ALL NSP FILES AS STANDARD CRYPTO"
    echo "***************************************************************************"
    echo "This means nsp files are installed without tickets and titlerights, this"
    echo "to keep the ticketblob in the console clean."
    echo ""
    echo "Input \"1\" or \"D\" to INSTALL WITH TITLERIGHTS (default)"
    echo "Input \"2\" to INSTALL AS STANDARD CRYPTO"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to MTP MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " bs

    v_MTP_standard_crypto="none"
    if [[ "${bs^^}" == "1" || "${bs^^}" == "D" ]]; then v_MTP_standard_crypto="False"; fi
    if [[ "${bs^^}" == "2" ]]; then v_MTP_standard_crypto="True"; fi
    if [[ "${bs^^}" == "0" ]]; then sc1; return; fi
    if [[ "${bs^^}" == "B" ]]; then MTP; return; fi
    if [[ "${bs^^}" == "E" ]]; then salida; return; fi

    if [ "$v_MTP_standard_crypto" == "none" ]; then
        echo "WRONG CHOICE"
        echo ""
        op_MTP_standard_crypto
        return
    fi

    v_MTP_standard_crypto="MTP_stc_installs=$v_MTP_standard_crypto"
    $pycommand "$listmanager" -cl "$op_file" -ln "181" -nl "set $v_MTP_standard_crypto"
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "181" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    MTP
}

# 函数：op_MTP_ptch_install_spec
op_MTP_ptch_install_spec() {
    clear
    logo
    echo "***************************************************************************"
    echo "SPECIFICATION FOR INSTALLATION OF PATCHED NSP AND XCI"
    echo "***************************************************************************"
    echo "Legacy creates the patched file or converted file and then transfers to the"
    echo "console."
    echo "Spec1 creates a patch to patch the stream on the fly. Spec1 treats multifiles"
    echo "as different files triggering several consecutive installations."
    echo ""
    echo "Input \"1\" or \"D\" to use SPECIFICATION Nº 1 (default)"
    echo "Input \"2\" to use LEGACY specification"
    echo ""
    echo "Input \"0\" to return to CONFIG MENU"
    echo "Input \"b\" to return to MTP MENU"
    echo "Input \"e\" to go back to the MAIN PROGRAM"
    echo ""
    read -p "Enter your choice: " bs

    v_MTP_ptch_install_spec="none"
    if [[ "${bs^^}" == "1" || "${bs^^}" == "D" ]]; then v_MTP_ptch_install_spec="spec1"; fi
    if [[ "${bs^^}" == "2" ]]; then v_MTP_ptch_install_spec="legacy"; fi
    if [[ "${bs^^}" == "0" ]]; then sc1; return; fi
    if [[ "${bs^^}" == "B" ]]; then MTP; return; fi
    if [[ "${bs^^}" == "E" ]]; then salida; return; fi

    if [ "$v_MTP_ptch_install_spec" == "none" ]; then
        echo "WRONG CHOICE"
        echo ""
        op_MTP_ptch_install_spec
        return
    fi

    v_MTP_ptch_install_spec="MTP_ptch_inst_spec=$v_MTP_ptch_install_spec"
    $pycommand "$listmanager" -cl "$op_file" -ln "182" -nl "set $v_MTP_ptch_install_spec"
    echo ""
    $pycommand "$listmanager" -rl "$op_file" -ln "182" -nl "Line in config was changed to: "
    echo ""
    read -p "Press Enter to continue"
    MTP
}

# 函数：op_mtp_defaults
op_mtp_defaults() {
    clear
    logo
    # MTP_verification
    v_mtp_verification="MTP_verification=True"
    $pycommand "$listmanager" -cl "$op_file" -ln "166" -nl "set $v_mtp_verification"
    $pycommand "$listmanager" -rl "$op_file" -ln "166" -nl "Line in config was changed to: "
    # MTP_prioritize_NSZ
    v_MTP_prioritize_NSZ="MTP_prioritize_NSZ=True"
    $pycommand "$listmanager" -cl "$op_file" -ln "167" -nl "set $v_MTP_prioritize_NSZ"
    $pycommand "$listmanager" -rl "$op_file" -ln "167" -nl "Line in config was changed to: "
    # MTP_exclude_xci_autinst
    v_MTP_exclude_xci_autinst="MTP_exclude_xci_autinst=True"
    $pycommand "$listmanager" -cl "$op_file" -ln "168" -nl "set $v_MTP_exclude_xci_autinst"
    $pycommand "$listmanager" -rl "$op_file" -ln "168" -nl "Line in config was changed to: "
    # MTP_aut_ch_medium
    v_MTP_aut_ch_medium="MTP_aut_ch_medium=True"
    $pycommand "$listmanager" -cl "$op_file" -ln "169" -nl "set $v_MTP_aut_ch_medium"
    $pycommand "$listmanager" -rl "$op_file" -ln "169" -nl "Line in config was changed to: "
    # MTP_chk_fw
    v_MTP_chk_fw="MTP_chk_fw=False"
    $pycommand "$listmanager" -cl "$op_file" -ln "170" -nl "set $v_MTP_chk_fw"
    $pycommand "$listmanager" -rl "$op_file" -ln "170" -nl "Line in config was changed to: "
    # MTP_prepatch_kg
    v_MTP_prepatch_kg="MTP_chk_fw=False"
    $pycommand "$listmanager" -cl "$op_file" -ln "171" -nl "set $v_MTP_prepatch_kg"
    $pycommand "$listmanager" -rl "$op_file" -ln "171" -nl "Line in config was changed to: "
    # MTP_prechk_Base
    v_MTP_prechk_Base="MTP_prechk_Base=True"
    $pycommand "$listmanager" -cl "$op_file" -ln "173" -nl "set $v_MTP_prechk_Base"
    $pycommand "$listmanager" -rl "$op_file" -ln "173" -nl "Line in config was changed to: "
    # MTP_prechk_Upd
    v_MTP_prechk_Upd="MTP_prechk_Upd=False"
    $pycommand "$listmanager" -cl "$op_file" -ln "174" -nl "set $v_MTP_prechk_Upd"
    $pycommand "$listmanager" -rl "$op_file" -ln "174" -nl "Line in config was changed to: "
    # MTP_saves_Inline
    v_MTP_saves_Inline="MTP_saves_Inline=False"
    $pycommand "$listmanager" -cl "$op_file" -ln "176" -nl "set $v_MTP_saves_Inline"
    $pycommand "$listmanager" -rl "$op_file" -ln "176" -nl "Line in config was changed to: "
    # MTP_saves_AddTIDandVer
    v_MTP_saves_AddTIDandVer="MTP_saves_AddTIDandVer=False"
    $pycommand "$listmanager" -cl "$op_file" -ln "177" -nl "set $v_MTP_saves_AddTIDandVer"
    $pycommand "$listmanager" -rl "$op_file" -ln "177" -nl "Line in config was changed to: "
    # MTP_pdrive_truecopy
    v_op_MTP_pdrive_truecopy="MTP_pdrive_truecopy=True"
    $pycommand "$listmanager" -cl "$op_file" -ln "179" -nl "set $v_op_MTP_pdrive_truecopy"
    $pycommand "$listmanager" -rl "$op_file" -ln "179" -nl "Line in config was changed to: "
    # MTP_standard_crypto
    v_MTP_standard_crypto="MTP_stc_installs=False"
    $pycommand "$listmanager" -cl "$op_file" -ln "181" -nl "set $v_MTP_standard_crypto"
    $pycommand "$listmanager" -rl "$op_file" -ln "181" -nl "Line in config was changed to: "
    # MTP_ptch_install_spec
    v_MTP_ptch_install_spec="MTP_ptch_inst_spec=spec1"
    $pycommand "$listmanager" -cl "$op_file" -ln "182" -nl "set $v_MTP_ptch_install_spec"
    $pycommand "$listmanager" -rl "$op_file" -ln "182" -nl "Line in config was changed to: "
    read -p "Press Enter to continue"
    sc1
}

# 函数：salida
salida() {
    exit 0
}

# 函数：idepend
idepend() {
    clear
    logo
    "$batdepend"
    sc1
}

# 假设的占位函数（需根据实际需求实现）
sc1() { echo "Return to CONFIG MENU (placeholder)"; }
MTP() { echo "Return to MTP MENU (placeholder)"; }

# 示例调用（根据实际需求调整）
# op_MTP_chk_fw
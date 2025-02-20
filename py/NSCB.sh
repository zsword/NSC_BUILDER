#!/bin/bash

# Initial Setup
TOP_INIT() {
    prog_dir="$(dirname "$0")"
    bat_name="$(basename "$0" .sh)"
    ofile_name="${bat_name}_options.sh"
    opt_interface="Interface_options.sh"
    opt_server="Server_options.sh"
    echo "NSC_Builder v1.01-b -- Profile: $ofile_name -- by JulesOnTheRoad"
    list_folder="${prog_dir}/lists"

    # Configurable option file path
    op_file="${prog_dir}/zconfig/${ofile_name}"
    opt_interface="${prog_dir}/zconfig/${opt_interface}"
    opt_server="${prog_dir}/zconfig/${opt_server}"

    # Source options from option file if it exists
    if [ -f "$op_file" ]; then
        source "$op_file"
    fi

    # Define variables with defaults (can be overridden by op_file)
    safe_var="${safe_var:-}"
    vrepack="${vrepack:-}"
    vrename="${vrename:-}"
    fi_rep="${fi_rep:-}"
    zip_restore="${zip_restore:-}"
    manual_intro="${manual_intro:-}"
    va_exit="${va_exit:-}"
    skipRSVprompt="${skipRSVprompt:-}"
    oforg="${oforg:-}"
    NSBMODE="${NSBMODE:-}"
    romaji="${romaji:-}"
    transnutdb="${transnutdb:-}"
    workers="${workers:-}"
    compression_lv="${compression_lv:-}"
    compression_threads="${compression_threads:-}"
    xci_export="${xci_export:-}"
    MTP_verification="${MTP_verification:-}"
    MTP_prioritize_NSZ="${MTP_prioritize_NSZ:-}"
    MTP_exclude_xci_autinst="${MTP_exclude_xci_autinst:-}"
    MTP_aut_ch_medium="${MTP_aut_ch_medium:-}"
    MTP_chk_fw="${MTP_chk_fw:-}"
    MTP_prepatch_kg="${MTP_prepatch_kg:-}"
    MTP_prechk_Base="${MTP_prechk_Base:-}"
    MTP_prechk_Upd="${MTP_prechk_Upd:-}"
    MTP_saves_Inline="${MTP_saves_Inline:-}"
    MTP_saves_AddTIDandVer="${MTP_saves_AddTIDandVer:-}"
    MTP_pdrive_truecopy="${MTP_pdrive_truecopy:-}"
    MTP_stc_installs="${MTP_stc_installs:-}"
    MTP_ptch_inst_spec="${MTP_ptch_inst_spec:-}"

    # Copy function variables
    pycommand="${pycommand:-python}"
    buffer="${buffer:-}"
    nf_cleaner="${nf_cleaner:-}"
    patchRSV="${patchRSV:-}"
    vkey="${vkey:-}"
    capRSV="${capRSV:-}"
    fatype="${fatype:-}"
    fexport="${fexport:-}"
    skdelta="${skdelta:-}"

    # Programs
    squirrel="${nut:-}"
    squirrel_lb="${squirrel_lb:-}"
    MTP="${MTP:-}"
    xci_lib="${xci_lib:-}"
    nsp_lib="${nsp_lib:-}"
    zip="${zip:-}"
    hacbuild="${hacbuild:-}"
    listmanager="${listmanager:-}"
    batconfig="${batconfig:-}"
    batdepend="${batdepend:-}"
    infobat="${infobat:-}"

    # Files
    uinput="${uinput:-}"
    dec_keys="${dec_keys:-}"

    # Folders
    w_folder="${prog_dir}/${w_folder:-}"
    fold_output="${fold_output:-}"
    zip_fold="${prog_dir}/${zip_fold:-}"

    # Set absolute routes
    for prog in squirrel squirrel_lb xci_lib nsp_lib zip hacbuild listmanager batconfig batdepend infobat; do
        if [ -f "${prog_dir}/${!prog}" ]; then
            eval "$prog=\"${prog_dir}/${!prog}\""
        fi
    done
    for file in uinput dec_keys; do
        if [ -f "${prog_dir}/${!file}" ]; then
            eval "$file=\"${prog_dir}/${!file}\""
        fi
    done

    # Ensure output folder exists
    mkdir -p "$fold_output"

    # Checks for missing dependencies
    check_missing
}

check_missing() {
    local missing=()
    for item in "$op_file" "$squirrel" "$xci_lib" "$nsp_lib" "$zip" "$hacbuild" "$listmanager" "$batconfig" "$infobat" "$dec_keys"; do
        if [ ! -f "$item" ]; then
            missing+=("$item")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        program_logo
        echo "...................................."
        echo "You're missing the following things:"
        echo "...................................."
        for miss in "${missing[@]}"; do
            echo "- $miss"
        done
        echo "Program will exit now"
        sleep 2
        exit 1
    fi
}

# Process input (file or folder)
process_input() {
    if [ -z "$1" ]; then
        manual
    elif [ "$vrepack" = "nodelta" ]; then
        aut_rebuild_nodeltas "$1"
    elif [ "$vrepack" = "rebuild" ]; then
        aut_rebuild_nsp "$1"
    elif [ -d "$1" ]; then
        folder "$1"
    else
        file "$1"
    fi
}

folder() {
    local input="$1"
    if [ "$fi_rep" = "multi" ]; then
        folder_mult_mode "$input"
    elif [ "$fi_rep" = "baseid" ]; then
        folder_packbyid "$input"
    else
        folder_ind_mode "$input"
    fi
}

folder_ind_mode() {
    local input="$1"
    program_logo
    echo "--------------------------------------"
    echo "Auto-Mode. Individual repacking is set"
    echo "--------------------------------------"
    echo

    # Process NSP files
    for file in "$input"/*.nsp; do
        if [ -f "$file" ]; then
            target="$file"
            rm -rf "$w_folder" 2>/dev/null
            mkdir -p "$w_folder"
            filename=$(basename "$file" .nsp)
            orinput="$file"
            showname="$orinput"
            squirrell
            if [ "$zip_restore" = "true" ]; then
                ziptarget="$file"
                makezip
            fi
            getname
            if [ "$vrename" = "true" ]; then
                addtags_from_nsp
            fi
            case "$vrepack" in
                "nsp") $pycommand "$squirrel" $buffer $patchRSV $vkey $capRSV $fatype $fexport $skdelta -o "$w_folder" -t "nsp" -dc "$file" ;;
                "xci") $pycommand "$squirrel" $buffer $patchRSV $vkey $capRSV $fatype $fexport $skdelta -o "$w_folder" -t "xci" -dc "$file" ;;
                "both") $pycommand "$squirrel" $buffer $patchRSV $vkey $capRSV $fatype $fexport $skdelta -o "$w_folder" -t "both" -dc "$file" ;;
            esac
            mkdir -p "$fold_output"
            mv "$w_folder"/*.{xci,xc*,nsp,ns*} "$fold_output" 2>/dev/null
            if [ -d "$w_folder/archfolder" ]; then
                $pycommand "$squirrel" -ifo "$w_folder/archfolder" -archive "$fold_output/$filename.nsp"
            fi
            rm -rf "$w_folder"
            echo "DONE"
            thumbup
        fi
    done

    # Process NSZ, XCI, XCZ similarly (omitted for brevity, follow same pattern)
    echo "---------------------------------------------------"
    echo "*********** ALL FILES WERE PROCESSED! *************"
    echo "---------------------------------------------------"
    aut_exit_choice
}

file() {
    local input="$1"
    case "${input##*.}" in
        "nsp"|"nsz") nsp "$input" ;;
        "xci"|"xcz") xci "$input" ;;
        *) other "$input" ;;
    esac
}

nsp() {
    local input="$1"
    orinput="$input"
    filename=$(basename "$input" .nsp)
    target="$input"
    showname="$orinput"
    rm -rf "$w_folder" 2>/dev/null
    squirrell
    if [ "$zip_restore" = "true" ]; then
        ziptarget="$input"
        makezip
    fi
    mkdir -p "$w_folder"
    getname
    if [ "$vrename" = "true" ]; then
        addtags_from_nsp
    fi
    case "$vrepack" in
        "nsp") $pycommand "$squirrel" $buffer $patchRSV $vkey $capRSV $fatype $fexport $skdelta -o "$w_folder" -t "nsp" -dc "$input" ;;
        "xci") $pycommand "$squirrel" $buffer $patchRSV $vkey $capRSV $fatype $fexport $skdelta -o "$w_folder" -t "xci" -dc "$input" ;;
        "both") $pycommand "$squirrel" $buffer $patchRSV $vkey $capRSV $fatype $fexport $skdelta -o "$w_folder" -t "both" -dc "$input" ;;
    esac
    mkdir -p "$fold_output"
    mv "$w_folder"/*.{xci,xc*,nsp,ns*} "$fold_output" 2>/dev/null
    if [ -d "$w_folder/archfolder" ]; then
        $pycommand "$squirrel" -ifo "$w_folder/archfolder" -archive "$fold_output/$filename.nsp"
    fi
    rm -rf "$w_folder"
    echo "DONE"
    thumbup
    aut_exit_choice
}

xci() {
    local input="$1"
    filename=$(basename "$input" .xci)
    orinput="$input"
    showname="$orinput"
    rm -rf "$w_folder" 2>/dev/null
    mkdir -p "$w_folder/secure"
    getname
    if [ "$vrename" = "true" ]; then
        addtags_from_xci
    fi
    case "$vrepack" in
        "nsp") $pycommand "$squirrel" $buffer $patchRSV $vkey $capRSV $fatype $fexport $skdelta -o "$w_folder" -t "nsp" -dc "$input" ;;
        "xci") $pycommand "$squirrel" $buffer $patchRSV $vkey $capRSV $fatype $fexport $skdelta -o "$w_folder" -t "xci" -dc "$input" ;;
        "both") $pycommand "$squirrel" $buffer $patchRSV $vkey $capRSV $fatype $fexport $skdelta -o "$w_folder" -t "both" -dc "$input" ;;
    esac
    mkdir -p "$fold_output"
    mv "$w_folder"/*.{xci,xc*,nsp,ns*} "$fold_output" 2>/dev/null
    if [ -d "$w_folder/archfolder" ]; then
        $pycommand "$squirrel" -ifo "$w_folder/archfolder" -archive "$fold_output/$filename.nsp"
    fi
    rm -rf "$w_folder"
    echo "DONE"
    thumbup
    aut_exit_choice
}

other() {
    echo "No valid file was dragged. The program only accepts xci or nsp files."
    echo "You'll be redirected to manual mode."
    read -p "Press Enter to continue..."
    manual
}

aut_exit_choice() {
    if [ "$va_exit" = "true" ]; then
        echo "PROGRAM WILL CLOSE NOW"
        sleep 2
        exit 0
    fi
    echo "Input \"0\" to go to the mode selection"
    echo "Input \"1\" to exit the program"
    read -p "Enter your choice: " choice
    case "$choice" in
        "0") manual ;;
        "1") exit 0 ;;
        *) aut_exit_choice ;;
    esac
}

manual() {
    clear
    program_logo
    echo "********************************"
    echo "YOU'VE ENTERED INTO MANUAL MODE"
    echo "********************************"
    case "$manual_intro" in
        "indiv") normalmode ;;
        "multi") multimode ;;
        "split") SPLMODE ;;
        *) manual_Reentry ;;
    esac
}

manual_Reentry() {
    clear
    if [ "$NSBMODE" = "legacy" ]; then
        "$prog_dir/ztools/LEGACY.sh"
    fi
    program_logo
    echo "......................................................."
    echo "Input \"1\" to process files INDIVIDUALLY"
    echo "Input \"2\" to enter into MULTI-PACK mode"
    echo "Input \"3\" to enter into MULTI-CONTENT SPLITTER mode"
    echo "Input \"0\" to enter into CONFIGURATION mode"
    echo "......................................................."
    read -p "Enter your choice: " choice
    case "$choice" in
        "1") normalmode ;;
        "2") multimode ;;
        "3") SPLMODE ;;
        "0") OPT_CONFIG ;;
        *) manual_Reentry ;;
    esac
}

normalmode() {
    # Placeholder for individual processing mode (to be implemented similarly)
    echo "Individual processing mode not fully implemented in this example."
    manual_Reentry
}

multimode() {
    # Placeholder for multi-pack mode (to be implemented similarly)
    echo "Multi-pack mode not fully implemented in this example."
    manual_Reentry
}

SPLMODE() {
    # Placeholder for splitter mode (to be implemented similarly)
    echo "Splitter mode not fully implemented in this example."
    manual_Reentry
}

OPT_CONFIG() {
    "$batconfig" "$op_file" "$listmanager" "$batdepend"
    TOP_INIT
}

# Subroutines
squirrell() {
    echo "                    ,;:;;,"
    echo "                   ;;;;"
    echo "           .=',    ;:;;:,"
    echo "          /_', \"=. ';:;:;"
    echo "          @=:__,  \\;:;:'"
    echo "            _(\.=  ;:;;'"
    echo "           \`\"_(  _/=\"\`"
    echo "            \`\"'"
}

program_logo() {
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
    echo "\"                                POWERED BY SQUIRREL                                \""
    echo "\"                    BASED ON THE WORK OF BLAWAR AND LUCA FRAGA                     \""
    echo "                                  VERSION 1.01 (NEW)"
    echo "-------------------------------------------------------------------------------------"
}

thumbup() {
    echo
    echo "    /@"
    echo "    \ \\"
    echo "  ___\\ \\"
    echo " (__O)  \\"
    echo " (____@) \\"
    echo " (____@)  \\"
    echo " (__o)_    \\"
    echo "       \\    \\"
    echo
    echo "HOPE YOU HAVE A FUN TIME"
}

getname() {
    mkdir -p "$w_folder"
    filename=$(echo "$filename" | sed 's/\[nap\]//g;s/\[xc\]//g;s/\[nc\]//g;s/\[rr\]//g;s/\[xcib\]//g;s/\[nxt\]//g;s/\[Trimmed\]//g')
    echo "$filename" > "$w_folder/fname.txt"
    end_folder=$(sed 's/\[.*//;s/(.*//' "$w_folder/fname.txt" | tr -d '\n')
    end_folder=$(echo "$end_folder" | tr '_' ' ' | sed 's/ $//')
    rm -f "$w_folder/fname.txt"
    if [ "$vrename" = "true" ]; then
        filename="$end_folder"
    fi
}

makezip() {
    echo "Making zip for $ziptarget"
    $pycommand "$squirrel" $buffer $patchRSV $vkey $capRSV -o "$w_folder/zip" --zip_combo "$ziptarget"
    # Add more zip creation logic as needed
}

addtags_from_nsp() {
    titleid=$($pycommand "$squirrel" --nsptitleid "$orinput")
    type=$($pycommand "$squirrel" --nsptype "$orinput")
    case "$type" in
        "BASE") filename="$filename[$titleid][v0]" ;;
        "UPDATE") filename="$filename[$titleid][UPD]" ;;
        "DLC") filename="$filename[$titleid][DLC]" ;;
    esac
}

addtags_from_xci() {
    ncameta=$(ls "$w_folder/secure"/*.cnmt.nca | head -n 1)
    titleid=$($pycommand "$squirrel" --ncatitleid "$ncameta")
    if echo "$titleid" | grep -q "000$"; then
        ttag="[v0]"
    elif echo "$titleid" | grep -q "800$"; then
        ttag="[UPD]"
    else
        ttag="[DLC]"
    fi
    filename="$filename[$titleid][$ttag]"
}

# Main execution
TOP_INIT
process_input "$1"
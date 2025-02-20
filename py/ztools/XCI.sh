#!/bin/bash

# Change directory to the second argument and then move up one level
cd "$2" || exit 1
cd .. || exit 1

# Main logic based on the first argument
case "$1" in
  "repack")
    xci_repack
    ;;
  "sp_repack")
    sp_xci_repack
    ;;
  *)
    exit 0
    ;;
esac

# Function to handle XCI repacking
xci_repack() {
  # Ensure directories exist
  [[ ! -d "$w_folder/normal" ]] && mkdir -p "$w_folder/normal"
  [[ ! -d "$w_folder/update" ]] && mkdir -p "$w_folder/update"

  # List .nca files and filter
  ls -1 "$w_folder/secure/"*.nca > "$w_folder/lisfiles.txt" 2>/dev/null
  grep -i "\.nca" "$w_folder/lisfiles.txt" > "$w_folder/nca_list.txt"
  rm -f "$w_folder/lisfiles.txt"

  # Count the number of .nca files
  nca_number=$(wc -l < "$w_folder/nca_list.txt")
  rm -f "$w_folder/nca_list.txt"

  # Add dummy files based on nca_number
  if [[ $nca_number -le 3 ]]; then
    touch "$w_folder/secure/000"
  fi
  if [[ $nca_number -le 2 ]]; then
    touch "$w_folder/secure/00"
  fi
  if [[ $nca_number -le 1 ]]; then
    touch "$w_folder/secure/0"
  fi

  # Output repacking message
  echo "-------------------------------"
  echo "Repacking as xci"
  echo "-------------------------------"

  # Clean up .dat and .xml files
  rm -f "$w_folder/secure/"*.dat 2>/dev/null
  rm -f "$w_folder/secure/"*.xml 2>/dev/null

  # Execute the repacking command
  "$pycommand" "$squirrel" $buffer -ifo "$w_folder" $fatype --create_xci "$w_folder/$filename.xci"
}

# Function to handle special XCI repacking
sp_xci_repack() {
  # Ensure directories exist
  [[ ! -d "$tfolder/normal" ]] && mkdir -p "$tfolder/normal"
  [[ ! -d "$tfolder/update" ]] && mkdir -p "$tfolder/update"

  # List .nca files and filter
  ls -1 "$tfolder/secure/"*.nca > "$tfolder/lisfiles.txt" 2>/dev/null
  grep -i "\.nca" "$tfolder/lisfiles.txt" > "$tfolder/nca_list.txt"
  rm -f "$tfolder/lisfiles.txt"

  # Count the number of .nca files
  nca_number=$(wc -l < "$tfolder/nca_list.txt")

  # Add dummy files based on nca_number
  if [[ $nca_number -le 3 ]]; then
    touch "$tfolder/secure/000"
  fi
  if [[ $nca_number -le 2 ]]; then
    touch "$tfolder/secure/00"
  fi
  if [[ $nca_number -le 1 ]]; then
    touch "$tfolder/secure/0"
  fi

  # Handle old license NSP method if no .tik files exist
  if [[ ! -f "$tfolder/secure/"*.tik ]]; then
    sp_build
    return
  fi

  # Create license directory and move files
  mkdir -p "$tfolder/lc"
  cp -f "$tfolder/secure/"*.cnmt.nca "$tfolder/lc/" 2>/dev/null
  mv "$tfolder/secure/"*.tik "$tfolder/lc/" 2>/dev/null
  mv "$tfolder/secure/"*.cert "$tfolder/lc/" 2>/dev/null

  # Identify control NCA
  ctrl_nca=""
  while IFS= read -r file; do
    nca_type=$("$pycommand" "$squirrel" --ncatype "$tfolder/secure/$file")
    if [[ "$nca_type" == "Content.CONTROL" ]]; then
      ctrl_nca="$file"
    fi
  done < "$tfolder/nca_list.txt"
  rm -f "$tfolder/nca_list.txt"

  # Copy control NCA to license folder
  cp -f "$tfolder/secure/$ctrl_nca" "$tfolder/lc/" 2>/dev/null

  # Generate list of license files and build NSP
  ls -1 "$tfolder/lc" > "$tfolder/lc_list.txt"
  row=""
  while IFS= read -r file; do
    row="$tfolder/lc/$file $row"
  done < "$tfolder/lc_list.txt"
  "$pycommand" "$squirrel" -c "$w_folder/output.nsp" $row 2>/dev/null
  mv "$w_folder/output.nsp" "$w_folder/$fname[lc].nsp"
  rm -f "$tfolder/lc_list.txt"
}

# Sub-function for sp_xci_repack to build XCI
sp_build() {
  echo "-------------------------------"
  echo "Repacking as xci"
  echo "-------------------------------"

  # Clean up .dat and .xml files
  rm -f "$tfolder/secure/"*.dat 2>/dev/null
  rm -f "$tfolder/secure/"*.xml 2>/dev/null

  # Execute the repacking command
  "$pycommand" "$squirrel" $buffer -ifo "$tfolder" $fatype --create_xci "$w_folder/$fname.xci"

  # Remove temporary folder
  rm -rf "$tfolder" 2>/dev/null
}

# Simulate the PING delay from the batch script (3 seconds)
sleep 3

exit 0
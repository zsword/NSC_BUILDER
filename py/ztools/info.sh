#!/bin/bash

# 定义初始变量
info_dir="$1INFO"

# 定义 logo 函数
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

# sc1 函数：文件输入界面
sc1() {
    clear
    logo
    echo "********************************************************"
    echo "FILE - INFORMATION"
    echo "********************************************************"
    echo ""
    echo "-- Input \"0\" to go back to the MAIN PROGRAM --"
    echo ""
    read -p "OR DRAG A XCI/NSP/NSX/NCA FILE AND PRESS ENTER: " bs
    bs=${bs//\"}  # 移除引号
    if [ "$bs" = "0" ]; then
        salida
    fi
    targt="$bs"
    extension="${bs##*.}"
    name="${bs%.*}"
    case "$extension" in
        nsp|nsx|xci)
            sc2
            ;;
        nca)
            sc3
            ;;
        nsz|xcz)
            sc2_1
            ;;
        *)
            echo "WRONG TYPE OF FILE"
            read -p "Press Enter to continue"
            sc1
            ;;
    esac
}

# sc2 函数：处理 xci/nsp/nsx 文件
sc2() {
    clear
    logo
    echo "......................................................."
    echo "Input \"1\" to get FILE LIST of the xci/nsp"
    echo "Input \"2\" to get CONTENT LIST of the xci/nsp"
    echo "Input \"3\" to get NUT-INFO of the xci/nsp"
    echo "Input \"4\" to get GAME-INFO and FW requirements"
    echo "Input \"5\" to READ the CNMT from the xci/nsp"
    echo "Input \"6\" to READ the NACP from the xci/nsp"
    echo "Input \"7\" to READ the main.NPDM from the xci/nsp"
    echo "Input \"8\" to VERIFY file (xci/nsp/nsx/nca)"
    echo ""
    echo "Input \"b\" to go back to FILE LOADING"
    echo "Input \"0\" to go back to the MAIN PROGRAM"
    echo ""
    echo "--- Or DRAG a New File to change the current target ---"
    echo "......................................................."
    echo ""
    read -p "Enter your choice: " bs
    bs=${bs//\"}
    extension="${bs##*.}"
    if [ -n "$extension" ]; then
        case "$extension" in
            nsp|nsx|xci)
                snfi
                ;;
            nsz|xcz)
                snfi2
                ;;
            nca)
                snfi_nca
                ;;
            *)
                wch
                ;;
        esac
    else
        case "$bs" in
            1)
                g_file_content
                ;;
            2)
                g_content_list
                ;;
            3)
                n_info
                ;;
            4)
                f_info
                ;;
            5)
                r_cnmt
                ;;
            6)
                r_nacp
                ;;
            7)
                r_npdm
                ;;
            8)
                verify
                ;;
            b)
                sc1
                ;;
            0)
                salida
                ;;
            *)
                wch
                ;;
        esac
    fi
}

# sc2_1 函数：处理 nsz/xcz 文件
sc2_1() {
    clear
    logo
    echo "......................................................."
    echo "Input \"1\" to get FILE LIST of the xci/nsp"
    echo "Input \"2\" to get CONTENT LIST of the xci/nsp"
    echo "Input \"3\" to get GAME-INFO and FW requirements"
    echo "Input \"4\" to READ the CNMT from the xci/nsp"
    echo "Input \"5\" to READ the NACP from the xci/nsp"
    echo "Input \"6\" to VERIFY file"
    echo ""
    echo "Input \"b\" to go back to FILE LOADING"
    echo "Input \"0\" to go back to the MAIN PROGRAM"
    echo ""
    echo "--- Or DRAG a New File to change the current target ---"
    echo "......................................................."
    echo ""
    read -p "Enter your choice: " bs
    bs=${bs//\"}
    extension="${bs##*.}"
    if [ -n "$extension" ]; then
        case "$extension" in
            nsp|nsx|xci)
                snfi
                ;;
            nsz|xcz)
                snfi2
                ;;
            nca)
                snfi_nca
                ;;
            *)
                wch2
                ;;
        esac
    else
        case "$bs" in
            1)
                g_file_content2
                ;;
            2)
                g_content_list2
                ;;
            3)
                f_info2
                ;;
            4)
                r_cnmt2
                ;;
            5)
                r_nacp2
                ;;
            6)
                verify2
                ;;
            b)
                sc1
                ;;
            0)
                salida
                ;;
            *)
                wch2
                ;;
        esac
    fi
}

# sc3 函数：处理 nca 文件
sc3() {
    clear
    logo
    echo "......................................................."
    echo "Input \"1\" to get NUT-INFO of the NCA"
    echo "Input \"2\" to READ the CNMT of a meta NCA"
    echo "Input \"3\" to READ the NACP of a control NCA"
    echo "Input \"4\" to READ the NPDM of a program NCA"
    echo "Input \"5\" to VERIFY the NCA"
    echo ""
    echo "Input \"b\" to go back to FILE LOADING"
    echo "Input \"0\" to go back to the MAIN PROGRAM"
    echo ""
    echo "--- Or DRAG a New File to change the current target ---"
    echo "......................................................."
    echo ""
    read -p "Enter your choice: " bs
    bs=${bs//\"}
    extension="${bs##*.}"
    if [ -n "$extension" ]; then
        case "$extension" in
            nca)
                snfi_nca
                ;;
            nsp|nsx|xci)
                snfi
                ;;
            *)
                wch_nca
                ;;
        esac
    else
        case "$bs" in
            1)
                n_info_nca
                ;;
            2)
                r_cnmt_nca
                ;;
            3)
                r_nacp_nca
                ;;
            4)
                r_npdm_nca
                ;;
            5)
                verify_nca
                ;;
            b)
                sc1
                ;;
            0)
                salida
                ;;
            *)
                wch_nca
                ;;
        esac
    fi
}

# snfi 函数：更新文件名并返回 sc2
snfi() {
    name="${bs%.*}"
    targt="$bs"
    sc2
}

# snfi2 函数：更新文件名并返回 sc2_1
snfi2() {
    name="${bs%.*}"
    targt="$bs"
    sc2_1
}

# snfi_nca 函数：更新文件名并返回 sc3
snfi_nca() {
    name="${bs%.*}"
    targt="$bs"
    sc3
}

# wch 函数：错误选择提示（sc2）
wch() {
    echo "WRONG CHOICE"
    read -p "Press Enter to continue"
    sc2
}

# wch2 函数：错误选择提示（sc2_1）
wch2() {
    echo "WRONG CHOICE"
    read -p "Press Enter to continue"
    sc2_1
}

# wch_nca 函数：错误选择提示（sc3）
wch_nca() {
    echo "WRONG CHOICE"
    read -p "Press Enter to continue"
    sc3
}

# g_file_content 函数：显示 nsp/xci 文件内容
g_file_content() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW NSP FILE CONTENT OR XCI SECURE PARTITION CONTENT"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --ADVfilelist "$targt"
    sc2
}

# g_file_content2 函数：显示 nsz/xcz 文件内容
g_file_content2() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW NSZ FILE CONTENT OR XCZ SECURE PARTITION CONTENT"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --ADVfilelist "$targt"
    sc2_1
}

# g_content_list 函数：按 ID 显示 nsp/xci 内容
g_content_list() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW NSP OR XCI CONTENT ARRANGED BY ID"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --ADVcontentlist "$targt"
    sc2
}

# g_content_list2 函数：按 ID 显示 nsz/xcz 内容
g_content_list2() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW NSP OR XCI CONTENT ARRANGED BY ID"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --ADVcontentlist "$targt"
    sc2_1
}

# n_info 函数：显示 NUT 信息
n_info() {
    clear
    logo
    echo "********************************************************"
    echo "NUT - INFO BY BLAWAR"
    echo "********************************************************"
    python3 "$squirrel" -i "$targt"
    echo ""
    echo "********************************************************"
    echo "Do you want to print the information to a text file?"
    echo "********************************************************"
    while true; do
        echo "Input \"1\" to print to text file"
        echo "Input \"2\" to NOT print to text file"
        echo ""
        read -p "Enter your choice: " bs
        case "$bs" in
            1)
                mkdir -p "$info_dir"
                i_file="$info_dir/${name}-info.txt"
                python3 "$squirrel" -i "$targt" > "$i_file"
                python3 "$squirrel" --strip_lines "$i_file" "2"
                echo "DONE"
                sc2
                break
                ;;
            2)
                sc2
                break
                ;;
            *)
                echo "WRONG CHOICE"
                echo ""
                ;;
        esac
    done
}

# f_info 函数：显示固件信息
f_info() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW INFORMATION AND DATA ABOUT THE REQUIRED FIRMWARE"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --translate "$transnutdb" --fw_req "$targt"
    sc2
}

# f_info2 函数：显示 nsz/xcz 固件信息
f_info2() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW INFORMATION AND DATA ABOUT THE REQUIRED FIRMWARE"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --translate "$transnutdb" --fw_req "$targt"
    sc2_1
}

# r_cnmt 函数：读取 CNMT 数据
r_cnmt() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW CMT DATA FROM META NCA IN NSP/XCI"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --Read_cnmt "$targt"
    sc2
}

# r_cnmt2 函数：读取 nsz/xcz CNMT 数据
r_cnmt2() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW CMT DATA FROM META NCA IN NSP/XCI"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --Read_cnmt "$targt"
    sc2_1
}

# r_nacp 函数：读取 NACP 数据
r_nacp() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW NACP DATA FROM CONTROL NCA IN NSP/XCI"
    echo "********************************************************"
    echo "IMPLEMENTATION OF 0LIAM'S NACP LIBRARY"
    python3 "$squirrel" -o "$info_dir" --Read_nacp "$targt"
    sc2
}

# r_nacp2 函数：读取 nsz/xcz NACP 数据
r_nacp2() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW NACP DATA FROM CONTROL NCA IN NSP/XCI"
    echo "********************************************************"
    echo "IMPLEMENTATION OF 0LIAM'S NACP LIBRARY"
    python3 "$squirrel" -o "$info_dir" --Read_nacp "$targt"
    sc2_1
}

# r_npdm 函数：读取 NPDM 数据
r_npdm() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW MAIN.NPDM DATA FROM PROGRAM NCA IN NSP/XCI"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --Read_npdm "$targt"
    sc2
}

# verify 函数：验证文件
verify() {
    clear
    logo
    echo "********************************************************"
    echo "VERIFY A NSP/XCI/NCA"
    echo "********************************************************"
    python3 "$squirrel" "$buffer" -o "$info_dir" -v "$targt"
    sc2
}

# verify2 函数：验证 nsz/xcz 文件
verify2() {
    clear
    logo
    echo "********************************************************"
    echo "VERIFY A NSZ/XCZ FILE"
    echo "********************************************************"
    python3 "$squirrel" "$buffer" -o "$info_dir" -v "$targt"
    sc2_1
}

# n_info_nca 函数：显示 NCA 的 NUT 信息
n_info_nca() {
    clear
    logo
    echo "********************************************************"
    echo "NUT - INFO BY BLAWAR"
    echo "********************************************************"
    python3 "$squirrel" -i "$targt"
    echo ""
    echo "********************************************************"
    echo "Do you want to print the information to a text file?"
    echo "********************************************************"
    while true; do
        echo "Input \"1\" to print to text file"
        echo "Input \"2\" to NOT print to text file"
        echo ""
        read -p "Enter your choice: " bs
        case "$bs" in
            1)
                mkdir -p "$info_dir"
                i_file="$info_dir/${name}-info.txt"
                python3 "$squirrel" -i "$targt" > "$i_file"
                python3 "$squirrel" --strip_lines "$i_file" "2"
                echo "DONE"
                sc3
                break
                ;;
            2)
                sc3
                break
                ;;
            *)
                echo "WRONG CHOICE"
                echo ""
                ;;
        esac
    done
}

# r_cnmt_nca 函数：读取 NCA 的 CNMT 数据
r_cnmt_nca() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW CMT DATA FROM META NCA IN NSP/XCI"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --Read_cnmt "$targt"
    sc3
}

# r_nacp_nca 函数：读取 NCA 的 NACP 数据
r_nacp_nca() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW NACP DATA FROM CONTROL NCA IN NSP/XCI"
    echo "********************************************************"
    echo "IMPLEMENTATION OF 0LIAM'S NACP LIBRARY"
    python3 "$squirrel" -o "$info_dir" --Read_nacp "$targt"
    sc3
}

# r_npdm_nca 函数：读取 NCA 的 NPDM 数据
r_npdm_nca() {
    clear
    logo
    echo "********************************************************"
    echo "SHOW MAIN.NPDM DATA FROM PROGRAM NCA IN NSP/XCI"
    echo "********************************************************"
    python3 "$squirrel" -o "$info_dir" --Read_npdm "$targt"
    sc3
}

# verify_nca 函数：验证 NCA 文件
verify_nca() {
    clear
    logo
    echo "********************************************************"
    echo "VERIFY A NSP/XCI/NCA"
    echo "********************************************************"
    python3 "$squirrel" "$buffer" -o "$info_dir" -v "$targt"
    sc3
}

# salida 函数：退出脚本
salida() {
    exit 0
}

# 脚本入口
sc1
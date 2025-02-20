#!/bin/bash

# 切换到第二个参数指定的目录
cd "$2"

# 切换到上级目录
cd ..

# 根据第一个参数调用相应的函数
if [ "$1" == "repack" ]; then
    nsp_repack
elif [ "$1" == "convert" ]; then
    nsp_convert
elif [ "$1" == "sp_convert" ]; then
    sp_nsp_convert
fi

# 延迟3秒
sleep 3

# 定义 nsp_repack 函数
nsp_repack() {
    echo "-----------------"
    echo "Repacking as nsp"
    echo "-----------------"

    # 删除 secure 目录下的 .dat 文件
    rm -f "$w_folder/secure/"*.dat 2>/dev/null

    # 生成 cnmt.nca 文件列表
    ls "$w_folder/secure/"*.cnmt.nca > "$w_folder/cnmt_fileslist.txt" 2>/dev/null

    # 读取文件列表并构建 row 变量
    row=""
    while read -r x; do
        row="$w_folder/secure/$x $row"
    done < "$w_folder/cnmt_fileslist.txt"

    # 调用 Python 命令生成 XML
    $pycommand "$squirrel" -o "$w_folder/secure" --xml_gen $row 2>/dev/null

    # 删除临时文件列表
    rm -f "$w_folder/cnmt_fileslist.txt" 2>/dev/null

    # 调用 Python 命令创建 nsp 文件
    $pycommand "$squirrel" $buffer $fatype $fexport -ifo "$w_folder/secure" -c "$w_folder/$filename.nsp"

    # 重命名 .ns* 文件
    for file in "$w_folder"/*.ns*; do
        if [ -f "$file" ]; then
            mv "$file" "$w_folder/$filename.ns${file##*.}" 2>/dev/null
        fi
    done
}

# 定义 nsp_convert 函数
nsp_convert() {
    echo "-----------------"
    echo "Repacking as nsp"
    echo "-----------------"

    # 删除 secure 目录下的 .dat 文件
    rm -f "$w_folder/secure/"*.dat 2>/dev/null

    # 生成 cnmt.nca 文件列表
    ls "$w_folder/secure/"*.cnmt.nca > "$w_folder/cnmt_fileslist.txt" 2>/dev/null

    # 读取文件列表并构建 row 变量
    row=""
    while read -r x; do
        row="$w_folder/secure/$x $row"
    done < "$w_folder/cnmt_fileslist.txt"

    # 调用 Python 命令生成 XML
    $pycommand "$squirrel" -o "$w_folder/secure" --xml_gen $row 2>/dev/null

    # 删除临时文件列表
    rm -f "$w_folder/cnmt_fileslist.txt" 2>/dev/null

    # 调用 Python 命令创建 nsp 文件
    $pycommand "$squirrel" $buffer $fatype $fexport -ifo "$w_folder/secure" -c "$w_folder/$filename.nsp"

    # 重命名 .ns* 文件
    for file in "$w_folder"/*.ns*; do
        if [ -f "$file" ]; then
            mv "$file" "$w_folder/$filename.ns${file##*.}" 2>/dev/null
        fi
    done
}

# 定义 sp_nsp_convert 函数
sp_nsp_convert() {
    echo "-----------------"
    echo "Repacking as nsp"
    echo "-----------------"

    # 删除 secure 目录下的 .dat 文件
    rm -f "$tfolder/secure/"*.dat 2>/dev/null

    # 生成 cnmt.nca 文件列表
    ls "$tfolder/secure/"*.cnmt.nca > "$tfolder/cnmt_fileslist.txt" 2>/dev/null

    # 读取文件列表并构建 row 变量
    row=""
    while read -r x; do
        row="$tfolder/secure/$x $row"
    done < "$tfolder/cnmt_fileslist.txt"

    # 调用 Python 命令生成 XML
    $pycommand "$squirrel" -o "$tfolder/secure" --xml_gen $row 2>/dev/null

    # 删除临时文件列表
    rm -f "$tfolder/cnmt_fileslist.txt" 2>/dev/null

    # 调用 Python 命令创建 nsp 文件
    $pycommand "$squirrel" $buffer $fatype $fexport -ifo "$tfolder/secure" -c "$w_folder/$fname.nsp"

    # 重命名 .ns* 文件
    for file in "$w_folder"/*.ns*; do
        if [ -f "$file" ]; then
            mv "$file" "$w_folder/$fname.ns${file##*.}" 2>/dev/null
        fi
    done
}
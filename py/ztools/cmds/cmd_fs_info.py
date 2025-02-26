#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import Fs
import Utils
import Print

# INFORMATION
# Show file filelist
def cmd_filelist(args):
    for filename in args.filelist:
        if filename.endswith('.nsp'):
            try:
                f = Fs.Nsp(filename, 'rb')
                f.print_file_list()
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        if filename.endswith('.xci'):
            try:
                f = Fs.factory(filename)
                f.open(filename, 'rb')
                f.print_file_list()
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
# Show advance filelist
def cmd_ADVfilelist(args):
    if args.ofolder:
        for var in args.ofolder:
            try:
                ofolder = var
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.ADVfilelist:
            dir=os.path.dirname(os.path.abspath(filename))
            info='INFO'
            ofolder =os.path.join(dir,info)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.text_file:
        tfile=args.text_file
        dir=os.path.dirname(os.path.abspath(tfile))
        if not os.path.exists(dir):
            os.makedirs(dir)
        err='badfiles.txt'
        errfile = os.path.join(dir, err)
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
    else:
        for filename in args.ADVfilelist:
            filename=filename
    basename=str(os.path.basename(os.path.abspath(filename)))
    ofile=basename[:-4]+'-Fcontent.txt'
    infotext=os.path.join(ofolder, ofile)
    if filename.endswith('.nsp') or filename.endswith('.nsx') or filename.endswith('.nsz'):
        try:
            f = Fs.Nsp(filename, 'rb')
            feed=f.adv_file_list()
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith('.xci') or filename.endswith('.xcz'):
        try:
            f = Fs.factory(filename)
            f.open(filename, 'rb')
            feed=f.adv_file_list()
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
# Show advance filelist
def cmd_ADVcontentlist(args):
    if args.ofolder:
        for var in args.ofolder:
            try:
                ofolder = var
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.ADVcontentlist:
            dir=os.path.dirname(os.path.abspath(filename))
            info='INFO'
            ofolder =os.path.join(dir,info)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.text_file:
        tfile=args.text_file
        dir=os.path.dirname(os.path.abspath(tfile))
        if not os.path.exists(dir):
            os.makedirs(dir)
        err='badfiles.txt'
        errfile = os.path.join(dir, err)
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
    else:
        for filename in args.ADVcontentlist:
            filename=filename
    basename=str(os.path.basename(os.path.abspath(filename)))
    ofile=basename[:-4]+'_ID_content.txt'
    infotext=os.path.join(ofolder, ofile)
    if filename.endswith('.nsp') or filename.endswith('.nsx') or filename.endswith('.nsz'):
        try:
            f = Fs.Nsp(filename, 'rb')
            feed=f.adv_content_list()
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith('.xci') or filename.endswith('.xcz'):
        try:
            f = Fs.factory(filename)
            f.open(filename, 'rb')
            feed=f.adv_content_list()
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
# FW REQ INFO
def cmd_fw_req(args):
    if args.translate:
        if str(args.translate).lower()=="true":
            trans=True
    else:
        trans=False
    if args.romanize:
        for val_ in args.romanize:
            roman=str(val_).upper()
            if roman == "FALSE":
                roman = False
            else:
                roman = True
    else:
        roman = True
    if args.ofolder:
        for var in args.ofolder:
            try:
                ofolder = var
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.fw_req:
            dir=os.path.dirname(os.path.abspath(filename))
            info='INFO'
            ofolder =os.path.join(dir,info)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.text_file:
        tfile=args.text_file
        dir=os.path.dirname(os.path.abspath(tfile))
        if not os.path.exists(dir):
            os.makedirs(dir)
        err='badfiles.txt'
        errfile = os.path.join(dir, err)
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
    else:
        for filename in args.fw_req:
            filename=filename
    basename=str(os.path.basename(os.path.abspath(filename)))
    ofile=basename[:-4]+'-fwinfo.txt'
    infotext=os.path.join(ofolder, ofile)
    if filename.endswith('.nsp') or filename.endswith('.nsx') or filename.endswith('.nsz'):
        try:		
            f = Fs.Nsp(filename, 'rb')
            feed=f.print_fw_req(trans,roma=roman)
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith('.xci') or filename.endswith('.xcz'):
        try:
            f = Fs.factory(filename)
            f.open(filename, 'rb')
            feed=f.print_fw_req(trans,roma=roman)
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
# XCI HEADER
def cmd_Read_xci_head(args):
    for filename in args.Read_xci_head:
        if filename.endswith('.xci'):
            try:
                f = Fs.factory(filename)
                f.open(filename, 'rb')
                f.print_head()
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
# ADD CONTENT TO DATABASE
def cmd_addtodb(args):
    if args.romanize:
        for input in args.romanize:
            roman=str(input).upper()
            if roman == "FALSE":
                roman = False
            else:
                roman = True
    else:
        roman = True
    if args.db_file:
        outfile=args.db_file
        dir=os.path.dirname(os.path.abspath(outfile))
        err='errorlog.txt'
        errfile = os.path.join(dir, err)
    else:
        for filename in args.addtodb:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder = os.path.join(dir, 'output')
            outname='nutdb.txt'
            outfile = os.path.join(ofolder, outname)
            err='errorlog.txt'
            errfile = os.path.join(ofolder, outname)
            if not os.path.exists(ofolder):
                os.makedirs(ofolder)
    if args.dbformat:
        for input in args.dbformat:
            input=str(input).lower()
            if input == "nutdb":
                outdb = "nutdb"
            elif input == "keyless":
                outdb = "keyless"
            elif input == "simple":
                outdb = "simple"
            elif input == "extended":
                outdb = "extended"
            else:
                outdb = "all"
    else:
        outdb = "extended"
    if args.addtodb:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filename = filelist.readline()
                filename=os.path.abspath(filename.rstrip('\n'))
        else:
            for filename in args.addtodb:
                filename=filename
        if (filename.lower()).endswith('.nsp') or (filename.lower()).endswith('.nsx') or (filename.lower()).endswith('.nsz'):
            try:
                infile=r''
                infile+=filename
                f = Fs.Nsp(filename, 'rb')
                f.addtodb(outfile,outdb,roman)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
                with open(errfile, 'a') as errfile:
                    now=datetime.now()
                    date=now.strftime("%x")+". "+now.strftime("%X")
                    errfile.write(date+' Error in "ADD TO DATABASE" function:'+'\n')
                    errfile.write("Route "+str(filename)+'\n')
                    errfile.write('- Exception: ' + str(e)+ '\n')
        if (filename.lower()).endswith('.xci') or (filename.lower()).endswith('.xcz'):
            try:
                infile=r''
                infile+=filename
                f = Fs.factory(filename)
                f.open(filename, 'rb')
                f.addtodb(outfile,outdb,roman)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
                with open(errfile, 'a') as errfile:
                    now=datetime.now()
                    date=now.strftime("%x")+". "+now.strftime("%X")
                    errfile.write(date+' Error in "ADD TO DATABASE" function:'+'\n')
                    errfile.write("Route "+str(filename)+'\n')
                    errfile.write('- Exception: ' + str(e)+ '\n')

#parser.add_argument('-nscdb_new', '--addtodb_new', nargs='+', help='Adds content to database')
def cmd_addtodb_new(args):
    if args.translate:
        if str(args.translate).lower()=="true":
            trans=True
    else:
        trans=False
    if args.db_file:
        DBfile=args.db_file
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filename = filelist.readline()
                filename=os.path.abspath(filename.rstrip('\n'))
        else:
            for filename in args.addtodb_new:
                filename=filename
        if (filename.lower()).endswith('.nsp') or (filename.lower()).endswith('.nsx') or (filename.lower()).endswith('.nsz'):
            try:
                f = Fs.Nsp(filename, 'rb')
                f.Incorporate_to_permaDB(DBfile,trans)
            except BaseException as e:
                Utils.logError(e)
        if (filename.lower()).endswith('.xci') or (filename.lower()).endswith('.xcz'):
            try:
                f = Fs.Xci(filename)
                f.Incorporate_to_permaDB(DBfile,trans)
            except BaseException as e:
                Utils.logError(e)
# Show info
def cmd_info(args):
    print(str(len(args.info)))
    if re.search(r'^[A-Fa-f0-9]+$', args.info.strip(), re.I | re.M | re.S):
        Print.info('%s version = %s' % (args.info.upper(), CDNSP.get_version(args.info.lower())))
    else:
        path = args.info
        if os.path.isdir(path):
            for filename in os.listdir(path):
                fp = os.path.join(path, filename)
                Print.info("FileInfo: "+fp)
                f = Fs.factory(fp)
                f.open(fp, 'r+b')
                f.printInfo()
        else:
            f = Fs.factory(args.info)
            f.open(args.info, 'r+b')
            f.printInfo()
            '''
            for i in f.cnmt():
                for j in i:
                    Print.info(j._path)
                    j.rewind()
                    buf = j.read()
                    Hex.dump(buf)
                    j.seek(0x28)
                    #j.writeInt64(0)
                    Print.info('min: ' + str(j.readInt64()))
            #f.flush()
            #f.close()
            '''
# Read ncap inside nsp or xci
def cmd_Read_nacp(args):
    if args.romanize:
        for val_ in args.romanize:
            roman=str(val_).upper()
            if roman == "FALSE":
                roman = False
            else:
                roman = True
    else:
        roman = True
    if args.ofolder:
        for var in args.ofolder:
            try:
                ofolder = var
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.Read_nacp:
            dir=os.path.dirname(os.path.abspath(filename))
            info='INFO'
            ofolder =os.path.join(dir,info)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.text_file:
        tfile=args.text_file
        dir=os.path.dirname(os.path.abspath(tfile))
        if not os.path.exists(dir):
            os.makedirs(dir)
        err='badfiles.txt'
        errfile = os.path.join(dir, err)
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
    else:
        for filename in args.Read_nacp:
            filename=filename
    basename=str(os.path.basename(os.path.abspath(filename)))
    ofile=basename[:-4]+'-nacp.txt'
    infotext=os.path.join(ofolder, ofile)
    if filename.endswith('.nsp') or filename.endswith('.nsx') or filename.endswith('.nsz'):
        try:
            f = Fs.Nsp(filename, 'rb')
            feed=f.read_nacp(roma=roman)
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith('.xci') or filename.endswith('.xcz'):
        try:
            f = Fs.factory(filename)
            f.open(filename, 'rb')
            feed=f.read_nacp(roma=roman)
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith('.nca'):
        try:
            f = Fs.Nca(filename, 'rb')
            if 	str(f.header.contentType) == 'Content.CONTROL':
                feed=f.read_nacp()
                f.flush()
                f.close()
            else:
                basename=str(os.path.basename(os.path.abspath(filename)))
                basename=basename.lower()
                feed=''
                message=basename+' is not a TYPE CONTROL NCA';print(message);feed+=message+'\n'
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
# Read ncap inside nsp or xci
def cmd_Read_icon(args):
    for filename in args.Read_icon:
        filename=filename
    if filename.endswith('.nsp') or filename.endswith('.nsx'):
        try:
            files_list=sq_tools.ret_nsp_offsets(filename)
            f = Fs.Nsp(filename, 'rb')
            f.icon_info(files_list)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith('.xci'):
        try:
            files_list=sq_tools.ret_xci_offsets(filename)
            f = Fs.Xci(filename)
            f.icon_info(files_list)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Raw extraction. For cases when a file is bad and triggers a exception
def cmd_raw_extraction(args):
    if args.buffer:
        for var in args.buffer:
            try:
                buffer = var
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    ofolder=False
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.text_file:
        tfile=args.text_file
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
            if ofolder != False:
                dir=ofolder
            else:
                dir=os.path.dirname(os.path.abspath(filename))
            basename=str(os.path.basename(os.path.abspath(filename)))
            basename=basename[:-4]
            ofolder =os.path.join(dir, basename)
    else:
        for filename in args.raw_extraction:
            if ofolder != False:
                dir=ofolder
            else:
                dir=os.path.dirname(os.path.abspath(filename))
            basename=str(os.path.basename(os.path.abspath(filename)))
            basename=basename[:-4]
            ofolder =os.path.join(dir, basename)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    test=filename.lower()
    if test.endswith('.nsp') or test.endswith('.nsx') or test.endswith('.nsz'):
        try:
            files_list=sq_tools.ret_nsp_offsets(filename,32)
            for i in range(len(files_list)):
                #print(files_list[i][0])
                #print(files_list[i][1])
                #print(files_list[i][2])
                off1=files_list[i][1]
                off2=files_list[i][2]
                filepath = os.path.join(ofolder, files_list[i][0])
                fp = open(filepath, 'w+b')
                s=files_list[i][3]
                if int(buffer)>s:
                    buf=s
                else:
                    buf=buffer
                #print(filepath)
                if sys.platform == 'win32':
                    v_drive, v_path = os.path.splitdrive(filepath)
                else:
                    v_drive = os.path.dirname(os.path.abspath(filepath))
                dsktotal, dskused, dskfree=disk_usage(str(v_drive))
                if int(dskfree)<int(s):
                    sys.exit("Warning disk space lower than required size. Program will exit")							
                t = tqdm(total=s, unit='B', unit_scale=True, leave=False)
                with open(filename, 'r+b') as f:
                    f.seek(off1)
                    c=0
                    t.write(tabs+'Copying: ' + str(files_list[i][0]))
                    for data in iter(lambda: f.read(int(buf)), ""):
                        fp.write(data)
                        fp.flush()
                        c=len(data)+c
                        t.update(len(data))
                        if c+int(buf)>s:
                            if (s-c)<0:
                                t.close()
                                fp.close()
                                break
                            data=f.read(s-c)
                            fp.write(data)
                            t.update(len(data))
                            t.close()
                            fp.close()
                            break
                        if not data:
                            t.close()
                            fp.close()
                            break
        except BaseException as e:
            Utils.logError(e)
    elif test.endswith('.xci') or test.endswith('.xcz'):
        try:
            files_list=sq_tools.ret_xci_offsets(filename,32)
            #print(files_list)
            for i in range(len(files_list)):
                #print(files_list[i][0])
                #print(files_list[i][1])
                #print(files_list[i][2])
                off1=files_list[i][1]
                off2=files_list[i][2]
                filepath = os.path.join(ofolder, files_list[i][0])
                fp = open(filepath, 'w+b')
                s=files_list[i][3]
                if int(buffer)>s:
                    buf=s
                else:
                    buf=buffer
                #print(filepath)
                if sys.platform == 'win32':
                    v_drive, v_path = os.path.splitdrive(filepath)
                else:
                    v_drive = os.path.dirname(os.path.abspath(filepath))
                dsktotal, dskused, dskfree=disk_usage(str(v_drive))
                if int(dskfree)<int(s):
                    sys.exit("Warning disk space lower than required size. Program will exit")					
                t = tqdm(total=s, unit='B', unit_scale=True, leave=False)
                with open(filename, 'r+b') as f:
                    f.seek(off1)
                    c=0
                    t.write(tabs+'Copying: ' + str(files_list[i][0]))
                    for data in iter(lambda: f.read(int(buf)), ""):
                        fp.write(data)
                        fp.flush()
                        c=len(data)+c
                        t.update(len(data))
                        if c+int(buf)>s:
                            if (s-c)<0:
                                t.close()
                                fp.close()
                                break
                            data=f.read(s-c)
                            fp.write(data)
                            t.update(len(data))
                            t.close()
                            fp.close()
                            break
                        if not data:
                            t.close()
                            fp.close()
                            break
        except BaseException as e:
            Utils.logError(e)
# NCA_FILE_EXTACTION. EXTRACT FILES PACKED IN NCA FROM NSP\XCI\NCA
def cmd_nca_file_extraction(args):
    if args.buffer:
        for var in args.buffer:
            try:
                buffer = var
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    ofolder=False
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.text_file:
        tfile=args.text_file
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
            if ofolder != False:
                dir=ofolder
            else:
                dir=os.path.dirname(os.path.abspath(filename))
            basename=str(os.path.basename(os.path.abspath(filename)))
            basename=basename[:-4]
            ofolder =os.path.join(dir, basename)
    else:
        for filename in args.nca_file_extraction:
            if ofolder != False:
                dir=ofolder
            else:
                dir=os.path.dirname(os.path.abspath(filename))
            basename=str(os.path.basename(os.path.abspath(filename)))
            basename=basename[:-4]
            ofolder =os.path.join(dir, basename)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if filename.endswith('.nsp'):
        try:
            files_list=sq_tools.ret_nsp_offsets(filename)
            f = Fs.Nsp(filename, 'rb')
            f.extract_nca(ofolder,files_list,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith('.xci'):
        try:
            files_list=sq_tools.ret_xci_offsets(filename)
            f = Fs.Xci(filename)
            f.extract_nca(ofolder,files_list,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# NCA_2_PLAINTEXT. EXTRACT OR CONVERT NCA FILES TO PLAINTEXT FROM NSP\XCI\NCA
def cmd_extract_plain_nca(args):
    if args.buffer:
        for var in args.buffer:
            try:
                buffer = var
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    ofolder=False
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.text_file:
        tfile=args.text_file
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
            if ofolder != False:
                dir=ofolder
            else:
                dir=os.path.dirname(os.path.abspath(filename))
            basename=str(os.path.basename(os.path.abspath(filename)))
            basename=basename[:-4]
            ofolder =os.path.join(dir, basename)
    else:
        for filename in args.extract_plain_nca:
            if ofolder != False:
                dir=ofolder
            else:
                dir=os.path.dirname(os.path.abspath(filename))
            basename=str(os.path.basename(os.path.abspath(filename)))
            basename=basename[:-4]
            ofolder =os.path.join(dir, basename)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if filename.endswith('.nsp'):
        try:
            files_list=sq_tools.ret_nsp_offsets(filename)
            f = Fs.Nsp(filename, 'rb')
            f.copy_as_plaintext(ofolder,files_list,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith('.xci'):
        try:
            files_list=sq_tools.ret_xci_offsets(filename)
            #print(files_list)
            f = Fs.Xci(filename)
            f.copy_as_plaintext(ofolder,files_list,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Read npdm from inside nsp or xci
def cmd_Read_npdm(args):
    if args.ofolder:
        for var in args.ofolder:
            try:
                ofolder = var
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.Read_npdm:
            dir=os.path.dirname(os.path.abspath(filename))
            info='INFO'
            ofolder =os.path.join(dir,info)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.text_file:
        tfile=args.text_file
        dir=os.path.dirname(os.path.abspath(tfile))
        if not os.path.exists(dir):
            os.makedirs(dir)
        err='badfiles.txt'
        errfile = os.path.join(dir, err)
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
    else:
        for filename in args.Read_npdm:
            filename=filename
    basename=str(os.path.basename(os.path.abspath(filename)))
    ofile=basename[:-4]+'-npdm.txt'
    infotext=os.path.join(ofolder, ofile)
    if filename.endswith(".nsp"):
        try:
            files_list=sq_tools.ret_nsp_offsets(filename)
            f = Fs.Nsp(filename, 'rb')
            feed=f.read_npdm(files_list)
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith(".xci"):
        try:
            files_list=sq_tools.ret_xci_offsets(filename)
            f = Fs.Xci(filename)
            feed=f.read_npdm(files_list)
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
# Read cnmt inside nsp or xci
def cmd_Read_cnmt(args):
    if args.ofolder:
        for var in args.ofolder:
            try:
                ofolder = var
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.Read_cnmt:
            dir=os.path.dirname(os.path.abspath(filename))
            info='INFO'
            ofolder =os.path.join(dir,info)
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.text_file:
        tfile=args.text_file
        dir=os.path.dirname(os.path.abspath(tfile))
        if not os.path.exists(dir):
            os.makedirs(dir)
        err='badfiles.txt'
        errfile = os.path.join(dir, err)
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
    else:
        for filename in args.Read_cnmt:
            filename=filename
    basename=str(os.path.basename(os.path.abspath(filename)))
    ofile=basename[:-4]+'-meta.txt'
    infotext=os.path.join(ofolder, ofile)
    if filename.endswith('.nsp') or filename.endswith('.nsx') or filename.endswith('.nsz'):
        try:
            f = Fs.Nsp(filename, 'rb')
            feed=f.read_cnmt()
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith('.xci') or filename.endswith('.xcz'):
        try:
            f = Fs.factory(filename)
            f.open(filename, 'rb')
            feed=f.read_cnmt()
            f.flush()
            f.close()
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
    if filename.endswith('.nca'):
        try:
            f = Fs.Nca(filename, 'rb')
            if 	str(f.header.contentType) == 'Content.META':
                feed=f.read_cnmt()
                f.flush()
                f.close()
            else:
                basename=str(os.path.basename(os.path.abspath(filename)))
                basename=basename.lower()
                feed=''
                message=basename+' is not a TYPE META NCA';print(message);feed+=message+'\n'
            if not args.text_file:
                print('\n********************************************************')
                print('Do you want to print the information to a text file')
                print('********************************************************')
                i=0
                while i==0:
                    print('Input "1" to print to text file')
                    print('Input "2" to NOT print to text file\n')
                    ck=input('Input your answer: ')
                    if ck ==str(1):
                        with open(infotext, 'w') as info:
                            info.write(feed)
                        i=1
                    elif ck ==str(2):
                        i=1
                    else:
                        print('WRONG CHOICE\n')
        except BaseException as e:
            Utils.logError(e)
# Change Required System Version in an nca file
def cmd_patchversion(args):
    for input in args.patchversion:
        try:
            if input!="false":
                number = int(input)
                break
        except BaseException as e:
            Utils.logError(e)
    else:
        number = 336592896
# Changes cnmt.nca RSV
def cmd_set_cnmt_RSV(args):
    for filename in args.set_cnmt_RSV:
        if filename.endswith('.nca'):
            try:
                f = Fs.Nca(filename, 'r+b')
                f.write_req_system(number)
                f.flush()
                f.close()
                ############################
                f = Fs.Nca(filename, 'r+b')
                sha=f.calc_pfs0_hash()
                f.flush()
                f.close()
                f = Fs.Nca(filename, 'r+b')
                f.set_pfs0_hash(sha)
                f.flush()
                f.close()
                ############################
                f = Fs.Nca(filename, 'r+b')
                sha2=f.calc_htable_hash()
                f.flush()
                f.close()
                f = Fs.Nca(filename, 'r+b')
                f.header.set_htable_hash(sha2)
                f.flush()
                f.close()
                ########################
                f = Fs.Nca(filename, 'r+b')
                sha3=f.header.calculate_hblock_hash()
                f.flush()
                f.close()
                f = Fs.Nca(filename, 'r+b')
                f.header.set_hblock_hash(sha3)
                f.flush()
                f.close()
                ########################
                with open(filename, 'r+b') as file:
                    nsha=sha256(file.read()).hexdigest()
                newname=nsha[:32] + '.cnmt.nca'
                Print.info('New name: ' + newname )
                dir=os.path.dirname(os.path.abspath(filename))
                newpath =os.path.join(dir, newname)
                os.rename(filename, newpath)
            except BaseException as e:
                Utils.logError(e)
        if filename.endswith('.nsp'):
            try:
                f = Fs.Nsp(filename, 'r+b')
                f.metapatcher(number)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
#parser.add_argument('--set_cnmt_titleid', nargs='+', help='Changes cnmt.nca titleid')
def cmd_set_cnmt_titleid(args):
    filename=args.set_cnmt_titleid[0]
    value=args.set_cnmt_titleid[1]
    if filename.endswith('.nca'):
        try:
            f = Fs.Nca(filename, 'r+b')
            f.header.setTitleID(value)
            print(hx(f.header.getTitleID()))
            f.flush()
            f.close()
            ############################
            f = Fs.Nca(filename, 'r+b')
            f.write_cnmt_titleid(value)
            f.write_cnmt_updid(value[:-4]+'80'+value[-1])
            #print(hx(f.get_cnmt_titleid()))
            f.flush()
            f.close()
            ############################
            f = Fs.Nca(filename, 'r+b')
            #f.write_cnmt_titleid(value)
            print(hx(f.get_cnmt_titleid()))
            f.flush()
            f.close()
            ############################
            f = Fs.Nca(filename, 'r+b')
            sha=f.calc_pfs0_hash()
            Print.info(tabs + '- Calculated hash from pfs0: ')
            Print.info(tabs +'  + '+ str(hx(sha)))
            f.flush()
            f.close()
            f = Fs.Nca(filename, 'r+b')
            f.set_pfs0_hash(sha)
            f.flush()
            f.close()
            ############################
            f = Fs.Nca(filename, 'r+b')
            sha2=f.calc_htable_hash()
            Print.info(tabs + '- Calculated hash from pfs0: ')
            Print.info(tabs +'  + '+ str(hx(sha2)))
            f.flush()
            f.close()
            f = Fs.Nca(filename, 'r+b')
            f.header.set_htable_hash(sha2)
            f.flush()
            f.close()
            ########################
            f = Fs.Nca(filename, 'r+b')
            sha3=f.header.calculate_hblock_hash()
            Print.info(tabs + '- Calculated hash from pfs0: ')
            Print.info(tabs +'  + '+ str(hx(sha3)))
            f.flush()
            f.close()
            f = Fs.Nca(filename, 'r+b')
            f.header.set_hblock_hash(sha3)
            f.flush()
            f.close()
            ########################
            with open(filename, 'r+b') as file:
                nsha=sha256(file.read()).hexdigest()
            newname=nsha[:32] + '.cnmt.nca'
            Print.info('New name: ' + newname )
            dir=os.path.dirname(os.path.abspath(filename))
            newpath =os.path.join(dir, newname)					
            os.rename(filename, newpath)
        except BaseException as e:
            Utils.logError(e)
# Change version number from nca
def cmd_set_cnmt_version(args):
    if args.patchversion:
        for input in args.patchversion:
            try:
                number = input
            except BaseException as e:
                Utils.logError(e)
    else:
        number = 65536
    for filename in args.set_cnmt_version:
        if filename.endswith('.nca'):
            try:
                f = Fs.Nca(filename, 'r+b')
                f.write_version(number)
                f.flush()
                f.close()
                ############################
                f = Fs.Nca(filename, 'r+b')
                sha=f.calc_pfs0_hash()
                f.flush()
                f.close()
                f = Fs.Nca(filename, 'r+b')
                f.set_pfs0_hash(sha)
                f.flush()
                f.close()
                ############################
                f = Fs.Nca(filename, 'r+b')
                sha2=f.calc_htable_hash()
                f.flush()
                f.close()
                f = Fs.Nca(filename, 'r+b')
                f.header.set_htable_hash(sha2)
                f.flush()
                f.close()
                ########################
                f = Fs.Nca(filename, 'r+b')
                sha3=f.header.calculate_hblock_hash()
                f.flush()
                f.close()
                f = Fs.Nca(filename, 'r+b')
                f.header.set_hblock_hash(sha3)
                f.flush()
                f.close()
                ########################
                with open(filename, 'r+b') as file:
                    nsha=sha256(file.read()).hexdigest()
                newname=nsha[:32] + '.cnmt.nca'
                Print.info('New name: ' + newname )
                dir=os.path.dirname(os.path.abspath(filename))
                newpath =os.path.join(dir, newname)
                os.rename(filename, newpath)
            except BaseException as e:
                Utils.logError(e)
# Read hfs0
def cmd_Read_hfs0(args):
    for filename in args.Read_hfs0:
            try:
                f = Fs.factory(filename)
                f.open(filename, 'rb')
                f.readhfs0()
                #f.printInfo()
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
# Update hashes in cnmt file
def cmd_update_hash(args):
    for filename in args.update_hash:
        if filename.endswith('.nca'):
            try:
                f = Fs.Nca(filename, 'r+b')
                pfs0_size,block_size,multiplier=f.get_pfs0_hash_data()
                Print.info('block size in bytes: ' + str(hx(block_size.to_bytes(8, byteorder='big'))))
                Print.info('Pfs0 size: ' +  str(hx(pfs0_size.to_bytes(8, byteorder='big'))))
                Print.info('Multiplier: ' +  str(multiplier))
                f.flush()
                f.close()
                ############################
                f = Fs.Nca(filename, 'r+b')
                sha=f.calc_pfs0_hash()
                f.flush()
                f.close()
                f = Fs.Nca(filename, 'r+b')
                f.set_pfs0_hash(sha)
                f.flush()
                f.close()
                ############################
                f = Fs.Nca(filename, 'r+b')
                sha2=f.calc_htable_hash()
                f.flush()
                f.close()
                f = Fs.Nca(filename, 'r+b')
                f.header.set_htable_hash(sha2)
                f.flush()
                f.close()
                ########################
                f = Fs.Nca(filename, 'r+b')
                sha3=f.header.calculate_hblock_hash()
                f.flush()
                f.close()
                f = Fs.Nca(filename, 'r+b')
                f.header.set_hblock_hash(sha3)
                f.flush()
                f.close()
                ########################
                with open(filename, 'r+b') as file:
                    nsha=sha256(file.read()).hexdigest()
                newname=nsha[:32] + '.cnmt.nca'
                Print.info('New name: ' + newname )
                dir=os.path.dirname(os.path.abspath(filename))
                newpath =os.path.join(dir, newname)
                os.rename(filename, newpath)
            except BaseException as e:
                Utils.logError(e)

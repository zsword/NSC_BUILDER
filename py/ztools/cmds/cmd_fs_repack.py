#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import Utils
import Fs
if sys.platform == 'win32':
    import win32con, win32api
import shutil

# REPACK
# Repack NCA files to NSP  
def cmd_create(args):
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.fat:
        for input in args.fat:
            try:
                if input == "fat32":
                    fat="fat32"
                else:
                    fat="exfat"
            except BaseException as e:
                Utils.logError(e)
    else:
        fat="exfat"
    if args.fexport:
        for input in args.fexport:
            try:
                if input == "files":
                    fx="files"
                else:
                    fx="folder"
            except BaseException as e:
                Utils.logError(e)
    else:
        fx="files"
    if args.ifolder:
        ruta = args.ifolder
        f_list = list()
        ncalist = list()
        orderlist = list()
        for dirpath, dnames, fnames in os.walk(ruta):
            for f in fnames:
                if f.endswith('.cnmt.nca'):
                    try:
                        filepath = os.path.join(ruta, f)
                        nca = Fs.Nca(filepath, 'r+b')
                        ncalist=ncalist+nca.ncalist_bycnmt()
                    except BaseException as e:
                        Utils.logError(e)
            for f in fnames:
                filepath = os.path.join(ruta, f)
                f_list.append(filepath)
            for f in ncalist:
                fpath= os.path.join(ruta, f)
                if fpath in f_list:
                    orderlist.append(fpath)
            for f in fnames:
                if f.endswith('.cnmt'):
                    fpath= os.path.join(ruta, f)
                    orderlist.append(fpath)
            for f in fnames:
                if f.endswith('.jpg'):
                    fpath= os.path.join(ruta, f)
                    orderlist.append(fpath)
            for f in fnames:
                if f.endswith('.tik') or f.endswith('.cert'):
                    fpath= os.path.join(ruta, f)
                    orderlist.append(fpath)
            nsp = Fs.Nsp(None, None)
            nsp.path = args.create
            nsp.pack(orderlist,buffer,fat,fx)
            #print (f_list)
            #print (fnames)
            #print (ncalist)
            #print (orderlist)
    else:
        nsp = Fs.Nsp(None, None)
        nsp.path = args.create
        nsp.pack(args.file,buffer,fat,fx)
    #for filePath in args.file:
    #	Print.info(filePath)


# parser.add_argument('-cpr', '--compress', help='Compress a nsp or xci')
def cmd_compress(args):
    if args.text_file:
        tfile=args.text_file
        with open(tfile,"r+", encoding='utf8') as filelist: 	
            filepath = filelist.readline()
            filepath=os.path.abspath(filepath.rstrip('\n'))	
        if isinstance(args.compress, list):
            inputs=len(args.compress)	
            try:
                if inputs==1:
                    level=int(args.compress[0])			
                elif inputs>1:
                    level=int(args.compress[(int(inputs)-1)])
                else:
                    level=17
            except:		
                level=17
        else:
            try:
                level=int(args.compress)
            except:	
                level=17
    else:
        if isinstance(args.compress, list):
            filepath=args.compress[0]
            inputs=len(args.compress)	
            if inputs>1:
                level=int(args.compress[(int(inputs)-1)])
            else:
                level=17
        else:
            filepath=args.compress
            level=17
    if filepath.endswith(".nsp") or filepath.endswith(".xci"):			
        import compressor
        try:
            level=int(level)
            if level>22:
                level=22
            if level<1:
                level=1							
        except:
            level=17
        if filepath.endswith(".nsp"): 	
            compressor.compress(filepath,ofolder,level,workers,delta,pos=position,nthreads=n_instances)
        elif filepath.endswith(".xci"):	
            basename=os.path.basename(os.path.abspath(filepath))
            if xci_exp=='nsz':
                outfile=basename[:-3]+'nsz'
                outfile =os.path.join(ofolder,outfile)	
                nszPath=compressor.xci_to_nsz(filepath,buffer=65536,outfile=outfile,keepupd=False,level = level, threads = workers,pos=position,nthreads=n_instances)												
                try:
                    f=Fs.Nsp(nszPath,'rb+')
                    f.seteshop()
                    f.flush()
                    f.close()
                except:pass	
            else:	
                outfile=basename[:-3]+'xcz'
                outfile =os.path.join(ofolder,outfile)							
                compressor.supertrim_xci(filepath,buffer=65536,outfile=outfile,keepupd=False,level = level, threads = workers,pos=position,nthreads=n_instances)						
# parser.add_argument('-dcpr', '--decompress', help='deCompress a nsz, xcz or ncz')
def cmd_decompress(args):
    if args.ofolder:		
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)	
    else:
        if type(args.decompress)==str:
            args.decompress=[args.decompress]
        for filepath in args.decompress:
            dir=os.path.dirname(os.path.abspath(filepath))
            ofolder =os.path.join(dir, 'output')
            break
    if args.decompress:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist: 	
                filepath = filelist.readline()
                filepath=os.path.abspath(filepath.rstrip('\n'))	
        else:
            for inpt in args.decompress:
                filepath=inpt
                break
        if filepath.endswith(".nsz"):	
            import decompressor	
            basename=os.path.basename(os.path.abspath(filepath))
            endname=basename[:-1]+'p'
            endname =os.path.join(ofolder,endname)
            decompressor.decompress_nsz(filepath,endname)		
        if filepath.endswith(".xcz"):	
            import decompressor	
            basename=os.path.basename(os.path.abspath(filepath))
            endname=basename[:-3]+'xci'
            endname =os.path.join(ofolder,endname)
            decompressor.decompress_xcz(filepath,endname)
# Repack NCA files to partition hfs0
def cmd_create_hfs0(args):
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    hfs0 = Fs.Hfs0(None, None)
    hfs0.path = args.create_hfs0
    if args.ifolder:
        ruta = args.ifolder
        f_list = list()
        for dirpath, dnames, fnames in os.walk(ruta):
            for f in fnames:
                filepath = os.path.join(ruta, f)
                f_list.append(filepath)
        hfs0.pack(f_list,buffer)
    else:
        hfs0.pack(args.file,buffer)
# Repack NCA files to root_hfs0
def cmd_create_rhfs0(args):
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.ifolder:
        ruta = args.ifolder
        ruta_update=os.path.join(ruta, "update")
        ruta_normal=os.path.join(ruta, "normal")
        ruta_secure=os.path.join(ruta, "secure")
        if os.path.isdir(ruta_update) == True:
            upd_list = list()
            for dirpath, dnames, fnames in os.walk(ruta_update):
                for f in fnames:
                    filepath = os.path.join(ruta_update, f)
                    upd_list.append(filepath)
        else:
            upd_list = list()
        if os.path.isdir(ruta_normal) == True:
            norm_list = list()
            for dirpath, dnames, fnames in os.walk(ruta_normal):
                for f in fnames:
                    filepath = os.path.join(ruta_normal, f)
                    norm_list.append(filepath)
        else:
            norm_list = list()
        if os.path.isdir(ruta_secure) == True:
            sec_list = list()
            for dirpath, dnames, fnames in os.walk(ruta_secure):
                for f in fnames:
                    filepath = os.path.join(ruta_secure, f)
                    sec_list.append(filepath)
        else:
            sec_list = list()
    else:
        if args.ifolder_update:
            ruta = args.ifolder_update
            upd_list = list()
            for dirpath, dnames, fnames in os.walk(ruta):
                for f in fnames:
                    filepath = os.path.join(ruta, f)
                    upd_list.append(filepath)
        else:
            upd_list = list()
        if args.ifolder_normal:
            ruta = args.ifolder_normal
            norm_list = list()
            for dirpath, dnames, fnames in os.walk(ruta):
                for f in fnames:
                    filepath = os.path.join(ruta, f)
                    norm_list.append(filepath)
        else:
            norm_list = list()
        if args.ifolder_secure:
            ruta = args.ifolder_secure
            sec_list = list()
            for dirpath, dnames, fnames in os.walk(ruta):
                for f in fnames:
                    filepath = os.path.join(ruta, f)
                    sec_list.append(filepath)
        else:
            sec_list = list()

    #print (upd_list)
    #print (norm_list)
    #print (sec_list)
    hfs0 = Fs.Hfs0(None, None)
    hfs0.path = args.create_rhfs0
    hfs0.pack_root(upd_list,norm_list,sec_list,buffer)
# Repack NCA files to xci
def cmd_create_xci(args):
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.fat:
        for input in args.fat:
            try:
                if input == "fat32":
                    fat="fat32"
                else:
                    fat="exfat"
            except BaseException as e:
                Utils.logError(e)
    else:
        fat="exfat"
    if args.ifolder:
        ruta = args.ifolder
        ruta_update=os.path.join(ruta, "update")
        ruta_normal=os.path.join(ruta, "normal")
        ruta_secure=os.path.join(ruta, "secure")
        if os.path.isdir(ruta_update) == True:
            upd_list = list()
            for dirpath, dnames, fnames in os.walk(ruta_update):
                for f in fnames:
                    filepath = os.path.join(ruta_update, f)
                    upd_list.append(filepath)
        else:
            upd_list = list()
        if os.path.isdir(ruta_normal) == True:
            norm_list = list()
            for dirpath, dnames, fnames in os.walk(ruta_normal):
                for f in fnames:
                    filepath = os.path.join(ruta_normal, f)
                    norm_list.append(filepath)
        else:
            norm_list = list()
        if os.path.isdir(ruta_secure) == True:
            sec_list = list()
            for dirpath, dnames, fnames in os.walk(ruta_secure):
                for f in fnames:
                    filepath = os.path.join(ruta_secure, f)
                    sec_list.append(filepath)
        else:
            sec_list = list()
    else:
        if args.ifolder_update:
            ruta = args.ifolder_update
            upd_list = list()
            for dirpath, dnames, fnames in os.walk(ruta):
                for f in fnames:
                    filepath = os.path.join(ruta, f)
                    upd_list.append(filepath)
        else:
            upd_list = list()
        if args.ifolder_normal:
            ruta = args.ifolder_normal
            norm_list = list()
            for dirpath, dnames, fnames in os.walk(ruta):
                for f in fnames:
                    filepath = os.path.join(ruta, f)
                    norm_list.append(filepath)
        else:
            norm_list = list()
        if args.ifolder_secure:
            ruta = args.ifolder_secure
            sec_list = list()
            for dirpath, dnames, fnames in os.walk(ruta):
                for f in fnames:
                    filepath = os.path.join(ruta, f)
                    sec_list.append(filepath)
        else:
            sec_list = list()

    #print (upd_list)
    #print (norm_list)
    #print (sec_list)
    xci = Fs.Xci(None)
    xci.path = args.create_xci
    xci.pack(upd_list,norm_list,sec_list,buffer,fat)
# Supertrimm a xci
def cmd_xci_super_trim(args):
    try:
        if str(args.xci_super_trim[1]).lower() == "keepupd":
            keepupd=True
        else:
            keepupd=False
    except:
        keepupd=False
    try:
        if str(args.nodecompress).lower() == "true":
            nodecompress=True
        else:
            nodecompress=False
    except:
        nodecompress=True				
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.text_file:
        tfile=args.text_file
        with open(tfile,"r+", encoding='utf8') as filelist:
            filepath = filelist.readline()
            filepath=os.path.abspath(filepath.rstrip('\n'))
    else:
        if args.xci_super_trim[0] !="":
            filepath=args.xci_super_trim[0]
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        dir=os.path.dirname(os.path.abspath(filepath))
        ofolder =os.path.join(dir, 'output')		
    if args.fat:
        for input in args.fat:
            try:
                if input == "fat32":
                    fat="fat32"
                else:
                    fat="exfat"
            except BaseException as e:
                Utils.logError(e)
    else:
        fat="exfat"
    if filepath.endswith('.xci'):
        try:
            f = Fs.factory(filepath)
            filename=os.path.basename(os.path.abspath(filepath))
            #print(filename)
            outfile = os.path.join(ofolder, filename)
            #print(f.path)
            f.open(filepath, 'rb')
            f.supertrim(buffer,outfile,ofolder,fat,keepupd)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    elif filepath.endswith('.xcz'):
        f = Fs.Xci(filepath)
        filename=os.path.basename(os.path.abspath(filepath))
        outfile = os.path.join(ofolder, filename)
        f.supertrim(buffer,outfile,ofolder,keepupd,nodecompress=True)
        f.flush()
        f.close()					
# Normal trimming for xci files
def cmd_xci_trim(args):
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.text_file:
        tfile=args.text_file
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
            dir=os.path.dirname(os.path.abspath(filename))
        if args.ofolder:
            for input in args.ofolder:
                try:
                    ofolder = input
                except BaseException as e:
                    Utils.logError(e)				
        else:				
            ofolder =os.path.join(dir, 'output')
    else:
        for filename in args.xci_trim:
            dir=os.path.dirname(os.path.abspath(filename))
        if args.ofolder:
            for input in args.ofolder:
                try:
                    ofolder = input
                except BaseException as e:
                    Utils.logError(e)				
        else:				
            ofolder =os.path.join(dir, 'output')
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.fat:
        for input in args.fat:
            try:
                if input == "fat32":
                    fat="fat32"
                else:
                    fat="exfat"
            except BaseException as e:
                Utils.logError(e)
    else:
        fat="exfat"
    if not args.text_file:	
        for filepath in args.xci_trim:
            if filepath.endswith('.xci'):
                try:
                    f = Fs.factory(filepath)
                    filename=os.path.basename(os.path.abspath(filepath))
                    #print(filename)
                    outfile = os.path.join(ofolder, filename)
                    #print(f.path)
                    f.open(filepath, 'rb')
                    f.trim(buffer,outfile,ofolder,fat)
                    f.flush()
                    f.close()
                except BaseException as e:
                    Utils.logError(e)
    else:
        filepath=filename
        if filepath.endswith('.xci'):
            try:
                f = Fs.factory(filepath)
                filename=os.path.basename(os.path.abspath(filepath))
                #print(filename)
                outfile = os.path.join(ofolder, filename)
                #print(f.path)
                f.open(filepath, 'rb')
                f.trim(buffer,outfile,ofolder,fat)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)		
# Untrimming for xci files
#parser.add_argument('-xci_untr', '--xci_untrim', nargs='+', help='Untrims xci')
def cmd_xci_untrim(args):
    filename=None
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    if args.text_file:
        tfile=args.text_file
        with open(tfile,"r+", encoding='utf8') as filelist:
            filename = filelist.readline()
            filename=os.path.abspath(filename.rstrip('\n'))
            if not args.ofolder:
                dir=os.path.dirname(os.path.abspath(filename))
                ofolder =os.path.join(dir, 'output')
    elif not args.ofolder:
        for filename in args.xci_untrim:
            if filename.endswith('.xci'):
                dir=os.path.dirname(os.path.abspath(filename))
                ofolder =os.path.join(dir, 'output')
                break
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.fat:
        for input in args.fat:
            try:
                if input == "fat32":
                    fat="fat32"
                else:
                    fat="exfat"
            except BaseException as e:
                Utils.logError(e)
    else:
        fat="exfat"
    if filename==None:	
        for filepath in args.xci_untrim:
            if filepath.endswith('.xci'):
                filename=filepath
    filepath=filename			
    try:
        f = Fs.factory(filepath)
        filename=os.path.basename(os.path.abspath(filepath))
        #print(filename)
        outfile = os.path.join(ofolder, filename)
        #print(f.path)
        f.open(filepath, 'rb')
        f.untrim(buffer,outfile,ofolder,fat)
        f.flush()
        f.close()
    except BaseException as e:
        Utils.logError(e)
# Take off deltas
def cmd_erase_deltas(args):
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filepath in args.erase_deltas:
            dir=os.path.dirname(os.path.abspath(filepath))
            ofolder = os.path.join(dir, 'output')
    if args.xml_gen:
        for input in args.xml_gen:
            try:
                if input == "true" or input == "True" or input == "TRUE":
                    xml_gen=True
                elif input == "false" or input == "False" or input == "FALSE":
                    xml_gen=False
                else:
                    xml_gen=False
            except BaseException as e:
                Utils.logError(e)
    if args.erase_deltas:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filepath = filelist.readline()
                filepath=os.path.abspath(filepath.rstrip('\n'))
        else:
            for filepath in args.erase_deltas:
                filepath=filepath
        endfile=os.path.basename(os.path.abspath(filepath))
        endfile=os.path.join(ofolder,endfile)
        if not os.path.exists(ofolder):
            os.makedirs(ofolder)
        if filepath.endswith(".nsp") or filepath.endswith(".nsz"):
            try:
                print('Processing: '+filepath)
                f = Fs.Nsp(filepath)
                f.rebuild(buffer,endfile,False,True,xml_gen)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
# Rebuild
def cmd_rebuild_nsp(args):
    skipper=False
    Damage=False
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.type:
        for input in args.type:
            if input == "nsp":
                export='nsp'
            elif input == "nsz":
                export='nsz'
            else:
                export='nsp'
    else:
        export='nsp'				
    if args.text_file:
        tfile=args.text_file
        with open(tfile,"r+", encoding='utf8') as filelist:
            filepath = filelist.readline()
            filepath=os.path.abspath(filepath.rstrip('\n'))
    elif args.ifolder:
        filepath=args.ifolder
    else:
        for filepath in args.rebuild_nsp:
            filepath=filepath
    if args.nodelta:
        for input in args.nodelta:
            try:
                if input == "true" or input == "True" or input == "TRUE":
                    delta=False
                elif input == "false" or input == "False" or input == "FALSE":
                    delta=True
                else:
                    delta=False
            except BaseException as e:
                Utils.logError(e)
    else:
        delta=True
    if args.xml_gen:
        for input in args.xml_gen:
            try:
                if input == "true" or input == "True" or input == "TRUE":
                    xml_gen=True
                elif input == "false" or input == "False" or input == "FALSE":
                    xml_gen=False
                else:
                    xml_gen=False
            except BaseException as e:
                Utils.logError(e)
    else:
        xml_gen=False
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filepath in args.rebuild_nsp:
            dir=os.path.dirname(os.path.abspath(filepath))
            ofolder = os.path.join(dir, 'output')
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    endfile=os.path.basename(os.path.abspath(filepath))
    endfile=os.path.join(ofolder,endfile)
    if args.v_organize:
        if args.v_organize != 'false':
            base_folder=os.path.join(ofolder,'base')
            update_folder=os.path.join(ofolder,'updates')
            dlc_folder=os.path.join(ofolder,'dlcs')
            if not os.path.exists(base_folder):
                os.makedirs(base_folder)
            if not os.path.exists(update_folder):
                os.makedirs(update_folder)
            if not os.path.exists(dlc_folder):
                os.makedirs(dlc_folder)
            try:
                f = Fs.Nsp(filepath)
                ctype=f.nsptype()
                #print(ctype)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
                Damage=True
                skipper=True
                print('Content seems to be damaged')
            if Damage==False:
                if 	ctype=='BASE':
                    endfile=os.path.basename(os.path.abspath(filepath))
                    endfile=os.path.join(base_folder,endfile)
                elif ctype=='UPDATE':
                    endfile=os.path.basename(os.path.abspath(filepath))
                    endfile=os.path.join(update_folder,endfile)
                elif ctype=='DLC':
                    endfile=os.path.basename(os.path.abspath(filepath))
                    endfile=os.path.join(dlc_folder,endfile)
                else:
                    print("Content can't be identified")
                    skipper=True
                print('Final destination:')
                print('  > '+endfile)
                if os.path.exists(endfile):
                    skipper=True
                    print("Content exists in final destination. Skipping...")
    if not args.ifolder:
        if args.rebuild_nsp and skipper==False:
            if filepath.endswith(".nsp"):
                try:
                    print('Processing: '+filepath)
                    f = Fs.Nsp(filepath)
                    f.rebuild(buffer,endfile,delta,False,xml_gen)
                    f.flush()
                    f.close()
                except BaseException as e:
                    Utils.logError(e)				
            elif filepath.endswith(".nsz"):
                if export == 'nsp':
                    try:
                        import decompressor	
                        basename=os.path.basename(os.path.abspath(filepath))
                        endname=basename[:-1]+'p'
                        endname =os.path.join(ofolder,endname)
                        decompressor.decompress_nsz(filepath,endname,buffer,delta,xml_gen)	
                    except BaseException as e:
                        Utils.logError(e)	
    else:
        import batchprocess
        batchprocess.rebuild_nsp(filepath,ofolder,buffer,delta,xml_gen,export)	
# Direct NSP OR XCI
def cmd_direct_creation(args):
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.nodelta:
        for input in args.nodelta:
            try:
                if input == "true" or input == "True" or input == "TRUE":
                    delta=False
                elif input == "false" or input == "False" or input == "FALSE":
                    delta=True
                else:
                    delta=False
            except BaseException as e:
                Utils.logError(e)
    else:
        delta=True
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filepath in args.direct_creation:
            dir=os.path.dirname(os.path.abspath(filepath))
            ofolder =os.path.join(dir, 'output')
    if args.fat:
        for input in args.fat:
            try:
                if input == "fat32":
                    fat="fat32"
                else:
                    fat="exfat"
            except BaseException as e:
                Utils.logError(e)
    else:
        fat="exfat"
    if args.fexport:
        for input in args.fexport:
            try:
                if input == "files":
                    fx="files"
                else:
                    fx="folder"
            except BaseException as e:
                Utils.logError(e)
    else:
        fx="files"
    if args.patchversion:
        for input in args.patchversion:
            try:
                metapatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        metapatch = 'false'
    if args.RSVcap:
        for input in args.RSVcap:
            try:
                RSV_cap = input
            except BaseException as e:
                Utils.logError(e)
    else:
        RSV_cap = 268435656
    if args.keypatch:
        for input in args.keypatch:
            try:
                vkeypatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        vkeypatch = 'false'

    if args.direct_creation:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filepath = filelist.readline()
                filepath=os.path.abspath(filepath.rstrip('\n'))
        else:
            for filepath in args.direct_creation:
                filepath=filepath
        if args.type:
            for input in args.type:
                if input == "xci" or input == "XCI":
                    export='xci'
                elif input == "nsp" or input == "NSP":
                    export='nsp'
                elif input == "both" or input == "BOTH":
                    export='both'
                else:
                    print ("Wrong Type!!!")
        else:
            if filepath.endswith('.nsp') or filepath.endswith('.nsz'):
                export='nsp'
            elif filepath.endswith('.xci') or filepath.endswith('.xcz'):
                export='xci'
            else:
                print ("Wrong Type!!!")
        if args.rename:
            for newname in args.rename:
                newname=newname+'.xxx'
                endfile = os.path.join(ofolder, newname)
        else:
            endfile=os.path.basename(os.path.abspath(filepath))
        if args.cskip=='False':
            cskip=False
        else:
            cskip=True

        if filepath.endswith(".nsp") or filepath.endswith('.nsz'):
            f = Fs.Nsp(filepath)
            TYPE=f.nsptype()
            f.flush()
            f.close()

            if cskip==True:
                if TYPE=='DLC' or TYPE=='UPDATE':
                    export='nsp'
            if export=='nsp':
                try:
                    print("Processing: " + filepath)
                    f = Fs.factory(filepath)
                    filename=endfile[:-3]+'nsp'
                    #print(filename)
                    outfile = os.path.join(ofolder, filename)
                    #print(f.path)
                    f.open(filepath, 'rb')
                    f.c_nsp_direct(buffer,outfile,ofolder,fat,fx,delta,metapatch,RSV_cap,vkeypatch)
                    f.flush()
                    f.close()
                except BaseException as e:
                    Utils.logError(e)
            elif export=='xci':
                try:
                    print("Processing: " + filepath)
                    f = Fs.factory(filepath)
                    filename=endfile[:-3]+'xci'
                    #print(filename)
                    outfile = os.path.join(ofolder, filename)
                    #print(f.path)
                    f.open(filepath, 'rb')
                    f.c_xci_direct(buffer,outfile,ofolder,fat,fx,delta,metapatch,RSV_cap,vkeypatch)
                    f.flush()
                    f.close()
                except BaseException as e:
                    Utils.logError(e)
            elif export=='both':
                try:
                    print("Processing: " + filepath)
                    f = Fs.factory(filepath)
                    filename=endfile[:-3]+'nsp'
                    #print(filename)
                    outfile = os.path.join(ofolder, filename)
                    #print(f.path)
                    f.open(filepath, 'rb')
                    f.c_nsp_direct(buffer,outfile,ofolder,fat,fx,delta,metapatch,RSV_cap,vkeypatch)
                    f.flush()
                    f.close()
                except BaseException as e:
                    Utils.logError(e)
                try:
                    print("Processing: " + filepath)
                    f = Fs.factory(filepath)
                    filename=endfile[:-3]+'xci'
                    #print(filename)
                    outfile = os.path.join(ofolder, filename)
                    #print(f.path)
                    f.open(filepath, 'rb')
                    f.c_xci_direct(buffer,outfile,ofolder,fat,fx,delta,metapatch,RSV_cap,vkeypatch)
                    f.flush()
                    f.close()
                except BaseException as e:
                    Utils.logError(e)

        if filepath.endswith(".xci") or filepath.endswith('.xcz'):
            if export=='nsp':
                try:
                    print("Processing: " + filepath)
                    f = Fs.factory(filepath)
                    filename=endfile[:-3]+'nsp'
                    #print(filename)
                    outfile = os.path.join(ofolder, filename)
                    #print(f.path)
                    f.open(filepath, 'rb')
                    f.c_nsp_direct(buffer,outfile,ofolder,fat,fx,delta,metapatch,RSV_cap,vkeypatch)
                    f.flush()
                    f.close()
                except BaseException as e:
                    Utils.logError(e)
            elif export=='xci':
                try:
                    print("Processing: " + filepath)
                    f = Fs.factory(filepath)
                    filename=endfile[:-3]+'xci'
                    #print(filename)
                    outfile = os.path.join(ofolder, filename)
                    #print(f.path)
                    f.open(filepath, 'rb')
                    temp=f.c_xci_direct(buffer,outfile,ofolder,fat,fx,delta,metapatch,RSV_cap,vkeypatch)
                    f.flush()
                    f.close()
                except BaseException as e:
                    Utils.logError(e)
            elif export=='both':
                try:
                    print("Processing: " + filepath)
                    f = Fs.factory(filepath)
                    filename=endfile[:-3]+'nsp'
                    #print(filename)
                    outfile = os.path.join(ofolder, filename)
                    #print(f.path)
                    f.open(filepath, 'rb')
                    f.c_nsp_direct(buffer,outfile,ofolder,fat,fx,delta,metapatch,RSV_cap,vkeypatch)
                    f.flush()
                    f.close()
                except BaseException as e:
                    Utils.logError(e)
                try:
                    print("Processing: " + filepath)
                    f = Fs.factory(filepath)
                    filename=endfile[:-3]+'xci'
                    #print(filename)
                    outfile = os.path.join(ofolder, filename)
                    #print(f.path)
                    f.open(filepath, 'rb')
                    f.c_xci_direct(buffer,outfile,ofolder,fat,fx,delta,metapatch,RSV_cap,vkeypatch)
                    f.flush()
                    f.close()
                except BaseException as e:
                    Utils.logError(e)
# Direct MULTI NSP OR XCI
def cmd_direct_multi(args):
    indent = 1
    index = 0
    tabs = '\t' * indent
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.romanize:
        for input in args.romanize:
            roman=str(input).upper()
            if roman == "FALSE":
                roman = False
            else:
                roman = True
    else:
        roman = True
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
                if not os.path.exists(ofolder):
                    os.makedirs(ofolder)
            except BaseException as e:
                Utils.logError(e)
    else:
        for filepath in args.direct_multi:
            dir=os.path.dirname(os.path.abspath(filepath))
            ofolder = os.path.join(dir, 'output')
            if not os.path.exists(ofolder):
                os.makedirs(ofolder)
    if args.fat:
        for input in args.fat:
            try:
                if input == "fat32":
                    fat="fat32"
                else:
                    fat="exfat"
            except BaseException as e:
                Utils.logError(e)
    else:
        fat="exfat"
    if args.fexport:
        for input in args.fexport:
            try:
                if input == "files":
                    fx="files"
                else:
                    fx="folder"
            except BaseException as e:
                Utils.logError(e)
    else:
        fx="files"
    if args.nodelta:
        for input in args.nodelta:
            try:
                if input == "true" or input == "True" or input == "TRUE":
                    delta=False
                elif input == "false" or input == "False" or input == "FALSE":
                    delta=True
                else:
                    delta=False
            except BaseException as e:
                Utils.logError(e)
    else:
        delta=True

    if args.patchversion:
        for input in args.patchversion:
            try:
                metapatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        metapatch = 'false'
    if args.RSVcap:
        for input in args.RSVcap:
            try:
                RSV_cap = input
            except BaseException as e:
                Utils.logError(e)
    else:
        RSV_cap = 268435656
    if args.keypatch:
        for input in args.keypatch:
            try:
                vkeypatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        vkeypatch = 'false'
    export=list()
    if args.type:
        for input in args.type:
            if input == "xci" or input == "XCI":
                export.append('xci')
            elif input == "nsp" or input == "NSP":
                export.append('nsp')
            elif input == "cnsp" or input == "CNSP":
                export.append('cnsp')
            else:
                print ("Wrong Type!!!")

    if args.direct_multi:
        if args.text_file:
            tfile=args.text_file
            filelist=list()
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as f:
                for line in f:
                    fp=line.strip()
                    filelist.append(fp)
            '''
            for file in filelist:
                print(file)
                pass
            '''
            prlist=list()
            print ('Calculating final content:')
            for filepath in filelist:
                if filepath.endswith('.nsp') or filepath.endswith('.nsz'):
                    #print(filepath)
                    try:
                        c=list()
                        f = Fs.Nsp(filepath)
                        if 'nsp' in export or 'cnsp' in export:
                            afolder=False
                            if fat=="fat32" and fx=="folder":
                                afolder=os.path.join(ofolder,"archfolder")
                                if not os.path.exists(afolder):
                                    os.makedirs(afolder)
                                contentlist=f.get_content(afolder,vkeypatch,delta)
                            else:
                                contentlist=f.get_content(ofolder,vkeypatch,delta)
                        else:
                            contentlist=f.get_content(False,False,delta)
                        # print(contentlist)
                        f.flush()
                        f.close()
                        if len(prlist)==0:
                            for i in contentlist:
                                prlist.append(i)
                            #print (prlist)
                        else:
                            for j in range(len(contentlist)):
                                notinlist=False
                                for i in range(len(prlist)):
                                    #print (contentlist[j][1])
                                    #print (prlist[i][1])
                                    #print (contentlist[j][6])
                                    #print (prlist[i][6])
                                    #pass
                                    if contentlist[j][1] == prlist[i][1]:
                                        #print('true')
                                        #print(contentlist[j][6])
                                        #print(prlist[i][6])
                                        if int(contentlist[j][6]) > int(prlist[i][6]):
                                            del prlist[i]
                                            #print(prlist[i])
                                            prlist.append(contentlist[j])
                                            notinlist=False
                                            break
                                        elif int(contentlist[j][6]) <= int(prlist[i][6]):
                                            notinlist=False
                                            break
                                    else:
                                        notinlist=True
                                if notinlist == True:
                                    prlist.append(contentlist[j])
                    except BaseException as e:
                        Utils.logError(e)

                if filepath.endswith('.xci') or filepath.endswith('.xcz'):
                    #print(filepath)
                    try:
                        c=list()
                        f = Fs.Xci(filepath)
                        if 'nsp' in export or 'cnsp' in export:
                            contentlist=f.get_content(ofolder,vkeypatch,delta)
                        else:
                            contentlist=f.get_content(False,False,delta)
                        f.flush()
                        f.close()
                        if len(prlist)==0:
                            for i in contentlist:
                                prlist.append(i)
                            #print (prlist)
                        else:
                            for j in range(len(contentlist)):
                                notinlist=False
                                for i in range(len(prlist)):
                                    #print (contentlist[j][1])
                                    #print (prlist[i][1])
                                    #print (contentlist[j][6])
                                    #print (prlist[i][6])
                                    #pass
                                    if contentlist[j][1] == prlist[i][1]:
                                        #print('true')
                                        #print(contentlist[j][6])
                                        #print(prlist[i][6])
                                        if int(contentlist[j][6]) > int(prlist[i][6]):
                                            del prlist[i]
                                            #print(prlist[i])
                                            prlist.append(contentlist[j])
                                            notinlist=False
                                            break
                                        elif int(contentlist[j][6]) <= int(prlist[i][6]):
                                            notinlist=False
                                            break
                                    else:
                                        notinlist=True
                                if notinlist == True:
                                    prlist.append(contentlist[j])
                    except BaseException as e:
                        Utils.logError(e)
            '''
            for i in range(len(prlist)):
                print (prlist[i][0])
                print (prlist[i][1]+' v'+prlist[i][6])
                for j in prlist[i][4]:
                    print (j[0])
                    print (j[1])
                print('////////////////////////////////////////////////////////////')
            '''
            tnamefile=False
            for f in args.direct_multi:
                if f == 'calculate':
                    #BASE
                    basecount=0; basename='';basever='';baseid='';basefile=''
                    updcount=0; updname='';updver='';updid='';updfile=''
                    dlccount=0; dlcname='';dlcver='';dlcid='';dlcfile=''
                    ccount='';bctag='';updtag='';dctag=''
                    for i in range(len(prlist)):
                        if prlist[i][5] == 'BASE':
                            basecount+=1
                            if baseid == "":
                                basefile=str(prlist[i][0])
                                baseid=str(prlist[i][1])
                                basever='[v'+str(prlist[i][6])+']'
                        if prlist[i][5] == 'UPDATE':
                            updcount+=1
                            endver=str(prlist[i][6])
                            if updid == "":
                                updfile=str(prlist[i][0])
                                updid=str(prlist[i][1])
                                updver='[v'+str(prlist[i][6])+']'
                        if prlist[i][5] == 'DLC':
                            dlccount+=1
                            if dlcid == "":
                                dlcfile=str(prlist[i][0])
                                dlcid=str(prlist[i][1])
                                dlcver='[v'+str(prlist[i][6])+']'
                        if 	basecount !=0:
                            bctag=str(basecount)+'G'
                        else:
                            bctag=''
                        if 	updcount !=0:
                            if bctag != '':
                                updtag='+'+str(updcount)+'U'
                            else:
                                updtag=str(updcount)+'U'
                        else:
                            updtag=''
                        if 	dlccount !=0:
                            if bctag != '' or updtag != '':
                                dctag='+'+str(dlccount)+'D'
                            else:
                                dctag=str(dlccount)+'D'
                        else:
                            dctag=''
                        ccount='('+bctag+updtag+dctag+')'
                    if baseid != "":
                        try:
                            if basefile.endswith('.xci') or basefile.endswith('.xcz') :
                                f = Fs.Xci(basefile)
                            elif basefile.endswith('.nsp') or basefile.endswith('.nsz') :
                                f = Fs.Nsp(basefile)
                            ctitl=f.get_title(baseid,roman)
                            f.flush()
                            f.close()
                            if ctitl=='DLC' or ctitl=='-':
                                tnamefile=True
                        except:
                            tnamefile=True
                        if tnamefile==True:
                            ctitl=str(os.path.basename(os.path.abspath(basefile)))
                            tid1=list()
                            tid2=list()
                            tid1=[pos for pos, char in enumerate(basefile) if char == '[']
                            tid2=[pos for pos, char in enumerate(basefile) if char == ']']
                            if len(tid1)>=len(tid2):
                                lentlist=len(tid1)
                            elif len(tid1)<len(tid2):
                                lentlist=len(tid2)
                            for i in range(lentlist):
                                i1=tid1[i]
                                i2=tid2[i]+1
                                t=basefile[i1:i2]
                                ctitl=ctitl.replace(t,'')
                                ctitl=ctitl.replace('  ',' ')
                            tid3=list()
                            tid4=list()
                            tid3=[pos for pos, char in enumerate(ctitl) if char == '(']
                            tid4=[pos for pos, char in enumerate(ctitl) if char == ')']
                            if len(tid3)>=len(tid4):
                                lentlist=len(tid3)
                            elif len(tid3)<len(tid4):
                                lentlist=len(tid4)
                            for i in range(lentlist):
                                i3=tid3[i]
                                i4=tid4[i]+1
                                t=ctitl[i3:i4]
                                ctitl=ctitl.replace(t,'')
                                ctitl=ctitl.replace('  ',' ')
                            tid5=list()
                            tid5=[pos for pos, char in enumerate(ctitl) if char == '-']
                            lentlist=len(tid5)
                            for i in range(lentlist):
                                i5=tid5[i]+1
                                ctitl=ctitl[i5:]
                                break
                            ctitl=ctitl[:-4]
                            if ctitl.endswith(' '):
                                ctitl=ctitl[:-1]
                            if ctitl.startswith(' '):
                                ctitl=ctitl[1:]
                    elif updid !="":
                        try:
                            if updfile.endswith('.xci') or updfile.endswith('.xcz') :
                                f = Fs.Xci(updfile)
                            elif updfile.endswith('.nsp') or updfile.endswith('.nsz') :
                                f = Fs.Nsp(updfile)
                            ctitl=f.get_title(updid,roman)
                            f.flush()
                            f.close()
                            if ctitl=='DLC' or ctitl=='-':
                                tnamefile=True
                        except:
                            tnamefile=True
                        if tnamefile==True:
                            ctitl=str(os.path.basename(os.path.abspath(updfile)))
                            tid1=list()
                            tid2=list()
                            tid1=[pos for pos, char in enumerate(updfile) if char == '[']
                            tid2=[pos for pos, char in enumerate(updfile) if char == ']']
                            if len(tid1)>=len(tid2):
                                lentlist=len(tid1)
                            elif len(tid1)<len(tid2):
                                lentlist=len(tid2)
                            for i in range(lentlist):
                                i1=tid1[i]
                                i2=tid2[i]+1
                                t=updfile[i1:i2]
                                ctitl=ctitl.replace(t,'')
                                ctitl=ctitl.replace('  ',' ')
                            tid3=list()
                            tid4=list()
                            tid3=[pos for pos, char in enumerate(ctitl) if char == '(']
                            tid4=[pos for pos, char in enumerate(ctitl) if char == ')']
                            if len(tid3)>=len(tid4):
                                lentlist=len(tid3)
                            elif len(tid3)<len(tid4):
                                lentlist=len(tid4)
                            for i in range(lentlist):
                                i3=tid3[i]
                                i4=tid4[i]+1
                                t=ctitl[i3:i4]
                                ctitl=ctitl.replace(t,'')
                                ctitl=ctitl.replace('  ',' ')
                            tid5=list()
                            tid5=[pos for pos, char in enumerate(ctitl) if char == '-']
                            lentlist=len(tid5)
                            for i in range(lentlist):
                                i5=tid5[i]+1
                                ctitl=ctitl[i5:]
                                break
                            ctitl=ctitl[:-4]
                            if ctitl.endswith(' '):
                                ctitl=ctitl[:-1]
                            if ctitl.startswith(' '):
                                ctitl=ctitl[1:]
                    elif dlcid !="":
                        try:
                            ctitl=str(os.path.basename(os.path.abspath(dlcfile)))
                            tid1=list()
                            tid2=list()
                            tid1=[pos for pos, char in enumerate(dlcfile) if char == '[']
                            tid2=[pos for pos, char in enumerate(dlcfile) if char == ']']
                            if len(tid1)>=len(tid2):
                                lentlist=len(tid1)
                            elif len(tid1)<len(tid2):
                                lentlist=len(tid2)
                            for i in range(lentlist):
                                i1=tid1[i]
                                i2=tid2[i]+1
                                t=dlcfile[i1:i2]
                                ctitl=ctitl.replace(t,'')
                                ctitl=ctitl.replace('  ',' ')
                            tid3=list()
                            tid4=list()
                            tid3=[pos for pos, char in enumerate(ctitl) if char == '(']
                            tid4=[pos for pos, char in enumerate(ctitl) if char == ')']
                            if len(tid3)>=len(tid4):
                                lentlist=len(tid3)
                            elif len(tid3)<len(tid4):
                                lentlist=len(tid4)
                            for i in range(lentlist):
                                i3=tid3[i]
                                i4=tid4[i]+1
                                t=ctitl[i3:i4]
                                ctitl=ctitl.replace(t,'')
                                ctitl=ctitl.replace('  ',' ')
                            tid5=list()
                            tid5=[pos for pos, char in enumerate(ctitl) if char == '-']
                            lentlist=len(tid5)
                            for i in range(lentlist):
                                i5=tid5[i]+1
                                ctitl=ctitl[i5:]
                                break
                            ctitl=ctitl[:-4]
                            if ctitl.endswith(' '):
                                ctitl=ctitl[:-1]
                            if ctitl.startswith(' '):
                                ctitl=ctitl[1:]
                        except:
                            if dlcfile.endswith('.xci') or dlcfile.endswith('.xcz'):
                                f = Fs.Xci(dlcfile)
                            elif dlcfile.endswith('.nsp') or dlcfile.endswith('.nsz') :
                                f = Fs.Nsp(dlcfile)
                            ctitl=f.get_title(dlcid,roman)
                            f.flush()
                            f.close()
                    else:
                        ctitl='UNKNOWN'
                    baseid='['+baseid.upper()+']'
                    updid='['+updid.upper()+']'
                    dlcid='['+dlcid.upper()+']'
                    if ccount == '(1G)' or ccount == '(1U)' or ccount == '(1D)':
                        ccount=''
                    targetnormal=list()
                    if baseid != "[]":
                        if updver != "":
                            endname=ctitl+' '+baseid+' '+updver+' '+ccount
                            targetnormal.append([baseid[1:-1],updver[2:-1]])
                        else:
                            endname=ctitl+' '+baseid+' '+basever+' '+ccount
                            targetnormal.append([baseid[1:-1],basever[2:-1]])
                    elif updid != "[]":
                        endname=ctitl+' '+updid+' '+updver+' '+ccount
                        targetnormal.append([updid[1:-1],updver[2:-1]])
                    else:
                        endname=ctitl+' '+dlcid+' '+dlcver+' '+ccount
                        targetnormal.append([dlcid[1:-1],dlcver[2:-1]])
                    #print('Filename: '+endname)
                else:
                    endname=str(f)
        endname = (re.sub(r'[\/\\\:\*\?]+', '', endname))
        endname = re.sub(r'[™©®`~^´ªº¢#£€¥$ƒ±¬½¼♡«»±•²‰œæÆ³☆<<>>|]', '', endname)
        endname = re.sub(r'[Ⅰ]', 'I', endname);endname = re.sub(r'[Ⅱ]', 'II', endname)
        endname = re.sub(r'[Ⅲ]', 'III', endname);endname = re.sub(r'[Ⅳ]', 'IV', endname)
        endname = re.sub(r'[Ⅴ]', 'V', endname);endname = re.sub(r'[Ⅵ]', 'VI', endname)
        endname = re.sub(r'[Ⅶ]', 'VII', endname);endname = re.sub(r'[Ⅷ]', 'VIII', endname)
        endname = re.sub(r'[Ⅸ]', 'IX', endname);endname = re.sub(r'[Ⅹ]', 'X', endname)
        endname = re.sub(r'[Ⅺ]', 'XI', endname);endname = re.sub(r'[Ⅻ]', 'XII', endname)
        endname = re.sub(r'[Ⅼ]', 'L', endname);endname = re.sub(r'[Ⅽ]', 'C', endname)
        endname = re.sub(r'[Ⅾ]', 'D', endname);endname = re.sub(r'[Ⅿ]', 'M', endname)
        endname = re.sub(r'[—]', '-', endname);endname = re.sub(r'[√]', 'Root', endname)
        endname = re.sub(r'[àâá@äå]', 'a', endname);endname = re.sub(r'[ÀÂÁÄÅ]', 'A', endname)
        endname = re.sub(r'[èêéë]', 'e', endname);endname = re.sub(r'[ÈÊÉË]', 'E', endname)
        endname = re.sub(r'[ìîíï]', 'i', endname);endname = re.sub(r'[ÌÎÍÏ]', 'I', endname)
        endname = re.sub(r'[òôóöø]', 'o', endname);endname = re.sub(r'[ÒÔÓÖØ]', 'O', endname)
        endname = re.sub(r'[ùûúü]', 'u', endname);endname = re.sub(r'[ÙÛÚÜ]', 'U', endname)
        endname = re.sub(r'[’]', "'", endname);endname = re.sub(r'[“”]', '"', endname)
        endname = re.sub(' {3,}', ' ',endname);re.sub(' {2,}', ' ',endname);
        try:
            endname = endname.replace("( ", "(");endname = endname.replace(" )", ")")
            endname = endname.replace("[ ", "[");endname = endname.replace(" ]", "]")
            endname = endname.replace("[ (", "[(");endname = endname.replace(") ]", ")]")
            endname = endname.replace("[]", "");endname = endname.replace("()", "")
            endname = endname.replace('" ','"');endname = endname.replace(' "','"')
            endname = endname.replace(" !", "!");endname = endname.replace(" ?", "?")
            endname = endname.replace("  ", " ");endname = endname.replace("  ", " ")
            endname = endname.replace('"', '');
            endname = endname.replace(')', ') ');endname = endname.replace(']', '] ')
            endname = endname.replace("[ (", "[(");endname = endname.replace(") ]", ")]")
            endname = endname.replace("  ", " ")
        except:pass
        if endname[-1]==' ':
            endname=endname[:-1]
        if fat=="fat32" and fx=="folder":
            tfname='filename.txt'
            tfname = os.path.join(ofolder, tfname)
            with open(tfname,"w", encoding='utf8') as tfile:
                tfile.write(endname)
        if 'nsp' in export:
            oflist=list()
            osizelist=list()
            totSize=0
            c=0
            # print(prlist)
            for i in range(len(prlist)):
                for j in prlist[i][4]:
                    oflist.append(j[0])
                    osizelist.append(j[1])
                    totSize = totSize+j[1]
            nspheader=sq_tools.gen_nsp_header(oflist,osizelist)
            endname_x=endname+'.nsp'
            endfile = os.path.join(ofolder, str(endname_x))
            print('Filename: '+endname_x)
            #print(hx(nspheader))
            totSize = len(nspheader) + totSize
            #print(str(totSize))
            if totSize <= 4294901760:
                fat="exfat"
            if fat=="fat32":
                splitnumb=math.ceil(totSize/4294901760)
                index=0
                endfile=endfile[:-1]+str(index)
            if fx=="folder" and fat=="fat32":
                output_folder = os.path.join(ofolder, "archfolder")
                endfile = os.path.join(output_folder, "00")
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
            elif fx=="folder" and fat=="exfat":
                ext='.xml'
                if os.path.exists(afolder) and os.path.isdir(afolder):
                    for dirpath, dirnames, filenames in os.walk(afolder):
                        for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
                            filename= os.path.join(afolder,filename)
                            shutil.move(filename,ofolder)
                shutil.rmtree(afolder, ignore_errors=True)
            if sys.platform == 'win32':
                v_drive, v_path = os.path.splitdrive(endfile)
            else:
                v_drive = os.path.dirname(os.path.abspath(endfile))
            dsktotal, dskused, dskfree=disk_usage(str(v_drive))
            if int(dskfree)<int(totSize):
                sys.exit("Warning disk space lower than required size. Program will exit")					
            t = tqdm(total=totSize, unit='B', unit_scale=True, leave=False)
            outf = open(endfile, 'w+b')
            t.write(tabs+'- Writing NSP header...')
            outf.write(nspheader)
            t.update(len(nspheader))
            c=c+len(nspheader)
            outf.close()
            for filepath in filelist:
                if filepath.endswith('.nsp') or filepath.endswith('.nsz'):
                    try:
                        f = Fs.Nsp(filepath)
                        for file in oflist:
                            if not file.endswith('xml'):
                                endfile,index,c = f.append_content(endfile,file,buffer,t,fat,fx,c,index)
                        f.flush()
                        f.close()
                    except BaseException as e:
                        Utils.logError(e)
            t.close()
        if 'xci' in export:
            endname_x=endname+'.xci'
            print('Filename: '+endname_x)
            endfile = os.path.join(ofolder, endname_x)
            oflist=list()
            osizelist=list()
            ototlist=list()
            totSize=0
            for i in range(len(prlist)):
                for j in prlist[i][4]:
                    el=j[0]
                    if el.endswith('.nca'):
                        oflist.append(j[0])
                        #print(j[0])
                        totSize = totSize+j[1]
                        #print(j[1])
                    ototlist.append(j[0])
            sec_hashlist=list()
            GClist=list()
            # print(filelist)
            for filepath in filelist:
                if filepath.endswith('.nsp') or filepath.endswith('.nsz'):
                    try:
                        f = Fs.Nsp(filepath)
                        for file in oflist:
                            sha,size,gamecard=f.file_hash(file)
                            if sha != False:
                                sec_hashlist.append(sha)
                                osizelist.append(size)
                                GClist.append([file,gamecard])
                        f.flush()
                        f.close()
                    except BaseException as e:
                        Utils.logError(e)
                if filepath.endswith('.xci') or filepath.endswith('.xcz'):
                    try:
                        f = Fs.Xci(filepath)
                        for file in oflist:
                            sha,size,gamecard=f.file_hash(file)
                            if sha != False:
                                sec_hashlist.append(sha)
                                osizelist.append(size)
                                GClist.append([file,gamecard])
                        f.flush()
                        f.close()
                    except BaseException as e:
                        Utils.logError(e)
            # print(oflist)
            # print(osizelist)
            # print(sec_hashlist)
            if totSize <= 4294934528:
                fat="exfat"
            if fat=="fat32":
                splitnumb=math.ceil(totSize/4294934528)
                index=0
                endfile=endfile[:-1]+str(index)

            xci_header,game_info,sig_padding,xci_certificate,root_header,upd_header,norm_header,sec_header,rootSize,upd_multiplier,norm_multiplier,sec_multiplier=sq_tools.get_xciheader(oflist,osizelist,sec_hashlist)
            totSize=len(xci_header)+len(game_info)+len(sig_padding)+len(xci_certificate)+rootSize
            #print(hx(xci_header))
            #print(str(totSize))
            c=0
            if sys.platform == 'win32':
                v_drive, v_path = os.path.splitdrive(endfile)
            else:
                v_drive = os.path.dirname(os.path.abspath(endfile))
            dsktotal, dskused, dskfree=disk_usage(str(v_drive))
            if int(dskfree)<int(totSize):
                sys.exit("Warning disk space lower than required size. Program will exit")					
            t = tqdm(total=totSize, unit='B', unit_scale=True, leave=False)
            t.write(tabs+'- Writing XCI header...')
            outf = open(endfile, 'w+b')
            outf.write(xci_header)
            t.update(len(xci_header))
            c=c+len(xci_header)
            t.write(tabs+'- Writing XCI game info...')
            outf.write(game_info)
            t.update(len(game_info))
            c=c+len(game_info)
            t.write(tabs+'- Generating padding...')
            outf.write(sig_padding)
            t.update(len(sig_padding))
            c=c+len(sig_padding)
            t.write(tabs+'- Writing XCI certificate...')
            outf.write(xci_certificate)
            t.update(len(xci_certificate))
            c=c+len(xci_certificate)
            t.write(tabs+'- Writing ROOT HFS0 header...')
            outf.write(root_header)
            t.update(len(root_header))
            c=c+len(root_header)
            t.write(tabs+'- Writing UPDATE partition header...')
            t.write(tabs+'  Calculated multiplier: '+str(upd_multiplier))
            outf.write(upd_header)
            t.update(len(upd_header))
            c=c+len(upd_header)
            t.write(tabs+'- Writing NORMAL partition header...')
            t.write(tabs+'  Calculated multiplier: '+str(norm_multiplier))
            outf.write(norm_header)
            t.update(len(norm_header))
            c=c+len(norm_header)
            t.write(tabs+'- Writing SECURE partition header...')
            t.write(tabs+'  Calculated multiplier: '+str(sec_multiplier))
            outf.write(sec_header)
            t.update(len(sec_header))
            c=c+len(sec_header)
            outf.close()

            for filepath in filelist:
                if filepath.endswith('.nsp') or filepath.endswith('.nsz'):
                    try:
                        GC=False
                        f = Fs.Nsp(filepath)
                        for file in oflist:
                            if not file.endswith('xml'):
                                for i in range(len(GClist)):
                                    if GClist[i][0] == file:
                                        GC=GClist[i][1]
                                endfile,index,c = f.append_clean_content(endfile,file,buffer,t,GC,vkeypatch,metapatch,RSV_cap,fat,fx,c,index,block=4294934528)
                        f.flush()
                        f.close()
                    except BaseException as e:
                        Utils.logError(e)
                if filepath.endswith('.xci') or filepath.endswith('.xcz'):
                    try:
                        GC=False
                        f = Fs.Xci(filepath)
                        for file in oflist:
                            if not file.endswith('xml'):
                                for i in range(len(GClist)):
                                    if GClist[i][0] == file:
                                        GC=GClist[i][1]
                                endfile,index,c = f.append_clean_content(endfile,file,buffer,t,GC,vkeypatch,metapatch,RSV_cap,fat,fx,c,index,block=4294934528)
                        f.flush()
                        f.close()
                    except BaseException as e:
                        Utils.logError(e)
            t.close()
        if 'cnsp' in export:
            oflist=list()
            osizelist=list()
            ototlist=list()
            totSize=0
            c=0
            for i in range(len(prlist)):
                for j in prlist[i][4]:
                    el=j[0]
                    if el.endswith('.nca') or el.endswith('.xml'):
                        oflist.append(j[0])
                        #print(j[0])
                        osizelist.append(j[1])
                        totSize = totSize+j[1]
                        #print(j[1])
                    ototlist.append(j[0])
            nspheader=sq_tools.gen_nsp_header(oflist,osizelist)
            endname_x=endname+'[rr].nsp'
            print('Filename: '+endname_x)
            endfile = os.path.join(ofolder, endname_x)
            #print(endfile)
            #print(hx(nspheader))
            totSize = len(nspheader) + totSize
            if totSize <= 4294901760:
                fat="exfat"
            if fat=="fat32":
                splitnumb=math.ceil(totSize/4294901760)
                index=0
                endfile=endfile[:-1]+str(index)
            if fx=="folder" and fat=="fat32":
                output_folder = os.path.join(ofolder, "archfolder")
                endfile = os.path.join(output_folder, "00")
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
            elif fx=="folder" and fat=="exfat":
                ext='.xml'
                if os.path.exists(afolder) and os.path.isdir(afolder):
                    for dirpath, dirnames, filenames in os.walk(afolder):
                        for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
                            filename= os.path.join(afolder,filename)
                            shutil.move(filename,ofolder)
                shutil.rmtree(afolder, ignore_errors=True)
            #print(str(totSize))
            if sys.platform == 'win32':
                v_drive, v_path = os.path.splitdrive(endfile)
            else:
                v_drive = os.path.dirname(os.path.abspath(endfile))
            dsktotal, dskused, dskfree=disk_usage(str(v_drive))	
            if int(dskfree)<int(totSize):
                sys.exit("Warning disk space lower than required size. Program will exit")					
            t = tqdm(total=totSize, unit='B', unit_scale=True, leave=False)
            outf = open(endfile, 'w+b')
            t.write(tabs+'- Writing NSP header...')
            outf.write(nspheader)
            t.update(len(nspheader))
            c=c+len(nspheader)
            outf.close()
            for filepath in filelist:
                if filepath.endswith('.nsp') or filepath.endswith('.nsz'):
                    try:
                        f = Fs.Nsp(filepath)
                        for file in oflist:
                            if not file.endswith('xml'):
                                endfile,index,c = f.append_clean_content(endfile,file,buffer,t,False,vkeypatch,metapatch,RSV_cap,fat,fx,c,index)
                        f.flush()
                        f.close()
                    except BaseException as e:
                        Utils.logError(e)
                if filepath.endswith('.xci') or filepath.endswith('.xcz'):
                    try:
                        f = Fs.Xci(filepath)
                        for file in oflist:
                            if not file.endswith('xml'):
                                endfile,index,c = f.append_clean_content(endfile,file,buffer,t,False,vkeypatch,metapatch,RSV_cap,fat,fx,c,index)
                        f.flush()
                        f.close()
                    except BaseException as e:
                        Utils.logError(e)
            t.close()
# Direct Splitter
def cmd_direct_splitter(args):
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536

    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filepath in args.direct_splitter:
            dir=os.path.dirname(os.path.abspath(filepath))
            ofolder = os.path.join(dir, 'output')
    if args.fat:
        for input in args.fat:
            try:
                if input == "fat32":
                    fat="fat32"
                else:
                    fat="exfat"
            except BaseException as e:
                Utils.logError(e)
    else:
        fat="exfat"
    if args.fexport:
        for input in args.fexport:
            try:
                if input == "files":
                    fx="files"
                else:
                    fx="folder"
            except BaseException as e:
                Utils.logError(e)
    else:
        fx="files"

    if args.direct_splitter:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filepath = filelist.readline()
                filepath=os.path.abspath(filepath.rstrip('\n'))
        else:
            for filepath in args.direct_splitter:
                filepath=filepath
        try:
            if str(args.nodecompress).lower() == "true":
                nodecompress=True
            else:
                nodecompress=False
        except:
            nodecompress=False
        if nodecompress==True:
            fat="exfat"
        if args.type:
            for input in args.type:
                if input == "xci" or input == "XCI":
                    export='xci'
                elif input == "nsp" or input == "NSP":
                    export='nsp'
                elif input == "both" or input == "BOTH":
                    export='both'
                else:
                    print ("Wrong Type!!!")
        else:
            if filepath.endswith('.nsp') or filepath.endswith('.nsz'):
                export='nsp'
            elif filepath.endswith('.xci') or filepath.endswith('.xcz'):
                export='xci'
            else:
                print ("Wrong Type!!!")
        if args.rename:
            for newname in args.rename:
                newname=newname+'.xxx'
                endfile = os.path.join(ofolder, newname)
        else:
            endfile=os.path.basename(os.path.abspath(filepath))
        if args.cskip=='False':
            cskip=False
        else:
            cskip=True

        if filepath.endswith(".nsp") or filepath.endswith('.nsz'):
            try:
                f = Fs.Nsp(filepath)
                f.sp_groupncabyid(buffer,ofolder,fat,fx,export,nodecompress)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        if filepath.endswith(".xci") or filepath.endswith('.xcz'):
            try:
                f = Fs.Xci(filepath)
                f.sp_groupncabyid(buffer,ofolder,fat,fx,export,nodecompress)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
# Archive to nsp
def cmd_archive(args):
    if sys.platform == 'win32':
        if args.archive and args.ifolder:
            indent = 1
            tabs = '\t' * indent
            if args.text_file:
                tfile=args.text_file
                with open(tfile,"r+", encoding='utf8') as tname:
                    name = tname.readline()
                    name=name+'.nsp'
                endfolder=args.archive
                endfolder = os.path.join(endfolder, name)
            else:
                endfolder=args.archive
            try:
                ruta = args.ifolder
                if not os.path.exists(endfolder):
                    os.makedirs(endfolder)
                #print (ruta)
                #print (os.path.isdir(ruta))
                print (tabs+"Archiving to output folder...")
                if os.path.isdir(ruta) == True:
                    for dirpath, dnames, fnames in os.walk(ruta):
                        #print (fnames)
                        for f in fnames:
                            filepath = os.path.join(ruta, f)
                            #print (f)
                            #win32api.SetFileAttributes(filepath,win32con.FILE_ATTRIBUTE_NORMAL)
                            shutil.move(filepath,endfolder)
                win32api.SetFileAttributes(endfolder,win32con.FILE_ATTRIBUTE_ARCHIVE)
            except BaseException as e:
                Utils.logError(e)
# Join split files
def cmd_joinfile(args):
    indent = 1
    tabs = '\t' * indent
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        filepath = args.joinfile
        dir=os.path.dirname(os.path.abspath(filepath))
        ofolder = os.path.join(dir, 'output')
    if not os.path.exists(ofolder):
        os.makedirs(ofolder)
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.text_file:
        tfile=args.text_file
        with open(tfile,"r+", encoding='utf8') as filelist:
            filepath = filelist.readline()
            filepath=os.path.abspath(filepath.rstrip('\n'))
    else:
        for filepath in args.joinfile:
            filepath=filepath
    print(filepath)
    file_list=list()
    try:
        bname=os.path.basename(os.path.abspath(filepath))
        bn=''
        if bname != '00':
            bn=bname[:-4]
        if filepath.endswith(".xc0"):
            outname = bn+".xci"
            ender=".xc"
        elif filepath.endswith(".ns0"):
            outname = bn+".nsp"
            ender=".ns"
        elif filepath[-2:]=="00":
            outname = "output.nsp"
            ender="0"
        else:
            print ("Not valid file")
        outfile = os.path.join(ofolder, outname)
        #print (outfile)
        ruta=os.path.dirname(os.path.abspath(filepath))
        #print(ruta)
        for dirpath, dnames, fnames in os.walk(ruta):
            for f in fnames:
                check=f[-4:-1]
                #print(check)
                #print(ender)
                #print(bname[:-1])
                #print(f[:-1])
                if check==ender and bname[:-1]==f[:-1]:
                    n=bname[-1];n=int(n)
                    try:
                        n=f[-1];n=int(n)
                        n+=1
                        fp = os.path.join(ruta, f)
                        file_list.append(fp)
                    except:	continue
        file_list.sort()
        #print(file_list)
    except BaseException as e:
        Utils.logError(e)
    totSize = sum(os.path.getsize(file) for file in file_list)
    if sys.platform == 'win32':
        v_drive, v_path = os.path.splitdrive(outfile)
    else:
        v_drive = os.path.dirname(os.path.abspath(outfile))
    dsktotal, dskused, dskfree=disk_usage(str(v_drive))
    if int(dskfree)<int(totSize):
        sys.exit("Warning disk space lower than required size. Program will exit")				
    t = tqdm(total=totSize, unit='B', unit_scale=True, leave=False)
    t.write(tabs+'- Joining files...')
    index=0
    outf = open(outfile, 'wb')
    #print(file_list)
    for file in file_list:
        t.write(tabs+'- Appending: '+ file)
        outfile=file[:-1]+str(index)
        with open(outfile, 'rb') as inf:
            while True:
                data = inf.read(int(buffer))
                outf.write(data)
                t.update(len(data))
                outf.flush()
                if not data:
                    break
        index+=1
    t.close()
    outf.close()
# ZIP
def cmd_zip(args):
    if args.zippy and args.ifolder:
        indent = 1
        tabs = '\t' * indent
        try:
            outfile=args.zippy
            ruta = args.ifolder
            endfolder=os.path.dirname(os.path.abspath(outfile))
            if not os.path.exists(endfolder):
                os.makedirs(endfolder)
            print (tabs+"Packing zip...")
            if os.path.isdir(ruta) == True:
                for dirpath, dnames, fnames in os.walk(ruta):
                    for f in fnames:
                        filepath = os.path.join(ruta, f)
                        with ZipFile(outfile, 'a') as zippy:
                            fp = os.path.join(ruta, f)
                            zippy.write(fp,f)
        except BaseException as e:
            Utils.logError(e)

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Fs
import Utils
import Status
import Print

# NCA/NSP IDENTIFICATION
def handleCmd(args):
    # Get titleid from nca file
    if args.ncatitleid:
        cmd_ncatitleid(args)
	# Get type from nca file
    if args.ncatype:
        cmd_ncatype(args)
    if args.nsptitleid:
        cmd_nsptitleid(args)
    # Read version number from nsp or xci
    if args.ReadversionID:
        cmd_ReadversionID(args)
# Identify type of nsp
def cmd_nsptype(args):
    for filename in args.nsptype:
        try:
            f = Fs.Nsp(filename, 'rb')
            TYPE=f.nsptype()
            print(TYPE)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Identify if nsp has titlerights
def cmd_nsp_htrights(args):
    for filename in args.nsp_htrights:
        try:
            f = Fs.Nsp(filename, 'rb')
            if f.trights_set() == 'TRUE':
                Print.info('TRUE')
            if f.trights_set() == 'FALSE':
                Print.info('FALSE')
        except BaseException as e:
            Utils.logError(e)
# Identify if nsp has ticket
def cmd_nsp_hticket(args):
    for filename in args.nsp_hticket:
        try:
            f = Fs.Nsp(filename, 'rb')
            if f.exist_ticket() == 'TRUE':
                Print.info('TRUE')
            if f.exist_ticket() == 'FALSE':
                Print.info('FALSE')
        except BaseException as e:
            Utils.logError(e)
# Identify if nsp has ticket
def cmd_nsp_hticket(args):
    for filename in args.nsp_hticket:
        try:
            f = Fs.Nsp(filename, 'rb')
            if f.exist_ticket() == 'TRUE':
                Print.info('TRUE')
            if f.exist_ticket() == 'FALSE':
                Print.info('FALSE')
        except BaseException as e:
            Utils.logError(e)
# REMOVE TITLERIGHTS FUNCTIONS
# Remove titlerights from input NSP
def cmd_remove_title_rights(args):
    for filename in args.remove_title_rights:
        try:
            f = Fs.Nsp(filename, 'r+b')
            f.removeTitleRights()
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Change Master keys
def cmd_set_masterkey(args):
    file=args.set_masterkey[0]
    if args.set_masterkey[1]:
        try:
            mkey=int(args.set_masterkey[1])
            if mkey==1:
                mkey=0
            f = Fs.Nsp(file, 'r+b')
            f.setMasterKeyRev(mkey)
            f.flush()
            f.close()
            pass
        except:
            print("Invalid masterkey number")					
    else:
        print("Missing masterkey number")
# Remove titlerights from an NSP using information from original NSP
def cmd_RTRNCA_h_nsp(args):
    for filename in args.external:
        try:
            f = Fs.Nsp(filename, 'r+b')
            masterKeyRev=f.nspmasterkey()
            titleKeyDec=f.nsptitlekeydec()
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    for filename in args.RTRNCA_h_nsp:
        try:
            f = Fs.Nca(filename, 'r+b')
            f.removeTitleRightsnca(masterKeyRev,titleKeyDec)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Remove titlerights from an NCA using information from an extracted TICKET
def cmd_RTRNCA_h_tick(args):
    for filename in args.external:
        try:
            f = Fs.Ticket(filename, 'r+b')
            f.open(filename, 'r+b')
            masterKeyRev=f.getMasterKeyRevision()
            titleKeyDec=f.get_titlekeydec()
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    for filename in args.RTRNCA_h_tick:
        try:
            f = Fs.Nca(filename, 'r+b')
            f.removeTitleRightsnca(masterKeyRev,titleKeyDec)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# GAMECARD FLAG FUNCTIONS
# Set isgamecard flag from all nca in an NSP as ESHOP
def cmd_seteshop(args):
    for filename in args.seteshop:
        try:
            f = Fs.Nsp(filename, 'r+b')
            f.seteshop()
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Set isgamecard flag from all nca in an NSP as CARD
def cmd_setcgame(args):
    for filename in args.setcgame:
        try:
            f = Fs.Nsp(filename, 'r+b')
            f.setcgame()
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Set isgamecard flag for one nca as ESHOP
def cmd_seteshop_nca(args):
    for filename in args.seteshop_nca:
        try:
            f = Fs.Nca(filename, 'r+b')
            f.header.setgamecard(0)
            Print.info('IsGameCard flag is now set as: ' + str(f.header.getgamecard()))
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Set isgamecard flag for one nca as CARD
def cmd_setcgame_nca(args):
    for filename in args.setcgame_nca:
        try:
            f = Fs.Nca(filename, 'r+b')
            f.header.setgamecard(1)
            Print.info('IsGameCard flag is now set as: ' + str(f.header.getgamecard()))
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    # ...................................................
    # Get isgamecard flag from a NCA file
    # ...................................................
    if args.cardstate:
        for filename in args.cardstate:
            try:
                f = Fs.Nca(filename, 'rb')
                f.cardstate()
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        Status.close()
    # ...................................................
    # Set value for network account
    # ...................................................
    if args.remlinkacc:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filename = filelist.readline()
                filename=os.path.abspath(filename.rstrip('\n'))
        else:
            for inpt in args.remlinkacc:
                filename=inpt
        try:
            if filename.endswith('.nsp') or filename.endswith('.nsx') or filename.endswith('.nsz'):
                f = Fs.Nsp(filename,'r+b')
                ctrl_list=f.gen_ctrl_list()
                f.flush()
                f.close()
                for item in ctrl_list:
                    print('-------------------------------------------------')
                    print('Processing: '+str(item))
                    print('-------------------------------------------------')
                    f = Fs.Nsp(filename,'r+b')
                    check=f.patch_netlicense()
                    f.flush()
                    f.close()
                    if check == True:
                        f = Fs.Nsp(filename, 'r+b')
                        leveldata,superhashoffset=f.reb_lv_hashes(item)
                        f.flush()
                        f.close()
                        n=len(leveldata)-1
                        for i in range(len(leveldata)):
                            j=n-i
                            if j==0:
                                break
                            f = Fs.Nsp(filename, 'r+b')
                            superhash=f.set_lv_hash(j,leveldata,item)
                            f.flush()
                            f.close()
                        f = Fs.Nsp(filename, 'r+b')
                        f.set_lvsuperhash(leveldata,superhashoffset,item)
                        f.flush()
                        f.close()
                        f = Fs.Nsp(filename, 'r+b')
                        f.ctrl_upd_hblock_hash(item)
                        f.flush()
                        f.close()
            elif filename.endswith('.xci') or filename.endswith('.xcz'):
                f = Fs.factory(filename)
                f.open(filename, 'r+b')
                ctrl_list=f.gen_ctrl_list()
                f.flush()
                f.close()
                for item in ctrl_list:
                    print('-------------------------------')
                    print('Processing: '+str(item))
                    print('-------------------------------')
                    f = Fs.factory(filename)
                    f.open(filename, 'r+b')
                    check=f.patch_netlicense(item)
                    f.flush()
                    f.close()
                    if check == True:
                        f = Fs.factory(filename)
                        f.open(filename, 'r+b')
                        leveldata,superhashoffset=f.reb_lv_hashes(item)
                        f.flush()
                        f.close()
                        n=len(leveldata)-1
                        for i in range(len(leveldata)):
                            j=n-i
                            if j==0:
                                break
                            f = Fs.factory(filename)
                            f.open(filename, 'r+b')
                            superhash=f.set_lv_hash(j,leveldata,item)
                            f.flush()
                            f.close()
                        f = Fs.factory(filename)
                        f.open(filename, 'r+b')
                        f.set_lvsuperhash(leveldata,superhashoffset,item)
                        f.flush()
                        f.close()
                        f = Fs.factory(filename)
                        f.open(filename, 'r+b')
                        f.ctrl_upd_hblock_hash(item)
                        f.flush()
                        f.close()
        except BaseException as e:
            Utils.logError(e)
        Status.close()            

def cmd_ncatype(args):
    for filename in args.ncatype:
        try:
            f = Fs.Nca(filename, 'rb')
            f.print_nca_type()
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)

def cmd_nsptitleid(args):
    for fileName in args.nsptitleid:
        try:
            f = Fs.Nsp(fileName, 'r+b')
            titleid=f.getnspid()
            Print.info(titleid)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)

def cmd_ReadversionID(args):
    for filename in args.ReadversionID:
        if filename.endswith('.nsp'):
            try:
                f = Fs.Nsp(filename, 'rb')
                f.get_cnmt_verID()
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        if filename.endswith('.xci'):
            try:
                f = Fs.factory(filename)
                f.open(filename, 'rb')
                f.get_cnmt_verID()
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)

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
    Status.close()

def cmd_extract(args):
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
        for filename in args.extract:
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
            f = Fs.Nsp(filename, 'rb')
            f.open(filename, 'rb')
            f.extract_all(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    elif test.endswith('.xci') or test.endswith('.xcz'):
        try:
            f = Fs.factory(filename)
            f.open(filename, 'rb')
            f.extract_all(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    Status.close()    	

def cmd_ncatitleid(args):
    for filename in args.ncatitleid:
        try:
            f = Fs.Nca(filename, 'rb')
            f.printtitleId()
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
           
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
    Status.close()

def cmd_extract(args):
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
        for filename in args.extract:
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
            f = Fs.Nsp(filename, 'rb')
            f.open(filename, 'rb')
            f.extract_all(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    elif test.endswith('.xci') or test.endswith('.xcz'):
        try:
            f = Fs.factory(filename)
            f.open(filename, 'rb')
            f.extract_all(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
    Status.close()    
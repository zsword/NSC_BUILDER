#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Fs
import Utils
import Status
import Print

# NCA/NSP IDENTIFICATION
# Get titleid from nca file
def cmd_ncatitleid(args):
    for filename in args.ncatitleid:
        try:
            f = Fs.Nca(filename, 'rb')
            f.printtitleId()
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Get type from nca file                
def cmd_ncatype(args):
    for filename in args.ncatype:
        try:
            f = Fs.Nca(filename, 'rb')
            f.print_nca_type()
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Get titleid from nsp file
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
# Read version number from nsp or xci
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
    # Set value for network account
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

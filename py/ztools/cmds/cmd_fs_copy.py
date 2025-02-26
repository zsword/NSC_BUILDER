#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import Fs
import Utils

# COPY FUNCTIONS
# Copy TICKET from NSP file
def cmd_NSP_copy_ticket(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_ticket:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')
    for filename in args.NSP_copy_ticket:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_ticket(ofolder)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy all FILES from NSP\XCI file
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
# Copy all NCA from NSP file
def cmd_NSP_copy_nca(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_nca:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
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
    for filename in args.NSP_copy_nca:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_nca(ofolder,buffer,metapatch,vkeypatch,int(RSV_cap))
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy all hfs0 partitions (update, normal,secure,logo) from XCI file
def cmd_XCI_copy_hfs0(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.XCI_copy_hfs0:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filePath in args.XCI_copy_hfs0:
        f = Fs.factory(filePath)
        f.open(filePath, 'rb')
        f.copy_hfs0(ofolder,buffer,"all")
        f.close()
# Copy update partition from XCI file as hfs0
def cmd_XCI_c_hfs0_update(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.XCI_c_hfs0_update:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filePath in args.XCI_c_hfs0_update:
        f = Fs.factory(filePath)
        f.open(filePath, 'rb')
        f.copy_hfs0(ofolder,buffer,"update")
        f.close()
# Copy normal partition from XCI file as hfs0
def cmd_XCI_c_hfs0_normal(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.XCI_c_hfs0_normal:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filePath in args.XCI_c_hfs0_normal:
        f = Fs.factory(filePath)
        f.open(filePath, 'rb')
        f.copy_hfs0(ofolder,buffer,"normal")
        f.close()
# Copy secure partition from XCI file as hfs0
def cmd_XCI_c_hfs0_secure(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.XCI_c_hfs0_secure:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filePath in args.XCI_c_hfs0_secure:
        f = Fs.factory(filePath)
        f.open(filePath, 'rb')
        f.copy_hfs0(ofolder,buffer,'secure')
        f.close()
# Copy nca from secure partition from XCI
def cmd_XCI_copy_nca_secure(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.XCI_copy_nca_secure:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.patchversion:
        for input in args.patchversion:
            try:
                metapatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        metapatch = 'false'
    if args.keypatch:
        for input in args.keypatch:
            try:
                vkeypatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        vkeypatch = 'false'
    if args.RSVcap:
        for input in args.RSVcap:
            try:
                RSV_cap = input
            except BaseException as e:
                Utils.logError(e)
    else:
        RSV_cap = 268435656
    for filePath in args.XCI_copy_nca_secure:
        f = Fs.Xci(filePath)
        f.open(filePath, 'rb')
        f.copy_nca(ofolder,buffer,'secure',metapatch,vkeypatch,int(RSV_cap))
        f.close()
# Copy nca from secure partition from XCI
def cmd_XCI_copy_nca_normal(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.C_clean:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.patchversion:
        for input in args.patchversion:
            try:
                metapatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        metapatch = 'false'
    if args.keypatch:
        for input in args.keypatch:
            try:
                vkeypatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        vkeypatch = 'false'
    if args.RSVcap:
        for input in args.RSVcap:
            try:
                RSV_cap = input
            except BaseException as e:
                Utils.logError(e)
    else:
        RSV_cap = 268435656
    for filePath in args.XCI_copy_nca_normal:
        f = Fs.nXci(filePath)
        f.open(filePath, 'rb')
        f.copy_nca(ofolder,buffer,'normal',metapatch,vkeypatch,int(RSV_cap))
        f.close()
# Copy nca from secure partition from XCI
def cmd_XCI_copy_nca_update(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.C_clean:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.patchversion:
        for input in args.patchversion:
            try:
                metapatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        metapatch = 'false'
    if args.keypatch:
        for input in args.keypatch:
            try:
                vkeypatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        vkeypatch = 'false'
    if args.RSVcap:
        for input in args.RSVcap:
            try:
                RSV_cap = input
            except BaseException as e:
                Utils.logError(e)
    else:
        RSV_cap = 268435656
    for filePath in args.XCI_copy_nca_update:
        f = Fs.uXci(filePath)
        f.open(filePath, 'rb')
        f.copy_nca(ofolder,buffer,'update',metapatch,vkeypatch,int(RSV_cap))
        f.close()
# Copy root.hfs0 from XCI
def cmd_XCI_copy_rhfs0(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.XCI_copy_rhfs0:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filePath in args.XCI_copy_rhfs0:
        f = Fs.factory(filePath)
        f.open(filePath, 'rb')
        f.copy_root_hfs0(ofolder,buffer)
        f.close()
# Copy OTHER KIND OF FILES from NSP file
def cmd_NSP_copy_other(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_other:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.NSP_copy_other:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_other(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy XML from NSP file
def cmd_NSP_copy_xml(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_xml:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.NSP_copy_xml:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_xml(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy CERT from NSP file
def cmd_NSP_copy_cert(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_cert:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.NSP_copy_cert:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_nsp_cert(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy JPG from NSP file
def cmd_NSP_copy_jpg(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_jpg:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.NSP_copy_jpg:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_jpg(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy meta cnmt files from NSP file
def cmd_NSP_copy_cnmt(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_cnmt:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.NSP_copy_cnmt:
        if filename.endswith('.nsp') or filename.endswith('.nsz') or filename.endswith('.nsx'):
            try:
                f = Fs.Nsp(filename, 'rb')
                f.copy_cnmt(ofolder,buffer)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        if filename.endswith('.xci') or  filename.endswith('.xcz'):
            try:
                f = Fs.factory(filename)
                f.open(filename, 'rb')
                f.copy_cnmt(ofolder,buffer)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)						
        if filename.endswith('.cnmt.nca'):
            try:
                f = Fs.Nca(filename)
                f.open(filename, 'rb')						
                data=f.return_cnmt()
                f.flush()	
                f.close()	
                f = Fs.Nca(filename)
                f.open(filename, 'rb')
                filenames=f.ret_cnmt_name()
                f.flush()	
                f.close()	
                try:	
                    basename=str(filenames[0])
                except:
                    basename=(str(os.path.basename(os.path.abspath(filename))))[:-4]
                ofile =os.path.join(ofolder,basename)
                with open (ofile,'wb') as o:
                    o.write(data)
            except BaseException as e:
                Utils.logError(e)
# Copy pfs0 from NSP file
def cmd_copy_pfs0_meta(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.copy_pfs0_meta:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.copy_pfs0_meta:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_pfs0_meta(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy control nacp files from NSP file
def cmd_copy_nacp(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.copy_nacp:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.copy_nacp:
        if filename.endswith(".nsp"):
            try:
                f = Fs.Nsp(filename, 'rb')
                f.copy_nacp(ofolder,buffer)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        '''
        if filename.endswith(".nca"):
            try:
                f = Fs.Nca(filename, 'rb')
                f.extract(ofolder,buffer)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        '''
# DEDICATED COPY FUNCTIONS. NCA TYPES.
# Copy all META NCA from NSP file
def cmd_NSP_copy_nca_meta(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_nca_meta:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.NSP_copy_nca_meta:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_nca_meta(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy all CONTROL NCA from NSP file
def cmd_NSP_copy_nca_control(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_nca_control:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.NSP_copy_nca_control:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_nca_control(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy all MANUAL NCA from NSP file
def cmd_NSP_copy_nca_manual(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_nca_manual:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.NSP_copy_nca_manual:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_nca_manual(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy all PROGRAM NCA from NSP file
def cmd_NSP_copy_nca_program(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_nca_program:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    for filename in args.NSP_copy_nca_program:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_nca_program(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy all DATA NCA from NSP file
def cmd_NSP_copy_nca_data(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_nca_data:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536

    for filename in args.NSP_copy_nca_data:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_nca_data(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy all PUBLIC DATA NCA from NSP file
def cmd_NSP_copy_nca_pdata(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_nca_pdata:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536

    for filename in args.NSP_copy_nca_pdata:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_nca_pdata(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# DEDICATED COPY FUNCTIONS. TITLERIGHTS.
# Copy all NCA WITH TITLERIGHTS from target NSP
def cmd_NSP_copy_tr_nca(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_tr_nca:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536

    for filename in args.NSP_copy_tr_nca:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_tr_nca(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy all NCA WITHOUT TITLERIGHTS from target NSP
def cmd_NSP_copy_ntr_nca(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_copy_ntr_nca:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536

    for filename in args.NSP_copy_ntr_nca:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_ntr_nca(ofolder,buffer)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Copy ALL NCA AND CLEAN TITLERIGHTS
def cmd_C_clean(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filename = filelist.readline()
                filename=os.path.abspath(filename.rstrip('\n'))
                dir=os.path.dirname(os.path.abspath(filename))
                ofolder =os.path.join(dir, 'output')
        else:
            for filename in args.C_clean:
                dir=os.path.dirname(os.path.abspath(filename))
                ofolder =os.path.join(dir, 'output')

    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.patchversion:
        for input in args.patchversion:
            try:
                metapatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        metapatch = 'true'
    if args.keypatch:
        for input in args.keypatch:
            try:
                vkeypatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        vkeypatch = 'false'
    if args.RSVcap:
        for input in args.RSVcap:
            try:
                RSV_cap = input
            except BaseException as e:
                Utils.logError(e)
    else:
        RSV_cap = 268435656
    if args.C_clean:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filename = filelist.readline()
                filename=os.path.abspath(filename.rstrip('\n'))
        else:
            for filename in args.C_clean:
                filename=filename
        if filename.endswith('.nsp'):
            try:
                f = Fs.Nsp(filename, 'rb')
                if f.trights_set() == 'FALSE':
                    Print.info("NSP DOESN'T HAVE TITLERIGHTS")
                    f.copy_nca(ofolder,buffer,metapatch,vkeypatch,int(RSV_cap))
                if f.trights_set() == 'TRUE':
                    if f.exist_ticket() == 'TRUE':
                        Print.info("NSP HAS TITLERIGHTS AND TICKET EXISTS")
                        f.cr_tr_nca(ofolder,buffer,metapatch,vkeypatch,int(RSV_cap))
                    if f.exist_ticket() == 'FALSE':
                        Print.error('NSP FILE HAS TITLERIGHTS BUT NO TICKET')
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        if filename.endswith('.xci'):
            try:
                f = Fs.factory(filename)
                f.open(filename, 'rb')
                if f.trights_set() == 'FALSE':
                    Print.info("XCI DOESN'T HAVE TITLERIGHTS")
                    f.copy_nca(ofolder,buffer,'secure',metapatch,vkeypatch,int(RSV_cap))
                if f.trights_set() == 'TRUE':
                    if f.exist_ticket() == 'TRUE':
                        Print.info("XCI HAS TITLERIGHTS AND TICKET EXISTS")
                        f.cr_tr_nca(ofolder,buffer,metapatch,vkeypatch,int(RSV_cap))
                    if f.exist_ticket() == 'FALSE':
                        Print.error('XCI FILE HAS TITLERIGHTS BUT NO TICKET')
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
# Copy ALL NCA AND CLEAN TITLERIGHTS WITHOUT DELTAS
def cmd_C_clean_ND(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filename = filelist.readline()
                filename=os.path.abspath(filename.rstrip('\n'))
                dir=os.path.dirname(os.path.abspath(filename))
                ofolder =os.path.join(dir, 'output')
        else:
            for filename in args.C_clean_ND:
                dir=os.path.dirname(os.path.abspath(filename))
                ofolder =os.path.join(dir, 'output')
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.patchversion:
        for input in args.patchversion:
            try:
                metapatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        metapatch = 'false'
    if args.keypatch:
        for input in args.keypatch:
            try:
                vkeypatch = input
            except BaseException as e:
                Utils.logError(e)
    else:
        vkeypatch = 'false'
    if args.RSVcap:
        for input in args.RSVcap:
            try:
                RSV_cap = input
            except BaseException as e:
                Utils.logError(e)
    else:
        RSV_cap = 268435656

    if args.C_clean_ND:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filename = filelist.readline()
                filename=os.path.abspath(filename.rstrip('\n'))
        else:
            for filename in args.C_clean_ND:
                filename=filename
        if filename.endswith('.nsp'):
            try:
                f = Fs.Nsp(filename, 'rb')
                if f.trights_set() == 'FALSE':
                    Print.info("NSP DOESN'T HAVE TITLERIGHTS")
                    f.copy_nca_nd(ofolder,buffer,metapatch,vkeypatch,int(RSV_cap))
                if f.trights_set() == 'TRUE':
                    if f.exist_ticket() == 'TRUE':
                        Print.info("NSP HAS TITLERIGHTS AND TICKET EXISTS")
                        f.cr_tr_nca_nd(ofolder,buffer,metapatch,vkeypatch,int(RSV_cap))
                    if f.exist_ticket() == 'FALSE':
                        Print.error('NSP FILE HAS TITLERIGHTS BUT NO TICKET')
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        if filename.endswith('.xci'):
            try:
                f = Fs.factory(filename)
                f.open(filename, 'rb')
                if f.trights_set() == 'FALSE':
                    Print.info("XCI DOESN'T HAVE TITLERIGHTS")
                    f.copy_nca_nd(ofolder,buffer,metapatch,vkeypatch,int(RSV_cap))
                if f.trights_set() == 'TRUE':
                    if f.exist_ticket() == 'TRUE':
                        Print.info("XCI HAS TITLERIGHTS AND TICKET EXISTS")
                        f.cr_tr_nca_nd(ofolder,buffer,metapatch,vkeypatch,int(RSV_cap))
                    if f.exist_ticket() == 'FALSE':
                        Print.error('XCI FILE HAS TITLERIGHTS BUT NO TICKET')
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
# Copy keyblock from nca files with titlerights from a nsp
def cmd_NSP_c_KeyBlock(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.NSP_c_KeyBlock:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')
    for filename in args.NSP_c_KeyBlock:
        try:
            f = Fs.Nsp(filename, 'rb')
            f.copy_KeyBlock(ofolder)
            f.flush()
            f.close()
        except BaseException as e:
            Utils.logError(e)
# Identify if nsp has titlerights
#		def cmd_nsp_htrights(args):
#			for filename in args.nsp_htrights:
#				try:
#					f = Fs.Nsp(filename, 'r+b')
#					if f.trights_set() == 'TRUE':
#						Print.info('TRUE')
#					if f.trights_set() == 'FALSE':
#						Print.info('FALSE')
#				except BaseException as e:
#					Utils.logError(e)

# Identify if nsp has ticket
#		def cmd_nsp_hticket(args):
#			for filename in args.nsp_hticket:
#				try:
#					f = Fs.Nsp(filename, 'r+b')
#					if f.exist_ticket() == 'TRUE':
#						Print.info('TRUE')
#					if f.exist_ticket() == 'FALSE':
#						Print.info('FALSE')
#				except BaseException as e:
#					Utils.logError(e)



# DEDICATED COPY FUNCTIONS. SPLIT OR UPDATE.
# Split content by titleid according to cnmt files
def cmd_splitter(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filename = filelist.readline()
                filename=os.path.abspath(filename.rstrip('\n'))
                dir=os.path.dirname(os.path.abspath(filename))
                ofolder =os.path.join(dir, 'output')
        else:
            for filename in args.splitter:
                dir=os.path.dirname(os.path.abspath(filename))
                ofolder =os.path.join(dir, 'output')
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.pathend:
        for input in args.pathend:
            try:
                pathend = input
            except BaseException as e:
                Utils.logError(e)
    else:
        pathend = ''
    if args.splitter:
        if args.text_file:
            tfile=args.text_file
            with open(tfile,"r+", encoding='utf8') as filelist:
                filename = filelist.readline()
                filename=os.path.abspath(filename.rstrip('\n'))
        else:
            for filename in args.splitter:
                filename=filename
        if filename.endswith('.nsp'):
            try:
                f = Fs.Nsp(filename, 'rb')
                f.splitter_read(ofolder,buffer,pathend)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        if filename.endswith('.xci'):
            try:
                f = Fs.factory(filename)
                f.open(filename, 'rb')
                f.splitter_read(ofolder,buffer,pathend)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
# Prepare base content to get it updated
def cmd_updbase(args):
    if args.ofolder:
        for input in args.ofolder:
            try:
                ofolder = input
            except BaseException as e:
                Utils.logError(e)
    else:
        for filename in args.updbase:
            dir=os.path.dirname(os.path.abspath(filename))
            ofolder =os.path.join(dir, 'output')
    if args.buffer:
        for input in args.buffer:
            try:
                buffer = input
            except BaseException as e:
                Utils.logError(e)
    else:
        buffer = 65536
    if args.cskip:
        for input in args.cskip:
            try:
                cskip = input
            except BaseException as e:
                Utils.logError(e)
    else:
        pathend = 'false'
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

    for filename in args.updbase:
        if filename.endswith('.nsp'):
            try:
                f = Fs.Nsp(filename, 'rb')
                f.updbase_read(ofolder,buffer,cskip,metapatch,vkeypatch,RSV_cap)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
        if filename.endswith('.xci'):
            try:
                f = Fs.factory(filename)
                f.open(filename, 'rb')
                f.updbase_read(ofolder,buffer,cskip,metapatch,vkeypatch,RSV_cap)
                f.flush()
                f.close()
            except BaseException as e:
                Utils.logError(e)
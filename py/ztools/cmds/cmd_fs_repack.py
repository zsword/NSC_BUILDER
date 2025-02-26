#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import Utils

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
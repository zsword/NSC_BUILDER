# -*- coding: utf-8 -*-
# cython:language_level=3

r'''
   _____			 _				__
  / ___/____ ___  __(_)____________  / /
  \__ \/ __ `/ / / / / ___/ ___/ _ \/ /
 ___/ / /_/ / /_/ / / /  / /  /  __/ /
/____/\__, /\__,_/_/_/  /_/   \___/_/
		/_/

By julesontheroad:
https://github.com/julesontheroad/
Squirrel is a fork of NUT made to support NSC Builder
https://github.com/julesontheroad/NSC_BUILDER

The original NUT is made and actively supported by blawar
https://github.com/blawar/nut

This fork doesn't follow NUT's main line and strips many features from nut
(like CDNSP support) while adds several functions based in new code.
This program specialices in content building and file management for several
Nintendo Switch formats.

Squirrel original's purpose is to support NSC_Builder though it serves as a
standalone program with many functions, some of them not being used currently in NSC_Builder.
'''
import argparse
import sys
import os
import re
import io
import pathlib
import urllib3
import json
from zipfile import ZipFile

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, 'lib')
try:
	sys.path.insert(0, 'private')
except:pass	
import sq_settings
sq_settings.set_prod_environment()
import Keys
import Config
import Status
import CDNSP
import Utils

# SET ENVIRONMENT
squirrel_dir=os.path.abspath(os.curdir)
NSCB_dir=os.path.abspath('../'+(os.curdir))

if os.path.exists(os.path.join(squirrel_dir,'ztools')):
	NSCB_dir=squirrel_dir
	zconfig_dir=os.path.join(NSCB_dir, 'zconfig')
	ztools_dir=os.path.join(NSCB_dir,'ztools')
	squirrel_dir=ztools_dir
elif os.path.exists(os.path.join(NSCB_dir,'ztools')):
	squirrel_dir=squirrel_dir
	ztools_dir=os.path.join(NSCB_dir, 'ztools')
	zconfig_dir=os.path.join(NSCB_dir, 'zconfig')
else:
	ztools_dir=os.path.join(NSCB_dir, 'ztools')
	zconfig_dir=os.path.join(NSCB_dir, 'zconfig')

if os.path.exists(zconfig_dir):
	DATABASE_folder=os.path.join(zconfig_dir, 'DB')
else:
	DATABASE_folder=os.path.join(squirrel_dir, 'DB')

if not os.path.exists(DATABASE_folder):
	os.makedirs(DATABASE_folder)

if __name__ == '__main__':
	try:
		urllib3.disable_warnings()
		parser = argparse.ArgumentParser()
		parser.add_argument('file',nargs='*')

		# INFORMATION
		parser.add_argument('-i', '--info', help='show info about title or file')
		parser.add_argument('--filelist', nargs='+', help='Prints file list from NSP/XCI secure partition')
		parser.add_argument('--ADVfilelist', nargs='+', help='Prints ADVANCED file list from NSP/XCI secure partition')
		parser.add_argument('--ADVcontentlist', nargs='+', help='Prints ADVANCED content list from NSP/XCI arranged by base titleid')
		parser.add_argument('--Read_cnmt', nargs='+', help='Read cnmt file inside NSP/XCI')
		parser.add_argument('--Read_nacp', nargs='+', help='Read nacp file inside NSP/XCI')
		parser.add_argument('--Read_icon', nargs='+', help='Read icon files inside NSP/XCI')
		parser.add_argument('--Read_npdm', nargs='+', help='Read npdm file inside NSP/XCI')
		parser.add_argument('--Read_hfs0', nargs='+', help='Read hfs0')
		parser.add_argument('--fw_req', nargs='+', help='Get information about fw requirements for NSP/XCI')
		parser.add_argument('--Read_xci_head', nargs='+', help='Get information about xci header and cert')
		parser.add_argument('-nscdb', '--addtodb', nargs='+', help='Adds content to database')
		parser.add_argument('-nscdb_new', '--addtodb_new', nargs='+', help='Adds content to database')
		parser.add_argument('-v', '--verify', nargs='+', help='Verify nsp or xci file')
		parser.add_argument('-vk', '--verify_key', nargs='+', help='Verify a key against a preorder nsp\nsx')
		# CNMT Flag funtions
		parser.add_argument('--set_cnmt_titleid', nargs='+', help='Changes cnmt.nca titleid')
		parser.add_argument('--set_cnmt_version', nargs='+', help='Changes cnmt.nca version number')
		parser.add_argument('--set_cnmt_RSV', nargs='+', help='Changes cnmt.nca RSV')
		parser.add_argument('--update_hash', nargs='+', help='Updates cnmt.nca hashes')
		parser.add_argument('--xml_gen', nargs='+', help='Generates cnmt.xml')

		# REPACK
		parser.add_argument('-c', '--create', help='create / pack a NSP')
		parser.add_argument('-cpr', '--compress', nargs='+', help='Compress a nsp or xci')
		parser.add_argument('-dcpr', '--decompress', help='deCompress a nsz, xcz or ncz')
		parser.add_argument('--create_hfs0', help='create / pack a hfs0')
		parser.add_argument('--create_rhfs0', help='create / pack a root hfs0')
		parser.add_argument('--create_xci', help='create / pack a xci')
		parser.add_argument('-xci_st', '--xci_super_trim', nargs='+', help='Supertrim xci')
		parser.add_argument('-xci_tr', '--xci_trim', nargs='+', help='Trims xci')
		parser.add_argument('-xci_untr', '--xci_untrim', nargs='+', help='Untrims xci')
		parser.add_argument('-dc', '--direct_creation', nargs='+', help='Create directly a nsp or xci')
		parser.add_argument('-dmul', '--direct_multi', nargs='+', help='Create directly a multi nsp or xci')
		parser.add_argument('-ed', '--erase_deltas', nargs='+', help='Take of deltas from updates')
		parser.add_argument('-rbnsp', '--rebuild_nsp', nargs='+', help='Rebuild nsp by cnmt order')
		parser.add_argument('-rst', '--restore', nargs='+', help='Restore a xci or nsp file')

		# nca/nsp identification
		parser.add_argument('--ncatitleid', nargs='+', help='Returns titleid from an nca input')
		parser.add_argument('--ncatype', nargs='+', help='Returns type of an nca file')
		parser.add_argument('--nsptitleid', nargs='+', help='Returns titleid for a nsp file')
		parser.add_argument('--nsptype', nargs='+', help='Returns type for a nsp file')
		parser.add_argument('--ReadversionID', nargs='+', help='Returns version number for nsp Oorxci')
		parser.add_argument('--nsp_htrights', nargs='+', help='Returns true if nsp has titlerights')
		parser.add_argument('--nsp_hticket', nargs='+', help='Returns true if nsp has ticket')

		# Remove titlerights functions
		parser.add_argument('--remove-title-rights', nargs='+', help='Removes title rights encryption from all NCA\'s in the NSP.')
		parser.add_argument('--RTRNCA_h_nsp', nargs='+', help='Removes title rights encryption from a single nca reading from original nsp')
		parser.add_argument('--RTRNCA_h_tick', nargs='+', help='Removes title rights encryption from a single nca reading from extracted ticket')
		parser.add_argument('--set_masterkey', nargs='+', help='Changes the master key encryption for NSP.')

		# Gamecard flag functions
		parser.add_argument('--seteshop', nargs='+', help='Set all nca in an nsp as eshop')
		parser.add_argument('--setcgame', nargs='+', help='Set all nca in an nsp card')
		parser.add_argument('--seteshop_nca', nargs='+', help='Set a single nca as eshop')
		parser.add_argument('--setcgame_nca', nargs='+', help='Set a single nca as card')
		parser.add_argument('--cardstate', nargs='+', help='Returns value for isgamecard flag from an nca')
		parser.add_argument('--remlinkacc', nargs='+', help='Removelinkedaccount')

		# NSP Copy functions
		parser.add_argument('-x', '--extract', nargs='+', help='Extracts all files from nsp or xci')
		parser.add_argument('-raw_x', '--raw_extraction', nargs='+', help='Extracts files without checking readability, useful when there is bad files')
		parser.add_argument('-nfx', '--nca_file_extraction', nargs='+', help='Extracts files files within nca files from nsp/xci\nca file')
		parser.add_argument('-plx', '--extract_plain_nca', nargs='+', help='Extracts nca files as plaintext or generate a plaintext file from an nca file')
		parser.add_argument('--NSP_copy_ticket', nargs='+', help='Extracts ticket from target nsp')
		parser.add_argument('--NSP_copy_nca', nargs='+', help='Extracts all nca files from target nsp')
		parser.add_argument('--NSP_copy_other', nargs='+', help='Extracts all kinds of files different from nca or ticket from target nsp')
		parser.add_argument('--NSP_copy_xml', nargs='+', help='Extracts xml files from target nsp')
		parser.add_argument('--NSP_copy_cert', nargs='+', help='Extracts cert files from target nsp')
		parser.add_argument('--NSP_copy_jpg', nargs='+', help='Extracts jpg files from target nsp')
		parser.add_argument('--NSP_copy_cnmt', nargs='+', help='Extracts cnmt files from target nsp')
		parser.add_argument('--copy_pfs0_meta', nargs='+', help='Extracts meta pfs0 from target nsp')
		parser.add_argument('--copy_nacp', nargs='+', help='Extracts nacp files from target nsp')

		# XCI Copy functions
		parser.add_argument('--XCI_copy_hfs0', nargs='+', help='Extracts hfs0 partition files from target xci')
		parser.add_argument('--XCI_c_hfs0_secure', nargs='+', help='Extracts secure hfs0 partition files from target xci')
		parser.add_argument('--XCI_c_hfs0_normal', nargs='+', help='Extracts normal hfs0 partition files from target xci')
		parser.add_argument('--XCI_c_hfs0_update', nargs='+', help='Extracts update hfs0 partition files from target xci')
		parser.add_argument('--XCI_copy_nca_secure', nargs='+', help='Extracts nca from secure partition')
		parser.add_argument('--XCI_copy_nca_normal', nargs='+', help='Extracts nca from normal partition')
		parser.add_argument('--XCI_copy_nca_update', nargs='+', help='Extracts nca from update partition')
		parser.add_argument('--XCI_copy_rhfs0', nargs='+', help='Extracts root.hfs0')

		# Dedicated copy functions. NCA Types.
		parser.add_argument('--NSP_copy_nca_meta', nargs='+', help='Extracts nca files with type meta from target nsp')
		parser.add_argument('--NSP_copy_nca_control', nargs='+', help='Extracts nca files with type control from target nsp')
		parser.add_argument('--NSP_copy_nca_manual', nargs='+', help='Extracts nca files with type manual from target nsp')
		parser.add_argument('--NSP_copy_nca_program', nargs='+', help='Extracts nca files with type program from target nsp')
		parser.add_argument('--NSP_copy_nca_data', nargs='+', help='Extracts nca files with type data from target nsp')
		parser.add_argument('--NSP_copy_nca_pdata', nargs='+', help='Extracts nca fles with type public data from target nsp')

		# Dedicated copy functions. TITLERIGHTS.
		parser.add_argument('--NSP_copy_tr_nca', nargs='+', help='Extracts nca files with titlerights from target nsp')
		parser.add_argument('--NSP_copy_ntr_nca', nargs='+', help='Extracts nca files without titlerights from target nsp')
		parser.add_argument('--NSP_c_KeyBlock', nargs='+', help='Extracts keyblock from nsca files with titlerigths  from target nsp')
		parser.add_argument('--C_clean', nargs='+', help='Extracts nca files and removes it.s titlerights from target NSP OR XCI')
		parser.add_argument('--C_clean_ND', nargs='+', help='Extracts nca files and removes it.s titlerights from target NSP OR XCI without deltas')

		# Dedicated copy functions. SPLIT OR UPDATE.
		parser.add_argument('--splitter', nargs='+', help='Split content by titleid according to cnmt files')
		parser.add_argument('-dspl', '--direct_splitter', nargs='+', help='Split content by titleid according to cnmt files')
		parser.add_argument('--updbase', nargs='+', help='Prepare base file to update it')

		# Combinations
		parser.add_argument('--gen_placeholder', help='Creates nsp or xci placeholder')
		parser.add_argument('--placeholder_combo', nargs='+', help='Extracts nca files for placeholder nsp')
		parser.add_argument('--license_combo', nargs='+', help='Extracts nca files for license nsp')
		parser.add_argument('--mlicense_combo', nargs='+', help='Extracts nca files for tinfoil license nsp')
		parser.add_argument('--zip_combo', nargs='+', help='Extracts and generate files to make a restore zip')

		# Auxiliary
		parser.add_argument('-o', '--ofolder', nargs='+', help='Set output folder for copy instructions')
			
		parser.add_argument('-ifo', '--ifolder', help='Input folder')
		parser.add_argument('-ifo_s', '--ifolder_secure', help='Input secure folder')
		parser.add_argument('-ifo_n', '--ifolder_normal', help='Input normal folder')
		parser.add_argument('-ifo_u', '--ifolder_update', help='Input update folder')
		parser.add_argument('-tfile', '--text_file', help='Output text file')
		parser.add_argument('-tfile_aux', '--text_file_aux', help='Auxiliary text file')
		parser.add_argument('-dbfile', '--db_file', help='Output text file for database')
		parser.add_argument('-b', '--buffer', nargs='+', help='Set buffer for copy instructions')
		parser.add_argument('-ext', '--external', nargs='+', help='Set original nsp or ticket for remove nca titlerights functions')
		parser.add_argument('-pv', '--patchversion', nargs='+', help='Number fot patch Required system version or program, patch or addcontent version')
		parser.add_argument('-kp', '--keypatch', nargs='+', help='patch masterkey to input number')
		parser.add_argument('-rsvc', '--RSVcap', nargs='+', help='RSV cap when patching. Default is FW4.0')
		parser.add_argument('-pe', '--pathend', nargs='+', help='Output to subfolder')
		parser.add_argument('-cskip', '--cskip', nargs='+', help='Skip dlc or update')
		parser.add_argument('-fat', '--fat', nargs='+', help='Split xci for fat32 or exfat')
		parser.add_argument('-fx', '--fexport', nargs='+', help='Export splitted nsp to files or folder')
		parser.add_argument('-t', '--type', nargs='+', help='Type of file')
		parser.add_argument('-tid', '--titleid', nargs='+', help='Filter with titleid')
		parser.add_argument('-bid', '--baseid', nargs='+', help='Filter with base titleid')
		parser.add_argument('-ND', '--nodelta', nargs='+', help='Exclude deltas')
		parser.add_argument('-dbformat', '--dbformat', nargs='+', help='Database format extended, nutdb or keyless-extended')
		parser.add_argument('-rn', '--rename', nargs='+', help='Filter with base titleid')
		parser.add_argument('-uin', '--userinput', help='Reads a user input')
		parser.add_argument('-incxml', '--includexml', nargs='+', help='Include xml by default true')
		parser.add_argument('-trans', '--translate', nargs='+', help='Google translation support for nutdb descriptions')
		parser.add_argument('-nodcr', '--nodecompress', help="Don't decompress nsz_xcz in several modes")	
		
		# LISTMANAGER
		parser.add_argument('-cl', '--change_line', help='Change line in text file')
		parser.add_argument('-rl', '--read_line', help='Read line in text file')
		parser.add_argument('-stripl', '--strip_lines', nargs='+', help='Strips lines from a text file')
		parser.add_argument('-showcline', '--show_current_line', nargs='+', help='Shows current line')
		parser.add_argument('-countlines', '--count_n_lines', nargs='+', help='Count the number of lines')
		parser.add_argument('-dff', '--delete_item', nargs='+', help='Deletes a os item listed in text file, a file or a folder')
		parser.add_argument('-ln', '--line_number', help='line number')
		parser.add_argument('-nl', '--new_line', help='new line')
		parser.add_argument('-ff', '--findfile', help='find different types of files')
		parser.add_argument('-fil', '--filter', nargs='+', help='filter using strings')
		parser.add_argument('-splid', '--split_list_by_id', nargs='+', help='split a list by file id')
		parser.add_argument('-mv_oupd', '--mv_old_updates', nargs='+', help='Moves old updates to another folder')
		parser.add_argument('-mv_odlc', '--mv_old_dlcs', nargs='+', help='Moves old dlcs to another folder')
		parser.add_argument('-cr_ilist', '--cr_incl_list', nargs='+', help='Creates a include list from a textfile and a folder or 2 textfiles')
		parser.add_argument('-cr_elist', '--cr_excl_list', nargs='+', help='Creates a exclude list from a textfile and a folder or 2 textfiles')
		parser.add_argument('-cr_xcioutlist', '--cr_outdated_xci_list', nargs='+', help='Creates a outdated xci list from a textfile and a folder')
		parser.add_argument('-cr_xexplist', '--cr_expand_list', nargs='+', help='Expands the list with games by baseid')
		parser.add_argument('-chdlcn', '--chck_dlc_numb', nargs='+', help='Checks if xci has corrent number of dlcs')
		parser.add_argument('-blckl', '--black_list', nargs='+', help='Deletes blacklisted files from a list')

		# Archive
		if sys.platform == 'win32':
			parser.add_argument('-archive','--archive', help='Archive to folder')
		parser.add_argument('-zippy','--zippy', help='Zip a file')
		parser.add_argument('-joinfile','--joinfile', nargs='+', help='Join split file')
		# OTHER
		parser.add_argument('-nint_keys','--nint_keys', help='Verify NS keys')
		parser.add_argument('-renf','--renamef', help='Rename file with proper name')
		parser.add_argument('-renftxt','--renameftxt', help='Rename file with proper name using a text list')
		parser.add_argument('-snz','--sanitize', help='Remove unreadable characters from names')
		parser.add_argument('-roma','--romanize', nargs='+', help='Translate kanji and extended kanna to romaji and sanitize name')
		parser.add_argument('-oaid','--onlyaddid', help='Rename file with proper name')
		parser.add_argument('-renm','--renmode', help='Rename mode (force,skip_corr_tid,skip_if_tid)')
		parser.add_argument('-addl','--addlangue', help='Add language string')
		parser.add_argument('-nover','--noversion', help="Don't add version (false,true,xci_no_v0)")
		parser.add_argument('-dlcrn','--dlcrname', help="If false keeps base name in dlcs")
		parser.add_argument('-cltg','--cleantags', help="Clean tags in filenames")
		parser.add_argument('-tgtype','--tagtype', help="Type of tag to remove")
		parser.add_argument('-vorg','--v_organize', help="Aux variable to organize files")
		parser.add_argument('-vt','--vertype', help="Verification type for auto, needs --text_file. Opt: dec,sig,full [DECryption, decryption and SIGnature, previous and hash check]")
		parser.add_argument('-threads','--threads', help="Number threads to use for certain functions")
		parser.add_argument('-pararell','--pararell', help="Number threads to use for certain functions")		
		parser.add_argument('-lib_call','--library_call', nargs='+',  help="Call a library function within squirrel")
		parser.add_argument('-loop','--loop', nargs='+', help="Loop the text file using secondary module")
		
		# Hidden
		parser.add_argument('-dev_env','--dev_environment', help=argparse.SUPPRESS)#Changes key environment to dev if True
		parser.add_argument('-pos','--position', help=argparse.SUPPRESS)#tqdm position, aux argument for pararell	
		parser.add_argument('-ninst','--n_instances', help=argparse.SUPPRESS)#number of instances, aux argument for pararell			
		parser.add_argument('-xarg','--explicit_argument', nargs='+', help=argparse.SUPPRESS)#Explicit	arguments for lib_call for files with ","			
		parser.add_argument('-mtpeval','--mtp_eval_link', nargs='+', help=argparse.SUPPRESS)#Explicit	arguments for lib_call for files with ","					
		# -> parser.add_argument('-act', '--action', nargs='+', help=argparse.SUPPRESS)		
		# -> parser.add_argument('-preverify', '--preverification', nargs='+', help=argparse.SUPPRESS)			
		# -> parser.add_argument('-verDB', '--verificationDB', nargs='+', help=argparse.SUPPRESS) #verificationDB
		args = parser.parse_args()

		Status.start()

		indent = 1
		tabs = '\t' * indent
		trans=False
		if args.file==list():
			args.file=None
		if args.dev_environment:		
			from importlib import reload 
			if 	str(args.dev_environment).upper()=="TRUE":
				sq_settings.set_dev_environment()
				reload(Keys)
				
		import sq_tools
		import listmanager
		import Titles
		import Fs	
		import Print
		import Nsps
		import DBmodule as dbmodule
		from hashlib import sha256
		from pathlib import Path
		from binascii import hexlify as hx, unhexlify as uhx
		if sys.platform == 'win32':
			import win32con, win32api
		import shutil
		from tqdm import tqdm
		from datetime import datetime
		import math
		import pykakasi
		from Fs.pyNCA3 import NCA3
		from shutil import disk_usage
		
		from cmds.Api import CmdApi
		cmdApi = CmdApi(args)

		if args.library_call:
			if (args.library_call[0]).startswith('Drive.'):
				sys.path.insert(0, 'Drive')
				args.library_call[0]=str(args.library_call[0]).replace("Drive.", "")
			if (args.library_call[0]).startswith('mtp.'):
				sys.path.insert(0, 'mtp')
				args.library_call[0]=str(args.library_call[0]).replace("mtp.", "")		
			if (args.library_call[0]).startswith('cmd.'):
				sys.path.insert(0, 'cmd')
				args.library_call[0]=str(args.library_call[0]).replace("cmd.", "")					
			import secondary
			if args.explicit_argument:
				#vret=secondary.call_library(args.library_call,args.explicit_argument)
				vret=secondary.call_library(args.library_call)
			else:
				vret=secondary.call_library(args.library_call)
			Status.close()
			
		if args.mtp_eval_link:
			tfile=args.mtp_eval_link[0]
			userfile=args.mtp_eval_link[1]			
			link=input("Enter your choice: ")
			link=link.strip()
			if '&' in link:
				varout='999'
			elif len(link)<2:
				varout=link
			else:
				varout='999'
			with open(userfile,"w", encoding='utf8') as userinput:
				userinput.write(varout)		
			if link.startswith('https://1fichier.com'):
				with open(tfile,"a", encoding='utf8') as textfile:
					textfile.write(link+'\n')				
			elif link.startswith('https://drive.google.com'):
				with open(tfile,"a", encoding='utf8') as textfile:
					textfile.write(link+'\n')						

		if args.threads and not args.compress and not args.decompress:
			import secondary
			workers=1
			try:
				workers=int(args.threads)
			except:pass
			try:
				if workers>1:
					secondary.route(args,workers)
					#secondary.printargs(args)
					Status.close()
				else:pass
			except:pass
		elif args.pararell and args.threads :
			import secondary
			instances=2
			if args.pararell=='true':
				args.pararell=None
				try:
					instances=int(args.threads)
					if instances<= 0:
						instances=1
				except:	
					instances=2
				args.threads=0	
				items=secondary.pararell(args,instances)
				if items==0:
					try:
						os.remove(args.text_file)
					except:
						pass						
					for attr in vars(args):
						setattr(args,attr,None)	
						
		if args.loop and args.ifolder:							
			if args.loop[0]!='true' and args.loop[0]!='false' and args.text_file!='false':
				if os.path.exists(args.text_file):
					try:
						os.remove(args.text_file)
					except:
						pass				
				import secondary
				args0=args
				args0.type=args0.loop
				args0.loop=None
				args0.findfile=args0.ifolder
				args0.ifolder=None
				secondary.pass_command(args0)
				args.ifolder=None
				args.findfile=None
				loop=list()
				loop.append('true')
				args.loop=loop
				
		if args.loop and args.text_file:		
			if str(args.loop[0]).lower()=='true':	
				import secondary
				args.loop=None
				items=secondary.pass_command(args)
				if items==0:
					try:
						os.remove(args.text_file)
					except:
						pass					
					for attr in vars(args):
						setattr(args,attr,None)				
			else:
				args.loop=None 
						
# NCA/NSP IDENTIFICATION
		cmdApi.handleFsDef()
		Status.close()
# REMOVE TITLERIGHTS FUNCTIONS
		cmdApi.handleFsDef()
		Status.close()
# GAMECARD FLAG FUNCTIONS
		cmdApi.handleFsDef()
		Status.close()
# COPY FUNCTIONS
		cmdApi.handleFsCopy()
		Status.close()
# DEDICATED COPY FUNCTIONS. NCA TYPES.
		cmdApi.handleFsCopy()
		Status.close()
# DEDICATED COPY FUNCTIONS. TITLERIGHTS.
		cmdApi.handleFsCopy()
		Status.close()
# DEDICATED COPY FUNCTIONS. SPLIT OR UPDATE.
		cmdApi.handleFsCopy()
		Status.close()
# COMBINATIONS
		# ............................................................
		# Get nca files to make a placeholder in eshop format from NSP
		# ............................................................
		'''
		parser.add_argument('--gen_placeholder', nargs='+', help='Creates nsp or xci placeholder')
		'''
		if args.gen_placeholder:
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
				folder = args.gen_placeholder
				dir=os.path.abspath(folder)
				ofolder = os.path.join(dir, 'output')
			if not os.path.exists(ofolder):
				os.makedirs(ofolder)
			if args.text_file:
				tfile=args.text_file
				with open(tfile,"r+", encoding='utf8') as filelist:
					filename = filelist.readline()
					ruta=os.path.abspath(filename.rstrip('\n'))
			else:
				ruta=args.gen_placeholder
				indent = 1
				tabs = '\t' * indent
				if ruta[-1]=='"':
					ruta=ruta[:-1]
				if ruta[0]=='"':
					ruta=ruta[1:]
			extlist=list()
			if args.type:
				for t in args.type:
					x='.'+t
					extlist.append(x)
					if x[-1]=='*':
						x=x[:-1]
						extlist.append(x)
			#print(extlist)
			if args.filter:
				for f in args.filter:
					filter=f

			filelist=list()
			ruta=str(ruta)
			#print(ruta)
			try:
				fname=""
				binbin='RECYCLE.BIN'
				for ext in extlist:
					#print (ext)
					if os.path.isdir(ruta):
						for dirpath, dirnames, filenames in os.walk(ruta):
							for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
								fname=""
								if args.filter:
									if filter.lower() in filename.lower():
										fname=filename
								else:
									fname=filename
								if fname != "":
									if binbin.lower() not in filename.lower():
										filelist.append(os.path.join(dirpath, filename))
					else:
						if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
							filename = ruta
							#print(filename)
							fname=""
							if args.filter:
								if filter.lower() in filename.lower():
									fname=filename
							else:
								fname=filename
							if fname != "":
								if binbin.lower() not in filename.lower():
									filelist.append(filename)
				'''
				for f in filelist:
					print(f)
				'''
				print('Files to process: '+str(len(filelist)))
				counter=len(filelist)
				for filepath in filelist:
					if filepath.endswith('.nsp') or filepath.endswith('.nsx'):
						export='nsp'
						try:
							prlist=list()
							f = Fs.Nsp(filepath)
							contentlist=f.get_content_placeholder(ofolder)
							#print(contentlist)
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
										#print (contentlist[j][6])
										#pass
										if contentlist[j][1] == prlist[i][1]:
											if contentlist[j][6] > prlist[i][6]:
												del prlist[i]
												prlist.append(contentlist[j])
												notinlist=False
											elif contentlist[j][6] == prlist[i][6]:
												notinlist=False
										else:
											notinlist=True
									if notinlist == True:
										prlist.append(contentlist[j])
						except BaseException as e:
							counter=int(counter)
							counter-=1
							Utils.logError(e)
							continue
					if filepath.endswith('.xci'):
						export='xci'
						try:
							prlist=list()
							f = Fs.Xci(filepath)
							contentlist=f.get_content_placeholder(ofolder)
							#print(contentlist)
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
										#print (contentlist[j][6])
										#pass
										if contentlist[j][1] == prlist[i][1]:
											if contentlist[j][6] > prlist[i][6]:
												del prlist[i]
												prlist.append(contentlist[j])
												notinlist=False
											elif contentlist[j][6] == prlist[i][6]:
												notinlist=False
										else:
											notinlist=True
									if notinlist == True:
										prlist.append(contentlist[j])
						except BaseException as e:
							counter=int(counter)
							counter-=1
							Utils.logError(e)
							continue
					if export=='nsp':
						oflist=list()
						osizelist=list()
						totSize=0
						#print(prlist)
						for i in range(len(prlist)):
							for j in prlist[i][4]:
								oflist.append(j[0])
								osizelist.append(j[1])
								totSize = totSize+j[1]
								filelist
						basename=str(os.path.basename(os.path.abspath(filepath)))
						endname=basename[:-4]+'[PLH].nsp'
						endfile = os.path.join(ofolder, endname)
						#print(str(filepath))
						#print(str(endfile))
						nspheader=sq_tools.gen_nsp_header(oflist,osizelist)
						#print(endfile)
						#print(hx(nspheader))
						totSize = len(nspheader) + totSize
						#print(str(totSize))
						vskip=False
						print('Processing: '+str(filepath))
						if os.path.exists(endfile) and os.path.getsize(endfile) == totSize:
							print('- Placeholder file already exists, skipping...')
							vskip=True
						else:
							if sys.platform == 'win32':
								v_drive, v_path = os.path.splitdrive(endfile)
							else:
								v_drive = os.path.dirname(os.path.abspath(endfile))
							dsktotal, dskused, dskfree=disk_usage(str(v_drive))
							if int(dskfree)<int(totSize):
								sys.exit("Warning disk space lower than required size. Program will exit")
						if vskip==False:
							t = tqdm(total=totSize, unit='B', unit_scale=True, leave=False)
							outf = open(endfile, 'w+b')
							t.write(tabs+'- Writing NSP header...')
							outf.write(nspheader)
							t.update(len(nspheader))
							outf.close()
							if filepath.endswith('.nsp') or filepath.endswith('.nsx'):
								try:
									f = Fs.Nsp(filepath)
									for file in oflist:
										if not file.endswith('xml'):
											f.append_content(endfile,file,buffer,t)
									f.flush()
									f.close()
									t.close()
									counter=int(counter)
									counter-=1
									print(tabs+'> Placeholder was created')
									if not args.text_file:
										print(tabs+'> Still '+str(counter)+' to go')
								except BaseException as e:
									counter=int(counter)
									counter-=1
									Utils.logError(e)
					if export=='xci':
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
						if filepath.endswith('.xci'):
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
						basename=str(os.path.basename(os.path.abspath(filepath)))
						endname=basename[:-4]+'[PLH].xci'
						endfile = os.path.join(ofolder, endname)
						#print(str(filepath))
						#print(str(endfile))
						xci_header,game_info,sig_padding,xci_certificate,root_header,upd_header,norm_header,sec_header,rootSize,upd_multiplier,norm_multiplier,sec_multiplier=sq_tools.get_xciheader(oflist,osizelist,sec_hashlist)
						totSize=len(xci_header)+len(game_info)+len(sig_padding)+len(xci_certificate)+rootSize
						#print(str(totSize))
						vskip=False
						print('Processing: '+str(filepath))
						if os.path.exists(endfile) and os.path.getsize(endfile) == totSize:
							print('- Placeholder file already exists, skipping...')
							vskip=True
						else:
							if sys.platform == 'win32':
								v_drive, v_path = os.path.splitdrive(endfile)
							else:
								v_drive = os.path.dirname(os.path.abspath(endfile))
							dsktotal, dskused, dskfree=disk_usage(str(v_drive))
							if int(dskfree)<int(totSize):
								sys.exit("Warning disk space lower than required size. Program will exit")						
						if vskip==False:
							c=0
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
							if filepath.endswith('.xci'):
								try:
									GC=False
									f = Fs.Xci(filepath)
									for file in oflist:
										if not file.endswith('xml'):
											for i in range(len(GClist)):
												if GClist[i][0] == file:
													GC=GClist[i][1]
											f.append_content(endfile,file,buffer,t,includexml=False)
									f.flush()
									f.close()
									t.close()
									counter=int(counter)
									counter-=1
									print(tabs+'> Placeholder was created')
									if not args.text_file:
										print(tabs+'> Still '+str(counter)+' to go')
								except BaseException as e:
									counter=int(counter)
									counter-=1
									Utils.logError(e)
			except BaseException as e:
				Utils.logError(e)
			Status.close()
		# ............................................................
		# Get files to make a [lc].nsp from NSP
		# ............................................................
		if args.license_combo:
			if args.ofolder:
				for input in args.ofolder:
					try:
						ofolder = input
					except BaseException as e:
						Utils.logError(e)
			else:
				for filename in args.license_combo:
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
			for filename in args.license_combo:
				try:
					f = Fs.Nsp(filename, 'rb')
					f.copy_nca_control(ofolder,buffer)
					f.copy_ticket(ofolder)
					f.copy_nsp_cert(ofolder,buffer)
					f.flush()
					f.close()
				except BaseException as e:
					Utils.logError(e)
			Status.close()
		# ............................................................
		# Get files to make a placeholder+license nsp from a NSP
		# ............................................................
		if args.mlicense_combo:
			if args.ofolder:
				for input in args.ofolder:
					try:
						ofolder = input
					except BaseException as e:
						Utils.logError(e)
			else:
				for filename in args.mlicense_combo:
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
			for filename in args.mlicense_combo:
				try:
					f = Fs.Nsp(filename, 'rb')
					f.copy_nca_control(ofolder,buffer)
					f.copy_nca_meta(ofolder,buffer)
					f.copy_ticket(ofolder)
					f.copy_nsp_cert(ofolder,buffer)
					f.flush()
					f.close()
				except BaseException as e:
					Utils.logError(e)
			Status.close()
		# ............................................................
		# Get files to make zip to restore nsp to original state
		# ............................................................
		if args.zip_combo:
			if args.ofolder:
				for input in args.ofolder:
					try:
						ofolder = input
					except BaseException as e:
						Utils.logError(e)
			else:
				for filename in args.zip_combo:
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

			for filename in args.zip_combo:
				try:
					f = Fs.Nsp(filename, 'rb')
					f.copy_nca_meta(ofolder,buffer)
					f.copy_ticket(ofolder)
					f.copy_other(ofolder,buffer)
					f.flush()
					f.close()
				except BaseException as e:
					Utils.logError(e)
			Status.close()
# REPACK
		cmdApi.handleFsRepack()
		Status.close()		
		# Archive to nsp
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
			Status.close()
# INFORMATION
		cmdApi.handleFsInfo()
		Status.close()

		# LISTMANAGER

		# ..................
		# Generate cnmt.xml
		# ..................
		if args.xml_gen:
			if args.ofolder:
				for input in args.ofolder:
					try:
						ofolder = input
					except BaseException as e:
						Utils.logError(e)
			else:
				for filename in args.xml_gen:
					dir=os.path.dirname(os.path.abspath(filename))
					ofolder =os.path.join(dir, 'output')
			for filename in args.xml_gen:
				if filename.endswith('.nca'):
					try:
						with open(filename, 'r+b') as file:
							nsha=sha256(file.read()).hexdigest()
						f = Fs.Nca(filename, 'r+b')
						f.xml_gen(ofolder,nsha)
					except BaseException as e:
						Utils.logError(e)
			Status.close()


		# ...................................................
		# Change line in text file
		# ...................................................

		if args.change_line:
			if args.line_number:
				try:
					line_number = int(args.line_number)
				except BaseException as e:
					Utils.logError(e)
			if args.new_line:
				try:
					new_line = str(args.new_line)
				except BaseException as e:
					Utils.logError(e)
			if args.change_line:
				try:
					config_file=os.path.abspath(str(args.change_line))
					lines = open(str(config_file)).read().splitlines()
					lines[line_number] = str(new_line)
					open(str(config_file),'w').write('\n'.join(lines))
				except BaseException as e:
					Utils.logError(e)
			Status.close()
		# ...................................................
		# Read line in text file
		# ...................................................

		if args.read_line:
			if args.new_line:
				try:
					write_line = str(args.new_line)
				except BaseException as e:
					Utils.logError(e)
			if args.line_number:
				try:
					line_number = int(args.line_number)
				except BaseException as e:
					Utils.logError(e)
			if args.read_line:
				try:
					indent = 4
					tabs = '\t' * indent
					config_file=os.path.abspath(str(args.read_line))
					lines = open(str(config_file)).read().splitlines()
					line2read= str(lines[line_number])
					Print.info(write_line + line2read)
				except BaseException as e:
					Utils.logError(e)
			Status.close()
		# ...................................................
		# Strip line in text file
		# ...................................................
		#parser.add_argument('-stripl', '--strip_lines', nargs='+', help='Strips lines from a text file')
		if args.strip_lines:
			if args.strip_lines[0]:
				textfile=args.strip_lines[0]
			try:
				if args.strip_lines[1]:
					number=args.strip_lines[1]
				else:
					number=1
			except:
				number=1
			try:
				if args.strip_lines[2]:
					uinput=args.strip_lines[2]
					if str(uinput).upper() == 'TRUE':
						counter=True
				else:
					counter=False
			except:
				counter=False
			try:
				listmanager.striplines(textfile,number,counter)
			except BaseException as e:
				Utils.logError(e)

		#parser.add_argument('-showcline', '--show_current_line', nargs='+', help='Shows current line')
		if args.show_current_line:
			if args.show_current_line[0]:
				textfile=args.show_current_line[0]
				try:
					number=args.show_current_line[1]
				except:
					number=1
			try:
				listmanager.printcurrent(textfile,number)
			except BaseException as e:
				Utils.logError(e)

		#parser.add_argument('-countlines', '--count_n_lines', nargs='+', help='Count the number of lines')
		if args.count_n_lines:
			if args.count_n_lines[0]:
				textfile=args.count_n_lines[0]
			try:
				c=listmanager.counter(textfile)
				print('STILL '+str(c)+' FILES TO PROCESS')
			except BaseException as e:
				Utils.logError(e)

		#parser.add_argument('-dff', '--delete_item', nargs='+', help='Deletes a os item listed in text file, a file or a folder')
		if args.delete_item:
			if args.text_file:
				tfile=args.text_file
				with open(tfile,"r+", encoding='utf8') as filelist:
					ruta = filelist.readline()
					ruta=os.path.abspath(ruta.rstrip('\n'))
					ruta = os.path.abspath(ruta)
				try:
					os.remove(ruta)
				except BaseException as e:
					Utils.logError(e)
					pass
			else:
				ruta = os.path.abspath(args.delete_item[0])
				if os.path.isdir(ruta):
					try:
						shutil.rmtree(ruta, ignore_errors=True)
					except BaseException as e:
						Utils.logError(e)
						pass
				elif os.path.isfile(ruta):
					try:
						os.remove(ruta)
					except BaseException as e:
						Utils.logError(e)
						pass
				else:
					print('Input is not a system file or folder')
			Status.close()
		# ...................................................
		# Generate list of files
		# ...................................................
		#parser.add_argument('-tid', '--titleid', nargs='+', help='Filter with titleid')
		#parser.add_argument('-bid', '--baseid', nargs='+', help='Filter with base titleid')

		if args.findfile:
			raised_error=False
			if args.findfile  == 'uinput':
				ruta=input("PLEASE DRAG A FILE OR FOLDER OVER THE WINDOW AND PRESS ENTER: ")
				if '&' in ruta:
					varout='999'
				elif len(ruta)<2:
					varout=ruta
				else:
					varout='999'

				if args.userinput:
					userfile=args.userinput
				else:
					userfile='uinput'

				with open(userfile,"w", encoding='utf8') as userinput:
					userinput.write(varout)
			else:
				ruta=args.findfile
			try:	
				if ruta[-1]=='"':
					ruta=ruta[:-1]
				if ruta[0]=='"':
					ruta=ruta[1:]
			except:
				raised_error=True
			if not os.path.exists(ruta):
				raised_error=True
			if raised_error==False:
				extlist=list()
				if args.type:
					for t in args.type:
						if t=="all":
							extlist.append('all')
							continue
						x='.'+t
						extlist.append(x)
						if x[-1]=='*':
							x=x[:-1]
							extlist.append(x)
						elif x==".00":
							extlist.append('00')
				#print(extlist)
				if args.filter:
					for f in args.filter:
						filter=f

				filelist=list()
				try:
					fname=""
					binbin='RECYCLE.BIN'
					if not 'all' in extlist:
						for ext in extlist:
							#print (ext)
							if os.path.isdir(ruta):
								for dirpath, dirnames, filenames in os.walk(ruta):
									for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
										fname=""
										if args.filter:
											if filter.lower() in filename.lower():
												fname=filename
										else:
											fname=filename
										if fname != "":
											if binbin.lower() not in filename.lower():
												filelist.append(os.path.join(dirpath, filename))
							else:
								if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
									filename = ruta
									fname=""
									if args.filter:
										if filter.lower() in filename.lower():
											fname=filename
									else:
										fname=filename
									if fname != "":
										if binbin.lower() not in filename.lower():
											filelist.append(filename)
					else:
						# print(ruta)
						if os.path.isdir(ruta):
							for dirpath, dirnames, filenames in os.walk(ruta):
								for filename in [f for f in filenames]:
									fname=""
									if args.filter:
										if filter.lower() in filename.lower():
											fname=filename
									else:
										fname=filename
									if fname != "":
										if binbin.lower() not in filename.lower():
											filelist.append(os.path.join(dirpath, filename))
						else:
							filename = ruta
							fname=""
							if args.filter:
								if filter.lower() in filename.lower():
									fname=filename
							else:
								fname=filename
							if fname != "":
								if binbin.lower() not in filename.lower():
									filelist.append(filename)
					if args.text_file:
						tfile=args.text_file
						with open(tfile,"a", encoding='utf8') as tfile:
							for line in filelist:
								try:
									tfile.write(line+"\n")
								except:
									continue
					else:
						for line in filelist:
							try:
								print (line)
							except:
								continue
				except BaseException as e:
					Utils.logError(e)

		if args.nint_keys:
			try:
				sq_tools.verify_nkeys(args.nint_keys)
			except BaseException as e:
				Utils.logError(e)
			Status.close()
		# ...................................................
		# Clean tags in filenames
		# ...................................................
		#parser.add_argument('-tgtype','--tagtype', help="Type of tag to remove")
		if args.cleantags:
			if args.tagtype:
				if args.tagtype=="[]":
					tagtype='brackets'
				elif args.tagtype=="()":
					tagtype='parenthesis'
				elif args.tagtype=="(":
					tagtype='('
				elif args.tagtype=="[":
					tagtype='['
				else:
					tagtype=False
			else:
				tagtype=False
			if args.text_file and args.cleantags == 'single':
				tfile=args.text_file
				with open(tfile,"r+", encoding='utf8') as filelist:
					ruta = filelist.readline()
					ruta=os.path.abspath(ruta.rstrip('\n'))
					ruta = os.path.abspath(ruta)
			else:
				ruta=args.cleantags
			#print(ruta)
			indent = 1
			tabs = '\t' * indent
			if ruta[-1]=='"':
				ruta=ruta[:-1]
			if ruta[0]=='"':
				ruta=ruta[1:]
			extlist=list()
			if args.type:
				for t in args.type:
					x='.'+t
					extlist.append(x)
					if x[-1]=='*':
						x=x[:-1]
						extlist.append(x)
			#print(extlist)
			if args.filter:
				for f in args.filter:
					filter=f

			filelist=list()
			try:
				fname=""
				binbin='RECYCLE.BIN'
				for ext in extlist:
					#print (ext)
					if os.path.isdir(ruta):
						for dirpath, dirnames, filenames in os.walk(ruta):
							for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
								fname=""
								if args.filter:
									if filter.lower() in filename.lower():
										fname=filename
								else:
									fname=filename
								if fname != "":
									if binbin.lower() not in filename.lower():
										filelist.append(os.path.join(dirpath, filename))
					else:
						if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
							filename = ruta
							fname=""
							if args.filter:
								if filter.lower() in filename.lower():
									fname=filename
							else:
								fname=filename
							if fname != "":
								if binbin.lower() not in filename.lower():
									filelist.append(filename)
				'''
				for f in filelist:
					print(f)
				'''
				print('Items to process: '+str(len(filelist)))
				counter=len(filelist)
				for filepath in filelist:
					basename=str(os.path.basename(os.path.abspath(filepath)))
					endname=basename
					dir=os.path.dirname(os.path.abspath(filepath))
					print('Filename: '+basename)
					if tagtype==False or tagtype=='brackets':
						tid1=list()
						tid2=list()
						tid1=[pos for pos, char in enumerate(filepath) if char == '[']
						tid2=[pos for pos, char in enumerate(filepath) if char == ']']
						if len(tid1)>=len(tid2):
							lentlist=len(tid1)
						elif len(tid1)<len(tid2):
							lentlist=len(tid2)
						for i in range(lentlist):
							i1=tid1[i]
							i2=tid2[i]+1
							t=filepath[i1:i2]
							endname=endname.replace(t,'')
							endname=endname.replace('  ',' ')
					if tagtype=='[':
						tid1=list()
						tid2=list()
						tid1=[pos for pos, char in enumerate(filepath) if char == '[']
						tid2=[pos for pos, char in enumerate(filepath) if char == ']']
						if len(tid1)>=len(tid2):
							lentlist=len(tid1)
						elif len(tid1)<len(tid2):
							lentlist=len(tid2)
						for i in range(lentlist):
							i1=tid1[i]
							i2=tid2[i]+1
							endname=filepath[:i1]+filepath[-4:]
							break
					if tagtype=='(':
						tid3=list()
						tid4=list()
						tid3=[pos for pos, char in enumerate(endname) if char == '(']
						tid4=[pos for pos, char in enumerate(endname) if char == ')']
						if len(tid3)>=len(tid4):
							lentlist=len(tid3)
						elif len(tid3)<len(tid4):
							lentlist=len(tid4)
						for i in range(lentlist):
							i3=tid3[i]
							i4=tid4[i]+1
							endname=filepath[:i3]+filepath[-4:]
							break
					if tagtype==False or tagtype=='parenthesis':
						tid3=list()
						tid4=list()
						tid3=[pos for pos, char in enumerate(endname) if char == '(']
						tid4=[pos for pos, char in enumerate(endname) if char == ')']
						if len(tid3)>=len(tid4):
							lentlist=len(tid3)
						elif len(tid3)<len(tid4):
							lentlist=len(tid4)
						for i in range(lentlist):
							i3=tid3[i]
							i4=tid4[i]+1
							t=endname[i3:i4]
							#print('t is '+t)
							endname=endname.replace(t,'')
							endname=endname.replace('  ',' ')
					endname=endname.replace(' .','.')
					dir=os.path.dirname(os.path.abspath(filepath))
					newpath=os.path.join(dir,endname)
					print('New name: '+endname)
					if os.path.exists(newpath) and newpath != filepath:
						if filepath.endswith('.xci'):
							endname=endname[:-4]+' (SeemsDuplicate)'+'.xci'
							newpath=os.path.join(dir,endname)
						elif filepath.endswith('.nsp'):
							endname=endname[:-4]+' (SeemsDuplicate)'+'.nsp'
							newpath=os.path.join(dir,endname)
						elif filepath.endswith('.xcz'):
							endname=endname[:-4]+' (SeemsDuplicate)'+'.xcz'
							newpath=os.path.join(dir,endname)
						elif filepath.endswith('.nsx'):
							endname=endname[:-4]+' (SeemsDuplicate)'+'.nsx'
							newpath=os.path.join(dir,endname)	
						elif filepath.endswith('.nsz'):
							endname=endname[:-4]+' (SeemsDuplicate)'+'.nsz'
							newpath=os.path.join(dir,endname)								
					try:
						os.rename(filepath, newpath)
						print(tabs+'> File was renamed to: '+endname)
					except BaseException as e:
						pass
			except BaseException as e:
				counter=int(counter)
				counter-=1
				Utils.logError(e)
			Status.close()
		# ...................................................
		# Rename file with proper name
		# ...................................................
		#parser.add_argument('-oaid','--onlyaddid', help='Rename file with proper name')
		#parser.add_argument('-renm','--renmode', help='Rename mode (force,skip_corr_tid,skip_if_tid)')
		#parser.add_argument('-addl','--addlangue', help='Add language string')
		#parser.add_argument('-nover','--noversion', help="Don't add version (false,true,xci_no_v0)")
		#parser.add_argument('-dlcrn','--dlcrname', help="If false keeps base name in dlcs")

		if args.renamef:
			import nutdb
			languetag=''
			if args.romanize:
				for input in args.romanize:
					roman=str(input).upper()
					if roman == "FALSE":
						roman = False
					else:
						roman = True
			else:
				roman = True			
			if args.onlyaddid:
				if args.onlyaddid=="true" or args.onlyaddid == "True" or args.onlyaddid == "TRUE":
					onaddid=True
				elif args.onlyaddid=="idtag":
					onaddid='idtag'
				else:
					onaddid=False
			else:
				onaddid=False
			if args.addlangue:
				if args.addlangue=="true" or args.addlangue == "True" or args.addlangue == "TRUE":
					addlangue=True
				else:
					addlangue=False
			else:
				addlangue=False
			if args.renmode:
				if args.renmode=="skip_if_tid":
					renmode="skip_if_tid"
				elif args.renmode=="force":
					renmode="force"
				else:
					renmode="skip_corr_tid"
			else:
				renmode="skip_corr_tid"
			if args.noversion:
				if args.noversion=="true" or args.noversion == "True" or args.noversion == "TRUE":
					nover=True
				elif args.noversion=="xci_no_v0":
					nover="xci_no_v0"
				else:
					nover=False
			else:
				nover=False
			if args.dlcrname:
				if args.dlcrname=="true" or args.dlcrname == "True" or args.dlcrname == "TRUE":
					dlcrname=True
				elif args.dlcrname=="tag" or args.dlcrname == "Tag" or args.dlcrname == "TAG":
					dlcrname='tag'
				else:
					dlcrname=False
			else:
				dlcrname=False
			if args.text_file and args.renamef == 'single':
				tfile=args.text_file
				with open(tfile,"r+", encoding='utf8') as filelist:
					ruta = filelist.readline()
					ruta=os.path.abspath(ruta.rstrip('\n'))
					ruta = os.path.abspath(ruta)
			else:
				ruta=args.renamef
			#print(ruta)
			indent = 1
			tabs = '\t' * indent
			if ruta[-1]=='"':
				ruta=ruta[:-1]
			if ruta[0]=='"':
				ruta=ruta[1:]
			extlist=list()
			if args.type:
				for t in args.type:
					x='.'+t
					extlist.append(x)
					if x[-1]=='*':
						x=x[:-1]
						extlist.append(x)
			#print(extlist)
			if args.filter:
				for f in args.filter:
					filter=f

			filelist=list()
			try:
				fname=""
				binbin='RECYCLE.BIN'
				for ext in extlist:
					#print (ext)
					if os.path.isdir(ruta):
						for dirpath, dirnames, filenames in os.walk(ruta):
							for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
								fname=""
								if args.filter:
									if filter.lower() in filename.lower():
										fname=filename
								else:
									fname=filename
								if fname != "":
									if binbin.lower() not in filename.lower():
										filelist.append(os.path.join(dirpath, filename))
					else:
						if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
							filename = ruta
							fname=""
							if args.filter:
								if filter.lower() in filename.lower():
									fname=filename
							else:
								fname=filename
							if fname != "":
								if binbin.lower() not in filename.lower():
									filelist.append(filename)
				'''
				for f in filelist:
					print(f)
				'''
				if args.text_file:
					print('Items to process: '+str(len(filelist)))
				counter=len(filelist)
				for filepath in filelist:
					setskip=False
					if renmode == "skip_if_tid":
						tid1=list()
						tid2=list()
						tid1=[pos for pos, char in enumerate(filepath) if char == '[']
						tid2=[pos for pos, char in enumerate(filepath) if char == ']']
						if len(tid1)>=len(tid2):
							lentlist=len(tid1)
						elif len(tid1)<len(tid2):
							lentlist=len(tid2)
						for i in range(lentlist):
							i1=tid1[i]+1
							i2=tid2[i]
							t=filepath[i1:i2]
							if len(t)==16:
								try:
									int(filepath[i1:i2], 16)
									basename=str(os.path.basename(os.path.abspath(filepath)))
									print('Filename: '+basename)
									print(tabs+'> File already has id: '+filepath[i1:i2])
									setskip=True
								except:
									pass
					if setskip == True:
						counter=int(counter)
						counter-=1
						if not args.text_file:
							print(tabs+'> Still '+str(counter)+' to go')
						continue
					if filepath.endswith('.nsp') or filepath.endswith('.nsx') or filepath.endswith('.nsz'):
						try:
							prlist=list()
							f = Fs.Nsp(filepath)
							contentlist=f.get_content(False,False,True)
							#print(contentlist)
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
										#print (contentlist[j][6])
										#pass
										if contentlist[j][1] == prlist[i][1]:
											if contentlist[j][6] > prlist[i][6]:
												del prlist[i]
												prlist.append(contentlist[j])
												notinlist=False
											elif contentlist[j][6] == prlist[i][6]:
												notinlist=False
										else:
											notinlist=True
									if notinlist == True:
										prlist.append(contentlist[j])
						except BaseException as e:
							counter=int(counter)
							counter-=1
							Utils.logError(e)
							continue
						#print(prlist)
					if filepath.endswith('.xci') or filepath.endswith('.xcz'):
						filepath.strip()
						print("Processing "+filepath)
						#print(filepath)
						try:
							prlist=list()
							#f = Fs.Xci(filepath)
							f = Fs.factory(filepath)
							f.open(filepath, 'rb')
							contentlist=f.get_content(False,False,True)
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
										#print (contentlist[j][6])
										#pass
										if contentlist[j][1] == prlist[i][1]:
											if contentlist[j][6] > prlist[i][6]:
												del prlist[i]
												prlist.append(contentlist[j])
												notinlist=False
											elif contentlist[j][6] == prlist[i][6]:
												notinlist=False
										else:
											notinlist=True
									if notinlist == True:
										prlist.append(contentlist[j])
						except BaseException as e:
							counter=int(counter)
							counter-=1
							Utils.logError(e)
							continue
					if filepath.endswith('.xci') or filepath.endswith('.nsp') or filepath.endswith('.nsx') or filepath.endswith('.nsz') or filepath.endswith('.xcz'):
						basecount=0; basename='';basever='';baseid='';basefile=''
						updcount=0; updname='';updver='';updid='';updfile=''
						dlccount=0; dlcname='';dlcver='';dlcid='';dlcfile=''
						endname=0; mgame=''
						ccount='';bctag='';updtag='';dctag=''
						for i in range(len(prlist)):
							#print(prlist[i][5])
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
									#print(str(prlist))
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
							basename=str(os.path.basename(os.path.abspath(filepath)))
							basename2=basename.upper()
							check=str('['+baseid+']').upper()
							#print(basename)
							#print(check)
							if renmode != "force":
								if basename2.find(check) != -1:
									print('Filename: '+basename)
									print(tabs+"> File already has correct id: "+baseid)
									counter=int(counter)
									counter-=1
									if not args.text_file:
										print(tabs+'> Still '+str(counter)+' to go')
									continue
							if filepath.endswith('.xci') or filepath.endswith('.xcz'):
								f = Fs.Xci(basefile)
							elif filepath.endswith('.nsp') or filepath.endswith('.nsx') or filepath.endswith('.nsz'):
								f = Fs.Nsp(basefile)
							ctitl=f.get_title(baseid,roman)
							if addlangue==True:
								languetag=f.get_lang_tag(baseid)
								if languetag != False:
									ctitl=ctitl+' '+languetag
							#print(ctitl)
							#print(baseid)
							f.flush()
							f.close()
							if ctitl=='DLC' or ctitl=='-':
								ctitl=''
						elif updid !="":
							basename=str(os.path.basename(os.path.abspath(filepath)))
							basename2=basename.upper()
							check=str('['+updid+']').upper()
							if renmode != "force":
								if basename2.find(check) != -1:
									basename=os.path.basename(os.path.abspath(filepath))
									print('Filename: '+basename)
									print(tabs+"> File already has correct id: "+updid)
									counter=int(counter)
									counter-=1
									if not args.text_file:
										print(tabs+'> Still '+str(counter)+' to go')
									continue
							if filepath.endswith('.xci') or filepath.endswith('.xcz'):
								f = Fs.Xci(updfile)
							elif filepath.endswith('.nsp') or filepath.endswith('.nsx') or filepath.endswith('.nsz'):
								f = Fs.Nsp(updfile)
							ctitl=f.get_title(updid,roman)
							if addlangue==True:
								languetag=f.get_lang_tag(baseid)
								if languetag != False:
									ctitl=ctitl+' '+languetag
							#print(ctitl)
							#print(updid)
							f.flush()
							f.close()
							if ctitl=='DLC' or ctitl=='-':
								ctitl=''
						elif dlcid !="":
							basename=str(os.path.basename(os.path.abspath(filepath)))
							basename2=basename.upper()
							check=str('['+dlcid+']').upper()
							if renmode != "force":
								if basename2.find(check) != -1:
									print('Filename: '+basename)
									print(tabs+"> File already has correct id: "+dlcid)
									counter=int(counter)
									counter-=1
									if not args.text_file:
										print(tabs+'> Still '+str(counter)+' to go')
									continue
								else:
									if filepath.endswith('.xci') or filepath.endswith('.xcz'):
										f = Fs.Xci(dlcfile)
									elif filepath.endswith('.nsp') or filepath.endswith('.nsx') or filepath.endswith('.nsz'):
										f = Fs.Nsp(dlcfile)
									ctitl=f.get_title(dlcid,roman)
									f.flush()
									f.close()
							elif dlcrname == False or dlcrname == 'tag':
								nutdbname=nutdb.get_dlcname(dlcid)
								if nutdbname!=False:
									dlcname=nutdbname
								else:
									dlcname=str(os.path.basename(os.path.abspath(filepath)))
									tid1=list()
									tid2=list()
									tid1=[pos for pos, char in enumerate(filepath) if char == '[']
									tid2=[pos for pos, char in enumerate(filepath) if char == ']']
									if len(tid1)>=len(tid2):
										lentlist=len(tid1)
									elif len(tid1)<len(tid2):
										lentlist=len(tid2)
									for i in range(lentlist):
										i1=tid1[i]
										i2=tid2[i]+1
										t=filepath[i1:i2]
										dlcname=dlcname.replace(t,'')
										dlcname=dlcname.replace('  ',' ')
									tid3=[pos for pos, char in enumerate(dlcname) if char == '(']
									tid4=[pos for pos, char in enumerate(dlcname) if char == ')']
									if len(tid3)>=len(tid4):
										lentlist=len(tid3)
									elif len(tid3)<len(tid4):
										lentlist=len(tid4)
									for i in range(lentlist):
										i3=tid3[i]
										i4=tid4[i]+1
										t=dlcname[i3:i4]
										dlcname=dlcname.replace(t,'')
										dlcname=dlcname.replace('  ',' ')
									if dlcname.endswith('.xci') or dlcname.endswith('.nsp') or dlcname.endswith('.xcz') or dlcname.endswith('.nsz'):
										dlcname=dlcname[:-4]
									if dlcname.endswith(' '):
										dlcname=dlcname[:-1]
								ctitl=dlcname
								if dlcrname == 'tag':
									if filepath.endswith('.xci') or filepath.endswith('.xcz'):
										f = Fs.Xci(dlcfile)
									elif filepath.endswith('.nsp') or filepath.endswith('.nsx') or filepath.endswith('.nsz'):
										f = Fs.Nsp(dlcfile)
									dlctag=f.get_title(dlcid,tag=True)
									dlctag='['+dlctag+']'
									ctitl=ctitl+' '+dlctag
									f.flush()
									f.close()
							else:
								if filepath.endswith('.xci') or filepath.endswith('.xcz'):
									f = Fs.Xci(dlcfile)
								elif filepath.endswith('.nsp') or filepath.endswith('.nsx') or filepath.endswith('.nsz'):
									f = Fs.Nsp(dlcfile)
								ctitl=f.get_title(dlcid)
								f.flush()
								f.close()
						else:
							ctitl='UNKNOWN'
						baseid='['+baseid.upper()+']'
						updid='['+updid.upper()+']'
						dlcid='['+dlcid.upper()+']'
						if basecount>1:
							mgame='(mgame)'
						if ccount == '(1G)' or ccount == '(1U)' or ccount == '(1D)':
							ccount=''
						basename=str(os.path.basename(os.path.abspath(filepath)))
						if onaddid=='idtag':
							from pathlib import Path
							g=Path(basename).stem	
							try:
								g0=[pos for pos, char in enumerate(g) if char == '[']							
								ctitl=(g[0:g0[0]]).strip()	
							except:
								ctitl=g.strip()	
							if languetag!='':
								ctitl+=' '+languetag
							renmode="force"
							onaddid=False
						if baseid != "" and baseid != "[]":
							if updver != "":
								if onaddid==True:
									endname=basename[:-4]+' '+baseid
								elif nover == True and (ccount==''):
									endname=ctitl+' '+baseid
								else:
									endname=ctitl+' '+baseid+' '+updver+' '+ccount+' '+mgame
							else:
								if onaddid==True:
									endname=basename[:-4]+' '+baseid
								elif nover == True and (ccount==''):
									endname=ctitl+' '+baseid
								elif (filepath.endswith('.xci') or filepath.endswith('.xcz')) and nover=="xci_no_v0" and ccount=='':
									if renmode=="force":
										endname=ctitl+' '+baseid+' '+ccount+' '+mgame
									elif onaddid==True:
										endname=basename[:-4]+' '+baseid
									else:
										endname=ctitl+' '+baseid+' '+ccount+' '+mgame
								else:
									endname=ctitl+' '+baseid+' '+basever+' '+ccount+' '+mgame
						elif updid !="" and updid != "[]":
							if onaddid==True:
								endname=basename[:-4]+' '+updid
							elif nover == True and (ccount==''):
								endname=ctitl+' '+updid
							else:
								endname=ctitl+' '+updid+' '+updver+' '+ccount+' '+mgame
						else:
							if onaddid==True:
								endname=basename[:-4]+' '+dlcid
							elif nover == True and (ccount==''):
								endname=ctitl+' '+dlcid
							else:
								endname=ctitl+' '+dlcid+' '+dlcver+' '+ccount+' '+mgame
					while endname[-1]==' ':
						endname=endname[:-1]
					#endname = re.sub(r'[\/\\\:\*\?\"\<\>\|\.\s™©®()\~]+', ' ', endname)
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
						if endname.endswith(' '):
							endname=endname[:-1]
						if dlcrname == 'tag':
							endname = endname.replace('DLC number', 'DLC')
					except:pass
					if filepath.endswith('.xci'):
						endname=endname+'.xci'
					elif filepath.endswith('.xcz'):
						endname=endname+'.xcz'						
					elif filepath.endswith('.nsp'):
						endname=endname+'.nsp'
					elif filepath.endswith('.nsx'):
						endname=endname+'.nsx'
					elif filepath.endswith('.nsz'):
						endname=endname+'.nsz'						
					basename=str(os.path.basename(os.path.abspath(filepath)))
					dir=os.path.dirname(os.path.abspath(filepath))
					newpath=os.path.join(dir,endname)
					if os.path.exists(newpath) and newpath != filepath:
						if filepath.endswith('.xci'):
							endname=endname[:-4]+' (SeemsDuplicate)'+'.xci'
							newpath=os.path.join(dir,endname)
						elif filepath.endswith('.xcz'):
							endname=endname[:-4]+' (SeemsDuplicate)'+'.xcz'
							newpath=os.path.join(dir,endname)							
						elif filepath.endswith('.nsp'):
							endname=endname[:-4]+' (SeemsDuplicate)'+'.nsp'
							newpath=os.path.join(dir,endname)
						elif filepath.endswith('.nsx'):
							endname=endname[:-4]+' (SeemsDuplicate)'+'.nsx'
							newpath=os.path.join(dir,endname)
						elif filepath.endswith('.nsz'):
							endname=endname[:-4]+' (SeemsDuplicate)'+'.nsz'
							newpath=os.path.join(dir,endname)							
					if 	ctitl=='UNKNOWN':
						if filepath.endswith('.xci'):
							endname=basename[:-4]+' (needscheck)'+'.xci'
							newpath=os.path.join(dir,endname)
						elif filepath.endswith('.xcz'):
							endname=basename[:-4]+' (needscheck)'+'.xcz'
							newpath=os.path.join(dir,endname)							
						elif filepath.endswith('.nsp'):
							endname=basename[:-4]+' (needscheck)'+'.nsp'
							newpath=os.path.join(dir,endname)
						elif filepath.endswith('.nsx'):
							endname=basename[:-4]+' (needscheck)'+'.nsx'
							newpath=os.path.join(dir,endname)
						elif filepath.endswith('.nsz'):
							endname=basename[:-4]+' (needscheck)'+'.nsz'
							newpath=os.path.join(dir,endname)							
					print('Old Filename: '+basename)
					print('Filename: '+endname)
					os.rename(filepath, newpath)
					counter=int(counter)
					counter-=1
					print(tabs+'File was renamed')
					if not args.text_file:
						print(tabs+'> Still '+str(counter)+' to go')
			except BaseException as e:
				counter=int(counter)
				counter-=1
				Utils.logError(e)
			Status.close()
		# **********************
		# Rename using txt file
		# **********************
		if args.renameftxt:
			ruta=args.renameftxt
			if args.romanize:
				for input in args.romanize:
					roman=str(input).upper()
					if roman == "FALSE":
						roman = False
					else:
						roman = True
			else:
				roman = True
			if args.text_file:
				tfile=args.text_file
				filelist=list()
				tfile=args.text_file
				with open(tfile,"r+", encoding='utf8') as f:
					for line in f:
						fp=line.strip()
						filelist.append(fp)
				prlist=list()
				print ('Calculating final name:')
				for filepath in filelist:
					if filepath.endswith('.nsp'):
						#print(filepath)
						try:
							c=list()
							f = Fs.Nsp(filepath)
							contentlist=f.get_content(False,False,True)
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
										#print (contentlist[j][6])
										#pass
										if contentlist[j][1] == prlist[i][1]:
											if contentlist[j][6] > prlist[i][6]:
												del prlist[i]
												prlist.append(contentlist[j])
												notinlist=False
											elif contentlist[j][6] == prlist[i][6]:
												notinlist=False
										else:
											notinlist=True
									if notinlist == True:
										prlist.append(contentlist[j])
						except BaseException as e:
							Utils.logError(e)
					if filepath.endswith('.xci'):
						try:
							c=list()
							f = Fs.Xci(filepath)
							contentlist=f.get_content(False,False,True)
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
										#print (contentlist[j][6])
										#pass
										if contentlist[j][1] == prlist[i][1]:
											if contentlist[j][6] > prlist[i][6]:
												del prlist[i]
												prlist.append(contentlist[j])
												notinlist=False
											elif contentlist[j][6] == prlist[i][6]:
												notinlist=False
										else:
											notinlist=True
									if notinlist == True:
										prlist.append(contentlist[j])
						except BaseException as e:
							Utils.logError(e)
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
					if basefile.endswith('.xci'):
						f = Fs.Xci(basefile)
					elif basefile.endswith('.nsp'):
						f = Fs.Nsp(basefile)
					ctitl=f.get_title(baseid)
					f.flush()
					f.close()
					if ctitl=='DLC' or ctitl=='-':
						ctitl=''
				elif updid !="":
					if updfile.endswith('.xci'):
						f = Fs.Xci(updfile)
					elif updfile.endswith('.nsp'):
						f = Fs.Nsp(updfile)
					ctitl=f.get_title(updid)
					f.flush()
					f.close()
					if ctitl=='DLC' or ctitl=='-':
						ctitl=''
				elif dlcid !="":
					ctitl=f.get_title(dlcid)
					if dlcfile.endswith('.xci'):
						f = Fs.Xci(dlcfile)
					elif dlcfile.endswith('.nsp'):
						f = Fs.Nsp(dlcfile)
					ctitl=f.get_title(dlcid)
					f.flush()
					f.close()
				else:
					ctitl='UNKNOWN'
				baseid='['+baseid.upper()+']'
				updid='['+updid.upper()+']'
				dlcid='['+dlcid.upper()+']'
				if ccount == '(1G)' or ccount == '(1U)' or ccount == '(1D)':
					ccount=''
				if baseid != "[]":
					if updver != "":
						endname=ctitl+' '+baseid+' '+updver+' '+ccount
					else:
						endname=ctitl+' '+baseid+' '+basever+' '+ccount
				elif updid != "[]":
					endname=ctitl+' '+updid+' '+updver+' '+ccount
				else:
					endname=ctitl+' '+dlcid+' '+dlcver+' '+ccount
				#print('Filename: '+endname)
			else:
				endname=str(f)
			if rom == True:
				kakasi = pykakasi.kakasi()
				kakasi.setMode("H", "a")
				kakasi.setMode("K", "a")
				kakasi.setMode("J", "a")
				kakasi.setMode("s", True)
				kakasi.setMode("E", "a")
				kakasi.setMode("a", None)
				kakasi.setMode("C", False)
				converter = kakasi.getConverter()
				endname=converter.do(endname)
				endname=endname[0].upper()+endname[1:]
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
			ext=ruta[-4:]
			endname=endname+ext
			print('New name: '+endname)
			basename=str(os.path.basename(os.path.abspath(ruta)))
			dir=os.path.dirname(os.path.abspath(ruta))
			newpath=os.path.join(dir,endname)
			try:
				os.rename(ruta, newpath)
				print(tabs+'> File was renamed to: '+endname)
			except BaseException as e:
				pass
			Status.close()

		#parser.add_argument('-snz','--sanitize', help='Remove unreadable characters from names')
		#parser.add_argument('-roma','--romanize', help='Translate kanji and extended kanna to romaji and sanitize name')
		if not args.direct_multi and not args.fw_req and not args.renameftxt and not args.renamef and not args.Read_nacp and not args.addtodb and (args.sanitize or args.romanize):
			if args.sanitize:
				san=True; rom=False
				route=args.sanitize[0]
			elif args.romanize:
				san=True; rom=True
				route=args.romanize[0]
			else:
				route=False
			if route != False:
				if args.text_file and route == 'single':
					tfile=args.text_file
					with open(tfile,"r+", encoding='utf8') as filelist:
						ruta = filelist.readline()
						ruta=os.path.abspath(ruta.rstrip('\n'))
						ruta = os.path.abspath(ruta)
				else:
					ruta=route
				if ruta[-1]=='"':
					ruta=ruta[:-1]
				if ruta[0]=='"':
					ruta=ruta[1:]
				extlist=list()
				if args.type:
					for t in args.type:
						x='.'+t
						extlist.append(x)
						if x[-1]=='*':
							x=x[:-1]
							extlist.append(x)
				filelist=list()
				try:
					fname=""
					binbin='RECYCLE.BIN'
					for ext in extlist:
						#print (ext)
						if os.path.isdir(ruta):
							for dirpath, dirnames, filenames in os.walk(ruta):
								for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
									fname=""
									if args.filter:
										if filter.lower() in filename.lower():
											fname=filename
									else:
										fname=filename
									if fname != "":
										if binbin.lower() not in filename.lower():
											filelist.append(os.path.join(dirpath, filename))
						else:
							if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
								filename = ruta
								fname=""
								if args.filter:
									if filter.lower() in filename.lower():
										fname=filename
								else:
									fname=filename
								if fname != "":
									if binbin.lower() not in filename.lower():
										filelist.append(filename)
					print('Items to process: '+str(len(filelist)))
					counter=len(filelist)
					for filepath in filelist:
						basename=str(os.path.basename(os.path.abspath(filepath)))
						dir=os.path.dirname(os.path.abspath(filepath))
						print('Processing: '+filepath)
						endname=basename
						if rom == True:
							kakasi = pykakasi.kakasi()
							kakasi.setMode("H", "a")
							kakasi.setMode("K", "a")
							kakasi.setMode("J", "a")
							kakasi.setMode("s", True)
							kakasi.setMode("E", "a")
							kakasi.setMode("a", None)
							kakasi.setMode("C", False)
							converter = kakasi.getConverter()
							endname=converter.do(endname)
							endname=endname[0].upper()+endname[1:]
						if san == True:
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
						if endname[-5]==" ":
							endname=endname[:-5]+endname[-4:]
						newpath=os.path.join(dir,endname)
						print('Old Filename: '+basename)
						print('Filename: '+endname)
						os.rename(filepath, newpath)
						counter=int(counter)
						counter-=1
						print(tabs+'File was renamed')
						if not args.text_file:
							print(tabs+'> Still '+str(counter)+' to go')
				except BaseException as e:
					counter=int(counter)
					counter-=1
					Utils.logError(e)
			Status.close()
		# ...................................................
		# Verify. File verification
		# ...................................................	
		if args.verify_key:		
			orig_kg=False
			if isinstance(args.verify_key, list):
				filepath=args.verify_key[0]
				userkey=args.verify_key[1]
				# print(args.verify_key[2])
				try:
					if args.verify_key[2]:
						if str(args.verify_key[2]).lower()=="true":
							unlock=True
					else:
						unlock=False
				except:		
					unlock=False
				try:	
					if args.verify_key[3]:
						try:
							orig_kg=int(args.verify_key[3])
						except:
							orig_kg=False	
				except:
					orig_kg=False	
				userkey=str(userkey).upper()
				if filepath.endswith('.nsp') or filepath.endswith('.nsx'):
					basename=str(os.path.basename(os.path.abspath(filepath)))
					try:
						f = Fs.Nsp(filepath, 'rb')
						if orig_kg==False:
							check=f.verify_input_key(userkey)
						else:
							check,userkey=f.verify_input_key_m2(userkey,orig_kg)
						f.flush()
						f.close()
						if check==True:
							print(('\nTitlekey {} is correct for '.format(userkey)).upper()+('"{}"').format(basename))
							print("-- YOU CAN UNLOCK AND ENJOY THE GAME --")
							if unlock==True:
								print("--> UNLOCKING...")		
								f = Fs.Nsp(filepath, 'r+b')
								f.unlock(userkey)
								try:
									f.flush()
									f.close()	
								except:pass	
						else:
							print(('\nTitlekey {} is incorrect for '.format(userkey)).upper()+('"{}"').format(basename))
							print("-- BETTER LUCK NEXT TIME --")	
					except BaseException as e:
						Utils.logError(e)
			else:
				print('Missing arguments')
	
		if args.verify:
			feed=''
			if args.vertype:
				if args.vertype=="dec" or args.vertype=="lv1":
					vertype="lv1"
				elif args.vertype=="sig" or args.vertype=="lv2":
					vertype="lv2"
				elif args.vertype=="sig" or args.vertype=="lv3":
					vertype="lv3"
				else:
					vertype="lv1"
			else:
				vertype="lv1"
			if args.buffer:
				for var in args.buffer:
					try:
						buffer = var
					except BaseException as e:
						Utils.logError(e)
			else:
				buffer = 65536
			if args.ofolder:
				for var in args.ofolder:
					try:
						ofolder = var
						tmpfolder =os.path.join(ofolder,'tmp')
					except BaseException as e:
						Utils.logError(e)
			else:
				for filename in args.verify:
					dir=os.path.dirname(os.path.abspath(filename))
					info='INFO'
					ofolder =os.path.join(dir,info)
					tmpfolder =os.path.join(dir,'tmp')
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
				for filename in args.verify:
					filename=filename
			basename=str(os.path.basename(os.path.abspath(filename)))
			ofile=basename[:-4]+'-verify.txt'
			infotext=os.path.join(ofolder, ofile)
			if filename.endswith('.nsp') or filename.endswith('.nsx'):
				try:
					f = Fs.Nsp(filename, 'rb')
					check,feed=f.verify()
					f.flush()
					f.close()
					if not args.text_file:
						f = Fs.Nsp(filename, 'rb')
						verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
						f.flush()
						f.close()
						i=0
						print('\n********************************************************')
						print('Do you want to verify the hash of the nca files?')
						print('********************************************************')
						while i==0:
							print('Input "1" to VERIFY hash of files')
							print('Input "2" to NOT verify hash  of files\n')
							ck=input('Input your answer: ')
							if ck ==str(1):
								print('')
								f = Fs.Nsp(filename, 'rb')
								verdict,feed=f.verify_hash_nca(buffer,headerlist,verdict,feed)
								f.flush()
								f.close()
								i=1
							elif ck ==str(2):
								f.flush()
								f.close()
								i=1
							else:
								print('WRONG CHOICE\n')
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
					elif args.text_file:
						if vertype == "lv2":
							f = Fs.Nsp(filename, 'rb')
							verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
							f.flush()
							f.close()
							if check == True:
								check=verdict
						elif vertype == "lv3":
							f = Fs.Nsp(filename, 'rb')
							verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
							f.flush()
							f.close()
							if check == True:
								check=verdict
							f = Fs.Nsp(filename, 'rb')
							verdict,feed=f.verify_hash_nca(buffer,headerlist,verdict,feed)
							f.flush()
							f.close()
							if check == True:
								check=verdict
						if check == False:
							with open(errfile, 'a') as errfile:
								now=datetime.now()
								date=now.strftime("%x")+". "+now.strftime("%X")
								errfile.write(date+'\n')
								errfile.write("Filename: "+str(filename)+'\n')
								errfile.write("IS INCORRECT"+'\n')
						dir=os.path.dirname(os.path.abspath(tfile))
						info='INFO'
						subf='MASSVERIFY'
						ofolder =os.path.join(dir,info)
						if not os.path.exists(ofolder):
							os.makedirs(ofolder)
						ofolder =os.path.join(ofolder,subf)
						if not os.path.exists(ofolder):
							os.makedirs(ofolder)
						infotext=os.path.join(ofolder, ofile)
						with open(infotext, 'w') as info:
							info.write(feed)
				except BaseException as e:
					Utils.logError(e)
					if args.text_file:
						with open(errfile, 'a') as errfile:
							now=datetime.now()
							date=now.strftime("%x")+". "+now.strftime("%X")
							errfile.write(date+'\n')
							errfile.write("Filename: "+str(filename)+'\n')
							errfile.write('Exception: ' + str(e)+'\n')
			if filename.endswith('.xci'):
				try:
					f = Fs.factory(filename)
					f.open(filename, 'rb')
					check,feed=f.verify()
					f.flush()
					f.close()
					if not args.text_file:
						f = Fs.factory(filename)
						f.open(filename, 'rb')
						verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
						f.flush()
						f.close()
						i=0
						print('\n********************************************************')
						print('Do you want to verify the hash of the nca files?')
						print('********************************************************')
						while i==0:
							print('Input "1" to VERIFY hash of files')
							print('Input "2" to NOT verify hash  of files\n')
							check=input('Input your answer: ')
							if check ==str(1):
								print('')
								f = Fs.factory(filename)
								f.open(filename, 'rb')
								verdict,feed=f.verify_hash_nca(buffer,headerlist,verdict,feed)
								f.flush()
								f.close()
								i=1
							elif check ==str(2):
								f.flush()
								f.close()
								i=1
							else:
								print('WRONG CHOICE\n')
						print('\n********************************************************')
						print('Do you want to print the information to a text file')
						print('********************************************************')
						i=0
						while i==0:
							print('Input "1" to print to text file')
							print('Input "2" to NOT print to text file\n')
							check=input('Input your answer: ')
							if check ==str(1):
								with open(infotext, 'w') as info:
									info.write(feed)
								i=1
							elif check ==str(2):
								i=1
							else:
								print('WRONG CHOICE\n')
					elif args.text_file:
						if vertype == "lv2":
							f = Fs.factory(filename)
							f.open(filename, 'rb')
							verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
							f.flush()
							f.close()
							if check == True:
								check=verdict
						elif vertype == "lv3":
							f = Fs.factory(filename)
							f.open(filename, 'rb')
							verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
							f.flush()
							f.close()
							if check == True:
								check=verdict
							f = Fs.factory(filename)
							f.open(filename, 'rb')
							verdict,feed=f.verify_hash_nca(buffer,headerlist,verdict,feed)
							f.flush()
							f.close()
							if check == True:
								check=verdict
						if check == False:
							with open(errfile, 'a') as errfile:
								now=datetime.now()
								date=now.strftime("%x")+". "+now.strftime("%X")
								errfile.write(date+'\n')
								errfile.write("Filename: "+str(filename)+'\n')
								errfile.write("IS INCORRECT"+'\n')
						dir=os.path.dirname(os.path.abspath(tfile))
						info='INFO'
						subf='MASSVERIFY'
						ofolder =os.path.join(dir,info)
						if not os.path.exists(ofolder):
							os.makedirs(ofolder)
						ofolder =os.path.join(ofolder,subf)
						if not os.path.exists(ofolder):
							os.makedirs(ofolder)
						infotext=os.path.join(ofolder, ofile)
						with open(infotext, 'w') as info:
							info.write(feed)
				except BaseException as e:
					Utils.logError(e)
					if args.text_file:
						with open(errfile, 'a') as errfile:
							now=datetime.now()
							date=now.strftime("%x")+". "+now.strftime("%X")
							errfile.write(date+'\n')
							errfile.write("Filename: "+str(filename)+'\n')
							errfile.write('Exception: ' + str(e)+'\n')
			if filename.endswith('.nsz'):
				try:
					f = Fs.Nsp(filename, 'rb')
					check,feed=f.verify()
					f.flush()
					f.close()
					if not args.text_file:
						f = Fs.Nsp(filename, 'rb')
						verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
						f.flush()
						f.close()
						i=0
						print('\n********************************************************')
						print('Do you want to verify the hash of the nca files?')
						print('********************************************************')
						while i==0:
							print('Input "1" to VERIFY hash of files')
							print('Input "2" to NOT verify hash  of files\n')
							ck=input('Input your answer: ')
							if ck ==str(1):
								print('')
								f = Fs.Nsp(filename, 'rb')
								verdict,feed=f.nsz_hasher(buffer,headerlist,verdict,feed)
								f.flush()
								f.close()
								i=1
							elif ck ==str(2):
								f.flush()
								f.close()
								i=1
							else:
								print('WRONG CHOICE\n')
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
					elif args.text_file:
						if vertype == "lv2":
							f = Fs.Nsp(filename, 'rb')
							verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
							f.flush()
							f.close()
							if check == True:
								check=verdict
						elif vertype == "lv3":
							f = Fs.Nsp(filename, 'rb')
							verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
							f.flush()
							f.close()
							if check == True:
								check=verdict
							f = Fs.Nsp(filename, 'rb')
							verdict,feed=f.nsz_hasher(buffer,headerlist,verdict,feed)
							f.flush()
							f.close()
							if check == True:
								check=verdict
						if check == False:
							with open(errfile, 'a') as errfile:
								now=datetime.now()
								date=now.strftime("%x")+". "+now.strftime("%X")
								errfile.write(date+'\n')
								errfile.write("Filename: "+str(filename)+'\n')
								errfile.write("IS INCORRECT"+'\n')
						dir=os.path.dirname(os.path.abspath(tfile))
						info='INFO'
						subf='MASSVERIFY'
						ofolder =os.path.join(dir,info)
						if not os.path.exists(ofolder):
							os.makedirs(ofolder)
						ofolder =os.path.join(ofolder,subf)
						if not os.path.exists(ofolder):
							os.makedirs(ofolder)
						infotext=os.path.join(ofolder, ofile)
						with open(infotext, 'w') as info:
							info.write(feed)
				except BaseException as e:
					Utils.logError(e)
					if args.text_file:
						with open(errfile, 'a') as errfile:
							now=datetime.now()
							date=now.strftime("%x")+". "+now.strftime("%X")
							errfile.write(date+'\n')
							errfile.write("Filename: "+str(filename)+'\n')
							errfile.write('Exception: ' + str(e)+'\n')		
			if filename.endswith('.xcz'):
				try:
					f = Fs.Xci(filename)
					check,feed=f.verify()
					f.flush()
					f.close()
					if not args.text_file:
						f = Fs.Xci(filename)
						verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
						f.flush()
						f.close()
						i=0
						print('\n********************************************************')
						print('Do you want to verify the hash of the nca files?')
						print('********************************************************')
						while i==0:
							print('Input "1" to VERIFY hash of files')
							print('Input "2" to NOT verify hash  of files\n')
							ck=input('Input your answer: ')
							if ck ==str(1):
								print('')
								f = Fs.Xci(filename)
								verdict,feed=f.xcz_hasher(buffer,headerlist,verdict,feed)
								f.flush()
								f.close()
								i=1
							elif ck ==str(2):
								f.flush()
								f.close()
								i=1
							else:
								print('WRONG CHOICE\n')
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
					elif args.text_file:
						if vertype == "lv2":
							f = Fs.Xci(filename)
							verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
							f.flush()
							f.close()
							if check == True:
								check=verdict
						elif vertype == "lv3":
							f = Fs.Xci(filename)
							verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
							f.flush()
							f.close()
							if check == True:
								check=verdict
							f = Fs.Xci(filename)
							verdict,feed=f.xcz_hasher(buffer,headerlist,verdict,feed)
							f.flush()
							f.close()
							if check == True:
								check=verdict
						if check == False:
							with open(errfile, 'a') as errfile:
								now=datetime.now()
								date=now.strftime("%x")+". "+now.strftime("%X")
								errfile.write(date+'\n')
								errfile.write("Filename: "+str(filename)+'\n')
								errfile.write("IS INCORRECT"+'\n')
						dir=os.path.dirname(os.path.abspath(tfile))
						info='INFO'
						subf='MASSVERIFY'
						ofolder =os.path.join(dir,info)
						if not os.path.exists(ofolder):
							os.makedirs(ofolder)
						ofolder =os.path.join(ofolder,subf)
						if not os.path.exists(ofolder):
							os.makedirs(ofolder)
						infotext=os.path.join(ofolder, ofile)
						with open(infotext, 'w') as info:
							info.write(feed)
				except BaseException as e:
					Utils.logError(e)
					if args.text_file:
						with open(errfile, 'a') as errfile:
							now=datetime.now()
							date=now.strftime("%x")+". "+now.strftime("%X")
							errfile.write(date+'\n')
							errfile.write("Filename: "+str(filename)+'\n')
							errfile.write('Exception: ' + str(e)+'\n')								
			if filename.endswith('.nca'):
				try:
					f = Fs.Nca(filename, 'rb')
					ver_,origheader,ncaname,feed,currkg,tr,tkey,iGC=f.verify(False)
					f.flush()
					f.close()
					if not args.text_file:
						i=0
						print('\n********************************************************')
						print('Do you want to verify the hash of the nca files?')
						print('********************************************************')
						while i==0:
							print('Input "1" to VERIFY hash of files')
							print('Input "2" to NOT verify hash  of files\n')
							check=input('Input your answer: ')
							if check ==str(1):
								print('')
								f = Fs.Nca(filename, 'rb')
								verdict,feed=f.verify_hash_nca(buffer,origheader,ver_,feed)
								f.flush()
								f.close()
								i=1
							elif check ==str(2):
								i=1
							else:
								print('WRONG CHOICE\n')
						print('\n********************************************************')
						print('Do you want to print the information to a text file')
						print('********************************************************')
						i=0
						while i==0:
							print('Input "1" to print to text file')
							print('Input "2" to NOT print to text file\n')
							check=input('Input your answer: ')
							if check ==str(1):
								with open(infotext, 'w') as info:
									info.write(feed)
								i=1
							elif check ==str(2):
								i=1
							else:
								print('WRONG CHOICE\n')
					if args.text_file:
						f = Fs.Nca(filename, 'rb')
						verdict,feed=f.verify_hash_nca(buffer,origheader,ver_,feed)
						f.flush()
						f.close()
						if ver_ == True:
							ver_=verdict
						if ver_ == False:
							with open(errfile, 'a') as errfile:
								now=datetime.now()
								date=now.strftime("%x")+". "+now.strftime("%X")
								errfile.write(date+'\n')
								errfile.write("Filename: "+str(filename)+'\n')
								errfile.write("IS INCORRECT"+'\n')
						dir=os.path.dirname(os.path.abspath(tfile))
						info='INFO'
						subf='MASSVERIFY'
						ofolder =os.path.join(dir,info)
						if not os.path.exists(ofolder):
							os.makedirs(ofolder)
						ofolder =os.path.join(ofolder,subf)
						if not os.path.exists(ofolder):
							os.makedirs(ofolder)
						infotext=os.path.join(ofolder, ofile)
						with open(infotext, 'w') as info:
							info.write(feed)
				except BaseException as e:
					Utils.logError(e)
					if args.text_file:
						with open(errfile, 'a') as errfile:
							now=datetime.now()
							date=now.strftime("%x")+". "+now.strftime("%X")
							errfile.write(date+'\n')
							errfile.write("Filename: "+str(filename)+'\n')
							errfile.write('Exception: ' + str(e)+'\n')
			Status.close()

		#split_list_by_id
		if args.split_list_by_id:
			for filepath in args.split_list_by_id:
				ofolder=os.path.abspath(filepath)
				if not os.path.exists(ofolder):
					os.makedirs(ofolder)
			baselist=list()
			addonlist=list()
			updlist=list()
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
			print('- Calculating base-ids for:')
			for filepath in filelist:
				try:
					if filepath.endswith('.nsp') or filepath.endswith('.nsz')  or filepath.endswith('.nsx') :
						f = Fs.Nsp(filepath)
					elif filepath.endswith('.xci') or filepath.endswith('.xcz') :
						f = Fs.factory(filepath)
						f.open(filepath, 'rb')
					print(tabs+filepath)
					validator,contentlist=f.cnmt_get_baseids()
					f.flush()
					f.close()
					if validator=='base':
						baselist.append([filepath,contentlist])
					elif validator=='update':
						updlist.append([filepath,contentlist])
					else:
						addonlist.append([filepath,contentlist])
				except BaseException as e:
					Utils.logError(e)
			'''
			print('Baselist')
			for i in baselist:
				print(i)
			print(str(len(baselist)))
			print('Updlist')
			for i in updlist:
				print(i)
			print(str(len(updlist)))
			print('Addonlist')
			for i in addonlist:
				print(i)
			print(str(len(addonlist)))
			'''

			print('')
			print('- Generating lists:')
			if len(baselist)>0:
				for i in range(len(baselist)):
					lname=''
					fileslist=list()
					idlist=baselist[i][1]
					for k in idlist:
						lname+='['+k+']'
					lname=lname.upper()
					lname+='.txt'
					fileslist.append(baselist[i][0])
					for j in range(len(updlist)):
						addid=updlist[j][1]
						addid=addid[0]
						if addid in idlist:
							if updlist[j][0] not in fileslist:
								fileslist.append(updlist[j][0])
					for j in range(len(addonlist)):
						addid=addonlist[j][1]
						addid=addid[0]
						if addid in idlist:
							if addonlist[j][0] not in fileslist:
								fileslist.append(addonlist[j][0])
					endfile=os.path.join(ofolder, lname)
					print('  > '+endfile)
					with open(endfile,"w", encoding='utf8') as tfile:
						for line in fileslist:
							try:
								print(tabs+line)
								tfile.write(line+"\n")
							except:
								continue
			elif len(updlist)>0:
				for i in range(len(updlist)):
					lname=''
					fileslist=list()
					idlist=updlist[i][1]
					for k in idlist:
						k=k[:-3]+'800'
						lname+='['+k+']'
					lname=lname.upper()
					lname+='.txt'
					fileslist.append(updlist[i][0])
					for j in range(len(addonlist)):
						addid=addonlist[j][1]
						addid=addid[0]
						if addid in idlist:
							if addonlist[j][0] not in fileslist:
								fileslist.append(addonlist[j][0])
					endfile=os.path.join(ofolder, lname)
					print('  > '+endfile)
					with open(endfile,"w", encoding='utf8') as tfile:
						for line in fileslist:
							try:
								print(tabs+line)
								tfile.write(line+"\n")
							except:
								continue
			elif len(addonlist)>0:
				for i in range(len(addonlist)):
					lname=''
					fileslist=list()
					idlist=addonlist[i][1]
					for k in idlist:
						lname+='['+k+']'
					lname=lname.upper()
					lname+='.txt'
					fileslist.append(addonlist[i][0])
					endfile=os.path.join(ofolder, lname)
					print('  > '+endfile)
					with open(endfile,"w", encoding='utf8') as tfile:
						for line in fileslist:
							try:
								print(tabs+line)
								tfile.write(line+"\n")
							except:
								continue
			Status.close()

		#--------------------------
		#Print list of old updates
		#--------------------------

		#parser.add_argument('-mv_oupd', '--mv_old_updates', nargs='+', help='Moves old updates to another folder')
		if args.mv_old_updates:
			if args.ofolder:
				for input in args.ofolder:
					try:
						ofolder = input
					except BaseException as e:
						Utils.logError(e)
			else:
				for filepath in args.mv_old_updates:
					ofolder=os.path.abspath(filepath)
					ofolder=os.path.join(ofolder, 'old')
			if not os.path.exists(ofolder):
				os.makedirs(ofolder)
			duplicates_f=os.path.join(ofolder, 'duplicates')
			if not os.path.exists(duplicates_f):
				os.makedirs(duplicates_f)
			baselist=list()
			addonlist=list()
			updlist=list();updtomove=list()
			filelist=list()
			if args.text_file:
				tfile=args.text_file
				tfile=args.text_file
				with open(tfile,"r+", encoding='utf8') as f:
					for line in f:
						fp=line.strip()
						filelist.append(fp)
			else:
				ruta=args.mv_old_updates[0]
				if ruta[-1]=='"':
					ruta=ruta[:-1]
				if ruta[0]=='"':
					ruta=ruta[1:]
				extlist=list()
				extlist.append('.nsp')
				extlist.append('.nsz')				
				if args.filter:
					for f in args.filter:
						filter=f
				try:
					fname=""
					binbin='RECYCLE.BIN'
					for ext in extlist:
						#print (ext)
						#print (ruta)
						if os.path.isdir(ruta):
							for dirpath, dirnames, filenames in os.walk(ruta):
								for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
									fname=""
									if args.filter:
										if filter.lower() in filename.lower():
											fname=filename
									else:
										fname=filename
										#print(fname)
									if fname != "":
										if binbin.lower() not in filename.lower():
											filelist.append(os.path.join(dirpath, filename))
						else:
							if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
								filename = ruta
								#print(ruta)
								fname=""
								if args.filter:
									if filter.lower() in filename.lower():
										fname=filename
								else:
									fname=filename
								if fname != "":
									if binbin.lower() not in filename.lower():
										filelist.append(filename)
				except BaseException as e:
					Utils.logError(e)
					pass
				'''
				for file in filelist:
					print(file)
					pass
				'''
				Datashelve = dbmodule.Dict('File01.dshlv');c=0
				for filepath in filelist:
					fileid='unknown';fileversion='unknown';cctag='unknown'
					tid1=list()
					tid2=list()
					tid1=[pos for pos, char in enumerate(filepath) if char == '[']
					tid2=[pos for pos, char in enumerate(filepath) if char == ']']
					if len(tid1)>=len(tid2):
						lentlist=len(tid1)
					elif len(tid1)<len(tid2):
						lentlist=len(tid2)
					for i in range(lentlist):
						try:
							i1=tid1[i]+1
							i2=tid2[i]
							t=filepath[i1:i2]
							#print(t)
							if len(t)==16:
								try:
									test1=filepath[i1:i2]
									int(filepath[i1:i2], 16)
									fileid=str(filepath[i1:i2]).upper()
									if fileid !='unknown':
										if int(fileid[-3:])==800:
											cctag='UPD'
										elif int(fileid[-3:])==000:
											cctag='BASE'
										else:
											try:
												int(fileid[-3:])
												cctag='DLC'
											except:pass
										break
								except:
									continue
						except:pass
					for i in range(lentlist):
						try:
							i1=tid1[i]+1
							i2=tid2[i]
						except:pass
						if (str(filepath[(i1)]).upper())=='V':
							try:
								test2=filepath[(i1+1):i2]
								fileversion=int(filepath[(i1+1):i2])
								if fileversion !='unknown':
									break
							except:
								continue

					#print(fileid+' '+str(fileversion)+' '+cctag)
					if fileid == 'unknown' or fileversion == 'unknown':
						print(fileid+' '+str(fileversion))
						print(str(os.path.basename(os.path.abspath(filepath))))
						print(test1)
						print(test2)

					if cctag!="UPD":
						print(str(os.path.basename(os.path.abspath(filepath))))

					if c==0:
						c+=1
						try:
							Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
						except BaseException as e:
							Utils.logError(e)
					else:
						try:
							if str(fileid) in Datashelve:
								shelvedfile=Datashelve[str(fileid)]
								#print(shelvedfile[2])
								if shelvedfile[1]==fileid:
									if int(shelvedfile[2])>int(fileversion):
										print(str(os.path.basename(os.path.abspath(filepath))))
										checker=os.path.join(ofolder, str(os.path.basename(os.path.abspath(filepath))))
										if not os.path.isfile(checker):
											shutil.move(filepath,ofolder)
										else:
											try:
												os.remove(filepath)
											except:pass
										Datashelve[str(fileid)]=shelvedfile
									elif int(shelvedfile[2])== int(fileversion):
										print(str(os.path.basename(os.path.abspath(filepath))))
										checker=os.path.join(ofolder, str(os.path.basename(os.path.abspath(filepath))))
										if not os.path.isfile(checker):
											shutil.move(filepath,duplicates_f)
										else:
											try:
												os.remove(filepath)
											except:pass
										Datashelve[str(fileid)]=shelvedfile
									else:
										print(str(os.path.basename(os.path.abspath(shelvedfile[0]))))
										checker=os.path.join(ofolder, str(os.path.basename(os.path.abspath(shelvedfile[0]))))
										if not os.path.isfile(checker):
											shutil.move(shelvedfile[0],ofolder)
										else:
											try:
												os.remove(filepath)
											except:pass
										Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
								else:
									pass
							else:
								Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
						except BaseException as e:
							Utils.logError(e)
				Datashelve.close()
				try:os.remove('File01.dshlv')
				except:pass
			Status.close()

		#parser.add_argument('-mv_odlc', '--mv_old_dlcs', nargs='+', help='Moves old dlcs to another folder')
		if args.mv_old_dlcs:
			if args.ofolder:
				for input in args.ofolder:
					try:
						ofolder = input
					except BaseException as e:
						Utils.logError(e)
			else:
				for filepath in args.mv_old_dlcs:
					ofolder=os.path.abspath(filepath)
					ofolder=os.path.join(ofolder, 'old')
			if not os.path.exists(ofolder):
				os.makedirs(ofolder)
			duplicates_f=os.path.join(ofolder, 'duplicates')
			if not os.path.exists(duplicates_f):
				os.makedirs(duplicates_f)
			baselist=list()
			addonlist=list()
			updlist=list();updtomove=list()
			filelist=list()
			if args.text_file:
				tfile=args.text_file
				with open(tfile,"r+", encoding='utf8') as f:
					for line in f:
						fp=line.strip()
						filelist.append(fp)
			else:
				ruta=args.mv_old_dlcs[0]
				if ruta[-1]=='"':
					ruta=ruta[:-1]
				if ruta[0]=='"':
					ruta=ruta[1:]
				extlist=list()
				extlist.append('.nsp')
				extlist.append('.nsz')				
				if args.filter:
					for f in args.filter:
						filter=f
				try:
					fname=""
					binbin='RECYCLE.BIN'
					for ext in extlist:
						#print (ext)
						#print (ruta)
						if os.path.isdir(ruta):
							for dirpath, dirnames, filenames in os.walk(ruta):
								for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
									fname=""
									if args.filter:
										if filter.lower() in filename.lower():
											fname=filename
									else:
										fname=filename
										#print(fname)
									if fname != "":
										if binbin.lower() not in filename.lower():
											filelist.append(os.path.join(dirpath, filename))
						else:
							if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
								filename = ruta
								#print(ruta)
								fname=""
								if args.filter:
									if filter.lower() in filename.lower():
										fname=filename
								else:
									fname=filename
								if fname != "":
									if binbin.lower() not in filename.lower():
										filelist.append(filename)
				except BaseException as e:
					Utils.logError(e)
					pass
				'''
				for file in filelist:
					print(file)
					pass
				'''
				Datashelve = dbmodule.Dict('File01.dshlv');c=0
				for filepath in filelist:
					fileid='unknown';fileversion='unknown';cctag='unknown'
					tid1=list()
					tid2=list()
					tid1=[pos for pos, char in enumerate(filepath) if char == '[']
					tid2=[pos for pos, char in enumerate(filepath) if char == ']']
					if len(tid1)>=len(tid2):
						lentlist=len(tid1)
					elif len(tid1)<len(tid2):
						lentlist=len(tid2)
					for i in range(lentlist):
						try:
							i1=tid1[i]+1
							i2=tid2[i]
							t=filepath[i1:i2]
							#print(t)
							if len(t)==16:
								try:
									test1=filepath[i1:i2]
									int(filepath[i1:i2], 16)
									fileid=str(filepath[i1:i2]).upper()
									if fileid !='unknown':
										if int(fileid[-3:])==800:
											cctag='UPD'
										elif int(fileid[-3:])==000:
											cctag='BASE'
										else:
											try:
												int(fileid[-3:])
												cctag='DLC'
											except:pass
										break
								except:
									try:
										fileid=str(filepath[i1:i2]).upper()
										if str(fileid[-3:])!='800' or str(fileid[-3:])!='000':
											DLCnumb=str(fileid)
											DLCnumb="0000000000000"+DLCnumb[-3:]
											DLCnumb=bytes.fromhex(DLCnumb)
											DLCnumb=str(int.from_bytes(DLCnumb, byteorder='big'))
											DLCnumb=int(DLCnumb)
											cctag='DLC'
									except:continue
						except:pass
					for i in range(lentlist):
						try:
							i1=tid1[i]+1
							i2=tid2[i]
						except:pass
						if (str(filepath[(i1)]).upper())=='V':
							try:
								test2=filepath[(i1+1):i2]
								fileversion=int(filepath[(i1+1):i2])
								if fileversion !='unknown':
									break
							except:
								continue

					#print(fileid+' '+str(fileversion)+' '+cctag)
					if fileid == 'unknown' or fileversion == 'unknown':
						print(fileid+' '+str(fileversion))
						print(str(os.path.basename(os.path.abspath(filepath))))
						print(test1)
						print(test2)

					if cctag!="DLC":
						print(str(os.path.basename(os.path.abspath(filepath))))

					if c==0:
						c+=1
						try:
							Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
						except BaseException as e:
							Utils.logError(e)
					else:
						try:
							if str(fileid) in Datashelve:
								shelvedfile=Datashelve[str(fileid)]
								#print(shelvedfile[2])
								if shelvedfile[1]==fileid:
									if int(shelvedfile[2])>int(fileversion):
										print(str(os.path.basename(os.path.abspath(filepath))))
										checker=os.path.join(ofolder, str(os.path.basename(os.path.abspath(filepath))))
										if not os.path.isfile(checker):
											shutil.move(filepath,ofolder)
										else:
											try:
												os.remove(filepath)
											except:pass
										Datashelve[str(fileid)]=shelvedfile
									elif int(shelvedfile[2])== int(fileversion):
										print(str(os.path.basename(os.path.abspath(filepath))))
										checker=os.path.join(ofolder, str(os.path.basename(os.path.abspath(filepath))))
										if not os.path.isfile(checker):
											shutil.move(filepath,duplicates_f)
										else:
											try:
												os.remove(filepath)
											except:pass
										Datashelve[str(fileid)]=shelvedfile
									else:
										print(str(os.path.basename(os.path.abspath(shelvedfile[0]))))
										checker=os.path.join(ofolder, str(os.path.basename(os.path.abspath(shelvedfile[0]))))
										if not os.path.isfile(checker):
											shutil.move(shelvedfile[0],ofolder)
										else:
											try:
												os.remove(filepath)
											except:pass
										Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
								else:
									pass
							else:
								Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
						except BaseException as e:
							Utils.logError(e)
				Datashelve.close()
				try:os.remove('File01.dshlv')
				except:pass
			Status.close()

		#parser.add_argument('-cr_ilist', '--cr_incl_list', nargs='+', help='Creates a include list from a textfile and a folder')
		#parser.add_argument('-tfile_aux', '--text_file_aux', help='Auxiliary text file')
		if args.cr_incl_list:
			# if args.ofolder:
				# for input in args.ofolder:
					# try:
						# ofolder = input
					# except BaseException as e:
						# Utils.logError(e)
			# else:
				# for filepath in args.cr_incl_list:
					# ofolder=os.path.abspath(filepath)
					# ofolder=os.path.join(ofolder, 'old')
			# if not os.path.exists(ofolder):
				# os.makedirs(ofolder)
			# duplicates_f=os.path.join(ofolder, 'duplicates')
			# if not os.path.exists(duplicates_f):
				# os.makedirs(duplicates_f)
			if args.fexport:
				for input in args.fexport:
					try:
						exportlist = input
					except BaseException as e:
						Utils.logError(e)
			baselist=list()
			addonlist=list()
			updlist=list();updtomove=list()
			filelist=list()
			if args.text_file:
				tfile=args.text_file
				with open(tfile,"r+", encoding='utf8') as f:
					for line in f:
						fp=line.strip()
						filelist.append(fp)
			if args.text_file_aux:
				filelist2=list()
				tfile2=args.text_file_aux
				with open(tfile2,"r+", encoding='utf8') as f:
					for line in f:
						fp=line.strip()
						filelist2.append(fp)
			else:
				filelist2=list()
				ruta=args.cr_incl_list[0]
				if ruta[-1]=='"':
					ruta=ruta[:-1]
				if ruta[0]=='"':
					ruta=ruta[1:]
				extlist=list()
				extlist.append('.nsp')
				extlist.append('.nsz')				
				extlist.append('.xci')
				extlist.append('.xcz')				
				if args.filter:
					for f in args.filter:
						filter=f
				#print(ruta)
				try:
					fname=""
					binbin='RECYCLE.BIN'
					for ext in extlist:
						#print (ext)
						#print (ruta)
						if os.path.isdir(ruta):
							for dirpath, dirnames, filenames in os.walk(ruta):
								for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
									fname=""
									if args.filter:
										if filter.lower() in filename.lower():
											fname=filename
									else:
										fname=filename
										#print(fname)
									if fname != "":
										if binbin.lower() not in filename.lower():
											filelist2.append(os.path.join(dirpath, filename))
						else:
							if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
								filename = ruta
								#print(ruta)
								fname=""
								if args.filter:
									if filter.lower() in filename.lower():
										fname=filename
								else:
									fname=filename
								if fname != "":
									if binbin.lower() not in filename.lower():
										filelist2.append(filename)
				except BaseException as e:
					Utils.logError(e)
					pass
			'''
			for file in filelist2:
				print(file)
				pass
			'''
			test2="";test=""
			Datashelve = dbmodule.Dict('File01.dshlv');c=0
			for filepath in filelist2:
				fileid='unknown';fileversion='unknown';cctag='unknown'
				tid1=list()
				tid2=list()
				tid1=[pos for pos, char in enumerate(filepath) if char == '[']
				tid2=[pos for pos, char in enumerate(filepath) if char == ']']
				if len(tid1)>=len(tid2):
					lentlist=len(tid1)
				elif len(tid1)<len(tid2):
					lentlist=len(tid2)
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
						t=filepath[i1:i2]
						#print(t)
						if len(t)==16:
							try:
								test1=filepath[i1:i2]
								int(filepath[i1:i2], 16)
								fileid=str(filepath[i1:i2]).upper()
								if fileid !='unknown':
									if int(fileid[-3:])==800:
										cctag='UPD'
									elif int(fileid[-3:])==000:
										cctag='BASE'
									else:
										try:
											int(fileid[-3:])
											cctag='DLC'
										except:pass
									break
							except:
								try:
									fileid=str(filepath[i1:i2]).upper()
									if str(fileid[-3:])!='800' or str(fileid[-3:])!='000':
										DLCnumb=str(fileid)
										DLCnumb="0000000000000"+DLCnumb[-3:]
										DLCnumb=bytes.fromhex(DLCnumb)
										DLCnumb=str(int.from_bytes(DLCnumb, byteorder='big'))
										DLCnumb=int(DLCnumb)
										cctag='DLC'
								except:continue
					except:pass
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
					except:pass
					if (str(filepath[(i1)]).upper())=='V':
						try:
							test2=filepath[(i1+1):i2]
							fileversion=int(filepath[(i1+1):i2])
							#print(fileversion)
							if fileversion !='unknown':
								break
						except:
							continue

				#print(fileid+' '+str(fileversion)+' '+cctag)
				if fileid == 'unknown' or fileversion == 'unknown':
					print(fileid+' '+str(fileversion))
					print(str(os.path.basename(os.path.abspath(filepath))))
					print(test1)
					print(test2)

				if cctag!="DLC" and cctag!="BASE" and cctag!="UPD":
					print(str(os.path.basename(os.path.abspath(filepath))))
				if c==0:
					c+=1
					try:
						Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
					except BaseException as e:
						Utils.logError(e)
				else:
					try:
						if str(fileid) in Datashelve:
							shelvedfile=Datashelve[str(fileid)]
							#print(shelvedfile[2])
							if shelvedfile[1]==fileid:
								if int(shelvedfile[2])>int(fileversion):
									Datashelve[str(fileid)]=shelvedfile
								elif int(shelvedfile[2])== int(fileversion):
									Datashelve[str(fileid)]=shelvedfile
								else:
									Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
							else:
								pass
						else:
							Datashelve[str(fileid)]=[filepath,str(fileid),fileversion,cctag]
					except BaseException as e:
						Utils.logError(e)
			del filelist2

			for filepath in filelist:
				fileid='unknown';fileversion='unknown';cctag='unknown'
				tid1=list()
				tid2=list()
				tid1=[pos for pos, char in enumerate(filepath) if char == '[']
				tid2=[pos for pos, char in enumerate(filepath) if char == ']']
				if len(tid1)>=len(tid2):
					lentlist=len(tid1)
				elif len(tid1)<len(tid2):
					lentlist=len(tid2)
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
						t=filepath[i1:i2]
						#print(t)
						if len(t)==16:
							try:
								test1=filepath[i1:i2]
								int(filepath[i1:i2], 16)
								fileid=str(filepath[i1:i2]).upper()
								if fileid !='unknown':
									if int(fileid[-3:])==800:
										cctag='UPD'
									elif int(fileid[-3:])==000:
										cctag='BASE'
									else:
										try:
											int(fileid[-3:])
											cctag='DLC'
										except:pass
									break
							except:
								try:
									fileid=str(filepath[i1:i2]).upper()
									if str(fileid[-3:])!='800' or str(fileid[-3:])!='000':
										DLCnumb=str(fileid)
										DLCnumb="0000000000000"+DLCnumb[-3:]
										DLCnumb=bytes.fromhex(DLCnumb)
										DLCnumb=str(int.from_bytes(DLCnumb, byteorder='big'))
										DLCnumb=int(DLCnumb)
										cctag='DLC'
								except:continue
					except:pass
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
					except:pass
					if (str(filepath[(i1)]).upper())=='V':
						try:
							test2=filepath[(i1+1):i2]
							fileversion=int(filepath[(i1+1):i2])
							if fileversion !='unknown':
								break
						except:
							continue

				#print(fileid+' '+str(fileversion)+' '+cctag)
				#print(filepath)
				if fileid == 'unknown' or fileversion == 'unknown':
					print(fileid+' '+str(fileversion))
					print(str(os.path.basename(os.path.abspath(filepath))))
					print(test1)
					print(test2)

				if cctag!="DLC" and cctag!="BASE" and cctag!="UPD":
					print(str(os.path.basename(os.path.abspath(filepath))))

				try:
					if str(fileid) in Datashelve:
						shelvedfile=Datashelve[str(fileid)]
						if int(shelvedfile[2])<int(fileversion):
							print(fileid +' v'+str(fileversion))
							with open(exportlist,"a", encoding='utf8') as tfile:
								tfile.write(filepath+'\n')
					else:
						print(fileid +' v'+str(fileversion))
						#print(filepath)
						#tfname='testmissdlc.txt'
						with open(exportlist,"a", encoding='utf8') as tfile:
							tfile.write(filepath+'\n')
				except BaseException as e:
					Utils.logError(e)
			Datashelve.close()
			try:os.remove('File01.dshlv')
			except:pass
			Status.close()

		# ...................................................
		# Create exclude list
		# ...................................................
		#parser.add_argument('-cr_elist', '--cr_excl_list', nargs='+', help='Creates a exclude list from a textfile and a folder or 2 textfiles')
		#parser.add_argument('-tfile_aux', '--text_file_aux', help='Auxiliary text file')
		if args.cr_excl_list:
			from listmanager import read_lines_to_list,folder_to_list,parsetags
			if args.fexport:
				for input in args.fexport:
					try:
						exportlist = input
					except BaseException as e:
						Utils.logError(e)
			baselist=list()
			addonlist=list()
			updlist=list();updtomove=list()
			filelist=list()
			if args.text_file:
				tfile=args.text_file
				filelist=read_lines_to_list(tfile,all=True)
			if args.text_file_aux:
				filelist2=list()
				tfile2=args.text_file_aux
				filelist2=read_lines_to_list(tfile2,all=True)
			else:
				filelist2=list()
				ruta=args.cr_excl_list[0]
				if ruta[-1]=='"':
					ruta=ruta[:-1]
				if ruta[0]=='"':
					ruta=ruta[1:]
				extlist=list()
				extlist.append('.nsp')
				extlist.append('.nsz')				
				extlist.append('.xci')
				extlist.append('.xcz')				
				if args.filter:
					for f in args.filter:
						filter=f
				else:
					filter=False
				#print(ruta)
				filelist2=folder_to_list(ruta,extlist,filter)
			'''
			for file in filelist2:
				print(file)
				pass
			'''
			test2="";test=""
			Datashelve = dbmodule.Dict('File01.dshlv');c=0
			for filepath in filelist2:
				fileid='unknown';fileversion='unknown';cctag='unknown';baseid='unknown'
				nG=0;nU=0;nD=0
				try:
					fileid,fileversion,cctag,nG,nU,nD,baseid=parsetags(filepath)
				except:pass	
				#print(fileid+' '+str(fileversion)+' '+cctag)
				if fileid == 'unknown' or fileversion == 'unknown':
					print(fileid+' '+str(fileversion))
					print(str(os.path.basename(os.path.abspath(filepath))))
					x=parsetags(filepath)
					print(str(x))
				if cctag!="DLC" and cctag!="BASE" and cctag!="UPD":
					print(str(os.path.basename(os.path.abspath(filepath))))
				if c==0:
					c+=1
					try:
						Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag,nG,nU,nD,baseid]
					except BaseException as e:
						Utils.logError(e)
				else:
					try:
						if str(fileid) in Datashelve:
							shelvedfile=Datashelve[str(fileid)]
							#print(shelvedfile[2])
							if shelvedfile[1]==fileid:
								if int(shelvedfile[2])>int(fileversion):
									Datashelve[str(fileid)]=shelvedfile
								elif int(shelvedfile[2])== int(fileversion):
									if int(shelvedfile[6])>=int(nD):
										Datashelve[str(fileid)]=shelvedfile
									else:
										Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag,nG,nU,nD,baseid]
								else:
									Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag,nG,nU,nD,baseid]
							else:
								pass
						else:
							Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag,nG,nU,nD,baseid]
					except BaseException as e:
						Utils.logError(e)
			del filelist2

			for filepath in filelist:
				fileid='unknown';fileversion='unknown';cctag='unknown';baseid='unknown'
				nG=0;nU=0;nD=0
				try:
					fileid,fileversion,cctag,nG,nU,nD,baseid=parsetags(filepath)
				except:pass	
				#print(fileid+' '+str(fileversion)+' '+cctag)
				#print(filepath)
				if fileid == 'unknown' or fileversion == 'unknown':
					print(fileid+' '+str(fileversion))
					print(str(os.path.basename(os.path.abspath(filepath))))
					x=parsetags(filepath)
					print(str(x))

				if cctag!="DLC" and cctag!="BASE" and cctag!="UPD":
					print(str(os.path.basename(os.path.abspath(filepath))))

				try:
					if str(fileid) in Datashelve:
						shelvedfile=Datashelve[str(fileid)]
						if str(filepath) != str(shelvedfile[0]):
							if int(shelvedfile[2])>int(fileversion):
								print(fileid +' v'+str(fileversion))
								with open(exportlist,"a", encoding='utf8') as tfile:
									tfile.write(filepath+'\n')
							elif int(shelvedfile[2])==int(fileversion):
								if int(shelvedfile[6])>int(nD):
									print(fileid +' v'+str(fileversion))
									with open(exportlist,"a", encoding='utf8') as tfile:
										tfile.write(filepath+'\n')									
					else:
						pass
				except BaseException as e:
					Utils.logError(e)
			Datashelve.close()
			try:os.remove('File01.dshlv')
			except:pass
			Status.close()

		# ...................................................
		# OUTDATED XCI LIST
		# ...................................................
		#parser.add_argument('-cr_xcioutlist', '--cr_outdated_xci_list', nargs='+', help='Creates a include list from a textfile and a folder')
		#parser.add_argument('-tfile_aux', '--text_file_aux', help='Auxiliary text file')
		if args.cr_outdated_xci_list:
			# if args.ofolder:
				# for input in args.ofolder:
					# try:
						# ofolder = input
					# except BaseException as e:
						# Utils.logError(e)
			# else:
				# for filepath in args.cr_outdated_xci_list:
					# ofolder=os.path.abspath(filepath)
					# ofolder=os.path.join(ofolder, 'old')
			# if not os.path.exists(ofolder):
				# os.makedirs(ofolder)
			# duplicates_f=os.path.join(ofolder, 'duplicates')
			# if not os.path.exists(duplicates_f):
				# os.makedirs(duplicates_f)
			if args.fexport:
				for input in args.fexport:
					try:
						exportlist = input
					except BaseException as e:
						Utils.logError(e)
			baselist=list()
			addonlist=list()
			updlist=list();updtomove=list()
			filelist=list()
			if args.text_file:
				tfile=args.text_file
				with open(tfile,"r+", encoding='utf8') as f:
					for line in f:
						fp=line.strip()
						filelist.append(fp)
			if args.text_file_aux:
				filelist2=list()
				tfile2=args.text_file_aux
				with open(tfile2,"r+", encoding='utf8') as f:
					for line in f:
						fp=line.strip()
						filelist2.append(fp)
			else:
				filelist2=list()
				ruta=args.cr_outdated_xci_list[0]
				if ruta[-1]=='"':
					ruta=ruta[:-1]
				if ruta[0]=='"':
					ruta=ruta[1:]
				extlist=list()
				extlist.append('.nsp')
				extlist.append('.nsz')				
				extlist.append('.xci')
				extlist.append('.xcz')				
				if args.filter:
					for f in args.filter:
						filter=f
				#print(ruta)
				try:
					fname=""
					binbin='RECYCLE.BIN'
					for ext in extlist:
						#print (ext)
						#print (ruta)
						if os.path.isdir(ruta):
							for dirpath, dirnames, filenames in os.walk(ruta):
								for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
									fname=""
									if args.filter:
										if filter.lower() in filename.lower():
											fname=filename
									else:
										fname=filename
										#print(fname)
									if fname != "":
										if binbin.lower() not in filename.lower():
											filelist2.append(os.path.join(dirpath, filename))
						else:
							if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
								filename = ruta
								#print(ruta)
								fname=""
								if args.filter:
									if filter.lower() in filename.lower():
										fname=filename
								else:
									fname=filename
								if fname != "":
									if binbin.lower() not in filename.lower():
										filelist2.append(filename)
				except BaseException as e:
					Utils.logError(e)
					pass
			'''
			for file in filelist2:
				print(file)
				pass
			'''
			test2="";test=""
			Datashelve = dbmodule.Dict('File01.dshlv');c=0
			for filepath in filelist2:
				fileid='unknown';fileversion='unknown';cctag='unknown'
				tid1=list()
				tid2=list()
				tid1=[pos for pos, char in enumerate(filepath) if char == '[']
				tid2=[pos for pos, char in enumerate(filepath) if char == ']']
				if len(tid1)>=len(tid2):
					lentlist=len(tid1)
				elif len(tid1)<len(tid2):
					lentlist=len(tid2)
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
						t=filepath[i1:i2]
						#print(t)
						if len(t)==16:
							try:
								test1=filepath[i1:i2]
								int(filepath[i1:i2], 16)
								fileid=str(filepath[i1:i2]).upper()
								if fileid !='unknown':
									if int(fileid[-3:])==800:
										cctag='UPD'
									elif int(fileid[-3:])==000:
										cctag='BASE'
									else:
										try:
											int(fileid[-3:])
											cctag='DLC'
										except:pass
									break
							except:
								try:
									fileid=str(filepath[i1:i2]).upper()
									if str(fileid[-3:])!='800' or str(fileid[-3:])!='000':
										DLCnumb=str(fileid)
										DLCnumb="0000000000000"+DLCnumb[-3:]
										DLCnumb=bytes.fromhex(DLCnumb)
										DLCnumb=str(int.from_bytes(DLCnumb, byteorder='big'))
										DLCnumb=int(DLCnumb)
										cctag='DLC'
								except:continue
					except:pass
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
					except:pass
					if (str(filepath[(i1)]).upper())=='V':
						try:
							test2=filepath[(i1+1):i2]
							fileversion=int(filepath[(i1+1):i2])
							#print(fileversion)
							if fileversion !='unknown':
								break
						except:
							continue
				if cctag=="BASE" and fileversion == 'unknown':
					fileversion=0
				#print(fileid+' '+str(fileversion)+' '+cctag)
				if fileid == 'unknown' or fileversion == 'unknown':
					print(fileid+' '+str(fileversion))
					print(str(os.path.basename(os.path.abspath(filepath))))
					print(test1)
					print(test2)

				if cctag!="DLC" and cctag!="BASE" and cctag!="UPD":
					print(str(os.path.basename(os.path.abspath(filepath))))
				if c==0:
					c+=1
					try:
						Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
					except BaseException as e:
						Utils.logError(e)
				else:
					try:
						if str(fileid) in Datashelve:
							shelvedfile=Datashelve[str(fileid)]
							#print(shelvedfile[2])
							if shelvedfile[1]==fileid:
								if int(shelvedfile[2])>int(fileversion):
									Datashelve[str(fileid)]=shelvedfile
								elif int(shelvedfile[2])== int(fileversion):
									Datashelve[str(fileid)]=shelvedfile
								else:
									Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
							else:
								pass
						else:
							Datashelve[str(fileid)]=[filepath,str(fileid),fileversion,cctag]
					except BaseException as e:
						Utils.logError(e)
			del filelist2

			for filepath in filelist:
				fileid='unknown';fileversion='unknown';cctag='unknown'
				tid1=list()
				tid2=list()
				tid1=[pos for pos, char in enumerate(filepath) if char == '[']
				tid2=[pos for pos, char in enumerate(filepath) if char == ']']
				if len(tid1)>=len(tid2):
					lentlist=len(tid1)
				elif len(tid1)<len(tid2):
					lentlist=len(tid2)
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
						t=filepath[i1:i2]
						#print(t)
						if len(t)==16:
							try:
								test1=filepath[i1:i2]
								int(filepath[i1:i2], 16)
								fileid=str(filepath[i1:i2]).upper()
								if fileid !='unknown':
									if int(fileid[-3:])==800:
										cctag='UPD'
									elif int(fileid[-3:])==000:
										cctag='BASE'
									else:
										try:
											int(fileid[-3:])
											cctag='DLC'
										except:pass
									break
							except:
								try:
									fileid=str(filepath[i1:i2]).upper()
									if str(fileid[-3:])!='800' or str(fileid[-3:])!='000':
										DLCnumb=str(fileid)
										DLCnumb="0000000000000"+DLCnumb[-3:]
										DLCnumb=bytes.fromhex(DLCnumb)
										DLCnumb=str(int.from_bytes(DLCnumb, byteorder='big'))
										DLCnumb=int(DLCnumb)
										cctag='DLC'
								except:continue
					except:pass
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
					except:pass
					if (str(filepath[(i1)]).upper())=='V':
						try:
							test2=filepath[(i1+1):i2]
							fileversion=int(filepath[(i1+1):i2])
							if fileversion !='unknown':
								break
						except:
							continue

				#print(fileid+' '+str(fileversion)+' '+cctag)
				#print(filepath)

				if cctag=="BASE" and fileversion == 'unknown':
					fileversion=0

				if fileid == 'unknown' or fileversion == 'unknown':
					print(fileid+' '+str(fileversion))
					print(str(os.path.basename(os.path.abspath(filepath))))
					print(test1)
					print(test2)

				if cctag!="DLC" and cctag!="BASE" and cctag!="UPD":
					print(str(os.path.basename(os.path.abspath(filepath))))

				isbase=False
				if str(fileid[-3:])=='000':
					isbase=True
				elif str(fileid[-3:])=='800':
					fileid=str(fileid[:-3])+'000'
				else:
					pass

				try:
					if str(fileid) in Datashelve:
						shelvedfile=Datashelve[str(fileid)]
						if int(shelvedfile[2])<int(fileversion):
							print(fileid +' v'+str(fileversion))
							with open(exportlist,"a", encoding='utf8') as tfile:
								tfile.write(filepath+'\n')
					elif isbase==True:
						print(fileid +' v'+str(fileversion))
						#print(filepath)
						#tfname='testmissdlc.txt'
						with open(exportlist,"a", encoding='utf8') as tfile:
							tfile.write(filepath+'\n')
					else:
						pass
				except BaseException as e:
					Utils.logError(e)
			Datashelve.close()
			try:os.remove('File01.dshlv')
			except:pass
			Status.close()

		# ...................................................
		# EXPAND LIST
		# ...................................................
		#parser.add_argument('-cr_xexplist', '--cr_expand_list', nargs='+', help='Expands the list with games by baseid')
		#parser.add_argument('-tfile_aux', '--text_file_aux', help='Auxiliary text file')
		if args.cr_expand_list:
			# if args.ofolder:
				# for input in args.ofolder:
					# try:
						# ofolder = input
					# except BaseException as e:
						# Utils.logError(e)
			# else:
				# for filepath in args.cr_expand_list:
					# ofolder=os.path.abspath(filepath)
					# ofolder=os.path.join(ofolder, 'old')
			# if not os.path.exists(ofolder):
				# os.makedirs(ofolder)
			# duplicates_f=os.path.join(ofolder, 'duplicates')
			# if not os.path.exists(duplicates_f):
				# os.makedirs(duplicates_f)
			if args.fexport:
				for input in args.fexport:
					try:
						exportlist = input
					except BaseException as e:
						Utils.logError(e)
			baselist=list()
			addonlist=list()
			updlist=list();updtomove=list()
			filelist=list()
			if args.text_file:
				tfile=args.text_file
				with open(tfile,"r+", encoding='utf8') as f:
					for line in f:
						fp=line.strip()
						filelist.append(fp)
			if args.text_file_aux:
				filelist2=list()
				tfile2=args.text_file_aux
				with open(tfile2,"r+", encoding='utf8') as f:
					for line in f:
						fp=line.strip()
						filelist2.append(fp)
			else:
				filelist2=list()
				ruta=args.cr_expand_list[0]
				if ruta[-1]=='"':
					ruta=ruta[:-1]
				if ruta[0]=='"':
					ruta=ruta[1:]
				extlist=list()
				extlist.append('.nsp')
				extlist.append('.nsz')				
				extlist.append('.xci')
				extlist.append('.xcz')				
				if args.filter:
					for f in args.filter:
						filter=f
				#print(ruta)
				try:
					fname=""
					binbin='RECYCLE.BIN'
					for ext in extlist:
						#print (ext)
						#print (ruta)
						if os.path.isdir(ruta):
							for dirpath, dirnames, filenames in os.walk(ruta):
								for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
									fname=""
									if args.filter:
										if filter.lower() in filename.lower():
											fname=filename
									else:
										fname=filename
										#print(fname)
									if fname != "":
										if binbin.lower() not in filename.lower():
											filelist2.append(os.path.join(dirpath, filename))
						else:
							if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
								filename = ruta
								#print(ruta)
								fname=""
								if args.filter:
									if filter.lower() in filename.lower():
										fname=filename
								else:
									fname=filename
								if fname != "":
									if binbin.lower() not in filename.lower():
										filelist2.append(filename)
				except BaseException as e:
					Utils.logError(e)
					pass
			'''
			for file in filelist2:
				print(file)
				pass
			'''
			test2="";test=""
			Datashelve = dbmodule.Dict('File01.dshlv');c=0
			for filepath in filelist2:
				fileid='unknown';fileversion='unknown';cctag='unknown'
				tid1=list()
				tid2=list()
				tid1=[pos for pos, char in enumerate(filepath) if char == '[']
				tid2=[pos for pos, char in enumerate(filepath) if char == ']']
				if len(tid1)>=len(tid2):
					lentlist=len(tid1)
				elif len(tid1)<len(tid2):
					lentlist=len(tid2)
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
						t=filepath[i1:i2]
						#print(t)
						if len(t)==16:
							try:
								test1=filepath[i1:i2]
								int(filepath[i1:i2], 16)
								fileid=str(filepath[i1:i2]).upper()
								if fileid !='unknown':
									if int(fileid[-3:])==800:
										cctag='UPD'
									elif int(fileid[-3:])==000:
										cctag='BASE'
									else:
										try:
											int(fileid[-3:])
											cctag='DLC'
										except:pass
									break
							except:
								try:
									fileid=str(filepath[i1:i2]).upper()
									if str(fileid[-3:])!='800' or str(fileid[-3:])!='000':
										DLCnumb=str(fileid)
										DLCnumb="0000000000000"+DLCnumb[-3:]
										DLCnumb=bytes.fromhex(DLCnumb)
										DLCnumb=str(int.from_bytes(DLCnumb, byteorder='big'))
										DLCnumb=int(DLCnumb)
										cctag='DLC'
								except:continue
					except:pass
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
					except:pass
					if (str(filepath[(i1)]).upper())=='V':
						try:
							test2=filepath[(i1+1):i2]
							fileversion=int(filepath[(i1+1):i2])
							#print(fileversion)
							if fileversion !='unknown':
								break
						except:
							continue

				if cctag=="BASE" and fileversion == 'unknown':
					fileversion=0
				#print(fileid+' '+str(fileversion)+' '+cctag)
				if fileid == 'unknown' or fileversion == 'unknown':
					print(fileid+' '+str(fileversion))
					print(str(os.path.basename(os.path.abspath(filepath))))
					print(test1)
					print(test2)

				if cctag!="DLC" and cctag!="BASE" and cctag!="UPD":
					print(str(os.path.basename(os.path.abspath(filepath))))
				if c==0:
					c+=1
					try:
						Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
					except BaseException as e:
						Utils.logError(e)
				else:
					try:
						if str(fileid) in Datashelve:
							shelvedfile=Datashelve[str(fileid)]
							#print(shelvedfile[2])
							if shelvedfile[1]==fileid:
								if int(shelvedfile[2])>int(fileversion):
									Datashelve[str(fileid)]=shelvedfile
								elif int(shelvedfile[2])== int(fileversion):
									Datashelve[str(fileid)]=shelvedfile
								else:
									Datashelve[str(fileid)]=[filepath,fileid,fileversion,cctag]
							else:
								pass
						else:
							Datashelve[str(fileid)]=[filepath,str(fileid),fileversion,cctag]
					except BaseException as e:
						Utils.logError(e)
			del filelist2

			for filepath in filelist:
				fileid='unknown';fileversion='unknown';cctag='unknown'
				tid1=list()
				tid2=list()
				tid1=[pos for pos, char in enumerate(filepath) if char == '[']
				tid2=[pos for pos, char in enumerate(filepath) if char == ']']
				if len(tid1)>=len(tid2):
					lentlist=len(tid1)
				elif len(tid1)<len(tid2):
					lentlist=len(tid2)
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
						t=filepath[i1:i2]
						#print(t)
						if len(t)==16:
							try:
								test1=filepath[i1:i2]
								int(filepath[i1:i2], 16)
								fileid=str(filepath[i1:i2]).upper()
								if fileid !='unknown':
									if int(fileid[-3:])==800:
										cctag='UPD'
									elif int(fileid[-3:])==000:
										cctag='BASE'
									else:
										try:
											int(fileid[-3:])
											cctag='DLC'
										except:pass
									break
							except:
								try:
									fileid=str(filepath[i1:i2]).upper()
									if str(fileid[-3:])!='800' or str(fileid[-3:])!='000':
										DLCnumb=str(fileid)
										DLCnumb="0000000000000"+DLCnumb[-3:]
										DLCnumb=bytes.fromhex(DLCnumb)
										DLCnumb=str(int.from_bytes(DLCnumb, byteorder='big'))
										DLCnumb=int(DLCnumb)
										cctag='DLC'
								except:continue
					except:pass
				for i in range(lentlist):
					try:
						i1=tid1[i]+1
						i2=tid2[i]
					except:pass
					if (str(filepath[(i1)]).upper())=='V':
						try:
							test2=filepath[(i1+1):i2]
							fileversion=int(filepath[(i1+1):i2])
							if fileversion !='unknown':
								break
						except:
							continue
				if cctag=="BASE" and fileversion == 'unknown':
					fileversion=0
				#print(fileid+' '+str(fileversion)+' '+cctag)
				#print(filepath)
				if fileid == 'unknown' or fileversion == 'unknown':
					print(fileid+' '+str(fileversion))
					print(str(os.path.basename(os.path.abspath(filepath))))
					print(test1)
					print(test2)

				if cctag!="DLC" and cctag!="BASE" and cctag!="UPD":
					print(str(os.path.basename(os.path.abspath(filepath))))
				if str(fileid[-3:])=='800':
					fileid=str(fileid[:-3])+'000'
				elif str(fileid[-3:])=='000':
					fileid=str(fileid)
				else:
					#print(str(fileid))
					DLCnumb=str(fileid)
					#print(hx(b''+bytes.fromhex('0'+DLCnumb[-4:-3])))
					token=int(hx(bytes.fromhex('0'+DLCnumb[-4:-3])),16)-int('1',16)
					token=str(hex(token))[-1]
					token=token.upper()
					#print(token)
					fileid=fileid[:-4]+token+'000'
					#print(fileid)
				try:
					if str(fileid) in Datashelve:
						shelvedfile=Datashelve[str(fileid)]
						if str(shelvedfile[0])!=str(filepath):
							print(str(fileid) +' v'+str(fileversion))
							with open(exportlist,"a", encoding='utf8') as tfile:
								tfile.write(str(filepath)+'\n')
					elif  str(fileid[:-3]+'800') in Datashelve:
						fileid=str(fileid[:-3]+'800')
						shelvedfile=Datashelve[str(fileid)]
						if str(shelvedfile[0])!=str(filepath):
							print(str(fileid) +' v'+str(fileversion))
							with open(exportlist,"a", encoding='utf8') as tfile:
								tfile.write(str(filepath)+'\n')
					else:
						pass
				except BaseException as e:
					Utils.logError(e)
			Datashelve.close()
			try:os.remove('File01.dshlv')
			except:pass
			Status.close()

		#parser.add_argument('-blckl', '--black_list', nargs='+', help='Deletes blacklisted files from a list')
		if args.black_list:
			try:
				if args.fexport:
					for input in args.fexport:
						try:
							exportlist = input
						except BaseException as e:
							Utils.logError(e)
				baselist=list()
				addonlist=list()
				updlist=list();updtomove=list()
				blacklist=list()
				if args.black_list:
					t_blacklist=args.black_list[0]
					if args.black_list[1]:
						if str(args.black_list[1]).lower()=='true':
							blacklistbaseid=True
						else:
							blacklistbaseid=False
					else:
						blacklistbaseid=False
					with open(t_blacklist,"r+", encoding='utf8') as f:
						for line in f:
							fp=line.strip()
							blacklist.append(fp)
				if args.text_file:
					filelist2=list()
					tfile2=args.text_file
					with open(tfile2,"r+", encoding='utf8') as f:
						for line in f:
							fp=line.strip()
							filelist2.append(fp)
				else:
					filelist2=list()
					ruta=args.cr_incl_list[0]
					if ruta[-1]=='"':
						ruta=ruta[:-1]
					if ruta[0]=='"':
						ruta=ruta[1:]
					extlist=list()
					extlist.append('.nsp')
					extlist.append('.nsz')					
					extlist.append('.xci')
					extlist.append('.xcz')					
					if args.filter:
						for f in args.filter:
							filter=f
					#print(ruta)
					try:
						fname=""
						binbin='RECYCLE.BIN'
						for ext in extlist:
							#print (ext)
							#print (ruta)
							if os.path.isdir(ruta):
								for dirpath, dirnames, filenames in os.walk(ruta):
									for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
										fname=""
										if args.filter:
											if filter.lower() in filename.lower():
												fname=filename
										else:
											fname=filename
											#print(fname)
										if fname != "":
											if binbin.lower() not in filename.lower():
												filelist2.append(os.path.join(dirpath, filename))
							else:
								if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
									filename = ruta
									#print(ruta)
									fname=""
									if args.filter:
										if filter.lower() in filename.lower():
											fname=filename
									else:
										fname=filename
									if fname != "":
										if binbin.lower() not in filename.lower():
											filelist2.append(filename)
					except BaseException as e:
						Utils.logError(e)
						pass
				test2="";test=""
				Datashelve = dbmodule.Dict('File01.dshlv');c=0
				for filepath in filelist2:
					fileid='unknown';fileversion='unknown';cctag='unknown'
					try:
						fileid,fileversion,cctag,nG,nU,nD,baseid=listmanager.parsetags(filepath)
					except:pass
					if 	cctag !='unknown':
						try:
							Datashelve[str(fileid)]=[filepath,str(fileid),fileversion,cctag,nG,nU,nD,baseid]
						except: pass
				del filelist2
				tfile=open(exportlist,"w", encoding='utf8')
				tfile.close()
				for filepath in blacklist:
					fileid='unknown';fileversion='unknown';cctag='unknown'
					try:
						fileid,fileversion,cctag,nG,nU,nD,baseid=listmanager.parsetags(filepath)
						#print(baseid)
					except:pass
					if 	cctag !='unknown':
						try:
							if str(fileid) in Datashelve:
								del Datashelve[str(fileid)]
							else:
								keylist=list()
								for k in Datashelve.keys():
									keylist.append(k)
								for k in keylist:
									if k in Datashelve:
										entry=Datashelve[k]
										test=str(entry[0]).lower()
										fp=str(filepath).lower()
										if test==fp:
											del Datashelve[k]
							if blacklistbaseid==False:
								pass
							else:
								keylist=list()
								for k in Datashelve.keys():
									keylist.append(k)
								for k in keylist:
									if k in Datashelve:
										entry=Datashelve[k]
										test=str(entry[-1]).lower()
										baseid=str(baseid).lower()
										if test==baseid:
											del Datashelve[k]
						except BaseException as e:
							Utils.logError(e)
							continue
				del blacklist
				for k in Datashelve.keys():
					with open(exportlist,"a", encoding='utf8') as tfile:
						entry=Datashelve[k]
						fp=str(entry[0])
						tfile.write(fp+'\n')
				Datashelve.close()
				try:os.remove('File01.dshlv')
				except:pass
			except:pass
			Status.close()

		#parser.add_argument('-chdlcn', '--chck_dlc_numb', nargs='+', help='Checks if xci has corrent number of dlcs')
		if args.chck_dlc_numb:
			try:
				if args.fexport:
					for input in args.fexport:
						try:
							exportlist = input
						except BaseException as e:
							Utils.logError(e)
				baselist=list()
				addonlist=list()
				updlist=list();updtomove=list()
				dlclist=list()
				if args.chck_dlc_numb:
					t_dlc_list=args.chck_dlc_numb[0]
					with open(t_dlc_list,"r+", encoding='utf8') as f:
						for line in f:
							fp=line.strip()
							dlclist.append(fp)
				if args.text_file:
					filelist2=list()
					tfile2=args.text_file
					with open(tfile2,"r+", encoding='utf8') as f:
						for line in f:
							fp=line.strip()
							filelist2.append(fp)
				else:
					filelist2=list()
					ruta=args.cr_incl_list[0]
					if ruta[-1]=='"':
						ruta=ruta[:-1]
					if ruta[0]=='"':
						ruta=ruta[1:]
					extlist=list()
					extlist.append('.nsp')
					extlist.append('.nsz')					
					extlist.append('.xci')
					extlist.append('.xcz')					
					if args.filter:
						for f in args.filter:
							filter=f
					#print(ruta)
					try:
						fname=""
						binbin='RECYCLE.BIN'
						for ext in extlist:
							#print (ext)
							#print (ruta)
							if os.path.isdir(ruta):
								for dirpath, dirnames, filenames in os.walk(ruta):
									for filename in [f for f in filenames if f.endswith(ext.lower()) or f.endswith(ext.upper()) or f[:-1].endswith(ext.lower()) or f[:-1].endswith(ext.lower())]:
										fname=""
										if args.filter:
											if filter.lower() in filename.lower():
												fname=filename
										else:
											fname=filename
											#print(fname)
										if fname != "":
											if binbin.lower() not in filename.lower():
												filelist2.append(os.path.join(dirpath, filename))
							else:
								if ruta.endswith(ext.lower()) or ruta.endswith(ext.upper()) or ruta[:-1].endswith(ext.lower()) or ruta[:-1].endswith(ext.upper()):
									filename = ruta
									#print(ruta)
									fname=""
									if args.filter:
										if filter.lower() in filename.lower():
											fname=filename
									else:
										fname=filename
									if fname != "":
										if binbin.lower() not in filename.lower():
											filelist2.append(filename)
					except BaseException as e:
						Utils.logError(e)
						pass
				test2="";test=""
				Datashelve = dbmodule.Dict('File01.dshlv');c=0
				for filepath in filelist2:
					fileid='unknown';fileversion='unknown';cctag='unknown'
					try:
						fileid,fileversion,cctag,nG,nU,nD,baseid=listmanager.parsetags(filepath)
					except:pass
					if 	cctag !='unknown':
						try:
							Datashelve[str(fileid)]=[filepath,str(fileid),fileversion,cctag,nG,nU,nD,baseid]
						except: pass
				del filelist2
				tfile=open(exportlist,"w", encoding='utf8')
				tfile.close()
				keylist=list()
				for k in Datashelve.keys():
					keylist.append(k)
				for k in keylist:
					if k in Datashelve:
						entry=Datashelve[k]
						numbDLC=entry[6]
						test=str(entry[1]).lower()
						count=0
						dlcpaths=list()
						# test2='['+test[:-4]
						for filepath in dlclist:
							fileid='unknown';fileversion='unknown';cctag='unknown'
							# print(test2)
							# if test2 in str(filepath).lower():
							try:
								# print(filepath)
								fileid,fileversion,cctag,nG,nU,nD,baseid=listmanager.parsetags(filepath)
								# print(baseid)
								# print(test)
								baseid=baseid.lower()
								if (str(baseid).lower())==test:
									if not filepath in dlcpaths:
										count+=1
										dlcpaths.append(filepath)
									dlclist.remove(filepath)
							except BaseException as e:
								Utils.logError(e)
								pass
							# print(str(count))
							# print(str(numbDLC))
						if count>int(numbDLC):
							with open(exportlist,"a", encoding='utf8') as tfile:
								tfile.write(str(entry[0])+'\n')
				Datashelve.close()
				try:os.remove('File01.dshlv')
				except:pass
			except:pass
			Status.close()
		# ...................................................
		# Restore. File Restoration
		# ...................................................
		
		if args.restore:
			feed='';cnmt_is_patched=False
			if args.buffer:
				for var in args.buffer:
					try:
						buffer = var
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
				for filename in args.restore:
					dir=os.path.dirname(os.path.abspath(filename))
					ofolder =os.path.join(dir, 'output')				
			if not os.path.exists(ofolder):
				os.makedirs(ofolder)
			tmpfolder =os.path.join(ofolder, 'tmp')	
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
				for filename in args.restore:
					filename=filename
			ofile=str(os.path.basename(os.path.abspath(filename)))
			ofile=os.path.join(ofolder, ofile)
			if filename.endswith('.nsp') or filename.endswith('.nsx'):
				try:
					f = Fs.Nsp(filename, 'rb')
					check,feed=f.verify()
					verdict,headerlist,feed=f.verify_sig(feed,tmpfolder,cnmt='nocheck')
					output_type='nsp';multi=False;cnmtcount=0
					if verdict == True:
						isrestored=True
						for i in range(len(headerlist)):
							entry=headerlist[i]
							if str(entry[0]).endswith('.cnmt.nca'):
								cnmtcount+=1
								if cnmt_is_patched==False:
									status=entry[2]
									if status=='patched':
										cnmt_is_patched=True
							if entry[1]!=False:
								if int(entry[-1])==1:
									output_type='xci'
								isrestored=False	
							else:
								pass
						if	isrestored == False:	
							if cnmt_is_patched !=True:
								print('\nFILE WAS MODIFIED. FILE IS RESTORABLE')
							else:
								print('\nFILE WAS MODIFIED AND CNMT PATCHED. FILE MAY BE RESTORABLE')
							if cnmtcount<2:
								if not os.path.exists(ofolder):
									os.makedirs(ofolder)
								f.restore_ncas(buffer,headerlist,verdict,ofile,feed,output_type)
							else:
								print(" -> Current Implementation doesn't support multicontent files")
								print("    Please use the multicontent splitter first")
						else:
							print("\nFILE WASN'T MODIFIED. SKIPPING RESTORATION")
					if verdict == False:		
						print("\nFILE WAS MODIFIED. FILE ISN'T RESTORABLE")					
				except BaseException as e:
					Utils.logError(e)
			if filename.endswith('.xci'):		
				try:
					f = Fs.Xci(filename)
					check,feed=f.verify()
					verdict,headerlist,feed=f.verify_sig(feed,tmpfolder)
					output_type='nsp';multi=False;cnmtcount=0
					if verdict == True:
						isrestored=True
						for i in range(len(headerlist)):
							entry=headerlist[i]
							if str(entry[0]).endswith('.cnmt.nca'):
								cnmtcount+=1
							if entry[1]!=False:
								if int(entry[-1])==1:
									output_type='xci'
								isrestored=False	
							else:
								pass
						if	isrestored == False:	
							print('\nFILE WAS MODIFIED. FILE IS RESTORABLE')
							if cnmtcount<2:
								if not os.path.exists(ofolder):
									os.makedirs(ofolder)
								f.restore_ncas(buffer,headerlist,verdict,ofile,feed,output_type)
							else:
								print(" -> Current Implementation doesn't support multicontent files")
								print("    Please use the multicontent splitter first")
						else:
							print("\nFILE WASN'T MODIFIED. SKIPPING RESTORATION")
					elif verdict == False:		
						print("\nFILE WAS MODIFIED. FILE ISN'T RESTORABLE")					
				except BaseException as e:
					Utils.logError(e)			

		Status.close()

		def init_interface():
			import secondary
			parameters=["Interface","start"]
			vret=secondary.call_library(parameters)
		#init_interface()

	except KeyboardInterrupt:
		Config.isRunning = False
		Status.close()
	except BaseException as e:
		Config.isRunning = False
		Status.close()
		raise
		
	# app=init_interface()




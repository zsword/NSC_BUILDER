extern crate aes128;
extern crate Title;
extern crate Titles;
extern crate Hex;
extern crate binascii;
extern crate struct;
extern crate Fs;
extern crate hashlib;
extern crate Fs_Type;
extern crate os;
extern crate re;
extern crate pathlib;

extern crate Keys;
extern crate Config;
extern crate Print;
extern crate Nsps;
extern crate sq_tools;
extern crate tqdm;
extern crate Pfs0;
extern crate Ticket;
extern crate Nca;
extern crate Nacp;
extern crate NcaHeader;
extern crate MemoryFile;
extern crate pyNCA3;
extern crate pyNPDM;
extern crate BaseFs;
extern crate math;
extern crate sys;
extern crate shutil;
extern crate DBmodule;

#[cfg(target_os = "windows")]
extern crate win32con;
#[cfg(target_os = "windows")]
extern crate win32api;

extern crate operator;
extern crate Crypto;
extern crate io;
extern crate nutdb;
extern crate textwrap;
extern crate PIL;
extern crate bytes2human;

use aes128::*;
use Title::*;
use Titles::*;
use Hex::*;
use binascii::{hexlify as hx, unhexlify as uhx};
use struct::{pack as pk, unpack as upk};
use Fs::File;
use hashlib::{sha256, sha1};
use Fs_Type::*;
use Fs::*;
use os::*;
use re::*;
use pathlib::*;

use Keys::*;
use Config::*;
use Print::*;
use Nsps::*;
use sq_tools::*;
use tqdm::*;
use Pfs0::*;
use Ticket::*;
use Nca::*;
use Nacp::*;
use NcaHeader::*;
use File::*;
use pyNCA3::*;
use pyNPDM::*;
use BaseFs::*;
use math::*;
use sys::*;
use shutil::*;
use DBmodule::*;

#[cfg(target_os = "windows")]
use win32con::*;
#[cfg(target_os = "windows")]
use win32api::*;

use operator::{itemgetter, attrgetter, methodcaller};
use Crypto::Cipher::AES;
use io::*;
use nutdb::*;
use textwrap::*;
use PIL::Image;
use bytes2human::*;

const MEDIA_SIZE: u32 = 0x200;
const indent: u32 = 1;
const tabs: &str = "\t" * indent;

struct SectionTableEntry {
    media_offset: u32,
    media_end_offset: u32,
    offset: u32,
    end_offset: u32,
    unknown1: u32,
    unknown2: u32,
    sha1: Option<[u8; 20]>,
}

impl SectionTableEntry {
    fn new(d: &[u8]) -> Self {
        let media_offset = u32::from_le_bytes(d[0x0..0x4].try_into().unwrap());
        let media_end_offset = u32::from_le_bytes(d[0x4..0x8].try_into().unwrap());
        let offset = media_offset * MEDIA_SIZE;
        let end_offset = media_end_offset * MEDIA_SIZE;
        let unknown1 = u32::from_le_bytes(d[0x8..0xc].try_into().unwrap());
        let unknown2 = u32::from_le_bytes(d[0xc..0x10].try_into().unwrap());
        SectionTableEntry {
            media_offset,
            media_end_offset,
            offset,
            end_offset,
            unknown1,
            unknown2,
            sha1: None,
        }
    }
}

fn get_section_filesystem(buffer: &[u8], crypto_key: &[u8]) -> Box<dyn BaseFs> {
    let fs_type = buffer[0x3];
    if fs_type == Fs_Type::Fs::PFS0 {
        return Box::new(Pfs0::new(buffer, Some(crypto_key)));
    }
    if fs_type == Fs_Type::Fs::ROMFS {
        return Box::new(Rom::new(buffer, Some(crypto_key)));
    }
    return Box::new(BaseFs::new(buffer, Some(crypto_key)));
}

fn get_file_and_offset(filelist: &[Vec<u8>], target_offset: u64) -> (Option<&str>, Option<u64>) {
    let mut start_offset = 0;
    let mut end_offset = 0;
    for entry in filelist {
        let filepath = String::from_utf8_lossy(&entry[0]);
        let size = u64::from_le_bytes(entry[1..9].try_into().unwrap());
        start_offset = end_offset;
        end_offset += size;
        if target_offset > end_offset {
            continue;
        } else {
            let partial_offset = target_offset - start_offset;
            return (Some(filepath.as_ref()), Some(partial_offset));
        }
    }
    return (None, None);
}

fn chain_streams(streams: impl Iterator<Item = impl Read>, buffer_size: usize) -> impl Read {
    let mut stream_iter = streams;
    let mut current_stream = stream_iter.next();
    let mut leftover = vec![];

    move |buf: &mut [u8]| {
        let mut total_read = 0;
        while total_read < buf.len() {
            if leftover.is_empty() {
                if let Some(ref mut s) = current_stream {
                    match s.read(buf) {
                        Ok(0) => {
                            current_stream = stream_iter.next();
                            if current_stream.is_none() {
                                break;
                            }
                        }
                        Ok(n) => {
                            total_read += n;
                            if n < buf.len() {
                                leftover.extend_from_slice(&buf[n..]);
                            }
                        }
                        Err(e) => return Err(e),
                    }
                } else {
                    break;
                }
            } else {
                let n = std::cmp::min(leftover.len(), buf.len());
                buf[..n].copy_from_slice(&leftover[..n]);
                leftover.drain(..n);
                total_read += n;
            }
        }
        Ok(total_read)
    }
}

fn generate_open_file_streams(filenames: &[&str]) -> impl Iterator<Item = impl Read> {
    filenames.iter().map(|&f| File::open(f).unwrap())
}

fn read_start(filepath: &str) {
    let filelist = retchunks(filepath);
    let filenames: Vec<&str> = filelist.iter().map(|f| f[0].as_str()).collect();
    let f = chain_streams(generate_open_file_streams(&filenames));
    if filepath.ends_with(".xc0") {
        let files_list = sq_tools::ret_xci_offsets(filepath);
    } else if filepath.ends_with(".ns0") {
        let files_list = sq_tools::ret_nsp_offsets(filepath);
    }
    println!("{:?}", files_list);
    f.flush().unwrap();
}

fn file_location(filepath: &str, t: &str, print_data: bool) -> Vec<Vec<String>> {
    let filenames = retchunks(filepath);
    let mut locations = vec![];
    let files_list = if filepath.ends_with(".xc0") {
        sq_tools::ret_xci_offsets(filepath)
    } else if filepath.ends_with(".ns0") {
        sq_tools::ret_nsp_offsets(filepath)
    } else {
        vec![]
    };
    for file in files_list {
        if t.to_lowercase() != "all" {
            if file[0].to_lowercase().ends_with(t.to_lowercase()) {
                let (location1, tgoffset1) = get_file_and_offset(&filenames, file[1]);
                let (location2, tgoffset2) = get_file_and_offset(&filenames, file[2]);
                locations.push(vec![
                    file[0].clone(),
                    file[3].clone(),
                    location1.unwrap_or("").to_string(),
                    tgoffset1.unwrap_or(0).to_string(),
                    location2.unwrap_or("").to_string(),
                    tgoffset2.unwrap_or(0).to_string(),
                ]);
                if print_data {
                    println!("{}", file[0]);
                    println!("- Starts in file {} at offset {}", location1.unwrap_or(""), tgoffset1.unwrap_or(0));
                    println!("- Ends in file {} at offset {}", location2.unwrap_or(""), tgoffset2.unwrap_or(0));
                }
            }
        } else {
            let (location1, tgoffset1) = get_file_and_offset(&filenames, file[1]);
            let (location2, tgoffset2) = get_file_and_offset(&filenames, file[2]);
            locations.push(vec![
                file[0].clone(),
                file[3].clone(),
                location1.unwrap_or("").to_string(),
                tgoffset1.unwrap_or(0).to_string(),
                location2.unwrap_or("").to_string(),
                tgoffset2.unwrap_or(0).to_string(),
            ]);
            if print_data {
                println!("{}", file[0]);
                println!("- Starts in file {} at offset {}", location1.unwrap_or(""), tgoffset1.unwrap_or(0));
                println!("- Ends in file {} at offset {}", location2.unwrap_or(""), tgoffset2.unwrap_or(0));
            }
        }
    }
    locations
}

fn retchunks(filepath: &str) -> Vec<Vec<u8>> {
    let mut file_list = vec![];
    let bname = std::path::Path::new(filepath).file_name().unwrap().to_str().unwrap();
    let bn = if bname != "00" {
        &bname[..bname.len() - 4]
    } else {
        ""
    };
    let ender = if filepath.ends_with(".xc0") {
        ".xc"
    } else if filepath.ends_with(".ns0") {
        ".ns"
    } else if filepath.ends_with("00") {
        "0"
    } else {
        println!("Not valid file");
        return vec![];
    };
    let ruta = std::path::Path::new(filepath).parent().unwrap();
    for entry in std::fs::read_dir(ruta).unwrap() {
        let f = entry.unwrap().path();
        if f.is_file() {
            let check = f.file_stem().unwrap().to_str().unwrap();
            if check == ender && &bname[..bname.len() - 1] == check {
                let n = bname.chars().last().unwrap().to_digit(10).unwrap();
                if n < 9 {
                    let fp = f.to_str().unwrap();
                    let size = std::fs::metadata(fp).unwrap().len();
                    file_list.push(vec![fp.as_bytes().to_vec(), size.to_le_bytes().to_vec()]);
                }
            }
        }
    }
    file_list.sort();
    file_list
}

fn return_dbdict(filepath: &str) -> serde_json::Value {
    let cnmtfiles = file_location(filepath, ".cnmt.nca", false);
    let content_number = cnmtfiles.len();
    memoryload(&cnmtfiles, false, ".cnmt.nca");
    if content_number > 1 {
        let (file, mcstring, mgame) = choosecnmt(&cnmtfiles);
        get_dbdict(file.as_deref(), content_number, mcstring, mgame)
    } else {
        get_dbdict(cnmtfiles[0][0].as_str(), content_number)
    }
}

fn memoryload(filelist: &[Vec<String>], target: bool, ender: &str) {
    for entry in filelist {
        let file = &entry[0];
        let size = u64::from_str_radix(&entry[1], 16).unwrap();
        let initpath = &entry[2];
        let off1 = u64::from_str_radix(&entry[3], 16).unwrap();
        let endpath = &entry[4];
        let off2 = u64::from_str_radix(&entry[5], 16).unwrap();
        if file.to_lowercase() == target.to_lowercase() {
            if initpath == endpath {
                let mut f = File::open(initpath).unwrap();
                f.seek(SeekFrom::Start(off1)).unwrap();
                let mut inmemoryfile = vec![0; size as usize];
                f.read_exact(&mut inmemoryfile).unwrap();
                let nca = Nca::new();
                nca.open(&inmemoryfile[..]);
                nca.read_cnmt();
            }
        } else if !target && ender != "" {
            if file.to_lowercase().ends_with(ender) {
                if initpath == endpath {
                    let mut f = File::open(initpath).unwrap();
                    f.seek(SeekFrom::Start(off1)).unwrap();
                    let mut inmemoryfile = vec![0; size as usize];
                    f.read_exact(&mut inmemoryfile).unwrap();
                    let nca_header = NcaHeader::new();
                    f.seek(SeekFrom::Start(off1)).unwrap();
                    nca_header.open(&inmemoryfile[..], Type::Crypto::XTS, &uhx(Keys::get("header_key")));
                    // nca_header.seek(0x400);
                    let mut nca3 = NCA3::new(&inmemoryfile[..], 0, file, &nca_header.title_key_dec);
                    for sec in nca3.sections {
                        if sec.fs_type == "RomFS" {
                            continue;
                        }
                        for buf in sec.decrypt_raw() {
                            Hex::dump(&buf);
                            // if file.ends_with('.cnmt') {
                            //     DAT = sec.fs.open(file);
                            //     for test in DAT {
                            //         Hex::dump(&test);
                            //     }
                            //     println!("{:?}", DAT);
                            // }
                        }
                    }
                }
            }
        }
    }
}

fn open_cnmt(nca: &Nca) -> Option<File> {
    for sec in &nca.sections {
        if sec.fs_type == "RomFS" {
            continue;
        }
        for file in sec.fs.files {
            if file.ends_with(".cnmt") {
                return Some(sec.fs.open(file));
            }
        }
    }
    None
}

fn print_cnmt(cnmt: &Cnmt) {
    println!("{} v{}:", cnmt.tid, cnmt.ver);
    if cnmt.title_type == "SystemUpdate" {
        println!("  Titles:");
        for (tid, d) in &cnmt.data {
            println!("  {}: ", tid);
            println!("    Type:  {}", d["Type"]);
            println!("    Version: {}", d["Version"]);
        }
    } else {
        println!("  Total title size: {}", bytes2human(cnmt.title_size));
        println!("  Files:");
        for (_, ncas) in &cnmt.data {
            if !ncas.is_empty() {
                for (nca_id, d) in ncas {
                    println!("  {}.nca:", nca_id);
                    println!("    Size:   {}", bytes2human(d["Size"]));
                    println!("    SHA256: {}", hx(&d["Hash"]).decode());
                }
            }
        }
    }
}

fn choosecnmt(cnmtnames: &[Vec<String>]) -> (Option<&str>, String, bool) {
    let mut file = None;
    let mut titleid = None;
    let mut nG = 0;
    let mut nU = 0;
    let mut nD = 0;
    let mut mcstring = String::new();
    let mut mGame = false;
    for nca in cnmtnames {
        if nca[0] == "Nca" {
            if titleid.is_none() {
                file = Some(nca[0].as_str());
            }
            titleid = Some(nca[1].clone());
            if titleid.as_ref().unwrap().ends_with("000") {
                nG += 1;
            } else if titleid.as_ref().unwrap().ends_with("800") {
                if nU == 0 && nG < 2 {
                    file = Some(nca[0].as_str());
                }
                nU += 1;
            } else {
                nD += 1;
            }
        }
    }
    if nG > 0 {
        mcstring += &format!("{} Game", nG);
        if nG > 1 {
            mcstring += "s";
            mGame = true;
        }
    }
    if nU > 0 {
        if nG > 0 {
            mcstring += ", ";
        }
        mcstring += &format!("{} Update", nU);
        if nU > 1 {
            mcstring += "s";
        }
    }
    if nD > 0 {
        if nG > 0 || nU > 0 {
            mcstring += ", ";
        }
        mcstring += &format!("{} DLC", nD);
        if nD > 1 {
            mcstring += "s";
        }
    }
    (file, mcstring, mGame)
}

fn get_dbdict(file: Option<&str>, content_number: usize, mcstring: String, mgame: bool) -> serde_json::Value {
    // Implement the logic to get the DB dictionary based on the provided parameters
    // This is a placeholder and needs to be implemented based on the actual logic
    serde_json::json!({})
}


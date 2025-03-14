extern crate aes128;
extern crate hex;
extern crate sha2;
extern crate num_bigint;
extern crate num_traits;
extern crate crypto;
extern crate image;
extern crate textwrap;
extern crateindicatif;

use aes128::{Aes128, BlockEncrypt, NewBlockEncrypt};
use crypto::{buffer, buffer::BufferResult, symmetriccipher::SymmetricCipherError};
use hex::{FromHex, ToHex};
use sha2::{Sha256, Sha1};
use num_bigint::{BigInt, Sign};
use num_traits::{FromPrimitive, ToPrimitive};
use std::fs::File;
use std::io::{Read, Write, Seek, SeekFrom, Cursor};
use std::path::Path;
use std::io::prelude::*;
use std::io::BufReader;
use std::io::BufWriter;
use std::collections::HashMap;
use indicatif::ProgressBar;
use image::GenericImageView;
use textwrap::fill;

const MEDIA_SIZE: u64 = 0x200;
const BUFFER_SIZE: usize = 65536;
const INDENT: usize = 1;
const TABS: &str = "\t";

fn read_int8(f: &mut dyn Read, byteorder: ByteOrder, signed: bool) -> i8 {
    let mut buffer = [0; 1];
    f.read_exact(&mut buffer).unwrap();
    i8::from_le_bytes(buffer)
}

fn read_int16(f: &mut dyn Read, byteorder: ByteOrder, signed: bool) -> i16 {
    let mut buffer = [0; 2];
    f.read_exact(&mut buffer).unwrap();
    i16::from_le_bytes(buffer)
}

fn read_int32(f: &mut dyn Read, byteorder: ByteOrder, signed: bool) -> i32 {
    let mut buffer = [0; 4];
    f.read_exact(&mut buffer).unwrap();
    i32::from_le_bytes(buffer)
}

fn read_int64(f: &mut dyn Read, byteorder: ByteOrder, signed: bool) -> i64 {
    let mut buffer = [0; 8];
    f.read_exact(&mut buffer).unwrap();
    i64::from_le_bytes(buffer)
}

fn read_int128(f: &mut dyn Read, byteorder: ByteOrder, signed: bool) -> i128 {
    let mut buffer = [0; 16];
    f.read_exact(&mut buffer).unwrap();
    i128::from_le_bytes(buffer)
}

fn get_section_filesystem(buffer: &[u8], crypto_key: &[u8]) -> Box<dyn FsType> {
    match buffer[0x3] {
        0x1 => Box::new(Pfs0::new(buffer, Some(crypto_key))),
        0x2 => Box::new(Rom::new(buffer, Some(crypto_key))),
        _ => Box::new(BaseFs::new(buffer, Some(crypto_key))),
    }
}

fn html_feed(feed: &str, style: u8, message: &str) -> String {
    match style {
        1 => format!("<p style=\"font-size: 14px; justify;text-justify: inter-word;\"><strong>{}</strong></p>", message),
        2 => format!("<p style=\"margin-bottom: 2px;margin-top: 2px;font-size: 2vh\"><strong>{}</strong></p>", message),
        3 => format!("<li style=\"margin-bottom: 2px;margin-top: 3px\"><strong>{} </strong><span>{}</span></li>", message[0], message[1]),
        4 => format!("<li style=\"margin-bottom: 2px;margin-top: 3px\"><strong>{} </strong><span>{}. </span><strong>{} </strong><strong>{}</strong></li>", message[0], message[1], message[2], message[3]),
        5 => format!("<p style=\"margin-bottom: 2px;margin-top: 2px;font-size: 2vh;text-indent:5vh;\"><strong style=\"text-indent:5vh;\">{}</strong></p>", message),
        6 => format!("<p style=\"margin-bottom: 2px;margin-top: 2px;font-size: 1.8vh;\"><strong>{}</strong></p>", message),
        7 => format!("<p style=\"margin-bottom: 2px;margin-top: 2px;font-size: 1.8vh;\"><strong>{}</strong>{}</p>", message[0], message[1]),
        _ => feed.to_string(),
    }
}

fn file_location(filepath: &str, t: &str, name: Option<&str>, print_data: bool) -> Vec<(String, u64, String, u64, String, u64)> {
    let filenames = ret_chunks(filepath);
    let mut locations = Vec::new();

    let files_list = if filepath.ends_with(".xc0") {
        ret_xci_offsets(filepath)
    } else if filepath.ends_with(".ns0") {
        ret_nsp_offsets(filepath)
    } else if filepath.ends_with("00") {
        let mut f = File::open(filepath).unwrap();
        let mut magic1 = [0; 4];
        f.read_exact(&mut magic1).unwrap();
        f.seek(SeekFrom::Start(0x100)).unwrap();
        let mut magic2 = [0; 4];
        f.read_exact(&mut magic2).unwrap();
        if magic1 == [b'P', b'F', b'S', b'0'] {
            ret_nsp_offsets(filepath)
        } else if magic2 == [b'H', b'E', b'A', b'D'] {
            ret_xci_offsets(filepath)
        } else {
            println!("Error. File isn't xci or nsp type");
            return locations;
        }
    } else {
        println!("Error. File isn't xci or nsp type");
        return locations;
    };

    for file in files_list {
        if let Some(name) = name {
            if file.0.to_lowercase() == name.to_lowercase() {
                let (location1, tgoffset1) = get_file_and_offset(&filenames, file.1);
                let (location2, tgoffset2) = get_file_and_offset(&filenames, file.2);
                locations.push((file.0, file.3, location1, tgoffset1, location2, tgoffset2));
                if print_data {
                    println!("{}", file.0);
                    println!("- Starts in file {} at offset {}", location1, tgoffset1);
                    println!("- Ends in file {} at offset {}", location2, tgoffset2);
                }
            }
        } else if t != "all" {
            if file.0.to_lowercase().ends_with(t.to_lowercase()) {
                let (location1, tgoffset1) = get_file_and_offset(&filenames, file.1);
                let (location2, tgoffset2) = get_file_and_offset(&filenames, file.2);
                locations.push((file.0, file.3, location1, tgoffset1, location2, tgoffset2));
                if print_data {
                    println!("{}", file.0);
                    println!("- Starts in file {} at offset {}", location1, tgoffset1);
                    println!("- Ends in file {} at offset {}", location2, tgoffset2);
                }
            }
        } else {
            let (location1, tgoffset1) = get_file_and_offset(&filenames, file.1);
            let (location2, tgoffset2) = get_file_and_offset(&filenames, file.2);
            locations.push((file.0, file.3, location1, tgoffset1, location2, tgoffset2));
            if print_data {
                println!("{}", file.0);
                println!("- Starts in file {} at offset {}", location1, tgoffset1);
                println!("- Ends in file {} at offset {}", location2, tgoffset2);
            }
        }
    }

    locations
}

fn get_file_and_offset(filelist: &[(String, u64)], targetoffset: u64) -> (String, u64) {
    let mut startoffset = 0;
    let mut endoffset = 0;

    for &(ref filepath, size) in filelist {
        startoffset = endoffset;
        endoffset += size;

        if targetoffset > endoffset {
            continue;
        } else {
            let partialoffset = targetoffset - startoffset;
            return (filepath.clone(), partialoffset);
        }
    }

    (String::new(), 0)
}

fn nacp_data(nca: &Nca) -> HashMap<String, String> {
    let mut dict = HashMap::new();
    let mut f = Cursor::new(nca.ret_nacp());
    let nacp = Nacp::new();

    dict.insert("RegionalNames".to_string(), nacp.get_name_and_pub(&mut f, 0x300 * 15));
    dict.insert("RegionalEditors".to_string(), nacp.get_name_and_pub(&mut f, 0x300 * 15));
    f.seek(SeekFrom::Start(0x3000)).unwrap();
    dict.insert("ISBN".to_string(), nacp.get_isbn(&mut f, 0x24));
    f.seek(SeekFrom::Start(0x3025)).unwrap();
    dict.insert("StartupUserAccount".to_string(), nacp.get_startup_user_account(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("UserAccountSwitchLock".to_string(), nacp.get_user_account_switch_lock(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("AddOnContentRegistrationType".to_string(), nacp.get_add_on_content_registration_type(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("ctype".to_string(), nacp.get_content_type(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("ParentalControl".to_string(), nacp.get_parental_control(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("ScreenshotsEnabled".to_string(), nacp.get_screenshot(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("VideocaptureEnabled".to_string(), nacp.get_video_capture(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("dataLossConfirmation".to_string(), nacp.get_data_loss_confirmation(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("PlayLogPolicy".to_string(), nacp.get_play_log_policy(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("PresenceGroupId".to_string(), nacp.get_presence_group_id(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3040)).unwrap();
    dict.insert("AgeRatings".to_string(), nacp.get_rating_age(&mut f, 0x20));
    f.seek(SeekFrom::Start(0x3060)).unwrap();
    dict.insert("BuildNumber".to_string(), nacp.get_display_version(&mut f, 0xF));
    f.seek(SeekFrom::Start(0x3070)).unwrap();
    dict.insert("AddOnContentBaseId".to_string(), nacp.get_add_on_content_base_id(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3078)).unwrap();
    dict.insert("SaveDataOwnerId".to_string(), nacp.get_save_data_owner_id(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3080)).unwrap();
    dict.insert("UserAccountSaveDataSize".to_string(), nacp.get_user_account_save_data_size(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3088)).unwrap();
    dict.insert("UserAccountSaveDataJournalSize".to_string(), nacp.get_user_account_save_data_journal_size(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3090)).unwrap();
    dict.insert("DeviceSaveDataSize".to_string(), nacp.get_device_save_data_size(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3098)).unwrap();
    dict.insert("DeviceSaveDataJournalSize".to_string(), nacp.get_device_save_data_journal_size(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x30A0)).unwrap();
    dict.insert("BcatDeliveryCacheStorageSize".to_string(), nacp.get_bcat_delivery_cache_storage_size(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x30A8)).unwrap();
    dict.insert("ApplicationErrorCodeCategory".to_string(), nacp.get_application_error_code_category(&mut f, 0x07));
    f.seek(SeekFrom::Start(0x30B0)).unwrap();
    dict.insert("LocalCommunicationId".to_string(), nacp.get_local_communication_id(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x30F0)).unwrap();
    dict.insert("LogoType".to_string(), nacp.get_logo_type(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("LogoHandling".to_string(), nacp.get_logo_handling(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("RuntimeAddOnContentInstall".to_string(), nacp.get_runtime_add_on_content_install(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("CrashReport".to_string(), nacp.get_crash_report(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("Hdcp".to_string(), nacp.get_hdcp(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("SeedForPseudoDeviceId".to_string(), nacp.get_seed_for_pseudo_device_id(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3100)).unwrap();
    dict.insert("BcatPassphrase".to_string(), nacp.get_bcat_passphrase(&mut f, 0x40));
    f.seek(SeekFrom::Start(0x3148)).unwrap();
    dict.insert("UserAccountSaveDataSizeMax".to_string(), nacp.get_user_account_save_data_size_max(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3150)).unwrap();
    dict.insert("UserAccountSaveDataJournalSizeMax".to_string(), nacp.get_user_account_save_data_journal_size_max(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3158)).unwrap();
    dict.insert("DeviceSaveDataSizeMax".to_string(), nacp.get_device_save_data_size_max(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3160)).unwrap();
    dict.insert("DeviceSaveDataJournalSizeMax".to_string(), nacp.get_device_save_data_journal_size_max(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3168)).unwrap();
    dict.insert("TemporaryStorageSize".to_string(), nacp.get_temporary_storage_size(read_int64(&mut f, ByteOrder::Little, false)));
    dict.insert("CacheStorageSize".to_string(), nacp.get_cache_storage_size(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3178)).unwrap();
    dict.insert("CacheStorageJournalSize".to_string(), nacp.get_cache_storage_journal_size(read_int64(&mut f, ByteOrder::Little, false)));
    dict.insert("CacheStorageDataAndJournalSizeMax".to_string(), nacp.get_cache_storage_data_and_journal_size_max(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3188)).unwrap();
    dict.insert("CacheStorageIndexMax".to_string(), nacp.get_cache_storage_index_max(read_int64(&mut f, ByteOrder::Little, false)));
    dict.insert("PlayLogQueryableApplicationId".to_string(), nacp.get_play_log_queryable_application_id(read_int64(&mut f, ByteOrder::Little, false)));
    f.seek(SeekFrom::Start(0x3210)).unwrap();
    dict.insert("PlayLogQueryCapability".to_string(), nacp.get_play_log_query_capability(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("Repair".to_string(), nacp.get_repair(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("ProgramIndex".to_string(), nacp.get_program_index(read_int8(&mut f, ByteOrder::Little, false)));
    dict.insert("RequiredNetworkServiceLicenseOnLaunch".to_string(), nacp.get_required_network_service_license_on_launch(read_int8(&mut f, ByteOrder::Little, false)));

    dict
}

fn retchunks(filepath: &str) -> io::Result<Vec<(PathBuf, u64)>> {
    let mut file_list = Vec::new();
    let filepath = Path::new(filepath);
    let bname = filepath.file_stem().and_then(|s| s.to_str()).unwrap_or("").to_string();
    let bn = if bname != "00" {
        bname.trim_end_matches("0123456789").to_string()
    } else {
        String::new()
    };

    let (outname, ender) = if filepath.ends_with(".xc0") {
        (format!("{}.xci", bn), ".xc")
    } else if filepath.ends_with(".ns0") {
        (format!("{}.nsp", bn), ".ns")
    } else if bname.ends_with("00") {
        ("output.nsp".to_string(), "0")
    } else {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, "Not valid file"));
    };

    let ruta = filepath.parent().ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "No parent directory found"))?;

    for entry in fs::read_dir(ruta)? {
        let entry = entry?;
        let f = entry.file_name().to_str().unwrap_or("").to_string();
        let check = &f[f.len() - 4..f.len() - 1];
        if check == ender && bname[..bname.len() - 1] == f[..f.len() - 1] {
            if let Ok(n) = f[f.len() - 1..].parse::<i32>() {
                let fp = entry.path();
                let size = fs::metadata(&fp)?.len();
                file_list.push((fp, size));
            }
        }
    }

    file_list.sort_by_key(|k| k.0.clone());
    Ok(file_list)
}



struct Chunk {
    maincontrol: Option<String>,
    nacpdata: Option<String>,
    cmtdata: Option<String>,
    maintitle_key: bool,
    maindeckey: bool,
    main_program_nca: Option<String>,
    firstchunk: String,
    chunklist: Vec<String>,
    filelist: Vec<String>,
    nca_list: Vec<String>,
    cnmtfiles: Vec<String>,
    maincnmt: String,
    ctype: String,
    maintitleid: String,
    mainbaseid: String,
}

impl Chunk {
    fn new(filepath: &str, chunk_type: &str, locations: Option<&str>, files: Option<&str>, fileopen: Option<&str>) -> Self {
        let maincontrol = None;
        let nacpdata = None;
        let cmtdata = None;
        let maintitle_key = false;
        let maindeckey = false;
        let main_program_nca = None;
        let firstchunk = filepath.to_string();
        let chunklist = ret_chunks(filepath);
        let (filelist, nca_list) = Self::get_filelist(&firstchunk);
        let cnmtfiles = file_location(filepath, ".cnmt.nca", false);
        let maincnmt = Self::choose_cnmt(&cnmtfiles);
        let cnmt_data = Self::get_cnmt_data(&maincnmt);
        let ctype = cnmt_data["ctype"].clone();
        let maintitleid = cnmt_data["titleid"].clone();
        let mainbaseid = cnmt_data["baseid"].clone();
        let db_get_titlekey = Self::db_get_titlekey();
        
        if ctype != "DLC" {
            let main_control_nca = Self::get_main_control_nca();
            let nacp_data = Self::get_nacp_data();
            let main_program_nca = Self::get_main_program_nca();
        }

        Self {
            maincontrol,
            nacpdata,
            cmtdata,
            maintitle_key,
            maindeckey,
            main_program_nca,
            firstchunk,
            chunklist,
            filelist,
            nca_list,
            cnmtfiles,
            maincnmt,
            ctype,
            maintitleid,
            mainbaseid,
        }
    }

    fn get_filelist(filepath: &str) -> (Vec<String>, Vec<String>) {
        let filedata = file_location(filepath);
        let mut filelist = Vec::new();
        let mut ncalist = Vec::new();
        
        for entry in filedata {
            filelist.push(entry[0].clone());
            if entry[0].ends_with(".nca") {
                ncalist.push(entry[0].clone());
            }
        }
        
        (filelist, ncalist)
    }

    fn choose_cnmt(cnmtfiles: &Vec<String>) -> String {
        if cnmtfiles.len() < 2 {
            return cnmtfiles[0].clone();
        }
        
        // Placeholder for the logic to choose the main cnmt file
        cnmtfiles[0].clone()
    }

    fn get_cnmt_data(maincnmt: &str) -> serde_json::Value {
        let nca = Nca::new();
        nca.open(MemoryFile::new(self.memoryload(maincnmt).read()));
        nca.rewind();
        let cnmt = io::BytesIO::new(nca.return_cnmt());
        let nca_name = maincnmt.to_string();
        let (titleid, titleversion, base_id, keygeneration, rights_id, rsv, rgv, ctype, metasdkversion, exesdkversion, has_html_manual, installed_size, delta_size, ncadata) = Self::cnmt_data(&cnmt, &nca, &nca_name);
        
        let mut d = serde_json::Map::new();
        d.insert("titleid".to_string(), titleid.into());
        d.insert("version".to_string(), titleversion.into());
        d.insert("baseid".to_string(), base_id.into());
        d.insert("keygeneration".to_string(), keygeneration.into());
        d.insert("rightsId".to_string(), rights_id.into());
        d.insert("rsv".to_string(), rsv.into());
        d.insert("rgv".to_string(), rgv.into());
        d.insert("ctype".to_string(), ctype.into());
        d.insert("metasdkversion".to_string(), metasdkversion.into());
        d.insert("exesdkversion".to_string(), exesdkversion.into());
        d.insert("hasHtmlManual".to_string(), has_html_manual.into());
        d.insert("Installedsize".to_string(), installed_size.into());
        d.insert("DeltaSize".to_string(), delta_size.into());
        d.insert("ncadata".to_string(), ncadata.into());
        
        serde_json::Value::Object(d)
    }

    fn read_cnmt(&self) -> String {
        let mut feed = String::new();
        
        for entry in &self.cnmtfiles {
            let nca = Nca::new();
            nca.open(MemoryFile::new(self.memoryload(entry).read()));
            nca._path = entry.clone();
            feed += &nca.read_cnmt();
        }
        
        feed
    }

    fn send_html_cnmt_data(&self) -> String {
        let mut feed = String::new();
        
        for entry in &self.cnmtfiles {
            let nca = ChromeNca::new();
            nca.open(MemoryFile::new(self.memoryload(entry).read()));
            nca._path = entry.clone();
            feed += &nca.read_cnmt();
        }
        
        feed
    }


fn get_main_control_nca(&mut self) {
    let ncadata = &self.cnmtdata["ncadata"];
    let mut ncaname = String::new();
    for entry in ncadata {
        if entry["NCAtype"].to_lowercase() == "control" {
            ncaname = format!("{}.nca", entry["NcaId"]);
            break;
        }
    }
    let results = file_location(self.firstchunk, name=ncaname, print_data=false);
    self.maincontrol = results[0];
}

fn get_nacp_data(&mut self) {
    let mut nca = Nca::new();
    nca.open(MemoryFile::new(self.memoryload(&self.maincontrol).read()));
    nca.rewind();
    self.nacpdata = nacp_data(&nca);
    nca.rewind();
    let (title, editor, sup_lg, ctype) = self.db_get_names(&nca);
    self.nacpdata.insert("title", title);
    self.nacpdata.insert("editor", editor);
    self.nacpdata.insert("SupLg", sup_lg);
    self.ctype = ctype;
}

fn memoryload(&self, filedata: &[u8]) -> io::Result<io::Cursor<Vec<u8>>> {
    if filedata[2] == filedata[4] {
        let mut f = File::open(filedata[2])?;
        f.seek(SeekFrom::Start(filedata[3] as u64))?;
        let mut inmemoryfile = io::Cursor::new(Vec::new());
        io::copy(&mut f.take((filedata[5] - filedata[3]) as u64), &mut inmemoryfile)?;
        Ok(inmemoryfile)
    } else {
        Err(io::Error::new(io::ErrorKind::InvalidInput, "Invalid file data"))
    }
}

fn read_at(&self, filedata: &[u8], start: usize, length: usize) -> io::Result<Vec<u8>> {
    let ck_size = fs::metadata(filedata[2])?.len() as usize;
    let mut initial_offset = filedata[3] as usize;
    let mut current = filedata[2].to_string();
    while (initial_offset + start) > ck_size {
        initial_offset = 0;
        start -= ck_size;
        current.pop();
        current.push((current.pop().unwrap() as u8 + 1) as char);
        ck_size = fs::metadata(&current)?.len() as usize;
    }
    let mut f = File::open(current)?;
    f.seek(SeekFrom::Start(initial_offset as u64 + start as u64))?;
    let mut data = vec![0; length];
    f.read_exact(&mut data)?;
    Ok(data)
}

fn db_get_names(&self, nca: &Nca) -> (String, String, String, String) {
    let ctype = self.ctype.clone();
    let (title, editor, ediver, sup_lg, regionstr, isdemo) = nca.get_langueblock("DLC", roman=true);
    let ctype = match ctype.as_str() {
        "GAME" => {
            if isdemo == 1 {
                "DEMO".to_string()
            } else if isdemo == 2 {
                "RETAILINTERACTIVEDISPLAY".to_string()
            } else {
                ctype
            }
        }
        "UPDATE" => {
            if isdemo == 1 {
                "DEMO UPDATE".to_string()
            } else if isdemo == 2 {
                "RETAILINTERACTIVEDISPLAY UPDATE".to_string()
            } else {
                ctype
            }
        }
        _ => ctype,
    };
    (title, editor, sup_lg, ctype)
}

fn db_get_names_from_nutdb(&self) -> (String, String, String) {
    let titleid = self.maintitleid;
    match nutdb.get_dlcData(titleid) {
        Ok((sqname, sqeditor)) => {
            let sup_lg = nutdb.get_content_langue(titleid).unwrap_or("-".to_string());
            (sqname, sqeditor, sup_lg)
        }
        Err(e) => {
            eprintln!("Exception: {}", e);
            ("-".to_string(), "-".to_string(), "-".to_string())
        }
    }
}

fn db_get_titlekey(&mut self) {
    let mut title_key = None;
    let mut deckey = None;
    let rights_id = &self.cnmtdata["rightsId"];
    let key_generation = &self.cnmtdata["keygeneration"];
    let has_rights = rights_id != "0";
    if let Ok(rights_id) = u64::from_str_radix(rights_id, 16) {
        if has_rights {
            let tkname = format!("{}.tik", rights_id.to_string().to_lowercase());
            if let Some(ticket) = file_location(filepath, name=tkname, print_data=false).first() {
                let mut tk = Ticket::new();
                tk.open(MemoryFile::new(self.memoryload(ticket).read()));
                tk.rewind();
                let title_key_block = tk.get_title_key_block();
                title_key = Some(hex::encode(title_key_block.to_bytes().to_vec()));
                deckey = Some(hex::encode(Keys::decrypt_title_key(
                    title_key_block.to_bytes().to_vec(),
                    Keys::get_master_key_index(key_generation.parse().unwrap()),
                )));
            }
        }
    }
    self.maintitle_key = title_key;
    self.main_deckey = deckey;
}


fn get_db_dict(&self) -> Result<HashMap<String, String>, Box<dyn std::error::Error>> {
    let ctype = self.ctype.clone();
    let mut db_dict: HashMap<String, String> = HashMap::new();

    let (sqname, sqeditor, sup_lg) = if ctype != "DLC" {
        let nacp_data = self.nacpdata.clone();
        (
            nacp_data.get("title").unwrap_or(&"-".to_string()).clone(),
            nacp_data.get("editor").unwrap_or(&"-".to_string()).clone(),
            nacp_data.get("SupLg").unwrap_or(&"-".to_string()).clone(),
        )
    } else {
        self.db_get_names_from_nutdb()?
    };

    let title_key = self.maintitle_key.clone();
    let deckey = self.maindeckey.clone();

    // cnmt flags
    let cnmt_data = self.cnmtdata.clone();
    db_dict.insert("id".to_string(), cnmt_data.get("titleid").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("baseid".to_string(), cnmt_data.get("baseid").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("rightsId".to_string(), cnmt_data.get("rightsId").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("Type".to_string(), ctype.clone());
    db_dict.insert("version".to_string(), cnmt_data.get("version").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("keygeneration".to_string(), cnmt_data.get("keygeneration").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("RSV".to_string(), cnmt_data.get("rsv").unwrap_or(&"-".to_string()).clone()[1..cnmt_data.get("rsv").unwrap_or(&"-".to_string()).len() - 1].to_string());
    db_dict.insert("RGV".to_string(), cnmt_data.get("rgv").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("metasdkversion".to_string(), cnmt_data.get("metasdkversion").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("exesdkversion".to_string(), cnmt_data.get("exesdkversion").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("InstalledSize".to_string(), cnmt_data.get("Installedsize").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("deltasize".to_string(), cnmt_data.get("DeltaSize").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("HtmlManual".to_string(), cnmt_data.get("hasHtmlManual").unwrap_or(&"-".to_string()).clone());
    db_dict.insert("ncasizes".to_string(), cnmt_data.get("ncadata").unwrap_or(&"-".to_string()).clone());

    // nacpt flags
    if ctype != "DLC" {
        db_dict.insert("baseName".to_string(), sqname.clone());
        db_dict.insert("contentname".to_string(), "-".to_string());
    } else {
        db_dict.insert("baseName".to_string(), "-".to_string());
        db_dict.insert("contentname".to_string(), sqname.clone());
    }
    db_dict.insert("editor".to_string(), sqeditor.clone());
    db_dict.insert("languages".to_string(), sup_lg.clone());

    if ctype != "DLC" {
        let nacp_dict = self.nacpdata.clone();
        if let (Some(startup_user_account), Some(required_network_service_license_on_launch)) = (
            nacp_dict.get("StartupUserAccount"),
            nacp_dict.get("RequiredNetworkServiceLicenseOnLaunch"),
        ) {
            db_dict.insert("linkedAccRequired".to_string(), if startup_user_account == "RequiredWithNetworkServiceAccountAvailable" || required_network_service_license_on_launch != "None" {
                "True".to_string()
            } else {
                "False".to_string()
            });
        }
        if let Some(build_number) = nacp_dict.get("BuildNumber") {
            db_dict.insert("dispversion".to_string(), build_number.clone());
        }
        if let Some(regional_names) = nacp_dict.get("RegionalNames") {
            db_dict.insert("RegionalBaseNames".to_string(), regional_names.clone());
        }
        db_dict.insert("RegionalContentNames".to_string(), "-".to_string());
        if let Some(regional_editors) = nacp_dict.get("RegionalEditors") {
            db_dict.insert("RegionalEditors".to_string(), regional_editors.clone());
        }
        if let Some(age_ratings) = nacp_dict.get("AgeRatings") {
            db_dict.insert("AgeRatings".to_string(), age_ratings.clone());
        }
        if let Some(isbn) = nacp_dict.get("ISBN") {
            db_dict.insert("isbn".to_string(), isbn.clone());
        }
        if let Some(startup_user_account) = nacp_dict.get("StartupUserAccount") {
            db_dict.insert("StartupUserAccount".to_string(), startup_user_account.clone());
        }
        if let Some(user_account_switch_lock) = nacp_dict.get("UserAccountSwitchLock") {
            db_dict.insert("UserAccountSwitchLock".to_string(), user_account_switch_lock.clone());
        }
        if let Some(add_on_content_registration_type) = nacp_dict.get("AddOnContentRegistrationType") {
            db_dict.insert("AddOnContentRegistrationType".to_string(), add_on_content_registration_type.clone());
        }
        if let Some(ctype) = nacp_dict.get("ctype") {
            db_dict.insert("ctype".to_string(), ctype.clone());
        }
        if let Some(parental_control) = nacp_dict.get("ParentalControl") {
            db_dict.insert("ParentalControl".to_string(), parental_control.clone());
        }
        if let Some(screenshots_enabled) = nacp_dict.get("ScreenshotsEnabled") {
            db_dict.insert("ScreenshotsEnabled".to_string(), screenshots_enabled.clone());
        }
        if let Some(videocapture_enabled) = nacp_dict.get("VideocaptureEnabled") {
            db_dict.insert("VideocaptureEnabled".to_string(), videocapture_enabled.clone());
        }
        if let Some(data_loss_confirmation) = nacp_dict.get("dataLossConfirmation") {
            db_dict.insert("DataLossConfirmation".to_string(), data_loss_confirmation.clone());
        }
        if let Some(play_log_policy) = nacp_dict.get("PlayLogPolicy") {
            db_dict.insert("PlayLogPolicy".to_string(), play_log_policy.clone());
        }
        if let Some(presence_group_id) = nacp_dict.get("PresenceGroupId") {
            db_dict.insert("PresenceGroupId".to_string(), presence_group_id.clone());
        }
        if let Some(add_on_content_base_id) = nacp_dict.get("AddOnContentBaseId") {
            db_dict.insert("AddOnContentBaseId".to_string(), add_on_content_base_id.clone());
        }
        if let Some(save_data_owner_id) = nacp_dict.get("SaveDataOwnerId") {
            db_dict.insert("SaveDataOwnerId".to_string(), save_data_owner_id.clone());
        }
        if let Some(user_account_save_data_size) = nacp_dict.get("UserAccountSaveDataSize") {
            db_dict.insert("UserAccountSaveDataSize".to_string(), user_account_save_data_size.clone());
        }
        if let Some(user_account_save_data_journal_size) = nacp_dict.get("UserAccountSaveDataJournalSize") {
            db_dict.insert("UserAccountSaveDataJournalSize".to_string(), user_account_save_data_journal_size.clone());
        }
        if let Some(device_save_data_size) = nacp_dict.get("DeviceSaveDataSize") {
            db_dict.insert("DeviceSaveDataSize".to_string(), device_save_data_size.clone());
        }
        if let Some(device_save_data_journal_size) = nacp_dict.get("DeviceSaveDataJournalSize") {
            db_dict.insert("DeviceSaveDataJournalSize".to_string(), device_save_data_journal_size.clone());
        }
        if let Some(bcat_delivery_cache_storage_size) = nacp_dict.get("BcatDeliveryCacheStorageSize") {
            db_dict.insert("BcatDeliveryCacheStorageSize".to_string(), bcat_delivery_cache_storage_size.clone());
        }
        if let Some(application_error_code_category) = nacp_dict.get("ApplicationErrorCodeCategory") {
            db_dict.insert("ApplicationErrorCodeCategory".to_string(), application_error_code_category.clone());
        }
        if let Some(local_communication_id) = nacp_dict.get("LocalCommunicationId") {
            db_dict.insert("LocalCommunicationId".to_string(), local_communication_id.clone());
        }
        if let Some(logo_type) = nacp_dict.get("LogoType") {
            db_dict.insert("LogoType".to_string(), logo_type.clone());
        }
        if let Some(logo_handling) = nacp_dict.get("LogoHandling") {
            db_dict.insert("LogoHandling".to_string(), logo_handling.clone());
        }
        if let Some(runtime_add_on_content_install) = nacp_dict.get("RuntimeAddOnContentInstall") {
            db_dict.insert("RuntimeAddOnContentInstall".to_string(), runtime_add_on_content_install.clone());
        }
        if let Some(crash_report) = nacp_dict.get("CrashReport") {
            db_dict.insert("CrashReport".to_string(), crash_report.clone());
        }
        if let Some(hdcp) = nacp_dict.get("Hdcp") {
            db_dict.insert("Hdcp".to_string(), hdcp.clone());
        }
        if let Some(seed_for_pseudo_device_id) = nacp_dict.get("SeedForPseudoDeviceId") {
            db_dict.insert("SeedForPseudoDeviceId".to_string(), seed_for_pseudo_device_id.clone());
        }
        if let Some(bcat_passphrase) = nacp_dict.get("BcatPassphrase") {
            db_dict.insert("BcatPassphrase".to_string(), bcat_passphrase.clone());
        }
        if let Some(user_account_save_data_size_max) = nacp_dict.get("UserAccountSaveDataSizeMax") {
            db_dict.insert("UserAccountSaveDataSizeMax".to_string(), user_account_save_data_size_max.clone());
        }
        if let Some(user_account_save_data_journal_size_max) = nacp_dict.get("UserAccountSaveDataJournalSizeMax") {
            db_dict.insert("UserAccountSaveDataJournalSizeMax".to_string(), user_account_save_data_journal_size_max.clone());
        }
        if let Some(device_save_data_size_max) = nacp_dict.get("DeviceSaveDataSizeMax") {
            db_dict.insert("DeviceSaveDataSizeMax".to_string(), device_save_data_size_max.clone());
        }
        if let Some(device_save_data_journal_size_max) = nacp_dict.get("DeviceSaveDataJournalSizeMax") {
            db_dict.insert("DeviceSaveDataJournalSizeMax".to_string(), device_save_data_journal_size_max.clone());
        }
        if let Some(temporary_storage_size) = nacp_dict.get("TemporaryStorageSize") {
            db_dict.insert("TemporaryStorageSize".to_string(), temporary_storage_size.clone());
        }
        if let Some(cache_storage_size) = nacp_dict.get("CacheStorageSize") {
            db_dict.insert("CacheStorageSize".to_string(), cache_storage_size.clone());
        }
        if let Some(cache_storage_journal_size) = nacp_dict.get("CacheStorageJournalSize") {
            db_dict.insert("CacheStorageJournalSize".to_string(), cache_storage_journal_size.clone());
        }
        if let Some(cache_storage_data_and_journal_size_max) = nacp_dict.get("CacheStorageDataAndJournalSizeMax") {
            db_dict.insert("CacheStorageDataAndJournalSizeMax".to_string(), cache_storage_data_and_journal_size_max.clone());
        }
        if let Some(cache_storage_index_max) = nacp_dict.get("CacheStorageIndexMax") {
            db_dict.insert("CacheStorageIndexMax".to_string(), cache_storage_index_max.clone());
        }
        if let Some(play_log_queryable_application_id) = nacp_dict.get("PlayLogQueryableApplicationId") {
            db_dict.insert("PlayLogQueryableApplicationId".to_string(), play_log_queryable_application_id.clone());
        }
        if let Some(play_log_query_capability) = nacp_dict.get("PlayLogQueryCapability") {
            db_dict.insert("PlayLogQueryCapability".to_string(), play_log_query_capability.clone());
        }
        if let Some(repair) = nacp_dict.get("Repair") {
            db_dict.insert("Repair".to_string(), repair.clone());
        }
        if let Some(program_index) = nacp_dict.get("ProgramIndex") {
            db_dict.insert("ProgramIndex".to_string(), program_index.clone());
        }
        if let Some(required_network_service_license_on_launch) = nacp_dict.get("RequiredNetworkServiceLicenseOnLaunch") {
            db_dict.insert("RequiredNetworkServiceLicenseOnLaunch".to_string(), required_network_service_license_on_launch.clone());
        }
    }

    // ticket flags
    if title_key.is_empty() {
        db_dict.insert("key".to_string(), "-".to_string());
        db_dict.insert("deckey".to_string(), "-".to_string());
    } else {
        db_dict.insert("key".to_string(), title_key.clone());
        db_dict.insert("deckey".to_string(), deckey.clone());
    }

    // Distribution type flags
    if ctype == "GAME" {
        db_dict.insert("DistEshop".to_string(), "-".to_string());
        db_dict.insert("DistCard".to_string(), "True".to_string());
    } else {
        db_dict.insert("DistEshop".to_string(), "-".to_string());
        db_dict.insert("DistCard".to_string(), "True".to_string());
    }

    // xci flags
    db_dict.insert("FWoncard".to_string(), "-".to_string());
    if let Ok(fw_on_card) = self.db_module().fw_db().detect_xci_fw(&self.firstchunk) {
        db_dict.insert("FWoncard".to_string(), fw_on_card);
    }

    if self.firstchunk.ends_with(".xc0") {
        let mut file = std::fs::File::open(&self.firstchunk)?;
        file.seek(0x10D)?;
        let gamecard_size = file.read_u8()?;
        file.seek(0x118)?;
        let valid_data_end_offset = file.read_u64::<LittleEndian>()?;
        let gc_flag = format!("{:X}", gamecard_size).to_uppercase();
        let valid_data = ((valid_data_end_offset + 1) * 0x200) as i64;
        let gc_size = sq_tools::get_gc_size_in_bytes(gc_flag)?;
        db_dict.insert("GCSize".to_string(), gc_size.to_string());
        db_dict.insert("TrimmedSize".to_string(), valid_data.to_string());
    }

    // Check if multicontent
    let content_number = self.cnmtfiles.len();
    db_dict.insert("ContentNumber".to_string(), content_number.to_string());
    if content_number > 1 {
        if self.m_game {
            db_dict.insert("Type".to_string(), "MULTIGAME".to_string());
        } else {
            db_dict.insert("Type".to_string(), "MULTICONTENT".to_string());
        }
        db_dict.insert("InstalledSize".to_string(), sq_tools::get_mc_isize(&self.firstchunk)?.to_string());
    }

    db_dict.insert("nsuId".to_string(), "-".to_string());
    db_dict.insert("genretags".to_string(), "-".to_string());
    db_dict.insert("ratingtags".to_string(), "-".to_string());
    db_dict.insert("worldreleasedate".to_string(), "-".to_string());
    db_dict.insert("numberOfPlayers".to_string(), "-".to_string());
    db_dict.insert("iconUrl".to_string(), "-".to_string());
    db_dict.insert("screenshots".to_string(), "-".to_string());
    db_dict.insert("bannerUrl".to_string(), "-".to_string());
    db_dict.insert("intro".to_string(), "-".to_string());
    db_dict.insert("description".to_string(), "-".to_string());

    let (nsu_id, world_release_date, genre_tags, rating_tags, number_of_players, intro, description, icon_url, screenshots, banner_url, region, rating, developer, product_code, online_play, save_data_cloud, play_modes, video, shop_url) = if ctype == "GAME" || ctype == "DLC" || ctype == "DEMO" {
        nutdb::get_content_data(&self.maintitleid)?
    } else {
        nutdb::get_content_data(&self.mainbaseid)?
    };

    let regions = nutdb::get_content_regions(&self.maintitleid)?;

    if let Some(nsu_id) = nsu_id {
        db_dict.insert("nsuId".to_string(), nsu_id);
    }
    if let Some(genre_tags) = genre_tags {
        db_dict.insert("genretags".to_string(), genre_tags);
    }
    if let Some(rating_tags) = rating_tags {
        db_dict.insert("ratingtags".to_string(), rating_tags);
    }
    if let Some(world_release_date) = world_release_date {
        db_dict.insert("worldreleasedate".to_string(), world_release_date);
    }
    if let Some(number_of_players) = number_of_players {
        db_dict.insert("numberOfPlayers".to_string(), number_of_players);
    }
    if let Some(icon_url) = icon_url {
        db_dict.insert("iconUrl".to_string(), icon_url);
    }
    if let Some(screenshots) = screenshots {
        db_dict.insert("screenshots".to_string(), screenshots);
    }
    if let Some(banner_url) = banner_url {
        db_dict.insert("bannerUrl".to_string(), banner_url);
    }
    if let Some(intro) = intro {
        db_dict.insert("intro".to_string(), intro);
    }
    if let Some(description) = description {
        db_dict.insert("description".to_string(), description);
    }
    if let Some(rating) = rating {
        db_dict.insert("eshoprating".to_string(), rating);
    }
    if let Some(developer) = developer {
        db_dict.insert("developer".to_string(), developer);
    }
    if let Some(product_code) = product_code {
        db_dict.insert("productCode".to_string(), product_code);
    }
    if let Some(online_play) = online_play {
        db_dict.insert("OnlinePlay".to_string(), online_play);
    }
    if let Some(save_data_cloud) = save_data_cloud {
        db_dict.insert("SaveDataCloud".to_string(), save_data_cloud);
    }
    if let Some(play_modes) = play_modes {
        db_dict.insert("playmodes".to_string(), play_modes);
    }
    if let Some(video) = video {
        db_dict.insert("video".to_string(), video);
    }
    if let Some(shop_url) = shop_url {
        db_dict.insert("shopurl".to_string(), shop_url);
	}
     if !regions.is_empty() {
    DBdict.insert("regions".to_string(), regions);
}
let (metascore, userscore, openscore) = nutdb.get_metascores(self.maintitleid);
DBdict.insert("metascore".to_string(), "-".to_string());
DBdict.insert("userscore".to_string(), "-".to_string());
DBdict.insert("openscore".to_string(), "-".to_string());
if metascore != false {
    DBdict.insert("metascore".to_string(), metascore);
}
if userscore != false {
    DBdict.insert("userscore".to_string(), userscore);
}
if openscore != false {
    DBdict.insert("openscore".to_string(), openscore);
}
DBdict
}


	fn send_html_nacp_data(&self, gui: bool) -> String {
    let mut feed = String::new();
    let ncadata = &self.cnmtdata["ncadata"];
    for entry in ncadata {
        if entry["NCAtype"].to_lowercase() == "control" {
            let ncaname = format!("{}.nca", entry["NcaId"]);
            let results = file_location(self.firstchunk, name = ncaname, print_data = false);
            let control = &results[0];
            let mut nca = Nca::new();
            nca.open(MemoryFile::new(self.memoryload(control).read()));
            nca.rewind();
            let titleid2 = nca.header.title_id;
            feed += &html_feed(feed, 1, message = format!("TITLEID: {}", titleid2.to_uppercase()));
            let offset = nca.get_nacp_offset();
            for f in nca {
                f.seek(offset);
                let mut nacp = ChromeNacp::new();
                feed = nacp.par_get_name_and_pub(f.read(0x300 * 15), feed, gui);
                feed = html_feed(feed, 2, message = "Nacp Flags:".to_string());
                feed += "<ul style=\"margin-bottom: 2px;margin-top: 3px\">";
                f.seek(offset + 0x3000);
                feed = nacp.par_isbn(f.read(0x24), feed);
                f.seek(offset + 0x3025);
                feed = nacp.par_get_startup_user_account(f.read_int8('little'), feed);
                feed = nacp.par_get_user_account_switch_lock(f.read_int8('little'), feed);
                feed = nacp.par_get_add_on_content_registration_type(f.read_int8('little'), feed);
                feed = nacp.par_get_content_type(f.read_int8('little'), feed);
                feed = nacp.par_get_parental_control(f.read_int8('little'), feed);
                feed = nacp.par_get_screenshot(f.read_int8('little'), feed);
                feed = nacp.par_get_video_capture(f.read_int8('little'), feed);
                feed = nacp.par_data_loss_confirmation(f.read_int8('little'), feed);
                feed = nacp.par_get_play_log_policy(f.read_int8('little'), feed);
                feed = nacp.par_get_presence_group_id(f.read_int64('little'), feed);
                feed += "</ul>";
                f.seek(offset + 0x3040);
                let mut listages = Vec::new();
                feed = html_feed(feed, 2, message = "Age Ratings:".to_string());
                feed += "<ul style=\"margin-bottom: 2px;margin-top: 3px\">";
                for i in 0..12 {
                    feed = nacp.par_get_rating_age(f.read_int8('little'), i, feed);
                }
                feed += "</ul>";
                f.seek(offset + 0x3060);
                if let Err(_) = nacp.par_get_display_version(f.read(0xF), feed) {
                    feed += "</ul>";
                    continue;
                }
                feed = html_feed(feed, 2, message = "Nacp Attributes:".to_string());
                feed += "<ul style=\"margin-bottom: 2px;margin-top: 3px\">";
                feed = nacp.par_get_add_on_content_base_id(f.read_int64('little'), feed);
                f.seek(offset + 0x3078);
                feed = nacp.par_get_save_data_owner_id(f.read_int64('little'), feed);
                f.seek(offset + 0x3080);
                feed = nacp.par_get_user_account_save_data_size(f.read_int64('little'), feed);
                f.seek(offset + 0x3088);
                feed = nacp.par_get_user_account_save_data_journal_size(f.read_int64('little'), feed);
                f.seek(offset + 0x3090);
                feed = nacp.par_get_device_save_data_size(f.read_int64('little'), feed);
                f.seek(offset + 0x3098);
                feed = nacp.par_get_device_save_data_journal_size(f.read_int64('little'), feed);
                f.seek(offset + 0x30A0);
                feed = nacp.par_get_bcat_delivery_cache_storage_size(f.read_int64('little'), feed);
                f.seek(offset + 0x30A8);
                feed = nacp.par_get_application_error_code_category(f.read(0x07), feed);
                f.seek(offset + 0x30B0);
                feed = nacp.par_get_local_communication_id(f.read_int64('little'), feed);
                f.seek(offset + 0x30F0);
                feed = nacp.par_get_logo_type(f.read_int8('little'), feed);
                feed = nacp.par_get_logo_handling(f.read_int8('little'), feed);
                feed = nacp.par_get_runtime_add_on_content_install(f.read_int8('little'), feed);
                feed = nacp.par_get_crash_report(f.read_int8('little'), feed);
                feed = nacp.par_get_hdcp(f.read_int8('little'), feed);
                feed = nacp.par_get_seed_for_pseudo_device_id(f.read_int64('little'), feed);
                f.seek(offset + 0x3100);
                feed = nacp.par_get_bcat_passphrase(f.read(0x40), feed);
                f.seek(offset + 0x3148);
                feed = nacp.par_user_account_save_data_size_max(f.read_int64('little'), feed);
                f.seek(offset + 0x3150);
                feed = nacp.par_user_account_save_data_journal_size_max(f.read_int64('little'), feed);
                f.seek(offset + 0x3158);
                feed = nacp.par_get_device_save_data_size_max(f.read_int64('little'), feed);
                f.seek(offset + 0x3160);
                feed = nacp.par_get_device_save_data_journal_size_max(f.read_int64('little'), feed);
                f.seek(offset + 0x3168);
                feed = nacp.par_get_temporary_storage_size(f.read_int64('little'), feed);
                feed = nacp.par_get_cache_storage_size(f.read_int64('little'), feed);
                f.seek(offset + 0x3178);
                feed = nacp.par_get_cache_storage_journal_size(f.read_int64('little'), feed);
                feed = nacp.par_get_cache_storage_data_and_journal_size_max(f.read_int64('little'), feed);
                f.seek(offset + 0x3188);
                feed = nacp.par_get_cache_storage_index_max(f.read_int64('little'), feed);
                feed = nacp.par_get_play_log_queryable_application_id(f.read_int64('little'), feed);
                f.seek(offset + 0x3210);
                feed = nacp.par_get_play_log_query_capability(f.read_int8('little'), feed);
                feed = nacp.par_get_repair(f.read_int8('little'), feed);
                feed = nacp.par_get_program_index(f.read_int8('little'), feed);
                feed = nacp.par_get_required_network_service_license_on_launch(f.read_int8('little'), feed);
                feed += "</ul>";
            }
        }
    }
    feed
}


fn send_html_adv_file_list(&self) -> String {
    let mut contentlist: Vec<String> = Vec::new();
    let mut feed = String::new();
    let mut size1 = 0;
    let mut size2 = 0;
    let mut size3 = 0;

    for entry in &self.cnmtfiles {
        let mut nca = Nca::new();
        nca.open(MemoryFile::new(self.memoryload(entry).read()));
        nca.set_path(entry[0].clone());
        nca.rewind();

        for f in &nca {
            for cnmt in f {
                nca.rewind();
                f.rewind();
                cnmt.rewind();
                let titleid = read_int64(cnmt);
                let titleversion = cnmt.read(0x4);
                cnmt.seek(0xE);
                let offset = read_int16(cnmt);
                let content_entries = read_int16(cnmt);
                let meta_entries = read_int16(cnmt);
                cnmt.seek(0x20);
                let original_id = read_int64(cnmt);
                let min_sversion = read_int32(cnmt);
                let length_of_emeta = read_int32(cnmt);
                let target = nca.get_path();
                let content_type_cnmt = cnmt.get_path();
                let content_type_cnmt = content_type_cnmt.trim_end_matches("Patch");
                
                let (reqtag, tit_name, editor, ediver, suplg, content_type) = match content_type_cnmt.as_str() {
                    "Patch" => {
                        ("RequiredSystemVersion: ", self.get_db_dict()["baseName"], self.get_db_dict()["editor"], self.get_db_dict()["dispversion"], self.get_db_dict()["languages"], self.get_db_dict()["ctype"])
                    },
                    "AddOnContent" => {
                        ("RequiredUpdateNumber: ", self.get_db_dict()["contentname"], self.get_db_dict()["editor"], self.get_db_dict()["dispversion"], self.get_db_dict()["languages"], "DLC".to_string())
                    },
                    "Application" => {
                        ("RequiredSystemVersion: ", self.get_db_dict()["baseName"], self.get_db_dict()["editor"], self.get_db_dict()["dispversion"], self.get_db_dict()["languages"], "Game or Application".to_string())
                    },
                    _ => ("", String::new(), String::new(), String::new(), Vec::new(), String::new()),
                };

                cnmt.seek(0x20 + offset);
                let titleid2 = format!("{:X}", titleid);
                let version = format!("{}", i32::from_le_bytes(titleversion.try_into().unwrap()));
                let v_number = version.parse::<i32>().unwrap() / 65536;
                let rs_number = min_sversion / 65536;
                let crypto1 = nca.header.get_crypto_type();
                let crypto2 = nca.header.get_crypto_type2();
                let keygen = if crypto1 == 2 {
                    if crypto1 > crypto2 { crypto1 } else { crypto2 }
                } else {
                    crypto2
                };

                let sdkversion = nca.get_sdkversion();
                let min_rsv = sq_tools::get_min_rsv(keygen, min_sversion);
                let fw_rq = sq_tools::get_fw_range_kg(keygen);
                let rsv_rq = sq_tools::get_fw_range_rsv(min_sversion);
                let rsv_rq_min = sq_tools::get_fw_range_rsv(min_rsv);

                feed += &html_feed(feed.clone(), 1, "TITLEID: ".to_string() + &titleid2.to_uppercase());
                feed += &html_feed(feed.clone(), 2, "- Titleinfo:".to_string());
                feed += "<ul style=\"margin-bottom: 2px;margin-top: 3px\">";
                
                if content_type_cnmt != "AddOnContent" {
                    feed += &html_feed(feed.clone(), 3, vec!["Name:".to_string(), tit_name]);
                    feed += &html_feed(feed.clone(), 3, vec!["Editor:".to_string(), editor]);
                    feed += &html_feed(feed.clone(), 3, vec!["Display Version:".to_string(), ediver]);
                    feed += &html_feed(feed.clone(), 3, vec!["Meta SDK version:".to_string(), sdkversion]);
                    feed += &html_feed(feed.clone(), 3, vec!["Supported Languages:".to_string(), suplg.join(", ")]);
                    feed += &html_feed(feed.clone(), 3, vec!["Content type:".to_string(), content_type]);
                    let data = format!("{} -> {} ({})", version, content_type_cnmt, v_number);
                    feed += &html_feed(feed.clone(), 3, vec!["Version:".to_string(), data]);
                }

                if content_type_cnmt == "AddOnContent" {
                    if tit_name != "DLC" {
                        feed += &html_feed(feed.clone(), 3, vec!["Name:".to_string(), tit_name]);
                        feed += &html_feed(feed.clone(), 3, vec!["Editor:".to_string(), editor]);
                    }
                    feed += &html_feed(feed.clone(), 3, vec!["Content type:".to_string(), "DLC".to_string()]);
                    let dlc_numb = format!("{:014X}", titleid2.parse::<u64>().unwrap());
                    let dlc_numb = u64::from_str_radix(&dlc_numb, 16).unwrap();
                    feed += &html_feed(feed.clone(), 3, vec!["DLC number:".to_string(), format!("{} -> AddOnContent ({})", dlc_numb, dlc_numb)]);
                    feed += &html_feed(feed.clone(), 3, vec!["DLC version Number:".to_string(), format!("{} -> Version ({})", version, v_number)]);
                    feed += &html_feed(feed.clone(), 3, vec!["Meta SDK version:".to_string(), sdkversion]);
                    if !suplg.is_empty() {
                        feed += &html_feed(feed.clone(), 3, vec!["Supported Languages:".to_string(), suplg.join(", ")]);
                    }
                }

                feed += "</ul>";
                feed += &html_feed(feed.clone(), 2, "- Required Firmware:".to_string());
                feed += "<ul style=\"margin-bottom: 2px;margin-top: 3px\">";
                let incl_firm = DBmodule::FWDB::detect_xci_fw(self.firstchunk, false);
                feed += &html_feed(feed.clone(), 3, vec!["Included Firmware:".to_string(), incl_firm.to_string()]);

                if content_type_cnmt == "AddOnContent" {
                    if v_number == 0 {
                        feed += &html_feed(feed.clone(), 3, vec!["Required game version:".to_string(), format!("{} -> Application ({})", min_sversion, rs_number)]);
                    }
                    if v_number > 0 {
                        feed += &html_feed(feed.clone(), 3, vec!["Required game version:".to_string(), format!("{} -> Patch ({})", min_sversion, rs_number)]);
                    }
                } else {
                    feed += &html_feed(feed.clone(), 3, vec![reqtag, format!("{} -> {}", min_sversion, rsv_rq)]);
                }

                feed += &html_feed(feed.clone(), 3, vec!["Encryption (keygeneration):".to_string(), format!("{} -> {}", keygen, fw_rq)]);
                if content_type_cnmt != "AddOnContent" {
                    feed += &html_feed(feed.clone(), 3, vec!["Patchable to:".to_string(), format!("{} -> {}", min_rsv, rsv_rq_min)]);
                } else {
                    feed += &html_feed(feed.clone(), 3, vec!["Patchable to:".to_string(), "DLC -> no RSV to patch".to_string()]);
                }

                feed += "</ul>";
                let mut ncalist: Vec<String> = Vec::new();
                let mut ncasize = 0;
                feed += &html_feed(feed.clone(), 2, "- Nca files (Non Deltas):".to_string());
                feed += "<ul style=\"margin-bottom: 2px;margin-top: 3px\">";

                for _ in 0..content_entries {
                    let vhash = cnmt.read(0x20);
                    let ncaid = cnmt.read(0x10);
                    let size = cnmt.read(0x6);
                    let ncatype = cnmt.read(0x1);
                    let ncatype = u8::from_le_bytes(ncatype.try_into().unwrap());
                    let unknown = cnmt.read(0x1);

                    if ncatype != 6 {
                        let nca_name = format!("{:X}.nca", ncaid);
                        let (s1, new_feed) = self.html_print_nca_by_title(nca_name, ncatype, feed.clone());
                        ncasize += s1;
                        ncalist.push(nca_name.trim_end_matches(".nca").to_string());
                        contentlist.push(nca_name);
                        feed = new_feed;
                    }

                    if ncatype == 6 {
                        let nca_name = format!("{:X}.nca", ncaid);
                        ncalist.push(nca_name.trim_end_matches(".nca").to_string());
                        contentlist.push(nca_name);
                    }
                }

                let nca_meta = nca.get_path();
                ncalist.push(nca_meta.trim_end_matches(".nca").to_string());
                contentlist.push(nca_meta);
                let (s1, new_feed) = self.html_print_nca_by_title(nca_meta, 0, feed.clone());
                ncasize += s1;
                size1 = ncasize;
                let size_pr = sq_tools::get_size(ncasize);
                feed += "</ul>";
                feed += &html_feed(feed.clone(), 5, format!("TOTAL SIZE: {}", size_pr));
                
                if self.actually_has_deltas() == "true" {
                    cnmt.seek(0x20 + offset);
                    for _ in 0..content_entries {
                        let vhash = cnmt.read(0x20);
                        let ncaid = cnmt.read(0x10);
                        let size = cnmt.read(0x6);
                        let ncatype = cnmt.read(0x1);
                        let ncatype = u8::from_le_bytes(ncatype.try_into().unwrap());
                        let unknown = cnmt.read(0x1);
                        if ncatype == 6 {
                            feed += &html_feed(feed.clone(), 2, "- Nca files (Deltas):".to_string());
                            feed += "<ul style=\"margin-bottom: 2px;margin-top: 3px\">";
                            break;
                        }
                    }

                    cnmt.seek(0x20 + offset);
                    ncasize = 0;
                    for _ in 0..content_entries {
                        let vhash = cnmt.read(0x20);
                        let ncaid = cnmt.read(0x10);
                        let size = cnmt.read(0x6);
                        let ncatype = cnmt.read(0x1);
                        let ncatype = u8::from_le_bytes(ncatype.try_into().unwrap());
                        let unknown = cnmt.read(0x1);
                        if ncatype == 6 {
                            let nca_name = format!("{:X}.nca", ncaid);
                            let (s1, new_feed) = self.html_print_nca_by_title(nca_name, ncatype, feed.clone());
                            ncasize += s1;
                            feed = new_feed;
                        }
                    }

                    size2 = ncasize;
                    let size_pr = sq_tools::get_size(ncasize);
                    feed += "</ul>";
                    feed += &html_feed(feed.clone(), 5, format!("TOTAL SIZE: {}", size_pr));
                }

                if self.actually_has_other(&titleid2) == "true" {
                    feed += &html_feed(feed.clone(), 2, "- Other types of files:".to_string());
                    feed += "<ul style=\"margin-bottom: 2px;margin-top: 3px\">";
                    let mut othersize = 0;
                    let (os1, new_feed) = self.html_print_xml_by_title(&contentlist, feed.clone());
                    let (os2, new_feed) = self.html_print_tac_by_title(&titleid2, &contentlist, new_feed);
                    let (os3, new_feed) = self.html_print_jpg_by_title(&contentlist, new_feed);
                    othersize += os1 + os2 + os3;
                    size3 = othersize;
                    let size_pr = sq_tools::get_size(othersize);
                    feed = new_feed;
                    feed += "</ul>";
                    feed += &html_feed(feed.clone(), 5, format!("TOTAL SIZE: {}", size_pr));
                }
            }
        }
    }

    let finalsize = size1 + size2 + size3;
    let size_pr = sq_tools::get_size(finalsize);
    feed += &html_feed(feed.clone(), 2, format!("FULL CONTENT TOTAL SIZE: {}", size_pr));
    self.html_printnonlisted(&contentlist, feed.clone());
    feed
}


fn get_sdkversion(&self, nca_name: &str) -> String {
    let ncadata = file_location(&self.firstchunk, name=nca_name, Printdata=false)[0];
    let mut ncaHeader = NcaHeader::new();
    ncaHeader.open(MemoryFile::new(self.read_at(&ncadata, 0x0, 0x400), Type::Crypto::XTS, uhx(Keys::get("header_key"))));
    ncaHeader.rewind();
    let sdkversion = format!("{}.{}.{}.{}", ncaHeader.sdkVersion4, ncaHeader.sdkVersion3, ncaHeader.sdkVersion2, ncaHeader.sdkVersion1);
    sdkversion
}

fn html_print_nca_by_title(&self, nca_name: &str, ncatype: &str, feed: &str) -> (u64, String) {
    let tab = "\t";
    let mut size = 0;
    let ncadata = file_location(&self.firstchunk, name=nca_name, Printdata=false)[0];
    let filename = &ncadata[0];
    let mut ncaHeader = NcaHeader::new();
    ncaHeader.open(MemoryFile::new(self.read_at(&ncadata, 0x0, 0x400), Type::Crypto::XTS, uhx(Keys::get("header_key"))));
    ncaHeader.rewind();
    size = ncaHeader.size;
    let size_pr = sq_tools::get_size(size);
    let content = &str::from_utf8(&ncaHeader.contentType).unwrap()[8..] + ": ";
    let ncatype = sq_tools::get_type_from_cnmt(ncatype);
    let mut feed = if ncatype != "Meta: " {
        let message = vec![ncatype, filename, "Size:", &size_pr];
        html_feed(feed, 4, &message)
    } else {
        let message = vec![ncatype, filename, "Size:", &size_pr];
        html_feed(feed, 4, &message)
    };
    (size, feed)
}

fn html_print_xml_by_title(&self, contentlist: &mut Vec<String>, feed: &str) -> (u64, String) {
    let tab = "\t";
    let mut size2return = 0;
    let ncalist = &self.nca_list;
    let xml_list = file_location(&self.firstchunk, t=".xml", Printdata=false);
    for entry in xml_list {
        let sz = entry[1];
        let filename = &entry[0];
        let size = sz;
        let size_pr = sq_tools::get_size(size);
        let xml = &filename[..filename.len()-4];
        if ncalist.contains(xml) {
            let message = vec!["XML:", filename, "Size:", &size_pr];
            feed = html_feed(feed, 4, &message);
            contentlist.push(filename.to_string());
            size2return += size;
        }
    }
    (size2return, feed.to_string())
}

fn html_print_tac_by_title(titleid: &str, contentlist: &mut Vec<String>, feed: &str) -> (u64, String) {
    let tab = "\t";
    let mut size2return = 0;
    let ticket_list = file_location(&self.firstchunk, t=".tick", Printdata=false);
    let cert_list = file_location(&self.firstchunk, t=".cert", Printdata=false);
    for entry in ticket_list {
        let filename = &ticket_list[0];
        let sz = &ticket_list[1];
        let size = *sz;
        let size_pr = sq_tools::get_size(size);
        let tik = &filename[..filename.len()-20];
        if tik == titleid {
            let message = vec!["Ticket:", filename, "Size:", &size_pr];
            feed = html_feed(feed, 4, &message);
            contentlist.push(filename.to_string());
            size2return += size;
        }
    }
    for entry in cert_list {
        let filename = &cert_list[0];
        let sz = &cert_list[1];
        let size = *sz;
        let size_pr = sq_tools::get_size(size);
        let cert_id = &filename[..filename.len()-21];
        if cert_id == titleid {
            let message = vec!["Cert:", filename, "Size:", &size_pr];
            feed = html_feed(feed, 4, &message);
            contentlist.push(filename.to_string());
            size2return += size;
        }
    }
    (size2return, feed.to_string())
}

fn html_print_jpg_by_title(&self, contentlist: &mut Vec<String>, feed: &str) -> (u64, String) {
    let mut size2return = 0;
    let tab = "\t";
    let jpg_list = file_location(&self.firstchunk, t=".jpg", Printdata=false);
    let size = jpg_list[1];
    let size_pr = sq_tools::get_size(size);
    let filename = &jpg_list[0];
    let jpg = &filename[..32];
    if self.ncalist.contains(jpg) {
        let message = vec!["JPG:", filename, "Size:", &size_pr];
        feed = html_feed(feed, 4, &message);
        contentlist.push(filename.to_string());
        size2return += size;
    }
    (size2return, feed.to_string())
}

fn actually_has_deltas(&self, feed: &str) -> String {
    let tab = "\t";
    let mut size = 0;
    let vfragment = "false";
    let ncadata = file_location(&self.firstchunk, t=".nca", Printdata=false);
    for entry in ncadata {
        let mut ncaHeader = NcaHeader::new();
        ncaHeader.open(MemoryFile::new(self.read_at(&entry, 0x0, 0x400), Type::Crypto::XTS, uhx(Keys::get("header_key"))));
        ncaHeader.rewind();
        if str::from_utf8(&ncaHeader.contentType).unwrap() == "Content.DATA" {
            if self.ncalist.contains(&entry[0]) {
                vfragment = "true";
                break;
            }
        }
    }
    vfragment.to_string()
}

fn actually_has_other(&self, titleid: &str) -> String {
    let vother = "false";
    let files_list = &self.filelist;
    let ncalist = &self.nca_list;
    for i in 0..files_list.len() {
        let filename = &files_list[i][0];
        if filename.ends_with(".xml") {
            let xml = &filename[..filename.len()-4];
            if ncalist.contains(xml) {
                return "true".to_string();
            }
        }
        if filename.ends_with(".tik") {
            let tik = &filename[..filename.len()-20];
            if tik == titleid {
                return "true".to_string();
            }
        }
        if filename.ends_with(".cert") {
            let cert_id = &filename[..filename.len()-21];
            if cert_id == titleid {
                return "true".to_string();
            }
        }
        if filename.ends_with(".jpg") {
            let jpg = &filename[..32];
            if ncalist.contains(jpg) {
                return "true".to_string();
            }
        }
    }
    vother.to_string()
}


fn html_printnonlisted(&self, contentlist: Vec<String>, feed: Option<String>) -> String {
    let tab = "\t";
    let mut list_nonlisted = false;
    for filename in &self.filelist {
        if !contentlist.contains(filename) {
            list_nonlisted = true;
        }
    }

    let filedata = file_location(self.firstchunk);
    let mut feed = feed.unwrap_or_default();
    if list_nonlisted {
        feed = html_feed(feed, 2, "Files not linked to content:".to_string());
        let mut totsnl = 0;
        for entry in &filedata {
            let filename = &entry[0];
            if !contentlist.contains(filename) {
                totsnl += entry[1];
                let size_pr = sq_tools::get_size(entry[1]);
                let message = vec!["OTHER:".to_string(), filename.clone(), "Size:".to_string(), size_pr];
                feed = html_feed(feed, 4, message);
            }
        }
        let size_pr = sq_tools::get_size(totsnl);
        feed = html_feed(feed, 5, vec!["TOTAL SIZE:".to_string(), size_pr]);
    }
    feed
}

fn cnmt_data(&self, cnmt: &mut dyn Read, nca: &Nca, nca_name: String) -> (String, String, String, i32, String, String, String, String, i32, i32, bool, i64, i64, Vec<HashMap<String, String>>) {
    let crypto1 = nca.header.get_crypto_type();
    let crypto2 = nca.header.get_crypto_type2();
    let keygeneration = if crypto2 > crypto1 { crypto2 } else { crypto1 };
    cnmt.seek(SeekFrom::Start(0)).unwrap();
    let titleid = read_int64(cnmt);
    let titleid2 = format!("{:x}", titleid);
    let titleid = titleid2.to_uppercase();
    let titleversion = cnmt.read(0x4).unwrap();
    let titleversion = titleversion.iter().map(|&b| b.to_string()).collect::<String>();
    let type_n = cnmt.read(0x1).unwrap();
    cnmt.seek(SeekFrom::Start(0xE)).unwrap();
    let offset = read_int16(cnmt);
    let content_entries = read_int16(cnmt);
    let meta_entries = read_int16(cnmt);
    cnmt.seek(SeekFrom::Start(0x20)).unwrap();
    let base_id = read_int64(cnmt);
    let base_id = format!("{:x}", base_id).to_uppercase();
    cnmt.seek(SeekFrom::Start(0x28)).unwrap();
    let min_sversion = read_int32(cnmt);
    let length_of_emeta = read_int32(cnmt);
    let content_type_cnmt = None;
    let mut ctype = String::new();
    match type_n {
        b'1' => ctype = "SystemProgram".to_string(),
        b'2' => ctype = "SystemData".to_string(),
        b'3' => ctype = "SystemUpdate".to_string(),
        b'4' => ctype = "BootImagePackage".to_string(),
        b'5' => ctype = "BootImagePackageSafe".to_string(),
        b'80' => ctype = "GAME".to_string(),
        b'81' => ctype = "UPDATE".to_string(),
        b'82' => ctype = "DLC".to_string(),
        b'83' => ctype = "Delta".to_string(),
        _ => (),
    }
    let metasdkversion = nca.get_sdkversion();
    let mut program_sdkversion = None;
    let mut data_sdkversion = None;
    let mut ncadata = Vec::new();
    let mut has_html_manual = false;
    let installedsize = nca.header.size as i64;
    let mut delta_size = 0;
    cnmt.seek(SeekFrom::Start(0x20 + offset as u64)).unwrap();
    for _ in 0..content_entries {
        let mut data = HashMap::new();
        let vhash = cnmt.read(0x20).unwrap();
        let vhash = format!("{:x}", vhash.iter().map(|&b| b.to_string()).collect::<String>());
        let ncaid = cnmt.read(0x10).unwrap();
        let ncaid = format!("{:x}", ncaid.iter().map(|&b| b.to_string()).collect::<String>());
        let size = cnmt.read(0x6).unwrap();
        let size = i64::from_le_bytes(size.try_into().unwrap());
        let ncatype = cnmt.read(0x1).unwrap();
        let ncatype = sq_tools::get_meta_content_type(ncatype[0]);
        let _unknown = cnmt.read(0x1).unwrap();
        data.insert("NcaId".to_string(), ncaid);
        data.insert("NCAtype".to_string(), ncatype);
        data.insert("Size".to_string(), size.to_string());
        data.insert("Hash".to_string(), vhash);
        let targetname = format!("{}.nca", ncaid).to_lowercase();
        if ncatype != "DeltaFragment" {
            installedsize += size;
        } else {
            delta_size += size;
        }
        if ncatype == "HtmlDocument" {
            has_html_manual = true;
        }
        if ncatype == "Program" && program_sdkversion.is_none() {
            program_sdkversion = Some(self.get_sdkversion(&targetname));
        }
        if ncatype == "Data" && data_sdkversion.is_none() {
            data_sdkversion = Some(self.get_sdkversion(&targetname));
        }
        ncadata.push(data);
    }
    let mut cnmtdata = HashMap::new();
    let metaname = nca_name.trim_end_matches(".cnmt").to_string();
    nca.rewind().unwrap();
    let block = nca.read().unwrap();
    let nsha = sha256::digest(block);
    cnmtdata.insert("NcaId".to_string(), metaname);
    cnmtdata.insert("NCAtype".to_string(), "Meta".to_string());
    cnmtdata.insert("Size".to_string(), nca.header.size.to_string());
    cnmtdata.insert("Hash".to_string(), nsha);
    ncadata.push(cnmtdata);
    let rightsid = format!("{}000000000000000{}", titleid, crypto2);
    let exesdkversion = if content_type_cnmt == "AddOnContent" { data_sdkversion.unwrap_or(0) } else { program_sdkversion.unwrap_or(0) };
    (titleid, titleversion, base_id, keygeneration, rightsid, RSV, RGV, ctype, metasdkversion, exesdkversion, has_html_manual, installedsize, delta_size, ncadata)
}

fn get_main_program_nca(&self) {
    let ncadata = &self.cnmtdata["ncadata"];
    let mut ncaname = String::new();
    for entry in ncadata {
        if entry["NCAtype"].to_lowercase() == "program" {
            ncaname = format!("{}.nca", entry["NcaId"]);
            break;
        }
    }
    let results = file_location(self.firstchunk, Some(ncaname), false);
    self.mainprogram = results.get(0).cloned();
}


	# def read_buildid(self):
		# ModuleId='';BuildID8='';BuildID16=''
		# sectionFilesystems=[]
		# if self.mainprogram!=None:
			# ncadata=file_location(self.firstchunk,name=self.mainprogram[0],Printdata=False)[0]
			# ncaHeader = NcaHeader()
			# ncaHeader.open(MemoryFile(self.read_at(ncadata,0x0,0xC00), Type.Crypto.XTS, uhx(Keys.get('header_key'))))
			# ncaHeader.rewind()
			# if ncaHeader.getRightsId() == 0:
				# decKey=ncaHeader.titleKeyDec
				# ncaHeader.seek(0x400)
				# for i in range(4):
					# hdr = ncaHeader.read(0x200)
					# section = BaseFs(hdr, cryptoKey = ncaHeader.titleKeyDec)
					# fs = GetSectionFilesystem(hdr, cryptoKey = -1)
					# if fs.fsType:
						# fs.offset=ncaHeader.sectionTables[i].offset
						# sectionFilesystems.append(fs)
						# Print.info('fs type = ' + hex(fs.fsType))
						# Print.info('fs crypto = ' + hex(fs.cryptoType))
						# # Print.info('fs cryptocounter = ' + str(fs.cryptoCounter))
						# Print.info('st end offset = ' + str(ncaHeader.sectionTables[i].endOffset - ncaHeader.sectionTables[i].offset))
						# Print.info('fs offset = ' + hex(ncaHeader.sectionTables[i].offset))
						# Print.info('fs section start = ' + hex(fs.sectionStart))
						# Print.info('titleKey = ' + str(hx(ncaHeader.titleKeyDec)))
				# for fs in sectionFilesystems:
					# if fs.fsType == Type.Fs.PFS0 and fs.cryptoType == Type.Crypto.CTR:
						# print(fs.fsType)
						# print(fs.cryptoType)
						# # print(fs.buffer)
						# pfs0=fs
						# sectionHeaderBlock = fs.buffer
						# print(fs.offset+fs.sectionStart+0xc00)
						# pfs0Offset=fs.offset+0x13800
						# # print(str(fs.cryptoCounter))
						# pfs0Header = self.read_at(ncadata,pfs0Offset,0x10*14)
						# # print(hex(pfs0Offset))
						# # print(hex(fs.sectionStart))
						# Hex.dump(pfs0Header)
						# ncaHeader.rewind()
						# off=fs.offset+fs.sectionStart
						# print(pfs0Offset)
						# print(off)
						# print(str(pfs0Offset-off))
						# ncaHeader.rewind()
						# print(str(off+0xc00+ncaHeader.get_htable_size()))
						# print(str(pfs0Offset-(off+0xc00+ncaHeader.get_htable_size())))
						# mem = MemoryFile(pfs0Header, Type.Crypto.CTR, decKey, pfs0.cryptoCounter, offset = off)
						# data = mem.read();
						# Hex.dump(data)
						# head=data[0:4]
						# n_files=(data[4:8])
						# n_files=int.from_bytes(n_files, byteorder='little')
						# st_size=(data[8:12])
						# st_size=int.from_bytes(st_size, byteorder='little')
						# junk=(data[12:16])
						# offset=(0x10 + n_files * 0x18)
						# stringTable=(data[offset:offset+st_size])
						# stringEndOffset = st_size
						# headerSize = 0x10 + 0x18 * n_files + st_size
						# print(head)
						# print(str(n_files))
						# print(str(st_size))
						# print(str((stringTable)))


						# pfs0Offset=fs.sectionStart
						# sectionHeaderBlock = fs.buffer
						# mem=MemoryFile(self.read_at(ncadata,pfs0Offset,0x10), Type.Crypto.CTR,ncaHeader.titleKeyDec, pfs0.cryptoCounter, offset = fs.offset)
						# print(Hex.dump(mem.read()))
						# print("here")
				# for fs in sectionFilesystems:
					# print(fs.fsType)
					# print(fs.cryptoType)
				# if fs.fsType == Type.Fs.PFS0 and fs.cryptoType == Type.Crypto.CTR:
					# mem=(MemoryFile(self.read_at(ncadata,fs.sectionStart,(ncaHeader.sectionTables[i].endOffset - ncaHeader.sectionTables[i].offset)), Type.Crypto.CTR, ncaHeader.titleKeyDec,fs.cryptoCounter, offset = ncaHeader.sectionTables[i].offset))
					# mem.rewind()
					# print(Hex.dump(mem.read(0x1000)))
					# Print.info('fs type = ' + hex(fs.fsType))
					# Print.info('fs crypto = ' + hex(fs.cryptoType))
					# Print.info('st end offset = ' + str(ncaHeader.sectionTables[i].endOffset - ncaHeader.sectionTables[i].offset))
					# Print.info('fs offset = ' + hex(ncaHeader.sectionTables[i].offset))
					# Print.info('fs section start = ' + hex(fs.sectionStart))
					# Print.info('titleKey = ' + str(ncaHeader.titleKeyDec))

			# if nca.header.getRightsId() != 0:
				# correct, tkey = self.verify_nca_key(str(nca._path))
				# if correct == True:
					# crypto1=nca.header.getCryptoType()
					# crypto2=nca.header.getCryptoType2()
					# if crypto2>crypto1:
						# masterKeyRev=crypto2
					# if crypto2<=crypto1:
						# masterKeyRev=crypto1
				# decKey = Keys.decryptTitleKey(tkey, Keys.getMasterKeyIndex(int(masterKeyRev)))
		# else:pass
		# files_list=sq_tools.ret_xci_offsets(self._path)
		# # print(files_list)
		# for nspF in self.hfs0:
			# if str(nspF._path)=="secure":
				# for nca in nspF:
					# if type(nca) == Fs.Nca:
						# if 	str(nca.header.contentType) == 'Content.PROGRAM':
							# if nca.header.getRightsId() == 0:
								# decKey=nca.header.titleKeyDec
							# if nca.header.getRightsId() != 0:
								# correct, tkey = self.verify_nca_key(str(nca._path))
								# if correct == True:
									# crypto1=nca.header.getCryptoType()
									# crypto2=nca.header.getCryptoType2()
									# if crypto2>crypto1:
										# masterKeyRev=crypto2
									# if crypto2<=crypto1:
										# masterKeyRev=crypto1
									# decKey = Keys.decryptTitleKey(tkey, Keys.getMasterKeyIndex(int(masterKeyRev)))
							# for i in range(len(files_list)):
								# if str(nca._path) == files_list[i][0]:
									# offset=files_list[i][1]
									# # print(offset)
									# break
							# nca.rewind()
							# for fs in nca.sectionFilesystems:
								# # print(fs.fsType)
								# # print(fs.cryptoType)
								# if fs.fsType == Type.Fs.PFS0 and fs.cryptoType == Type.Crypto.CTR:
									# nca.seek(0)
									# ncaHeader = NcaHeader()
									# ncaHeader.open(MemoryFile(nca.read(0x400), Type.Crypto.XTS, uhx(Keys.get('header_key'))))
									# ncaHeader.seek(0)
									# fs.rewind()
									# pfs0=fs
									# sectionHeaderBlock = fs.buffer
									# nca.seek(fs.offset)
									# pfs0Offset=fs.offset
									# pfs0Header = nca.read(0x10*30)
									# mem = MemoryFile(pfs0Header, Type.Crypto.CTR, decKey, pfs0.cryptoCounter, offset = pfs0Offset)
									# data = mem.read();
									# # Hex.dump(data)
									# head=data[0:4]
									# n_files=(data[4:8])
									# n_files=int.from_bytes(n_files, byteorder='little')
									# st_size=(data[8:12])
									# st_size=int.from_bytes(st_size, byteorder='little')
									# junk=(data[12:16])
									# offset=(0x10 + n_files * 0x18)
									# stringTable=(data[offset:offset+st_size])
									# stringEndOffset = st_size
									# headerSize = 0x10 + 0x18 * n_files + st_size
									# # print(head)
									# # print(str(n_files))
									# # print(str(st_size))
									# # print(str((stringTable)))
									# files_list=list()
									# for i in range(n_files):
										# i = n_files - i - 1
										# pos=0x10 + i * 0x18
										# offset = data[pos:pos+8]
										# offset=int.from_bytes(offset, byteorder='little')
										# size = data[pos+8:pos+16]
										# size=int.from_bytes(size, byteorder='little')
										# nameOffset = data[pos+16:pos+20] # just the offset
										# nameOffset=int.from_bytes(nameOffset, byteorder='little')
										# name = stringTable[nameOffset:stringEndOffset].decode('utf-8').rstrip(' \t\r\n\0')
										# stringEndOffset = nameOffset
										# junk2 = data[pos+20:pos+24] # junk data
										# # print(name)
										# # print(offset)
										# # print(size)
										# files_list.append([name,offset,size])
									# files_list.reverse()
									# # print(files_list)
									# for i in range(len(files_list)):
										# if files_list[i][0] == 'main':
											# off1=files_list[i][1]+pfs0Offset+headerSize
											# nca.seek(off1)
											# np=nca.read(0x60)
											# mem = MemoryFile(np, Type.Crypto.CTR, decKey, pfs0.cryptoCounter, offset = off1)
											# magic=mem.read(0x4)
											# if magic==b'NSO0':
												# mem.seek(0x40)
												# data = mem.read(0x20);
												# ModuleId=(str(hx(data)).upper())[2:-1]
												# BuildID8=(str(hx(data[:8])).upper())[2:-1]
												# BuildID16=(str(hx(data[:16])).upper())[2:-1]
												# iscorrect=True;
											# break
								# break
		# if iscorrect==False:
			# try:
				# from nutFS.Nca import Nca as nca3type
				# for nspF in self.hfs0:
					# if str(nspF._path)=="secure":
						# for nca in nspF:
							# if type(nca) == Fs.Nca:
								# if 	str(nca.header.contentType) == 'Content.PROGRAM':
									# nca3type=Nca(nca)
									# nca3type._path=nca._path
									# ModuleId=str(nca3type.buildId)
									# BuildID8=ModuleId[:8]
									# BuildID16=ModuleId[:16]
			# except:
				# ModuleId='';BuildID8='';BuildID16='';
		# return ModuleId,BuildID8,BuildID16

fn get_cnmt_files(path: &str) {
    let ck = Chunk::new(path);
    ck.read_buildid();
}

fn open_all_dat(nca: &Nca) -> io::Result<Vec<File>> {
    let mut dat_files = Vec::new();
    // Implement the logic to open .dat files
    Ok(dat_files)
}

fn print_dat(mut dat: File) -> io::Result<Vec<u8>> {
    dat.rewind()?;
    let mut buffer = Vec::new();
    dat.read_to_end(&mut buffer)?;
    Ok(buffer)
}

fn icon_info(path: &str) -> io::Result<Vec<u8>> {
    let ck = Chunk::new(path);
    if ck.maincontrol.is_some() {
        let inmemoryfile = ck.memoryload(ck.maincontrol.unwrap());
        let mut nca = Nca { header: Header { contentType: ContentType::CONTROL, titleKeyDec: vec![] }, _path: path.to_string() };
        let mut file = File::open(&path)?;
        nca.open(file);
        nca.rewind();
        if nca.header.contentType == ContentType::CONTROL {
            let tk = nca.header.titleKeyDec;
            let mut checksums = Vec::new();
            let mut nca3 = NCA3::new(File::open(&path)?, 0, path.to_string(), tk, vec![]);
            for dat in open_all_dat(&nca)? {
                let mut hasher = Sha1::new();
                io::copy(&mut dat, &mut hasher)?;
                let checksum = hasher.finalize().to_vec();
                if !checksums.contains(&checksum) {
                    checksums.push(checksum);
                    let data = print_dat(dat)?;
                    return Ok(data);
                }
            }
        }
    }
    Err(io::Error::new(io::ErrorKind::Other, "No valid .dat file found"))
}


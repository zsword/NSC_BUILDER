use std::fs::File;
use std::io::{self, Read, Seek, Write};
use std::path::Path;
use aes128::{AesCtr, AesXts};
use hashlib::sha256;

struct BaseFile {
    offset: u64,
    size: Option<u64>,
    file: Option<File>,
    crypto: Option<Box<dyn Crypto>>,
    crypto_key: Option<Vec<u8>>,
    crypto_type: CryptoType,
    crypto_counter: Option<Vec<u8>>,
    crypto_offset: u64,
    ctr_val: u64,
    is_partition: bool,
    children: Vec<BaseFile>,
    path: Option<String>,
    buffer: Option<Vec<u8>>,
    relative_pos: u64,
    buffer_offset: u64,
    buffer_size: u64,
    buffer_align: u64,
    buffer_dirty: bool,
}

impl BaseFile {
    fn new(
        path: Option<&str>,
        mode: Option<&str>,
        crypto_type: i32,
        crypto_key: i32,
        crypto_counter: i32,
    ) -> Self {
        let mut file = BaseFile {
            offset: 0x0,
            size: None,
            file: None,
            crypto: None,
            crypto_key: None,
            crypto_type: CryptoType::None,
            crypto_counter: None,
            crypto_offset: 0,
            ctr_val: 0,
            is_partition: false,
            children: vec![],
            path: None,
            buffer: None,
            relative_pos: 0x0,
            buffer_offset: 0x0,
            buffer_size: 0x1000,
            buffer_align: 0x1000,
            buffer_dirty: false,
        };

        if let (Some(path), Some(mode)) = (path, mode) {
            file.open(path, mode, crypto_type, crypto_key, crypto_counter);
        }

        file.setup_crypto(crypto_type, crypto_key, crypto_counter);
        file
    }

    fn open(
        &mut self,
        path: &str,
        mode: &str,
        crypto_type: i32,
        crypto_key: i32,
        crypto_counter: i32,
    ) {
        if self.is_open() {
            self.close();
        }

        self.file = Some(File::open(path).unwrap());
        self.path = Some(path.to_string());
        self.size = self.file.as_ref().unwrap().metadata().unwrap().len();
        self.setup_crypto(crypto_type, crypto_key, crypto_counter);
    }

    fn close(&mut self) {
        if let Some(file) = &self.file {
            self.flush();
            for child in &self.children {
                child.close();
            }
            self.children = vec![];
            drop(file);
            self.file = None;
        }
    }

    fn flush(&self) {
        if let Some(file) = &self.file {
            file.flush().unwrap();
        }
    }

    fn tell(&self) -> u64 {
        self.file.as_ref().unwrap().seek(io::SeekFrom::Current(0)).unwrap() - self.offset
    }

    fn eof(&self) -> bool {
        self.tell() >= self.size.unwrap_or(0)
    }

    fn is_open(&self) -> bool {
        self.file.is_some()
    }

    fn set_counter(&self, ofs: u64) -> Vec<u8> {
        let mut ctr = self.crypto_counter.as_ref().unwrap().clone();
        ofs >>= 4;
        for j in 0..8 {
            ctr[0x10 - j - 1] = (ofs & 0xFF) as u8;
            ofs >>= 8;
        }
        ctr
    }

    fn set_bktr_counter(&self, ctr_val: u64, ofs: u64) -> Vec<u8> {
        let mut ctr = self.crypto_counter.as_ref().unwrap().clone();
        ofs >>= 4;
        for j in 0..8 {
            ctr[0x10 - j - 1] = (ofs & 0xFF) as u8;
            ofs >>= 8;
        }
        for j in 0..4 {
            ctr[0x8 - j - 1] = (ctr_val & 0xFF) as u8;
            ctr_val >>= 8;
        }
        ctr
    }

    fn print_info(&self, max_depth: i32, indent: i32) {
        let tabs = "\t".repeat(indent as usize);
        if let Some(path) = &self.path {
            println!("{}File Path: {}", tabs, path);
        }
        println!("{}File Size: {}", tabs, self.size.unwrap_or(0));
    }

    fn sha256(&self) -> String {
        let mut hash = sha256::Hash::new();
        self.rewind();
        if self.size.unwrap_or(0) >= 10000 {
            while let Ok(buf) = self.read(1 * 1024 * 1024, true) {
                if buf.is_empty() {
                    break;
                }
                hash.update(&buf);
            }
        } else {
            hash.update(&self.read(None, true));
        }
        hash.finalize().to_hex()
    }

    fn setup_crypto(&mut self, crypto_type: i32, crypto_key: i32, crypto_counter: i32) {
        if crypto_type != -1 {
            self.crypto_type = CryptoType::from_i32(crypto_type);
        }
        if crypto_key != -1 {
            self.crypto_key = Some(vec![crypto_key as u8; 16]);
        }
        if crypto_counter != -1 {
            self.crypto_counter = Some(vec![crypto_counter as u8; 16]);
        }
        match self.crypto_type {
            CryptoType::Ctr | CryptoType::Bktr => {
                if let Some(key) = &self.crypto_key {
                    self.crypto = Some(Box::new(AesCtr::new(key, self.crypto_counter.as_ref().unwrap().clone())));
                    self.crypto_type = CryptoType::Ctr;
                    self.enable_buffered_io(0x10, 0x10);
                }
            }
            CryptoType::Xts => {
                if let Some(key) = &self.crypto_key {
                    self.crypto = Some(Box::new(AesXts::new(key)));
                    self.crypto_type = CryptoType::Xts;
                    if self.size.unwrap_or(0) < 1 || self.size.unwrap_or(0) > 0xFFFFFF {
                        panic!("AESXTS Block too large or small");
                    }
                    self.rewind();
                    self.enable_buffered_io(self.size.unwrap_or(0), 0x10);
                }
            }
            CryptoType::Bktr => {
                self.crypto_type = CryptoType::Bktr;
            }
            CryptoType::Nca0 => {
                self.crypto_type = CryptoType::Nca0;
            }
            CryptoType::None => {
                self.crypto_type = CryptoType::None;
            }
        }
    }

    fn enable_buffered_io(&mut self, size: u64, align: u64) {
        self.buffer_size = size;
        self.buffer_align = align;
        self.buffer_offset = 0;
        self.relative_pos = 0x0;
    }

    fn partition(&mut self, offset: u64, size: Option<u64>, n: Option<&mut BaseFile>, crypto_type: i32, crypto_key: i32, crypto_counter: i32, auto_open: bool) -> &mut BaseFile {
        let mut n = n.unwrap_or(&mut BaseFile::new(None, None, -1, -1, -1));
        n.offset = offset;
        n.size = size.or_else(|| self.size.map(|s| s - n.offset - self.offset));
        n.file = Some(self.file.as_ref().unwrap().try_clone().unwrap());
        n.is_partition = true;
        self.children.push(n);
        if auto_open {
            n.open(None, None, crypto_type, crypto_key, crypto_counter);
        }
        n
    }

    fn remove_child(&mut self, child: &BaseFile) {
        self.children.retain(|c| c as *const _ != child as *const _);
    }

    fn read(&self, size: Option<u64>, direct: bool) -> Vec<u8> {
        let size = size.unwrap_or(self.size.unwrap_or(0));
        let mut buf = vec![0; size as usize];
        self.file.as_ref().unwrap().read_exact(&mut buf).unwrap();
        buf
    }

    fn read_int(&self, size: u64, byteorder: ByteOrder, signed: bool) -> i128 {
        let buf = self.read(Some(size), false);
        i128::from_le_bytes(buf.try_into().unwrap())
    }

    fn write(&self, value: &[u8], size: Option<u64>) -> io::Result<()> {
        let size = size.unwrap_or(value.len() as u64);
        self.file.as_ref().unwrap().write_all(&value[..size as usize])
    }

    fn write_int(&self, value: i128, size: u64, byteorder: ByteOrder, signed: bool) -> io::Result<()> {
        let buf = value.to_le_bytes();
        self.write(&buf[..size as usize], None)
    }

    fn seek(&self, offset: i64, from_what: i32) -> io::Result<()> {
        if !self.is_open() {
            return Err(io::Error::new(io::ErrorKind::Other, "Trying to seek on closed file"));
        }
        match from_what {
            0 => self.file.as_ref().unwrap().seek(io::SeekFrom::Start(self.offset as u64 + offset as u64)),
            1 => self.file.as_ref().unwrap().seek(io::SeekFrom::Current(offset)),
            2 => {
                if offset > 0 {
                    return Err(io::Error::new(io::ErrorKind::Other, "Invalid seek offset"));
                }
                self.file.as_ref().unwrap().seek(io::SeekFrom::End(offset))
            }
            _ => return Err(io::Error::new(io::ErrorKind::Other, "Invalid seek type")),
        }
    }

    fn rewind(&self, offset: Option<i64>) {
        if let Some(offset) = offset {
            self.seek(-offset, 1).unwrap();
        } else {
            self.seek(0, 0).unwrap();
        }
    }
}

struct BufferedFile {
    base: BaseFile,
}

impl BufferedFile {
    fn new(
        path: Option<&str>,
        mode: Option<&str>,
        crypto_type: i32,
        crypto_key: i32,
        crypto_counter: i32,
    ) -> Self {
        BufferedFile {
            base: BaseFile::new(path, mode, crypto_type, crypto_key, crypto_counter),
        }
    }

    fn read(&self, size: Option<u64>, direct: bool) -> Vec<u8> {
        let size = size.unwrap_or(self.base.size.unwrap_or(0));
        if self.base.relative_pos + size > self.base.size.unwrap_or(0) {
            size = self.base.size.unwrap_or(0) - self.base.relative_pos;
        }
        if size < 1 {
            return vec![];
        }
        if self.base.buffer_offset == 0 || self.base.buffer.is_none() || self.base.relative_pos < self.base.buffer_offset || (self.base.relative_pos + size) > self.base.buffer_offset + self.base.buffer.as_ref().unwrap().len() as u64 {
            self.base.flush_buffer();
            self.base.buffer_offset = (self.base.relative_pos / self.base.buffer_align) * self.base.buffer_align;
            let page_read_size = self.base.buffer_size;
            while self.base.relative_pos + size > self.base.buffer_offset + page_read_size {
                page_read_size += self.base.buffer_size;
            }
            if page_read_size > self.base.size.unwrap_or(0) - self.base.buffer_offset {
                page_read_size = self.base.size.unwrap_or(0) - self.base.buffer_offset;
            }
            self.base.seek(self.base.buffer_offset, 0).unwrap();
            self.base.buffer = Some(self.base.read(Some(page_read_size), true));
            self.page_refreshed();
            if self.base.buffer.as_ref().unwrap().is_empty() {
                panic!("read returned empty");
            }
        }
        let offset = self.base.relative_pos - self.base.buffer_offset;
        let r = self.base.buffer.as_ref().unwrap()[offset as usize..offset as usize + size as usize].to_vec();
        self.base.relative_pos += size;
        r
    }

    fn write(&self, value: &[u8], size: Option<u64>) {
        let size = size.unwrap_or(value.len() as u64);
        if self.base.buffer_offset == 0 || self.base.buffer.is_none() || self.base.relative_pos < self.base.buffer_offset || (self.base.relative_pos + size) > self.base.buffer_offset + self.base.buffer.as_ref().unwrap().len() as u64 {
            self.base.flush_buffer();
            let pos = self.base.tell();
            self.read(size, false);
            self.base.seek(pos, 0).unwrap();
        }
        let offset = self.base.relative_pos - self.base.buffer_offset;
        self.base.buffer = Some(self.base.buffer.as_ref().unwrap()[..offset as usize].to_vec());
        self.base.buffer.as_mut().unwrap().extend_from_slice(value);
        self.base.buffer.as_mut().unwrap().extend_from_slice(&self.base.buffer.as_ref().unwrap()[offset as usize + size as usize..]);
        self.base.relative_pos += size;
        self.base.buffer_dirty = true;
    }

    fn flush_buffer(&self) {
        if let Some(file) = &self.base.file {
            if let Some(buffer) = &self.base.buffer {
                if self.base.buffer_dirty {
                    self.base.seek(self.base.buffer_offset, 0).unwrap();
                    self.base.write(&self.get_page_flush_buffer(buffer), None).unwrap();
                    self.base.buffer_dirty = false;
                }
            }
        }
    }

    fn get_page_flush_buffer(&self, buffer: &[u8]) -> Vec<u8> {
        if let Some(crypto) = &self.base.crypto {
            match self.base.crypto_type {
                CryptoType::Ctr => {
                    crypto.seek(self.base.offset + self.base.buffer_offset);
                    crypto.encrypt(buffer)
                }
                CryptoType::Bktr => {
                    crypto.seek(self.base.offset + self.base.buffer_offset);
                    crypto.encrypt(buffer)
                }
                _ => buffer.to_vec(),
            }
        } else {
            buffer.to_vec()
        }
    }

    fn flush(&self) {
        self.flush_buffer();
        self.base.flush();
    }

    fn page_refreshed(&self) {
        if let Some(crypto) = &self.base.crypto {
            match self.base.crypto_type {
                CryptoType::Ctr | CryptoType::Bktr => {
                    crypto.seek(self.base.offset + self.base.buffer_offset);
                    self.base.buffer = Some(crypto.decrypt(self.base.buffer.as_ref().unwrap()));
                }
                _ => {}
            }
        }
    }

    fn tell(&self) -> u64 {
        self.base.relative_pos
    }

    fn close(&self) {
        self.flush_buffer();
        self.base.close();
    }

    fn seek(&self, offset: i64, from_what: i32) -> io::Result<()> {
        if !self.base.is_open() {
            return Err(io::Error::new(io::ErrorKind::Other, "Trying to seek on closed file"));
        }
        match from_what {
            0 => {
                self.base.relative_pos = offset as u64;
                Ok(())
            }
            1 => {
                if let Some(buffer) = &self.base.buffer {
                    self.base.relative_pos += offset as u64;
                    Ok(())
                } else {
                    self.base.file.as_ref().unwrap().seek(io::SeekFrom::Start(self.base.offset as u64 + offset as u64))
                }
            }
            2 => {
                if offset > 0 {
                    return Err(io::Error::new(io::ErrorKind::Other, "Invalid seek offset"));
                }
                self.base.relative_pos = (self.base.offset as i64 + offset as i64 + self.base.size.unwrap_or(0) as i64) as u64;
                Ok(())
            }
            _ => Err(io::Error::new(io::ErrorKind::Other, "Invalid seek type")),
        }
    }
}

struct File {
    buffered: BufferedFile,
}

impl File {
    fn new(
        path: Option<&str>,
        mode: Option<&str>,
        crypto_type: i32,
        crypto_key: i32,
        crypto_counter: i32,
    ) -> Self {
        File {
            buffered: BufferedFile::new(path, mode, crypto_type, crypto_key, crypto_counter),
        }
    }

    fn page_refreshed(&self) {
        if let Some(crypto) = &self.buffered.base.crypto {
            match self.buffered.base.crypto_type {
                CryptoType::Ctr | CryptoType::Bktr => {
                    crypto.seek(self.buffered.base.offset + self.buffered.base.buffer_offset);
                    self.buffered.base.buffer = Some(crypto.decrypt(self.buffered.base.buffer.as_ref().unwrap()));
                }
                _ => {}
            }
        }
    }
}



use std::io::{self, Read, Seek, Write};

struct MemoryFile {
    buffer: Vec<u8>,
    size: usize,
    _buffer_offset: usize,
    crypto: Option<Box<dyn Crypto>>,
}

impl MemoryFile {
    fn new(buffer: Vec<u8>, crypto_type: i32, crypto_key: i32, crypto_counter: i32, offset: Option<usize>) -> Self {
        let _buffer_offset = offset.unwrap_or(0);
        let mut file = MemoryFile {
            buffer,
            size: buffer.len(),
            _buffer_offset,
            crypto: None,
        };
        file.setup_crypto(crypto_type, crypto_key, crypto_counter);
        if let Some(crypto) = &file.crypto {
            if crypto.crypto_type() == CryptoType::CTR || crypto.crypto_type() == CryptoType::BKTR {
                crypto.seek(_buffer_offset);
            }
            file.buffer = crypto.decrypt(file.buffer);
        }
        file
    }

    fn setup_crypto(&mut self, crypto_type: i32, crypto_key: i32, crypto_counter: i32) {
        // Implementation for setting up crypto
    }

    fn read(&self, size: Option<usize>) -> Vec<u8> {
        let size = size.unwrap_or(self.size - self._relative_pos());
        self.buffer[self._relative_pos()..self._relative_pos() + size].to_vec()
    }

    fn write(&mut self, _value: &[u8], _size: Option<usize>) -> io::Result<()> {
        Ok(())
    }

    fn seek(&mut self, offset: usize, from_what: u8) -> io::Result<()> {
        match from_what {
            0 => self.set_relative_pos(offset),
            1 => self.set_relative_pos(self._buffer_offset + offset),
            2 => {
                if offset > 0 {
                    return Err(io::Error::new(io::ErrorKind::InvalidInput, "Invalid seek offset"));
                }
                self.set_relative_pos(self._buffer_offset + offset + self.size);
            }
            _ => return Err(io::Error::new(io::ErrorKind::InvalidInput, "Invalid from_what value")),
        }
        Ok(())
    }

    fn open(&self, _path: &str, _mode: &str, _crypto_type: i32, _crypto_key: i32, _crypto_counter: i32) -> io::Result<()> {
        Ok(())
    }

    fn _relative_pos(&self) -> usize {
        // Implementation for getting relative position
        0
    }

    fn set_relative_pos(&mut self, pos: usize) {
        // Implementation for setting relative position
    }
}

struct CryptoFile {
    // Implementation for CryptoFile
}

impl CryptoFile {
    fn page_refreshed(&mut self) -> Vec<u8> {
        // Implementation for page refreshed
        vec![]
    }

    fn read2(&self, size: Option<usize>) -> Vec<u8> {
        // Implementation for read2
        vec![]
    }
}

struct AesXtsFile {
    // Implementation for AesXtsFile
}

impl AesXtsFile {
    fn new(_path: Option<&str>, _mode: Option<&str>, _crypto_type: i32, _crypto_key: i32, _crypto_counter: i32) -> Self {
        // Implementation for AesXtsFile
        AesXtsFile {}
    }
}

struct AesCtrFile {
    // Implementation for AesCtrFile
}

impl AesCtrFile {
    fn new(_path: Option<&str>, _mode: Option<&str>, _crypto_type: i32, _crypto_key: i32, _crypto_counter: i32) -> Self {
        // Implementation for AesCtrFile
        AesCtrFile {}
    }
}

trait Crypto {
    fn crypto_type(&self) -> CryptoType;
    fn seek(&mut self, offset: usize);
    fn decrypt(&self, data: Vec<u8>) -> Vec<u8>;
}

enum CryptoType {
    CTR,
    BKTR,
}

// Placeholder implementations for Crypto trait
struct DummyCrypto;

impl Crypto for DummyCrypto {
    fn crypto_type(&self) -> CryptoType {
        CryptoType::CTR
    }

    fn seek(&mut self, _offset: usize) {
        // Implementation for seek
    }

    fn decrypt(&self, data: Vec<u8>) -> Vec<u8> {
        data
    }
}

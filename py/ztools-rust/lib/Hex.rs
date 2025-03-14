use std::fmt::Write;

fn buffer_to_hex(buffer: &[u8], start: usize, count: usize) -> String {
    let mut accumulator = String::new();
    for item in 0..count {
        write!(accumulator, "{:02X} ", buffer[start + item]).unwrap();
    }
    accumulator
}

fn buffer_to_ascii(buffer: &[u8], start: usize, count: usize) -> String {
    let mut accumulator = String::new();
    for item in 0..count {
        let char = buffer[start + item] as char;
        if char.is_ascii_alphanumeric() || char.is_ascii_punctuation() || char == ' ' {
            accumulator.push(char);
        } else {
            accumulator.push('.');
        }
    }
    accumulator
}

fn dump(data: &[u8], size: usize) {
    let bytesRead = data.len();
    let mut index = 0;
    let hex_format = format!("{{:0<{} }}", size * 3);
    let ascii_format = format!("{{:0<{} }}", size);

    println!();
    while index < bytesRead {
        let hex = buffer_to_hex(data, index, size);
        let ascii = buffer_to_ascii(data, index, size);

        println!("{} |{}|", hex_format.replace("{}", &hex), ascii_format.replace("{}", &ascii));
        
        index += size;
        if bytesRead - index < size {
            size = bytesRead - index;
        }
    }
}

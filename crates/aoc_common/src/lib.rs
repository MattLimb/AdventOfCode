use std::{io, fs};

pub fn read_file(filepath: String) -> io::Result<String> {
    fs::read_to_string(filepath)
}
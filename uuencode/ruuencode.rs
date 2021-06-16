use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    //println!("{:?}", args);
    let path = Path::new(&args[1]);
    //let path = Path::new("/home/guillaume/Documents/subtitle_extract/v5r/todoroki.ass");
    let buf = read_file(path);
    //println!("{:?}", path);
    //println!("{:?}", uuencode(&buf));
    print_buf(&uuencode(&buf));
}

fn read_file(src: &Path) -> Vec<u8> {
    let mut file = match File::open(&src) {
        Err(e) => panic!("Opening failed, {}", e),
        Ok(f) => f,
    };
    let mut buf: Vec<u8> = Vec::new();
    match file.read_to_end(&mut buf) {
        Err(e) => panic!("Reading failed, {}", e),
        Ok(_) => (),
    };
    buf
}

fn uuencode(buf: &Vec<u8>) -> Vec<u8> {
    let mut ebuf: Vec<u8> = Vec::new();
    let n = buf.len();
    let m = match n%3 {
	1 => n+2,
	2 => n+1,
	_ => n,
    };
    for i in (0..m).step_by(3) {
	let x1 = get_or_zero(buf, i) as u32;
	let x2 = get_or_zero(buf, i+1) as u32;
	let x3 = get_or_zero(buf, i+2) as u32;
	let x = (x1<<16)+(x2<<8)+x3;
	ebuf.push(byte_encode((x>>18) as u8));
	ebuf.push(byte_encode((x>>12) as u8));
	ebuf.push(byte_encode((x>>6) as u8));
	ebuf.push(byte_encode(x as u8));
    };
    ebuf
}

fn get_or_zero(buf: &Vec<u8>, i: usize) -> u8 {
    match buf.get(i) {
	Some(&x) => x,
	None => 0,
    }
}

fn byte_encode(x: u8) -> u8 {
    (x&63)+33
}

fn print_buf(buf: &Vec<u8>) {
    let n = buf.len();
    for i in 0..n {
	print!("{}", buf[i] as char);
	if ((i+1)%80) == 0 && i != 0 {
	    print!("\n");
	};	
    };
}

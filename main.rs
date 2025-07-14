use std::io::{self, BufRead, BufReader, Write};

#[allow(unused_macros)]
macro_rules! debug {
  ($($arg::tt)*) => {
    #[cfg(debug_assertions)]
    eprintln!($($arg)*);
  };
}

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();
    // code goes here ...
}

#[allow(dead_code)]
fn read_line() -> String {
    let stdin = io::stdin();
    let mut line = String::new();
    stdin.read_line(&mut line).unwrap();
    line.trim().to_string()
}

#[allow(dead_code)]
fn read_nums<T: std::str::FromStr>() -> Vec<T>
where
    T::Err: std::fmt::Debug,
{
    read_line()
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect()
}

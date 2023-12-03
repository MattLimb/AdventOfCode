use aoc_common::read_file;
use std::process::exit;

use fancy_regex::Regex;

fn convert_to_u32(unknown_string: &str) -> u32 {
    match unknown_string {
        "1" | "one" => 1,
        "2" | "two" => 2,
        "3" | "three" => 3,
        "4" | "four" => 4,
        "5" | "five" => 5,
        "6" | "six" => 6,
        "7" | "seven" => 7,
        "8" | "eight" => 8,
        "9" | "nine" => 9,
        _ => 0,
    }
}

fn calculations(part: i32, puzzle_input: String, regex: &str) {
    let re = Regex::new(regex).unwrap();
    let input_as_lines: Vec<&str> = puzzle_input.split('\n').collect();
    let mut sum_per_line: Vec<u32> = vec![];

    for line in input_as_lines.into_iter() {
        let captures = re
            .captures_iter(line)
            .map(|capture| match capture {
                Ok(cap) => {
                    if let Some(c) = cap.get(1) {
                        convert_to_u32(c.as_str())
                    } else {
                        println!("INVALID: {:?}", cap);
                        0
                    }
                }
                Err(err) => {
                    println!("Encountered an error running regex for: {:?}", err);
                    exit(1);
                }
            })
            .collect::<Vec<u32>>();

        let first: u32 = captures[0];
        let last: u32 = captures[captures.len() - 1];

        sum_per_line.push((first * 10) + last);
    }

    println!("Part {}: {:?}", part, sum_per_line.iter().sum::<u32>());
}

fn main() {
    let input_path: String = "inputs/day_1.txt".to_string();

    let puzzle_input: String = match read_file(input_path) {
        Ok(s) => s,
        Err(e) => {
            println!("Encountered an error reading the puzzle input: {:?}", e);
            exit(1);
        }
    };

    calculations(1, puzzle_input.clone(), r"([1-9])");
    calculations(
        2,
        puzzle_input,
        r"(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))",
    );
}

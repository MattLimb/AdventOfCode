use aoc_common::read_file;
use std::process::exit;

#[derive(Debug, Clone)]
struct CoOrdinate {
    y: usize,
    x: usize
}

#[derive(Debug, Clone)]
struct Grid {
    grid: Vec<Vec<char>>,
    num_rows: usize,
    num_cols: usize
}


impl Grid {
    fn new(grid_string: String) -> Self {
        let mut grid: Vec<Vec<char>> = vec![];
        let mut temp_row : Vec<char> = vec![];
        let mut row_size: usize = 0;

        for c in grid_string.chars() {
            match c {
                '\r' => continue,
                '\n' => {
                    grid.push(temp_row.clone());
                    
                    let trl: usize = temp_row.len();
                    
                    if trl > row_size {
                        row_size = trl;
                    }
                    temp_row.clear();
                }
                _ => temp_row.push(c),
            }
        }

        grid.push(temp_row.clone());

        Grid {
            grid: grid.clone(), 
            num_cols: row_size,
            num_rows: grid.len()
        }
    }

    fn get(&self, coordinate: &CoOrdinate) -> Result<char, String> {
        if coordinate.y > self.num_rows {
            return Err(format!("Row index {} is out of bounds. (Too High)", coordinate.y));
        }

        if coordinate.x > self.num_cols {
            return Err(format!("Column index {} is out of bounds. (Too High)", coordinate.x));
        }
    
        Ok(self.grid[coordinate.y][coordinate.x])
    }

    fn is_number(c: &char) -> bool {
        match c {
            '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' => true,
            _ => false,
        }
    }

    fn discover_number(&self, start: CoOrdinate) -> Result<u32, String> {
        let error: String = "Number could not be found.".to_string();
        let mut number: String = String::new();

        // Check that the start point is a valid number.
        let ch: Result<char, String> = self.get(&start);

        if &ch.is_err() == &true {
            return Err(error);
        } else {
            let c: char = ch.unwrap();

            if Grid::is_number(&c) == false {
                return Err(error);
            } else {
                number.push(c);
            }
        }

        let mut new_x = start.clone().x;

        if start.clone().x > 0 {
            // Go Left
            new_x -= 1;
            loop {
                let ch: char = match self.get(&CoOrdinate { y: start.clone().y, x: new_x }) {
                    Ok(c) => c,
                    Err(_) => continue,
                };

                match Grid::is_number(&ch) {
                    true => {
                        number = format!("{ch}{number}");
                    },
                    false => break,
                }

                if new_x == 0 {
                    break
                } else {
                    new_x -= 1;
                }
            }
        }

        new_x = start.clone().x;

        if start.clone().x < self.num_cols {
            // Go Right
            new_x += 1;

            loop {
                let ch: char = match self.get(&CoOrdinate { y: start.clone().y, x: new_x }) {
                    Ok(c) => c,
                    Err(_) => continue,
                };

                match Grid::is_number(&ch) {
                    true => {
                        number = format!("{number}{ch}");
                    },
                    false => break,
                }

                if new_x == self.num_cols - 1 {
                    break
                } else {
                    new_x += 1;
                }
            }
        }

        match number.parse::<u32>() {
            Err(_) => Err(format!("Cannot parse invalid number: {number}")),
            Ok(t) => Ok(t)
        }
    }

    fn discover_surrounds(&self, start: CoOrdinate) -> Vec<u32> {
        let mut surrounds: Vec<CoOrdinate> = vec![];

        // Discover Top Row
        if start.y != 0 {
            // Can go Left?
            if start.x != 0 {
                surrounds.push(CoOrdinate { y: start.y - 1, x: start.x - 1 });
            }

            surrounds.push(CoOrdinate { y: start.y - 1, x: start.x });

            // Can go Right?
            if start.x != self.num_cols {
                surrounds.push(CoOrdinate { y: start.y - 1, x: start.x + 1 });
            }
        }

        // Discover Current Row
        // Can go Left?
        if start.x != 0 {
            surrounds.push(CoOrdinate { y: start.y, x: start.x - 1 });
        }

        surrounds.push(CoOrdinate { y: start.y, x: start.x });

        // Can go Right?
        if start.x != self.num_cols {
            surrounds.push(CoOrdinate { y: start.y, x: start.x + 1 });
        }

        // Discover Bottom Row
        if start.y != self.num_rows {
            // Can go Left?
            if start.x != 0 {
                surrounds.push(CoOrdinate { y: start.y + 1, x: start.x - 1 });
            }

            surrounds.push(CoOrdinate { y: start.y + 1, x: start.x });

            // Can go Right?
            if start.x != self.num_cols {
                surrounds.push(CoOrdinate { y: start.y + 1, x: start.x + 1 });
            }
        }

        let valid_surrounds: Vec<CoOrdinate> = surrounds.into_iter().filter(|co| {
            match self.get(co) {
                Ok(ch) => Grid::is_number(&ch),
                Err(_) => false
            }
        }).collect();

        let mut valid_numbers: Vec<u32> = vec![];

        for co in valid_surrounds {
            match self.discover_number(co) {
                Ok(num) => {
                    if valid_numbers.contains(&num) == false {
                        valid_numbers.push(num);
                    }
                },
                Err(_) => continue,
            }
        }

        valid_numbers    
    }
}


fn part_1(grid: Grid) {
    let mut all_nums: Vec<u32> = vec![];

    for (y_idx, row) in grid.clone().grid.into_iter().enumerate() {
        for (x_idx, col) in row.into_iter().enumerate() {
            if col.is_ascii_punctuation() && col != '.' {
                all_nums.extend(grid.discover_surrounds(CoOrdinate { y: y_idx, x: x_idx }));
            }
        }
    }

    println!("Part 1: {}", all_nums.into_iter().sum::<u32>());
}

fn part_2(grid: Grid) {
    let mut all_nums: Vec<u32> = vec![];

    for (y_idx, row) in grid.clone().grid.into_iter().enumerate() {
        for (x_idx, col) in row.into_iter().enumerate() {
            if col.is_ascii_punctuation() && col != '.' {
                let nums_around = grid.discover_surrounds(CoOrdinate { y: y_idx, x: x_idx });

                if &nums_around.len() == &2 {
                    all_nums.push(nums_around[0] * nums_around[1]);
                }
            }
        }
    }

    println!("Part 2: {}", all_nums.into_iter().sum::<u32>());
}

fn main() {
    let input_path: String = "inputs/day_3.txt".to_string();

    let puzzle_input: String = match read_file(input_path) {
        Ok(s) => s,
        Err(e) => {
            println!("Encountered an error reading the puzzle input: {:?}", e);
            exit(1);
        }
    };

    let grid = Grid::new(puzzle_input);

    part_1(grid.clone());
    part_2(grid)
}

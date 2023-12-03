use aoc_common::read_file;
use std::process::exit;


#[derive(Debug, Clone)]
struct ShownCubes {
    red: u32,
    green: u32,
    blue: u32
}

#[derive(Debug, Clone)]
struct Game {
    id: u32,
    shown_cubes: Vec<ShownCubes>
}


#[derive(Debug)]
struct Games {
    games: Vec<Game>
}

impl ShownCubes {
    fn parse(input: &str) -> Self {
        let mut red = 0;
        let mut blue = 0;
        let mut green = 0;

        for item in input.split(",") {
            let item_split: (&str, &str) = match item.trim().split_once(" ") {
                Some(t) => t,
                None => {
                    println!("Game contained no results.");
                    exit(1);
                }
            };

            match item_split {
                (i, "blue") => blue = i.parse().unwrap(),
                (i, "green") => green = i.parse().unwrap(),
                (i, "red") => red = i.parse().unwrap(),
                (_, s) => {
                    println!("Unsupported colour {s}");
                    exit(1);
                }
            }
        }

        Self { red, blue, green }
    }
}


impl Game {
    fn parse(input: &str) -> Self {
        let split_input: (&str, &str) = match input.split_once(":") {
            Some(t) => t,
            None => {
                println!("Game contained no results.");
                exit(1);
            }
        };

        let split_game: (&str, u32) = match split_input.0.trim().split_once(" ") {
            Some(t) => (t.0, t.1.parse().unwrap()),
            None => {
                println!("Error Parsing Game ID {}", split_input.0);
                exit(1);
            }
        };
        let shown_cubes: Vec<ShownCubes> = split_input.1.trim().split(";").map(|sc| { ShownCubes::parse(sc) }).collect();

        Self { id: split_game.1, shown_cubes }
    }

    fn is_possible(&self, red: u32, green: u32, blue: u32) -> bool {
        for sc in self.shown_cubes.iter() {
            if sc.red > red {
                return false;
            } 

            if sc.green > green {
                return false;
            }

            if sc.blue > blue {
                return false;
            }
        }

        true
    }

    fn minimum_required(&self) -> ShownCubes {
        let mut red: u32 = 0;
        let mut green: u32 = 0;
        let mut blue: u32 = 0;

        for game in self.shown_cubes.clone() {
            if game.red > red {
                red = game.red;
            }

            if game.green > green {
                green = game.green;
            }

            if game.blue > blue {
                blue = game.blue
            }
        }

        ShownCubes { red, green, blue }
    }
}

impl Games {
    fn part_1(&self) -> u32 {
        self.games.clone().into_iter().filter(|g| {g.is_possible(12, 13, 14) }).map(|g| g.id).sum()
    }

    fn part_2(&self) -> u32 {
        self.games.clone().into_iter().map(|g| {
            let min_req: ShownCubes = g.minimum_required();

            min_req.red * min_req.green * min_req.blue
        }).sum()
    }
}

fn main() {
    let input_path: String = "inputs/day_2.txt".to_string();

    let puzzle_input: String = match read_file(input_path) {
        Ok(s) => s,
        Err(e) => {
            println!("Encountered an error reading the puzzle input: {:?}", e);
            exit(1);
        }
    };

    let games: Games = Games {
        games: puzzle_input.split("\n").map(|g| { Game::parse(g) }).collect::<Vec<Game>>() 
    };

    println!("Part 1: {}", games.part_1());
    println!("Part 2: {}", games.part_2());
}

use std::io;

const MAX_RED: i32 = 12;
const MAX_GREEN: i32 = 13;
const MAX_BLUE: i32 = 14;

fn hand_possible(g: &str) -> bool {
    for term in g.split(", ") {
        let Some((lhs, rhs)) = term.split_once(" ") else { todo!() };
        let count = lhs.parse::<i32>().unwrap();
        let limit = match &rhs[..] {
            "red" => MAX_RED,
            "green" => MAX_GREEN,
            "blue" => MAX_BLUE,
            _ => panic!("don't know!"),
        };
        if count > limit {
            return false
        }
    }
    true
}

fn main() {
    let lines = io::stdin().lines();
    let mut lineno = 0;
    let mut score = 0;
    for line in lines {
        lineno += 1;
        let mut l = line.unwrap();
        let pos = match l.find(":") {
            None => return,
            Some(n) => n,
        };
        // Skip the colon and the following space.
        l = l[pos+2..].to_string();

        let mut game_possible = true;
        for hand in l.split("; ") {
            if !hand_possible(hand) {
                game_possible = false;
                break;
            }
        }
        if game_possible {
            score += lineno;
        }
    }

    println!("{}", score);
}

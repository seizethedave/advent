use std::io;
use std::collections::HashSet;

fn game_score(s: &str) -> i64 {
    let mut winners = HashSet::new();
    let mut mine = HashSet::new();
    let mut processing_winners = true;

    for i in s.split_whitespace() {
        if i == "|" {
            processing_winners = false;
            continue;
        } else if processing_winners {
            winners.insert(i);
        } else {
            mine.insert(i);
        }
    }

    let count = mine.intersection(&winners).collect::<HashSet<_>>().len();
    if count == 0 {
        0
    } else {
        i64::pow(2, count as u32 - 1)
    }
}

fn main() {
    let mut score :i64 = 0;
    for line in io::stdin().lines() {
        let mut l = line.unwrap();
        let pos = match l.find(":") {
            None => return,
            Some(n) => n,
        };
        // Skip the colon and the following space.
        l = l[pos+2..].to_string();
        score += game_score(&l);
    }

    println!("{}", score);
}
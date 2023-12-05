use std::io;
use std::collections::HashSet;
use std::collections::VecDeque;

fn game_score(s: &str) -> (i64, i32) {
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
        (0, 0)
    } else {
        (i64::pow(2, count as u32 - 1), count as i32)
    }
}

fn main() {
    let mut score: i64 = 0;
    let mut cards: i64 = 0;
    let mut agenda = VecDeque::new();

    for line in io::stdin().lines() {
        let mut l = line.unwrap();
        let pos = match l.find(":") {
            None => return,
            Some(n) => n,
        };

        // Skip the colon and the following space.
        l = l[pos+2..].to_string();
        let (sc, bonus_games) = game_score(&l);

        let mul = 1 + match agenda.pop_front() {
            Some(m) => m,
            _ => 0,
        };

        score += sc;
        cards += mul;

        // Maintain a queue of upcoming bonuses. Whatever bonus this last card
        // earned gets boosted by that card's multiplier.

        for bonus in 0..bonus_games {
            if let Some(v) = agenda.get_mut(bonus as usize) {
                *v += mul;
            } else {
                agenda.push_back(mul);
            }
        }
    }

    println!("{}", score);
    println!("{}", cards);
}
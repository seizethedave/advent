use std::io;
use std::cmp;

fn read_hand(h: &str) -> (i32, i32, i32) {
    let (mut r, mut g, mut b) = (0, 0, 0);
    for term in h.split(", ") {
        let Some((lhs, rhs)) = term.split_once(" ") else { todo!() };
        let count = lhs.parse::<i32>().unwrap();
        match &rhs[..] {
            "red" => r = count,
            "green" => g = count,
            "blue" => b = count,
            _ => panic!("don't know!"),
        };
    }
    (r, g, b)
}

fn min_cube_power(g: &str) -> i32 {
    let (mut br, mut bg, mut bb) = (0, 0, 0);
    for hand in g.split("; ") {
        let (r, g, b) = read_hand(hand);
        br = cmp::max(br, r);
        bg = cmp::max(bg, g);
        bb = cmp::max(bb, b);
    }
    br * bg * bb
}

fn main() {
    let mut score = 0;
    for line in io::stdin().lines() {
        let mut l = line.unwrap();
        let pos = match l.find(":") {
            None => return,
            Some(n) => n,
        };
        // Skip the colon and the following space.
        l = l[pos+2..].to_string();
        score += min_cube_power(&l);
    }

    println!("{}", score);
}

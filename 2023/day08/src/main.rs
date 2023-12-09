use std::io;
use std::collections::HashMap;
use num::integer::lcm;

fn lcm_multi(ns: &Vec<i64>) -> i64 {
    ns.into_iter().fold(1, |acc, n| lcm(acc, *n))
}

fn main() {
    let mut line_iter = io::stdin().lines();
    let lr_line = match line_iter.next().unwrap() {
        Ok(val) => val,
        Err(e) => panic!("unexpected err getting LR line: {}", e),
    };

    let mut nodes: HashMap<String, (String, String)> = HashMap::new();

    for line in line_iter.skip(1) {
        let line_val = line.unwrap().clone();
        let l = &line_val;

        let (lhs, rhs) = match l.split_once(" = ") {
            None => panic!("expected equal-delimited line"),
            Some((l, r)) => (l, r),
        };

        // Strip parens off of RHS.
        let rhs_len = rhs.len();
        let rhs_inner = &rhs[1..rhs_len-1];

        let (left_turn, right_turn) = match rhs_inner.split_once(", ") {
            None => panic!("expected comma delimited RHS"),
            Some((l, r)) => (l, r),
        };

        nodes.insert(lhs.to_string(), (left_turn.to_string(), right_turn.to_string()));
    }

    // Part 1:
    let mut pos = "AAA";
    const DEST: &str = "ZZZ";

    for (i, dir) in lr_line.chars().cycle().enumerate() {
        pos = {
            let (l, r) = nodes.get(pos).expect("node not found!");
            if dir == 'L' { l } else { r }
        };
        if pos == DEST {
            println!("{}", i + 1);
            break;
        }
    }

    // Part 2.
    // Instead of a single position, track ALL positions.
    // |A| = |Z| and that means every A origin touches a Z destination once then
    // loops again. Thus we need to find the length of each path from A to Z then
    // find the LCM of all of these paths.
    let positions: Vec<&String> = nodes.keys().filter(|k| k.ends_with('A')).collect();
    let mut pathlens: Vec<i64> = Vec::new();
    pathlens.reserve_exact(positions.len());

    for p in positions.iter() {
        let mut thispos = *p;
        for (i, dir) in lr_line.chars().cycle().enumerate() {
            thispos = {
                let (l, r) = nodes.get(thispos).expect("node not found!");
                if dir == 'L' { l } else { r }
            };
            if thispos.ends_with('Z') {
                pathlens.push(i as i64 + 1);
                break;
            }
        }
    }

    println!("{}", lcm_multi(&pathlens));
}

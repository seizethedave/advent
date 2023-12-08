use std::io;
use std::collections::HashMap;

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

    let mut pos = "AAA";
    const DEST: &str = "ZZZ";

    for (i, dir) in lr_line.chars().cycle().enumerate() {
        let opts = nodes.get(pos).expect("node not found!");
        pos = {
            let (l, r) = opts;
            if dir == 'L' { l } else { r }
        };

        if pos == DEST {
            println!("{}", i + 1);
            break;
        }
    }
}

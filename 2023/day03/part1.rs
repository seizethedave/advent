use std::io;

fn grid_get(grid: &Vec<char>, width: usize, y: usize, x: usize) -> (bool, char) {
    let pos = (y * width + x) as usize;
    match grid.get(pos) {
        Some(c) => (true, *c),
        None => (false, '!'),
    }
}

fn is_symbol(grid: &Vec<char>, width: usize, y: usize, x: usize) -> bool {
    let (valid, c) = grid_get(grid, width, y, x);
    valid && !c.is_ascii_digit() && c != '.'
}

fn near_symbol(grid: &Vec<char>, width: usize, y: usize, start: usize, end: usize) -> bool {
    for i in start..=end {
        if (y > 0 && is_symbol(grid, width, y - 1, i)) || is_symbol(grid, width, y + 1, i) {
            return true;
        }
    }

    // Check columns left and right of the number.

    if start > 0 {
        if (y > 0 && is_symbol(grid, width, y - 1, start - 1)) ||
            is_symbol(grid, width, y, start - 1) ||
            is_symbol(grid, width, y + 1, start - 1) {
            return true;
        }
    }

    (y > 0 && is_symbol(grid, width, y - 1, end + 1)) ||
        is_symbol(grid, width, y, end + 1) ||
        is_symbol(grid, width, y + 1, end + 1)
}

fn main() {
    let mut grid: Vec<char> = Vec::new();
    let mut width: usize = 0;
    let mut height: usize = 0;
    for line in io::stdin().lines() {
        let ll = line.unwrap();
        let l = ll.trim_end();
        width = l.len();
        height += 1;
        grid.extend(l.chars());
    }

    fn terminate_number(gr: &Vec<char>, width: usize, y: usize, start: usize, end: usize) -> i32 {
        if near_symbol(gr, width, y, start, end) {
            let mut tally: i32 = 0;
            for i in start..=end {
                let (valid, c) = grid_get(gr, width, y, i);
                if !valid {
                    panic!("terminate_number expected valid spots");
                }
                if let Some(cn) = c.to_digit(10) {
                    tally = tally * 10 + (cn as i32);
                }
            }
            tally
        } else {
            0
        }
    }

    let mut score = 0;

    // Scan L->R one line at a time.
    let mut start: usize = 0;
    let mut running = false;

    for y in 0..height {
        for x in 0..width {
            let (valid, ch) = grid_get(&grid, width, y, x);
            if !valid {
                panic!("past grid bounds?")
            }
            if ch.is_ascii_digit() {
                if !running {
                    start = x;
                    running = true;
                }
            } else if running {
                score += terminate_number(&grid, width, y, start, x-1);
                running = false;
            }
        }

        if running {
            score += terminate_number(&grid, width, y, start, width-1);
            running = false;
        }
    }

    println!("{}", score)
}

use std::io;

struct Grid<'a> {
    g: &'a Vec<char>,
    width: usize,
    height: usize,
}

impl Grid<'_> {
    fn get(&self, y: usize, x: usize) -> (bool, char) {
        let pos = (y * self.width + x) as usize;
        match self.g.get(pos) {
            Some(c) => (true, *c),
            None => (false, '!'),
        }
    }

    fn is_symbol(&self, y: usize, x: usize) -> bool {
        let (valid, c) = self.get(y, x);
        valid && !c.is_ascii_digit() && c != '.'
    }

    fn near_symbol(&self, y: usize, start: usize, end: usize) -> bool {
        for i in start..=end {
            if (y > 0 && self.is_symbol(y - 1, i)) || self.is_symbol(y + 1, i) {
                return true;
            }
        }
    
        // Check columns left and right of the number.
    
        if start > 0 {
            if (y > 0 && self.is_symbol(y - 1, start - 1)) ||
                self.is_symbol(y, start - 1) ||
                self.is_symbol(y + 1, start - 1) {
                return true;
            }
        }
    
        (y > 0 && self.is_symbol(y - 1, end + 1)) ||
            self.is_symbol(y, end + 1) ||
            self.is_symbol(y + 1, end + 1)
    }

    fn terminate_number(&self, y: usize, start: usize, end: usize) -> i32 {
        if !self.near_symbol(y, start, end) {
            return 0;
        }

        let mut tally: i32 = 0;
        for i in start..=end {
            let (valid, c) = self.get(y, i);
            if !valid {
                panic!("terminate_number expected valid spots");
            }
            if let Some(cn) = c.to_digit(10) {
                tally = tally * 10 + (cn as i32);
            }
        }
        tally
    }
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

    let gg = Grid {
        g: &grid,
        width: width,
        height: height,
    };

    

    let mut score = 0;

    // Scan L->R one line at a time.
    let mut start: usize = 0;
    let mut running = false;

    for y in 0..gg.height {
        for x in 0..gg.width {
            let (valid, ch) = gg.get(y, x);
            if !valid {
                panic!("past grid bounds?")
            }
            if ch.is_ascii_digit() {
                if !running {
                    start = x;
                    running = true;
                }
            } else if running {
                score += gg.terminate_number(y, start, x-1);
                running = false;
            }
        }

        if running {
            score += gg.terminate_number(y, start, width-1);
            running = false;
        }
    }

    println!("{}", score)
}

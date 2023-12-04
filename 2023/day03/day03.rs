use std::io;
use std::collections::HashMap;

struct Grid {
    g: Vec<char>,
    width: usize,
    height: usize,
    gears: HashMap<(usize, usize), Vec<i32>>,
}

impl Grid {
    fn get(&self, y: usize, x: usize) -> (bool, char) {
        let pos = (y * self.width + x) as usize;
        match self.g.get(pos) {
            Some(c) => (true, *c),
            None => (false, '!'),
        }
    }

    fn get_symbol(&self, y: usize, x: usize) -> (bool, char) {
        let (valid, c) = self.get(y, x);
        let is_sym = valid && !c.is_ascii_digit() && c != '.';
        (is_sym, c)
    }

    fn is_symbol(&self, y: usize, x: usize) -> bool {
        let (sym, _c) = self.get_symbol(y, x);
        sym
    }

    fn is_gear(&self, y: usize, x: usize) -> bool {
        let (valid, c) = self.get(y, x);
        valid && c == '*'
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

    fn index_gear(&mut self, y: usize, x: usize, tally: i32) {
        if let Some(v) = self.gears.get_mut(&(y, x)) {
            v.push(tally);
        } else {
            self.gears.insert((y, x), vec![tally]);
        }
    }

    fn gear_score(&self) -> i32 {
        self.gears.iter()
            .filter(|(_k, v)| v.len() == 2)
            .map(|(_k, v)| v[0] * v[1])
            .sum()
    }

    fn process_gears(&mut self, y: usize, start: usize, end: usize, tally: i32) {
        // Similar to near_symbol, but looks at *all* neighboring cells without returning early.
        for i in start..=end {
            if y > 0 && self.is_gear(y - 1, i) {
                self.index_gear(y-1, i, tally);
            }
            if self.is_gear(y + 1, i) {
                self.index_gear(y+1, i, tally);
            }
        }
    
        // Scan columns left of the number.
        if start > 0 {
            if y > 0 && self.is_gear(y - 1, start - 1) {
                self.index_gear(y-1, start-1, tally);
            }
            if self.is_gear(y, start - 1) {
                self.index_gear(y, start-1, tally);
            }
            if self.is_gear(y + 1, start - 1) {
                self.index_gear(y+1, start-1, tally);
            }
        }

        // and right.
        if y > 0 && self.is_gear(y - 1, end + 1) {
            self.index_gear(y-1, end+1, tally);
        }
        if self.is_gear(y, end + 1) {
            self.index_gear(y, end+1, tally);
        }
        if self.is_gear(y + 1, end + 1) {
            self.index_gear(y+1, end+1, tally);
        }
    }

    fn terminate_number(&mut self, y: usize, start: usize, end: usize) -> i32 {
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

        self.process_gears(y, start, end, tally);
        tally
    }
}

fn main() {
    let mut grid = {
        let mut gg = Grid {
            g: Vec::new(),
            width: 0,
            height: 0,
            gears: HashMap::new(),
        };
        for line in io::stdin().lines() {
            let ll = line.unwrap();
            let l = ll.trim_end();
            gg.width = l.len();
            gg.height += 1;
            gg.g.extend(l.chars());
        }
        gg
    };

    let mut score = 0;

    // Scan L->R one line at a time.
    let mut start: usize = 0;
    let mut running = false;

    for y in 0..grid.height {
        for x in 0..grid.width {
            let (valid, ch) = grid.get(y, x);
            if !valid {
                panic!("past grid bounds?")
            }
            if ch.is_ascii_digit() {
                if !running {
                    start = x;
                    running = true;
                }
            } else if running {
                score += grid.terminate_number(y, start, x-1);
                running = false;
            }
        }

        if running {
            score += grid.terminate_number(y, start, grid.width-1);
            running = false;
        }
    }

    println!("part 1: {}", score);
    println!("part 2: {}", grid.gear_score());
}

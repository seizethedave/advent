use std::io;
use std::collections::HashMap;
use std::collections::VecDeque;

/*
We'll have a hashmap that is all known modules {"name" => mod_instance}
Each mod instance has a list of destination node strings.
We'll have a linked list of actions. We put broadcast in this linked list and execute it.
All resulting actions go to the end.
We then pop off the front and do it again.
*/

const PREFIX_FLIP_FLOP: char = '%';
const PREFIX_CONJUNCTION: char = '&';

const MODULE_BUTTON: &str = "button";
const MODULE_BROADCAST: &str = "broadcaster";

enum Behavior {
    Broadcast,
    Conjunction(HashMap<String, bool>),
    FlipFlop(bool),
}

impl Behavior {
    fn call<C>(&mut self, neighbors: &Vec<String>, sender: &str, high_pulse: bool, mut callback: C)
        where C: FnMut(String, bool)
    {
        match *self {
            Self::Broadcast => {
                for n in neighbors {
                    callback(n.to_owned(), high_pulse)
                }
            },
            Self::Conjunction(ref mut h) => {
                h.insert(sender.to_owned(), high_pulse);
                let pulse = h.values().any(|v| !*v);
                for n in neighbors {
                    callback(n.to_owned(), pulse)
                }
            },
            Self::FlipFlop(ref mut on) => {
                if !high_pulse {
                    *on = !*on;
                    for n in neighbors {
                        callback(n.to_owned(), *on);
                    }
                }
            },
        }
    }

    fn add_source(&mut self, source_module: &str) {
        match *self {
            Self::Broadcast => { },
            Self::Conjunction(ref mut h) => {
                h.insert(source_module.to_owned(), false);
            },
            Self::FlipFlop(_) => { },
        }
    }

    fn reset(&mut self) {
        match *self {
            Self::Broadcast => { },
            Self::Conjunction(ref mut h) => {
                for v in h.values_mut() {
                    *v = false;
                }
            },
            Self::FlipFlop(ref mut on) => {
                *on = false;
            },
        }
    }
}

struct Module {
    neighbors: Vec<String>,
    behavior: Behavior,
}

fn read_input() -> HashMap<String, Box<Module>> {
    let mut modules = HashMap::new();

    for line in io::stdin().lines() {
        let line = line.unwrap();
        let (lhs, rhs) = line.split_once(" -> ").unwrap();
        let neighbors: Vec<String> = rhs.split(", ").map(String::from).collect();

        let (mod_name, behavior) = if lhs.starts_with(PREFIX_FLIP_FLOP) {
            (&lhs[1..], Behavior::FlipFlop(false))
        } else if lhs.starts_with(PREFIX_CONJUNCTION) {
            (&lhs[1..], Behavior::Conjunction(HashMap::new()))
        } else {
            (lhs, Behavior::Broadcast)
        };

        modules.insert(mod_name.to_owned(), Box::new(Module{
            neighbors,
            behavior,
        }));
    }

    // Go back through and install source modules now that the modules map is
    // fully populated.

    let mut connections: Vec<(String, String)> = Vec::new();
    for (k, v) in modules.iter() {
        for n in v.neighbors.iter() {
            connections.push((k.to_owned(), n.to_owned()));
        }
    }

    for (src, dest) in &connections {
        if let Some(dest_module) = modules.get_mut(dest) {
            dest_module.behavior.add_source(src);
        }
    }

    modules
}

fn main() {
    let mut mods = read_input();
    let mut actions: VecDeque<(String, String, bool)> = VecDeque::new();

    const PRESSES: i16 = 1000;
    let mut low_pulses: i64 = 0;
    let mut high_pulses: i64 = 0;

    for _i in 0..PRESSES {
        actions.push_back((MODULE_BUTTON.to_owned(), MODULE_BROADCAST.to_owned(), false));

        while let Some((sender, dest, high_pulse)) = actions.pop_front() {
            if high_pulse {
                high_pulses += 1;
            } else {
                low_pulses += 1;
            }
            if let Some(c) = mods.get_mut(&dest) {
                c.behavior.call(&c.neighbors, &sender, high_pulse, |n, p| {
                    actions.push_back((dest.to_owned(), n, p))
                })
            }
        }
    }

    println!("{}", low_pulses * high_pulses);

    // Now reset the module state and see how many button presses it takes to
    // get a low pulse on module "rx".

    for m in mods.values_mut() {
        m.behavior.reset();
    }

    let mut ct: i64 = 0;

    'outer: loop {
        ct += 1;
        if (ct % 1_000_000) == 0 {
            println!("{}", ct);
        }
        actions.push_back((MODULE_BUTTON.to_owned(), MODULE_BROADCAST.to_owned(), false));

        while let Some((sender, dest, high_pulse)) = actions.pop_front() {
            if !high_pulse && dest == "rx" {
                println!("{}", ct);
                break 'outer;
            }

            if let Some(c) = mods.get_mut(&dest) {
                c.behavior.call(&c.neighbors, &sender, high_pulse, |n, p| {
                    actions.push_back((dest.to_owned(), n, p))
                })
            }
        }
    }
}

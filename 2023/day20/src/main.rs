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
const MODULE_END: &str = "rx";

type ModuleRef = usize;

struct RefStore {
    entries: HashMap<String, ModuleRef>,
}

impl RefStore {
    fn get(&mut self, val: &str) -> ModuleRef {
        match self.entries.get(val) {
            Some(r) => *r,
            None => {
                let next = self.entries.len();
                self.entries.insert(String::from(val), next);
                next
            }
        }
    }
}

enum Behavior {
    Broadcast,
    Conjunction(HashMap<ModuleRef, bool>),
    FlipFlop(bool),
}

impl Behavior {
    fn call<C>(&mut self, neighbors: &Vec<ModuleRef>, sender: ModuleRef, high_pulse: bool, mut callback: C)
        where C: FnMut(ModuleRef, bool)
    {
        match *self {
            Self::Broadcast => {
                for n in neighbors {
                    callback(*n, high_pulse)
                }
            },
            Self::Conjunction(ref mut h) => {
                h.insert(sender, high_pulse);
                let pulse = h.values().any(|v| !*v);
                for n in neighbors {
                    callback(*n, pulse)
                }
            },
            Self::FlipFlop(ref mut on) => {
                if !high_pulse {
                    *on = !*on;
                    for n in neighbors {
                        callback(*n, *on);
                    }
                }
            },
        }
    }

    fn add_source(&mut self, source_module: ModuleRef) {
        match *self {
            Self::Broadcast => { },
            Self::Conjunction(ref mut h) => {
                h.insert(source_module, false);
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
    neighbors: Vec<ModuleRef>,
    behavior: Behavior,
}

fn read_input(ref_store: &mut RefStore) -> HashMap<ModuleRef, Box<Module>> {
    let mut modules: HashMap<ModuleRef, Box<Module>> = HashMap::new();

    for line in io::stdin().lines() {
        let line = line.unwrap();
        let (lhs, rhs) = line.split_once(" -> ").unwrap();
        let neighbors: Vec<ModuleRef> = rhs.split(", ").map(|s| ref_store.get(s)).collect();

        let (mod_name, behavior) = if lhs.starts_with(PREFIX_FLIP_FLOP) {
            (&lhs[1..], Behavior::FlipFlop(false))
        } else if lhs.starts_with(PREFIX_CONJUNCTION) {
            (&lhs[1..], Behavior::Conjunction(HashMap::new()))
        } else {
            (lhs, Behavior::Broadcast)
        };

        modules.insert(ref_store.get(mod_name), Box::new(Module{
            neighbors,
            behavior,
        }));
    }

    // Go back through and install source modules now that the modules map is
    // fully populated.

    let mut connections: Vec<(ModuleRef, ModuleRef)> = Vec::new();
    for (k, v) in modules.iter() {
        for n in v.neighbors.iter() {
            connections.push((*k, *n));
        }
    }

    for (src, dest) in connections {
        if let Some(dest_module) = modules.get_mut(&dest) {
            dest_module.behavior.add_source(src);
        }
    }

    modules
}

fn main() {
    let mut ref_store = RefStore{entries: HashMap::new()};
    let mut mods = read_input(&mut ref_store);
    let mut actions: VecDeque<(ModuleRef, ModuleRef, bool)> = VecDeque::new();

    let button_ref = ref_store.get(MODULE_BUTTON);
    let broadcast_ref = ref_store.get(MODULE_BROADCAST);
    let rx_ref = ref_store.get(MODULE_END);

    const PRESSES: i16 = 1000;
    let mut low_pulses: i64 = 0;
    let mut high_pulses: i64 = 0;

    for _i in 0..PRESSES {
        actions.push_back((button_ref, broadcast_ref, false));

        while let Some((sender, dest, high_pulse)) = actions.pop_front() {
            if high_pulse {
                high_pulses += 1;
            } else {
                low_pulses += 1;
            }
            if let Some(c) = mods.get_mut(&dest) {
                c.behavior.call(&c.neighbors, sender, high_pulse, |n, p| {
                    actions.push_back((dest, n, p))
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
        actions.push_back((button_ref, broadcast_ref, false));

        while let Some((sender, dest, high_pulse)) = actions.pop_front() {
            if !high_pulse && dest == rx_ref {
                println!("{}", ct);
                break 'outer;
            }

            if let Some(c) = mods.get_mut(&dest) {
                c.behavior.call(&c.neighbors, sender, high_pulse, |n, p| {
                    actions.push_back((dest, n, p))
                })
            }
        }
    }
}

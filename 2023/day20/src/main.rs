use std::io;
use std::collections::HashMap;
use std::collections::HashSet;
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

struct FlipFlopModule {
    on: bool,
    neighbors: Vec<String>,
}

struct ConjunctionModule {
    neighbors: Vec<String>,
    neighbor_high_pulse: HashSet<String>,
}

struct BroadcastModule {
    neighbors: Vec<String>,
}

pub trait CallableModule {
    fn call(&mut self, sender: &String, high_pulse: bool) -> Vec<(String, bool)>;
}

impl CallableModule for FlipFlopModule {
    fn call(&mut self, _sender: &String, high_pulse: bool) -> Vec<(String, bool)> {
        let mut res = Vec::new();
        if !high_pulse {
            self.on = !self.on;
            for n in &self.neighbors {
                res.push((n.to_string(), self.on));
            }
        }
        res
    }
}

impl CallableModule for ConjunctionModule {
    fn call(&mut self, sender: &String, high_pulse: bool) -> Vec<(String, bool)> {
        if high_pulse {
            self.neighbor_high_pulse.insert(sender.to_owned());
        } else {
            self.neighbor_high_pulse.remove(sender);
        }
        let pulse = self.neighbor_high_pulse.len() != self.neighbors.len();
        let res: Vec<(String, bool)> = self.neighbors.iter().map(|n| (n.to_owned(), pulse)).collect();
        res
    }
}

impl CallableModule for BroadcastModule {
    fn call(&mut self, _sender: &String, high_pulse: bool) -> Vec<(String, bool)> {
        let mut res = Vec::new();
        for n in &self.neighbors {
            res.push((n.to_owned(), high_pulse));
        }
        res
    }
}

fn read_input() -> HashMap<String, Box<dyn CallableModule>> {
    let mut modules: HashMap<String, Box<dyn CallableModule>> = HashMap::new();

    for line in io::stdin().lines() {
        let line = line.unwrap();
        let (lhs, rhs) = line.split_once(" -> ").unwrap();
        let neighbors: Vec<String> = rhs.split(", ").map(String::from).collect();

        let (mod_name, mod_box) = if lhs.starts_with(PREFIX_FLIP_FLOP) {
            let boxed: Box<dyn CallableModule> = Box::new(FlipFlopModule{
                on: false,
                neighbors: neighbors,
            });
            (&lhs[1..], boxed)
        } else if lhs.starts_with(PREFIX_CONJUNCTION) {
            let boxed: Box<dyn CallableModule> = Box::new(ConjunctionModule{
                neighbors: neighbors,
                neighbor_high_pulse: HashSet::new(),
            });
            (&lhs[1..], boxed)
        } else {
            let boxed: Box<dyn CallableModule> = Box::new(BroadcastModule{
                neighbors: neighbors,
            });
            (lhs, boxed)
        };

        modules.insert(mod_name.to_owned(), mod_box);
    }

    modules
}

fn main() {
    let mut mods = read_input();
    let mut actions: VecDeque<(String, String, bool)> = VecDeque::new();
    actions.push_back((MODULE_BUTTON.to_owned(), MODULE_BROADCAST.to_owned(), false));

    while let Some((sender, dest, high_pulse)) = actions.pop_front() {
        println!("{} -{}-> {}", sender, if high_pulse { "high" } else { "low"}, dest);
        if let Some(c) = mods.get_mut(&dest) {
            for (n, p) in c.call(&sender, high_pulse) {
                actions.push_back((dest.to_owned(), n, p))
            }
        }
    }
}

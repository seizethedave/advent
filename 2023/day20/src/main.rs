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

struct Module {
    neighbors: Vec<String>,
    behavior: Box<dyn ModuleBehavior>,
}

struct FlipFlopBehavior {
    on: bool,
}

struct ConjunctionBehavior {
    source_high_pulse: HashMap<String, bool>,
}

struct BroadcastBehavior;

trait ModuleBehavior {
    fn call(&mut self, neighbors: &Vec<String>, sender: &String, high_pulse: bool) -> Vec<(String, bool)>;
    fn add_source(&mut self, _source_module: &String) {}
}

impl ModuleBehavior for FlipFlopBehavior {
    fn call(&mut self, neighbors: &Vec<String>, _sender: &String, high_pulse: bool) -> Vec<(String, bool)> {
        let mut res = Vec::with_capacity(neighbors.len());
        if !high_pulse {
            self.on = !self.on;
            for n in neighbors {
                res.push((n.to_string(), self.on));
            }
        }
        res
    }
}

impl ModuleBehavior for ConjunctionBehavior {
    fn call(&mut self, neighbors: &Vec<String>, sender: &String, high_pulse: bool) -> Vec<(String, bool)> {
        if let Some(v) = self.source_high_pulse.get_mut(sender) {
            *v = high_pulse;
        }
        let pulse = self.source_high_pulse.values().any(|v| !(*v));
        let res: Vec<(String, bool)> = neighbors.iter().map(|n| (n.to_owned(), pulse)).collect();
        res
    }

    fn add_source(&mut self, source_module: &String) {
        self.source_high_pulse.insert(source_module.to_owned(), false);
    }
}

impl ModuleBehavior for BroadcastBehavior {
    fn call(&mut self, neighbors: &Vec<String>, _sender: &String, high_pulse: bool) -> Vec<(String, bool)> {
        let mut res = Vec::with_capacity(neighbors.len());
        for n in neighbors {
            res.push((n.to_owned(), high_pulse));
        }
        res
    }
}

fn read_input() -> HashMap<String, Box<Module>> {
    let mut modules = HashMap::new();

    for line in io::stdin().lines() {
        let line = line.unwrap();
        let (lhs, rhs) = line.split_once(" -> ").unwrap();
        let neighbors: Vec<String> = rhs.split(", ").map(String::from).collect();

        let (mod_name, behavior) = if lhs.starts_with(PREFIX_FLIP_FLOP) {
            let boxed: Box<dyn ModuleBehavior> = Box::new(FlipFlopBehavior{
                on: false,
            });
            (&lhs[1..], boxed)
        } else if lhs.starts_with(PREFIX_CONJUNCTION) {
            let boxed: Box<dyn ModuleBehavior> = Box::new(ConjunctionBehavior{
                source_high_pulse: HashMap::new(),
            });
            (&lhs[1..], boxed)
        } else {
            let boxed: Box<dyn ModuleBehavior> = Box::new(BroadcastBehavior{
            });
            (lhs, boxed)
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
    actions.push_back((MODULE_BUTTON.to_owned(), MODULE_BROADCAST.to_owned(), false));

    while let Some((sender, dest, high_pulse)) = actions.pop_front() {
        println!("{} -{}-> {}", sender, if high_pulse { "high" } else { "low"}, dest);
        if let Some(c) = mods.get_mut(&dest) {
            for (n, p) in c.behavior.call(&c.neighbors, &sender, high_pulse) {
                actions.push_back((dest.to_owned(), n, p))
            }
        }
    }
}

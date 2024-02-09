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

struct FlipFlopModule {
    neighbors: Vec<String>,
}

struct ConjunctionModule {
    neighbors: Vec<String>,
}

struct BroadcastModule {
    neighbors: Vec<String>,
}

pub trait CallableModule {
    fn call(&mut self);
}

impl CallableModule for FlipFlopModule {
    fn call(&mut self) {
        println!("call::flipflop")
    }
}
impl CallableModule for ConjunctionModule {
    fn call(&mut self) {
        println!("call::conjunction")
    }
}
impl CallableModule for BroadcastModule {
    fn call(&mut self) {
        println!("call::broadcast")
    }
}

fn read_input() -> HashMap<String, Box<dyn CallableModule>> {
    let mut modules: HashMap<String, Box<dyn CallableModule>> = HashMap::new();

    for line in io::stdin().lines() {
        let line = line.unwrap();
        let (lhs, rhs) = line.split_once(" -> ").unwrap();
        let neighbors: Vec<String> = rhs.split(", ").map(String::from).collect();

        let (mod_name, mod_box) = if lhs.starts_with(PREFIX_FLIP_FLOP) {
            let boxed: Box<dyn CallableModule> = Box::new(FlipFlopModule{neighbors: neighbors});
            (&lhs[1..], boxed)
        } else if lhs.starts_with(PREFIX_CONJUNCTION) {
            let boxed: Box<dyn CallableModule> = Box::new(ConjunctionModule{neighbors: neighbors});
            (&lhs[1..], boxed)
        } else {
            let boxed: Box<dyn CallableModule> = Box::new(BroadcastModule{neighbors: neighbors});
            (lhs, boxed)
        };

        modules.insert(mod_name.to_string(), mod_box);
    }

    modules
}

fn main() {
    let mut mods = read_input();
    let mut actions: VecDeque<(String, String)> = VecDeque::new();
    actions.push_back((MODULE_BUTTON.to_string(), MODULE_BROADCAST.to_string()));

    loop {
        if let Some((sender, dest)) = actions.pop_front() {
            println!("{} -> {}", sender, dest);

            if let Some(c) = mods.get_mut(&dest) {
                c.call();
            }
        } else {
            return;
        }
    }
}

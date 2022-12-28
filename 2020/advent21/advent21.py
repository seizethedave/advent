from collections import Counter
import copy
from operator import itemgetter
import sys

class Solver:
    def __init__(self):
        self.foods = []
        self.ingredients = {}
        self.unassigned_allergens = set()
        self.unassigned_ingredients = set()
        self.allergy_free_ingredients = set()
        self.solution = None

    def add_food(self, ingredients, allergens):
        self.foods.append((set(ingredients), set(allergens)))
        self.unassigned_allergens.update(allergens)
        self.unassigned_ingredients.update(ingredients)
        self.allergy_free_ingredients.update(ingredients)

    def assign(self, ingredient, allergen):
        self.ingredients[ingredient] = allergen
        self.unassigned_ingredients.remove(ingredient)
        self.unassigned_allergens.remove(allergen)

    def unassign(self, ingredient, allergen):
        del self.ingredients[ingredient]
        self.unassigned_ingredients.add(ingredient)
        self.unassigned_allergens.add(allergen)

    def eligible_for_allergen(self, ing, allerg):
        for fi, fa in self.foods:
            if allerg in fa and ing not in fi:
                return False
        return True

    def solve(self):
        if not self.unassigned_allergens:
            self.allergy_free_ingredients &= self.unassigned_ingredients
            if self.solution is None:
                self.solution = copy.deepcopy(self.ingredients)
            return True

        for ingredient in self.unassigned_ingredients:
            for allergen in self.unassigned_allergens:
                if not self.eligible_for_allergen(ingredient, allergen):
                    continue
                self.assign(ingredient, allergen)
                solved = self.solve()
                self.unassign(ingredient, allergen)
                if solved:
                    return True
        else:
            return False

s = Solver()

for line in sys.stdin:
    ingredients, allergens = line.split("(")
    ingredients = ingredients.strip().split(" ")
    allergens = allergens[9:-1].rstrip("\n)").split(", ")
    s.add_food(ingredients, allergens)

s.solve()

c = Counter()
for f_i, _ in s.foods:
    c.update(f_i & s.allergy_free_ingredients)

# Part 1:
print(sum(c.values()))

# Part 2:
print(
    ",".join(k for k, _ in sorted(s.solution.items(), key=itemgetter(1)))
)
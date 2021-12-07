"""
Advent of Code Day 6: Lantern Fish
A massive school of glowing lanternfish swims past. They must spawn quickly to reach such large numbers
- maybe exponentially quickly? You should model their growth rate to be sure.

So, suppose you have a lanternfish with an internal timer value of 3:

After one day, its internal timer would become 2.
After another day, its internal timer would become 1.
After another day, its internal timer would become 0.
After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7.
This list means that the first fish has an internal timer of 3, the second fish has an internal timer of 4, and so on until the fifth fish, which has an internal timer of 2. Simulating these fish over several days would proceed as follows:
Example:
Initial state: 3,4,3,1,2
After  1 day:  2,3,2,0,1
After  2 days: 1,2,1,6,0,8
After  3 days: 0,1,0,5,6,7,8
After  4 days: 6,0,6,4,5,6,7,8,8
After  5 days: 5,6,5,3,4,5,6,7,7,8
After  6 days: 4,5,4,2,3,4,5,6,6,7
After  7 days: 3,4,3,1,2,3,4,5,5,6
After  8 days: 2,3,2,0,1,2,3,4,4,5
After  9 days: 1,2,1,6,0,1,2,3,3,4,8
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8
"""
from __future__ import annotations
from datetime import datetime
from typing import List
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from tqdm import tqdm

example_starting_stages = """3,4,3,1,2""".split(",")
starting_stages = """
3,3,2,1,4,1,1,2,3,1,1,2,1,2,1,1,1,1,1,1,4,1,1,5,2,1,1,2,1
,1,1,3,5,1,5,5,1,1,1,1,3,1,1,3,2,1,1,1,1,1,1,4,1,1,1,1,1,1,1,4,1,3,3,1,1,3,1,3,1,2,1,3,1,
1,4,1,2,4,4,5,1,1,1,1,1,1,4,1,5,1,1,5,1,1,3,3,1,3,2,5,2,4,1,4,1,2,4,5,1,1,5,1,1,1,4,1,1,5,
2,1,1,5,1,1,1,5,1,1,1,1,1,3,1,5,3,2,1,1,2,2,1,2,1,1,5,1,1,4,5,1,4,3,1,1,1,1,1,1,5,1,1,1,5,
2,1,1,1,5,1,1,1,4,4,2,1,1,1,1,1,1,1,3,1,1,4,4,1,4,1,1,5,3,1,1,1,5,2,2,4,2,1,1,3,1,5,5,1,1,
1,4,1,5,1,1,1,4,3,3,3,1,3,1,5,1,4,2,1,1,5,1,1,1,5,5,1,1,2,1,1,1,3,1,1,1,2,3,1,2,2,3,1,3,
1,1,4,1,1,2,1,1,1,1,3,5,1,1,2,1,1,1,4,1,1,1,1,1,2,4,1,1,5,3,1,1,1,2,2,2,1,5,1,3,5,3,1,1,4,1,1,4
""".replace(
    "\n", ""
).split(
    ","
)

# breed a new fish when stage is 0
breed_at = 0
# new fish start with a timer of 8
new_fish_level = 8
# after a fish breeds its new stage is 6
new_cycle_level = 6
# how many days to simulate
stage_1_breeding_days = 80
stage_2_breeding_days = 256


def main():
    """Main function"""
    # example_school = School(example_starting_stages)
    day_school = School(starting_stages)
    # example_school.simulate(80)
    day_school.simulate(1024)


class School:
    def __init__(self, initial_stages: list[str] = [], day: int = 0):
        self.fish: dict[int,int] = {}
        self.initial_stages = initial_stages
        self.day = day
        self.days: dict[int,dict[int,int]] = {}
        self.load_initial_population(initial_stages)

    def load_initial_population(self, initial_stages: list[str]):
        """Load the initial population"""
        stages = [int(stage) for stage in initial_stages]
        fish = {}
        day = {}
        for i in range(9):
            fish[i] = stages.count(i)
            day[i] = stages.count(i)
        self.fish.update(fish)
        self.days[self.day] = day


    def new_day(self):
        """Age all fish in the school"""
        new_stages = {k:0 for k in range(9)}
        new_fish = 0
        new_cycle_fish = 0
        with tqdm(total=8,leave=False,position=1, desc="Stage") as pbar:
            for stage in range(9):
                pbar.desc = f"Stage {stage}/8"
                # print(f"{stage}: {population}")
                population = self.fish.get(stage, 0)
                if stage > 0:
                    new_stage = stage - 1
                    new_stages[new_stage] = population
                if stage == breed_at:
                    new_fish += population
                    new_cycle_fish += population
                pbar.update(1)

        new_stages[new_fish_level] += new_fish
        new_stages[new_cycle_level] += new_cycle_fish
        
        self.fish.update(new_stages)
        self.days[self.day + 1] = new_stages
        self.day += 1
        
        
    def simulate(self, num_days):
        """Simulate the school for num_days"""
        day_range = list(range(1, num_days + 1))
        sim_start = datetime.now()
        with tqdm(total=num_days, leave=True, position=0, desc="Day 0") as pbar:
            for day in day_range:
                pbar.desc = f"Day {day}/{num_days}"
                breed_start_time = datetime.now()
                self.new_day()
                # print(self)
                breed_end_time = datetime.now()
                pbar.write(f"{self} took {breed_end_time - breed_start_time}")
                pbar.update(1)
        sim_end = datetime.now()
        print(f"total fish: {self.population()} in {self.day} days. Simulated in {sim_end - sim_start}")
        
    
    def population(self):
        """Return the total population"""
        return sum(self.fish.values())
    
    def __str__(self):
        return f"School Day {self.day}: Total Fish: {self.population()} Total Days: {len(self.days)}"


if __name__ == "__main__":
    main()

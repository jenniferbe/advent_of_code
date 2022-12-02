import heapq

"""
The jungle must be too overgrown and difficult to navigate in vehicles or access
from the air; the Elves' expedition traditionally goes on foot. As your boats
approach land, the Elves begin taking inventory of their supplies. One important
consideration is food - in particular, the number of Calories each Elf is carrying
(your puzzle input).

The Elves take turns writing down the number of Calories contained by the various
meals, snacks, rations, etc. that they've brought with them, one item per line.
Each Elf separates their own inventory from the previous Elf's inventory (if any)
by a blank line.

For example, suppose the Elves finish writing their items' Calories and end up with
the following list:
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

This list represents the Calories of the food carried by five Elves:

    The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total of 6000 Calories.
    The second Elf is carrying one food item with 4000 Calories.
    The third Elf is carrying food with 5000 and 6000 Calories, a total of 11000 Calories.
    The fourth Elf is carrying food with 7000, 8000, and 9000 Calories, a total of 24000 Calories.
    The fifth Elf is carrying one food item with 10000 Calories.

In case the Elves get hungry and need extra snacks, they need to know which Elf to
ask: they'd like to know how many Calories are being carried by the Elf carrying the
most Calories. In the example above, this is 24000 (carried by the fourth Elf).

Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?

Solution: 67016
"""
input_file = "input.txt"

def get_max_total_calories(input_file):
    f = open(input_file, "r")
    line = f.readline()

    curr_calories, max_calories = 0, 0
    while (line):
        if line.strip() == "":
            if curr_calories > max_calories:
                max_calories = curr_calories
            curr_calories = 0
        else:
            curr_calories += int(line)
        line = f.readline()
    if curr_calories > max_calories:
        max_calories = curr_calories
    f.close()
    return max_calories

print("Max total calories: {}".format(get_max_total_calories(input_file)))

"""
By the time you calculate the answer to the Elves' question, they've already
realized that the Elf carrying the most Calories of food might eventually run out of
snacks.

To avoid this unacceptable situation, the Elves would instead like to know the total
Calories carried by the top three Elves carrying the most Calories. That way, even
if one of those Elves runs out of snacks, they still have two backups.

In the example above, the top three Elves are the fourth Elf (with 24000 Calories),
then the third Elf (with 11000 Calories), then the fifth Elf (with 10000 Calories).
The sum of the Calories carried by these three elves is 45000.

Find the top three Elves carrying the most Calories. How many Calories are those
Elves carrying in total?

Solution: 200116
"""
def save_top_n_calories(heap, n, calories):
    if (len(heap) < n):
        heap.append(calories)
    elif (calories > heap[0]):
        heapq.heappushpop(heap, calories)

def get_top_n_calories(input_file, n):
    f = open(input_file, "r")
    line = f.readline()

    curr_calories, top_n_calories = 0, []
    heapq.heapify(top_n_calories)
    while line:
        if line.strip() == "":
            save_top_n_calories(top_n_calories, n, curr_calories)
            curr_calories = 0
        else:
            curr_calories += int(line)
        line = f.readline()
    f.close()
    save_top_n_calories(top_n_calories, n, curr_calories)
    return sum(top_n_calories)

print("Total Calories for Top 3 Elves: {}".format(get_top_n_calories(input_file, 3)))

import os
import sys
from parser import Parser, ParssingError
print()
while True:
	maps = [
		{
			"maps/easy": [
				"01_linear_path.txt",
				"02_simple_fork.txt",
				"03_basic_capacity.txt",
			]
		},
		{
			"maps/medium": [
				"01_dead_end_trap.txt",
				"02_circular_loop.txt",
				"03_priority_puzzele.txt",
			]
		},
		{
			"maps/hard": [
				"01_maze_nightmare.txt",
                "02_capacity_hell.txt",
                "03_ultimate_challenge.txt",
			]
		},
		{
			"maps/challenger": [
                "01_the_impossible_dream.txt",
            ]
		}
	]

	print(
		"map levels:",
		"\n (1) easy (2) medium (3) hard (4) chalenger (5) exit"
	)
	while True:
		try:
			level = int(input("Choose the level: ")) - 1
		except ValueError:
			print("Only the allowed numbers!")
			continue
		if level not in [0, 1, 2, 3, 4]:
			print(level)
			print("Invalid number, Choose the number [1, 2, 3, 4, 5].")
		if level == 4:
			sys.exit(0)
		else:
			break
	print("\navailable maps on this level:")

	for i in list(maps[level].values()[0]):
		print("   -", i)
	
	while True:
		try:
			index = int(input("\nChoose a number:"))
		except ValueError:
			print("Only the allowed numbers!")
			continue
		map = list(maps[level].items()[0])
		if not 0 < index <= len(map[1]):
			print(
				"Invalid number. Choose a number in this:"
				f"{[i + 1 for i in range(len(map[1]))]}"
			)
		else:
			break
	os.system('cls' if os.name == 'nt' else 'clear')
	try:
		parser = Parser(f"{map[0]}/{map[1][index - 1]}")
	except (ParssingError, ValueError)
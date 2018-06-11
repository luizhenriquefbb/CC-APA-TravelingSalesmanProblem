'''
USAGES:
	- python3 [number of executions] [file to read - a tsp file]
'''


from City import City
from TSP import TSP

import random
import time
import itertools
import urllib
import csv
import functools
import pprint 
import sys
import timeit

def main(argv):
	print ("init main...")
	number_exec = int(argv[1])

	cities = []

	# Read file
	fileContent = open(argv[2], 'r').read()
	
	# Attention: file must be well formated
	# TODO: make it more robust
	lines = fileContent.split("\n")
	filename = lines[0]
	for line in lines[7:]:
		try:
			aux = line.split(" ")
			# Get id, position x and position Y
			city = City(aux[0], aux[1], aux[2])
			cities.append(city)
		except Exception as e:
			print ("1 " + str(e) + " city :" + str(city.id))
			break
	
	tsp = TSP()
	M = tsp.get_distance_matrix(cities)
	
	# print matrix of distances
	# tsp.pretty_print(M)
	# exit()

	print ("Executing " + str(number_exec) + " times on : " + str(filename) )

	start_time = timeit.default_timer()

	minimo = float("inf")

	for i in range(number_exec):
		print("Attempt "+str(i))

		# alpha = random.uniform(0, 1)
		alpha = 0.5

		tour, custo_final = tsp.runGRASP(cities, M, alfa=alpha)

		if custo_final < minimo:
			print ("\nCusto: " + str(custo_final))
			tsp.plot_cities(tour)
			minimo = custo_final
		

	elapsed = timeit.default_timer() - start_time

	input("presse ENTER to continue")
	print ("Elapsed time : " + str(elapsed) + " s")
	print ("---------------------------------------------\n\n")


if __name__ == "__main__":
	main(sys.argv)




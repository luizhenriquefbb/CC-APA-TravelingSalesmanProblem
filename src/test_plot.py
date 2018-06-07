import City
import TSP
import pdb

def main():
	tsp = TSP.TSP()

	# Creat a list of cities
	cities = [
		City.City("1", "20833.3333", "17100.0000"),
		City.City("2", "20900.0000", "17066.6667"),
		City.City("3", "21300.0000", "13016.6667")
	]

	tsp.plot_cities(cities)

	
	pdb.set_trace()

if __name__ == '__main__':
	main()


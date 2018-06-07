import math
from matplotlib import pyplot as plt
import collections
import random

class TSP:
	""" Define os algoritmos para resolucao do TSP  """
	
	def __init__(self):
		pass
	
	def get_distance_matrix(self, cities):
		'''transforma a lista de cidades em uma matrix de custos'''

		size = len(cities) + 1

		M = [ [ 0 for _ in range(size) ] for __ in range(size) ]

		for i in cities:
			for j in cities:
				M[i.id][j.id] = self.distance(i, j)

		return M

	def pretty_print(self, M):
		'''imprime a matrix de custo de uma forma mais legivel'''
		print('\n'.join([''.join(['{:5}'.format(item) for item in row]) for row in M]))

	def distance(self, c1, c2):
		'''Calcula distancia ecludiana entre dois objectos cidade'''

		xd = c1.x - c2.x 
		yd = c1.y - c2.y 
		dij = int( math.sqrt( xd*xd + yd*yd) + 0.5 )

		# return infinito se o calculo for efetuado para a mesma cidade
		if dij == 0:
			return float("inf")
		else:
			return dij

	def distance_by_matrix(self, c1, c2, M):
		'''retorna distancia entre 2 cidades'''
		return M[c1.id][c2.id]

	def _nearest_neighbor(self, A, cities, M):
		'''
		retorna o vizinho mais proximo
		A => cidade atual
		Cities => possiveis vizinhos
		M => matrix de distancias
		'''
		
		min_d = float("inf")
		min_city = None
		for i in cities:
			ci = cities[i]

			if M[A.id][ci.id] < min_d:
				min_d = M[A.id][ci.id]
				min_city = ci

		return min_city

	def nn_tsp(self, cities, M):
		'''
		Retorna o caminho utilizando a heuristica do vizinho mais proximo
		cities => array de cidades (randomico ate aqui)
		M => matrix de distancias
		'''

		# cria se um mapa, utilizando o id das cidades como KEY
		mapa = { i.id : i for i in cities }

		startCity = mapa[1]
		del mapa[1]

		# primeira cidade da rota sera a cidade na posicao [startIndex] do array
		tour = [startCity]

		# enquanto existir cidades nao visitadas no mapa do...
		while len(mapa):
			lastVisitedCity = tour[-1]
			C = self._nearest_neighbor(lastVisitedCity, mapa, M)

			# adiciona na rota final
			tour.append(C)
			# remove cidade do mapa (para garantir o encerramento do while)
			del mapa[C.id]

		# adiciona a cidade original ao fim do rota final (volta do caixeiro para a cidade de origem)
		tour.append(startCity)

		return tour

	def print_tour(self, cities):
		for i in cities:
			print (i)

	def print_tour_simple(self, cities):
		string = ""
		for i in cities:
			string += str(i.id) + " "

		print (string)

	def plot_cities(self, cities):
		fig = plt.figure(figsize=(11, 6))
		ax = fig.add_subplot(111)

		Xs = [ i.x for i in cities ]
		Ys = [ i.y for i in cities ]

		plt.scatter(Xs, Ys, marker='o', cmap=plt.get_cmap('Spectral'))
		plt.plot(Xs, Ys)
		
		for i in cities:                                    
			ax.annotate(i.id, [i.x, i.y], textcoords='data')
		
		plt.show(block = False)

	def get_cost(self, tour, M):
		
		deque_cities = collections.deque(tour)

		total_cost = 0

		current_city = deque_cities.popleft()

		while len(deque_cities):
			next_city = deque_cities.popleft()

			total_cost += self.distance_by_matrix(current_city, next_city, M)

			current_city = next_city

		return total_cost

	def _swap(self, tour, i1, i2):
		clone = tour[:]

		aux = clone[i1]
		clone[i1] = clone[i2]
		clone[i2] = aux

		return clone

	def swap_2opt(self, tour, M):
		'''
		movimento de vizinhanca 2opt

		Utiliza o movimento ate encontrar um minimo local (o algoritmo nao consegue melhorar)
		'''
		
		min_cost = self.get_cost(tour, M)
		min_tour = tour[:]

		for i in range(1, len(min_tour) - 3 ):
			for j in range(i + 1, len(min_tour) - 2 ):

				new_tour = self._swap(min_tour, i, j)
				new_cost = self.get_cost(new_tour, M)

				if new_cost < min_cost:
					#print ("FOUND ! 2opt: " + str(new_cost) )
					min_cost = new_cost
					min_tour = new_tour
		
		return min_tour

	# mesma logica do 2opt, a mudanca agora ocorrem em 3 arestas 
	def swap_3opt(self, tour, M):
		
		min_cost = self.get_cost(tour, M)
		min_tour = tour[:]

		for i in range(1, len(min_tour) - 4 ):
			for j in range(i + 1, len(min_tour) - 3 ):

				new_tour = self._swap(min_tour, i, j)
				new_tour2 = self._swap(new_tour, j, j+1)
				new_cost = self.get_cost(new_tour2, M)

				#print("Trocando " + str(i) + " Com " + str(j) )
				if new_cost < min_cost:
					#print ("FOUND 3opt! : " + str(new_cost) )
					min_cost = new_cost
					min_tour = new_tour2
		 
		return min_tour

	def VND(self, tour, M):
		'''
		O vnd tenta melhorar a rota utilizando os movimentos de vizinhanca 2opt e 3opt.
		
		O algoritmo ira utilizar o 2opt ate que se atinja um minimo local (sem mais melhorars),
		apos o minimo local do 2opt, o 3opt eh chamado, Se houver ganhas na rota o algoritmo repete todo 
		o processo com o 2opt. 
		
		ele so vai parar quando nen o 2opt nen o 3opt obtiverem resultados melhores
		'''
		
		min_cost = self.get_cost(tour, M)
		min_tour = tour[:]

		size = len(tour)

		cost3opt = float("inf")

		while True:

			#print ("\nStarting 2opt...\n")
			tour2opt = self.swap_2opt(min_tour, M)
			cost2opt = self.get_cost(tour2opt, M)

			if cost2opt < min_cost:
				min_tour = tour2opt
				min_cost = cost2opt
				continue

			# chegou no minimo local (2opt e 3opt nao conseguiram nenhum improvment)
			elif cost3opt == min_cost:
				break

			elif cost2opt == min_cost: # apos o 2opt, tenta aprimorar ainda mais com o 3opt

				while True:
					#print ("\nStarting 3opt...\n")
					tour3opt = self.swap_3opt(min_tour, M)
					cost3opt = self.get_cost(tour3opt, M)

					if cost3opt < min_cost: # se o 3opt obter resutaods, volta pro 2opt
						min_tour = tour3opt
						min_cost = cost3opt
						break

					elif cost3opt == min_cost: # se nao conseguir melhores resultados => volta pro 2opt
						break

		return min_tour

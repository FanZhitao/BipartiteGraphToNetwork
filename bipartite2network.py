file = open('ratings.dat', 'r')

# Assume movie no is no more than 3952.
# The memory space of movie bitmap of each user is 3952/8 = 494 Bytes
#
# Assume there are no more than 6040 users.
# The memory space is 494 * 6040 + 6040 ^ 2 Bytes (for Network) = 39,465,360 Bytes, approximately 38 MiB

# initialization
user_count, movie_count = 6040, 3952
movie_range = int(movie_count / 8) + 1
bitmap = [[0 for x in range(movie_range)] for x in range(user_count + 1)]
network = [[0 for x in range(user_count)] for x in range(user_count)]

# generate bitmap
#max_user, max_movie = 0, 0 #debug code
for line in file:
	arr = line.split('::')
	user, movie = int(arr[0]), int(arr[1])
	#max_user, max_movie = max(user, max_user), max(movie, max_movie) #debug code
	bitmap[user][movie / 8] |= 1 << (movie % 8)

# update network
for user_i in range(1, user - 1):
	for user_j in range(user_i + 1, user_count):
		for movie_batch in range(movie_range):
			if (bitmap[user_i][movie_batch] & bitmap[user_j][movie_batch] != 0):
				# user i and j have rated at least one same movie
				network[user_i][user_j] = network[user_j][user_i] = 1
				break

#print max_user, max_movie #debug code

# output to file
output = open('network.dat', 'w')
for i in range(1, user_count):
	for j in range(1, user_count):
		output.write(str(i) + ' ' + str(j) + ': ' + str(network[i][j]) + '\n')
output.close()
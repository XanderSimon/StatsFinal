import time
import numpy

' Can be changed, but we thought that 6 was a fair number to use'
global_rounding = 6

' Creates an NxN square matrix of the users choosing. The matrix must be a markov chain such that the sum of the rows is 1 (although there is some leeway due to rounding) with each entry being the probability of going from one state to the next. The function takes in no parameters because these are defined by the user in the command line '
def create_matrix():
  ' Determines the size of the matrix and validates the input'
  matrix_bool = False
  while not matrix_bool:
    try:
      matrix_size = int(input("What is the size of your square matrix? "))
      matrix = [[] for _ in range(matrix_size)]
      matrix_bool = True
    except:
      print('Your input must be a number')

  ' Builds the matrix row by row, validating each row before adding to the matrix'
  row = 0
  while row < matrix_size:
    input_str = "Please enter the {} items seperated by spaces for row #{} of your matrix:\n".format(matrix_size, row+1)
    row_bool = False
    while not row_bool:
      try:
        current_row = numpy.array(input(input_str).split())
        current_row = current_row.astype(float)
        row_length = len(current_row)
        row_sum = round(numpy.sum(current_row),global_rounding)
        row_bool = True
      except:
        print('Your input must be {} probabilities separated by spaces'.format(matrix_size))

    ' Checks if the row is appropriate based on the matrix size and the sum of the row equaling 1'
    if row_length != matrix_size:
      print("Row must have ", matrix_size, " items. Please try again:")
    elif (row_sum != 1.000):
      print("Row must sum to exactly 1 as each entry must be a probability for this markov matrix. Please try again")
    else:
      matrix[row] = current_row
      row += 1
  matrix = numpy.matrix(matrix)

  ' Ensures this is the matrix the user wants before proceeding to the operations '
  matrix_str = "This is your matrix, does it look correct (Y/N)\n{}\n".format(matrix)
  correct_matrix = input(matrix_str)
  if correct_matrix == "Y":
    print("Good!")
    return matrix
  elif correct_matrix == "N":
    print("Ok, we will restart")
    create_matrix()
  else:
    print("Neither Y or N was given so we will assume you want to restart")
    create_matrix()

' Finds the fixed vector given the matrix and also counts the steps to reach this fixed vector. This function can be called if the user wants to check the amount of steps to reach the fixed vector or if they want to find the fixed vector. Only works on regular matrices though. '
def find_vector_and_steps(matrix, want_steps, counter=1):
  if not is_regular(matrix):
    print('This is not a regular matrix and therefore there is no fixed vector')
    return
  new_matrix = numpy.linalg.matrix_power(matrix, counter)
  rounded_matrix = new_matrix.round(global_rounding)
  if check_matrix(rounded_matrix):
    if want_steps:
      print("It took {} steps to reach the fixed vector (rounded to {} decimals)".format(counter-1, global_rounding))
    else:
      print("The fixed vector is {}".format(rounded_matrix[0]))
    return rounded_matrix[0]
  else:
    find_vector_and_steps(matrix, want_steps, counter+1)

' Checks if a matrix has reached its fixed vector state by comparing each of the elements of a column together to see if they match '
def check_matrix(matrix):
  transpose = matrix.T
  for row in transpose:
    if(not numpy.all(row == row[0])):
      return False
  return True

' Determines if a matrix is ergotic by keeping track of the number of times each entry in the matrix has been visited over 100 steps to see if the matrix is fully connected. '
def is_ergodic(matrix, reached_matrix, counter=1):
  new_matrix = numpy.linalg.matrix_power(matrix, counter)
  flat_matrix = numpy.ravel(new_matrix)
  flat_reached_matrix = numpy.ravel(reached_matrix)
  for index in range(len(flat_matrix)):
    if flat_matrix[index] != 0:
      flat_reached_matrix[index] = 1
  if numpy.any(reached_matrix == 0):
    if counter <= 100:
      is_ergodic(matrix, reached_matrix, counter+1)
    else:
      print('It appears that this matrix might not be ergodic as there are still entries that have not been reached in the matrix after 100 steps')
      return False
  else:
    print('Yes, this matrix is ergodic')
    return True

' Determines if a matrix is regular by seeing if there are any entries with 0 probability after 100 steps. '
def is_regular(matrix):
  new_matrix = numpy.linalg.matrix_power(matrix, 100)
  output = numpy.any(new_matrix == 0)
  if output:
    return False
  else:
    return True

' Finds the first absorbing state in which the diagonal of a matrix has a probability of 1. '
def find_absorbing(matrix):
  diagonals = numpy.diagonal(matrix)
  output = numpy.any(diagonals == 1)
  if output:
    diag_list = diagonals.tolist()
    absorbing = diag_list.index(1.0)
    print('This matrix has an absorbing state at {}'.format(absorbing+1))
  else:
    print('This matrix has no absorbing state')

' Finds the state of the matrix after n steps'
def n_steps(matrix, n):
  return numpy.linalg.matrix_power(matrix, n).round(global_rounding)

' Provides the list of inputs and calls the proper functions so a user can interact with the program. '
def next_steps(matrix):
  step_str = "You can do any of the below:\n\
    1. Check if it is ergodic - type 'ergodic'\n\
    2. Check if it is regular - type 'regular'\n\
    3. If it is not ergodic, check which state is absorbing - type 'absorbing'\n\
    4. Find the fixed vector of the matrix if it is regular - type 'find vector'\n\
    5. Find the number of steps to reach a fixed vector if it is regular - type 'count steps'\n\
    6. Find the state of the matrix after N steps - type 'n steps'\n\
    7. End program - type 'end'"
  print(step_str)
  while True:
    function_call = input("What would you like to do with your matrix? ")
    if function_call == 'ergodic':
      is_ergodic(matrix, numpy.zeros(matrix.size))
    elif function_call == 'regular':
      if is_regular(matrix):
        print('Yes, the matrix is regular')
      else:
        print('It appears that this matrix might not be regular as there are still entries in the matrix that have 0 probability after 100 steps')
    elif function_call == 'absorbing':
      find_absorbing(matrix)
    elif function_call == 'find vector':
      find_vector_and_steps(matrix, False)
    elif function_call == 'count steps':
      find_vector_and_steps(matrix, True)
    elif function_call == 'n steps':
      step_bool = False
      while not step_bool:
        try:
          n = int(input("How many steps would you like? "))
          new_matrix = n_steps(matrix, int(n))
          step_bool = True
        except:
          print('Your input must be an integer')
      print("This is what your matrix looks like after {} steps:\n{}".format(n, new_matrix))
    elif function_call == 'end':
      return
    else:
      print("You did not provide one of the inputs")
    time.sleep(3)

' The functions that are actually called when the program runs. They call the appropriate functions depending on the users input '
global_matrix =  create_matrix()
next_steps(global_matrix)

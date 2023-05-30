def flatList(list_of_lists, flat_list=[]):
  if not list_of_lists:
    return flat_list
  else:
    for item in list_of_lists:
      if type(item) == list:
        flatList(item, flat_list)
      else:
        flat_list.append(item)
  return flat_list



def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class style():
  BLACK = '\033[30m'
  RED = '\033[31m'
  GREEN = '\033[32m'
  YELLOW = '\033[33m'
  BLUE = '\033[34m'
  MAGENTA = '\033[35m'
  CYAN = '\033[36m'
  WHITE = '\033[37m'
  UNDERLINE = '\033[4m'
  RESET = '\033[0m'

  INFO = BLUE
  OK = GREEN
  WARN = YELLOW
  ERROR = RED


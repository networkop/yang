
def write_file(fn, text):
    with open(fn, 'w') as f:
        f.write(text)

def read_file(fn):
   with open(fn) as f:
      result = f.read()
   return result

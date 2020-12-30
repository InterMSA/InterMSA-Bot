import asyncio, re

def edit_file(file, value):
   with open(file, 'r+') as f:
      lines = f.readlines()
      f.seek(0); found = False
      for line in lines:
         line = line.strip('\n')
         if str(line).lower() != str(value).lower():
            f.write(line + '\n')
         else:
            found = True
      f.truncate()
      return found

with open("verify.txt")as f:
   print(f.readlines())
   print(edit_file("verify.txt", "3968 djm65@njit.edu 233691753922691072 Brother"))

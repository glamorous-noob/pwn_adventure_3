#!/usr/bin/python3

# Quick script to generate a markdown table of contents
# The script is entirely based on the document format I am using for this project
# The script is not clean nor secure, I don't recommend using it blindly

from sys import stdin, stdout
import string

alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
header_2_start = "## "
header_3_start = "### "

if __name__ == "__main__":

  titles = []
  lines = []
  ind=None
  for line in stdin:
    lines.append(line)
    if ind==None and line.startswith(header_2_start):
      ind=len(lines)
    elif line.startswith(header_3_start):
      titles.append(line[len(header_3_start):].strip())
  
  lines.insert(ind,header_3_start+'Contents\n')
  ind+=1
  for title in titles:
    link = "".join(c for c in title.lower().replace(' ','-') if c in alphabet)
    lines.insert(ind,"["+title+"](#"+link+")\n\n")
    ind+=1
  lines.insert(ind,'------\n')
  
  for line in lines:
    stdout.write(line)
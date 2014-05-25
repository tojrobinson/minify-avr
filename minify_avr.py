#!/usr/bin/env python

import sys, string, re

if len(sys.argv) < 2:
   print 'must provide .asm input file'
   sys.exit(1)

symbols = string.ascii_lowercase
i = 0
conflict = ''

mappings = {}
first_pass = []

with open(sys.argv[1], 'r') as fd:
   for line in fd:
      line = line.strip().lower()
      if not line or line[0] == ';':
         continue

      if re.search(r'^\.(?:def|equ)', line):
         parts = re.search(r'([^ ]+\s+)([^ ]+)(.*)', line)
         prefix = parts.group(1)
         token = parts.group(2)
         suffix = conflict + parts.group(3)
      elif re.search(r'^[^ :]+:', line):
         parts = re.search(r'(^[^ :]+)(:.*)', line)
         prefix = ''
         token = parts.group(1)
         suffix = conflict + parts.group(2)
      else:
         token = None

      if token:
         s = mappings.get(token, None)
         if s:
            line = prefix + s + suffix
         else:
            mappings[token] = symbols[i]
            line = prefix + symbols[i] + suffix
            i += 1

            if i == len(symbols):
               i = 0
               conflict += '_'

         if prefix == '' and len(suffix) == 1:
            line = line + ' '
            first_pass.append(line)
            continue
      first_pass.append(line + '\n')

with open('out.asm', 'w+') as fd:
   for line in first_pass:
      if not re.search(r'\.(?:db|include)', line):
         line = re.sub(r' +', ' ', line)
         for key in mappings.keys():
            line = re.sub(r'\b' + key + r'\b', mappings.get(key), line)

      parts = re.search(r'^(\.(?:def|equ))(.*)', line)

      if parts:
         line = parts.group(1) + ' ' + re.sub(r' *', '', parts.group(2)) + '\n'
      fd.write(line)

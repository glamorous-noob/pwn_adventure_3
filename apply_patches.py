#!/usr/bin/python3

def use_mana_patch(gamelogic_bytes):
  start_addr=0x519c3
  print("Player.useMana() never decreases mana")
  for i in range(start_addr, start_addr+4):
    gamelogic_bytes[i]=0x90

def cant_be_damaged(gamelogic_bytes):
  start_addr=0x7726c
  print("Player.canBeDamaged() returns false")
  gamelogic_bytes[start_addr]=0xc0
  gamelogic_bytes[start_addr+1]=0x16
    
patch_strings=["Mana never decreases when used (Infinite Mana)", \
                "Player can't be damaged (Infinite Health)", \
                ] 
patch_funcs=[use_mana_patch, \
              cant_be_damaged, \
              ]
apply_patch = dict()
for s,f in zip(patch_strings, patch_funcs):
  apply_patch[s]=f

if __name__=='__main__':
  from sys import argv
  filename="GameLogic.dll"
  if len(argv)>1:
    filename=argv[1]
  file_ext="."+filename.split(".")[-1]
  filename=filename[:-len(file_ext)]
  s="Available Patches:"
  print(s)
  print("-"*len(s))
  for i in range(len(patch_strings)):
    s=patch_strings[i]
    print("#"+str(i+1)+" -", s)
  print("\nEnter the numbers for the patches you wish to apply, separated by commas")
  print("Enter '0' to apply all of them")
  user_in=input("Patch numbers : ").strip()
  if user_in:
    if user_in=="0":
      indexes=[i+1 for i in range(len(patch_strings))]
    else:
      indexes = [int(e) for e in user_in.split(",")]
    if indexes:
      infile=open(filename+file_ext, "rb")
      gamelogic_bytes = bytearray(infile.read())
      infile.close()
      for i in indexes:
        apply_patch[patch_strings[i-1]](gamelogic_bytes)
      outfile=open(filename+"_patch_"+"_".join(str(i) for i in indexes)+file_ext, "wb")
      outfile.write(bytes(gamelogic_bytes))
      outfile.close()
  else:
    print("meh")
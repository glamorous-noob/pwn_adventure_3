#!/usr/bin/python3

# code_diff == 0x1004ec5b-0x4e0x5b == 0x10000c00
# rdata_diff == 0x1006f000 - 0x6de00 == 0x10001200

def nop_bytes(gamelogic_bytes, start_addr, n):
  for i in range(start_addr, start_addr+n):
    gamelogic_bytes[i] = 0x90


def replace_bytes(gamelogic_bytes, start_addr, replacement_bytes):
  n = len(replacement_bytes)
  for i in range(n):
    gamelogic_bytes[start_addr+i]=replacement_bytes[i]
    
def use_mana_patch(gamelogic_bytes):
  print("Player.useMana() never decreases mana")
  nop_bytes(gamelogic_bytes, 0x519c3, 4)

def cant_be_damaged_patch(gamelogic_bytes):
  print("Player.canBeDamaged() returns false")
  replace_bytes(gamelogic_bytes, 0x7726c, [0xc0, 0x16])

def player_call_actor_damage_patch(gamelogic_bytes):
  print("Player.Damage() doesn't call Actor.Damage()")
  replace_bytes(gamelogic_bytes, 0x505d6, [0x23, 0x0f])
  
patch_strings=["Mana never decreases when used (Infinite Mana)", \
                "Player can't be damaged (Infinite Health)", \
                "Received damage is never applied (Infinite Health)" \
                ] 
patch_funcs=[use_mana_patch, \
              cant_be_damaged_patch, \
              player_call_actor_damage_patch \
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
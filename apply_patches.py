#!/usr/bin/python3

# code_diff == 0x1004ec5b-0x4e0x5b == 0x10000c00
# rdata_diff == 0x1006f000 - 0x6de00 == 0x10001200

def virtual_address_to_file_offset(a):
  return a-0x10000c00

def bytes_string_to_list(s):
  return list(bytes.fromhex(s.replace(" ","")))

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
  print()

def cant_be_damaged_patch(gamelogic_bytes):
  print("Player.canBeDamaged() returns false")
  replace_bytes(gamelogic_bytes, 0x7726c, [0xc0, 0x16])
  print()

def player_call_actor_damage_patch(gamelogic_bytes):
  print("Player.Damage() doesn't call Actor.Damage()")
  replace_bytes(gamelogic_bytes, 0x505d6, [0x23, 0x0f])
  print()

def sudden_death_patch(gamelogic_bytes):
  offset = virtual_address_to_file_offset(0x100020c2)
  patch_bytes = bytes_string_to_list("8b 47 30")
  print("Actor.Damage() drops health to 0 disregarding the value of the damage")
  replace_bytes(gamelogic_bytes, offset, patch_bytes)
  print()

def gun_shop_change_greeting(gamelogic_bytes):
  print("GunShopOwner greets you differently")
  new_s = "Such glamorous_noob. Much free stuff."
  replace_bytes(gamelogic_bytes, 0x74fdc, new_s.encode('ascii')+b'\x00')
  
def buy_price_item_always_0_patch(gamelogic_bytes):
  print("NPC.GetBuyPriceForItem() always returns 0 & Player.PerformBuyItem() accepts price==0")
  replace_bytes(gamelogic_bytes, 0x4e05b, [0x31, 0xc0])
  nop_bytes(gamelogic_bytes, 0x53cee, 2)
  gun_shop_change_greeting(gamelogic_bytes)
  print()
  
def memset_player_cons(gamelogic_bytes):
  address = virtual_address_to_file_offset(0x10050190)
  patch_bytes = bytes_string_to_list("51 52 68 bc 00 00 00 68 00 00 00 00 8d 87 2c 01 00 00 50 e8 14 59 01 00 83 c4 0c 5a 59 eb 31")
  print('Tweaking the Player constructor to make space for patches')
  replace_bytes(gamelogic_bytes, address, patch_bytes)

def rich_bitch_patch(gamelogic_bytes):
  memset_player_cons(gamelogic_bytes)
  offset = virtual_address_to_file_offset(0x100501af)
  patch_bytes = bytes_string_to_list("50 51 e8 ea 0a fd ff 89 c1 e8 53 2f fc ff 50 90 e8 5c dc fc ff 68 00 00 00 00 68 ff ff ff 7f 50 8b 03 89 d9 ff 90 30 00 00 00 59 58 e9 b0 84 fe ff")
  print("Code for adding coins is insearted in dead area in Player constructor") 
  replace_bytes(gamelogic_bytes, offset, patch_bytes)
  offset = virtual_address_to_file_offset(0x1003868b)
  patch_bytes = bytes_string_to_list("e9 1f 7b 01 00 5f 5b 5d c2 04 00")
  print("Maximum amount of money is added when Great Balls of Fire spell is fired")
  replace_bytes(gamelogic_bytes, offset, patch_bytes)
  print()

def not_paying_patch(gamelogic_bytes):
  offset = virtual_address_to_file_offset(0x100548f4)
  patch_bytes = bytes_string_to_list("eb 22 90")
  print("RemoveItem is not called in PerformBuyItem. Bying does not decrease money.") 
  replace_bytes(gamelogic_bytes, offset, patch_bytes)

def increase_speed_patch(gamelogic_bytes):
  print("Walking speed set to 800.00 instead of 200.00")
  offset = virtual_address_to_file_offset(0x100502db)
  patch_bytes = bytes_string_to_list("00 00 48 44")
  replace_bytes(gamelogic_bytes, offset, patch_bytes)
  print("Jumping speed set to 800.00 instead of 420.00")
  offset = virtual_address_to_file_offset(0x100502e5)
  replace_bytes(gamelogic_bytes, offset, patch_bytes)
  print()

patch_strings=["Mana never decreases when used (Infinite Mana)", \
                "Player can't be damaged (Infinite Health)", \
                "Received damage is never applied (Infinite Health)", \
                "Sudden death: 1 hit = 1 kill. Combine with \"Infinite Health\" for protection.",\
                "NPCs' items prices are 0 (Free Merchandise)", \
                "Don't pay for stuff you can afford", \
                "Become a rich bitch when you shoot Great Balls of Fire (Max Amount of Money)", \
                "Walking and jumping speed increased"
                ] 
patch_funcs=[use_mana_patch, \
              cant_be_damaged_patch, \
              player_call_actor_damage_patch, \
              sudden_death_patch, \
              buy_price_item_always_0_patch, \
              not_paying_patch, \
              rich_bitch_patch, \
              increase_speed_patch
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
  print()
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
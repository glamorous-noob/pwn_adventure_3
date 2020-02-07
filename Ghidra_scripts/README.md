# Scripts created during this project

While suffering my way into understanding how to tackle this game, I had several ideas. Most of them demanded me to do stuff that was very repetitive and time-consuming. So I thought I'd automate it.

This folder contains the list of the scripts I've made so far.

## Scripts

### Rename_vftable_funcs.py

It works like this:

- You place the cursor at the beginning of the vftable of `GlamorousClass`
- You run the script
- BAM all of its functions that still had their default name are renamed to `TGN_GlamorousClass_vftable[index_in_vftable]`

Sometimes a derived class's vftable will contain a lot of the base class's functions. This script tries to make them easier to spot by giving the functions meaningful names about their position in a class's vftable.

The most convenient way to use this script in my opinion is to start with the base classes and then move down to the deriving classes. You should check the RTTI structures in order to know class hierarchy.

It also sets the calling convention of the vftable functions to ` __this_call` ([default calling convention in c++ with a few exceptions](https://docs.microsoft.com/en-us/cpp/cpp/thiscall?view=vs-2019)), and activates custom variable storage. Custom variable storage is a prerequisite for retyping `this` from `void *` to `GlamorousClass *` for example (to be done manually or by other scripts)
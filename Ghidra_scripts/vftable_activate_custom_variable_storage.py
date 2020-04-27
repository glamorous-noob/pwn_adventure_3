# Activates custom variable storage in all of the vftable functions
#@category TheirGlamorousNoobness
# The script expects the currentAddress to be equal to the beginning of the vftable
# Do not use it unless you understand it line by line

from ghidra.program.model.symbol import SourceType, SymbolType

vftableAddress = currentAddress
naming_prefix = "TGN_"

code_manager = currentProgram.getCodeManager()
func_manager = currentProgram.getFunctionManager()

d = code_manager.getDataAt(vftableAddress)
assert(d.isArray())

assert(d.getPrimarySymbol().getParentNamespace().getSymbol().getSymbolType()==SymbolType.CLASS)
class_name = d.getPrimarySymbol().getParentNamespace().getName()

for i in range(d.getNumComponents()):
  comp = d.getComponent(i)
  assert(comp.isPointer())
  func_addr = comp.getValue()
  func = func_manager.getFunctionAt(func_addr)
  assert(func!=None)
  func.setCustomVariableStorage(True)

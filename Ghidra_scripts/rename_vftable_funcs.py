# Renames functions of a vftable who still have their default name "FUN_0xsomething"
#@category TheirGlamorousNoobness
# The script expects the currentAddress to be equal to the beginning of the vftable
# The default "vftable" symbol name is renamed to improve readability
# __thiscall and custom variable storage are set to all of the vftable's functions
# Do not use it unless you understand it line by line

from ghidra.program.model.symbol import SourceType, SymbolType

vftableAddress = currentAddress
naming_prefix = "TGN_"

code_manager = currentProgram.getCodeManager()
func_manager = currentProgram.getFunctionManager()

d = code_manager.getDataAt(vftableAddress)
assert(d.isArray())

assert(d.getPrimarySymbol().getName() == "vftable")
assert(d.getPrimarySymbol().getParentNamespace().getSymbol().getSymbolType()==SymbolType.CLASS)
class_name = d.getPrimarySymbol().getParentNamespace().getName()

for i in range(d.getNumComponents()):
  comp = d.getComponent(i)
  assert(comp.isPointer())
  func_addr = comp.getValue()
  func = func_manager.getFunctionAt(func_addr)
  assert(func!=None)
  func_name = func.getName()
  if func_name == 'FUN_'+func_addr.toString() and func.getSymbol().getSource() == SourceType.DEFAULT:
    func.setName(naming_prefix+class_name+'_vftable'+comp.getFieldName(), SourceType.USER_DEFINED)
  func.setCallingConvention('__thiscall')
  func.setCustomVariableStorage(True)
d.getPrimarySymbol().setName(naming_prefix+class_name+"_vftable", SourceType.USER_DEFINED)

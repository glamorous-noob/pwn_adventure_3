# Renames functions of a vftable who still have their default name "FUN_0xsomething"
#@category TheirGlamorousNoobness
# The script expects the currentAddress to be equal to the beginning of the vftable
# A label is added at the beginning of the vftable, functions with default names are renamed
# __thiscall and custom variable storage are set to all of the vftable's functions

from ghidra.program.model.symbol import SourceType
from ghidra.app.cmd.label import AddLabelCmd

vftableAddress = currentAddress

code_manager = currentProgram.getCodeManager()
func_manager = currentProgram.getFunctionManager()

d = code_manager.getDataAt(vftableAddress)
assert(d.isArray())

vftable_title = d.getComment(3).replace('const ', '').split('::')
assert(vftable_title[1]=='vftable')
class_name = vftable_title[0]

symbols = currentProgram.getSymbolTable().getGlobalSymbols(class_name)
assert (any(symb.getSymbolType().toString() == "Class" for symb in symbols))

for i in range(d.getNumComponents()):
  comp = d.getComponent(i)
  assert(comp.isPointer())
  func_addr = comp.getValue()
  func = func_manager.getFunctionAt(func_addr)
  assert(func!=None)
  func_name = func.getName()
  if func_name == 'FUN_'+func_addr.toString() and func.getSymbol().getSource() == SourceType.DEFAULT:
    func.setName('TGN_'+class_name+'_vftable'+comp.getFieldName(), SourceType.USER_DEFINED)
  func.setCallingConvention('__thiscall')
  func.setCustomVariableStorage(True)
AddLabelCmd(vftableAddress, 'TGN_'+class_name+"_vftable", SourceType.USER_DEFINED).applyTo(currentProgram)


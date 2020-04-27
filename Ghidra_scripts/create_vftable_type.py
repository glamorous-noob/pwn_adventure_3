# Creates type for vftable
#@category TheirGlamorousNoobness
# The script expects the currentAddress to be equal to the beginning of the vftable
# A vftable type is created and the names of its fields named after the vftable functions names
# The fields are typed as dword returning __thiscall function pointers
# Do not use it unless you understand it line by line

from ghidra.program.model.symbol import SourceType, SymbolType
from ghidra.program.model.data import CategoryPath, StructureDataType, DataTypeConflictHandler, PointerDataType, FunctionDefinitionDataType, DWordDataType, GenericCallingConvention

naming_prefix = "TGN_"
categoryPathString = "/TGN"
vftableAddress = currentAddress

code_manager = currentProgram.getCodeManager()
typeManager = currentProgram.getDataTypeManager()
func_manager = currentProgram.getFunctionManager()

d = code_manager.getDataAt(vftableAddress)
assert(d.isArray())
assert(d.getPrimarySymbol().getParentNamespace().getSymbol().getSymbolType()==SymbolType.CLASS)
class_name = d.getPrimarySymbol().getParentNamespace().getName()
vftable_classname = naming_prefix+class_name+"_vftable"

l = []
typeManager.findDataTypes(vftable_classname,l)

if l!=[]:
  print("Class "+vftable_classname+" already exists. Nothing is changed.")
else:
  category = typeManager.createCategory(CategoryPath(categoryPathString))
  vftable_type = StructureDataType(vftable_classname, 0)
  for i in range(d.getNumComponents()):
    comp = d.getComponent(i)
    assert(comp.isPointer())
    func_addr = comp.getValue()
    func = func_manager.getFunctionAt(func_addr)
    assert(func!=None)
    func_name = func.getName()
    func_dt = FunctionDefinitionDataType("TGN_func")
    func_dt.setGenericCallingConvention(GenericCallingConvention.thiscall)
    func_dt.setReturnType(DWordDataType())
    datatype = PointerDataType(func_dt)
    vftable_type.insert(i, datatype, datatype.getLength(), func_name, "TGN: Automatically created field")
  category.addDataType(vftable_type, DataTypeConflictHandler.REPLACE_HANDLER)
  
from collections import defaultdict
from typing import TYPE_CHECKING

from classiq.interface.generator.constant import Constant
from classiq.interface.generator.types.compilation_metadata import CompilationMetadata
from classiq.interface.generator.types.enum_declaration import EnumDeclaration
from classiq.interface.generator.types.qstruct_declaration import QStructDeclaration
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.model.native_function_definition import (
    NativeFunctionDefinition,
)

if TYPE_CHECKING:
    from classiq.qmod.quantum_function import GenerativeQFunc


class ModelStateContainer:
    enum_decls: dict[str, EnumDeclaration]
    type_decls: dict[str, StructDeclaration]
    qstruct_decls: dict[str, QStructDeclaration]
    native_defs: dict[str, NativeFunctionDefinition]
    constants: dict[str, Constant]
    functions_compilation_metadata: dict[str, CompilationMetadata]
    generative_functions: dict[str, "GenerativeQFunc"]
    function_dependencies: dict[str, list[str]]

    def reset(self) -> None:
        self.enum_decls = {}
        self.type_decls = {}
        self.qstruct_decls = {}
        self.native_defs = {}
        self.constants = {}
        self.functions_compilation_metadata = {}
        self.generative_functions = {}
        self.function_dependencies = defaultdict(list)


QMODULE = ModelStateContainer()
QMODULE.reset()

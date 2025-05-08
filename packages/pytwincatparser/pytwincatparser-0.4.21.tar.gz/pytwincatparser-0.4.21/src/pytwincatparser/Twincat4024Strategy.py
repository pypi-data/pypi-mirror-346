import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path, PurePath, PureWindowsPath
from typing import List, Optional

from .BaseStrategy import BaseStrategy
from .Loader import add_strategy
from .TwincatObjects.tc_plc_object import (
    Dut,
    Get,
    Itf,
    Method,
    Pou,
    Property,
    Set,
    TcPlcObject,
    Gvl,
)
from .TwincatObjects.tc_plc_project import Compile, Project, PlaceholderReference
from . import TwincatDataclasses as tcd


from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

logger = logging.getLogger(__name__)





def parse_documentation(declaration: str) -> Optional[tcd.Documentation]:
    """
    Parse documentation comments from a declaration string.

    Args:
        declaration: The declaration string containing documentation comments.

    Returns:
        A TcDocumentation object or None if no documentation is found.
    """
    if not declaration:
        return None

    # Extract only the part before the first variable block
    var_pattern = re.compile(
        r"VAR(?:_INPUT|_OUTPUT|_IN_OUT|_INST|_STAT|_GLOBAL|[ ]CONSTANT)?", re.DOTALL
    )
    struct_pattern = re.compile(r"STRUCT", re.DOTALL)

    # Find the position of the first variable block
    var_match = var_pattern.search(declaration)
    struct_match = struct_pattern.search(declaration)

    # Determine the end position of the documentation block
    end_pos = len(declaration)
    if var_match:
        end_pos = min(end_pos, var_match.start())
    if struct_match:
        end_pos = min(end_pos, struct_match.start())

    # Extract only the part before the first variable block
    doc_part = declaration[:end_pos]

    # Define regex patterns for different comment styles
    # 1. Multi-line comment: (* ... *)
    # 2. Single-line comment: // ...
    # 3. Multi-line comment with stars: (*** ... ***)
    multiline_comment_pattern = re.compile(r"\(\*\s*(.*?)\s*\*\)", re.DOTALL)
    singleline_comment_pattern = re.compile(r"//\s*(.*?)$", re.MULTILINE)

    # Extract all comments
    comments = []

    # Check for multi-line comments
    for match in multiline_comment_pattern.finditer(doc_part):
        comments.append(match.group(1).strip())

    # Check for single-line comments
    single_line_comments = []
    for match in singleline_comment_pattern.finditer(doc_part):
        single_line_comments.append(match.group(1).strip())

    if single_line_comments:
        comments.append("\n".join(single_line_comments))

    if not comments:
        return None

    # Join all comments
    comment_text = "\n".join(comments)

    # Parse documentation tags
    doc = tcd.Documentation()

    # Define regex patterns for documentation tags
    details_pattern = re.compile(r"@details\s*(.*?)(?=@\w+|\Z)", re.DOTALL)
    usage_pattern = re.compile(r"@usage\s*(.*?)(?=@\w+|\Z)", re.DOTALL)
    returns_pattern = re.compile(r"@return\s*(.*?)(?=@\w+|\Z)", re.DOTALL)
    custom_tag_pattern = re.compile(r"@(\w+)\s*(.*?)(?=@\w+|\Z)", re.DOTALL)

    # Helper function to clean up tag content
    def clean_tag_content(content):
        if content:
            # Remove lines that are just asterisks
            content = re.sub(r"^\s*\*+\s*$", "", content, flags=re.MULTILINE)
            # Remove trailing asterisks and whitespace
            content = re.sub(r"\s*\*+\s*$", "", content)
            # Remove leading asterisks and whitespace from each line
            content = re.sub(r"^\s*\*+\s*", "", content, flags=re.MULTILINE)
            # Remove leading and trailing whitespace
            content = content.strip()
            # Replace multiple whitespace with a single space
            content = re.sub(r"\s+", " ", content)
        return content

    # Extract details
    details_match = details_pattern.search(comment_text)
    if details_match:
        doc.details = clean_tag_content(details_match.group(1))

    # Extract usage
    usage_match = usage_pattern.search(comment_text)
    if usage_match:
        doc.usage = clean_tag_content(usage_match.group(1))

    # Extract returns
    returns_match = returns_pattern.search(comment_text)
    if returns_match:
        doc.returns = clean_tag_content(returns_match.group(1))

    # Extract custom tags
    for match in custom_tag_pattern.finditer(comment_text):
        tag_name = match.group(1)
        tag_value = clean_tag_content(match.group(2))
        if tag_name not in ["details", "usage", "return"]:
            doc.custom_tags[tag_name] = tag_value

    return doc


def parse_variables(declaration: str) -> List[tcd.Variable]:
    """
    Parse variables from a declaration string.

    Args:
        declaration: The declaration string containing variable sections.

    Returns:
        A list of tcd.Variable objects.
    """
    if not declaration:
        return []

    # Define regex patterns
    section_pattern = re.compile(
        r"(VAR(?:_INPUT|_OUTPUT|_IN_OUT|_INST|_STAT|_GLOBAL|[ ]CONSTANT)?)\s*(.*?)END_VAR",
        re.DOTALL,
    )
    struct_pattern = re.compile(r"STRUCT\s*(.*?)END_STRUCT", re.DOTALL)
    attribute_pattern = re.compile(
        r"\{attribute\s+\'([^\']+)\'\s*(?:\:=\s*\'([^\']*)\')?\}"
    )
    comment_pattern = re.compile(
        r"(?://(.*)$)|(?:\(\*\s*(.*?)\s*\*\))|(?:\(\*\*\*(.*?)\*\*\*\))",
        re.MULTILINE | re.DOTALL,
    )

    # Find all variables
    variables = []

    # Process VAR sections
    for section_match in section_pattern.finditer(declaration):
        section_type = section_match.group(1).strip()
        section_content = section_match.group(2).strip()

        # Split the section content into lines
        lines = section_content.split("\n")



        for line in lines:
            # Process each line
            current_var = None
            current_attributes = {}

            line = line.strip()
            if not line:
                continue

            # Check for attribute
            attr_match = attribute_pattern.search(line)
            if attr_match:
                attr_name = attr_match.group(1)
                attr_value = attr_match.group(2) if attr_match.group(2) else ""
                current_attributes[attr_name] = attr_value
                continue

            # Check for variable declaration
            if ":" in line:
                # If we have a previous variable, add it to the list
                # if current_var:
                #     variables.append(current_var)
                #     current_var = None

                # Parse the new variable
                var_parts = line.split(":", 1)
                var_name = var_parts[0].strip()

                # Extract comment if present
                var_comment = None
                comment_match = comment_pattern.search(line)
                if comment_match:
                    # Get the first non-None group
                    for group in comment_match.groups():
                        if group:
                            var_comment = group.strip()
                            break

                # Remove comment from line for further processing
                if comment_match:
                    line = line[: comment_match.start()].strip()

                # Parse type and initial value
                type_value_parts = var_parts[1].strip()
                if ";" in type_value_parts:
                    type_value_parts = type_value_parts.rstrip(";")

                var_type = type_value_parts
                var_initial_value = None

                # Check for initial value
                if ":=" in type_value_parts:
                    type_init_parts = type_value_parts.split(":=", 1)
                    var_type = type_init_parts[0].strip()
                    var_initial_value = type_init_parts[1].strip()

                var_type = var_type.split(";")[0]

                doc = tcd.Documentation(details=var_comment)

                # Create the variable
                current_var = tcd.Variable(
                    name=var_name,
                    type=var_type,
                    initial_value=var_initial_value,
                    comment=var_comment,
                    attributes=current_attributes if current_attributes else None,
                    section_type=section_type.lower(),
                    documentation=doc,
                )

                current_var.labels.append(var_type)
                variables.append(current_var)


            #         # Reset attributes for the next variable
            #         current_attributes = {}

            # # Add the last variable if there is one
            # if current_var:
            #     variables.append(current_var)

    # Process STRUCT sections for DUTs
    for struct_match in struct_pattern.finditer(declaration):
        struct_content = struct_match.group(1).strip()

        # Split the struct content into lines
        lines = struct_content.split("\n")



        for line in lines:

            # Process each line
            current_var = None
            current_attributes = {}

            line = line.strip()
            if not line:
                continue

            # Check for attribute
            attr_match = attribute_pattern.search(line)
            if attr_match:
                attr_name = attr_match.group(1)
                attr_value = attr_match.group(2) if attr_match.group(2) else ""
                current_attributes[attr_name] = attr_value
                continue

            # Check for variable declaration
            if ":" in line:
                # If we have a previous variable, add it to the list
                # if current_var:
                #     variables.append(current_var)
                #     current_var = None

                # Parse the new variable
                var_parts = line.split(":", 1)
                var_name = var_parts[0].strip()

                # Extract comment if present
                var_comment = None
                comment_match = comment_pattern.search(line)
                if comment_match:
                    # Get the first non-None group
                    for group in comment_match.groups():
                        if group:
                            var_comment = group.strip()
                            break

                # Remove comment from line for further processing
                if comment_match:
                    line = line[: comment_match.start()].strip()

                # Parse type and initial value
                type_value_parts = var_parts[1].strip()
                if ";" in type_value_parts:
                    type_value_parts = type_value_parts.rstrip(";")

                var_type = type_value_parts
                var_initial_value = None

                # Check for initial value
                if ":=" in type_value_parts:
                    type_init_parts = type_value_parts.split(":=", 1)
                    var_type = type_init_parts[0].strip()
                    var_initial_value = type_init_parts[1].strip()

                var_type = var_type.split(";")[0]

                doc = tcd.Documentation(details=var_comment)

                # Create the variable
                current_var = tcd.Variable(
                    name=var_name,
                    type=var_type,
                    initial_value=var_initial_value,
                    comment=var_comment,
                    attributes=current_attributes if current_attributes else None,
                    section_type="STRUCT".lower(),
                    documentation=doc,
                )
                current_var.labels.append(var_type)
                variables.append(current_var)
        #         # Reset attributes for the next variable
        #         current_attributes = {}

        # # Add the last variable if there is one
        # if current_var:
        #     variables.append(current_var)

    return variables


def load_method(method: Method):
    if method is None:
        return None

    # Extract implementation text
    implementation_text = ""
    if hasattr(method.implementation, "st"):
        implementation_text = method.implementation.st

    # Parse access modifier and return type from declaration
    accessModifier = None
    returnType = None
    variables = []
    documentation = None

    if method.declaration:
        declaration_lines = method.declaration.strip().split("\n")
        if declaration_lines:
            first_line = declaration_lines[0].strip()
            # Look for METHOD [MODIFIER] name : return_type;
            if first_line.startswith("METHOD "):
                # Check for return type after colon
                if ":" in first_line:
                    # Split by colon and get the part after it
                    return_part = first_line.split(":", 1)[1].strip()
                    # Remove trailing semicolon if present
                    if return_part.endswith(";"):
                        return_part = return_part[:-1].strip()
                    returnType = return_part

                # Check for access modifier
                parts = first_line.split(" ")
                if len(parts) >= 3:
                    # Check if the second part is an access modifier
                    possible_modifier = parts[1].upper()
                    if possible_modifier in [
                        "PROTECTED",
                        "PRIVATE",
                        "INTERNAL",
                        "PUBLIC",
                    ]:
                        accessModifier = possible_modifier

        # Parse variable sections
        variables = parse_variables(method.declaration)

        # Parse documentation
        documentation = parse_documentation(method.declaration)

    tcMeth = tcd.Method(
        name=method.name,
        accessModifier=accessModifier,
        returnType=returnType,
        declaration=method.declaration,
        implementation=implementation_text,
        documentation=documentation,
    )

    for var in variables:
        var.parent = tcMeth
        var.name_space = tcMeth.name_space

    if returnType is not None:
        tcMeth.labels.append(returnType)
    if accessModifier is not None:
        tcMeth.labels.append(accessModifier)

    tcMeth.variables = variables
    return tcMeth


def load_property(property: Property):
    if property is None:
        return None

    # Parse return type from declaration
    returnType = None
    if property.declaration:
        declaration_lines = property.declaration.strip().split("\n")
        if declaration_lines:
            first_line = declaration_lines[0].strip()
            # Look for PROPERTY name : return_type
            if first_line.startswith("PROPERTY "):
                # Check for return type after colon
                if ":" in first_line:
                    # Split by colon and get the part after it
                    return_part = first_line.split(":", 1)[1].strip()
                    returnType = return_part
        # Parse documentation
        documentation = parse_documentation(property.declaration)


    tcProp = tcd.Property(
        name=property.name,
        returnType=returnType,
        get=load_get_property(get=property.get),
        set=load_set_property(set=property.set),
        documentation=documentation,
    )

    if returnType is not None:
        tcProp.labels.append(returnType)
    if tcProp.get is not None and tcProp.set is not None:
        tcProp.labels.append("Get/Set")
    elif tcProp.get is not None:
        tcProp.labels.append("Get")
    elif tcProp.set is not None:
        tcProp.labels.append("Set")

    return tcProp


def load_get_property(get: Get):
    if get is None:
        return None

    # Extract implementation text
    implementation_text = ""
    if hasattr(get.implementation, "st"):
        implementation_text = get.implementation.st

    return tcd.Get(
        name=get.name, declaration=get.declaration, implementation=implementation_text
    )


def load_set_property(set: Set):
    if set is None:
        return None

    # Extract implementation text
    implementation_text = ""
    if hasattr(set.implementation, "st"):
        implementation_text = set.implementation.st

    return tcd.Set(
        name=set.name, declaration=set.declaration, implementation=implementation_text
    )

def parse_placeholder_reference(placeholder : PlaceholderReference) -> tcd.Dependency:

    pattern = r"^(.*?),\s*([\d\.\*]+)\s*\((.*?)\)$"
    match = re.match(pattern, placeholder.default_resolution)
    if match:
        name, version, vendor = match.groups()
        return tcd.Dependency(name=name,
                            version=version,
                            category=vendor)


class FileHandler(ABC):



    def __init__(self, suffix):
        self.suffix: str = suffix.lower()
        self.config = ParserConfig(fail_on_unknown_properties=False)
        self.parser = XmlParser(config=self.config)
        super().__init__()

    @abstractmethod
    def load_object(self, path: Path, obj_store: List[tcd.Objects], parent: tcd.Objects|None = None):
        raise NotImplementedError()



_handler: List[FileHandler] = []


def add_handler(handler: FileHandler):
    _handler.append(handler)

def get_all_handler()-> List[FileHandler]:
    return _handler

def is_handler_in_list(suffix:str)->bool:
    for handler in _handler:
        if handler.suffix.lower() == suffix.lower():
            return True
    logger.error(f"no handler found for: {suffix}")
    return False

def get_handler(suffix: str) -> FileHandler:
    for handler in _handler:
        if handler.suffix.lower() == suffix.lower():
            return handler
    raise Exception(f"Handler for suffix:  <{suffix}> not found. Registered Handlers: {', '.join(x.suffix for x in _handler)}")




class SolutionHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".sln")

    def load_object(self, path, obj_store: List[tcd.Objects], parent: tcd.Objects|None = None):
        raise NotImplementedError("SolutionFileHandler not implemented")


class TwincatProjectHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tsproj")

    def load_object(self, path, obj_store: List[tcd.Objects], parent: tcd.Objects|None = None):
        raise NotImplementedError("TwincatProjectHandler not implemented")


class XtiHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".xti")

    def load_object(self, path, obj_store: List[tcd.Objects], parent: tcd.Objects|None = None):
        raise NotImplementedError("XtiHandler not implemented")
    
class TcTtoHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tctto")

    def load_object(self, path, obj_store: List[tcd.Objects], parent: tcd.Objects|None = None):
        raise NotImplementedError("tcttoHandler not implemented")


class PlcProjectHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".plcproj")  


    def load_object(self, path, obj_store: List[tcd.Objects], parent: tcd.Objects|None = None):
        _prj: Project = self.parser.parse(path, Project)
        if _prj is None:
            return None

        # Sub Elements
        object_paths: List[Path] = []
        dependencies: List[tcd.Dependency] = []
        compile_elements: List[Compile] = []
        for object in _prj.item_group:
            for elem in object.compile:
                if not elem.exclude_from_build:
                    compile_elements.append(elem)

            # Dependencies
            for dependency in object.placeholder_reference:
                if not dependency.system_library:
                    _dep = parse_placeholder_reference(placeholder=dependency)
                    if _dep:
                        dependencies.append(_dep)

        for elem in compile_elements:
            object_paths.append((path.parent / Path(PureWindowsPath(elem.include))).resolve())


        plcproj = tcd.PlcProject(
            name=_prj.property_group.name,
            path=path.resolve(),
            default_namespace=_prj.property_group.default_namespace,
            name_space=_prj.property_group.default_namespace,
            version=_prj.property_group.project_version,
            sub_paths=object_paths,
            dependencies=dependencies
            )


        for object_path in object_paths:
            if is_handler_in_list(object_path.suffix):
                handler = get_handler(object_path.suffix)
                handler.load_object(path=object_path, obj_store=obj_store, parent=plcproj)

        obj_store.append(plcproj)


class TcPouHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tcpou")

    def load_object(self, path, obj_store: List[tcd.Objects], parent: tcd.Objects|None = None):
        _pou: Pou = self.parser.parse(path, TcPlcObject).pou
        if _pou is None:
            return None

        # Extract implementation text
        implementation_text = ""
        if hasattr(_pou.implementation, "st"):
            implementation_text = _pou.implementation.st

        properties = []
        if hasattr(_pou, "property") and _pou.property:
            properties = [load_property(property=prop) for prop in _pou.property]
        for prop in properties:
            prop.parent = _pou.name

        methods = []
        if hasattr(_pou, "method") and _pou.method:
            methods = [load_method(method=meth) for meth in _pou.method]
        for meth in methods:
            meth.parent = _pou.name

        # Parse extends and implements from declaration
        extends = None
        implements = None
        variables = []

        if _pou.declaration:
            declaration_lines = _pou.declaration.strip().split("\n")
            if declaration_lines:
                first_line = declaration_lines[0].strip()

                # Check for EXTENDS
                if " EXTENDS " in first_line:
                    # Extract the part after EXTENDS
                    extends_part = first_line.split(" EXTENDS ")[1]
                    # If there's an IMPLEMENTS part, remove it
                    if " IMPLEMENTS " in extends_part:
                        extends_part = extends_part.split(" IMPLEMENTS ")[0]
                    extends = extends_part.strip()

                # Check for IMPLEMENTS
                if " IMPLEMENTS " in first_line:
                    # Extract the part after IMPLEMENTS
                    implements_part = first_line.split(" IMPLEMENTS ")[1]
                    # Split by comma to get multiple interfaces
                    implements = [
                        interface.strip() for interface in implements_part.split(",")
                    ]

            # Parse variable sections
            variables = parse_variables(_pou.declaration)

            # Parse documentation
            documentation = parse_documentation(_pou.declaration)



        tcPou = tcd.Pou(
            name=_pou.name,
            path=path.resolve(),
            declaration=_pou.declaration,
            implementation=implementation_text,
            extends=extends,
            implements=implements,
            documentation=documentation,
        )


        if parent is not None:
            tcPou.parent = parent
            if parent.__class__ == tcd.PlcProject:
                if hasattr(parent, "name_space"):
                    tcPou.name_space = parent.name_space
                if hasattr(parent, "pous"):
                    parent.pous.append(tcPou)
        
        for var in variables:
            var.parent = tcPou
            var.name_space = tcPou.name_space
        for prop in properties:
            prop.parent = tcPou
            prop.name_space = tcPou.name_space
        for meth in methods:
            meth.parent = tcPou    
            meth.name_space = tcPou.name_space 

        tcPou.variables = variables
        tcPou.properties = properties
        tcPou.methods = methods   

        if extends is not None:
            tcPou.labels.append("Ext: "+ extends)
        if implements is not None:
            tcPou.labels.append("Impl: " + ", ".join([impl for impl in implements]))

        obj_store.append(tcPou)
        obj_store.extend(methods)
        obj_store.extend(properties)



class TcItfHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tcio")

    def load_object(self, path, obj_store: List[tcd.Objects], parent: tcd.Objects|None = None):
        _itf: Itf = self.parser.parse(path, TcPlcObject).itf
        if _itf is None:
            return None

        properties = []
        if hasattr(_itf, "property") and _itf.property:
            properties = [load_property(property = prop) for prop in _itf.property]

        methods = []
        if hasattr(_itf, "method") and _itf.method:
            methods = [load_method(method=meth) for meth in _itf.method]

        # Parse extends from declaration
        extends = None

        if _itf.declaration:
            declaration_lines = _itf.declaration.strip().split("\n")
            if declaration_lines:
                first_line = declaration_lines[0].strip()

                # Check for EXTENDS
                if " Extends " in first_line or " EXTENDS " in first_line:
                    # Extract the part after EXTENDS (case insensitive)
                    if " Extends " in first_line:
                        extends_part = first_line.split(" Extends ")[1]
                    else:
                        extends_part = first_line.split(" EXTENDS ")[1]

                    # Split by comma to get multiple interfaces
                    extends = [
                        interface.strip() for interface in extends_part.split(",")
                    ]

        tcitf = tcd.Itf(
            name=_itf.name,
            path=path.resolve(),
            extends=extends,
        )

        for prop in properties:
            prop.parent = tcitf
        for meth in methods:
            meth.parent = tcitf     

        tcitf.properties = properties
        tcitf.methods = methods

        if parent is not None:
            tcitf.parent = parent
            if parent.__class__ == tcd.PlcProject:
                if hasattr(parent, "name_space"):
                    tcitf.name_space = parent.name_space
                if hasattr(parent, "itfs"):
                    parent.itfs.append(tcitf)

        if extends is not None:
            tcitf.labels.append("Ext: " + ", ".join([ext for ext in extends]))


        obj_store.append(tcitf)
        obj_store.extend(methods)
        obj_store.extend(properties)



class TcDutHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tcdut")

    def load_object(self, path, obj_store: List[tcd.Objects], parent: tcd.Objects|None = None):
        _dut: Dut = self.parser.parse(path, TcPlcObject).dut
        if _dut is None:
            return None

        variables = []
        documentation = None
        if _dut.declaration:
            # Parse variable sections
            variables = parse_variables(_dut.declaration)

            # Parse documentation
            documentation = parse_documentation(_dut.declaration)

        dut = tcd.Dut(
            name=_dut.name,
            path=path.resolve(),
            declaration=_dut.declaration,
            documentation=documentation,
        )

        for var in variables:
            var.parent = dut
            var.name_space = dut.name_space

        if parent is not None:
            dut.parent = parent
            if parent.__class__ == tcd.PlcProject:
                if hasattr(parent, "name_space"):
                    dut.name_space = parent.name_space
                if hasattr(parent, "duts"):
                    parent.duts.append(dut)

        dut.variables = variables

        obj_store.append(dut)



class TcGvlHandler(FileHandler):
    def __init__(self):
        super().__init__(suffix=".tcgvl")

    def load_object(self, path, obj_store: List[tcd.Objects], parent: tcd.Objects|None = None):
        _gvl: Gvl = self.parser.parse(path, TcPlcObject).gvl
        if _gvl is None:
            return None

        variables = []
        documentation = None
        if _gvl.declaration:
            # Parse variable sections
            variables = parse_variables(_gvl.declaration)

            # Parse documentation
            documentation = parse_documentation(_gvl.declaration)

        gvl:tcd.Gvl = tcd.Gvl(
            name=_gvl.name,
            path=path.resolve(),
            declaration=_gvl.declaration,
            documentation=documentation,
        )
    
        for var in variables:
            var.parent = gvl
            var.name_space = gvl.name_space

        if parent is not None:
            gvl.parent = parent
            if parent.__class__ == tcd.PlcProject:
                if hasattr(parent, "name_space"):
                    gvl.name_space = parent.name_space
                if hasattr(parent, "gvls"):
                    parent.gvls.append(gvl)

        gvl.variables = variables

        obj_store.append(gvl)



#add_handler(handler=SolutionHandler())
#add_handler(handler=TwincatProjectHandler())
#add_handler(handler=XtiHandler())
add_handler(handler=PlcProjectHandler())
add_handler(handler=TcPouHandler())
add_handler(handler=TcItfHandler())
add_handler(handler=TcDutHandler())
add_handler(handler=TcGvlHandler())
#add_handler(handler=TcTtoHandler())


class Twincat4024Strategy(BaseStrategy):



    def check_strategy(self, path: Path):
        for handler in _handler:
            if path.suffix == handler.suffix:
                return True
            


    def load_objects(self, path: Path) -> List[tcd.Objects]:
        _path = PurePath(path)
        _obj: List[tcd.Objects] = []
        if is_handler_in_list(suffix=_path.suffix):
            handler = get_handler(suffix=_path.suffix)
            handler.load_object(path,obj_store=_obj)
            return _obj
        else:
            return []






# present the strategy to the loader
add_strategy(Twincat4024Strategy)

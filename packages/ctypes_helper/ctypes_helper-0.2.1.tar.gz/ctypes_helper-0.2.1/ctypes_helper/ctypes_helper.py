from ctypes import *
from enum import Flag, auto

ctype_shorter_map = {
    "wchar": "int32_t",
    "char": "int8_t",
    "signed char": "int8_t",
    "unsigned char": "uint8_t",
    "short": "int16_t",
    "signed short": "int16_t",
    "unsigned short": "uint16_t",
    "int": "int32_t",
    "signed int": "int32_t",
    "unsigned int": "uint32_t",
    "long": "int64_t",
    "signed long": "int64_t",
    "unsigned long": "uint64_t",
    "long int": "int64_t",
    "signed long int": "int64_t",
    "unsigned long int": "uint64_t",
    "long long": "int64_t",
    "signed long long": "int64_t",
    "unsigned long long": "uint64_t",
    "long long int": "int64_t",
    "signed long long int": "int64_t",
    "unsigned long long int": "int64_t",
    # "int8_t": "",
    # "uint8_t": "",
    # "int16_t": "",
    # "uint16_t: "",
    # "int32_t": "",
    # "uint32_t": "",
    # "int64_t": "",
    # "uint64_t:: "",
    "__int64": "int64_t",
    "signed __int64": "int64_t",
    "unsigned __int64": "uint64_t",
    "float32_t": "float",
    "float64_t": "double",
    "float128_t": "long double",
    # "bool": "",
    "signed": "int32_t",
    "unsigned": "uint32_t",
    # "float": "",
    # "double": "",
    # "long double": "",
    "size_t": "uint32_t",
    "void": "pointer",
    "uintptr_t": "pointer",
    "char_ptr": "pointer",
    "wchar_ptr": "pointer",
}


ctype_fmt_prec = {
    "float": r"%.6f",
    "double": r"%.8f",
    "uintptr_t": r"%ld",
    "pointer": r"%ld",
    "int64_t": r"%lld",
    "uint64_t": r"%lld",
    "bool": r"%d",
}


class CTypeTag(Flag):
    NONE = 0

    BIT8 = 8
    BIT16 = 16
    BIT32 = 32
    BIT64 = 64
    BIT128 = 128

    SIGNED = auto()
    UNSIGNED = auto()

    INT = auto()
    FLOAT = auto()
    POINTER = auto()

    BITS = BIT8 | BIT16 | BIT32 | BIT64 | BIT128
    SIGN = SIGNED | UNSIGNED
    CATEGORY = INT | FLOAT | POINTER


class CTypeDescriptor:
    def __init__(self, name, sign, category, bits, ctype):
        self.name: str = name  # type name
        self.sign: str = sign  # signed | unsigned
        self.category: str = category  # int | float
        self.bits: int = bits  # bit
        self.ctype = ctype  # ctype
        self.tag = CTypeTag.NONE
        self.short: str = ctype_shorter_map.get(name, name)
        self.fmt: str = ctype_fmt_prec.get(self.short, r"%d")

        if self.sign == "signed":
            self.tag |= CTypeTag.SIGNED
        elif self.sign == "unsigned":
            self.tag |= CTypeTag.UNSIGNED

        if self.category == "int":
            self.tag |= CTypeTag.INT
        elif self.category == "float":
            self.tag |= CTypeTag.FLOAT
        elif self.category == "pointer":
            self.tag |= CTypeTag.POINTER

        if self.bits == 8:
            self.tag |= CTypeTag.BIT8
        elif self.bits == 16:
            self.tag |= CTypeTag.BIT16
        elif self.bits == 32:
            self.tag |= CTypeTag.BIT32
        elif self.bits == 64:
            self.tag |= CTypeTag.BIT64
        elif self.bits == 128:
            self.tag |= CTypeTag.BIT128

        max_min_value = self._calc_min_max() if name != "bool" else (0, 1)
        self.min: int | float | None = max_min_value[0]  # min value
        self.max: int | float | None = max_min_value[1]  # max value

    def __str__(self) -> str:
        return (
            f"({self.name}) sign: {self.sign}, category: {self.category}, bits: {self.bits}"
            f", range: [{self.min}, {self.max}], short: {self.short}, fmt: {self.fmt}, ctype: {self.ctype}"
        )

    def _calc_min_max(self) -> tuple[int | float | None, int | float | None]:
        if self.category == "int":
            if self.sign == "signed":
                min_value = -(2 ** (self.bits - 1))
                max_value = 2 ** (self.bits - 1) - 1
            else:  # unsigned
                min_value = 0
                max_value = 2**self.bits - 1
        elif self.category == "float":
            if self.bits == 32:
                min_value = -3.4e38
                max_value = 3.4e38
            elif self.bits == 64:
                min_value = -1.7e308
                max_value = 1.7e308
            elif self.bits == 128:
                min_value = -1.1e4932
                max_value = 1.1e4932
        else:
            return None, None

        return min_value, max_value

    def clip(self, value) -> int | float | None:
        if self.min is None:
            return None
        value = int(value) if self.category == "int" else float(value)
        return max(self.min, min(value, self.max))

    def to_value(self, value: str | int | float, clip: bool = False) -> int | float:
        try:
            if isinstance(value, str):
                converted_value = int(value) if self.category == "int" else float(value)
        except ValueError as e:
            return f"Error converting {value} to {self.name}: {e}"
        if clip:
            converted_value = max(self.min, min(converted_value, self.max))
        return converted_value


class CTypeRegistry:
    def __init__(self) -> None:
        self.types: dict[str, CTypeDescriptor] = {}
        self._init_builtin_types()
        self._init_ctype_name_map()

    def _init_builtin_types(self) -> None:
        self.types["wchar"] = CTypeDescriptor("wchar", "signed", "int", 32, c_wchar)

        self.types["char"] = CTypeDescriptor("char", "signed", "int", 8, c_char)  # int8_t
        self.types["signed char"] = CTypeDescriptor("signed char", "signed", "int", 8, c_char)  # int8_t
        self.types["unsigned char"] = CTypeDescriptor("unsigned char", "unsigned", "int", 8, c_ubyte)  # uint8_t

        self.types["short"] = CTypeDescriptor("short", "signed", "int", 16, c_short)  # int16_t
        self.types["signed short"] = CTypeDescriptor("signed short", "signed", "int", 16, c_short)  # int16_t
        self.types["unsigned short"] = CTypeDescriptor("unsigned short", "unsigned", "int", 16, c_ushort)  # uint16_t

        self.types["int"] = CTypeDescriptor("int", "signed", "int", 32, c_int)  # int32_t
        self.types["signed int"] = CTypeDescriptor("signed int", "signed", "int", 32, c_int)  # int32_t
        self.types["unsigned int"] = CTypeDescriptor("unsigned int", "unsigned", "int", 32, c_uint)  # uint32_t

        self.types["long"] = CTypeDescriptor("long", "signed", "int", 64, c_long)  # int64_t
        self.types["signed long"] = CTypeDescriptor("signed long", "signed", "int", 64, c_long)  # int64_t
        self.types["unsigned long"] = CTypeDescriptor("unsigned long", "unsigned", "int", 64, c_ulong)  # uint64_t

        self.types["long int"] = CTypeDescriptor("long int", "signed", "int", 64, c_long)
        self.types["signed long int"] = CTypeDescriptor("signed long int", "signed", "int", 64, c_long)
        self.types["unsigned long int"] = CTypeDescriptor("unsigned long int", "unsigned", "int", 64, c_ulong)

        self.types["long long"] = CTypeDescriptor("long long", "signed", "int", 64, c_long)
        self.types["signed long long"] = CTypeDescriptor("signed long long", "signed", "int", 64, c_long)
        self.types["unsigned long long"] = CTypeDescriptor("unsigned long long", "unsigned", "int", 64, c_ulong)

        self.types["long long int"] = CTypeDescriptor("long long int", "signed", "int", 64, c_long)
        self.types["signed long long int"] = CTypeDescriptor("signed long long int", "signed", "int", 64, c_long)
        self.types["unsigned long long int"] = CTypeDescriptor("unsigned long long int", "unsigned", "int", 64, c_ulong)

        self.types["int8_t"] = CTypeDescriptor("int8_t", "signed", "int", 8, c_char)
        self.types["uint8_t"] = CTypeDescriptor("uint8_t", "unsigned", "int", 8, c_ubyte)
        self.types["int16_t"] = CTypeDescriptor("int16_t", "signed", "int", 16, c_short)
        self.types["uint16_t"] = CTypeDescriptor("uint16_t", "unsigned", "int", 16, c_ushort)
        self.types["int32_t"] = CTypeDescriptor("int32_t", "signed", "int", 32, c_int)
        self.types["uint32_t"] = CTypeDescriptor("uint32_t", "unsigned", "int", 32, c_uint)
        self.types["int64_t"] = CTypeDescriptor("int64_t", "signed", "int", 64, c_long)
        self.types["uint64_t"] = CTypeDescriptor("uint64_t", "unsigned", "int", 64, c_ulong)
        self.types["__int64"] = CTypeDescriptor("__int64", "signed", "int", 64, c_long)
        self.types["signed __int64"] = CTypeDescriptor("signed __int64", "signed", "int", 64, c_long)
        self.types["unsigned __int64"] = CTypeDescriptor("unsigned __int64", "unsigned", "int", 64, c_ulong)

        self.types["float32_t"] = CTypeDescriptor("float32_t", "signed", "float", 32, c_float)
        self.types["float64_t"] = CTypeDescriptor("float64_t", "signed", "float", 64, c_double)
        self.types["float128_t"] = CTypeDescriptor("float128_t", "signed", "float", 128, c_longdouble)

        self.types["bool"] = CTypeDescriptor("bool", "signed", "int", 8, c_bool)

        self.types["signed"] = CTypeDescriptor("signed", "signed", "int", 32, c_int)  # int32_t
        self.types["unsigned"] = CTypeDescriptor("unsigned", "unsigned", "int", 32, c_uint)  # uint32_t

        self.types["float"] = CTypeDescriptor("float", "signed", "float", 32, c_float)
        self.types["double"] = CTypeDescriptor("double", "signed", "float", 64, c_double)
        self.types["long double"] = CTypeDescriptor("long double", "signed", "float", 128, c_longdouble)

        self.types["size_t"] = CTypeDescriptor("size_t", "unsigned", "int", 32, c_size_t)  # 32-bit platform

        self.types["void"] = CTypeDescriptor("void", "unsigned", "pointer", 32, c_void_p)  # 32-bit platform
        self.types["uintptr_t"] = CTypeDescriptor("uintptr_t", "unsigned", "pointer", 32, c_void_p)  # 32-bit platform
        # self.types["char_ptr"] = CTypeDescriptor("char_ptr", "unsigned", "pointer", 32, c_char_p)  # 32-bit platform
        # self.types["wchar_ptr"] = CTypeDescriptor("wchar_ptr", "unsigned", "pointer", 32, c_wchar_p)  # 32-bit platform

    def _init_ctype_name_map(self):
        self.map: dict = {k: v.ctype.__name__ for k, v in self.types.items()}

    def get(self, type_str: str) -> CTypeDescriptor | None:
        return self.types.get(type_str, CTypeDescriptor("unknown", None, None, None, None))

    def to_ctypes_name(self, type_str: str, _default: str = None) -> str:
        return self.map.get(type_str, _default)


ctyp = CTypeRegistry()

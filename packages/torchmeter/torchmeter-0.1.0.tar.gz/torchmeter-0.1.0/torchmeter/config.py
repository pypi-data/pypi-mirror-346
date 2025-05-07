from __future__ import annotations

import os
import warnings
from enum import Enum, unique
from types import SimpleNamespace
from typing import TYPE_CHECKING
from threading import Lock

import yaml
from rich import box

from torchmeter.utils import indent_str

if TYPE_CHECKING:
    import sys

    if sys.version_info >= (3, 10):
        from typing import TypeAlias
    else:
        from typing_extensions import TypeAlias

    from typing import Any, Dict, List, Union, Callable, Optional, Sequence

    CFG_CONTENT_TYPE: TypeAlias = Union[
        int, float, str, bool, Sequence["CFG_CONTENT_TYPE"], Dict[str, "CFG_CONTENT_TYPE"], None
    ]

__all__ = ["get_config", "Config"]

DEFAULT_FIELDS = [
    "render_interval",
    "tree_fold_repeat",
    "tree_repeat_block_args",
    "tree_levels_args",
    "table_column_args",
    "table_display_args",
    "combine",
]

DEFAULT_CFG = """\
render_interval: 0.15

tree_fold_repeat: True

tree_repeat_block_args:
    title: '[i]Repeat [[b]<repeat_time>[/b]] Times[/]'
    title_align: center
    subtitle: null
    subtitle_align: center
    
    style: dark_goldenrod
    highlight: True
    
    box: HEAVY_EDGE
    border_style: dim
    
    width: null
    height: null
    padding: 
        - 0
        - 1
    expand: False
        
tree_levels_args:
    default:
        label: '[b gray35](<node_id>) [green]<name>[/green] [cyan]<type>[/]'
        
        style: tree
        guide_style: light_coral
        highlight: True
        
        hide_root: False
        expanded: True
      
    '0': 
        label: '[b light_coral]<name>[/]'
        guide_style: light_coral
          
table_column_args:
    style: none
    
    justify: center
    vertical: middle
    
    overflow: fold
    no_wrap: False
        
table_display_args:
    style: spring_green4
    highlight: True
    
    width: null
    min_width: null
    expand: False
    padding: 
        - 0
        - 1
    collapse_padding: False
    pad_edge: True
    leading: 0
    
    title: null
    title_style: bold
    title_justify: center
    
    caption: null
    caption_style: null
    caption_justify: center
    
    show_header: True
    header_style: bold
    
    show_footer: False
    footer_style: italic
    
    show_lines: False
    row_styles: null
    
    show_edge: True
    box: ROUNDED
    safe_box: True
    border_style: null

combine:
    horizon_gap: 2
"""


@unique
class BOX(Enum):
    ASCII = box.ASCII
    ASCII2 = box.ASCII2
    ASCII_DOUBLE_HEAD = box.ASCII_DOUBLE_HEAD
    DOUBLE = box.DOUBLE
    DOUBLE_EDGE = box.DOUBLE_EDGE
    HEAVY = box.HEAVY
    HEAVY_EDGE = box.HEAVY_EDGE
    HEAVY_HEAD = box.HEAVY_HEAD
    HORIZONTALS = box.HORIZONTALS
    MARKDOWN = box.MARKDOWN
    MINIMAL = box.MINIMAL
    MINIMAL_DOUBLE_HEAD = box.MINIMAL_DOUBLE_HEAD
    MINIMAL_HEAVY_HEAD = box.MINIMAL_HEAVY_HEAD
    ROUNDED = box.ROUNDED
    SIMPLE = box.SIMPLE
    SIMPLE_HEAD = box.SIMPLE_HEAD
    SIMPLE_HEAVY = box.SIMPLE_HEAVY
    SQUARE = box.SQUARE
    SQUARE_DOUBLE_HEAD = box.SQUARE_DOUBLE_HEAD


# all the keys should be str, while all the value should be enum
# int each value, all the member's name should not be the same with its value's repr
UNSAFE_KV = {"box": BOX}


def list_to_callbacklist(ls: List[Any], callback_func: Callable[[], Any] = lambda: None) -> CallbackList:
    _list: List[Any] = []
    for item in ls:
        if isinstance(item, dict):
            _list.append(dict_to_namespace(item))
        elif isinstance(item, list):
            _list.append(list_to_callbacklist(item, callback_func=callback_func))
        else:
            _list.append(item)
    return CallbackList(_list, callback_func=callback_func)


def dict_to_namespace(d: Dict[str, Any]) -> FlagNameSpace:
    """
    Recursively converts a dictionary to a FlagNameSpace object.
    """  # noqa: DOC201, DOC501
    if not isinstance(d, dict):
        raise TypeError(f"Input must be a dictionary, but got `{type(d).__name__}`")

    ns = FlagNameSpace()

    for k, v in d.items():
        # overwrite the value of unsafe key to get the unrepresent value
        if k in UNSAFE_KV and isinstance(v, str):
            v = getattr(UNSAFE_KV[k], v).value

        if isinstance(v, dict):
            setattr(ns, k, dict_to_namespace(v))

        elif isinstance(v, list):
            setattr(ns, k, list_to_callbacklist(v, callback_func=ns.mark_change))

        elif isinstance(v, set):
            setattr(ns, k, CallbackSet(v, callback_func=ns.mark_change))

        else:
            if not isinstance(k, str):
                raise TypeError(f"Attribute name must be a string, but got `{type(k).__name__}`")

            setattr(ns, k, v)

    return ns


def namespace_to_dict(ns: FlagNameSpace, safe_resolve: bool = False) -> Dict[str, CFG_CONTENT_TYPE]:
    """
    Recursively converts a FlagNameSpace object to a dictionary.
    """  # noqa: DOC201, DOC501
    if not isinstance(ns, FlagNameSpace):
        raise TypeError(f"Input must be an instance of FlagNameSpace, but got `{type(ns).__name__}`")

    d: Dict[str, CFG_CONTENT_TYPE] = {}
    for k, v in ns.data_dict.items():
        # transform the unrepresent value to its name defined in corresponding Enum
        if k in UNSAFE_KV and safe_resolve:
            v = UNSAFE_KV[k](v).name

        if isinstance(v, FlagNameSpace):
            d[k] = namespace_to_dict(v, safe_resolve=safe_resolve)

        elif isinstance(v, list):
            _list: List[CFG_CONTENT_TYPE] = []
            for item in v:
                if isinstance(item, FlagNameSpace):
                    _list.append(namespace_to_dict(item, safe_resolve=safe_resolve))
                else:
                    _list.append(item)
            d[k] = _list

        else:
            d[k] = v

    return d


def get_config(config_path: Optional[str] = None) -> Config:
    cfg_path = os.environ.get("TORCHMETER_CONFIG", config_path)
    cfg = Config(config_path=cfg_path)  # always exist an instance cause display.py and core.py depend on it
    return cfg


class CallbackList(list):
    def __init__(self, *args, callback_func: Callable = lambda: None, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._callback_func = callback_func
        self._register_callback(
            "append",
            "extend",
            "insert",
            "pop",
            "remove",
            "clear",
            "reverse",
            "sort",
            "__setitem__",
            "__delitem__",
            "__iadd__",
            "__imul__",
        )

    def _register_callback(self, *methods) -> None:
        for method_name in methods:
            orig_method = getattr(self.__class__, method_name)

            def wrapped_method(*args, _method: Callable = orig_method, **kwargs) -> Any:
                result = _method(*args, **kwargs)
                self._callback_func()
                return result

            setattr(self.__class__, method_name, wrapped_method)


class CallbackSet(set):
    def __init__(self, *args, callback_func: Callable = lambda: None, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._callback_func = callback_func
        self._register_callback(
            "add",
            "update",
            "difference_update",
            "intersection_update",
            "symmetric_difference_update",
            "discard",
            "pop",
            "remove",
            "clear",
            "__isub__",
            "__iand__",
            "__ixor__",
            "__ior__",
        )

    def _register_callback(self, *methods) -> None:
        for method_name in methods:
            orig_method = getattr(self.__class__, method_name)

            def wrapped_method(*args, _method: Callable = orig_method, **kwargs) -> Any:
                result = _method(*args, **kwargs)
                self._callback_func()
                return result

            setattr(self.__class__, method_name, wrapped_method)


class FlagNameSpace(SimpleNamespace):
    __flag_key = "__FLAG"

    def __init__(self, **kwargs) -> None:
        list(map(lambda x: setattr(self, x, kwargs[x]), kwargs))
        self.mark_unchange()

    def __setattr__(self, key: str, value: Any) -> None:
        if key in ("__flag_key", self.__flag_key):
            raise AttributeError(
                f"`{key}` is preserved for internal use, " + "you should never try to set it to a new value."
            )

        if isinstance(value, dict):
            value = dict_to_namespace(value)
        elif isinstance(value, list):
            value = list_to_callbacklist(value, callback_func=self.mark_change)
        elif isinstance(value, set):
            value = CallbackSet(value, callback_func=self.mark_change)

        super().__setattr__(key, value)

        self.mark_change()

    def __delattr__(self, key: str) -> None:
        if key in ("__flag_key", self.__flag_key):
            raise AttributeError(f"`{key}` is preserved for internal use, " + "you should never try to delete it.")

        super().__delattr__(key)

        self.mark_change()

    @property
    def data_dict(self) -> Dict[str, Any]:
        full_dict = self.__dict__.copy()
        del full_dict[self.__flag_key]
        return full_dict

    def update(self, other: Union[dict, FlagNameSpace], *, replace: bool = False) -> None:
        """`other` should keep a same hierarchy structure with `self`"""  # noqa: DOC501

        if not isinstance(other, (dict, FlagNameSpace)):
            raise TypeError(
                f"Instance of `{self.__class__.__name__}` can only be updated with a dict or "
                + f"another instance of `{self.__class__.__name__}`, but got `{type(other).__name__}`."
            )

        if isinstance(other, dict):
            other = dict_to_namespace(other)

        if replace:
            replace_data = other.data_dict
            self.__dict__.update(replace_data)

            del_keys = set(self.data_dict.keys()) - set(replace_data.keys())
            list(map(lambda k: delattr(self, k), del_keys))

            self.mark_change()
            return

        for k, v in other.data_dict.items():
            if k not in self.__dict__:
                if isinstance(v, dict):
                    v = dict_to_namespace(v)
                setattr(self, k, v)
                continue

            # if the value is a dict or a FlagNameSpace,
            # update the orgin namespace (origin must be a FlagNameSpace)
            origin_val_type = type(self.__dict__[k]).__name__
            new_val_type = type(v).__name__
            if origin_val_type == "FlagNameSpace":
                if new_val_type not in ["dict", "FlagNameSpace"]:
                    raise RuntimeError(
                        f"Operation aborted: the origin value of `{k}` is of type "
                        + "`FlagNameSpace` which has a inner structure, "
                        + f"set to `{new_val_type}` will destroy it."
                    )
                else:
                    self.__dict__[k].update(v)
            else:
                setattr(self, k, v)

    def is_change(self) -> bool:
        res = getattr(self, self.__flag_key) or any(
            args.is_change() for args in self.__dict__.values() if isinstance(args, self.__class__)
        )
        self.__dict__[self.__flag_key] = res
        return res

    def mark_change(self) -> None:
        self.__dict__[self.__flag_key] = True

    def mark_unchange(self) -> None:
        self.__dict__[self.__flag_key] = False
        list(map(lambda x: x.mark_unchange() if isinstance(x, self.__class__) else None, self.__dict__.values()))


class ConfigMeta(type):
    """To achieve sigleton pattern"""

    __instances = None
    __thread_lock = Lock()

    def __call__(cls, config_path: Optional[str] = None) -> Config:
        with cls.__thread_lock:
            if cls.__instances is None:
                instance = super().__call__(config_path)
                cls.__instances = instance
            else:
                if cls.__instances.config_file != config_path:
                    cls.__instances.config_file = config_path
        return cls.__instances


class Config(metaclass=ConfigMeta):
    """You can only read or write the predefined fields in the instance"""

    render_interval: float
    tree_fold_repeat: bool
    tree_repeat_block_args: FlagNameSpace
    tree_levels_args: FlagNameSpace
    table_column_args: FlagNameSpace
    table_display_args: FlagNameSpace
    combine: FlagNameSpace

    __slots__ = [*DEFAULT_FIELDS, "__cfg_file"]

    def __init__(self, config_path: Optional[str] = None) -> None:
        """Load default settings by default"""
        # init __cfg_file
        self.__cfg_file = None

        # set __cfg_file, load config file and check its integrity
        self.config_file = config_path

    @property
    def config_file(self) -> Optional[str]:
        return self.__cfg_file

    @config_file.setter
    def config_file(self, file_path: Optional[str] = None) -> None:
        if file_path is not None and not isinstance(file_path, str):
            raise TypeError(
                "You must pass in a string or None to change config or use the default config, "
                + f"but got `{type(file_path).__name__}`."
            )

        if file_path:
            file_path = os.path.abspath(file_path)
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"Config file {file_path} does not exist.")
            if not file_path.endswith(".yaml"):
                raise ValueError(f"Config file must be a yaml file, but got `{file_path}`")

        self.__cfg_file = file_path
        self.__load()
        self.check_integrity()

    def __load(self) -> None:
        if self.config_file is None:
            raw_data = yaml.safe_load(DEFAULT_CFG)
        else:
            with open(self.config_file, "r") as f:
                raw_data = yaml.safe_load(f)

        ns: FlagNameSpace = dict_to_namespace(raw_data)
        for k, v in ns.data_dict.items():
            is_reload = hasattr(self, k)

            if is_reload and isinstance(v, FlagNameSpace):
                getattr(self, k).update(v, replace=True)
            else:
                setattr(self, k, v)

    def restore(self) -> None:
        self.__load()
        self.check_integrity()

    def check_integrity(self) -> None:
        # no need to check integrity when loading default settings
        if self.config_file is None:
            return None

        with open(self.config_file, "r") as f:
            custom_cfg = yaml.safe_load(f)

        for field in DEFAULT_FIELDS:
            if field not in custom_cfg:
                warnings.warn(
                    category=UserWarning,
                    message=f"Config file {self.config_file} does not contain '{field}' field, "
                    + "using default settings instead.",
                )

    def asdict(self, safe_resolve: bool = False) -> Dict[str, CFG_CONTENT_TYPE]:
        d: Dict[str, CFG_CONTENT_TYPE] = {}

        for field in DEFAULT_FIELDS:
            field_val = getattr(self, field)

            if isinstance(field_val, FlagNameSpace):
                d[field] = namespace_to_dict(field_val, safe_resolve=safe_resolve)

            elif isinstance(field_val, list):
                d[field] = [
                    namespace_to_dict(v, safe_resolve=safe_resolve) if isinstance(v, FlagNameSpace) else v
                    for v in field_val
                ]

            elif isinstance(field_val, dict):
                d[field] = {
                    k: namespace_to_dict(v, safe_resolve=safe_resolve) if isinstance(v, FlagNameSpace) else v
                    for k, v in field_val.items()
                }

            else:
                d[field] = field_val

        return d

    def dump(self, save_path: str) -> None:
        d = self.asdict(safe_resolve=True)

        with open(save_path, "w") as f:
            yaml.safe_dump(d, f, indent=2, sort_keys=False, encoding="utf-8", allow_unicode=True)

    def __setattr__(self, name: str, value: Any) -> None:
        # the attribute is already exist
        try:
            origin_val = getattr(self, name)
            # to avoid break the format
            if isinstance(origin_val, (dict, FlagNameSpace)):
                origin_val.update(value)
            else:
                super().__setattr__(name, value)

        # the first time to set the attribute
        except AttributeError:
            super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        # every attribute of Config object is important and should be there
        raise RuntimeError("You cannot delete attributes from Config object.")

    def __repr__(self) -> str:
        d = self.asdict(safe_resolve=True)

        def simple_data_repr(val: Any) -> str:
            val_repr = []

            if isinstance(val, dict):
                val_repr.append("namespace{")
                val_repr.extend([f"{k} = {simple_data_repr(v)}" for k, v in val.items()])
                # val_repr[-1] += "}"
                val_repr.append("}")

            elif isinstance(val, (tuple, list, set)):
                val_repr.append(f"{type(val).__name__}(")
                val_repr.extend([f"- {simple_data_repr(v)}" for v in val])
                # val_repr[-1] += ")"
                val_repr.append(")")

            else:
                return f"{val} | <{type(val).__name__}>"

            return indent_str(val_repr, indent=4, process_first=False)

        s = "• Config file: " + (self.config_file if self.config_file else "None(default setting below)") + "\n" * 2
        for field_name, field_vals in d.items():
            s += f"• {field_name}: " + simple_data_repr(field_vals) + "\n" * 2
        return s


if __name__ == "__main__":
    default_cfg = Config()
    print(default_cfg)
    cfg1 = Config()
    cfg2 = Config()
    if id(cfg1) == id(cfg2):
        print("Singleton Pattern Success.")

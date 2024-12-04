import json
from json.decoder import JSONDecodeError as PyJSONDecodeError
from json.decoder import JSONDecoder, py_scanstring
from json.scanner import py_make_scanner
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union

from httpcore import stream
from pydantic import BaseModel


class FixResult(NamedTuple):
    success: bool
    line: str
    origin: bool


class JSONDecodeError:
    def __init__(self, parser, message):
        self.message = message
        self.parser = parser

    def __eq__(self, err):
        return err.parser == self.parser and self.message in err.message


class errors:
    StringInvalidUXXXXEscape = JSONDecodeError(
        "py_scanstring", "Invalid \\uXXXX escape"
    )
    # 2 different case
    StringUnterminatedString = JSONDecodeError(
        "py_scanstring", "Unterminated string starting at"
    )
    StringInvalidControlCharacter = JSONDecodeError(
        "py_scanstring", "Invalid control character"
    )
    StringInvalidEscape = JSONDecodeError("py_scanstring", "Invalid \\escape")
    ObjectExceptColon = JSONDecodeError("JSONObject", "Expecting ':' delimiter")
    ObjectExceptObject = JSONDecodeError("JSONObject", "Expecting value")
    # 2 different case
    ObjectExceptKey = JSONDecodeError(
        "JSONObject", "Expecting property name enclosed in double quotes"
    )
    ObjectExceptComma = JSONDecodeError("JSONObject", "Expecting ',' delimiter")
    ArrayExceptObject = JSONDecodeError("JSONArray", "Expecting value")
    ArrayExceptComma = JSONDecodeError("JSONArray", "Expecting ',' delimiter")

    @classmethod
    def get_decode_error(cls, parser, message):
        err = JSONDecodeError(parser, message)
        for _, value in cls.__dict__.items():
            if isinstance(value, JSONDecodeError):
                if err == value:
                    return value
        return None


def errmsg_inv(e: ValueError) -> Dict[str, Any]:
    assert isinstance(e, PyJSONDecodeError)
    parser = e.__dict__.get("parser", "")
    errmsg = e.msg
    localerr = errors.get_decode_error(parser, errmsg)
    return {
        "parsers": e.__dict__.get("parsers", []),
        "error": localerr,
        "lineno": e.lineno,
        "colno": e.colno,
        "pos": e.pos,
    }


def record_parser_name(parser: Any) -> Any:
    def new_parser(*args: Any, **kwargs: Any) -> Any:
        try:
            return parser(*args, **kwargs)
        except Exception as e:
            if "parser" not in e.__dict__:
                e.__dict__["parser"] = parser.__name__
            if "parsers" not in e.__dict__:
                e.__dict__["parsers"] = []
            e.__dict__["parsers"].append(parser.__name__)
            raise e

    return new_parser


def make_decoder(*, strict: bool = True) -> JSONDecoder:
    json.decoder.scanstring = record_parser_name(py_scanstring)

    decoder = JSONDecoder(strict=strict)
    decoder.parse_object = record_parser_name(decoder.parse_object)
    decoder.parse_array = record_parser_name(decoder.parse_array)
    decoder.parse_string = record_parser_name(py_scanstring)
    decoder.parse_object = record_parser_name(decoder.parse_object)

    decoder.scan_once = py_make_scanner(decoder)
    return decoder


class DecodeResult(NamedTuple):
    success: bool
    exception: Optional[Exception]
    err_info: Optional[Union[Dict[str, Any], Tuple[Any, Any]]]


decoder = make_decoder()
decoder_unstrict = make_decoder(strict=False)


def decode_line(line: str, *, strict: bool = True) -> DecodeResult:
    try:
        obj, end = (decoder if strict else decoder_unstrict).scan_once(line, 0)
        ok = end == len(line)
        return DecodeResult(success=ok, exception=None, err_info=(obj, end))
    except StopIteration as e:
        return DecodeResult(success=False, exception=e, err_info=None)
    except ValueError as e:
        err_info = errmsg_inv(e)
        return DecodeResult(success=False, exception=e, err_info=err_info)


# TODO better name
def patch_lastest_left_object_and_array(line: str) -> str:
    # '}]{[' --> '[{}]{['
    pairs = {"}": "{", "]": "["}
    breaks = "{["
    left = ""
    for char in line:
        if char in breaks:
            break
        if char in pairs:
            left = pairs[char] + left

    return left


# TODO better name
# TODO change to latest
# TODO {}}]]]] --> { not [
def patch_guess_left(line: str) -> str:
    miss_object = line.count("}") - line.count("{")
    miss_array = line.count("]") - line.count("[")
    if miss_object == miss_array == 0:
        if line[-1:] == '"' and line.count('"') == 1:
            return '"'
    elif miss_object >= miss_array:
        return "{"
    else:
        return "["
    return ""


def insert_line(line: str, value: str, pos: int) -> str:
    return line[:pos] + value + line[pos:]


def remove_line(line: str, start: int, end: int) -> str:
    return line[:start] + line[end:]


class JSONFixer:
    def __init__(
        self, max_try: int = 20, max_stack: int = 3, *, js_style: bool = False
    ) -> None:
        self._max_try = max_try
        self._max_stack = max_stack
        self._js_style = js_style
        self.last_fix: Optional[bool] = None
        self.fix_stack: List[str] = []

    def fix(self, line: str, *, strict: bool = True):
        try:
            json.loads(line, strict=strict)
            return FixResult(success=True, line=line, origin=True)
        except Exception:
            pass

        ok, new_line = self.fixwithtry(line, strict=strict)
        return FixResult(success=ok, line=new_line, origin=False)

    def fixwithtry(self, line: str, *, strict: bool = True) -> Tuple[bool, str]:
        if self._max_try <= 0:
            return False, line

        self.fix_stack = []
        self.last_fix = None

        ok = False
        for _ in range(self._max_try):
            ok, new_line = self.patch_line(line, strict=strict)
            if ok:
                return ok, new_line

            self.last_fix = line != new_line
            if self.last_fix:
                self.fix_stack.insert(0, new_line)
                self.fix_stack = self.fix_stack[: self._max_stack]

            line = new_line
        return ok, line

    def patch_line(self, line: str, *, strict: bool = True) -> Tuple[bool, str]:
        result = decode_line(line, strict=strict)
        if result.success:
            return True, line

        if isinstance(result.exception, ValueError):
            return self.patch_value_error(line, result.err_info)

        if isinstance(result.exception, StopIteration):
            return self.patch_stop_iteration(line)

        if result.exception is None:
            return self.patch_half_parse(line, result.err_info)

        return False, line

    def patch_value_error(self, line: str, err_info: Any) -> Tuple[bool, str]:
        if err_info["error"] is None:
            return False, line

        error = err_info["error"]
        pos = err_info["pos"]
        nextchar = line[pos : pos + 1]
        lastchar = line[pos - 1 : pos]
        nextline = line[pos:]
        lastline = line[:pos]

        if error == errors.StringUnterminatedString:
            return False, insert_line(line, '"', len(line))
        if error == errors.ObjectExceptKey:
            if nextchar == "":
                return False, insert_line(line, "}", pos)
            if nextchar == ":":
                return False, insert_line(line, '""', pos)
            if lastchar in "{," and nextchar == ",":
                return False, remove_line(line, pos, pos + 1)
            if lastchar == "," and nextchar == "}":
                return False, remove_line(line, pos - 1, pos)
            if nextchar in "[{":
                return False, insert_line(line, '"":', pos)
            if self._js_style:
                # find 'abc'
                if nextchar == "'":
                    nextline = remove_line(nextline, 0, 1)
                    idx = nextline.find(":")
                    if idx != -1 and idx != 0 and nextline[idx - 1] == "'":
                        nextline = remove_line(nextline, idx - 1, idx)

                    return False, lastline + nextline
                # abc:1 --> "aabc":1
                idx = nextline.find(":")
                if idx != -1:
                    line = lastline + insert_line(nextline, '"', idx)
                    return False, insert_line(line, '"', pos)
            # TODO process more case "
            return False, insert_line(line, '"', pos)
        if error == errors.ObjectExceptColon:
            return False, insert_line(line, ":", pos)
        if error == errors.ObjectExceptObject:
            if nextchar == "":
                if lastchar == "{":
                    return False, insert_line(line, "}", pos)
                return False, insert_line(line, "null}", pos)
            if nextchar == "}":
                return False, insert_line(line, "null", pos)
            # TODO guess more
            return False, insert_line(line, '"', pos)
        if error == errors.ObjectExceptComma:
            if nextchar == "":
                return False, insert_line(line, "}", pos)
            return False, insert_line(line, ",", pos)
        if error == errors.ArrayExceptObject:
            if nextchar == "," and lastchar == "[":
                return False, remove_line(line, pos, pos + 1)
            if nextchar == ",":
                return False, insert_line(line, "null", pos)
            if nextchar == "]":
                return False, remove_line(line, pos - 1, pos)
            if nextchar == "":
                if lastchar == "[":
                    return False, insert_line(line, "]", pos)
                return False, insert_line(line, "null]", pos)
            # TODO guess more?
            return False, insert_line(line, "{", pos)
        if error == errors.ArrayExceptComma:
            if len(line) == pos:
                return False, insert_line(line, "]", pos)
            return False, insert_line(line, ",", pos)
        # TODO unknonwn
        return False, line

    def patch_stop_iteration(self, line: str) -> Tuple[bool, str]:
        # TODO clean
        # TODO fix
        # 1. }]
        # 2. ]}
        # 3. constants
        # 4. -
        # First patch {[]}
        # TODO: process number
        if line.startswith("-."):
            new_line = "-0." + line[2:]
            return False, new_line
        # patch
        left = patch_lastest_left_object_and_array(line)
        if left == "":
            if not self.last_fix:
                left = patch_guess_left(line)

        new_line = left + line
        return False, new_line

    def patch_half_parse(self, line: str, err_info: Any) -> Tuple[bool, str]:
        obj, end = err_info
        nextline = line[end:].strip()
        nextchar = nextline[:1]
        left = patch_lastest_left_object_and_array(nextline)
        # ??
        if left == "":
            if nextchar == ",":
                left = "["
            elif nextchar == ":" and isinstance(obj, str):
                left = "{"
            else:
                if not self.last_fix:
                    left = patch_guess_left(nextline)

        new_line = left + line[:end] + nextline
        return False, new_line


def match_keys(line: str, model: BaseModel) -> dict:
    """json line to model instance

    Args:
        line (str): json line
        model (BaseModel): pydantic model

    Returns:
        dict: model instance
    """
    keys = model.model_fields.keys()
    line = json.loads(line)
    result = {}
    for key in keys:
        if key in line:
            result[key] = line[key]
        else:
            result[key] = None
    return result


def change_model(model: BaseModel) -> BaseModel:
    """change pydantic model to BaseModel

    Args:
        model (BaseModel): pydantic model

    Returns:
        BaseModel: BaseModel
    """
    annotations = {
        field: Optional[type_] for field, type_ in model.__annotations__.items()
    }
    new_model = type(model.__name__, (BaseModel,), {"__annotations__": annotations})
    return new_model


def stream_to_model(response: stream, model: BaseModel) -> stream:
    """stream response to model instance

    Args:
        response (stream): stream response
        model (BaseModel): pydantic model

    Returns:
        stream: stream response
    """
    response_model = change_model(model)
    Util = JSONFixer()
    str = ""
    json_started = False
    for i in response:
        if i == "{":
            json_started = True
        if i == "}":
            json_started = False
        if json_started:
            str += i
            try:
                source = Util.fix(str)
                result = match_keys(source.line, model)
                result = response_model(**result)
                yield result
            except Exception as e:
                raise e

"""Tolerant reader for the data-only object literals that TanStack/seroval
emits into server-rendered HTML (``$R[n]={key:"v",flag:!0,x:void 0}``).

It never evaluates JavaScript. Functions, streams and other non-data
constructs raise ``SerovalParseError`` so callers can record the gap instead
of guessing. Only the literal subset needed for publication metadata is
supported: objects, arrays, strings, numbers, true/false (``!0``/``!1``),
null, ``void 0`` and ``$R[n]=`` reference assignments.
"""
from __future__ import annotations

import json
import re
from typing import Any


class SerovalParseError(ValueError):
    pass


_IDENT = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")
_NUMBER = re.compile(r"-?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")
_REF = re.compile(r"\$R\[(\d+)\]")


class _Reader:
    def __init__(self, text: str, pos: int = 0):
        self.t = text
        self.i = pos
        self.refs: dict[int, Any] = {}

    def ws(self) -> None:
        while self.i < len(self.t) and self.t[self.i] in " \t\r\n":
            self.i += 1

    def peek(self, s: str) -> bool:
        return self.t.startswith(s, self.i)

    def expect(self, s: str) -> None:
        if not self.peek(s):
            raise SerovalParseError(f"expected {s!r} at {self.i}: {self.t[self.i:self.i+40]!r}")
        self.i += len(s)

    def value(self) -> Any:
        self.ws()
        m = _REF.match(self.t, self.i)
        if m:
            self.i = m.end()
            if self.peek("="):
                self.i += 1
                v = self.value()
                self.refs[int(m.group(1))] = v
                return v
            idx = int(m.group(1))
            if idx not in self.refs:
                raise SerovalParseError(f"forward/unknown reference $R[{idx}] at {self.i}")
            return self.refs[idx]
        c = self.t[self.i] if self.i < len(self.t) else ""
        if c == "{":
            return self.obj()
        if c == "[":
            return self.arr()
        if c in "\"'":
            return self.string()
        if self.peek("!0"):
            self.i += 2
            return True
        if self.peek("!1"):
            self.i += 2
            return False
        if self.peek("void 0"):
            self.i += 6
            return None
        for word, val in (("null", None), ("true", True), ("false", False)):
            if self.peek(word) and not _IDENT.match(self.t, self.i + len(word)):
                self.i += len(word)
                return val
        m = _NUMBER.match(self.t, self.i)
        if m:
            self.i = m.end()
            s = m.group(0)
            return float(s) if any(ch in s for ch in ".eE") else int(s)
        raise SerovalParseError(f"unsupported construct at {self.i}: {self.t[self.i:self.i+40]!r}")

    def string(self) -> str:
        q = self.t[self.i]
        j = self.i + 1
        out = []
        while j < len(self.t):
            ch = self.t[j]
            if ch == "\\":
                out.append(self.t[j:j + 2])
                j += 2
                continue
            if ch == q:
                break
            out.append(ch)
            j += 1
        else:
            raise SerovalParseError("unterminated string")
        raw = "".join(out)
        self.i = j + 1
        try:
            if q == '"':
                return json.loads('"' + raw + '"')
            return json.loads('"' + re.sub(r'(?<!\\)"', '\\"', raw).replace("\\'", "'") + '"')
        except json.JSONDecodeError:
            return raw

    def key(self) -> str:
        self.ws()
        if self.t[self.i] in "\"'":
            return self.string()
        m = _IDENT.match(self.t, self.i)
        if not m:
            raise SerovalParseError(f"bad key at {self.i}: {self.t[self.i:self.i+30]!r}")
        self.i = m.end()
        return m.group(0)

    def obj(self) -> dict:
        self.expect("{")
        out: dict[str, Any] = {}
        self.ws()
        if self.peek("}"):
            self.i += 1
            return out
        while True:
            k = self.key()
            self.ws()
            self.expect(":")
            out[k] = self.value()
            self.ws()
            if self.peek(","):
                self.i += 1
                continue
            self.expect("}")
            return out

    def arr(self) -> list:
        self.expect("[")
        out: list[Any] = []
        self.ws()
        if self.peek("]"):
            self.i += 1
            return out
        while True:
            out.append(self.value())
            self.ws()
            if self.peek(","):
                self.i += 1
                continue
            self.expect("]")
            return out


def parse_assignment_after(text: str, anchor: str) -> Any:
    """Parse the literal that follows the first ``anchor`` (e.g. ``project:``)."""
    idx = text.find(anchor)
    if idx < 0:
        raise SerovalParseError(f"anchor {anchor!r} not found")
    return _Reader(text, idx + len(anchor)).value()

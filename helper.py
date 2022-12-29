import dataclasses
from typing import Optional


@dataclasses.dataclass
class Pos:
    o_start: int
    o_end: int
    h_start: int
    h_end: int


def find_shared_kana(orig: str, o_i: int, hira: str, h_i: int):
    o_start, h_start = o_i, h_i

    while orig[o_i] == hira[h_i]:
        o_i += 1
        h_i += 1
        if len(orig) == o_i or len(hira) == h_i:
            return Pos(o_start, len(orig) - 1, h_start, len(hira) - 1)

    return Pos(o_start, o_i - 1, h_start, h_i - 1)


def traverse(orig: str, hira: str) -> Optional[Pos]:
    for o_i in range(1, len(orig)):
        for h_i in range(1, len(hira)):
            if orig[o_i] == hira[h_i]:
                return find_shared_kana(orig, o_i, hira, h_i)
    return None


def deconstruct(orig: str, hira: str) -> str:
    if orig == hira:
        return f"<span style=\"color: #7c7c7c\">{orig}</span>"

    if p := traverse(orig, hira):
        return f"<ruby>{orig[:p.o_start]} <rt>{hira[:p.h_start]}</rt></ruby>" + orig[
                                                                                p.o_start:p.o_end + 1] + deconstruct(
            orig[p.o_end + 1:], hira[p.h_end + 1:])
    else:
        return f"<ruby>{orig} <rt>{hira}</rt></ruby>"


if __name__ == "__main__":
    print(deconstruct("受け付け", "うけつけ"))
    print(deconstruct("送り仮名", "おくりがな"))
    print(deconstruct("ありがとう", "ありがとう"))

    assert deconstruct("受け付け", "うけつけ") == "<ruby>受 <rt>う</rt></ruby>け<ruby>付 <rt>つ</rt></ruby>け<span style=\"color: #7c7c7c\"></span>"
    assert deconstruct("送り仮名", "おくりがな") == "<ruby>送 <rt>おく</rt></ruby>り<ruby>仮名 <rt>がな</rt></ruby>"
    assert deconstruct("ありがとう", "ありがとう") == "<span style=\"color: #7c7c7c\">ありがとう</span>"

# 题目官方完整明文（不需要破解，直接用）
SEQUENCE_TO_CHUNK = {
    0: "My secre",
    1: "t is a f",
    2: "amous sa",
    3: "ying of ",
    4: "Albert E",
    5: "instein.",
    6: " That is",
    7: ' "Logic ',
    8: "will get",
    9: " you fro",
    10: "m A to B",
    11: ". Imagin",
    12: "ation wi",
    13: "ll take ",
    14: "you ever",
    15: 'ywhere."'
}

fulltext = "".join(SEQUENCE_TO_CHUNK[i] for i in range(16))
print("完整明文：")
print(fulltext)
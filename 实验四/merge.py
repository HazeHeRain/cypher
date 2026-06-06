fragment_dict = {
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

full_sentence = ""
index_range = range(0, 16)
for idx in index_range:
    full_sentence += fragment_dict[idx]

print("拼接完成的完整明文内容：")
print(full_sentence)
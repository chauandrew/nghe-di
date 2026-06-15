"""
An explicit, basic curriculum that Claude references to improvise lesson plans

The fallback for unlisted days still works — Claude will improvise a sensible
lesson — but explicit hints produce more focused results.
"""

CURRICULUM: dict[tuple[int, int], dict] = {
    # Day 0 is a pronunciation primer (vowels by mouth-shape + the six tones).
    # It teaches no vocabulary; it is hand-authored in lessons/L1-D0/lesson.json.
    (1,  0):  {"vocab": [],                                            "scene": "pronunciation primer: rounded, neutral, and front vowels, plus the six southern tones"},
    # --- Foundations: politeness, address, numbers, measure words, money ---
    (1,  1):  {"vocab": ["xin chào", "cảm ơn", "dạ"],                  "scene": "greeting a street vendor politely, using dạ to sound respectful"},
    (1,  2):  {"vocab": ["anh", "chị", "em"],                          "scene": "learning to address people by age and gender when greeting them"},
    (1,  3):  {"vocab": ["bao nhiêu", "một", "hai", "ba"],             "scene": "asking the price and counting one to three at a coffee stall"},
    (1,  4):  {"vocab": ["bốn", "năm", "mười"],                        "scene": "counting higher while buying several items"},
    (1,  5):  {"vocab": ["cái", "ly", "chai", "tô", "ổ", "người", "này", "đó"], "scene": "STRUCTURE: measure words and pointing — [number]+[measure]+[noun], and cái này / cái đó"},
    (1,  6):  {"vocab": ["chục", "trăm", "ngàn"],                      "scene": "STRUCTURE: real prices in thousands; cái này bao nhiêu; mấy vs bao nhiêu"},
    # --- Core verbs and grammar frames ---
    (1,  7):  {"vocab": ["tôi muốn", "cà phê", "nước"],               "scene": "ordering: tôi muốn + [number][measure][noun]"},
    (1,  8):  {"vocab": ["ngon", "cay", "quá", "không phải"],          "scene": "STRUCTURE: negation — không + adjective, and không phải"},
    (1,  9):  {"vocab": ["có", "đói", "phải không"],                  "scene": "STRUCTURE: yes/no questions — có...không, ...phải không, answer có/không"},
    (1, 10):  {"vocab": ["ăn", "rồi", "chưa"],                        "scene": "STRUCTURE: completion — ...chưa, answer rồi or chưa"},
    (1, 11):  {"vocab": ["thêm", "ít", "đá"],                          "scene": "customizing an order; the ...đi softener"},
    (1, 12):  {"vocab": ["thích", "đường"],                            "scene": "saying what you like; không đường"},
    # --- Survival scenarios that recycle the frames ---
    (1, 13):  {"vocab": ["ở đâu", "nhà vệ sinh", "bên phải"],          "scene": "asking a guard for the restroom inside a mall"},
    (1, 14):  {"vocab": ["đi", "Bến Thành", "bao lâu"],               "scene": "taking a motorbike taxi to Bến Thành market"},
    (1, 15):  {"vocab": ["tên tôi là", "bạn tên gì"],                 "scene": "introducing yourself to a new coworker"},
    (1, 16):  {"vocab": ["đắt quá", "giảm giá", "được không"],        "scene": "bargaining over a souvenir at a market"},
    (1, 17):  {"vocab": ["tôi không hiểu", "nói chậm hơn", "lại"],     "scene": "asking a taxi driver to repeat the fare slowly"},
    (1, 18):  {"vocab": ["cho tôi", "hóa đơn"],                        "scene": "asking for the bill at a restaurant"},
    (1, 19):  {"vocab": ["gọi món", "lớn", "phần"],                    "scene": "ordering food: a large bowl, one portion"},
    (1, 20):  {"vocab": ["hôm nay", "ngày mai", "hôm qua"],            "scene": "small talk about days with a neighbour"},
    (1, 21):  {"vocab": ["mấy giờ", "buổi sáng", "mở cửa"],           "scene": "calling a restaurant to ask what time it opens"},
    (1, 22):  {"vocab": ["gần", "xa", "đi bộ"],                        "scene": "asking a local whether a place is walkable"},
    (1, 23):  {"vocab": ["siêu thị", "túi ni lông", "tiền thối"],      "scene": "buying snacks and getting change at a supermarket"},
    (1, 24):  {"vocab": ["anh ơi", "chị ơi", "chờ một chút"],         "scene": "getting a busy waiter's attention"},
    (1, 25):  {"vocab": ["hết rồi", "còn không", "loại khác"],        "scene": "the dish you wanted is sold out, asking for an alternative"},
    (1, 26):  {"vocab": ["phòng", "còn phòng không", "một đêm"],       "scene": "checking into a small hotel and asking about availability"},
    (1, 27):  {"vocab": ["tôi bị lạc", "đường này", "quẹo trái"],      "scene": "asking a passerby for directions when lost"},
    (1, 28):  {"vocab": ["tôi cần", "thuốc", "nhà thuốc"],            "scene": "finding a pharmacy and explaining you need medicine"},
    (1, 29):  {"vocab": ["đặt bàn", "mấy người", "tối nay"],          "scene": "calling a restaurant to book a table for tonight"},
    (1, 30):  {"vocab": ["tạm biệt", "hẹn gặp lại", "chúc mừng"],    "scene": "a wrap-up café scene revisiting the most common Level 1 situations"},
    # Add Level 2 entries here:
    # (2,  1): {"vocab": [...], "scene": "..."},
}
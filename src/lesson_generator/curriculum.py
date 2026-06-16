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

    # ===================================================================
    # Level 2 — Time, routines & connected speech (A1->A2)
    # ===================================================================
    (2,  1):  {"vocab": ["giờ", "rưỡi", "sáng", "tối"],               "scene": "STRUCTURE: telling the time — giờ, rưỡi, buổi sáng / buổi tối"},
    (2,  2):  {"vocab": ["thứ hai", "thứ bảy", "chủ nhật"],            "scene": "the days of the week"},
    (2,  3):  {"vocab": ["đang"],                                     "scene": "STRUCTURE: the progressive — đang + verb (I am ...ing)"},
    (2,  4):  {"vocab": ["đã", "sẽ"],                                  "scene": "STRUCTURE: past đã and future sẽ, contrasted with rồi / chưa"},
    (2,  5):  {"vocab": ["dậy", "ngủ", "ăn sáng"],                     "scene": "daily routine verbs: waking, sleeping, breakfast"},
    (2,  6):  {"vocab": ["làm việc", "về nhà", "nấu ăn"],             "scene": "daily routine verbs: work, going home, cooking"},
    (2,  7):  {"vocab": ["thường", "hay", "thỉnh thoảng"],            "scene": "STRUCTURE: frequency adverbs — thường, hay, thỉnh thoảng, không bao giờ"},
    (2,  8):  {"vocab": ["trước", "sau", "sau đó"],                    "scene": "STRUCTURE: sequencing a routine — trước, sau, rồi, sau đó"},
    (2,  9):  {"vocab": ["ông", "bà", "cô", "chú"],                   "scene": "extended address: ông, bà, cô, chú, bác, con"},
    (2, 10):  {"vocab": ["buổi trưa", "buổi chiều"],                  "scene": "describing your whole day (cumulative routine synthesis)"},
    (2, 11):  {"vocab": ["khi", "lúc"],                                "scene": "STRUCTURE: when-clauses — khi, lúc"},
    (2, 12):  {"vocab": ["vậy", "hả", "à"],                            "scene": "STRUCTURE: casual questions — sao vậy, gì vậy, thật à"},
    (2, 13):  {"vocab": ["xe buýt", "Grab", "máy bay"],               "scene": "transport and booking a Grab"},
    (2, 14):  {"vocab": ["cuối tuần", "nghỉ"],                         "scene": "making weekend plans (sẽ + time)"},
    (2, 15):  {"vocab": ["hôm qua", "đi chơi"],                        "scene": "talking about what you did yesterday (đã + past time)"},
    (2, 16):  {"vocab": ["và", "với", "cũng"],                         "scene": "STRUCTURE: joining ideas — và, với, cũng"},
    (2, 17):  {"vocab": ["tháng", "năm", "ngày mấy"],                  "scene": "months and dates"},
    (2, 18):  {"vocab": ["hẹn", "gặp", "lịch"],                        "scene": "making an appointment by phone"},
    (2, 19):  {"vocab": ["nha", "nhé", "nghen"],                       "scene": "STRUCTURE: friendly softeners — nha, nhé, nghen, đi"},
    (2, 20):  {"vocab": ["hơn", "bằng", "nhất"],                       "scene": "STRUCTURE: comparatives — hơn, bằng, nhất"},
    (2, 21):  {"vocab": ["lớn hơn", "rẻ hơn"],                         "scene": "comparing two options (price, size, distance)"},
    (2, 22):  {"vocab": ["chơi", "xem", "nghe nhạc"],                  "scene": "hobbies and free time"},
    (2, 23):  {"vocab": ["rủ", "rảnh"],                                "scene": "inviting someone out (rủ, đi ... không, ... nha)"},
    (2, 24):  {"vocab": ["bao lâu rồi", "được"],                       "scene": "STRUCTURE: duration — how long you have been doing something"},
    (2, 25):  {"vocab": ["lâu rồi", "dạo này"],                        "scene": "catching up with someone you have not seen"},
    (2, 26):  {"vocab": ["bận", "dời", "trễ"],                         "scene": "a phone call to reschedule"},
    (2, 27):  {"vocab": ["hai mươi", "một trăm", "thứ tự"],            "scene": "numbers 11 to 100+ and ordinals"},
    (2, 28):  {"vocab": ["ga", "vé", "chuyến"],                        "scene": "at the bus or train station, buying tickets"},
    (2, 29):  {"vocab": ["một ngày", "bình thường"],                  "scene": "a full day-in-the-life dialogue (integration)"},
    (2, 30):  {"vocab": ["ôn tập", "tiếp theo"],                       "scene": "review and bridge to Level 3"},

    # ===================================================================
    # Level 3 — People, places & opinions (A2)
    # ===================================================================
    (3,  1):  {"vocab": ["ba", "má", "vợ", "chồng"],                  "scene": "family members"},
    (3,  2):  {"vocab": ["đẹp", "lớn", "nhỏ", "mới"],                 "scene": "STRUCTURE: describing nouns — adjective comes after the noun"},
    (3,  3):  {"vocab": ["rất", "hơi", "khá"],                         "scene": "STRUCTURE: degree — rất, hơi, khá (intensity scale)"},
    (3,  4):  {"vocab": ["màu", "đỏ", "xanh", "vàng"],                "scene": "colors"},
    (3,  5):  {"vocab": ["gia đình", "người"],                         "scene": "describing your family"},
    (3,  6):  {"vocab": ["bác sĩ", "giáo viên", "kỹ sư"],             "scene": "jobs and occupations (làm nghề gì)"},
    (3,  7):  {"vocab": ["vui", "buồn", "mệt", "bận"],                "scene": "STRUCTURE: feelings and states — thấy + adjective"},
    (3,  8):  {"vocab": ["khỏe", "sao rồi"],                          "scene": "asking how someone is and how they feel"},
    (3,  9):  {"vocab": ["phòng khách", "phòng ngủ", "bếp"],         "scene": "the house and its rooms"},
    (3, 10):  {"vocab": ["trên", "dưới", "trong", "bên cạnh"],        "scene": "STRUCTURE: location prepositions"},
    (3, 11):  {"vocab": ["ở giữa", "đối diện"],                       "scene": "describing where things are"},
    (3, 12):  {"vocab": ["chợ", "công viên", "ngân hàng"],            "scene": "places around the city"},
    (3, 13):  {"vocab": ["hãy", "đừng", "mình"],                      "scene": "STRUCTURE: suggestions — mình ... đi, ... nhé, hãy, đừng"},
    (3, 14):  {"vocab": ["đi dạo", "cùng"],                           "scene": "suggesting an outing"},
    (3, 15):  {"vocab": ["vì", "nên"],                                "scene": "STRUCTURE: reason — vì ... nên"},
    (3, 16):  {"vocab": ["tại vì", "cho nên"],                        "scene": "explaining why you like or dislike something"},
    (3, 17):  {"vocab": ["cao", "thấp", "dễ thương", "hiền"],        "scene": "appearance and personality"},
    (3, 18):  {"vocab": ["tính tình", "trông"],                       "scene": "describing a friend"},
    (3, 19):  {"vocab": ["tôi nghĩ", "theo tôi"],                     "scene": "STRUCTURE: opinions — tôi nghĩ, theo tôi, thấy ... thế nào"},
    (3, 20):  {"vocab": ["đâu", "luôn", "chứ", "mà"],                 "scene": "STRUCTURE: emphasis & soft negation — đâu có / không...đâu, luôn, chứ, mà"},
    (3, 21):  {"vocab": ["dở", "tuyệt"],                              "scene": "giving an opinion about food or a place (using đâu/luôn/chứ for attitude)"},
    (3, 22):  {"vocab": ["áo", "quần", "thử"],                        "scene": "clothing vocabulary"},
    (3, 23):  {"vocab": ["chật", "rộng", "vừa"],                      "scene": "buying clothes (color, size, trying on)"},
    (3, 24):  {"vocab": ["giống", "khác"],                            "scene": "comparing people and things (hơn + degree review)"},
    (3, 25):  {"vocab": ["đây là", "giới thiệu"],                     "scene": "introductions — đây là (this is my ...)"},
    (3, 26):  {"vocab": ["bạn bè", "quen"],                           "scene": "introducing two people to each other"},
    (3, 27):  {"vocab": ["mời", "sinh nhật"],                         "scene": "invitations and RSVP — mời, rảnh không, được/bận"},
    (3, 28):  {"vocab": ["tham gia", "tiệc"],                         "scene": "inviting someone to a birthday and responding"},
    (3, 29):  {"vocab": ["họp mặt", "vui vẻ"],                        "scene": "a social gathering (integration)"},
    (3, 30):  {"vocab": ["ôn tập", "tiếp theo"],                       "scene": "review and bridge to Level 4"},
}
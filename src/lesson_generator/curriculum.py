"""
An explicit, basic curriculum that Claude references to improvise lesson plans

The fallback for unlisted days still works — Claude will improvise a sensible
lesson — but explicit hints produce more focused results.
"""

CURRICULUM: dict[tuple[int, int], dict] = {
    # Day 0 is a pronunciation primer (vowels by mouth-shape + the six tones).
    # It is hand-authored in lessons/L1-D0/lesson.json. It teaches no vocabulary —
    # tones are described in plain English here and throughout L1-L3 (too much,
    # too soon, for a Day-1 beginner to name six tone marks). The tone-mark NAMES
    # themselves are taught later, as real vocabulary, at L4-D0 — from L4-D0 onward
    # the system prompt names a word's tone in Vietnamese using those names instead
    # of an English description.
    (1,  0):  {"vocab": [],                                            "scene": "pronunciation primer: rounded, neutral, and front vowels, plus the six southern tones"},
    # --- Foundations: politeness, address, numbers, measure words, money ---
    (1,  1):  {"vocab": ["xin chào", "cảm ơn", "dạ"],                  "scene": "greeting a street vendor politely, using dạ to sound respectful"},
    (1,  2):  {"vocab": ["anh", "chị", "em"],                          "scene": "learning to address people by age and gender when greeting them"},
    (1,  3):  {"vocab": ["bao nhiêu", "một", "hai", "ba", "bốn", "năm"], "scene": "asking the price and counting one to five at a coffee stall (numbers are a rote set, so this day runs a little heavier)"},
    (1,  4):  {"vocab": ["sáu", "bảy", "tám", "chín", "mười"],          "scene": "counting six to ten while buying several items; after today the learner can count one to ten"},
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
    (1, 13):  {"vocab": ["ở đâu", "nhà vệ sinh", "bên phải", "bên trái"], "scene": "asking a guard for the restroom inside a mall; bên phải/bên trái (on the right/on the left) taught as a pair"},
    (1, 14):  {"vocab": ["đi", "Bến Thành", "bao lâu"],               "scene": "taking a motorbike taxi to Bến Thành market"},
    (1, 15):  {"vocab": ["tên tôi là", "bạn tên gì", "ai", "gì"],     "scene": "introducing yourself to a new coworker; ai (who) and gì (what) taught as free-standing question words"},
    (1, 16):  {"vocab": ["đắt quá", "rẻ", "giảm giá", "được không"],  "scene": "bargaining over a souvenir at a market; đắt/rẻ (expensive/cheap) taught as a pair"},
    (1, 17):  {"vocab": ["tôi không hiểu", "biết", "nói chậm hơn", "lại"], "scene": "asking a taxi driver to repeat the fare slowly; tôi không biết pairs with tôi không hiểu"},
    (1, 18):  {"vocab": ["cho tôi", "hóa đơn"],                        "scene": "asking for the bill at a restaurant"},
    (1, 19):  {"vocab": ["gọi món", "lớn", "phần"],                    "scene": "ordering food: a large bowl, one portion"},
    (1, 20):  {"vocab": ["hôm nay", "ngày mai", "hôm qua"],            "scene": "small talk about days with a neighbour"},
    (1, 21):  {"vocab": ["mấy giờ", "buổi sáng", "mở cửa", "đóng cửa"], "scene": "calling a restaurant to ask what time it opens; mở cửa/đóng cửa (open/closed) taught as a pair"},
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
    (2,  1):  {"vocab": ["giờ", "rưỡi", "sáng", "trưa", "chiều", "tối"], "scene": "STRUCTURE: telling the time — giờ, rưỡi, and the full sáng/trưa/chiều/tối day-part set (a closed set, taught together rather than split)"},
    (2,  2):  {"vocab": ["thứ hai", "thứ bảy", "chủ nhật"],            "scene": "the days of the week"},
    (2,  3):  {"vocab": ["đang"],                                     "scene": "STRUCTURE: the progressive — đang + verb (I am ...ing)"},
    (2,  4):  {"vocab": ["đã", "sẽ"],                                  "scene": "STRUCTURE: past đã and future sẽ, contrasted with rồi / chưa"},
    (2,  5):  {"vocab": ["dậy", "ngủ", "ăn sáng"],                     "scene": "daily routine verbs: waking, sleeping, breakfast"},
    (2,  6):  {"vocab": ["làm việc", "về nhà", "nấu ăn"],             "scene": "daily routine verbs: work, going home, cooking"},
    (2,  7):  {"vocab": ["thường", "hay", "thỉnh thoảng", "không bao giờ"], "scene": "STRUCTURE: frequency adverbs — thường, hay, thỉnh thoảng, không bao giờ"},
    (2,  8):  {"vocab": ["trước", "sau", "sau đó"],                    "scene": "STRUCTURE: sequencing a routine — trước, sau, rồi, sau đó"},
    (2,  9):  {"vocab": ["ông", "bà", "cô", "chú", "bác", "con"],     "scene": "extended address: ông, bà, cô, chú, bác, con (a closed set, taught together)"},
    (2, 10):  {"vocab": [],                                           "scene": "describing your whole day (cumulative routine synthesis, no new words — trưa/chiều now taught at D1)"},
    (2, 11):  {"vocab": ["khi", "lúc", "khi nào"],                     "scene": "STRUCTURE: when-clauses — khi, lúc, and the question word khi nào (when?)"},
    (2, 12):  {"vocab": ["vậy", "hả", "à"],                            "scene": "STRUCTURE: casual questions — sao vậy, gì vậy, thật à"},
    (2, 13):  {"vocab": ["xe buýt", "Grab", "máy bay"],               "scene": "transport and booking a Grab"},
    (2, 14):  {"vocab": ["cuối tuần", "nghỉ"],                         "scene": "making weekend plans (sẽ + time)"},
    (2, 15):  {"vocab": ["đi chơi"],                                   "scene": "talking about what you did yesterday (đã + past time; hôm qua is review from L1-D20, not new)"},
    (2, 16):  {"vocab": ["và", "với", "cũng"],                         "scene": "STRUCTURE: joining ideas — và, với, cũng"},
    (2, 17):  {"vocab": ["mười lăm", "hai mươi mốt", "tư", "một trăm"], "scene": "STRUCTURE: building numbers — teens (mười + digit), tens (digit + mươi), hundreds (trăm), ordinals via thứ (review). Teach the three sound-changes: năm->lăm (15, 25), một->mốt (21, 31), bốn->tư (24, and tháng Tư = April). The learner already counts 1-10, so this consolidates rather than first-teaches. Comes before dates so the calendar has its numbers."},
    (2, 18):  {"vocab": ["tháng", "năm", "ngày mấy"],                  "scene": "months and dates (note: năm here means year — a different word from năm/five taught in L1-D3; flag the contrast for the learner)"},
    (2, 19):  {"vocab": ["hẹn", "gặp", "lịch"],                        "scene": "making an appointment by phone"},
    (2, 20):  {"vocab": ["nha", "nhé", "nghen", "đi (softener)"],      "scene": "STRUCTURE: friendly softeners — nha, nhé, nghen, đi. Note: this đi is a different word/job from đi = go taught at L1-D14 — flag the contrast for the learner"},
    (2, 21):  {"vocab": ["hơn", "bằng", "nhất"],                       "scene": "STRUCTURE: comparatives — hơn, bằng, nhất"},
    (2, 22):  {"vocab": ["lớn hơn", "rẻ hơn"],                         "scene": "comparing two options (price, size, distance)"},
    (2, 23):  {"vocab": ["chơi", "xem", "nghe nhạc"],                  "scene": "hobbies and free time"},
    (2, 24):  {"vocab": ["rủ", "rảnh"],                                "scene": "inviting someone out (rủ, đi ... không, ... nha)"},
    (2, 25):  {"vocab": ["bao lâu rồi", "được"],                       "scene": "STRUCTURE: duration — how long you have been doing something (note: được here means to manage/capability — a different job from the được không tag-question at L1-D16; flag the contrast)"},
    (2, 26):  {"vocab": ["lâu rồi", "dạo này"],                        "scene": "catching up with someone you have not seen"},
    (2, 27):  {"vocab": ["bận", "dời", "trễ", "sớm"],                  "scene": "a phone call to reschedule; sớm/trễ (early/late) taught as a pair"},
    (2, 28):  {"vocab": ["ga", "vé", "chuyến"],                        "scene": "at the bus or train station, buying tickets"},
    (2, 29):  {"vocab": ["một ngày", "bình thường"],                  "scene": "a full day-in-the-life dialogue (integration)"},
    (2, 30):  {"vocab": ["ôn tập", "tiếp theo"],                       "scene": "review and bridge to Level 3"},

    # ===================================================================
    # Level 3 — People, places & opinions (A2)
    # ===================================================================
    (3,  1):  {"vocab": ["ba", "má", "vợ", "chồng"],                  "scene": "family members (note: ba here means dad — a different word from ba/three taught in L1-D3; flag the contrast for the learner)"},
    (3,  2):  {"vocab": ["đẹp", "nhỏ", "mới", "cũ"],                  "scene": "STRUCTURE: describing nouns — adjective comes after the noun (lớn is review from L1-D19, not new; mới/cũ taught as a pair)"},
    (3,  3):  {"vocab": ["rất", "hơi", "khá"],                         "scene": "STRUCTURE: degree — rất, hơi, khá (intensity scale)"},
    (3,  4):  {"vocab": ["màu", "đỏ", "xanh", "vàng", "đen", "trắng"], "scene": "colors (a closed set, taught together rather than split)"},
    (3,  5):  {"vocab": ["gia đình", "người"],                         "scene": "describing your family"},
    (3,  6):  {"vocab": ["bác sĩ", "giáo viên", "kỹ sư"],             "scene": "jobs and occupations (làm nghề gì)"},
    (3,  7):  {"vocab": ["vui", "buồn", "mệt", "bận"],                "scene": "STRUCTURE: feelings and states — thấy + adjective"},
    (3,  8):  {"vocab": ["khỏe", "sao rồi"],                          "scene": "asking how someone is and how they feel"},
    (3,  9):  {"vocab": ["phòng khách", "phòng ngủ", "bếp"],         "scene": "the house and its rooms"},
    (3, 10):  {"vocab": ["trên", "dưới", "trong", "ngoài", "bên cạnh"], "scene": "STRUCTURE: location prepositions (trong/ngoài taught as a pair)"},
    (3, 11):  {"vocab": ["ở giữa", "đối diện"],                       "scene": "describing where things are"},
    (3, 12):  {"vocab": ["chợ", "công viên", "ngân hàng"],            "scene": "places around the city"},
    (3, 13):  {"vocab": ["hãy", "đừng", "mình"],                      "scene": "STRUCTURE: suggestions — mình ... đi, ... nhé, hãy, đừng"},
    (3, 14):  {"vocab": ["đi dạo", "cùng"],                           "scene": "suggesting an outing"},
    (3, 15):  {"vocab": ["vì", "nên", "tại sao"],                     "scene": "STRUCTURE: reason — vì ... nên, plus the question word tại sao (why?)"},
    (3, 16):  {"vocab": ["tại vì", "cho nên"],                        "scene": "explaining why you like or dislike something"},
    (3, 17):  {"vocab": ["cao", "thấp", "dễ thương", "hiền"],        "scene": "appearance and personality"},
    (3, 18):  {"vocab": ["tính tình", "trông"],                       "scene": "describing a friend"},
    (3, 19):  {"vocab": ["tôi nghĩ", "theo tôi", "thế nào"],          "scene": "STRUCTURE: opinions — tôi nghĩ, theo tôi, thấy ... thế nào"},
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

    # ===================================================================
    # Level 4 — Problem-solving, modality & conditionals (A2->B1)
    # Vocab curated to <=3-4 new content words/day (structure days lighter);
    # the doc's fuller domain lists are split across days to keep the pace
    # catchable for a beginner. See docs/curriculum-units-2-5.md.
    # ===================================================================
    # Day 0 is a second pronunciation primer, hand-authored in lessons/L4-D0/lesson.json.
    # By now the learner has 320+ words and has heard hundreds of plain-English tone
    # descriptions ("a high, rising tone") — this is where those get names. Teaches the
    # six tone-mark NAMES as real vocabulary. From here on, the system prompt names a
    # word's tone in Vietnamese using these names instead of an English description.
    (4,  0):  {"vocab": ["ngang", "dấu huyền", "dấu sắc", "dấu hỏi", "dấu ngã", "dấu nặng"],
                                                                        "scene": "pronunciation primer, part two: naming the six tones you already hear — ngang, dấu huyền, dấu sắc, dấu hỏi, dấu ngã, dấu nặng"},
    (4,  1):  {"vocab": ["đầu", "bụng", "tay", "chân"],               "scene": "body parts: head, stomach, hand/arm, leg/foot"},
    (4,  2):  {"vocab": ["đau", "bị", "sốt", "cảm"],                   "scene": "STRUCTURE: symptoms — đau + body part, bị + illness (bị cảm, bị sốt)"},
    (4,  3):  {"vocab": ["khám", "họng", "ho"],                        "scene": "at the doctor: describing symptoms (bác sĩ khám, đau họng, ho)"},
    (4,  4):  {"vocab": ["nên", "phải", "cần"],                        "scene": "STRUCTURE: modality — nên (should), phải (must), cần (need); recombines known words. Note: this nên is a different word from the vì...nên connector at L3-D15 — flag the contrast for the learner"},
    (4,  5):  {"vocab": ["viên", "lần"],                              "scene": "at the pharmacy: dosage — uống mấy viên, mấy lần một ngày"},
    (4,  6):  {"vocab": ["có thể"],                                   "scene": "STRUCTURE: ability & permission — có thể, ...được không (may I; được không is review from L1-D16, not new — it generalizes here to any request)"},
    (4,  7):  {"vocab": ["phiền", "giúp"],                             "scene": "making a polite request and asking permission (phiền anh..., ...giúp)"},
    (4,  8):  {"vocab": ["nếu", "thì"],                                "scene": "STRUCTURE: conditional — nếu ... thì (if ... then)"},
    (4,  9):  {"vocab": ["mưa", "nắng", "trời", "nóng", "lạnh"],       "scene": "planning around the weather (nếu trời mưa thì ...); nóng/lạnh (hot/cold) taught as a pair"},
    (4, 10):  {"vocab": ["rút tiền", "đổi tiền", "chuyển khoản"],      "scene": "at the bank: withdraw, exchange, transfer money"},
    (4, 11):  {"vocab": ["thẻ", "hư", "thử lại"],                      "scene": "a problem at the ATM (máy nuốt thẻ, thẻ bị hư)"},
    (4, 12):  {"vocab": ["gửi", "bưu điện", "kiện hàng"],             "scene": "the post office and deliveries (gửi kiện hàng)"},
    (4, 13):  {"vocab": ["bị", "được"],                               "scene": "STRUCTURE: passive — bị (bad outcome) / được (good outcome) + verb. Note: được is doing its THIRD distinct job here (after the L1-D16 tag-question and the L2-D25 capability sense) — flag the contrast for the learner"},
    (4, 14):  {"vocab": ["mất", "trộm", "bể"],                         "scene": "reporting something lost, stolen, or broken (bị mất, bị trộm)"},
    (4, 15):  {"vocab": ["máy lạnh"],                                  "scene": "hotel room problems (máy lạnh bị hư, không có nước nóng; nóng is review from L4-D9, not new)"},
    (4, 16):  {"vocab": ["sửa", "đổi phòng"],                          "scene": "complaining at the hotel and getting it fixed"},
    (4, 17):  {"vocab": ["kẹt xe", "lỡ", "hủy"],                       "scene": "transport problems: traffic jam, missed it, cancelled"},
    (4, 18):  {"vocab": ["kịp", "chuyến sau"],                         "scene": "missing your transport and rebooking (chuyến sau, cho kịp)"},
    (4, 19):  {"vocab": ["càng"],                                     "scene": "STRUCTURE: superlative nhất (review) and càng ... càng (the more ... the more)"},
    (4, 20):  {"vocab": ["tốt", "lựa chọn"],                          "scene": "choosing the best option (tốt nhất, so sánh lựa chọn)"},
    (4, 21):  {"vocab": ["qua", "dọc theo", "ngã tư"],                "scene": "complex directions: across, along, at the intersection"},
    (4, 22):  {"vocab": ["đèn đỏ", "vòng xoay"],                       "scene": "directions across town (rẽ ở đèn đỏ, qua vòng xoay)"},
    (4, 23):  {"vocab": ["cấp cứu", "cảnh sát", "nguy hiểm"],          "scene": "emergencies: ambulance/ER, police, danger (gọi giúp)"},
    (4, 24):  {"vocab": ["gấp", "ngay"],                              "scene": "asking for urgent help (cần gấp, tới ngay)"},
    (4, 25):  {"vocab": ["nói là", "bảo"],                             "scene": "STRUCTURE: simple reported speech — nói là, bảo (X said that ...)"},
    (4, 26):  {"vocab": ["nhắn", "tin nhắn"],                          "scene": "relaying a message (nhắn giúp, để lại tin nhắn)"},
    (4, 27):  {"vocab": ["thợ", "xong"],                              "scene": "services and repairs: thợ (worker), sửa (review), bao lâu xong"},
    (4, 28):  {"vocab": [],                                           "scene": "cumulative problem-solving review: recombine the Level 4 frames, no new words"},
    (4, 29):  {"vocab": [],                                           "scene": "a multi-step errand: bank, then post office, then a repair (full integration)"},
    (4, 30):  {"vocab": ["ôn tập", "tiếp theo"],                       "scene": "review and bridge to Level 5"},

    # ===================================================================
    # Level 5 — Narration, nuance & culture (B1)
    # Southern register throughout; northern-only particles from the doc
    # (đấy, cơ) are replaced by southern đó and taught with a register note.
    # ===================================================================
    (5,  1):  {"vocab": ["đầu tiên", "cuối cùng"],                    "scene": "STRUCTURE: narrative sequencing — đầu tiên (first), sau đó (review), cuối cùng (finally)"},
    (5,  2):  {"vocab": ["kể"],                                       "scene": "telling the story of your day or a trip (extended narration with sequencers)"},
    (5,  3):  {"vocab": ["nhưng", "tuy nhiên", "mặc dù"],             "scene": "STRUCTURE: contrast — nhưng (but), tuy nhiên (however), mặc dù ... nhưng (although)"},
    (5,  4):  {"vocab": ["sinh ra", "lớn lên", "kết hôn"],            "scene": "life events and timeline: born, grew up, married"},
    (5,  5):  {"vocab": ["chuyển đến", "quê"],                         "scene": "telling your life story briefly (quê, chuyển đến, integration)"},
    (5,  6):  {"vocab": ["mong", "hi vọng", "ước"],                   "scene": "STRUCTURE: wishes and hopes — mong, hi vọng, ước"},
    (5,  7):  {"vocab": ["mục tiêu", "tương lai"],                     "scene": "talking about goals and future plans (mong/hi vọng + sẽ)"},
    (5,  8):  {"vocab": ["giá mà", "phải chi"],                        "scene": "STRUCTURE: hypothetical & regret — giá mà / phải chi ... (if only ...)"},
    (5,  9):  {"vocab": ["biết trước"],                               "scene": "expressing regret about the past (giá mà biết trước ... thì đã ...)"},
    (5, 10):  {"vocab": ["Tết", "lì xì"],                             "scene": "Tết customs: Tết, lì xì (lucky money), chúc (review)"},
    (5, 11):  {"vocab": ["sức khỏe", "may mắn"],                       "scene": "Tết greetings and small talk (chúc sức khỏe, chúc may mắn)"},
    (5, 12):  {"vocab": ["món ăn", "đặc sản", "miền"],                "scene": "regional food culture: món ăn, đặc sản (specialty), miền (region)"},
    (5, 13):  {"vocab": ["nổi tiếng"],                                "scene": "recommending and describing a dish (đặc sản nổi tiếng, thử review)"},
    (5, 14):  {"vocab": ["có lẽ", "chắc", "không hẳn"],               "scene": "STRUCTURE: opinion nuance — có lẽ (maybe), chắc (probably), không hẳn (not really)"},
    (5, 15):  {"vocab": ["đồng ý", "phản đối"],                       "scene": "discussing a topic and (dis)agreeing (đồng ý, không đồng ý, phản đối)"},
    (5, 16):  {"vocab": ["đám cưới", "cô dâu", "chú rể"],             "scene": "weddings: đám cưới, cô dâu (bride), chú rể (groom)"},
    (5, 17):  {"vocab": ["mừng", "quà"],                              "scene": "at a celebration: congratulations and small talk (mừng, tặng quà)"},
    (5, 18):  {"vocab": ["mà"],                                       "scene": "STRUCTURE: relative clauses — [noun] mà [clause] (the ... that ...); mà reviewed as relativizer"},
    (5, 19):  {"vocab": ["nơi", "kỷ niệm"],                           "scene": "describing a person or place in detail (relative clauses)"},
    (5, 20):  {"vocab": ["công ty", "dự án", "áp lực"],               "scene": "work and career: công ty (company), dự án (project), áp lực (pressure)"},
    (5, 21):  {"vocab": ["đồng nghiệp", "thăng chức"],                "scene": "a conversation about work (đồng nghiệp, deadlines, thăng chức)"},
    (5, 22):  {"vocab": ["chứ", "đó"],                                "scene": "STRUCTURE: emphatic particles (southern) — chứ (reviewed from its L3-D20 soft-negation use, now an agreement-seeking particle), đó (reviewed from its L1-D5 demonstrative use, now a sentence-final particle); note the northern đấy/cơ you will also hear"},
    (5, 23):  {"vocab": [],                                           "scene": "a lively casual conversation reusing particles and softeners, no new words"},
    (5, 24):  {"vocab": ["chuyến đi", "ấn tượng", "phong cảnh"],       "scene": "narrating a trip: chuyến đi, ấn tượng (impression), phong cảnh (scenery)"},
    (5, 25):  {"vocab": ["nhớ", "quên"],                              "scene": "recounting a memorable trip (nhớ, quên, past narration)"},
    (5, 26):  {"vocab": ["miền Bắc", "miền Nam", "giọng"],            "scene": "register and regional differences: miền Bắc/Nam, giọng (accent), North vs South words"},
    (5, 27):  {"vocab": ["lịch sự", "thân mật"],                       "scene": "switching register by audience (lịch sự formal vs thân mật casual)"},
    (5, 28):  {"vocab": ["môi trường", "công nghệ", "vấn đề"],         "scene": "current topics: môi trường (environment), công nghệ (technology), vấn đề (issue)"},
    (5, 29):  {"vocab": [],                                           "scene": "a reasoned opinion on a topic (vì...nên, tôi nghĩ, có lẽ), no new words"},
    (5, 30):  {"vocab": ["ôn tập", "tổng kết"],                       "scene": "capstone: extended free conversation and course wrap-up"},
}
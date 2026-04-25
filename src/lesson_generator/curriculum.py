"""
An explicit, basic curriculum that Claude references to improvise lesson plans

The fallback for unlisted days still works — Claude will improvise a sensible
lesson — but explicit hints produce more focused results.
"""

CURRICULUM: dict[tuple[int, int], dict] = {
    (1,  1):  {"vocab": ["xin chào", "cảm ơn", "bao nhiêu"],           "scene": "greeting a vendor at a HCMC street coffee stall and asking the price"},
    (1,  2):  {"vocab": ["một", "hai", "ba", "năm nghìn"],              "scene": "ordering one or two bánh mì sandwiches and paying"},
    (1,  3):  {"vocab": ["tôi muốn", "cà phê sữa đá", "không đường"],  "scene": "ordering a customised drink at a Highlands Coffee in HCMC"},
    (1,  4):  {"vocab": ["ở đâu", "nhà vệ sinh", "bên phải"],           "scene": "asking a security guard for the bathroom inside a Vincom mall"},
    (1,  5):  {"vocab": ["đi", "bến thành", "bao lâu"],                 "scene": "negotiating a xe ôm ride to Bến Thành market"},
    (1,  6):  {"vocab": ["ngon", "không ngon", "cay"],                  "scene": "commenting on food at a bún bò Huế stall with a local colleague"},
    (1,  7):  {"vocab": ["tên tôi là", "bạn tên gì", "người Việt Nam"], "scene": "introducing yourself to a new coworker at the office"},
    (1,  8):  {"vocab": ["hôm nay", "ngày mai", "hôm qua"],             "scene": "chatting about weekend plans with a neighbour in the elevator"},
    (1,  9):  {"vocab": ["mấy giờ", "buổi sáng", "mở cửa"],            "scene": "calling a phở restaurant to ask what time they open"},
    (1, 10):  {"vocab": ["đắt quá", "rẻ hơn", "được không"],           "scene": "bargaining over a souvenir lacquerware bowl at Chợ Lớn"},
    (1, 11):  {"vocab": ["tôi không hiểu", "nói chậm hơn", "lại"],     "scene": "asking a taxi driver to repeat the fare more slowly"},
    (1, 12):  {"vocab": ["cho tôi", "hóa đơn", "thêm"],                "scene": "asking for the bill and an extra napkin at a sit-down restaurant"},
    (1, 13):  {"vocab": ["gọi món", "tô lớn", "ít đá"],                "scene": "ordering phở with customisations at a Phở Hùng restaurant"},
    (1, 14):  {"vocab": ["bốn", "năm", "mười"],                        "scene": "counting items and paying exact change at a convenience store"},
    (1, 15):  {"vocab": ["gần", "xa", "đi bộ"],                        "scene": "asking a local whether the nearest ATM is walkable"},
    (1, 16):  {"vocab": ["trời", "nóng", "mưa"],                       "scene": "making small talk about the heat with a shopkeeper"},
    (1, 17):  {"vocab": ["tôi bị lạc", "đường này", "quẹo trái"],      "scene": "stopping a passerby for directions after getting turned around in Bình Thạnh"},
    (1, 18):  {"vocab": ["siêu thị", "túi ni lông", "tiền thối"],       "scene": "buying water and snacks at a Co.op Mart and getting change"},
    (1, 19):  {"vocab": ["tôi thích", "không thích", "món ăn"],        "scene": "telling a street vendor which dishes you enjoy and which you avoid"},
    (1, 20):  {"vocab": ["số điện thoại", "của tôi", "nhắn tin"],       "scene": "exchanging phone numbers with a new acquaintance after a language exchange"},
    (1, 21):  {"vocab": ["uống", "trà đá", "nước cam"],                 "scene": "being offered drinks as a guest at a colleague's home in Gò Vấp"},
    (1, 22):  {"vocab": ["anh ơi", "chị ơi", "chờ một chút"],          "scene": "flagging down a waiter at a busy rooftop bar in District 3"},
    (1, 23):  {"vocab": ["hết rồi", "còn không", "loại khác"],         "scene": "discovering the dish you wanted is sold out and asking for an alternative"},
    (1, 24):  {"vocab": ["phòng", "còn phòng không", "một đêm"],        "scene": "checking into a mini-hotel in Phú Nhuận and asking about availability"},
    (1, 25):  {"vocab": ["wifi", "mật khẩu", "kết nối"],               "scene": "asking café staff for the wifi password"},
    (1, 26):  {"vocab": ["tôi cần", "thuốc", "nhà thuốc"],             "scene": "finding a pharmacy and explaining you need cold medicine"},
    (1, 27):  {"vocab": ["lâu chưa", "mới đến", "đã lâu"],             "scene": "chatting with an expat neighbour about how long you have both lived in HCMC"},
    (1, 28):  {"vocab": ["đặt bàn", "bao nhiêu người", "tối nay"],     "scene": "calling a restaurant in Thảo Điền to book a table for tonight"},
    (1, 29):  {"vocab": ["giao hàng", "địa chỉ", "bao lâu nữa"],       "scene": "tracking a GrabFood order and asking the driver how much longer they will be"},
    (1, 30):  {"vocab": ["tạm biệt", "hẹn gặp lại", "chúc mừng"],     "scene": "a wrap-up café scene revisiting the most common Level 1 situations"},
    # Add Level 2 entries here:
    # (2,  1): {"vocab": [...], "scene": "..."},
}
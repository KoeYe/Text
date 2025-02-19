import random

# 3D模型类型列表
object_types = ['billboard', 'street sign', 'wayfinding sign', 'city slogan banner', 'storefront sign', 'traffic sign', 'building text', 'advertisement board']

# 可能出现的具体文字内容
texts = [
    "Super Sale! 50% off all items",
    "Next-Gen Gadgets Available Now!",
    "Route 42 - Downtown Express",
    "Unity in Diversity",
    "Live, Laugh, Love",
    "Cafe Bliss",
    "Freshly Baked Bread, Hot Out of the Oven",
    "STOP",
    "YIELD",
    "Sky Tower - The Ultimate Experience",
    "Dedicated to the Founders of the City",
    "Live Music Tonight: Rock Legends",
    "Fall Collection Now Available"
]

# 描述文字风格
styles = [
    "in bold, eye-catching letters with a bright red background",
    "in futuristic font with neon lighting effects",
    "in a clear, simple font",
    "in bold yellow letters on a reflective background",
    "in clear, large font with directional arrows",
    "in clear white text on a blue background",
    "in colorful, large letters",
    "in a modern cursive font with bright pink and yellow colors",
    "in stylish, cursive font",
    "in white chalk font",
    "in bold white font",
    "in sleek, modern letters",
    "in stone engraving",
    "in large, colorful text"
]

# 随机生成prompt
def generate_prompt():
    object_type = random.choice(object_types)
    text = random.choice(texts)
    style = random.choice(styles)

    return f"A 3D model of a {object_type} displaying the text '{text}' {style}."

# 生成多个不同的prompt
for _ in range(10):
    print(generate_prompt())

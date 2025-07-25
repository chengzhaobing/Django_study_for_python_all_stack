

from PIL import Image,ImageDraw,ImageFont

# 生成白底图片
img = Image.new(mode='RGB',size=(120,30), color=(255,255,255))

# 创建画笔
draw = ImageDraw.Draw(img, mode='RGB')

# 设置字体字号
font = ImageFont.truetype("fontone.ttf", size=20)

# 绘制文本
draw.text([0,0], '程照斌', 'red', font=font)



with open('chengzhaobin.png', 'wb') as f:
    img.save(f, format='png')

from notify.util import SQLite, Redis


sqlite = SQLite()
redis = Redis()

db = {
 'colors': 'White / Green / Blue',
 'date': '2019-01-03 21:57:33',
 'image': 'https://cdn.shopify.com/s/files/1/0094/2252/products/Adidas_Yung_1_G27031_3935_700x700_crop_center.progressive.jpg?v=1543535712',
 'link': 'https://kith.com/collections/footwear/products/adidas-originals-yung-1-white-green-blue',
 'name': 'adidas Originals Yung 1',
 'price': '$120.00',
 'size': ['https://kith.com/cart/add.js?id=18551300980805&quantity=1'],
 'sizes': ['13', '']
}

cursor = sqlite.create_tables()

# redis.push('nike', 'Airmax')
# redis.push('nike', 'Airmax Jordan')
# redis.push('nike', 'Jordan Kicks')
val = redis().sadd('kith', "{} {}".format(db['link'], db['image']))
print(val)
# print(redis().linsert('nike', 'after', 'Airmax Jordan', "Airmax Kobe"))
print(redis.pull('nike'))

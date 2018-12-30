
from notify.util import select_data, insert_data, create_tables
import random


data = [
{'colors': '',
 'date': '2018-12-30',
 'image': 'https://cdn.shopify.com/s/files/1/1765/5971/products/fin_440x.jpg?v=1543693873',
 'link': 'https://yeezysupply.com/products/mens-combat-boot-in-thick-suede-military?c=%2Fcollections%2Fnew-arrivals-footwear%2F',
 'name': 'THICK SUEDE COMBAT BOOT',
 'price': '$220'},
{'colors': '',
 'date': '2018-12-30',
 'image': 'https://cdn.shopify.com/s/files/1/1765/5971/products/la_440x.jpg?v=1543693861',
 'link': 'https://yeezysupply.com/products/mens-combat-boot-in-thick-suede-graphite?c=%2Fcollections%2Fnew-arrivals-footwear%2F',
 'name': 'THICK SUEDE COMBAT BOOT',
 'price': '$220'},
{'colors': '',
 'date': '2018-12-30',
 'image': 'https://cdn.shopify.com/s/files/1/1765/5971/products/KW2581.022_Side1_color_onyx-shade_10313325-1773-49dd-9aea-6b9861925324_440x.jpg?v=1544040245',
 'link': 'https://yeezysupply.com/products/womens-military?c=%2Fcollections%2Fnew-arrivals-footwear%2F',
 'name': 'WOMENS BOOT',
 'price': '$220'},
{'colors': '',
 'date': '2018-12-30',
 'image': 'https://cdn.shopify.com/s/files/1/1765/5971/products/KM2606.012_Side1_color_onyx-shade_70012e4e-b24a-401a-992f-81e61300586f_440x.jpg?v=1544039929',
 'link': 'https://yeezysupply.com/products/mens-military-boot?c=%2Fcollections%2Fnew-arrivals-footwear%2F',
 'name': 'MENS BOOT',
 'price': '$220'}
]

cursor = create_tables()

d = random.choice(data)

res = insert_data('yeezy', name=str(d['name']), price=d['price'], image=d['image'], link=d['link'], date=d['date'])
print(res)

da = select_data('yeezy')
print(len(da))

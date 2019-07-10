import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey

# 改成你存放数据库文件的路径，注意data.db需要提前创建
db_file = r'E:\pythonProjects\cluebearpython\chapter9\data'
engine = create_engine('sqlite:///{}'.format(os.path.join(db_file, 'data.db')), encoding='utf8')
DBSession = sessionmaker(bind=engine)
# 创建数据库会话实例
sess = DBSession()


Base = declarative_base()
class ShopBasic(Base):
    # 表的名字:
    __tablename__ = 'basic'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    time = Column(String(20), nullable=True)


class ShopCoupon(Base):
    # 表的名字:
    __tablename__ = 'coupon'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 添加外键
    shop_id = Column(Integer, ForeignKey('basic.id'))
    day = Column(String(5))
    coupon = Column(String(30))

# 会自动检查表是否存在，如果表不存在，则创建；如果已经存在，则忽略，也可以手动注释，增强可读性。
Base.metadata.create_all(engine)


shops = [
    (311, "老北京涮羊肉", '11:00-21:00', [['周一', '满60减10'], ['周二', '满100减20']]),
    (312, "大龙燚火锅", '10:00-22:00', [['周一', '满60减10'], ['周二', '满100减20']]),
    (313, "一尊皇牛", '00:00-24:00', [['周一', '满80减10'], ['周二', '满100减10']]),
]

news = []
for shop in shops:
    new = ShopBasic(id=shop[0], name=shop[1], time=shop[2])
    news.append(new)

sess.add_all(news)
sess.commit()

shops = sess.query(ShopBasic).all()
for shop in shops:
    print(shop.id, shop.name, shop.time)

shops = sess.query(ShopBasic).filter_by(name='老北京涮羊肉').all()
shops[0].__dict__

# 排序
shops = sess.query(ShopBasic).order_by('name').all()
for shop in shops:
    print(shop.id, shop.name, shop.time)

# 修改营业时间
shop = sess.query(ShopBasic).filter_by(name='老北京涮羊肉').first()
shop.time = "09:00-21:00"
sess.commit()
# 修改后，查看数据是否更新
shop = sess.query(ShopBasic).filter_by(name='老北京涮羊肉').first()
shop.__dict__

# 把营业时间设置为None，模拟数据缺失
shop = sess.query(ShopBasic).filter_by(name='老北京涮羊肉').first()
shop.time = None
sess.commit()

# 删除营业时间缺失的数据
shop = sess.query(ShopBasic).filter_by(time=None).first()
sess.delete(shop)
sess.commit()

shops = sess.query(ShopBasic).all()
for shop in shops:
    print(shop.name)


shops = [
    (311, "老北京涮羊肉", '11:00-21:00', [['周一', '满60减10'], ['周二', '满100减20']]),
    (312, "大龙燚火锅", '10:00-22:00', [['周一', '满60减10'], ['周二', '满100减20']]),
    (313, "一尊皇牛", '00:00-24:00', [['周一', '满80减10'], ['周二', '满100减10']]),
]

for shop in shops:
    shop_id = shop[0]
    shop_ = sess.query(ShopBasic).filter_by(id=shop_id).first()
    coupons = shop[3]
    coupon_ls = []
    for c in coupons:
        day = c[0]
        coupon = c[1]
        print(day, coupon)
        new = ShopCoupon(
            shop_id=shop_.id,
            day=day,
            coupon=coupon,
        )
        coupon_ls.append(new)

    sess.add_all(coupon_ls)
    sess.commit()

coupons = sess.query(ShopCoupon).all()
for coupon in coupons:
    print(coupon.shop_id)


import os
import pandas as pd
from sqlalchemy import create_engine

db_file = r'E:\pythonProjects\cluebearpython\chapter9\data'
engine = create_engine('sqlite:///{}'.format(os.path.join(db_file, 'data.db')), encoding='utf8')
df = pd.read_sql('basic', engine)
df


sess.close()

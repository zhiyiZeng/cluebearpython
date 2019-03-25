import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey


db_file = r'E:\pythonProjects\cluebearpython\chapter11\data'
engine = create_engine('sqlite:///{}'.format(os.path.join(db_file, 'data.db')), encoding='utf8')
DBSession = sessionmaker(bind=engine)
sess = DBSession()


Base = declarative_base()
class Student(Base):
    # 表的名字:
    __tablename__ = 'student'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    stu_id = Column(Integer, nullable=True)
    name = Column(String(20))
    age = Column(Integer)
    enroll = Column(Integer, nullable=True)


class Course(Base):
    # 表的名字:
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 添加外键
    stu_id = Column(Integer, ForeignKey('student.stu_id'))
    day = Column(String(5))
    course = Column(String(10))

Base.metadata.create_all(engine)

students = [
    (2014114153, '张三', 17, 2018),
    (2014114154, '李四', 18, 2017),
    (2014114155, '王五', 16, 2016),
]


news = []
for stu in students:
    new = Student(stu_id=stu[0], name=stu[1], age=stu[2], enroll=stu[3])
    news.append(new)

sess.add_all(news)
sess.commit()

students = sess.query(Student).all()
for stu in students:
    print(stu.stu_id, stu.name, stu.age, stu.enroll)

students = sess.query(Student).filter_by(name='张三').all()
students[0].__dict__
students = sess.query(Student).order_by('enroll').all()
for stu in students:
    print(stu.stu_id, stu.name, stu.age, stu.enroll)

student = sess.query(Student).filter_by(name='张三').first()
student.enroll = 2017
sess.commit()

student = sess.query(Student).filter_by(name='张三').first()
student.stu_id = None
student.enroll = None
sess.commit()

student = sess.query(Student).filter_by(name='张三').first()
student.__dict__
sess.delete(student)
sess.commit()

students = sess.query(Student).all()
for stu in students:
    print(stu.name)



infos = [
    (2014114153, '张三', 17, 2018, [['礼拜一', '高等数学'], ['礼拜二', '大学英语']]),
    (2014114154, '李四', 18, 2017, [['礼拜一', '大学计算机'], ['礼拜二', '大学物理']]),
    (2014114155, '王五', 16, 2016, [['礼拜一', '国学经典'], ['礼拜二', '创业学']]),
]

students = sess.query(Student).all()
for info in infos:
    stu_id = info[0]
    stu = sess.query(Student).filter_by(stu_id=stu_id).first()
    courses = info[4]
    course_ls = []
    for c in courses:
        day = c[0]
        course = c[1]
        print(day, course)
        new = Course(
            stu_id=stu.stu_id,
            day=day,
            course=course,
        )
        course_ls.append(new)

    sess.add_all(course_ls)
    sess.commit()
courses = sess.query(Course).all()
for course in courses:
    print(course.stu_id)


import os
import pandas as pd
from sqlalchemy import create_engine

db_file = r'E:\pythonProjects\cluebearpython\chapter11\data'
engine = create_engine('sqlite:///{}'.format(os.path.join(db_file, 'data.db')), encoding='utf8')
df = pd.read_sql('student', engine)
df


sess.close()

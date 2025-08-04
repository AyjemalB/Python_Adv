from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, aliased
from sqlalchemy import func

# Создаем экземпляр движка для подключения к SQLite
engine = create_engine('sqlite:///my_database.db')

# Создание базового класса
Base = declarative_base()

# Модель категории
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    products = relationship("Product", backref="category")

# Модель продукта
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

# Создание всех таблиц
Base.metadata.create_all(engine)

# Создаем класс Session, который будет использоваться для взаимодействия с БД
Session = sessionmaker(bind=engine)

# Создаем экземпляр сессии
session = Session()

#--------------------------------------------------------------------------------------------------------#

"""
Задача 1: Наполнение данными
Добавьте в базу данных следующие категории и продукты
    1. Добавление категорий: Добавьте в таблицу categories следующие категории:
        - Название: "Электроника", Описание: "Гаджеты и устройства."
        - Название: "Книги", Описание: "Печатные книги и электронные книги."
        - Название: "Одежда", Описание: "Одежда для мужчин и женщин."
    2. Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый 
продукт связан с соответствующей категорией:
        - Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
        - Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
        - Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
        - Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
        - Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда
"""
# Добавление категорий
category1 = Category(name="Электроника", description="Гаджеты и устройства.")
category2 = Category(name="Книги", description="Печатные книги и электронные книги.")
category3 = Category(name="Одежда", description="Одежда для мужчин и женщин.")

# Добавляем в сессию и сохраняем
session.add_all([category1, category2, category3])
session.commit()

# Добавление продуктов
product1 = Product(name="Смартфон", price=299.99, in_stock=True, category=category1)
product2 = Product(name="Ноутбук", price=499.99, in_stock=True, category=category1)
product3 = Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=category2)
product4 = Product(name="Джинсы", price=40.50, in_stock=True, category=category3)
product5 = Product(name="Футболка", price=20.00, in_stock=True, category=category3)

# Добавляем в сессию и сохраняем
session.add_all([product1, product2, product3, product4, product5])
session.commit()

#-----------------------------------------------------------------------------------------------------------#
"""
Задача 2: Чтение данных
Извлеките все записи из таблицы categories. Для каждой категории 
извлеките и выведите все связанные с ней продукты, включая их названия и цены.
"""
# Получаем все категории с их продуктами
categories = session.query(Category).all()

#Выводим данные
for category in categories:
    print(f"Категория: {category.name}")
    print(f"Описание: {category.description}")
    print("Продукты:")
    for product in category.products:
        print(f" - {product.name}, Цена: {product.price}")
    print("-" * 40)

#-----------------------------------------------------------------------------------------------------------#
"""
Задача 3: Обновление данных
Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.
"""
#Поиск первого продукта с названием "Смартфон"
smartphone = session.query(Product).filter_by(name="Смартфон").first()

#Обновление цены, если продукт найден
if smartphone:
    smartphone.price = 349.99
    session.commit()
    print("Цена смартфона успешно обновлена.")
else:
    print("Продукт 'Смартфон' не найден.")

#-----------------------------------------------------------------------------------------------------------#
"""
Задача 4: Агрегация и группировка
Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.
"""
#Группировка и подсчет количества продуктов по категориям
category_counts = session.query(
    Category.name,
    func.count(Product.id).label("product_count")
).join(Product).group_by(Category.id).all()

#Вывод результатов
for name, count in category_counts:
    print(f"Категория: {name}, Количество продуктов: {count}")

#-----------------------------------------------------------------------------------------------------------#
"""
Задача 5: Группировка с фильтрацией
Отфильтруйте и выведите только те категории, в которых более одного продукта.
"""
#Группировка + фильтрация
category_counts = session.query(
    Category.name,
    func.count(Product.id).label("product_count")
).join(Product).group_by(Category.id).having(func.count(Product.id) > 1).all()

#Вывод результата
for name, count in category_counts:
    print(f"Категория: {name}, Количество продуктов: {count}")
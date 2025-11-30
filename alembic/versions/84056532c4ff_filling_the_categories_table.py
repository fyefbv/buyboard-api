import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '84056532c4ff'
down_revision: Union[str, Sequence[str], None] = '9a0e4ac94306'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    categories_table = sa.table(
        'categories',
        sa.column('id', UUID),
        sa.column('name_translations', JSONB)
    )

    translated_categories = [
        {"en": "Electronics", "ru": "Электроника"},
        {"en": "Computers", "ru": "Компьютеры"},
        {"en": "Smartphones", "ru": "Смартфоны"},
        {"en": "Tablets", "ru": "Планшеты"},
        {"en": "Laptops", "ru": "Ноутбуки"},
        {"en": "Computer Components", "ru": "Комплектующие для ПК"},
        {"en": "Audio Equipment", "ru": "Аудиотехника"},
        {"en": "Photo & Video", "ru": "Фото и видео"},
        {"en": "Gaming Consoles", "ru": "Игровые приставки"},
        {"en": "Smart Home", "ru": "Умный дом"},
        {"en": "Home Appliances", "ru": "Бытовая техника"},
        {"en": "Kitchen Appliances", "ru": "Кухонная техника"},
        {"en": "Furniture", "ru": "Мебель"},
        {"en": "Home Decor", "ru": "Декор для дома"},
        {"en": "Real Estate", "ru": "Недвижимость"},
        {"en": "Apartments", "ru": "Квартиры"},
        {"en": "Houses", "ru": "Дома"},
        {"en": "Commercial Property", "ru": "Коммерческая недвижимость"},
        {"en": "Cars", "ru": "Автомобили"},
        {"en": "Motorcycles", "ru": "Мотоциклы"},
        {"en": "Bicycles", "ru": "Велосипеды"},
        {"en": "Auto Parts", "ru": "Автозапчасти"},
        {"en": "Tires & Wheels", "ru": "Шины и диски"},
        {"en": "Car Audio", "ru": "Автозвук"},
        {"en": "Clothing", "ru": "Одежда"},
        {"en": "Shoes", "ru": "Обувь"},
        {"en": "Accessories", "ru": "Аксессуары"},
        {"en": "Jewelry", "ru": "Украшения"},
        {"en": "Watches", "ru": "Часы"},
        {"en": "Beauty & Health", "ru": "Красота и здоровье"},
        {"en": "Cosmetics", "ru": "Косметика"},
        {"en": "Perfumes", "ru": "Парфюмерия"},
        {"en": "Sports", "ru": "Спорт"},
        {"en": "Fitness Equipment", "ru": "Фитнес оборудование"},
        {"en": "Outdoor Sports", "ru": "Активный отдых"},
        {"en": "Winter Sports", "ru": "Зимние виды спорта"},
        {"en": "Hobbies", "ru": "Хобби"},
        {"en": "Books", "ru": "Книги"},
        {"en": "Music", "ru": "Музыка"},
        {"en": "Musical Instruments", "ru": "Музыкальные инструменты"},
        {"en": "Movies", "ru": "Фильмы"},
        {"en": "Games", "ru": "Игры"},
        {"en": "Board Games", "ru": "Настольные игры"},
        {"en": "Collectibles", "ru": "Коллекционные предметы"},
        {"en": "Antiques", "ru": "Антиквариат"},
        {"en": "Tools", "ru": "Инструменты"},
        {"en": "Construction", "ru": "Строительство"},
        {"en": "Building Materials", "ru": "Строительные материалы"},
        {"en": "Garden", "ru": "Сад и огород"},
        {"en": "Plants", "ru": "Растения"},
        {"en": "Children's Products", "ru": "Детские товары"},
        {"en": "Toys", "ru": "Игрушки"},
        {"en": "Baby Products", "ru": "Товары для малышей"},
        {"en": "Pets", "ru": "Животные"},
        {"en": "Pet Supplies", "ru": "Товары для животных"},
        {"en": "Food", "ru": "Продукты питания"},
        {"en": "Services", "ru": "Услуги"},
        {"en": "Repair Services", "ru": "Ремонтные услуги"},
        {"en": "Beauty Services", "ru": "Красота и уход"},
        {"en": "Transport Services", "ru": "Транспортные услуги"},
        {"en": "Jobs", "ru": "Работа"},
        {"en": "Business", "ru": "Бизнес"},
        {"en": "Office Equipment", "ru": "Офисная техника"},
        {"en": "Education", "ru": "Образование"},
        {"en": "Tickets", "ru": "Билеты"},
        {"en": "Travel", "ru": "Путешествия"},
        {"en": "Other", "ru": "Другое"}
    ]

    op.bulk_insert(
        categories_table,
        [{"id": str(uuid.uuid4()), "name_translations": category} for category in translated_categories]
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM categories")

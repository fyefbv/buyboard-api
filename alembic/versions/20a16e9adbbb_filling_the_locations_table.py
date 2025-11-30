import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '20a16e9adbbb'
down_revision: Union[str, Sequence[str], None] = '30bafab8dd03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    locations_table = sa.table(
        'locations',
        sa.column('id', UUID),
        sa.column('name_translations', JSONB)
    )

    translated_locations = [
        {"en": "Moscow", "ru": "Москва"},
        {"en": "Saint Petersburg", "ru": "Санкт-Петербург"},
        {"en": "Novosibirsk", "ru": "Новосибирск"},
        {"en": "Yekaterinburg", "ru": "Екатеринбург"},
        {"en": "Kazan", "ru": "Казань"},
        {"en": "Nizhny Novgorod", "ru": "Нижний Новгород"},
        {"en": "Chelyabinsk", "ru": "Челябинск"},
        {"en": "Samara", "ru": "Самара"},
        {"en": "Omsk", "ru": "Омск"},
        {"en": "Rostov-on-Don", "ru": "Ростов-на-Дону"},
        {"en": "Ufa", "ru": "Уфа"},
        {"en": "Krasnoyarsk", "ru": "Красноярск"},
        {"en": "Voronezh", "ru": "Воронеж"},
        {"en": "Perm", "ru": "Пермь"},
        {"en": "Volgograd", "ru": "Волгоград"},
        {"en": "Krasnodar", "ru": "Краснодар"},
        {"en": "Saratov", "ru": "Саратов"},
        {"en": "Tyumen", "ru": "Тюмень"},
        {"en": "Tolyatti", "ru": "Тольятти"},
        {"en": "Izhevsk", "ru": "Ижевск"},
        {"en": "Barnaul", "ru": "Барнаул"},
        {"en": "Ulyanovsk", "ru": "Ульяновск"},
        {"en": "Irkutsk", "ru": "Иркутск"},
        {"en": "Khabarovsk", "ru": "Хабаровск"},
        {"en": "Yaroslavl", "ru": "Ярославль"},
        {"en": "Vladivostok", "ru": "Владивосток"},
        {"en": "Makhachkala", "ru": "Махачкала"},
        {"en": "Tomsk", "ru": "Томск"},
        {"en": "Orenburg", "ru": "Оренбург"},
        {"en": "Kemerovo", "ru": "Кемерово"},
        {"en": "Novokuznetsk", "ru": "Новокузнецк"},
        {"en": "Ryazan", "ru": "Рязань"},
        {"en": "Astrakhan", "ru": "Астрахань"},
        {"en": "Naberezhnye Chelny", "ru": "Набережные Челны"},
        {"en": "Penza", "ru": "Пенза"},
        {"en": "Lipetsk", "ru": "Липецк"},
        {"en": "Kirov", "ru": "Киров"},
        {"en": "Cheboksary", "ru": "Чебоксары"},
        {"en": "Tula", "ru": "Тула"},
        {"en": "Kaliningrad", "ru": "Калининград"},
        {"en": "Balashikha", "ru": "Балашиха"},
        {"en": "Kursk", "ru": "Курск"},
        {"en": "Stavropol", "ru": "Ставрополь"},
        {"en": "Ulan-Ude", "ru": "Улан-Удэ"},
        {"en": "Tver", "ru": "Тверь"},
        {"en": "Magnitogorsk", "ru": "Магнитогорск"},
        {"en": "Sochi", "ru": "Сочи"},
        {"en": "Ivanovo", "ru": "Иваново"},
        {"en": "Bryansk", "ru": "Брянск"},
        {"en": "Belgorod", "ru": "Белгород"},
        {"en": "Surgut", "ru": "Сургут"},
        {"en": "Vladimir", "ru": "Владимир"},
        {"en": "Nizhny Tagil", "ru": "Нижний Тагил"},
        {"en": "Arkhangelsk", "ru": "Архангельск"},
        {"en": "Chita", "ru": "Чита"},
        {"en": "Kaluga", "ru": "Калуга"},
        {"en": "Smolensk", "ru": "Смоленск"},
        {"en": "Volzhsky", "ru": "Волжский"},
        {"en": "Kurgan", "ru": "Курган"},
        {"en": "Cherepovets", "ru": "Череповец"},
        {"en": "Vladikavkaz", "ru": "Владикавказ"},
        {"en": "Murmansk", "ru": "Мурманск"},
        {"en": "Saransk", "ru": "Саранск"},
        {"en": "Tambov", "ru": "Тамбов"},
        {"en": "Yoshkar-Ola", "ru": "Йошкар-Ола"},
        {"en": "Nizhnevartovsk", "ru": "Нижневартовск"},
        {"en": "Kostroma", "ru": "Кострома"},
        {"en": "Novorossiysk", "ru": "Новороссийск"},
        {"en": "Komsomolsk-on-Amur", "ru": "Комсомольск-на-Амуре"},
        {"en": "Petrozavodsk", "ru": "Петрозаводск"},
        {"en": "Taganrog", "ru": "Таганрог"},
        {"en": "Nalchik", "ru": "Нальчик"},
        {"en": "Syktyvkar", "ru": "Сыктывкар"},
        {"en": "Khimki", "ru": "Химки"},
        {"en": "Shakhty", "ru": "Шахты"},
        {"en": "Bratsk", "ru": "Братск"},
        {"en": "Noginsk", "ru": "Ногинск"},
        {"en": "Dzerzhinsk", "ru": "Дзержинск"},
        {"en": "Orsk", "ru": "Орск"},
        {"en": "Angarsk", "ru": "Ангарск"},
        {"en": "Grozny", "ru": "Грозный"},
        {"en": "Sterlitamak", "ru": "Стерлитамак"},
        {"en": "Yuzhno-Sakhalinsk", "ru": "Южно-Сахалинск"},
        {"en": "Volgodonsk", "ru": "Волгодонск"},
        {"en": "Abakan", "ru": "Абакан"},
        {"en": "Maykop", "ru": "Майкоп"},
        {"en": "Miass", "ru": "Миасс"},
        {"en": "Novocherkassk", "ru": "Новочеркасск"},
        {"en": "Pyatigorsk", "ru": "Пятигорск"},
        {"en": "Rubtsovsk", "ru": "Рубцовск"},
        {"en": "Berezniki", "ru": "Березники"},
        {"en": "Salavat", "ru": "Салават"},
        {"en": "Mytishchi", "ru": "Мытищи"},
        {"en": "Korolyov", "ru": "Королёв"},
        {"en": "Kolomna", "ru": "Коломна"},
        {"en": "Elektrostal", "ru": "Электросталь"},
        {"en": "Odintsovo", "ru": "Одинцово"},
        {"en": "Kopeysk", "ru": "Копейск"},
        {"en": "Zhukovsky", "ru": "Жуковский"},
        {"en": "Almetyevsk", "ru": "Альметьевск"},
        {"en": "Pervouralsk", "ru": "Первоуральск"},
        {"en": "Krasnogorsk", "ru": "Красногорск"},
        {"en": "Serpukhov", "ru": "Серпухов"}
    ]

    op.bulk_insert(
        locations_table,
        [{"id": str(uuid.uuid4()), "name_translations": location} for location in translated_locations]
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM locations")

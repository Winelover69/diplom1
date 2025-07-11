# tests/test_burger.py

import pytest
from unittest.mock import Mock
from src.burger import Burger
from src.ingredient import Ingredient  # Импортируем Ingredient для типажей и моков


# --- Мокирование Ingredient ---
# Вместо реальных объектов Ingredient мы будем создавать их моки.
# Это позволяет нам контролировать возвращаемые значения методов get_type(), get_name(), get_price().

@pytest.fixture
def mock_bun():
    """Фикстура для мока булки."""
    mock = Mock(spec=Ingredient)
    mock.get_type.return_value = "bun"
    mock.get_name.return_value = "black bun"
    mock.get_price.return_value = 100
    return mock


@pytest.fixture
def mock_sauce():
    """Фикстура для мока соуса."""
    mock = Mock(spec=Ingredient)
    mock.get_type.return_value = "sauce"
    mock.get_name.return_value = "hot sauce"
    mock.get_price.return_value = 50
    return mock


@pytest.fixture
def mock_filling():
    """Фикстура для мока начинки."""
    mock = Mock(spec=Ingredient)
    mock.get_type.return_value = "filling"
    mock.get_name.return_value = "cutlet"
    mock.get_price.return_value = 150
    return mock


# --- Тесты класса Burger ---

class TestBurger:

    def test_set_buns(self, mock_bun):
        """Проверяет, что метод set_buns корректно устанавливает две булки."""
        burger = Burger()
        burger.set_buns(mock_bun)
        assert len(burger.buns) == 2
        assert burger.buns[0] == mock_bun
        assert burger.buns[1] == mock_bun

    def test_add_ingredient(self, mock_sauce, mock_filling):
        """Проверяет, что метод add_ingredient корректно добавляет ингредиент."""
        burger = Burger()
        burger.add_ingredient(mock_sauce)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_sauce
        burger.add_ingredient(mock_filling)
        assert len(burger.ingredients) == 2
        assert burger.ingredients[1] == mock_filling

    def test_remove_ingredient(self, mock_sauce, mock_filling):
        """Проверяет, что метод remove_ingredient корректно удаляет ингредиент по индексу."""
        burger = Burger()
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)

        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_filling

        # Проверка удаления последнего ингредиента
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 0

    @pytest.mark.parametrize("from_index, to_index, expected_order", [
        (0, 1, ["sauce", "filling"]),  # Переместить первый на вторую позицию
        (1, 0, ["filling", "sauce"]),  # Переместить второй на первую позицию
        (0, 0, ["sauce", "filling"])  # Переместить на то же место
    ])
    def test_move_ingredient(self, mock_sauce, mock_filling, from_index, to_index, expected_order):
        """Проверяет, что метод move_ingredient корректно перемещает ингредиенты."""
        burger = Burger()
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)

        # Убедимся, что моки возвращают ожидаемые имена для проверки порядка
        mock_sauce.get_name.return_value = "sauce"
        mock_filling.get_name.return_value = "filling"

        burger.move_ingredient(from_index, to_index)

        # Проверяем порядок ингредиентов по их именам
        actual_order_names = [ing.get_name() for ing in burger.ingredients]
        assert actual_order_names == expected_order

    @pytest.mark.parametrize("bun_price, sauce_price, filling_price, expected_price", [
        (100, 50, 150, 2 * 100 + 50 + 150),  # Булка, соус, начинка
        (0, 0, 0, 0),  # Все цены 0
        (50, 10, 20, 2 * 50 + 10 + 20)  # Другие цены
    ])
    def test_get_price(self, bun_price, sauce_price, filling_price, expected_price):
        """
        Проверяет, что метод get_price корректно рассчитывает общую стоимость бургера.
        Используем параметризацию для различных цен ингредиентов.
        """
        burger = Burger()

        # Мокируем ингредиенты с параметризованными ценами
        mock_bun = Mock(spec=Ingredient)
        mock_bun.get_type.return_value = "bun"
        mock_bun.get_price.return_value = bun_price

        mock_sauce = Mock(spec=Ingredient)
        mock_sauce.get_type.return_value = "sauce"
        mock_sauce.get_price.return_value = sauce_price

        mock_filling = Mock(spec=Ingredient)
        mock_filling.get_type.return_value = "filling"
        mock_filling.get_price.return_value = filling_price

        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)

        assert burger.get_price() == expected_price

    def test_get_price_no_buns(self, mock_sauce, mock_filling):
        """Проверяет, что get_price работает, если булки не установлены."""
        burger = Burger()
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        # Если булок нет, цена должна быть только за ингредиенты
        expected_price = mock_sauce.get_price() + mock_filling.get_price()
        assert burger.get_price() == expected_price

    @pytest.mark.parametrize("bun_name, sauce_name, filling_name, expected_receipt", [
        ("black bun", "hot sauce", "cutlet",
         "(булка black bun)\n(соус hot sauce)\n(котлета cutlet)\n(булка black bun)"),
        ("white bun", "sweet sauce", "chicken cutlet",
         "(булка white bun)\n(соус sweet sauce)\n(котлета chicken cutlet)\n(булка white bun)")
    ])
    def test_get_receipt(self, bun_name, sauce_name, filling_name, expected_receipt):
        """
        Проверяет, что метод get_receipt корректно формирует чек.
        Используем параметризацию для различных имен ингредиентов.
        """
        burger = Burger()

        # Мокируем ингредиенты с параметризованными именами и типами
        mock_bun = Mock(spec=Ingredient)
        mock_bun.get_type.return_value = "bun"
        mock_bun.get_name.return_value = bun_name

        mock_sauce = Mock(spec=Ingredient)
        mock_sauce.get_type.return_value = "sauce"
        mock_sauce.get_name.return_value = sauce_name

        mock_filling = Mock(spec=Ingredient)
        mock_filling.get_type.return_value = "filling"
        mock_filling.get_name.return_value = filling_name

        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)

        assert burger.get_receipt() == expected_receipt

    def test_get_receipt_no_ingredients(self, mock_bun):
        """Проверяет get_receipt для бургера только с булками."""
        burger = Burger()
        burger.set_buns(mock_bun)
        mock_bun.get_name.return_value = "black bun"
        expected_receipt = "(булка black bun)\n(булка black bun)"
        assert burger.get_receipt() == expected_receipt

    def test_get_receipt_no_buns(self, mock_sauce):
        """
        Проверяет, что get_receipt вызывает ошибку, если булки не установлены.
        (Согласно коду, обращение к self.buns[0] без булок вызовет IndexError).
        """
        burger = Burger()
        burger.add_ingredient(mock_sauce)  # Добавляем что-то, чтобы не было совсем пусто
        with pytest.raises(IndexError):
            burger.get_receipt()
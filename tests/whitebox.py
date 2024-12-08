from app.models import MysticBurger

def mystic_burger():
    # Return a MysticBurger instance for testing
    return MysticBurger(
        store="Test Store",
        category="Test Category",
        item="Test Item",
        description="Test Description",
        price=10.0,
        qty=5,
        magic=False
    )
def test_mystic_burger_str(mystic_burger):
    # Test string representation of MysticBurger instance
    expected_str = "Test Store, Test Category, Test Item,Test Description, 10.0, 5, False"
    # Check if string representation matches
    assert str(mystic_burger) == expected_str
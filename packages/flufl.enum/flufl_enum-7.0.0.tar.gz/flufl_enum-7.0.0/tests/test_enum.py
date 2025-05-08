import pytest

from flufl.enum import Enum, IntEnum, EnumValue
from flufl.enum._enum import IntEnumValue
from itertools import combinations
from operator import attrgetter, index

SPACE = ' '


class Colors(Enum):
    red = 1
    green = 2
    blue = 3


class OtherColors(Enum):
    red = 1
    blue = 2
    yellow = 3


class MoreColors(Colors):
    pink = 4
    cyan = 5


ALL_COLORS = ['red', 'green', 'blue']


class Rush(Enum):
    geddy = 'bass'
    alex = 'guitar'
    neil = 'drums'


class Animals(IntEnum):
    ant = 1
    bee = 2
    cat = 3


def test_basic_reprs():
    assert str(Colors.red) == 'Colors.red'
    assert str(Colors.green) == 'Colors.green'
    assert str(Colors.blue) == 'Colors.blue'
    assert str(Colors['red']) == 'Colors.red'
    assert repr(Colors.red) == '<EnumValue: Colors.red [value=1]>'


def test_string_value():
    assert repr(Rush.alex) == '<EnumValue: Rush.alex [value=guitar]>'


def test_factory_single_string():
    Color = Enum('Color', SPACE.join(ALL_COLORS))
    for c in ALL_COLORS:
        assert str(Color[c]) == 'Color.' + c


def test_enum_dir():
    # dir() returns the list of enumeration item names.
    assert sorted(dir(Colors)) == sorted(ALL_COLORS)


def test_enumclass_getitem():
    assert Colors[2] is Colors.green
    assert Colors['red'] is Colors.red
    assert Colors[Colors.red] is Colors.red


def test_iteration():
    # Iteration of Enums preserves the order in which the attributes appear.
    A = Enum('A', dict(a=1, b=2, c=3))
    assert [e.name for e in A] == ['a', 'b', 'c']
    B = Enum('B', dict(c=1, b=2, a=3))
    assert [e.name for e in B] == ['c', 'b', 'a']
    # If iteration sorted over values, this would give a TypeError.
    C = Enum('C', dict(a='7', b=7))
    assert [e.name for e in C] == ['a', 'b']


def test_hashing():
    getvalue = attrgetter('value')
    apples = {}
    apples[Colors.red] = 'red delicious'
    apples[Colors.green] = 'granny smith'
    assert [(c.name, apples[c]) for c in sorted(apples, key=getvalue)] == [
        ('red', 'red delicious'),
        ('green', 'granny smith'),
    ]


def test_value_enum_attributes():
    for i, c in enumerate(ALL_COLORS, 1):
        # enum attribute
        assert Colors[c].enum is Colors
        # name attribute
        assert Colors[c].name == c
        # value attribute
        assert Colors[c].value == i


def test_enum_class_name():
    assert Colors.__name__ == 'Colors'


def test_comparisons():
    r, g, b = Colors.red, Colors.green, Colors.blue
    for c in r, g, b:
        assert c is c
        assert c == c
    for first, second in combinations([r, g, b], 2):
        assert first is not second
        assert first != second

    with pytest.raises(TypeError):
        Colors.red < Colors.blue
    with pytest.raises(TypeError):
        Colors.red <= Colors.blue
    with pytest.raises(TypeError):
        Colors.red > Colors.green
    with pytest.raises(TypeError):
        Colors.green >= Colors.blue


def test_comparison_with_int():
    with pytest.raises(TypeError):
        Colors.red < 3
    with pytest.raises(TypeError):
        Colors.red <= 3
    with pytest.raises(TypeError):
        Colors.blue > 2
    with pytest.raises(TypeError):
        Colors.green >= 1

    assert Colors.green != 2
    assert Colors.blue != 3
    assert Colors.green != 3


def test_comparison_with_other_enum():
    assert OtherColors.red is not Colors.red
    assert OtherColors.red != Colors.red
    assert hash(OtherColors.red) != hash(Colors.red)


def test_subclass():
    assert Colors.red is MoreColors.red
    assert Colors.blue is MoreColors.blue


def test_pickle():
    from .fruit import Fruit
    from pickle import dumps, loads

    assert Fruit.tomato is loads(dumps(Fruit.tomato))


def test_functional_api_single_string():
    animals = Enum('Animals', 'ant bee cat dog')
    assert repr(animals) == '<Animals {ant: 1, bee: 2, cat: 3, dog: 4}>'


def test_functional_api_sequence():
    people = Enum('People', ('anne', 'bart', 'cate', 'dave'))
    assert repr(people) == '<People {anne: 1, bart: 2, cate: 3, dave: 4}>'


def test_functional_api_2_tuples():
    def enumiter():
        start = 1
        while True:
            yield start
            start <<= 1

    flags = Enum('Flags', zip(list('abcdefg'), enumiter()))
    assert (
        repr(flags) == '<Flags {a: 1, b: 2, c: 4, d: 8, e: 16, f: 32, g: 64}>'
    )


def test_functional_api_dict():
    # Note: repr is sorted by attribute name
    bassists = dict(geddy='rush', chris='yes', flea='rhcp', jack='cream')
    assert (
        repr(Enum('Bassists', bassists))
        == '<Bassists {chris: yes, flea: rhcp, geddy: rush, jack: cream}>'
    )


def test_invalid_getitem_arguments():
    # Trying to get an invalid value raises an exception.
    with pytest.raises(KeyError) as exc_info:
        Colors['magenta']
    assert exc_info.value.args == ('magenta',)


def test_no_duplicates():
    with pytest.raises(ValueError) as exc_info:

        class Bad(Enum):
            cartman = 1
            stan = 2
            kyle = 3
            kenny = 3   # Oops!
            butters = 4

    assert (
        str(exc_info.value)
        == "Conflicting enum value '3' for names: 'kenny' and 'kyle'"
    )


def test_no_duplicates_in_subclass():
    with pytest.raises(ValueError) as exc_info:

        class BadMoreColors(Colors):
            yellow = 4
            magenta = 2   # Oops!

    assert (
        str(exc_info.value)
        == "Conflicting enum value '2' for names: 'green' and 'magenta'"
    )


def test_no_duplicates_in_dict():
    with pytest.raises(ValueError) as exc_info:
        Enum('Things', dict(a='yes', b='no', c='maybe', d='yes'))
    assert (
        exc_info.value.args[0]
        == "Conflicting enum value 'yes' for names: 'a' and 'd'"
    )


def test_functional_api_not_all_2_tuples():
    # If 2-tuples are used, all items must be 2-tuples.
    with pytest.raises(ValueError):
        Enum(
            'Animals',
            (
                ('ant', 1),
                ('bee', 2),
                'cat',
                ('dog', 4),
            ),
        )
    with pytest.raises(ValueError):
        Enum(
            'Animals',
            (
                ('ant', 1),
                ('bee', 2),
                ('cat',),
                ('dog', 4),
            ),
        )
    with pytest.raises(ValueError):
        Enum(
            'Animals',
            (
                ('ant', 1),
                ('bee', 2),
                ('cat', 3, 'oops'),
                ('dog', 4),
            ),
        )


def test_functional_api_identifiers():
    # Ensure that the functional API enforces identifiers.
    with pytest.raises(ValueError) as exc_info:
        Enum('Foo', ('1', '2', '3'))
    assert exc_info.value.args[0] == 'non-identifiers: 1 2 3'
    with pytest.raises(ValueError) as exc_info:
        Enum('Foo', (('ant', 1), ('bee', 2), ('3', 'cat')))
    assert exc_info.value.args[0] == 'non-identifiers: 3'


def test_functional_api_identifiers_lp1167052():
    # LP: #1167052
    with pytest.raises(ValueError):
        Enum('X', 'a-1')


def test_functional_api_identifiers_numbers():
    # There was a typo in IDENTIFIER_RE where the range 0-0 was used.
    MyEnum = Enum('X', 'a9')
    assert MyEnum.a9.name == 'a9'


def test_explicit_getattr():
    Fruit = Enum('Fruit', 'apple banana tangerine orange')
    assert getattr(Fruit, 'banana') is Fruit.banana
    assert getattr(Fruit, Fruit.banana.name) is Fruit.banana


def test_issue_17576():
    # http://bugs.python.org/issue17576
    #
    # The problem is that despite the documentation, operator.index() is
    # *not* equivalent to calling obj.__index__() when the object in
    # question is an int subclass.
    # Test that while the actual type returned by operator.index() and
    # obj.__index__() are not the same (because the former returns the
    # subclass instance, but the latter returns the .value attribute) they
    # are equal.
    assert index(Animals.bee) == Animals.bee.__index__()


def test_basic_intenum():
    animal_list = [Animals.ant, Animals.bee, Animals.cat]
    assert animal_list == [1, 2, 3]
    assert [int(a) for a in animal_list] == [1, 2, 3]
    assert list(range(10)[Animals.ant : Animals.cat]) == [1, 2]


def test_int_enums_type():
    # IntEnum() enum values are ints.
    Toppings = IntEnum(
        'Toppings',
        dict(olives=1, onions=2, mushrooms=4, cheese=8, garlic=16).items(),
    )
    assert Toppings.garlic == 16
    assert isinstance(Toppings.mushrooms, int)


def test_intenum_comparisons():
    assert Animals.ant < Animals.bee
    assert Animals.cat > Animals.ant
    assert Animals.ant <= 1.0
    assert Animals.bee == 2

    class Toppings(IntEnum):
        anchovies = 1
        black_olives = 2

    assert Animals.bee == Toppings.black_olives


def test_intenum_iteration():
    # Iteration over IntEnums is by value.
    A = IntEnum('A', 'a b c')
    assert list(v.name for v in A) == ['a', 'b', 'c']
    B = IntEnum('B', 'c b a')
    # Iteration over this enum is different than if it were an Enum.
    assert list(v.name for v in B) == ['c', 'b', 'a']


def test_conflicting_factories():
    # An enum extension cannot have a different value factory.
    class First(Enum):
        __value_factory__ = EnumValue
        red = 1
        green = 2
        blue = 3

    with pytest.raises(TypeError):
        class Second(First):
            __value_factory__ = IntEnumValue
            red = 1
            green = 2
            blue = 3


def test_weird_getitem():
    # If we try to get an enum item with an argument that pretends to be an
    # item, but really isn't, we'll get a KeyError.
    class Balls(Enum):
        foot = 1
        base = 2
        golf = 3

    class NotAnEnumItem:
        value = 99

    with pytest.raises(KeyError):
        Balls[NotAnEnumItem()]


def test_make_with_inconsistent_values():
    # Passing a dictionary into the functional API requires that all values be
    # of the same type.
    with pytest.raises(ValueError):
        Enum('Animal', ('ant', 7))

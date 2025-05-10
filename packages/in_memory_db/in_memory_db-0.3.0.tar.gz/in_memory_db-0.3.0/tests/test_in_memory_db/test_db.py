from pytest import fixture

from in_memory_db.db import InMemoryDb


type Db = InMemoryDb[str]


@fixture
def db() -> Db:
    return InMemoryDb[str]()


@fixture
def db_with_abc() -> Db:
    return InMemoryDb(["a", "b", "c"])


def test_insert(db: Db) -> None:
    db.insert("x")

    assert list(db) == ["x"]


def test_extend(db: Db) -> None:
    db.extend("abc")

    assert list(db) == ["a", "b", "c"]


def test_select_one_ok(db_with_abc: Db) -> None:
    value = db_with_abc.select_one(lambda it: it == "b")

    assert value == "b"


def test_select_many_ok(db_with_abc: Db) -> None:
    values = db_with_abc.select_many(lambda it: it in "bc")

    assert values == ("b", "c")


def test_select_one_no_value(db_with_abc: Db) -> None:
    value = db_with_abc.select_one(lambda it: it == "x")

    assert value is None


def test_select_many_no_values(db_with_abc: Db) -> None:
    values = db_with_abc.select_many(lambda it: it in "xyz")

    assert values == tuple()


def test_empty_subset_iter(db_with_abc: Db) -> None:
    values = tuple(db_with_abc.subset(int))

    assert values == tuple()


def test_empty_subset_bool(db_with_abc: Db) -> None:
    assert not db_with_abc.subset(int)


def test_empty_subset_len(db_with_abc: Db) -> None:
    assert len(db_with_abc.subset(int)) == 0

import pytest
import pytest_asyncio

# internal imports
from easydict_nicegui.backends.sqlite_backend import search_async, SQLiteBackend
from easydict_nicegui.backends.backend import Result

# type anotations
adb: SQLiteBackend


@pytest_asyncio.fixture
async def adb(tmp_path):
    file_db = tmp_path / "test.db"
    file_db.touch()
    async_db = SQLiteBackend(file_db)
    await async_db.db_init()
    try:
        yield async_db
    finally:
        await async_db.conn.close()


@pytest.fixture
def dummy_data():
    return """
test_eng	test_cze	note	special	author
eng	cze	note	special	author
english	czech	notes	specials	authors
    """.strip()


@pytest.fixture
def dummy_file(tmp_path, dummy_data):
    file = tmp_path / "test.db"
    file.write_text(dummy_data)
    return file


async def test_prepare_db(adb):
    table_name = "test"
    sql = (
        f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?",
        [f"{table_name}"],
    )

    async with adb.conn.execute(*sql) as cursor:
        results = await cursor.fetchall()  # result format is here [(0,)]
        assert results[0][0] == 0  # should find 0 match, table wasn't created yet

    await adb.prepare_db(table_name)  # create table

    async with adb.conn.execute(*sql) as cursor:
        results = await cursor.fetchall()
        assert results[0][0] == 1  # should find 1 match


async def test_fill_db(adb, dummy_file, dummy_data):
    await adb.prepare_db("eng_cze")  # create table
    await adb.fill_db(dummy_file)  # fill table with dummy data from dummy file
    sql = "SELECT * FROM eng_cze"  # get all data from table
    dummy_data = dummy_data.split("\n")  # split dummy data by new line
    dummy_data = [
        tuple(row.split("\t")) for row in dummy_data
    ]  # every line is now tuple; originally each element was separated by a tab
    async with adb.conn.execute(sql) as cursor:
        index = 0
        async for row in cursor:  # one row is tuple of columns
            assert row == dummy_data[index]
            index += 1


async def test_search_in_db(adb, dummy_file):
    await adb.prepare_db("eng_cze")  # create table

    search = adb.search_in_db(word="test", lang="eng", search_type="fulltext")
    async for x in search:
        assert False  # this will never run if no results are found

    await adb.fill_db(dummy_file)  # fill table with dummy data from dummy file
    # and try search again
    async for result in adb.search_in_db(
        word="test", lang="eng", search_type="fulltext"
    ):
        assert result  # this time we should have some results
        assert isinstance(result, Result)  # and result should be correct type


async def test_search_in_db_with_all_search_types(adb, dummy_file):
    await adb.prepare_db("eng_cze")  # create table
    await adb.fill_db(dummy_file)  # fill table with dummy data from dummy file
    # test fulltext search
    async for result in adb.search_in_db(
        word="test", lang="eng", search_type="fulltext"
    ):
        assert result.eng == "test_eng"
    # test first_chars search
    async for result in adb.search_in_db(
        word="eng", lang="eng", search_type="first_chars"
    ):
        assert "eng" in result.eng
    # test whole_word search
    async for result in adb.search_in_db(
        word="english", lang="eng", search_type="whole_word"
    ):
        assert result.eng == "english"
    # test bad type os search_type parameter
    with pytest.raises(ValueError, match="Unknown search_type argument."):
        async for result in adb.search_in_db(
            word="ehm", lang="eng", search_type="unknown"
        ):
            assert False  # this will never run if no results are found

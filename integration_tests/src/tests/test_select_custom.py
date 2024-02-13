from integration_tests.src.settings import processing_connect, logger


def test_get_one_result():
    sql = "SELECT id FROM tabl_name limit 1"
    logger.info("sql > {}".format(sql))

    result = processing_connect.get_one_result(sql)
    logger.info("sql < {}".format(result))

    assert isinstance(result, int)


def test_get_list_result():
    sql = "SELECT * FROM tabl_name limit 2"
    logger.info("sql > {}".format(sql))

    result = processing_connect.get_list_result(sql)
    logger.info("sql < {}".format(result))

    assert isinstance(result[0][0], int)


def test_get_dict_result():
    sql = "SELECT * FROM tabl_name limit 2"
    logger.info("sql > {}".format(sql))

    result = processing_connect.get_dict_result(sql)
    logger.info("sql < {}".format(result))

    assert isinstance(result[0]["id"], int)

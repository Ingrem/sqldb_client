from integration_tests.src.settings import processing_connect, logger


def test_delete():
    sql = "delete from tabl_name where id = -100000"
    logger.info("sql > {}".format(sql))

    processing_connect.session.execute(sql)

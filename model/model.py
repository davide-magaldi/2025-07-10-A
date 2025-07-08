from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getDateRange(self):
        return DAO.getDateRange()
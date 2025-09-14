from database.DB_connect import DBConnect
from model.products import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select category_name from categories c"

        cursor.execute(query)

        for row in cursor:
            results.append(row["category_name"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodes(cat):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = '''select p.* from products p 
                    join categories c 
                    on p.category_id = c.category_id 
                    where c.category_name = %s'''

        cursor.execute(query, (cat,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(cat, first, last):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor()
        query = '''select tab1.product_id, tab2.product_id, (n1+n2) as sum from ((select oi.* , count(*) as n1 from products p 
                    join categories c 
                    on p.category_id = c.category_id 
                    join order_items oi 
                    on p.product_id = oi.product_id 
                    join orders o 
                    on oi.order_id = o.order_id 
                    where c.category_name = %s and o.order_date between %s and %s
                    group by product_id ) tab1
                    join (select oi.* , count(*) as n2 from products p 
                    join categories c 
                    on p.category_id = c.category_id 
                    join order_items oi 
                    on p.product_id = oi.product_id 
                    join orders o 
                    on oi.order_id = o.order_id 
                    where c.category_name = %s and o.order_date between %s and %s
                    group by product_id) tab2
                    on tab1.product_id <> tab2.product_id)
                    where n1 >= n2
                    order by sum desc'''

        cursor.execute(query, (cat, first, last, cat, first, last))

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

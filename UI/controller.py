import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.start = None
        self.end = None

    def handleCreaGrafo(self, e):
        cat = self._view._ddcategory.value
        first = self._view._dp1.value
        last = self._view._dp2.value
        if cat is None or cat == "" or first is None or first == "" or last is None or last == "":
            self._view.create_alert("Selezionare una categoria e le date!")
            return
        self._model.buildGraph(cat, first, last)
        self.fillDDStartp()
        self.fillDDEndp()
        self._view._btnBestProdotti.disabled = False
        self._view._btnCercaCammino.disabled = False
        nnodes, nedges = self._model.getInfoGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Date selzionate:"))
        self._view.txt_result.controls.append(ft.Text(f"Start date: {first}"))
        self._view.txt_result.controls.append(ft.Text(f"End date: {last}"))
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato, con {nnodes} nodi e {nedges} archi"))

        self._view.update_page()

    def handleBestProdotti(self, e):
        best = self._model.getBestProducts()
        self._view.txt_result.controls.append(ft.Text("I cinque prodotti più venduti sono: "))
        for i in best:
            self._view.txt_result.controls.append(ft.Text(f"{i[0].product_name} with score {i[1]}"))
        self._view.update_page()

    def fillDDStartp(self):
        self._view._ddProdStart.options.clear()
        for n in self._model.graph.nodes:
            self._view._ddProdStart.options.append(ft.dropdown.Option(text=n.product_name, data=n, on_click=self.read_data))

    def read_data(self, e):
        self.start = e.control.data

    def fillDDEndp(self):
        self._view._ddProdEnd.options.clear()
        for n in self._model.graph.nodes:
            self._view._ddProdEnd.options.append(ft.dropdown.Option(text=n.product_name, data=n, on_click=self.read_data2))

    def read_data2(self, e):
        self.end = e.control.data

    def handleCercaCammino(self, e):
        lun = self._view._txtInLun.value
        if lun == "" or lun is None or self.start is None or self.end is None:
            self._view.create_alert("Selezionare i nodi e la lunghezza desiderata!")
            return
        try:
            lun = int(lun)
        except ValueError:
            self._view.create_alert("La lunghezza deve essere un intero")
            return
        self._view.txt_result.controls.clear()
        path, score = self._model.getBestPath(lun, self.start, self.end)
        self._view.txt_result.controls.append(ft.Text(f"Identificato un cammino ottimo con score {score}: "))
        for n in path:
            self._view.txt_result.controls.append(ft.Text(n.product_name))
        self._view.update_page()





    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)

    def fillDDCategory(self):
        cat = self._model.getCategories()
        for c in cat:
            self._view._ddcategory.options.append(ft.dropdown.Option(c))

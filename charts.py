from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtChart import *
from PyQt5.QtGui import QPainter, QPen, QFont, QBrush, QColor

import login_query


class Chart_Window(QWidget):

    def __init__(self, username, password, year):
        super().__init__()
        if year == "all":
            self.all_years(username, password)
        else:
            self.one_year(username, password, year)

    def one_year(self, username, password, year):
        result_oneYear = login_query.connection.login_chart_oneYear(self, username, password, year)
        # create barseries
        set_tkf = QBarSet("TAEKWON-DO")
        set_fenc= QBarSet("ΞΙΦΑΣΚΙΑ")
        set_oplo = QBarSet("ΟΠΛΟΜΑΧΙΑ")
        set_spends = QBarSet("ΕΞΟΔΑ")
        for i in range(len(result_oneYear[0])):  #για καθε μηνα που εχει στην πρωτη εσωτερικη λιστα
            if result_oneYear[1][i][0] is None:
                tkd= 0
            else:
                tkd = result_oneYear[1][i][0]
            set_tkf.append(tkd)
            if result_oneYear[1][i][1] is None:
                fenc= 0
            else:
                fenc = result_oneYear[1][i][1]
            set_fenc.append(fenc)
            if result_oneYear[1][i][2] is None:
                oplo= 0
            else:
                oplo = result_oneYear[1][i][2]
            set_oplo.append(oplo)
            if result_oneYear[1][i][3] is None:
                spen= 0
            else:
                spen = result_oneYear[1][i][3]
            set_spends.append(spen)
        # we want to create percent bar series
        series = QBarSeries()
        series.append(set_tkf)
        series.append(set_fenc)
        series.append(set_oplo)
        series.append(set_spends)

        # create chart and add the series in the chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Μηνιαία Στατιστικά ανά Έτος")
        chart.setAnimationOptions(QChart.SeriesAnimations())
        chart.setTheme(QChart.ChartThemeBrownSand)

        # create axis for the chart
        #categories = ["Ιαν", "Φεβρ", "Μαρτ", "Απρ", "Μαι", "Ιουν", "Ιουλ", "Αυγ", "Σεπτ", "Οκτ", "Νοεμ", "Δεκ"]
        categories = result_oneYear[0]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        # create chartview and add the chart in the chartview
        chartview = QChartView(chart)

        vbox = QVBoxLayout()
        vbox.addWidget(chartview)
        self.setLayout(vbox)

    def all_years(self, username, password):
        results_eco = login_query.connection.login_chart_year_all(self, username, password)
        set0 = QBarSet("Έτη")
        series = QBarSeries()
        set0.append(results_eco[1])
        series.append(set0)
        categories = results_eco[0]
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Ετήσια Στατιστικά")

        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeBrownSand)
        chart.setBackgroundBrush(QBrush(QColor("transparent")))

        #create axis for the chart

        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        #create chartview and add the chart in the chartview
        chartview = QChartView(chart)

        vbox = QVBoxLayout()
        vbox.addWidget(chartview)
        self.setLayout(vbox)

#
# App = QApplication(sys.argv)
# window = ChartDesign()
# window.show()
# sys.exit(App.exec())
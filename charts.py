from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtChart import *
from PyQt5.QtGui import QPainter, QPen, QFont, QBrush, QColor

import login_query


class Chart_Window(QWidget):

    def all_years(self, year):
        # #create barseries
        if year == "all":
        # set0 = QBarSet("TAEKWON-DO")
        # set1 = QBarSet("FENCING")
        # set2 = QBarSet("OPLOMAXIA")
            results_eco = login_query.connection.login_chart_year_all(self,"axion", "h6945441201")


        # for item in results_eco[0]:
        #     QBarSet(str(item))

        set0 = QBarSet("Έτη")
        series = QBarSeries()
        set0.append(results_eco[1])
        series.append(set0)
        # for item in results_eco[1]:
        #     series.append(str(item))
        categories = results_eco[0]
        # #insert data to the barseries
        # set0.append([4,5,6,7,8,2,1,12,33,12,43,5])
        # set1.append([4,5,6,7,8,2,1,12,33,12,43,5])
        # set2.append([4,5,6,7,8,2,1,12,33,12,43,5])

        #we want to create percent bar series
        # series = QBarSeries()
        # series.append(set0)
        # series.append(set1)
        # series.append(set2)

        #create chart and add the series in the chart
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
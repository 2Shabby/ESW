from django.shortcuts import render
from django.http import HttpResponse
from collections import OrderedDict
from mainapp.models import MainModel
from datetime import datetime, timedelta

from .fusioncharts import FusionCharts


def index(request):
    time_threshold = datetime.now() - timedelta(hours=100)

    l = MainModel.objects.filter(time__gte=time_threshold)

    data_source = [OrderedDict(), OrderedDict(), OrderedDict(), OrderedDict(), OrderedDict(), OrderedDict(),
                   OrderedDict(), OrderedDict(), OrderedDict()]
    data_source[0]['chart'] = OrderedDict({
        "caption": "Temperature(in past 24 hours)",
        "subCaption": "In degrees Celsius",
        "xAxisName": "Reading in past 24 hours",
        "yAxisName": "Temperature",
        "theme": "candy"
    })
    data_source[0]['data'] = []
    data_source[1]['chart'] = OrderedDict({
        "caption": "Humidity(in past 24 hours)",
        "subCaption": "In %",
        "xAxisName": "Reading in past 24 hours",
        "yAxisName": "Humidity",
        "theme": "candy"
    })
    data_source[1]['data'] = []
    data_source[2]['chart'] = OrderedDict({
        "caption": "Energy from meter 1(in past 24 hours)",
        "subCaption": "In Wh",
        "xAxisName": "Reading in past 24 hours",
        "yAxisName": "Energy",
        "theme": "candy"
    })
    data_source[2]['data'] = []
    data_source[3]['chart'] = OrderedDict({
        "caption": "Energy from meter 2(in past 24 hours)",
        "subCaption": "In Wh",
        "xAxisName": "Reading in past 24 hours",
        "yAxisName": "Energy",
        "theme": "candy"
    })
    data_source[3]['data'] = []
    data_source[4]['chart'] = OrderedDict({
        "caption": "Energy from meter 3(in past 24 hours)",
        "subCaption": "In Wh",
        "xAxisName": "Reading in past 24 hours",
        "yAxisName": "Energy",
        "theme": "candy"
    })
    data_source[4]['data'] = []
    data_source[5]['chart'] = OrderedDict({
        "caption": "Energy from meter 4(in past 24 hours)",
        "subCaption": "In Wh",
        "xAxisName": "Reading in past 24 hours",
        "yAxisName": "Energy",
        "theme": "candy"
    })
    data_source[5]['data'] = []
    data_source[6]['chart'] = OrderedDict({
        "caption": "Energy from meter 5(in past 24 hours)",
        "subCaption": "In Wh",
        "xAxisName": "Reading in past 24 hours",
        "yAxisName": "Energy",
        "theme": "candy"
    })
    data_source[6]['data'] = []
    data_source[7]['chart'] = OrderedDict({
        "caption": "Temperature vs Energy(in past 24 hours)",
        "subCaption": "In the campus",
        "xAxisName": "Temperature",
        "yAxisName": "Energy",
        "xNumberSuffix": "° C",
        "theme": "candy"
    })
    data_source[7]['dataset'] = [
        OrderedDict({
            "seriesname": "Energy 1",
            "showregressionline": "1",
            "data": []
        }),
        OrderedDict({
            "seriesname": "Energy 2",
            "showregressionline": "1",
            "data": []
        }),
        OrderedDict({
            "seriesname": "Energy 3",
            "showregressionline": "1",
            "data": []
        }),
        OrderedDict({
            "seriesname": "Energy 4",
            "showregressionline": "1",
            "data": []
        }),
        OrderedDict({
            "seriesname": "Energy 5",
            "showregressionline": "1",
            "data": []
        }),
    ]
    data_source[8]['chart'] = OrderedDict({
        "caption": "Humidity vs Energy(in past 24 hours)",
        "subCaption": "In the campus",
        "xAxisName": "Humidity",
        "yAxisName": "Energy",
        "xNumberSuffix": "%",
        "theme": "candy"
    })
    data_source[8]['dataset'] = [
        OrderedDict({
            "seriesname": "Energy 1",
            "showregressionline": "1",
            "data": []
        }),
        OrderedDict({
            "seriesname": "Energy 2",
            "showregressionline": "1",
            "data": []
        }),
        OrderedDict({
            "seriesname": "Energy 3",
            "showregressionline": "1",
            "data": []
        }),
        OrderedDict({
            "seriesname": "Energy 4",
            "showregressionline": "1",
            "data": []
        }),
        OrderedDict({
            "seriesname": "Energy 5",
            "showregressionline": "1",
            "data": []
        }),
    ]
    i = 1

    for model in l[:40]:
        data_source[0]["data"].append({'label': i, 'value': float(model.temp)})
        data_source[1]["data"].append({'label': i, 'value': float(model.humidity)})
        data_source[2]["data"].append({'label': i, 'value': float(model.energy_1)})
        data_source[3]["data"].append({'label': i, 'value': float(model.energy_2)})
        data_source[4]["data"].append({'label': i, 'value': float(model.energy_3)})
        data_source[5]["data"].append({'label': i, 'value': float(model.energy_4)})
        data_source[6]["data"].append({'label': i, 'value': float(model.energy_5)})
        data_source[7]["dataset"][0]["data"].append({'y': float(model.energy_1), 'x': float(model.temp)})
        data_source[7]["dataset"][1]["data"].append({'y': float(model.energy_2), 'x': float(model.temp)})
        data_source[7]["dataset"][2]["data"].append({'y': float(model.energy_3), 'x': float(model.temp)})
        data_source[7]["dataset"][3]["data"].append({'y': float(model.energy_4), 'x': float(model.temp)})
        data_source[7]["dataset"][4]["data"].append({'y': float(model.energy_5), 'x': float(model.temp)})
        data_source[8]["dataset"][0]["data"].append({'y': float(model.energy_1), 'x': float(model.humidity)})
        data_source[8]["dataset"][1]["data"].append({'y': float(model.energy_2), 'x': float(model.humidity)})
        data_source[8]["dataset"][2]["data"].append({'y': float(model.energy_3), 'x': float(model.humidity)})
        data_source[8]["dataset"][3]["data"].append({'y': float(model.energy_4), 'x': float(model.humidity)})
        data_source[8]["dataset"][4]["data"].append({'y': float(model.energy_5), 'x': float(model.humidity)})
        i = i + 1

    graph = [
        FusionCharts("line", "Temperature", "800", "500", "temp-container", "json", data_source[0]),
        FusionCharts("line", "Humidity", "800", "500", "hum-container", "json", data_source[1]),
        FusionCharts("line", "Energy from meter 1", "800", "500", "energy-1-container", "json", data_source[2]),
        FusionCharts("line", "Energy from meter 2", "800", "500", "energy-2-container", "json", data_source[3]),
        FusionCharts("line", "Energy from meter 3", "800", "500", "energy-3-container", "json", data_source[4]),
        FusionCharts("line", "Energy from meter 4", "800", "500", "energy-4-container", "json", data_source[5]),
        FusionCharts("line", "Energy from meter 5", "800", "500", "energy-5-container", "json", data_source[6]),
        FusionCharts("scatter", "Temperature Energy Scatter", "600", "1000", "energy-temp-container", "json",
                     data_source[7]),
        FusionCharts("scatter", "Humidity Energy Scatter", "600", "1000", "energy-hum-container", "json",
                     data_source[8]),
    ]

    return render(request, 'index.html', {
        'temp_output': graph[0].render(),
        'hum_output': graph[1].render(),
        'e1_output': graph[2].render(),
        'e2_output': graph[3].render(),
        'e3_output': graph[4].render(),
        'e4_output': graph[5].render(),
        'e5_output': graph[6].render(),
        'et_output': graph[7].render(),
        'eh_output': graph[8].render(),
    })


# {
#     "chart": {
#         "caption": "Sales of Beer & Ice-cream vs Temperature",
#         "subCaption": "Los Angeles Topanga",
#         "baseFont": "Helvetica Neue,Arial",
#         "xAxisName": "Average Day Temperature",
#         "yAxisName": "Sales (In USD)",
#         "xAxisMinValue": "23",
#         "xAxisMaxValue": "95",
#         "yNumberPrefix": "$",
#         "xNumberSuffix": "&deg; F",
#         "theme": "fusion"
#     },
#     "categories": [
#         {
#             "verticalLineDashed": "1",
#             "verticalLineDashLen": "1",
#             "verticalLineDashGap": "1",
#             "verticalLineThickness": "1",
#             "verticalLineColor": "#000000",
#             "category": [
#                 {
#                     "x": "23",
#                     "label": "23° F",
#                     "showverticalline": "0"
#                 },
#                 {
#                     "x": "32",
#                     "label": "32° F",
#                     "showverticalline": "1"
#                 },
#                 {
#                     "x": "50",
#                     "label": "50° F",
#                     "showverticalline": "1"
#                 },
#                 {
#                     "x": "68",
#                     "label": "68° F",
#                     "showverticalline": "1"
#                 },
#                 {
#                     "x": "80",
#                     "label": "80° F",
#                     "showverticalline": "1"
#                 },
#                 {
#                     "x": "95",
#                     "label": "95° F",
#                     "showverticalline": "1"
#                 }
#             ]
#         }
#     ],
#     "dataset": [
#         {
#             "seriesname": "Ice Cream",
#             "showregressionline": "1",
#             "data": [
#
#                 {
#                     "x": "90",
#                     "y": "7500"
#                 },
#                 {
#                     "x": "92",
#                     "y": "7640"
#                 }
#             ]
#         },
#         {
#             "seriesname": "Beer",
#             "showregressionline": "1",
#             "data": [
#
#                 {
#                     "x": "90",
#                     "y": "5500"
#                 },
#                 {
#                     "x": "92",
#                     "y": "5240"
#                 }
#             ]
#         }
#     ],
#     "vtrendlines": [
#         {
#             "line": [
#                 {
#                     "startvalue": "23",
#                     "endvalue": "32",
#                     "istrendzone": "1",
#                     "displayvalue": " ",
#                     "color": "#adebff",
#                     "alpha": "25"
#                 },
#                 {
#                     "startvalue": "23",
#                     "endvalue": "32",
#                     "istrendzone": "1",
#                     "alpha": "0",
#                     "displayvalue": "Very cold"
#                 },
#                 {
#                     "startvalue": "32",
#                     "endvalue": "50",
#                     "istrendzone": "1",
#                     "displayvalue": " ",
#                     "color": "#adebff",
#                     "alpha": "15"
#                 },
#                 {
#                     "startvalue": "32",
#                     "endvalue": "50",
#                     "istrendzone": "1",
#                     "alpha": "0",
#                     "displayvalue": "Cold"
#                 },
#                 {
#                     "startvalue": "50",
#                     "endvalue": "68",
#                     "istrendzone": "1",
#                     "alpha": "0",
#                     "displayvalue": "Moderate"
#                 },
#                 {
#                     "startvalue": "68",
#                     "endvalue": "80",
#                     "istrendzone": "1",
#                     "alpha": "0",
#                     "displayvalue": "Hot"
#                 },
#                 {
#                     "startvalue": "68",
#                     "endvalue": "80",
#                     "istrendzone": "1",
#                     "displayvalue": " ",
#                     "color": "#f2a485",
#                     "alpha": "15"
#                 },
#                 {
#                     "startvalue": "80",
#                     "endvalue": "95",
#                     "istrendzone": "1",
#                     "alpha": "0",
#                     "displayvalue": "Very hot"
#                 },
#                 {
#                     "startvalue": "80",
#                     "endvalue": "95",
#                     "istrendzone": "1",
#                     "displayvalue": " ",
#                     "color": "#f2a485",
#                     "alpha": "25"
#                 }
#             ]
#         }
#     ]
# }

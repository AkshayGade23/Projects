import 'package:flutter/material.dart';
import 'package:charts_flutter/flutter.dart' as charts;
import 'package:optiride_client/chart_model.dart';

class Chartt extends StatelessWidget {
  final providerScores;

  Chartt({this.providerScores});

  List<String> providerNames = ["OLA", "Uber", "Rapido"];
  List<charts.Series<ChartModel, String>> _createSampleData() {
    final List<ChartModel> data = [
      ChartModel(
          provider: "Ola",
          score: providerScores['OLA'],
          color: charts.ColorUtil.fromDartColor(Colors.blue)),
      ChartModel(
          provider: "Rapido",
          score: providerScores['RAPIDO'],
          color: charts.ColorUtil.fromDartColor(Colors.green)),
      ChartModel(
          provider: "Uber",
          score: providerScores['UBER'],
          color: charts.ColorUtil.fromDartColor(Colors.red)),
    ];

    return [
      charts.Series<ChartModel, String>(
        data: data,
        id: 'poles',
        
        insideLabelStyleAccessorFn: (_, __) =>
            charts.TextStyleSpec(fontSize: 50),
        colorFn: (ChartModel chartModel, _) => chartModel.color,
        domainFn: (ChartModel chartModel, _) => chartModel.provider,
        measureFn: (ChartModel chartModel, _) => chartModel.score,
      )
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: charts.BarChart(
        _createSampleData(),
        animate: false,
      ),
    );
  }
}

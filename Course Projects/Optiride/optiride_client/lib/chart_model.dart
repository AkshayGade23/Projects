import 'package:flutter/material.dart';
import 'package:charts_flutter/flutter.dart' as charts;

class ChartModel {
  ChartModel({required this.provider, required this.score,required this.color});

  final String provider;
  final double score;
  final charts.Color color;
}

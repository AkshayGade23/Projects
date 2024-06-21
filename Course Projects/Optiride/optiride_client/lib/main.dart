import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:optiride_client/Experience.dart';
import 'package:optiride_client/show_chart.dart';
import 'connect_backed.dart';
import 'new_textf.dart';
import 'get_ride.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'O p t i R i d e'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Color pink = Colors.pink;

  bool isGetRide = true;

  void setGetRide() {
    if (!isGetRide) {
      setState(() {
        isGetRide = true;
      });
    }
  }

  void setExperience() {
    if (isGetRide) {
      setState(() {
        isGetRide = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.pink[100],
        title: Container(
          width: double.infinity,
          alignment: Alignment.center,
          child: Text(
            widget.title,
            style: TextStyle(
                fontSize: 30,
                color: Colors.pink[500],
                fontWeight: FontWeight.bold),
          ),
        ),
      ),
      body: Container(
        height: double.maxFinite,
        child: Column(
          children: [
            Container(
              margin: const EdgeInsets.all(15),
              width: 500,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Container(
                    child: TextButton(
                      onPressed: setGetRide,
                      child: Container(
                        width: 200,
                        height: 40,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: isGetRide ? pink : Colors.pink[200],
                          borderRadius:
                              const BorderRadius.all(Radius.circular(17)),
                        ),
                        child: const Text(
                          "Get Ride",
                          style: TextStyle(color: Colors.white, fontSize: 20),
                        ),
                      ),
                    ),
                  ),
                  Container(
                    child: TextButton(
                      onPressed: setExperience,
                      child: Container(
                        width: 200,
                        height: 40,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: isGetRide ? Colors.pink[200] : pink,
                          borderRadius:
                              const BorderRadius.all(Radius.circular(17)),
                        ),
                        child: const Text(
                          "Add Ride",
                          style: TextStyle(color: Colors.white, fontSize: 20),
                        ),
                      ),
                    ),
                  )
                ],
              ),
            ),
            Expanded(
              child: isGetRide ? GetRide() : Experience(),
            )
          ],
        ),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}

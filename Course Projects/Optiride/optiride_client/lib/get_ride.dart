// import 'dart:collection';
import 'dart:convert';
// import 'dart:ffi';

import 'package:flutter/material.dart';
import 'connect_backed.dart';
import 'show_chart.dart';
import 'new_textf.dart';

class GetRide extends StatefulWidget {
  const GetRide({super.key});

  @override
  State<GetRide> createState() => _GetRideState();
}

class _GetRideState extends State<GetRide> {
  Color pink = Colors.pink;

  TextEditingController source = TextEditingController();
  TextEditingController destination = TextEditingController();
  TextEditingController gg = TextEditingController();

  String route = "";
  bool show_chart = false;
  var providerScores;

  void onOptimum() async {
    if (source.text != "" && destination.text != "") {
      String src = source.text;
      String dest = destination.text;
      var data = {"source": src, "destination": dest, "vehicle": _value + 2};
      
      var res = await sendData(data).then((value) => value.body);
      providerScores = jsonDecode(res);
      // print(providerScores['Uber']);

      var bestProvider = providerScores['UBER'];
      String bestProviderName = 'UBER';
      if(providerScores.length == 0) bestProviderName = "Not available";
      // for (var i = 0; i < providerScores.length; i++) {
      //     if(bestProvider < providerScores)

print(providerScores);
      // }
      final Map providerScores1 = providerScores;

      providerScores1.forEach((key, value) {
        if (value > bestProvider) {
          bestProviderName = key;
          bestProvider = value;
        }
      });

      setState(() {
        route = "Optimum Provider for Ride ( " +src + ", " + dest + " )  => " + bestProviderName;
            bestProviderName;
        show_chart = true;
      });
    }
  }

  int _value = 0;
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Container(
        alignment: Alignment.center,
        // width: double.maxFinite,
        child: Column(
          children: [
            Container(
              width: 500,
              height: 550,
              decoration: BoxDecoration(
                color: Colors.pink[50],
                borderRadius: BorderRadius.all(Radius.circular(15)),
              ),
              alignment: Alignment.center,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                    height: 150,
                    child: Image.asset("assets/images/g.png"),
                  ),
                  NewTextF(
                    pink: pink,
                    label: "Source",
                    controller: source,
                  ),
                  NewTextF(
                    pink: pink,
                    label: "Destination",
                    controller: destination,
                  ),
                  Container(
                    margin: const EdgeInsets.only(top: 15),
                    child: Text(
                      "Choose Vehicle",
                      style: TextStyle(fontSize: 20, color: Colors.pink[800]),
                    ),
                  ),
                  Container(
                    margin: EdgeInsets.only(top: 30),
                    alignment: Alignment.center,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: <Widget>[
                        GestureDetector(
                          onTap: () => setState(() => _value = 0),
                          child: Container(
                            alignment: Alignment.center,
                            decoration: BoxDecoration(
                              border: Border.all(color: pink, width: 2),
                              borderRadius:
                                  BorderRadius.all(Radius.circular(30)),
                              color: _value == 0 ? pink : Colors.white,
                            ),
                            height: 56,
                            width: 56,
                            child: Text(
                              "🚴",
                              style: TextStyle(
                                  color: _value == 0 ? Colors.white : pink,
                                  fontSize: 25,
                                  fontWeight: FontWeight.w500),
                            ),
                          ),
                        ),
                        SizedBox(width: 20),
                        GestureDetector(
                          onTap: () => setState(() => _value = 1),
                          child: Container(
                            alignment: Alignment.center,
                            decoration: BoxDecoration(
                              border: Border.all(color: pink, width: 2),
                              borderRadius:
                                  BorderRadius.all(Radius.circular(30)),
                              color: _value == 1 ? pink : Colors.white,
                            ),
                            height: 56,
                            width: 56,
                            child: Text(
                              "🛺",
                              style: TextStyle(
                                color: _value == 1 ? Colors.white : pink,
                                fontSize: 25,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ),
                        ),
                        SizedBox(width: 20),
                        GestureDetector(
                          onTap: () => setState(() => _value = 2),
                          child: Container(
                            decoration: BoxDecoration(
                              border: Border.all(color: pink, width: 2),
                              borderRadius:
                                  BorderRadius.all(Radius.circular(30)),
                              color: _value == 2 ? pink : Colors.white,
                            ),
                            alignment: Alignment.center,
                            height: 56,
                            width: 56,
                            child: Text(
                              "🚗",
                              style: TextStyle(
                                color: _value == 2 ? Colors.white : pink,
                                fontSize: 25,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  Container(
                    margin: const EdgeInsets.only(top: 30),
                    child: TextButton(
                      onPressed: onOptimum,
                      child: Container(
                        width: 200,
                        height: 40,
                        alignment: Alignment.center,
                        decoration: BoxDecoration(
                          color: pink,
                          borderRadius:
                              const BorderRadius.all(Radius.circular(30)),
                        ),
                        child: const Text(
                          "Optimum",
                          style: TextStyle(color: Colors.white, fontSize: 20),
                        ),
                      ),
                    ),
                  )
                ],
              ),
            ),

            if (show_chart)
              Container(
                margin: EdgeInsets.only(top: 50,bottom: 20 ),
                child: Text(
                  route,
                  style: const TextStyle(
                      color: Colors.pink,
                      fontSize: 25,
                      fontWeight: FontWeight.bold),
                ),
              ),
            if (show_chart)
              Container(
                width: 750,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Container(
                      width: 3,
                      margin: const EdgeInsets.symmetric(horizontal: 20),
                      child: const Text(
                        "OptiScore",
                        style: TextStyle(
                            fontSize: 20, fontWeight: FontWeight.bold),
                      ),
                    ),
                    SizedBox(
                      height: 800,
                      width: 700 - 40,
                      child: Chartt(
                        providerScores: providerScores,
                      ),
                    ),
                  ],
                ),
              ),
            if (show_chart)
              Container(
                child: const Text(
                  "Providers",
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
              ),
            const SizedBox(
              height: 50,
            )
          ],
        ),
      ),
    );
  }
}

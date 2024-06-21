import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'connect_backed.dart';
import 'package:duration_picker/duration_picker.dart';
import 'show_chart.dart';
import 'new_textf.dart';

class Experience extends StatefulWidget {
  Experience({super.key});

  @override
  State<Experience> createState() => _ExperienceState();
}

class _ExperienceState extends State<Experience> {
  Color pink = Colors.pink;

  TextEditingController name = TextEditingController();
  TextEditingController age = TextEditingController();
  TextEditingController source = TextEditingController();
  TextEditingController destination = TextEditingController();
  TextEditingController cost = TextEditingController();
  int _value = 0;

  int _carValue = 0;
  int _providerValue = 1;
  int _custId = 0;
  bool isSubmit = false;

  bool isUploaded = false;

  late Duration _duration = Duration.zero;

  void onSubmitCust() async {
    if (name.text != "" && age.text != "") {
      var data = {
        "name": name.text,
        "age": int.parse(age.text),
        "gender": _value == 1 ? "FEMALE" : "MALE",
      };

      print("tinktinktinktinktink");
      var res = await sendCustomerData(data).then((value) => value.body);

      var d = jsonDecode(res);
      _custId = d['id'];

      setState(() {
        isSubmit = true;
      });
    }
  }

  void onSubmitRide() async {
    if (source.text != "" && destination.text != "" && cost.text != "") {
      var data = {
        "src": source.text,
        "dest": destination.text,
        "cost": int.parse(cost.text),
        "duration": _duration.toString().substring(0,7),
        "vehicle": _carValue + 2,
        "prov_id": _providerValue,
        'cust_id': _custId,
      };

      var res = postRidesDetails(data).then((value) => value.body);

      setState(() {
        // isSubmit = true;
        isUploaded = true;
      });
    }
  }

  Widget success(){
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SizedBox(
          height: 150,
          child: Image.asset("assets/images/g.png"),
        ),
        Container(
          height: 200,
          alignment: Alignment.center,
          child: Text(
            "Submitted Data Successfully !!!",
            style: TextStyle(fontSize: 40, color: Colors.green[900]),
          ),
        ),
      ],
    );
  }

  Widget customerdetails() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SizedBox(
          height: 150,
          child: Image.asset("assets/images/g.png"),
        ),
        Container(
          child: Text(
            "Your Details",
            style: TextStyle(fontSize: 40, color: Colors.pink[800]),
          ),
        ),
        NewTextF(
          pink: pink,
          label: "Name",
          controller: name,
        ),
        Container(
          margin: const EdgeInsets.all(15),
          width: 400,
          height: 50,
          child: TextFormField(
            inputFormatters: [FilteringTextInputFormatter.digitsOnly],
            controller: age,
            cursorColor: pink,
            textAlign: TextAlign.center,
            decoration: InputDecoration(
              filled: true,
              fillColor: Colors.white,
              labelStyle: TextStyle(
                color: pink,
              ),
              focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: pink),
                  borderRadius: const BorderRadius.all(Radius.circular(25))),
              enabledBorder: OutlineInputBorder(
                borderSide: BorderSide(color: pink),
              ),
              focusColor: pink,
              labelText: "Age",
            ),
          ),
        ),
        Container(
          margin: const EdgeInsets.only(top: 15),
          child: Text(
            "Gender",
            style: TextStyle(fontSize: 20, color: Colors.pink[800]),
          ),
        ),
        Container(
          margin: const EdgeInsets.only(top: 15),
          alignment: Alignment.center,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              GestureDetector(
                onTap: () => setState(() => _value = 0),
                child: Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    borderRadius: const BorderRadius.all(Radius.circular(30)),
                    color: _value == 0 ? pink : Colors.white,
                  ),
                  height: 56,
                  width: 56,
                  child: Text("👨‍🦰",
                      style: TextStyle(
                        fontSize: 25,
                        fontWeight: FontWeight.w500,
                        color: _value == 1 ? pink : Colors.white,
                      )),
                ),
              ),
              const SizedBox(width: 20),
              GestureDetector(
                onTap: () => setState(() => _value = 1),
                child: Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    borderRadius: const BorderRadius.all(Radius.circular(30)),
                    color: _value == 1 ? pink : Colors.white,
                  ),
                  height: 56,
                  width: 56,
                  child: Text(
                    "👩‍🦰",
                    style: TextStyle(
                        fontSize: 25,
                        fontWeight: FontWeight.w500,
                        color: _value == 1 ? Colors.white : pink),
                  ),
                ),
              ),
            ],
          ),
        ),
        Container(
          margin: const EdgeInsets.only(top: 40),
          child: InkWell(
            onTap: onSubmitCust,
            child: Container(
              width: 200,
              height: 40,
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: pink,
                borderRadius: const BorderRadius.all(Radius.circular(30)),
              ),
              child: const Text(
                "Submit",
                style: TextStyle(color: Colors.white, fontSize: 20),
              ),
            ),
          ),
        ),
        SizedBox(
          height: 40,
        ),
      ],
    );
  }

  Widget ridedetails() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SizedBox(
          height: 150,
          child: Image.asset("assets/images/g.png"),
        ),
        Container(
          child: Text(
            "Ride Details",
            style: TextStyle(fontSize: 40, color: Colors.pink[800]),
          ),
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
          margin: const EdgeInsets.all(15),
          width: 400,
          height: 50,
          child: TextFormField(
            inputFormatters: [FilteringTextInputFormatter.digitsOnly],
            controller: cost,
            cursorColor: pink,
            textAlign: TextAlign.center,
            decoration: InputDecoration(
              filled: true,
              fillColor: Colors.white,
              labelStyle: TextStyle(
                color: pink,
              ),
              focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: pink),
                  borderRadius: const BorderRadius.all(Radius.circular(25))),
              enabledBorder: OutlineInputBorder(
                borderSide: BorderSide(color: pink),
              ),
              focusColor: pink,
              labelText: "Cost",
            ),
          ),
        ),
        // Duration
        Container(
          margin: const EdgeInsets.only(top: 15),
          child: Text(
            "Duration",
            style: TextStyle(fontSize: 20, color: Colors.pink[800]),
          ),
        ),
        DurationPicker(
          duration: _duration,
          baseUnit: BaseUnit.minute,
          onChange: (val) {
            setState(() => _duration = val);
          },
          snapToMins: 5.0,
        ),
        //Vehicle
        Container(
          margin: const EdgeInsets.only(top: 15),
          child: Text(
            "Choose Vehicle",
            style: TextStyle(fontSize: 20, color: Colors.pink[800]),
          ),
        ),
        Container(
          margin: const EdgeInsets.only(top: 30),
          alignment: Alignment.center,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              GestureDetector(
                onTap: () => setState(() => _carValue = 0),
                child: Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    border: Border.all(color: pink, width: 2),
                    borderRadius: const BorderRadius.all(Radius.circular(30)),
                    color: _carValue == 0 ? pink : Colors.white,
                  ),
                  height: 56,
                  width: 56,
                  child: Text(
                    "🚴",
                    style: TextStyle(
                        color: _carValue == 0 ? Colors.white : pink,
                        fontSize: 25,
                        fontWeight: FontWeight.w500),
                  ),
                ),
              ),
              const SizedBox(width: 20),
              GestureDetector(
                onTap: () => setState(() => _carValue = 1),
                child: Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    border: Border.all(color: pink, width: 2),
                    borderRadius: const BorderRadius.all(Radius.circular(30)),
                    color: _carValue == 1 ? pink : Colors.white,
                  ),
                  height: 56,
                  width: 56,
                  child: Text(
                    "🛺",
                    style: TextStyle(
                      color: _carValue == 1 ? Colors.white : pink,
                      fontSize: 25,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 20),
              GestureDetector(
                onTap: () => setState(() => _carValue = 2),
                child: Container(
                  decoration: BoxDecoration(
                    border: Border.all(color: pink, width: 2),
                    borderRadius: const BorderRadius.all(Radius.circular(30)),
                    color: _carValue == 2 ? pink : Colors.white,
                  ),
                  alignment: Alignment.center,
                  height: 56,
                  width: 56,
                  child: Text(
                    "🚗",
                    style: TextStyle(
                      color: _carValue == 2 ? Colors.white : pink,
                      fontSize: 25,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        //PRovider
        Container(
          margin: const EdgeInsets.only(top: 15),
          child: Text(
            "Choose Provider",
            style: TextStyle(fontSize: 20, color: Colors.pink[800]),
          ),
        ),
        Container(
          margin: const EdgeInsets.only(top: 30),
          alignment: Alignment.center,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              GestureDetector(
                onTap: () => setState(() => _providerValue = 1),
                child: Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    border: Border.all(color: pink, width: 2),
                    borderRadius: const BorderRadius.all(Radius.circular(30)),
                    color: _providerValue == 1 ? pink : Colors.white,
                  ),
                  height: 56,
                  width: 56,
                  child: Text(
                    "Ola",
                    style: TextStyle(
                        color: _providerValue == 1 ? Colors.white : pink,
                        fontSize: 15,
                        fontWeight: FontWeight.w500),
                  ),
                ),
              ),
              const SizedBox(width: 20),
              GestureDetector(
                onTap: () => setState(() => _providerValue = 2),
                child: Container(
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    border: Border.all(color: pink, width: 2),
                    borderRadius: const BorderRadius.all(Radius.circular(30)),
                    color: _providerValue == 2 ? pink : Colors.white,
                  ),
                  height: 56,
                  width: 56,
                  child: Text(
                    "Uber",
                    style: TextStyle(
                      color: _providerValue == 2 ? Colors.white : pink,
                      fontSize: 15,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 20),
              GestureDetector(
                onTap: () => setState(() => _providerValue = 3),
                child: Container(
                  decoration: BoxDecoration(
                    border: Border.all(color: pink, width: 2),
                    borderRadius: const BorderRadius.all(Radius.circular(30)),
                    color: _providerValue == 3 ? pink : Colors.white,
                  ),
                  alignment: Alignment.center,
                  height: 56,
                  width: 56,
                  child: Text(
                    "Rapido",
                    style: TextStyle(
                      color: _providerValue == 3 ? Colors.white : pink,
                      fontSize: 15,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        Container(
          margin: const EdgeInsets.only(top: 40),
          child: InkWell(
            onTap: onSubmitRide,
            child: Container(
              width: 200,
              height: 40,
              alignment: Alignment.center,
              decoration: BoxDecoration(
                color: pink,
                borderRadius: const BorderRadius.all(Radius.circular(30)),
              ),
              child: const Text(
                "Submit",
                style: TextStyle(color: Colors.white, fontSize: 20),
              ),
            ),
          ),
        ),
        SizedBox(
          height: 30,
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.topCenter,
      child: SingleChildScrollView(
        child: Container(
          width: 800,
          decoration: BoxDecoration(
            color: Colors.pink[50],
            borderRadius: const BorderRadius.all(Radius.circular(15)),
          ),
          alignment: Alignment.center,
          child: isUploaded ? success() : isSubmit ? ridedetails() : customerdetails(),
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';

class NewTextF extends StatelessWidget {
  const NewTextF({
    super.key,
    required this.controller,
    required this.pink,
    required this.label,
  });

  final TextEditingController controller;
  final Color pink;
  final String label;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.all(15),
      width: 400,
      height: 50,
      child: TextFormField(
        controller: controller,
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
            labelText: label,
           ),
      ),
    );
  }
}

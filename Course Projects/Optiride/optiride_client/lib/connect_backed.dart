import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

 Map<String, String> requestHeaders = {
    'Content-type': 'application/json',
    'Accept': 'application/json',
  };

  String url1 = "http://localhost:8000/getData";
  String url2= "http://localhost:8000/reqData";
  String url3= "http://localhost:8000/getCustomerData";
  String url4= "http://localhost:8000/postCustomerDetails";

  

Future<http.Response> sendData(var data) async {
  var res = await http.post(Uri.parse(url1),
      body: jsonEncode(data), headers: requestHeaders);

  return res;
}


Future<http.Response> getData()async{
  var result = await http.get(Uri.parse(url2),headers: requestHeaders);
  return result;
}


Future<http.Response> sendCustomerData(var data) async {
  var res = await http.post(Uri.parse(url3),
      body: jsonEncode(data), headers: requestHeaders);
  return res;
}

Future<http.Response> postRidesDetails(var data) async {
  print(data);
  print("djadaadda");
  var res = await http.post(Uri.parse(url4),
      body: jsonEncode(data), headers: requestHeaders);
  return res;
}

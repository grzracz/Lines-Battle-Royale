// Copyright (c) 2019 Grzegorz Raczek
// https://github.com/grzracz
// Files available under MIT license

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:io';
import 'package:get_ip/get_ip.dart';
import 'package:vibration/vibration.dart';

String host = "192.168.43.173";
int port = 8000;
ScaffoldState bar;
Socket s;
String connectionStatus = "Disconnected";
Color statusColor = Colors.red;
Color gearColor = Colors.black;
IconData connectionIcon = Icons.clear;
String ip = "none";
_StatusState connectionButton;
String tempAddrValue = host + ":" + port.toString();
String errorText = "";

showError(error){
  bar.showSnackBar(new SnackBar(
      duration: const Duration(milliseconds: 1500),
      content: Text(error, textAlign: TextAlign.center)
  )
  );
}

void main() {
  runApp(MyApp());
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);
  SystemChrome.setEnabledSystemUIOverlays([]);
  findIp();
}

Future<void> findIp() async {
  ip = await GetIp.ipAddress;
}

void connect() {
  if (s == null) {
    connectionButton.setState(() {
      connectionStatus = "Connecting...";
      statusColor = Colors.yellow;
      gearColor = Colors.grey;
      connectionIcon = null;
    });
    Socket.connect(host, port).then((socket) {
      print('Connected to: ''${socket.remoteAddress.address}:${socket
          .remotePort}');
      s = socket;
      s.write(ip);
      connectionButton.setState(() {
        connectionStatus = "Connected";
        statusColor = Colors.green;
        gearColor = Colors.grey;
        connectionIcon = Icons.check;
      });
    }).catchError((socket) {
      if (s == null) {
        connectionButton.setState(() {
          connectionStatus = "Disconnected";
          statusColor = Colors.red;
          gearColor = Colors.black;
          connectionIcon = Icons.clear;
        });
        showError("Unable to connect. Check connection settings.");
      }
    });
  }
}

void disconnect() {
  if (s != null) {
    s.destroy();
    s = null;
    connectionButton.setState((){
      connectionStatus = "Disconnected";
      statusColor = Colors.red;
      gearColor = Colors.black;
      connectionIcon = Icons.clear;
    });
  }
}

void sendInput(input) {
  Vibration.vibrate(duration: 50);
  if (s != null) s.write(input);
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'Tetris Controller',
        home: Scaffold(
          body: Controls(),
        )
    );
  }
}

class Status extends StatefulWidget {
  @override
  _StatusState createState() => _StatusState();
}

class _StatusState extends State<Status> {
  @override
  Widget build(BuildContext context) {
    connectionButton = this;
    return Row(
        children: <Widget> [
          Flexible(
              flex: 4,
              child: FlatButton(
                  textColor: statusColor,
                  onPressed: () {
                    if (connectionStatus == "Disconnected") {
                      connect();
                    } else {
                      disconnect();
                    }
                  },
                  child: Row(
                      children: <Widget> [
                        Icon(connectionIcon, size: 17),
                        Text(connectionStatus, style: new TextStyle(
                          fontSize: 17.0,
                        ))
                      ]
                  )
              )
          ),
          Flexible(
              flex: 1,
              child: FlatButton(
                  child: Icon(Icons.settings, size: 20, color: gearColor),
                  onPressed: () {
                    if (connectionStatus == "Disconnected") {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => ConnectingMenu()),
                      );
                    }
                    else return null;
                  }
              )
          )
        ]
    );
  }
}

class Controls extends StatelessWidget {
  @override
  Widget build (BuildContext context)
  {
    bar = Scaffold.of(context);
    return Scaffold(
        body: Row(
            children: <Widget> [
              Flexible(
                  flex: 2,
                  child: Container(
                      color: Colors.black12,
                      padding: EdgeInsets.all(10.0),
                      width: double.infinity,
                      height: double.infinity,
                      child: FlatButton(
                          color: Colors.white,
                          child: Icon(Icons.keyboard_arrow_left, size: 100),
                          onPressed: () //SEND THIS FOR LEFT MOVEMENT
                          {
                            sendInput("LEFT");
                          }
                      )
                  )
              ),
              Flexible(
                  flex: 3,
                  child: Column (
                      children: <Widget> [
                        Flexible(
                            flex: 1,
                            child: Container(
                                color: Colors.white,
                                padding: EdgeInsets.all(10.0),
                                width: double.infinity,
                                child: Status()
                            )
                        ),
                        Flexible(
                            flex: 4,
                            child:
                            Container(
                                color: Colors.black38,
                                padding: EdgeInsets.all(10.0),
                                width: double.infinity,
                                height: double.infinity,
                                child: FlatButton(
                                  color: Colors.white,
                                  child: Icon(Icons.keyboard_arrow_up, size: 100),
                                  onPressed: () //SEND THIS FOR ROTATION
                                  {
                                    sendInput("UP");
                                    SystemChrome.setEnabledSystemUIOverlays([]);
                                  },
                                )
                            )
                        ),
                        Flexible(
                            flex: 4,
                            child: Container(
                                color: Colors.black54,
                                padding: EdgeInsets.all(10.0),
                                width: double.infinity,
                                height: double.infinity,
                                child: FlatButton(
                                    color: Colors.white,
                                    child: Icon(Icons.keyboard_arrow_down, size: 100),
                                    onPressed: () //SEND THIS FOR DOWN MOVEMENT
                                    {
                                      sendInput("DOWN");
                                    }
                                )
                            )
                        )
                      ]
                  )
              ),
              Flexible(
                  flex: 2,
                  child: Container(
                      color: Colors.black12,
                      padding: EdgeInsets.all(10.0),
                      width: double.infinity,
                      height: double.infinity,
                      child: FlatButton(
                          color: Colors.white,
                          child: Icon(Icons.keyboard_arrow_right, size: 100),
                          onPressed: () //SEND THIS FOR RIGHT MOVEMENT
                          {
                            sendInput("RIGHT");
                          }
                      )
                  )
              )
            ]
        )
    );
  }
}


class ConnectingMenu extends StatefulWidget {
  @override
  _MenuState createState() => _MenuState();
}

class _MenuState extends State<ConnectingMenu> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.black,
          title: Text("Connection Settings"),
        ),
        body: SettingsForm()
    );
  }
}

class SettingsForm extends StatefulWidget {
  @override
  _SettingsFormState createState() => _SettingsFormState();
}

class _SettingsFormState extends State<SettingsForm> {

  bool isIPCorrect(String ipAddr) {
    int temp = 0;
    for (int i = 0; i < ipAddr.length - 1; ++i) {
      if (ipAddr[i] == ".") {
        ++temp;
      }
      if (ipAddr[i] == "." && ipAddr[i+1] == ".") return false;
    }
    if (temp != 3) return false;
    if (!ipAddr.contains(":")) return false;
    int i1 = 0;
    for (int i = 0; i < 4; ++i) {
      int i2 = ipAddr.indexOf(".", i1);
      if (i2 == -1) i2 = ipAddr.indexOf(":", i1);
      String substr = ipAddr.substring(i1, i2);
      i1 = i2 + 1;
      if (substr == "") return false;
      if (int.parse(substr) < 0 || int.parse(substr) > 255) return false;
    }
    String substr = ipAddr.substring(ipAddr.indexOf(":") + 1, ipAddr.length);
    if (substr == "") return false;
    if (int.parse(substr) < 0 || int.parse(substr) > 65535) return false;
    return true;
  }

  void tempAddr(String input){
    if (tempAddrValue == "Server address changed!") setState(() {
      tempAddrValue = tempAddrValue = host + ":" + port.toString();
    });
    if (input == "BACKSPACE") {
      if (tempAddrValue.length > 0) setState(() {
        tempAddrValue = tempAddrValue.substring(0, tempAddrValue.length - 1);
      });
    }
    else if (input == "CLEAR"){
      if (tempAddrValue != "") setState((){
        tempAddrValue = "";
      });
    }
    else if (input == "RESET"){
      confirmReset();
    }
    else if (input == "CONFIRM"){
      setState((){
        if (isIPCorrect(tempAddrValue)) {
          confirm();
        }
        else
        {
          errorText = "This server address does not seem to be correct.";
        }
      });
    }
    else {
      setState((){
        if (tempAddrValue.length < 21) tempAddrValue += input;
      });
    }
  }

  void confirmReset() {
    // flutter defined function
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // return object of type Dialog
        return AlertDialog(
          title: new Text("Confirm changes"),
          content: new Text("Are you sure you want reset settings?"),
          actions: <Widget>[
            // usually buttons at the bottom of the dialog
            new FlatButton(
              child: new Text("Yes"),
              onPressed: () {
                setState((){
                  host = "192.168.43.173";
                  port = 8001;
                  tempAddrValue = host + ":" + port.toString();
                });
                Navigator.of(context).pop();
              },
            ),
            new FlatButton(
                child: new Text("No"),
                onPressed: (){
                  Navigator.of(context).pop();
                }
            )
          ],
        );
      },
    );
  }

  void confirm() {
    // flutter defined function
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // return object of type Dialog
        return AlertDialog(
          title: new Text("Confirm changes"),
          content: new Text("Are you sure you want to use this server address?"),
          actions: <Widget>[
            // usually buttons at the bottom of the dialog
            new FlatButton(
              child: new Text("Yes"),
              onPressed: () {
                setState((){
                  host = tempAddrValue.substring(0, tempAddrValue.lastIndexOf(":"));
                  port = int.parse(tempAddrValue.substring(
                      tempAddrValue.lastIndexOf(":") + 1, tempAddrValue.length));
                  tempAddrValue = "Server address changed!";
                  errorText = "";
                });
                Navigator.of(context).pop();
              },
            ),
            new FlatButton(
                child: new Text("No"),
                onPressed: (){
                  Navigator.of(context).pop();
                }
            )
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
        children: <Widget> [
          Flexible( //current values
              flex: 3,
              child: Row(
                  children: <Widget> [
                    Flexible(
                        flex: 1,
                        child: Container(
                            padding: EdgeInsets.all(10.0),
                            width: double.infinity,
                            height: double.infinity,
                            child: Column(
                                children: [
                                  Text("Current server address:"),
                                  Text("Address of this device:")
                                ]
                            )
                        )
                    ),
                    Flexible(
                        flex: 1,
                        child: Container(
                            padding: EdgeInsets.all(10.0),
                            width: double.infinity,
                            height: double.infinity,
                            child: Column(
                                children: [
                                  Text(host + ":" + port.toString()),
                                  Text(ip)
                                ]
                            )
                        )
                    )
                  ]
              )
          ),
          Flexible( // input fields
              flex: 10,
              child: Container(
                  padding: EdgeInsets.all(10.0),
                  width: double.infinity,
                  height: double.infinity,
                  child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Flexible(
                            child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: <Widget> [
                                  Text("Change server address:",
                                      style: new TextStyle(
                                          fontSize: 15
                                      )),
                                  Text(tempAddrValue,
                                      style: new TextStyle(
                                          color: Colors.black54,
                                          fontSize: 30
                                      )),
                                  Text("Server IP address and port",
                                      style: new TextStyle(
                                          color: Colors.black54,
                                          fontStyle: FontStyle.italic
                                      )),
                                  Row(
                                      children: [
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("1"),
                                              onPressed: (){
                                                tempAddr("1");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("2"),
                                              onPressed: (){
                                                tempAddr("2");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("3"),
                                              onPressed: (){
                                                tempAddr("3");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("4"),
                                              onPressed: (){
                                                tempAddr("4");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("5"),
                                              onPressed: (){
                                                tempAddr("5");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("6"),
                                              onPressed: (){
                                                tempAddr("6");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("7"),
                                              onPressed: (){
                                                tempAddr("7");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("8"),
                                              onPressed: (){
                                                tempAddr("8");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("9"),
                                              onPressed: (){
                                                tempAddr("9");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("0"),
                                              onPressed: (){
                                                tempAddr("0");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text("."),
                                              onPressed: (){
                                                tempAddr(".");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Text(":"),
                                              onPressed: (){
                                                tempAddr(":");
                                              },
                                            )
                                        ),
                                        Flexible(
                                            flex: 1,
                                            child: RaisedButton(
                                              child: Icon(Icons.backspace),
                                              onPressed: (){
                                                tempAddr("BACKSPACE");
                                              },
                                            )
                                        ),
                                      ]
                                  ),
                                  Row(
                                      children: [
                                        Flexible(
                                            child: Container(
                                                width: double.infinity,
                                                padding: EdgeInsets.all(5.0),
                                                child: RaisedButton(
                                                  child: Text("Reset settings"),
                                                  onPressed: (){
                                                    tempAddr("RESET");
                                                  },
                                                )
                                            )
                                        ),
                                        Flexible(
                                            child: Container(
                                                width: double.infinity,
                                                padding: EdgeInsets.all(5.0),
                                                child: RaisedButton(
                                                  child: Text("Clear input"),
                                                  onPressed: (){
                                                    tempAddr("CLEAR");
                                                  },
                                                )
                                            )
                                        ),
                                        Flexible(
                                            child: Container(
                                                width: double.infinity,
                                                padding: EdgeInsets.all(5.0),
                                                child: RaisedButton(
                                                  child: Text("Confirm address"),
                                                  onPressed: () {
                                                    tempAddr("CONFIRM");
                                                  },
                                                )
                                            )
                                        )
                                      ]
                                  )
                                ]
                            )
                        ),
                      ]
                  )
              )
          ),
          Flexible(
              flex: 2,
              child: Text(errorText, style: new TextStyle(color: Colors.red))
          ),
        ]
    );
  }
}

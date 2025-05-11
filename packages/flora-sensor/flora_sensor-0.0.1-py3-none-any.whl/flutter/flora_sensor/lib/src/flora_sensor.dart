import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'dart:async';
import 'package:ambient_light/ambient_light.dart';

class FloraSensor extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const FloraSensor({
    super.key,
    required this.parent,
    required this.control,
    required this.backend
  });

  @override
  _FloraSensorState createState() => _FloraSensorState();
}

class _FloraSensorState extends State<FloraSensor> {
  final AmbientLight _ambientLight = AmbientLight();
  double? _currentAmbientLightStream;
  StreamSubscription<double>? _ambientLightSubscription;

  @override
  void initState() {
    super.initState();
    _startListening();
  }

  @override
  void dispose() {
    _ambientLightSubscription?.cancel();
    super.dispose();
  }

  Future<void> _startListening() async {
    _ambientLightSubscription?.cancel();
    _ambientLightSubscription = _ambientLight.ambientLightStream.listen((lux) {
      if (!mounted) return;
      setState(() {
        _currentAmbientLightStream = lux;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "get_sensor_value":
            return "$_currentAmbientLightStream";
          case "on":
            setState(() {
              _startListening();
            });
            return "ok";
          case "off":
            setState(() {
              dispose();
            });
            return "ok";
        }
        return "";
      });
    }();
    return constrainedControl(
      context,
      Text("$_currentAmbientLightStream"),
      widget.parent,
      widget.control,
    );
  }
}
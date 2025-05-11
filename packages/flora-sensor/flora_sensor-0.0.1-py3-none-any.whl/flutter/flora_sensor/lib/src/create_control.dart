import 'package:flet/flet.dart';

import 'flora_sensor.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "flora_sensor":
      return FloraSensor(
        parent: args.parent,
        control: args.control,
        backend: args.backend
      );
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to initialize
}
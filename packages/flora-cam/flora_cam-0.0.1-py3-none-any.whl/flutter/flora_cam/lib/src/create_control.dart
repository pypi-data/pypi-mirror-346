import 'package:flet/flet.dart';

import 'flora_cam.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "flora_cam":
      return FloraCam(
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
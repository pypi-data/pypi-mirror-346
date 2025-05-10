import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:path_provider/path_provider.dart';

class CameraControl extends StatefulWidget {
  final CameraDescription camera;

  const CameraControl({
    super.key,
    required this.camera,
  });

  @override
  CameraControlState createState() => CameraControlState();
}

class CameraControlState extends State<CameraControl> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  bool _isCameraEnabled = true;
  CameraLensDirection _lensDirection = CameraLensDirection.back;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.medium,
    );
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void switchCamera(){
    setState(() {
      if (_lensDirection == CameraLensDirection.back){
        _lensDirection = CameraLensDirection.front;
      }else{
        _lensDirection = CameraLensDirection.back;
      }
    });
    dispose();
    _controller = CameraController(
      CameraDescription(
        lensDirection: _lensDirection,
        name: "1",
        sensorOrientation: 0,
      ),
      ResolutionPreset.high,
    );
    setState(() {
      _initializeControllerFuture = _controller.initialize();
    });
  }

  void cameraMode() {
    setState(() {
      _isCameraEnabled = !_isCameraEnabled;
    });
    if (_isCameraEnabled) {
      dispose();
      _controller = CameraController(
        CameraDescription(
          lensDirection: _lensDirection,
          name: "1",
          sensorOrientation: 0,
        ),
        ResolutionPreset.medium,
      );
      setState(() {
        _initializeControllerFuture = _controller.initialize();
      });
    } else {
      dispose();
    }
    if (mounted){
      setState(() {});
    }
  }

  Future<String> takePic() async {
    if (_isCameraEnabled) {
      try {
          await _initializeControllerFuture;
          final image = await _controller.takePicture();
          final directory = await getApplicationDocumentsDirectory();
          final imagePath = '${directory.path}/frame.png';
          await image.saveTo(imagePath);
          return imagePath;
      } catch (e) {
        print(e);
      }
    }
    return "";
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<void>(
      future: _initializeControllerFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.done) {
          return CameraPreview(_controller);
        } else {
          return const Center(child: CircularProgressIndicator());
        }
      },
    );
  }
}

class FloraCam extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const FloraCam({
    super.key,
    required this.parent,
    required this.control,
    required this.backend
  });

  @override
  // ignore: library_private_types_in_public_api
  _FloraCamState createState() => _FloraCamState();
}

class _FloraCamState extends State<FloraCam> {
  late GlobalKey<CameraControlState> stateCamera;

  @override
  void initState() {
    super.initState();
    stateCamera = GlobalKey<CameraControlState>();
    widget.control.onRemove.clear();
    widget.control.onRemove.add(_onRemove);
  }

  void _onRemove() {
    debugPrint("PermissionHandler.remove($hashCode)");
    widget.backend.unsubscribeMethods(widget.control.id);
  }

  @override
  Widget build(BuildContext context) {
    // default camera settings
    final CameraControl fletCam = CameraControl(
      key: stateCamera,
      camera: const CameraDescription(
        lensDirection: CameraLensDirection.back,
        name: "1",
        sensorOrientation: 0,
      ),
    );

    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "camera_mode":
            stateCamera.currentState?.cameraMode();
            return "ok";
          case "switch_camera":
            stateCamera.currentState?.switchCamera();
            return "ok";
          case "take_picture":
            return stateCamera.currentState?.takePic();
        }
        return "";
      });
    }();
    return constrainedControl(
      context,
      fletCam,
      widget.parent,
      widget.control,
    );
  }
}
# Mobile Integration Guide

## Overview

This guide covers integrating Paniki with mobile applications using React Native and Flutter.

## React Native Integration

### Installation

```bash
# Install dependencies
npm install react-native-webrtc react-native-audio
# or
yarn add react-native-webrtc react-native-audio
```

### Basic Setup

```javascript
import {
  RTCPeerConnection,
  RTCIceCandidate,
  RTCSessionDescription,
  mediaDevices,
} from 'react-native-webrtc';

class PanikiMobileClient {
  constructor(serverUrl) {
    this.serverUrl = serverUrl;
    this.pc = new RTCPeerConnection({
      iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
      ],
    });
    this.setupWebRTC();
  }

  async setupWebRTC() {
    try {
      const stream = await mediaDevices.getUserMedia({
        audio: true,
        video: false,
      });

      stream.getTracks().forEach(track => {
        this.pc.addTrack(track, stream);
      });

      // Handle connection events
      this.pc.onicecandidate = this.handleIceCandidate;
      this.pc.ontrack = this.handleTrack;
    } catch (error) {
      console.error('Error setting up WebRTC:', error);
    }
  }

  // ... other methods
}
```

### React Native Component

```jsx
import React, { useEffect, useRef } from 'react';
import { View, Button, PermissionsAndroid } from 'react-native';
import { PanikiMobileClient } from './PanikiMobileClient';

const VoiceAssistant = () => {
  const clientRef = useRef(null);

  useEffect(() => {
    requestPermissions();
    setupClient();

    return () => {
      clientRef.current?.cleanup();
    };
  }, []);

  const requestPermissions = async () => {
    try {
      await PermissionsAndroid.requestMultiple([
        PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
      ]);
    } catch (error) {
      console.error('Error requesting permissions:', error);
    }
  };

  const setupClient = () => {
    clientRef.current = new PanikiMobileClient('wss://your-server.com');
  };

  const startRecording = async () => {
    try {
      await clientRef.current?.start();
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  const stopRecording = () => {
    clientRef.current?.stop();
  };

  return (
    <View>
      <Button title="Start" onPress={startRecording} />
      <Button title="Stop" onPress={stopRecording} />
    </View>
  );
};

export default VoiceAssistant;
```

## Flutter Integration

### Dependencies

```yaml
# pubspec.yaml
dependencies:
  flutter_webrtc: ^0.9.0
  web_socket_channel: ^2.4.0
```

### WebRTC Client

```dart
import 'package:flutter_webrtc/flutter_webrtc.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class PanikiFlutterClient {
  RTCPeerConnection? _peerConnection;
  MediaStream? _localStream;
  WebSocketChannel? _websocket;
  
  Future<void> initialize() async {
    final configuration = {
      'iceServers': [
        {'urls': 'stun:stun.l.google.com:19302'},
      ],
    };

    _peerConnection = await createPeerConnection(configuration);
    await _setupMediaStream();
    _connectWebSocket();
  }

  Future<void> _setupMediaStream() async {
    final constraints = {
      'audio': true,
      'video': false,
    };

    try {
      _localStream = await navigator.mediaDevices.getUserMedia(constraints);
      _localStream?.getTracks().forEach((track) {
        _peerConnection?.addTrack(track, _localStream!);
      });
    } catch (e) {
      print('Error getting user media: $e');
    }
  }

  void _connectWebSocket() {
    _websocket = WebSocketChannel.connect(
      Uri.parse('wss://your-server.com'),
    );

    _websocket?.stream.listen(
      (message) => _handleWebSocketMessage(message),
      onError: (error) => print('WebSocket error: $error'),
      onDone: () => print('WebSocket connection closed'),
    );
  }

  // ... other methods
}
```

### Flutter Widget

```dart
import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';

class VoiceAssistantWidget extends StatefulWidget {
  @override
  _VoiceAssistantWidgetState createState() => _VoiceAssistantWidgetState();
}

class _VoiceAssistantWidgetState extends State<VoiceAssistantWidget> {
  PanikiFlutterClient? _client;
  bool _isRecording = false;

  @override
  void initState() {
    super.initState();
    _setupClient();
  }

  Future<void> _setupClient() async {
    await _requestPermissions();
    _client = PanikiFlutterClient();
    await _client?.initialize();
  }

  Future<void> _requestPermissions() async {
    await Permission.microphone.request();
  }

  void _startRecording() async {
    try {
      await _client?.start();
      setState(() => _isRecording = true);
    } catch (e) {
      print('Error starting recording: $e');
    }
  }

  void _stopRecording() {
    _client?.stop();
    setState(() => _isRecording = false);
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton(
          onPressed: _isRecording ? _stopRecording : _startRecording,
          child: Text(_isRecording ? 'Stop' : 'Start'),
        ),
      ],
    );
  }

  @override
  void dispose() {
    _client?.dispose();
    super.dispose();
  }
}
```

## Audio Processing

### React Native Audio Processing

```javascript
import { AudioRecorder, AudioUtils } from 'react-native-audio';

class AudioProcessor {
  constructor() {
    this.audioPath = AudioUtils.DocumentDirectoryPath + '/recording.wav';
  }

  async prepareRecording() {
    await AudioRecorder.prepareRecordingAtPath(this.audioPath, {
      SampleRate: 16000,
      Channels: 1,
      AudioQuality: 'Low',
      AudioEncoding: 'wav',
    });
  }

  async startProcessing() {
    try {
      await this.prepareRecording();
      await AudioRecorder.startRecording();
      
      AudioRecorder.onProgress = (data) => {
        // Process audio data
        this.processAudioData(data);
      };
    } catch (error) {
      console.error('Error in audio processing:', error);
    }
  }

  processAudioData(data) {
    // Implement audio processing logic
  }
}
```

### Flutter Audio Processing

```dart
import 'package:flutter_sound/flutter_sound.dart';

class AudioProcessor {
  FlutterSoundRecorder? _recorder;
  
  Future<void> initialize() async {
    _recorder = FlutterSoundRecorder();
    await _recorder?.openRecorder();
    
    await _recorder?.setSubscriptionDuration(
      Duration(milliseconds: 10),
    );
  }

  Future<void> startProcessing() async {
    await _recorder?.startRecorder(
      toStream: true,
      codec: Codec.pcm16,
      numChannels: 1,
      sampleRate: 16000,
    );

    _recorder?.onProgress?.listen((event) {
      // Process audio data
      _processAudioData(event);
    });
  }

  void _processAudioData(RecordingDisposition event) {
    // Implement audio processing logic
  }
}
```

## Error Handling

### React Native Error Handling

```javascript
class ErrorHandler {
  static async handlePermissionError(error) {
    if (error.code === 'permission_denied') {
      // Handle permission denial
    }
  }

  static async handleAudioError(error) {
    // Handle audio errors
  }

  static async handleNetworkError(error) {
    // Handle network errors
  }
}
```

### Flutter Error Handling

```dart
class ErrorHandler {
  static Future<void> handlePermissionError(Exception error) async {
    // Handle permission errors
  }

  static Future<void> handleAudioError(Exception error) async {
    // Handle audio errors
  }

  static Future<void> handleNetworkError(Exception error) async {
    // Handle network errors
  }
}
```

## Platform-Specific Considerations

### iOS Configuration

```xml
<!-- Info.plist -->
<key>NSMicrophoneUsageDescription</key>
<string>We need access to your microphone for voice interaction</string>
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

### Android Configuration

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```
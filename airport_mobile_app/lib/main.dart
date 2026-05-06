import 'package:flutter/material.dart';

import 'screens/login_screen.dart';

void main() {
  runApp(const AirportApp());
}

class AirportApp extends StatelessWidget {
  const AirportApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Airport Internal App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontSize: 15),
          bodyMedium: TextStyle(fontSize: 14),
          bodySmall: TextStyle(fontSize: 12),
          titleLarge: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          titleMedium: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          titleSmall: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
        ),
      ),
      builder: (context, child) {
        return MediaQuery(
          data: MediaQuery.of(context).copyWith(
            textScaler: const TextScaler.linear(0.9),
          ),
          child: child!,
        );
      },
      home: const LoginScreen(),
    );
  }
}
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../config/api_config.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final String apiBaseUrl = ApiConfig.baseUrl;

  bool isLoading = true;
  String errorMessage = '';
  Map<String, dynamic>? employee;

  @override
  void initState() {
    super.initState();
    fetchProfile();
  }

  Future<void> fetchProfile() async {
    setState(() {
      isLoading = true;
      errorMessage = '';
    });

    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('access_token') ?? '';

      final response = await http.get(
        Uri.parse('$apiBaseUrl/api/profile'),
        headers: {'Authorization': 'Bearer $token'},
      );

      if (!mounted) return;

      if (response.statusCode == 200) {
        setState(() {
          employee = jsonDecode(response.body);
          isLoading = false;
        });
      } else {
        setState(() {
          errorMessage = 'Không lấy được thông tin cá nhân';
          isLoading = false;
        });
      }
    } catch (e) {
      if (!mounted) return;

      setState(() {
        errorMessage = 'Không kết nối được Backend API';
        isLoading = false;
      });
    }
  }

  Widget buildContent() {
    if (isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (errorMessage.isNotEmpty) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.wifi_off, size: 54, color: Colors.grey),
              const SizedBox(height: 12),
              Text(
                errorMessage,
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 16),
              FilledButton(
                onPressed: fetchProfile,
                child: const Text('Thử lại'),
              ),
            ],
          ),
        ),
      );
    }

    final data = employee!;

    return RefreshIndicator(
      onRefresh: fetchProfile,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            elevation: 2,
            color: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(18),
            ),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  const CircleAvatar(
                    radius: 42,
                    backgroundColor: Color(0xffe3f2fd),
                    child: Icon(Icons.person, size: 48, color: Colors.blue),
                  ),
                  const SizedBox(height: 14),
                  Text(
                    data['name'] ?? '',
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    data['position'] ?? '',
                    style: const TextStyle(color: Colors.grey),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 14),
          ProfileInfoItem(
            icon: Icons.badge,
            label: 'Mã nhân viên',
            value: data['code'] ?? '',
          ),
          ProfileInfoItem(
            icon: Icons.business,
            label: 'Phòng ban',
            value: data['department'] ?? '',
          ),
          ProfileInfoItem(
            icon: Icons.work,
            label: 'Chức vụ',
            value: data['position'] ?? '',
          ),
          ProfileInfoItem(
            icon: Icons.phone,
            label: 'Số điện thoại',
            value: data['phone'] ?? '',
          ),
          ProfileInfoItem(
            icon: Icons.email,
            label: 'Email',
            value: data['email'] ?? '',
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xfff4f7fb),
      appBar: AppBar(
        title: const Text('Cá nhân'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: buildContent(),
    );
  }
}

class ProfileInfoItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const ProfileInfoItem({
    super.key,
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      elevation: 1,
      color: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      child: ListTile(
        leading: Icon(icon, color: Colors.blue),
        title: Text(label),
        subtitle: Text(
          value,
          style: const TextStyle(
            fontWeight: FontWeight.w600,
            color: Colors.black87,
          ),
        ),
      ),
    );
  }
}

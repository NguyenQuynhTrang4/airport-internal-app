import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../config/api_config.dart';

class IncidentReportScreen extends StatefulWidget {
  const IncidentReportScreen({super.key});

  @override
  State<IncidentReportScreen> createState() => _IncidentReportScreenState();
}

class _IncidentReportScreenState extends State<IncidentReportScreen> {
  final titleController = TextEditingController();
  final locationController = TextEditingController();
  final descriptionController = TextEditingController();

  final String apiBaseUrl = ApiConfig.baseUrl;

  String selectedLevel = 'Bình thường';
  bool isLoading = false;

  Future<void> submitIncident() async {
    final title = titleController.text.trim();
    final location = locationController.text.trim();
    final description = descriptionController.text.trim();

    if (title.isEmpty || location.isEmpty || description.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Vui lòng nhập đầy đủ thông tin sự cố')),
      );
      return;
    }

    setState(() {
      isLoading = true;
    });

    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('access_token') ?? '';

      final response = await http.post(
        Uri.parse('$apiBaseUrl/api/incidents'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: jsonEncode({
          'title': title,
          'location': location,
          'level': selectedLevel,
          'description': description,
        }),
      );

      if (!mounted) return;

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Đã gửi báo cáo sự cố thành công')),
        );

        Navigator.pop(context, true);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Gửi thất bại: ${response.statusCode} - ${response.body}',
            ),
          ),
        );
      }
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Lỗi kết nối Backend: $e')));
    } finally {
      if (mounted) {
        setState(() {
          isLoading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    titleController.dispose();
    locationController.dispose();
    descriptionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xfff4f7fb),
      appBar: AppBar(
        title: const Text('Báo cáo sự cố'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            elevation: 2,
            color: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  TextField(
                    controller: titleController,
                    decoration: const InputDecoration(
                      labelText: 'Tiêu đề sự cố',
                      prefixIcon: Icon(Icons.title),
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 14),
                  TextField(
                    controller: locationController,
                    decoration: const InputDecoration(
                      labelText: 'Vị trí xảy ra',
                      prefixIcon: Icon(Icons.location_on),
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 14),
                  DropdownButtonFormField<String>(
                    value: selectedLevel,
                    decoration: const InputDecoration(
                      labelText: 'Mức độ',
                      prefixIcon: Icon(Icons.priority_high),
                      border: OutlineInputBorder(),
                    ),
                    items: const [
                      DropdownMenuItem(
                        value: 'Bình thường',
                        child: Text('Bình thường'),
                      ),
                      DropdownMenuItem(
                        value: 'Quan trọng',
                        child: Text('Quan trọng'),
                      ),
                      DropdownMenuItem(
                        value: 'Khẩn cấp',
                        child: Text('Khẩn cấp'),
                      ),
                    ],
                    onChanged: (value) {
                      setState(() {
                        selectedLevel = value!;
                      });
                    },
                  ),
                  const SizedBox(height: 14),
                  TextField(
                    controller: descriptionController,
                    maxLines: 5,
                    decoration: const InputDecoration(
                      labelText: 'Mô tả chi tiết',
                      alignLabelWithHint: true,
                      prefixIcon: Icon(Icons.description),
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 18),
                  SizedBox(
                    width: double.infinity,
                    height: 48,
                    child: FilledButton.icon(
                      onPressed: isLoading ? null : submitIncident,
                      icon: isLoading
                          ? const SizedBox(
                              width: 18,
                              height: 18,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                color: Colors.white,
                              ),
                            )
                          : const Icon(Icons.send),
                      label: Text(isLoading ? 'Đang gửi...' : 'Gửi báo cáo'),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

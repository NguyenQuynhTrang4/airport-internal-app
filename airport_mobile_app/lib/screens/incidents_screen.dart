import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import '../config/api_config.dart';
import 'incident_report_screen.dart';

class IncidentsScreen extends StatefulWidget {
  const IncidentsScreen({super.key});

  @override
  State<IncidentsScreen> createState() => _IncidentsScreenState();
}

class _IncidentsScreenState extends State<IncidentsScreen> {
  final String apiBaseUrl = ApiConfig.baseUrl;

  bool isLoading = true;
  String errorMessage = '';
  List<dynamic> incidents = [];

  @override
  void initState() {
    super.initState();
    fetchIncidents();
  }

  Future<void> fetchIncidents() async {
    setState(() {
      isLoading = true;
      errorMessage = '';
    });

    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('access_token') ?? '';

      final response = await http.get(
        Uri.parse('$apiBaseUrl/api/incidents'),
        headers: {'Authorization': 'Bearer $token'},
      );

      if (!mounted) return;

      if (response.statusCode == 200) {
        setState(() {
          incidents = jsonDecode(response.body);
          isLoading = false;
        });
      } else {
        setState(() {
          errorMessage = 'Không lấy được danh sách sự cố';
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

  Future<void> openReportScreen() async {
    await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const IncidentReportScreen()),
    );

    fetchIncidents();
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
                onPressed: fetchIncidents,
                child: const Text('Thử lại'),
              ),
            ],
          ),
        ),
      );
    }

    if (incidents.isEmpty) {
      return RefreshIndicator(
        onRefresh: fetchIncidents,
        child: ListView(
          children: const [
            SizedBox(height: 180),
            Icon(Icons.report_problem_outlined, size: 60, color: Colors.grey),
            SizedBox(height: 12),
            Center(
              child: Text(
                'Chưa có sự cố nào',
                style: TextStyle(color: Colors.grey),
              ),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: fetchIncidents,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: incidents.length,
        itemBuilder: (context, index) {
          final incident = incidents[index];

          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            elevation: 2,
            color: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const CircleAvatar(
                    backgroundColor: Color(0xffffebee),
                    child: Icon(Icons.report_problem, color: Colors.red),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          incident['title'] ?? '',
                          style: const TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          'Vị trí: ${incident['location'] ?? ''}',
                          style: const TextStyle(
                            fontSize: 13,
                            color: Colors.black87,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Mức độ: ${incident['level'] ?? ''}',
                          style: const TextStyle(
                            fontSize: 13,
                            color: Colors.black87,
                          ),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          incident['description'] ?? '',
                          style: const TextStyle(
                            fontSize: 13,
                            color: Colors.black87,
                            height: 1.35,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 10,
                            vertical: 5,
                          ),
                          decoration: BoxDecoration(
                            color: const Color(0xffe3f2fd),
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            incident['status'] ?? '',
                            style: const TextStyle(
                              fontSize: 12,
                              color: Colors.blue,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xfff4f7fb),
      appBar: AppBar(
        title: const Text('Danh sách sự cố'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: buildContent(),
      floatingActionButton: FloatingActionButton(
        onPressed: openReportScreen,
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        child: const Icon(Icons.add),
      ),
    );
  }
}

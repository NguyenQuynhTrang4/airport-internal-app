import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../config/api_config.dart';

class ChatbotScreen extends StatefulWidget {
  const ChatbotScreen({super.key});

  @override
  State<ChatbotScreen> createState() => _ChatbotScreenState();
}

class _ChatbotScreenState extends State<ChatbotScreen> {
  final questionController = TextEditingController();

  final String apiBaseUrl = ApiConfig.baseUrl;
  bool isLoading = false;

  final List<Map<String, String>> messages = [
    {
      'sender': 'bot',
      'text':
          'Xin chào! Tôi là chatbot nội bộ sân bay. Bạn có thể hỏi về quy trình, ca trực, tài liệu hoặc thông báo.',
    },
  ];

  Future<void> sendMessage() async {
    final question = questionController.text.trim();

    if (question.isEmpty || isLoading) {
      return;
    }

    setState(() {
      messages.add({'sender': 'user', 'text': question});

      questionController.clear();
      isLoading = true;
    });

    try {
      final response = await http.post(
        Uri.parse('$apiBaseUrl/api/chatbot/ask'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'question': question}),
      );

      if (!mounted) return;

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        setState(() {
          messages.add({
            'sender': 'bot',
            'text': data['answer'] ?? 'Không có câu trả lời.',
          });
        });
      } else {
        setState(() {
          messages.add({
            'sender': 'bot',
            'text': 'Backend không xử lý được câu hỏi này.',
          });
        });
      }
    } catch (e) {
      if (!mounted) return;

      setState(() {
        messages.add({
          'sender': 'bot',
          'text': 'Không kết nối được Backend API.',
        });
      });
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
    questionController.dispose();
    super.dispose();
  }

  Widget buildMessageBubble(Map<String, String> message) {
    final isUser = message['sender'] == 'user';

    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.all(12),
        constraints: const BoxConstraints(maxWidth: 280),
        decoration: BoxDecoration(
          color: isUser ? Colors.blue : Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            if (!isUser)
              const BoxShadow(
                color: Colors.black12,
                blurRadius: 4,
                offset: Offset(0, 2),
              ),
          ],
        ),
        child: Text(
          message['text']!,
          style: TextStyle(
            fontSize: 14,
            color: isUser ? Colors.white : Colors.black87,
            height: 1.35,
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xfff4f7fb),
      appBar: AppBar(
        title: const Text('Chatbot'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: messages.length + (isLoading ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == messages.length) {
                  return buildMessageBubble({
                    'sender': 'bot',
                    'text': 'Đang trả lời...',
                  });
                }

                return buildMessageBubble(messages[index]);
              },
            ),
          ),
          Container(
            color: Colors.white,
            padding: const EdgeInsets.all(12),
            child: SafeArea(
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: questionController,
                      decoration: InputDecoration(
                        hintText: 'Nhập câu hỏi...',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                        ),
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 10,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  CircleAvatar(
                    backgroundColor: Colors.blue,
                    child: IconButton(
                      onPressed: isLoading ? null : sendMessage,
                      icon: isLoading
                          ? const SizedBox(
                              width: 18,
                              height: 18,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                color: Colors.white,
                              ),
                            )
                          : const Icon(Icons.send, color: Colors.white),
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

import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:googleapis/gmail/v1.dart';
import 'package:googleapis_auth/googleapis_auth.dart' as auth;
import 'package:http/http.dart' as http;

class Home extends StatefulWidget {
  @override
  HomeState createState() => HomeState();
}

class HomeState extends State<Home> {
  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['https://www.googleapis.com/auth/gmail.readonly'],
  );

  List<String> emails = [];

  Future<void> _signInAndFetchEmails() async {
    try {
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      if (googleUser == null) return;

      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
      final auth.AuthClient authClient = auth.authenticatedClient(
        http.Client(),
        auth.AccessCredentials(
          auth.AccessToken(
            'Bearer',
            googleAuth.accessToken!,
            DateTime.now().toUtc().add(Duration(hours: 1)),
          ),
          googleAuth.idToken,
          ['https://www.googleapis.com/auth/gmail.readonly'],
        ),
      );

      final gmailApi = GmailApi(authClient);
      final messages = await gmailApi.users.messages.list('me').then((res) => res.messages);

      if (messages != null) {
        List<String> emailSnippets = [];
        for (var msg in messages) {
          var message = await gmailApi.users.messages.get('me', msg.id!);
          emailSnippets.add(message.snippet ?? 'No content');
        }
        print("Emails: $emailSnippets");
        setState(() {
          emails = emailSnippets;
        });
      }
    } catch (error) {
      print("Error: $error");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Gmail Reader')),
      body: Column(
        children: [
          ElevatedButton(
            onPressed: _signInAndFetchEmails,
            child: Text('Sign in & Read Emails'),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: emails.length,
              itemBuilder: (context, index) {
                return ListTile(title: Text(emails[index]));
              },
            ),
          ),
        ],
      ),
    );
  }
}
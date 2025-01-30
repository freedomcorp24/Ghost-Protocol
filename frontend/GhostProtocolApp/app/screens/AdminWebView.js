/**
 * GhostProtocolApp/app/screens/AdminWebView.js
 */
import React from 'react';
import {View, StyleSheet} from 'react-native';
import WebView from 'react-native-webview';

function AdminWebView() {
  return (
    <View style={{flex:1, backgroundColor:'#000'}}>
      <WebView source={{ uri: 'https://yourdomain.com/admin-panel' }} />
    </View>
  );
}

export default AdminWebView;

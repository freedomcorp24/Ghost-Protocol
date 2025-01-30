/**
 * GhostProtocolApp/app/screens/LoginScreen.js
 */
import React, {useState} from 'react';
import {View, Text, TextInput, TouchableOpacity, Alert} from 'react-native';
import globalStyles from '../styles/globalStyles';
import {loginApi} from '../api/auth';

function LoginScreen({navigation}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await loginApi(username, password);
      if (response.success) {
        // If decoyMode is in the response, store it in some global or AsyncStorage if needed
        navigation.replace('Home');
      } else {
        Alert.alert('Login Error', response.message || 'Invalid credentials');
      }
    } catch (err) {
      Alert.alert('Error', err.message);
    }
  };

  return (
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>Ghost Protocol - Login</Text>
      <TextInput
        style={globalStyles.input}
        placeholder="Username"
        placeholderTextColor="#888"
        onChangeText={setUsername}
        value={username}
      />
      <TextInput
        style={globalStyles.input}
        placeholder="Password (or Decoy Password)"
        placeholderTextColor="#888"
        secureTextEntry
        onChangeText={setPassword}
        value={password}
      />
      <TouchableOpacity style={globalStyles.button} onPress={handleLogin}>
        <Text style={globalStyles.buttonText}>Login</Text>
      </TouchableOpacity>
      <TouchableOpacity
        style={globalStyles.button}
        onPress={() => navigation.navigate('Register')}
      >
        <Text style={globalStyles.buttonText}>Register</Text>
      </TouchableOpacity>
    </View>
  );
}

export default LoginScreen;

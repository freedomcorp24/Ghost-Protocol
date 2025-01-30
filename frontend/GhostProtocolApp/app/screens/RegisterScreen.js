/**
 * GhostProtocolApp/app/screens/RegisterScreen.js
 */
import React, {useState} from 'react';
import {View, Text, TextInput, TouchableOpacity, Alert} from 'react-native';
import globalStyles from '../styles/globalStyles';
import {registerApi} from '../api/auth';

function RegisterScreen({navigation}) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPass, setConfirmPass] = useState('');

  const handleRegister = async () => {
    if (password !== confirmPass) {
      Alert.alert('Error', 'Passwords do not match');
      return;
    }
    try {
      const res = await registerApi(username, email, password);
      if (res.success) {
        Alert.alert('Registration Success', 'Recovery Key: ' + (res.recoveryKey || 'N/A'));
        navigation.replace('Login');
      } else {
        Alert.alert('Error', res.message || 'Server error');
      }
    } catch (err) {
      Alert.alert('Error', err.message);
    }
  };

  return (
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>Register</Text>
      <TextInput
        style={globalStyles.input}
        placeholder="Username"
        placeholderTextColor="#888"
        onChangeText={setUsername}
        value={username}
      />
      <TextInput
        style={globalStyles.input}
        placeholder="Email"
        placeholderTextColor="#888"
        onChangeText={setEmail}
        value={email}
      />
      <TextInput
        style={globalStyles.input}
        placeholder="Password"
        placeholderTextColor="#888"
        secureTextEntry
        onChangeText={setPassword}
        value={password}
      />
      <TextInput
        style={globalStyles.input}
        placeholder="Confirm Password"
        placeholderTextColor="#888"
        secureTextEntry
        onChangeText={setConfirmPass}
        value={confirmPass}
      />
      <TouchableOpacity style={globalStyles.button} onPress={handleRegister}>
        <Text style={globalStyles.buttonText}>Register</Text>
      </TouchableOpacity>
    </View>
  );
}

export default RegisterScreen;

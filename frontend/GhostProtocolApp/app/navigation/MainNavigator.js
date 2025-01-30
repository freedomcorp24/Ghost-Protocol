/**
 * GhostProtocolApp/app/navigation/MainNavigator.js
 */
import React from 'react';
import {createNativeStackNavigator} from '@react-navigation/native-stack';

import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import HomeScreen from '../screens/HomeScreen';
import ChatScreen from '../screens/ChatScreen';
import VaultScreen from '../screens/VaultScreen';
import SubscriptionScreen from '../screens/SubscriptionScreen';
import AdminWebView from '../screens/AdminWebView';
import SettingsScreen from '../screens/SettingsScreen';
import TermsScreen from '../screens/TermsScreen';
import BlockScreen from '../screens/BlockScreen';
import QrCodeScreen from '../screens/QrCodeScreen';
import CallScreen from '../screens/CallScreen';

const Stack = createNativeStackNavigator();

function MainNavigator(){
  return(
    <Stack.Navigator initialRouteName="Login">
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="Register" component={RegisterScreen} />
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Chat" component={ChatScreen} />
      <Stack.Screen name="Vault" component={VaultScreen} />
      <Stack.Screen name="Subscription" component={SubscriptionScreen} />
      <Stack.Screen name="AdminWebView" component={AdminWebView} />
      <Stack.Screen name="Settings" component={SettingsScreen} />
      <Stack.Screen name="Terms" component={TermsScreen} />
      <Stack.Screen name="BlockScreen" component={BlockScreen} />
      <Stack.Screen name="QrCodeScreen" component={QrCodeScreen} />
      <Stack.Screen name="CallScreen" component={CallScreen} />
    </Stack.Navigator>
  );
}

export default MainNavigator;

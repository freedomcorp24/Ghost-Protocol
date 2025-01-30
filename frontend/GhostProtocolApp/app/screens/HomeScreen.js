import React, {useEffect, useState} from 'react';
import {View, Text, TouchableOpacity} from 'react-native';
import globalStyles from '../styles/globalStyles';
import {getArchivedUnreadCountApi} from '../api/chat'; // if you have an endpoint
import AsyncStorage from '@react-native-async-storage/async-storage';

function HomeScreen({navigation}){
  const [archivedCount, setArchivedCount] = useState(0);

  useEffect(()=>{
    loadArchivedCount();
  },[]);

  const loadArchivedCount = async()=>{
    let res = await getArchivedUnreadCountApi();
    if(res.success){
      setArchivedCount(res.count);
    }
  };

  const handleLogout= async()=>{
    await AsyncStorage.clear();
    navigation.replace('Login');
  };

  return(
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>Ghost Protocol - Home</Text>
      <TouchableOpacity style={globalStyles.button} onPress={()=>navigation.navigate('Chat')}>
        <Text style={globalStyles.buttonText}>Go to Chat</Text>
      </TouchableOpacity>
      <TouchableOpacity style={globalStyles.button} onPress={()=>navigation.navigate('Vault')}>
        <Text style={globalStyles.buttonText}>Vault</Text>
      </TouchableOpacity>
      <TouchableOpacity style={globalStyles.button} onPress={()=>navigation.navigate('Subscription')}>
        <Text style={globalStyles.buttonText}>Subscription</Text>
      </TouchableOpacity>
      <TouchableOpacity style={globalStyles.button} onPress={()=>navigation.navigate('Settings')}>
        <Text style={globalStyles.buttonText}>Settings</Text>
      </TouchableOpacity>
      <TouchableOpacity style={globalStyles.button} onPress={()=>navigation.navigate('AdminWebView')}>
        <Text style={globalStyles.buttonText}>Admin Panel</Text>
      </TouchableOpacity>
      <TouchableOpacity style={globalStyles.button} onPress={()=>navigation.navigate('BlockScreen')}>
        <Text style={globalStyles.buttonText}>Block/Unblock</Text>
      </TouchableOpacity>
      <TouchableOpacity style={globalStyles.button} onPress={()=>navigation.navigate('QrCodeScreen')}>
        <Text style={globalStyles.buttonText}>QR Contacts</Text>
      </TouchableOpacity>
      <TouchableOpacity style={globalStyles.button} onPress={()=>navigation.navigate('CallScreen')}>
        <Text style={globalStyles.buttonText}>Calls</Text>
      </TouchableOpacity>
      <Text style={globalStyles.text}>Archived Unread: {archivedCount}</Text>

      <TouchableOpacity style={[globalStyles.button,{backgroundColor:'red'}]} onPress={handleLogout}>
        <Text style={globalStyles.buttonText}>Logout</Text>
      </TouchableOpacity>
    </View>
  );
}

export default HomeScreen;

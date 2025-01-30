/**
 * GhostProtocolApp/app/screens/CallScreen.js
 */
import React, {useState, useRef} from 'react';
import {View, Text, TouchableOpacity, StyleSheet, Alert} from 'react-native';
import globalStyles from '../styles/globalStyles';
import {createCallApi, joinCallApi} from '../api/call';
import {NodeCameraView} from 'react-native-webrtc'; // or some approach
// For PiP:
import RNAndroidPip from 'react-native-pip-android';

function CallScreen(){
  const [sessionId, setSessionId] = useState('');

  const handleCreateCall= async(isGroup=false)=>{
    let res= await createCallApi(isGroup);
    if(res.success){
      setSessionId(res.session_id);
      Alert.alert('Created call', `Session: ${res.session_id}`);
      // startLocalMedia etc
    }
  };

  const handleJoin= async()=>{
    let userInput = prompt('Enter session ID:');
    if(!userInput) return;
    let res= await joinCallApi(userInput);
    if(res.success){
      setSessionId(userInput);
      Alert.alert('Joined call', userInput);
      // do local media
    }
  };

  const enterPip= ()=>{
    if(RNAndroidPip) RNAndroidPip.enterPictureInPictureMode();
  };

  return(
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>Calls</Text>
      <TouchableOpacity style={globalStyles.button} onPress={()=>handleCreateCall(false)}>
        <Text style={globalStyles.buttonText}>Create 1-on-1</Text>
      </TouchableOpacity>
      <TouchableOpacity style={globalStyles.button} onPress={()=>handleCreateCall(true)}>
        <Text style={globalStyles.buttonText}>Create Group Call</Text>
      </TouchableOpacity>
      <TouchableOpacity style={globalStyles.button} onPress={handleJoin}>
        <Text style={globalStyles.buttonText}>Join Call</Text>
      </TouchableOpacity>
      <TouchableOpacity style={globalStyles.button} onPress={enterPip}>
        <Text style={globalStyles.buttonText}>Enter PiP</Text>
      </TouchableOpacity>
      <Text style={globalStyles.text}>Current Session: {sessionId}</Text>
      {/* We’d integrate react-native-webrtc or actual call UI here */}
    </View>
  );
}

export default CallScreen;

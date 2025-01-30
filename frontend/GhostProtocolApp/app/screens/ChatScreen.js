/**
 * GhostProtocolApp/app/screens/ChatScreen.js
 */
import React, {useState, useEffect} from 'react';
import {View, Text, TextInput, TouchableOpacity, FlatList, Alert} from 'react-native';
import globalStyles from '../styles/globalStyles';
import AudioRecorderPlayer from 'react-native-audio-recorder-player';
import {fetchChatMessagesApi, sendEphemeralMessageApi} from '../api/chat';

function ChatScreen() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [recording, setRecording] = useState(false);
  const audioRecorderPlayer = new AudioRecorderPlayer();

  useEffect(() => {
    loadMessages();
  }, []);

  const loadMessages = async () => {
    try {
      const res = await fetchChatMessagesApi();
      if (res.success) {
        setMessages(res.messages);
      }
    } catch (err) {
      console.log(err);
    }
  };

  const handleSend = async () => {
    if (!inputText.trim()) return;
    try {
      const res = await sendEphemeralMessageApi({ content: inputText });
      if (res.success) {
        setInputText('');
        loadMessages();
      }
    } catch (err) {
      Alert.alert('Error', err.message);
    }
  };

  const startRecord = async() => {
    try {
      const path = await audioRecorderPlayer.startRecorder();
      setRecording(true);
    } catch (err) {
      console.log(err);
    }
  };

  const stopRecord = async() => {
    try {
      const result = await audioRecorderPlayer.stopRecorder();
      audioRecorderPlayer.removeRecordBackListener();
      setRecording(false);
      // Now upload the file as ephemeral attachment
      const res = await sendEphemeralMessageApi({ attachmentFilePath: result });
      if (res.success) {
        loadMessages();
      }
    } catch (err) {
      console.log(err);
    }
  };

  const renderItem = ({item}) => (
    <View style={{padding:8, borderWidth:1, borderColor:'#555', marginBottom:8}}>
      <Text style={[globalStyles.text, {fontWeight:'bold'}]}>{item.senderUsername}</Text>
      <Text style={globalStyles.text}>{item.content}</Text>
      {item.attachmentUrl && (
        <TouchableOpacity onPress={()=>playAudio(item.attachmentUrl)}>
          <Text style={{color:'yellow'}}>Play Voice Msg</Text>
        </TouchableOpacity>
      )}
    </View>
  );

  const playAudio = (url) => {
    // You might handle streaming the file or downloading locally
    Alert.alert('Play Audio', 'Voice message from ' + url);
  };

  return (
    <View style={globalStyles.container}>
      <FlatList
        data={messages}
        keyExtractor={msg=>String(msg.id)}
        renderItem={renderItem}
        style={{flex:1}}
      />
      <View style={{flexDirection:'row', alignItems:'center'}}>
        <TextInput
          style={[globalStyles.input, {flex:1}]}
          placeholder="Type a message"
          placeholderTextColor="#888"
          onChangeText={setInputText}
          value={inputText}
        />
        <TouchableOpacity style={globalStyles.button} onPress={handleSend}>
          <Text style={globalStyles.buttonText}>Send</Text>
        </TouchableOpacity>
      </View>
      <View style={{flexDirection:'row', justifyContent:'space-between'}}>
        <TouchableOpacity
          style={[globalStyles.button, {backgroundColor: recording?'red':'#339966'}]}
          onPress={recording? stopRecord: startRecord}
        >
          <Text style={globalStyles.buttonText}>
            {recording? 'Stop' : 'Record'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

export default ChatScreen;

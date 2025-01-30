/**
 * GhostProtocolApp/app/screens/BlockScreen.js
 * UI for listing blocklist, blocking/unblocking
 */
import React, {useEffect, useState} from 'react';
import {View, Text, TextInput, TouchableOpacity, Alert} from 'react-native';
import globalStyles from '../styles/globalStyles';
import {fetchBlocklist, blockUser, unblockUser} from '../api/block';

function BlockScreen(){
  const [blocks, setBlocks] = useState([]);
  const [blockIdInput, setBlockIdInput] = useState('');

  useEffect(()=>{
    loadBlocks();
  },[]);

  const loadBlocks= async()=>{
    let res= await fetchBlocklist();
    if(res.success){
      setBlocks(res.blocks);
    } else {
      Alert.alert('Error', res.message);
    }
  };

  const handleBlock= async()=>{
    if(!blockIdInput.trim()) return;
    let res= await blockUser(blockIdInput);
    if(res.success){
      setBlockIdInput('');
      loadBlocks();
    } else {
      Alert.alert('Error', res.message);
    }
  };

  const handleUnblock= async(bId)=>{
    let res= await unblockUser(bId);
    if(res.success){
      loadBlocks();
    } else {
      Alert.alert('Error', res.message);
    }
  };

  return(
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>Block/Unblock Users</Text>
      {blocks.map(b=>(
        <View key={b.blockId} style={{borderWidth:1, borderColor:'#555',padding:8, marginBottom:8}}>
          <Text style={globalStyles.text}>Blocked: {b.blockedName}</Text>
          <TouchableOpacity style={globalStyles.button} onPress={()=>handleUnblock(b.blockId)}>
            <Text style={globalStyles.buttonText}>Unblock</Text>
          </TouchableOpacity>
        </View>
      ))}
      <TextInput
        style={globalStyles.input}
        placeholder="Enter userId to block"
        placeholderTextColor="#888"
        value={blockIdInput}
        onChangeText={setBlockIdInput}
      />
      <TouchableOpacity style={globalStyles.button} onPress={handleBlock}>
        <Text style={globalStyles.buttonText}>Block User</Text>
      </TouchableOpacity>
    </View>
  );
}

export default BlockScreen;

/**
 * GhostProtocolApp/app/screens/VaultScreen.js
 * Minimal vault with ephemeral notes, password entries, etc.
 */
import React, {useState, useEffect} from 'react';
import {View, Text, TextInput, TouchableOpacity, FlatList, Alert} from 'react-native';
import globalStyles from '../styles/globalStyles';
import {fetchVaultItemsApi, createVaultItemApi} from '../api/chat';

function VaultScreen() {
  const [items, setItems] = useState([]);
  const [newNote, setNewNote] = useState('');

  useEffect(() => {
    loadVault();
  }, []);

  const loadVault = async() => {
    try {
      const res = await fetchVaultItemsApi();
      if (res.success) {
        setItems(res.items);
      }
    } catch(err){
      console.log(err);
    }
  };

  const handleAddNote = async() => {
    if(!newNote.trim()) return;
    try {
      const res = await createVaultItemApi({ item_type: 'note', data: newNote });
      if(res.success) {
        setNewNote('');
        loadVault();
      }
    } catch(err){
      Alert.alert('Error', err.message);
    }
  };

  const renderItem = ({item})=>(
    <View style={{borderWidth:1, borderColor:'#333', padding:8, marginBottom:8}}>
      <Text style={globalStyles.text}>
        {item.item_type.toUpperCase()}: {item.data}
      </Text>
    </View>
  );

  return (
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>Vault</Text>
      <FlatList
        data={items}
        keyExtractor={i=>String(i.id)}
        renderItem={renderItem}
      />
      <TextInput
        style={globalStyles.input}
        placeholder="Add a note"
        placeholderTextColor="#888"
        value={newNote}
        onChangeText={setNewNote}
      />
      <TouchableOpacity style={globalStyles.button} onPress={handleAddNote}>
        <Text style={globalStyles.buttonText}>Add Note</Text>
      </TouchableOpacity>
    </View>
  );
}

export default VaultScreen;

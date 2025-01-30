/**
 * GhostProtocolApp/app/api/chat.js
 */
import {getBaseUrl} from '../utils/torToggle';

// fetch ephemeral messages
export async function fetchChatMessagesApi() {
  try {
    const url = getBaseUrl() + '/messaging/chatList'; // adjust to your actual route
    let res = await fetch(url);
    let json = await res.json();
    return json;
  } catch(err) {
    return {success:false, message: err.message};
  }
}

export async function sendEphemeralMessageApi({ content='', attachmentFilePath=null }) {
  try {
    const url = getBaseUrl() + '/messaging/sendMessage';
    let formData = new FormData();
    formData.append('content', content);
    if(attachmentFilePath) {
      formData.append('attachment', {
        uri: 'file://' + attachmentFilePath,
        type: 'audio/aac', // or whatever
        name: 'voiceMessage.aac'
      });
    }
    let res = await fetch(url, {
      method:'POST',
      body: formData
    });
    let json = await res.json();
    return json;
  } catch(err){
    return {success:false, message: err.message};
  }
}

// Vault
export async function fetchVaultItemsApi() {
  try {
    let res = await fetch(getBaseUrl() + '/messaging/vaultList');
    return await res.json();
  } catch(err){
    return {success:false, message:err.message};
  }
}

export async function createVaultItemApi({item_type, data}) {
  try {
    let formData = new FormData();
    formData.append('item_type', item_type);
    formData.append('data', data);
    let res = await fetch(getBaseUrl() + '/messaging/vaultCreate', {
      method:'POST',
      body: formData
    });
    return await res.json();
  } catch(err){
    return {success:false, message:err.message};
  }
}

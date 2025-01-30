import {getBaseUrl} from '../utils/torToggle';

export async function fetchBlocklist(){
  try {
    let url = getBaseUrl() + '/accounts/webBlockList';
    let res = await fetch(url);
    return await res.json();
  } catch(err){
    return {success:false, message:err.message};
  }
}

export async function blockUser(blockedId){
  try {
    let fd = new FormData();
    fd.append('blocked_id', blockedId);
    let url = getBaseUrl() + '/accounts/webBlockAdd';
    let res = await fetch(url,{method:'POST', body:fd});
    return await res.json();
  } catch(err){
    return {success:false, message:err.message};
  }
}

export async function unblockUser(blockId){
  try {
    let fd = new FormData();
    fd.append('block_id', blockId);
    let url = getBaseUrl() + '/accounts/webBlockRemove';
    let res = await fetch(url, {method:'POST', body:fd});
    return await res.json();
  } catch(err){
    return {success:false, message:err.message};
  }
}

/**
 * GhostProtocolApp/app/api/auth.js
 */
import {getBaseUrl} from '../utils/torToggle';

export async function loginApi(username, password) {
  try {
    const url = getBaseUrl() + '/accounts/loginApi'; // your endpoint
    let res = await fetch(url, {
      method:'POST',
      headers:{ 'Content-Type': 'application/json' },
      body: JSON.stringify({username, password})
    });
    let json = await res.json();
    return json;
  } catch(err) {
    return {success:false, message: err.message};
  }
}

export async function registerApi(username, email, password) {
  try {
    const url = getBaseUrl() + '/accounts/registerApi';
    let res = await fetch(url, {
      method:'POST',
      headers:{ 'Content-Type':'application/json'},
      body: JSON.stringify({username, email, password})
    });
    let json = await res.json();
    return json;
  } catch(err) {
    return {success:false, message:err.message};
  }
}

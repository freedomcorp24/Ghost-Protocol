/**
 * GhostProtocolApp/app/api/payments.js
 */
import {getBaseUrl} from '../utils/torToggle';

export async function fetchTiersApi() {
  try {
    let url = getBaseUrl() + '/payments/tiers';
    let res = await fetch(url);
    let json = await res.json();
    return json;
  } catch(err){
    return {success:false, message: err.message};
  }
}

export async function createPaymentApi(tierId, {currency, amount}) {
  try {
    let url = getBaseUrl() + `/payments/payment/${tierId}`;
    let formData = new FormData();
    formData.append('currency', currency);
    formData.append('amount', amount);
    // or JSON approach
    let res = await fetch(url, {
      method: 'POST',
      body: formData
    });
    return await res.json();
  } catch(err){
    return {success:false, message: err.message};
  }
}

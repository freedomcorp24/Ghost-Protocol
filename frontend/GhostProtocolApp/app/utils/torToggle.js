import {API_BASE_URL, TOR_API_BASE_URL} from '@env';

let useTor=false;

export function toggleTor(on){
  useTor=on;
}

export function getBaseUrl(){
  return useTor? TOR_API_BASE_URL : API_BASE_URL;
}

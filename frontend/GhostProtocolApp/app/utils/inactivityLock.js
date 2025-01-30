import {AppState} from 'react-native';
import {Alert} from 'react-native';

let inactivityTimer=null;
let lastState='active';

export function startInactivityTimer(){
  AppState.addEventListener('change', handleStateChange);
  resetTimer();
}

export function stopInactivityTimer(){
  AppState.removeEventListener('change', handleStateChange);
  clearTimeout(inactivityTimer);
}

function handleStateChange(nextState){
  if(nextState==='active'){
    resetTimer();
  } else {
    clearTimeout(inactivityTimer);
  }
  lastState = nextState;
}

function resetTimer(){
  clearTimeout(inactivityTimer);
  inactivityTimer = setTimeout(()=>{
    Alert.alert('Auto Lock','App locked due to inactivity. Please re-login');
    // you can do a logout or navigate to lock screen
  }, 5*60*1000); // 5 minutes
}

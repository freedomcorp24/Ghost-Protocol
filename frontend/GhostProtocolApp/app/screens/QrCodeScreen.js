/**
 * GhostProtocolApp/app/screens/QrCodeScreen.js
 */
import React, {useState} from 'react';
import {View, Text, TouchableOpacity} from 'react-native';
import globalStyles from '../styles/globalStyles';
import QRCode from 'react-native-qrcode-svg';
// for scanning:
import {RNCamera} from 'react-native-camera';

function QrCodeScreen(){
  const [myGhostId, setMyGhostId] = useState('GHOST12345');
  const [scanMode, setScanMode] = useState(false);
  const [scanResult, setScanResult] = useState('');

  const handleBarCodeRead= (e)=>{
    setScanMode(false);
    setScanResult(e.data);
    // parse e.data to add contact or something
  };

  return(
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>QR Code</Text>
      {!scanMode && (
        <View style={{alignItems:'center', marginBottom:16}}>
          <QRCode value={`ghostprotocol://addContact?ghostId=${myGhostId}`} size={200}/>
        </View>
      )}

      {scanMode?(
        <RNCamera
          style={{flex:1}}
          onBarCodeRead={handleBarCodeRead}
        />
      ):(
        <View>
          <Text style={globalStyles.text}>Scan result: {scanResult}</Text>
          <TouchableOpacity style={globalStyles.button} onPress={()=>setScanMode(true)}>
            <Text style={globalStyles.buttonText}>Scan QR</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
}

export default QrCodeScreen;

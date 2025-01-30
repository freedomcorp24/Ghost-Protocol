/**
 * GhostProtocolApp/app/screens/SettingsScreen.js
 */
import React, {useState} from 'react';
import {View, Text, Switch, TouchableOpacity} from 'react-native';
import globalStyles from '../styles/globalStyles';
import {toggleTor, getBaseUrl} from '../utils/torToggle';

function SettingsScreen() {
  const [useTor, setUseTor] = useState(false);

  const handleTorSwitch = (val) => {
    setUseTor(val);
    toggleTor(val);
  };

  return (
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>Settings</Text>
      <View style={{flexDirection:'row', alignItems:'center', marginBottom:12}}>
        <Text style={globalStyles.text}>Use Tor?</Text>
        <Switch
          value={useTor}
          onValueChange={handleTorSwitch}
        />
      </View>
      <Text style={globalStyles.text}>Current Base URL: {getBaseUrl()}</Text>
    </View>
  );
}

export default SettingsScreen;

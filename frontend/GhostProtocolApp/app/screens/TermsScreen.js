/**
 * GhostProtocolApp/app/screens/TermsScreen.js
 */
import React from 'react';
import {View, Text, ScrollView} from 'react-native';
import globalStyles from '../styles/globalStyles';

function TermsScreen() {
  return (
    <ScrollView style={globalStyles.container}>
      <Text style={globalStyles.title}>Ghost Protocol - Terms of Service</Text>
      <Text style={globalStyles.text}>
        {`Add your final TOS here...
- Ephemeral encryption disclaimers
- Liability disclaimers
- Payment disclaimers
etc.
`}
      </Text>
      <Text style={[globalStyles.text, {marginTop:16, fontWeight:'bold'}]}>
        Privacy Policy
      </Text>
      <Text style={globalStyles.text}>
        {`Add your privacy policy content here...
We do ephemeral chat, minimal logs, etc.
`}
      </Text>
    </ScrollView>
  );
}

export default TermsScreen;

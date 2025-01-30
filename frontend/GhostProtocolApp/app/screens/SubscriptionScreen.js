/**
 * GhostProtocolApp/app/screens/SubscriptionScreen.js
 */
import React, {useState, useEffect} from 'react';
import {View, Text, TouchableOpacity, Alert} from 'react-native';
import globalStyles from '../styles/globalStyles';
import {fetchTiersApi, createPaymentApi} from '../api/payments';

function SubscriptionScreen() {
  const [tiers, setTiers] = useState([]);

  useEffect(() => {
    loadTiers();
  }, []);

  const loadTiers = async() => {
    try {
      const res = await fetchTiersApi();
      if(res.success){
        setTiers(res.tiers);
      }
    } catch(err){
      Alert.alert('Error', err.message);
    }
  };

  const handleBuy = async(tierId) => {
    try {
      const payRes = await createPaymentApi(tierId, { currency:'BTC', amount:'0.01' });
      if(payRes.success){
        Alert.alert('Success','Payment created. Wait for confirmation.');
      } else {
        Alert.alert('Error', payRes.message||'Server error');
      }
    } catch(err){
      Alert.alert('Error', err.message);
    }
  };

  return (
    <View style={globalStyles.container}>
      <Text style={globalStyles.title}>Subscription Tiers</Text>
      {tiers.map((t)=>(
        <View key={t.id} style={{borderWidth:1, borderColor:'#333', marginBottom:8, padding:8}}>
          <Text style={globalStyles.text}>{t.name} - {t.storage_gb}GB</Text>
          <Text style={globalStyles.text}>Monthly: €{t.monthly_price_eur}</Text>
          <TouchableOpacity style={globalStyles.button} onPress={()=>handleBuy(t.id)}>
            <Text style={globalStyles.buttonText}>Buy Monthly</Text>
          </TouchableOpacity>
        </View>
      ))}
    </View>
  );
}

export default SubscriptionScreen;

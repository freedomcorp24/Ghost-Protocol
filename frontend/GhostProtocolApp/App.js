/**
 * GhostProtocolApp/App.js
 */
import React, {useEffect} from 'react';
import {SafeAreaView, StatusBar, StyleSheet, AppState} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import MainNavigator from './app/navigation/MainNavigator';
import {blockScreenshots, unblockScreenshots} from './app/utils/screenshotBlocker';
import {startInactivityTimer, stopInactivityTimer} from './app/utils/inactivityLock';

const App = () => {
  useEffect(() => {
    blockScreenshots();
    startInactivityTimer();
    return () => {
      unblockScreenshots();
      stopInactivityTimer();
    };
  }, []);

  return (
    <NavigationContainer>
      <StatusBar barStyle="light-content" />
      <SafeAreaView style={styles.container}>
        <MainNavigator />
      </SafeAreaView>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  container: {
    flex:1,
    backgroundColor:'#111',
  },
});

export default App;

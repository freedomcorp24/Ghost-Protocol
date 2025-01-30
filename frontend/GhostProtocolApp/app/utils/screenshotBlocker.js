/**
 * GhostProtocolApp/app/utils/screenshotBlocker.js
 */
import {NativeModules, Platform} from 'react-native';

// This depends on react-native-screen-protector or a custom module
export function blockScreenshots() {
  if (Platform.OS === 'android') {
    if (NativeModules && NativeModules.ScreenProtector) {
      NativeModules.ScreenProtector.activateSecure();
    }
    // else fallback
  }
  // iOS approach depends on library; if not supported, you'd do a partial approach
}

export function unblockScreenshots() {
  if (Platform.OS === 'android') {
    if (NativeModules && NativeModules.ScreenProtector) {
      NativeModules.ScreenProtector.deactivateSecure();
    }
  }
}

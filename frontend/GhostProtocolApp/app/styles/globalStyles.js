import {StyleSheet} from 'react-native';

const globalStyles = StyleSheet.create({
  container: {
    flex:1,
    backgroundColor: '#111',
    padding:16,
  },
  title: {
    fontSize:24,
    color:'#fff',
    marginBottom:12,
    fontWeight:'bold',
  },
  input: {
    borderWidth:1,
    borderColor:'#555',
    borderRadius:4,
    color:'#fff',
    padding:8,
    marginBottom:12,
  },
  button: {
    backgroundColor:'#339966',
    padding:12,
    borderRadius:4,
    alignItems:'center',
    marginBottom:12,
  },
  buttonText: {
    color:'#fff',
    fontSize:16,
  },
  text: {
    color:'#fff',
    fontSize:16,
  },
});

export default globalStyles;

import React, {useContext} from 'react';
import {Button, StyleSheet, Text, View} from 'react-native';
import Spinner from 'react-native-loading-spinner-overlay';
import {AuthContext} from '../context/AuthContext.js';
import ServiceScreen from './ServiceConnection.js';

const HomeScreen = ({navigation, username}) => {
  const {userInfo, isLoading, logout} = useContext(AuthContext);
  return (
    <View style={styles.container}>
      <Spinner visible={isLoading} />
      <Text style={styles.welcome}>Bienvenue sur notre app AREA</Text>
      <Button title="Add Areas" color="grey" onPress={() => navigation.navigate("Area")} />
      <Button title="Customisation" color="grey" onPress={() => navigation.navigate("Service Connection")} />
      {/*<Button title="AREA" color="red" onPress={() => navigation.navigate('AREA')} />*/}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  welcome: {
    fontSize: 18,
    marginBottom: 8,
  },
});

export default HomeScreen;

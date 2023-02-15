import React, {useContext, useCallback, useState} from 'react';
import {Button, StyleSheet, Text, View, Linking, TextInput} from 'react-native';
import Spinner from 'react-native-loading-spinner-overlay';
import {AuthContext} from '../context/AuthContext.js';
import client from '../config';


const AddMessage = ({navigation, username}) => {

  const {userInfo, isLoading, sendToBack} = useContext(AuthContext);
  const [type, setType] = useState('')
  const [service, setService] = useState('')
  const [message, setMessage] = useState('')

  return (
  <View style={styles.container}>
    <Spinner visible={isLoading} />
    <Text style={styles.welcome}>Idoles !</Text>
    <Text >Service</Text>
    <TextInput style={styles.input} onChangeText={setService} value={service}/>
    <Text >message</Text>
    <TextInput style={styles.input} onChangeText={setMessage} value={message}/>
    <Text >type</Text>
    <TextInput style={styles.input} onChangeText={setType} value={type}/>
    <Button title="ADD" color="blue" onPress={() => sendToBack({"service": service, "message": message, "type": type}, '/addMessage')} />
  </View>
);
};

const styles = StyleSheet.create({
  input: {
    height: 40,
    margin: 12,
    borderWidth: 1,
    padding: 10,
  },
});

export default AddMessage;

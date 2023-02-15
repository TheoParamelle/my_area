import React, {useContext, useCallback, useState} from 'react';
import {Button, StyleSheet, Text, View, Linking, TextInput} from 'react-native';
import Spinner from 'react-native-loading-spinner-overlay';
import {AuthContext} from '../context/AuthContext.js';
import client from '../config';


const AddIdoles = ({navigation, username}) => {

  const {userInfo, isLoading, sendToBack} = useContext(AuthContext);
  const [text, setText] = useState('')

  return (
  <View style={styles.container}>
    <Spinner visible={isLoading} />
    <Text style={styles.welcome}>Idoles !</Text>

    <TextInput style={styles.input} onChangeText={setText} value={text}/>
    <Button title="ADD" color="blue" onPress={() => sendToBack({"idole": text}, '/twitter/addIdole')} />
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

export default AddIdoles;

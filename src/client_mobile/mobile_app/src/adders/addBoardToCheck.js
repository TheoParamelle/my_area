import React, {useContext, useCallback, useState} from 'react';
import {Button, StyleSheet, Text, View, Linking, TextInput} from 'react-native';
import Spinner from 'react-native-loading-spinner-overlay';
import {AuthContext} from '../context/AuthContext.js';
import client from '../config';


const AddBoard = ({navigation, username}) => {

  const {userInfo, isLoading, sendToBack} = useContext(AuthContext);
  const [boardName, setBoardName] = useState('')

  return (
  <View style={styles.container}>
    <Spinner visible={isLoading} />
    <Text >Board Name</Text>
    <TextInput style={styles.input} onChangeText={setBoardName} value={boardName}/>
    <Button title="ADD" color="blue" onPress={() => sendToBack({"boardName": boardName}, '/trello/addBoardToCheck')} />
  </View>
);
};

const styles = StyleSheet.create({
  input: {
    height: 40,
    margin: 12,
    borderWidth: 1,
    padding: 10,
  }
});

export default AddBoard;

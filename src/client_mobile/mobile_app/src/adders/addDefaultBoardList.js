import React, {useContext, useCallback, useState} from 'react';
import {Button, StyleSheet, Text, View, Linking, TextInput} from 'react-native';
import Spinner from 'react-native-loading-spinner-overlay';
import {AuthContext} from '../context/AuthContext.js';
import client from '../config';


const AddDefaultBoardList = ({navigation, username}) => {

  const {userInfo, isLoading, sendToBack} = useContext(AuthContext);
  const [repoName, setRepoName] = useState('')
  const [boardName, setBoardName] = useState('')
  const [listName, setListName] = useState('')

  return (
  <View style={styles.container}>
    <Spinner visible={isLoading} />
    <Text >Repo Name</Text>
    <TextInput style={styles.input} onChangeText={setRepoName} value={repoName}/>
    <Text >Board Name</Text>
    <TextInput style={styles.input} onChangeText={setBoardName} value={boardName}/>
    <Text >List Name</Text>
    <TextInput style={styles.input} onChangeText={setListName} value={listName}/>
    <Button title="ADD" color="blue" onPress={() => sendToBack({"repoName": repoName, "boardName": boardName, "listName": listName}, '/github/addDefaultBoardList')} />
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

export default AddDefaultBoardList;

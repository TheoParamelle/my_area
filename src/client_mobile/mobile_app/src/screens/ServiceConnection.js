import React, {useContext, useCallback} from 'react';
import {Button, StyleSheet, Text, View, Linking} from 'react-native';
import Spinner from 'react-native-loading-spinner-overlay';
import {AuthContext} from '../context/AuthContext.js';

const ServiceScreen = ({navigation, username}) => {

    const {userInfo, isLoading, logout} = useContext(AuthContext);
    const {setService} = useContext(AuthContext);

    function addInfo(service) {
        navigation.navigate(service)
    }

    return (
    <View style={styles.container}>
      <Spinner visible={isLoading} />
      <Text style={styles.welcome}>Customisation !</Text>
      <Button title="Add an idole for twitter" color="blue" onPress={() => addInfo("addIdole")} />
      <Button title="Add Message" color="blue" onPress={() => addInfo("addMessage")} />
      <Button title="Add defaultLabel for trello" color="blue" onPress={() => addInfo("addDefaultLabel")} />
      <Button title="Add Trello Board" color="blue" onPress={() => addInfo("addBoard")} />
      <Button title="Add Github Repo" color="blue" onPress={() => addInfo("addRepo")} />
      <Button title="Add a default trello list for the github issue" color="blue" onPress={() => addInfo("addDefaultBoardList")} />
      <Button title="Link a github repo and a board trello" color="blue" onPress={() => addInfo("addRepoTrello")} />
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

export default ServiceScreen;

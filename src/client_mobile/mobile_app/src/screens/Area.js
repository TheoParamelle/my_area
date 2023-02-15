import React, { useContext, useState } from 'react';
import { Button, StyleSheet, Text, View } from 'react-native';
import Spinner from 'react-native-loading-spinner-overlay';
import { AuthContext } from '../context/AuthContext.js';
import DropDownPicker from 'react-native-dropdown-picker';


const AreaScreen = ({ navigation, username }) => {
  const [actionService, setActionService] = useState('');
  const [actionType, setActionType] = useState('');
  const { userInfo, isLoading, logout, sendArea } = useContext(AuthContext);
  const [actionServiceSelected, setActionServiceSelected] = useState(0);
  const intitialAreas = { "action": { "service": actionService, "type": actionType }, "reaction": [] }
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState(null);
  const [myitems, setItems] = useState([
    { label: 'Spotify', value: 'spotify' },
    { label: 'New album from one of your artist', value: 'newArtistAlbum', parent: 'spotify' },
    { label: 'New liked song', value: 'newSavedTrack', parent: 'spotify' },
    { label: 'Creation of a new playlist', value: 'newPlaylist', parent: 'spotify' },

    { label: 'Github', value: 'github' },
    { label: 'New issue', value: 'newIssue', parent: 'github' },
    { label: 'New branch', value: 'newBranch', parent: 'github' },
    { label: 'New pull', value: 'newPull', parent: 'github' },

    { label: 'Trello', value: 'trello' },
    { label: 'New card', value: 'newCard', parent: 'trello' },
    { label: 'New list', value: 'newList', parent: 'trello' },
    { label: 'New label', value: 'newLabel', parent: 'trello' },
    { label: 'Archived list', value: 'archivedList', parent: 'trello' },

    { label: 'Twitter', value: 'twitter' },
    { label: 'New follow', value: 'follow', parent: 'twitter' },
    { label: 'Tweet from an idol', value: 'idolesTweet', parent: 'twitter' },
    { label: 'New direct message', value: 'dm', parent: 'twitter' },
  ]);
  const createAction = (actionService, actionType) => {
    intitialAreas.action.service = actionService
    intitialAreas.action.type = actionType
    setActionServiceSelected(1)
    console.log("caca")
    console.log(intitialAreas.action)
  }
  const handleSelectReaction = (service, type) => {
    var serviceExist = false
    for (const elem of intitialAreas.reaction) {
      if (elem.service === service) {
        console.log("je suis rentré")
        elem.type.push(type)
        serviceExist = true
      }
    }
    if (serviceExist === false) {
      console.log("je suis LAAAAAA")
      intitialAreas.reaction.push({ "service": service, "type": [type] })
    }
    console.log(intitialAreas)
    console.log(intitialAreas.reaction)
  }
  return (
    <View style={styles.container}>
      <Spinner visible={isLoading} />
      <Text style={styles.welcome}>Choisissez votre action</Text>
      {actionServiceSelected !== 1 &&
        <DropDownPicker
          open={open}
          value={value}
          items={myitems}
          setValue={setValue}
          setItems={setItems}
          setOpen={setOpen}
          onSelectItem={(item) => {
            setActionService(item.parent)
            setActionType(item.value)
          }}
        />}
      {actionServiceSelected === 1 && actionType === "follow" &&
        <Button variant="primary" title="Followback the person" onPress={() => handleSelectReaction("twitter", "followback")}></Button>}
      {actionServiceSelected === 1 && actionType === "follow" &&
        <Button variant="primary" title="Make a post" onPress={() => handleSelectReaction("twitter", "post")}></Button>}

      {actionServiceSelected === 1 && actionType === "idolesTweet" &&
        <Button variant="primary" title="Retweet their post automatically" onPress={() => handleSelectReaction("twitter", "retweet")}></Button>}
      {actionServiceSelected === 1 && actionType === "idolesTweet" &&
        <Button variant="primary" title="Like their post automatically" onPress={() => handleSelectReaction("twitter", "like")}></Button>}

      {actionServiceSelected === 1 && actionType === "dm" &&
        <Button variant="primary" title="Mark the direct message as read" onPress={() => handleSelectReaction("twitter", "markRead")}></Button>}
      {actionServiceSelected === 1 && actionType === "dm" &&
        <Button variant="primary" title="Send an automatic message" onPress={() => handleSelectReaction("twitter", "sendDm")}></Button>}

      {actionServiceSelected === 1 && actionType === "newCard" &&
        <Button variant="primary" title="Add a default label" onPress={() => handleSelectReaction("trello", "defaultLabel")}></Button>}
      {actionServiceSelected === 1 && actionType === "newCard" &&
        <Button variant="primary" title="Send yourself a direct message on Twitter" onPress={() => handleSelectReaction("twitter", "sendDm")}></Button>}
      {actionServiceSelected === 1 && actionType === "newCard" &&
        <Button variant="primary" title="Skips to next track in the user queue" onPress={() => handleSelectReaction("spotify", "nextTrack")}></Button>}

      {actionServiceSelected === 1 && actionType === "newList" &&
        <Button variant="primary" title="Send yourself a direct message on Twitter" onPress={() => handleSelectReaction("twitter", "sendDm")}></Button>}
      {actionServiceSelected === 1 && actionType === "newList" &&
        <Button variant="primary" title="Add a new card" onPress={() => handleSelectReaction("trello", "addCard")}></Button>}

      {actionServiceSelected === 1 && actionType === "archivedList" &&
        <Button variant="primary" title="Create a pull request on the Branch to main" onPress={() => handleSelectReaction("github", "pullRequest")}></Button>}
      {actionServiceSelected === 1 && actionType === "archivedList" &&
        <Button variant="primary" title="Send yourself a direct message on Twitter" onPress={() => handleSelectReaction("twitter", "sendDm")}></Button>}

      {actionServiceSelected === 1 && actionType === "newLabel" &&
        <Button variant="primary" title="Send yourself a direct message on Twitter" onPress={() => handleSelectReaction("twitter", "sendDm")}></Button>}
      {actionServiceSelected === 1 && actionType === "newLabel" &&
        <Button variant="primary" title="Create a new issue on Github" onPress={() => handleSelectReaction("github", "newIssue")}></Button>}

      {actionServiceSelected === 1 && actionType === "newIssue" &&
        <Button variant="primary" title="Add a comment on Github" onPress={() => handleSelectReaction("github", "addComment")}></Button>}
      {actionServiceSelected === 1 && actionType === "newIssue" &&
        <Button variant="primary" title="Add a new card on Trello" onPress={() => handleSelectReaction("trello", "addCard")}></Button>}
      {actionServiceSelected === 1 && actionType === "newIssue" &&
        <Button variant="primary" title="Send yourself a direct message on Twitter" onPress={() => handleSelectReaction("twitter", "sendDm")}></Button>}

      {actionServiceSelected === 1 && actionType === "newBranch" &&
        <Button variant="primary" title="Create a new list on Trello" onPress={() => handleSelectReaction("trello", "addList")}></Button>}
      {actionServiceSelected === 1 && actionType === "newBranch" &&
        <Button variant="primary" title="Send yourself a direct message on Twitter" onPress={() => handleSelectReaction("twitter", "sendDm")}></Button>}

      {actionServiceSelected === 1 && actionType === "newPull" &&
        <Button variant="primary" title="Send yourself a direct message on Twitter" onPress={() => handleSelectReaction("twitter", "sendDm")}></Button>}

      {actionServiceSelected === 1 && actionType === "newArtistAlbum" &&
        <Button variant="primary" title="Send yourself a direct message on Twitter" onPress={() => handleSelectReaction("twitter", "sendDm")}></Button>}
      {actionServiceSelected === 1 && actionType === "newArtistAlbum" &&
        <Button variant="primary" title="Save the album to your library" onPress={() => handleSelectReaction("spotify", "saveAlbum")}></Button>}

      {actionServiceSelected === 1 && actionType === "newSavedTrack" &&
        <Button variant="primary" title="Put the new track to the playlist filter by the genre" onPress={() => handleSelectReaction("spotify", "newSavedTrack")}></Button>}

      {actionServiceSelected === 1 && actionType === "newPlaylist" &&
        <Button variant="primary" title="Post a tweet to share your playlist" onPress={() => handleSelectReaction("twitter", "post")}></Button>}
      {actionServiceSelected === 1 && actionType === "newPlaylist" &&
        <Button variant="primary" title="Send yourself a direct message on Twitter" onPress={() => handleSelectReaction("twitter", "sendDm")}></Button>}
      {actionServiceSelected !== 1 && <Button
        title="Go Reaction"
        onPress={() => {
          console.log("bouton OK press")
          console.log("service :", actionService)
          console.log("action :", actionType)
          createAction(actionService, actionType)
        }}
      />}
      {actionServiceSelected === 1 && <Button
        variant="outline-success"
        title="Go Go Go"
        onPress={() => {
          console.log("dans le boutton : ", intitialAreas)
          sendArea(intitialAreas)
        }
        }
      />}
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

export default AreaScreen;
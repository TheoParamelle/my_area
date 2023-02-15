import React from "react";
import { useState } from "react";
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';

const AddArea = ({username}) => {

    const [actionService, setActionService] = useState('');
    // const [action, setAction] = useState('');
    const [actionServiceSelected, setActionServiceSelected] = useState(0);
    const [actionType, setActionType] = useState('');
    const intitialAreas = {"action" : {"service": actionService, "type": actionType}, "reaction" : []}

    const handleSelect=(e)=>{
        intitialAreas.action = e
        // setAreas(intitialAreas.action = e)
        setActionService(e)
    }
    const handleSelectAction=(e)=>{
        intitialAreas.action.type = e
        setActionType(e)
        // setAreas(intitialAreas.action.type = e)
    }
    const handleSelectReaction=(service, type)=>{
        var serviceExist = false
        for (const elem of intitialAreas.reaction) {
            if (elem.service === service) {
                elem.type.push(type)
                serviceExist = true
            }
        }
        if (serviceExist === false) {
            intitialAreas.reaction.push({"service" : service, "type" : [type]})
        }
        console.log(intitialAreas)
    }

    function sendArea(actService, actionType) {
        if (actService === "" || actionType === "") {
            console.log("ntm\n")
        }
        else if (actService !== "" && actionType !== "") {
            // console.log(actService)
            // console.log(reactService)
            console.log(intitialAreas.action.service)
            console.log(intitialAreas.action.type)
            // console.log(areas.action.service)
            // console.log(areas.action.type)
            setActionServiceSelected(1);
            if (intitialAreas.reaction.length > 0) {
                console.log(intitialAreas)
                fetch("addArea",
                {
                    'method': "POST",
                    headers: {
                        'Content-Type':'application/json'
                    },
                    body: JSON.stringify(intitialAreas)
                })
                .then(res => res.json())
                .then(data => console.log(data))
            }
        }
        // let url = "http://localhost:8080/login/" + service + "/" + username
        // window.open(url, "_self")
    }

    return(
        <div className="addArea">
        <h1>Add Area !</h1>
            <div>
                Add new area for more fun !!!
            </div>
            <br/>
            <br/>
            <br/>
            {actionServiceSelected !== 1 &&
                <DropdownButton id="dropdown-basic-button" title="Select action service" onSelect={handleSelect}>
                <Dropdown.Item eventKey="twitter">Twitter</Dropdown.Item>
                <Dropdown.Item eventKey="trello">Trello</Dropdown.Item>
                <Dropdown.Item eventKey="github">Github</Dropdown.Item>
                <Dropdown.Item eventKey="spotify">Spotify</Dropdown.Item>
            </DropdownButton>}


            {/* {actionServiceSelected === 1 && actionType === "follow" &&
                // intitialAreas.reaction.map("twitter")
                <ButtonGroup>
                <Button variant="primary" value="followback" onClick={handleSelectReaction("twitter", "followback")}>Followback the person</Button>
                <Button variant="primary" value="post" onClick={handleSelectReaction("twitter", "post")}>Make a post to say thanks</Button>
            </ButtonGroup>} */}

            {actionServiceSelected === 1 && actionType === "follow" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "followback")}> Followback the person </Button>}
            {actionServiceSelected === 1 && actionType === "follow" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "post")}>Make a post to say thanks</Button>}

            {actionServiceSelected === 1 && actionType === "idolesTweet" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "retweet")}>Retweet their post automatically</Button>}
            {actionServiceSelected === 1 && actionType === "idolesTweet" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "like")}>Like their post automatically</Button>}

            {actionServiceSelected === 1 && actionType === "dm" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "markRead")}>Mark the direct message as read</Button>}
            {actionServiceSelected === 1 && actionType === "dm" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "sendDm")}>Send an automatic message</Button>}

            {actionServiceSelected === 1 && actionType === "newCard" &&
                <Button variant="primary" onClick={() => handleSelectReaction("trello", "defaultLabel")}>Add a default label</Button>}
            {actionServiceSelected === 1 && actionType === "newCard" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "sendDm")}>Send yourself a direct message on Twitter</Button>}
            {actionServiceSelected === 1 && actionType === "newCard" &&
                <Button variant="primary" onClick={() => handleSelectReaction("spotify", "nextTrack")}>Skips to next track in the user queue</Button>}

            {actionServiceSelected === 1 && actionType === "newList" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "sendDm")}>Send yourself a direct message on Twitter</Button>}
            {actionServiceSelected === 1 && actionType === "newList" &&
                <Button variant="primary" onClick={() => handleSelectReaction("trello", "addCard")}>Add a new card</Button>}

            {actionServiceSelected === 1 && actionType === "archivedList" &&
                <Button variant="primary" onClick={() => handleSelectReaction("github", "pullRequest")}>Create a pull request on the Branch to main</Button>}
            {actionServiceSelected === 1 && actionType === "archivedList" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "sendDm")}>Send yourself a direct message on Twitter</Button>}

            {actionServiceSelected === 1 && actionType === "newLabel" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "sendDm")}>Send yourself a direct message on Twitter</Button>}
            {actionServiceSelected === 1 && actionType === "newLabel" &&
                <Button variant="primary" onClick={() => handleSelectReaction("github", "newIssue")}>Create a new issue on Github</Button>}

            {actionServiceSelected === 1 && actionType === "newIssue" &&
                <Button variant="primary" onClick={() => handleSelectReaction("github", "addComment")}>Add a comment on Github</Button>}
            {actionServiceSelected === 1 && actionType === "newIssue" &&
                <Button variant="primary" onClick={() => handleSelectReaction("trello", "addCard")}>Add a new card on Trello</Button>}
            {actionServiceSelected === 1 && actionType === "newIssue" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "sendDm")}>Send yourself a direct message on Twitter</Button>}

            {actionServiceSelected === 1 && actionType === "newBranch" &&
                <Button variant="primary" onClick={() => handleSelectReaction("trello", "addList")}>Create a new list on Trello</Button>}
            {actionServiceSelected === 1 && actionType === "newBranch" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "sendDm")}>Send yourself a direct message on Twitter</Button>}

            {actionServiceSelected === 1 && actionType === "newPull" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "sendDm")}>Send yourself a direct message on Twitter</Button>}

            {actionServiceSelected === 1 && actionType === "newArtistAlbum" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "sendDm")}>Send yourself a direct message on Twitter</Button>}
            {actionServiceSelected === 1 && actionType === "newArtistAlbum" &&
                <Button variant="primary" onClick={() => handleSelectReaction("spotify", "saveAlbum")}>Save the album to your library</Button>}

            {actionServiceSelected === 1 && actionType === "newSavedTrack" &&
                <Button variant="primary" onClick={() => handleSelectReaction("spotify", "newSavedTrack")}>Put the new track to the playlist filter by the genre</Button>}

            {actionServiceSelected === 1 && actionType === "newPlaylist" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "post")}>Post a tweet to share your playlist</Button>}
            {actionServiceSelected === 1 && actionType === "newPlaylist" &&
                <Button variant="primary" onClick={() => handleSelectReaction("twitter", "sendDm")}>Send yourself a direct message on Twitter</Button>}
            <br/>
            <br/>
            <br/>
            <br/>
            <br/>
            {actionServiceSelected !== 1 && actionService === "twitter" &&
                <DropdownButton id="dropdown-basic-button" title="Choose a Twitter action" onSelect={handleSelectAction}>
                <Dropdown.Item eventKey ="follow">New follow</Dropdown.Item>
                <Dropdown.Item eventKey ="idolesTweet">Tweet from an idole</Dropdown.Item>
                <Dropdown.Item eventKey ="dm">New direct message</Dropdown.Item>
            </DropdownButton>}
            {actionServiceSelected !== 1 && actionService === "trello" &&
                <DropdownButton id="dropdown-basic-button" title="Choose a Trello action" onSelect={handleSelectAction}>
                <Dropdown.Item eventKey ="newCard">New card</Dropdown.Item>
                <Dropdown.Item eventKey ="newList">New list</Dropdown.Item>
                <Dropdown.Item eventKey ="newLabel">New label</Dropdown.Item>
                <Dropdown.Item eventKey ="archivedList">Archived list</Dropdown.Item>
            </DropdownButton>}
            {actionServiceSelected !== 1 && actionService === "github" &&
                <DropdownButton id="dropdown-basic-button" title="Choose a Github action" onSelect={handleSelectAction}>
                <Dropdown.Item eventKey ="newIssue">New issue</Dropdown.Item>
                <Dropdown.Item eventKey ="newBranch">New branch</Dropdown.Item>
                <Dropdown.Item eventKey ="newPull">New pull</Dropdown.Item>
            </DropdownButton>}
            {actionServiceSelected !== 1 && actionService === "spotify" &&
                <DropdownButton id="dropdown-basic-button" title="Choose a Spotify action" onSelect={handleSelectAction}>
                <Dropdown.Item eventKey ="newArtistAlbum">New album from one of your artists</Dropdown.Item>
                <Dropdown.Item eventKey ="newSavedTrack">New liked song</Dropdown.Item>
                <Dropdown.Item eventKey ="newPlaylist">Creation of a new playlist</Dropdown.Item>
            </DropdownButton>}
            <br/>
            <br/>
            <br/>
            <Button variant="outline-success" onClick={() => sendArea(actionService, actionType)}>
                Ok
            </Button>

        </div>
        );
}

export default AddArea
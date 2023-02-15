import React from "react";
import { useState } from "react";
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import { Link } from "react-router-dom";

const SetTexts = ({ username }) => {
    const [idole, setIdole] = useState("")
    const idoles = { "idole": idole }
    const [message, setMessage] = useState("")
    const twitterMessage = { "service": "twitter", "message": message, "type": "follow" }
    const [boardName, setBoardName] = useState("")
    const [labelName, setLabelName] = useState("")
    const trelloLabel = { "boardName": boardName, "labelName": labelName }
    const [boardNameTrello, setBoardNameTrello] = useState("")
    const trelloBoardName = { "boardName": boardNameTrello }
    const [repoName, setRepoNameTrello] = useState("")
    const repo = { "repoName": repoName }
    const [repoListName, setRepoListName] = useState("")
    const [listBoardName, setListBoardName] = useState("")
    const [listName, setListName] = useState("")
    const trelloList = { "repoName": repoListName, "boardName": listBoardName, "listName": listName }
    const [trelloRepoName, setTrelloRepoName] = useState("")
    const [trelloBoardRName, setTrelloBoardRName] = useState("")
    const trelloRepo = { "boardName": trelloBoardRName, "repoName": trelloRepoName }

    function sendTexts() {
        if (idole !== "") {
            fetch("twitter/addIdole",
                {
                    'method': "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(idoles)
                })
                .then(res => res.json())
                .then(data => console.log(data))
        }
        if (message !== "") {
            fetch("twitter/addMessage",
                {
                    'method': "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(twitterMessage)
                })
                .then(res => res.json())
                .then(data => console.log(data))
        }
        if (boardName !== "" && labelName !== "") {
            fetch("trello/addDefaultLabel",
                {
                    'method': "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(trelloLabel)
                })
                .then(res => res.json())
                .then(data => console.log(data))
        }
        if (boardNameTrello !== "") {
            fetch("trello/addBoardToCheck",
                {
                    'method': "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(trelloBoardName)
                })
                .then(res => res.json())
                .then(data => console.log(data))
        }
        if (repoName !== "") {
            fetch("github/addRepo",
                {
                    'method': "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(repo)
                })
                .then(res => res.json())
                .then(data => console.log(data))
        }
        if (repoListName !== "" && listBoardName !== "" &&listName !== "") {
            fetch("github/addDefaultBoardList",
                {
                    'method': "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(trelloList)
                })
                .then(res => res.json())
                .then(data => console.log(data))
        }
        if (trelloBoardRName !== "" && trelloRepoName !== "") {
            fetch("trello/addRepo",
                {
                    'method': "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(trelloRepo)
                })
                .then(res => res.json())
                .then(data => console.log(data))
        }
    }

    return (
        <div className="setTexts">
            <h1>Set your future actions and reactions here !</h1>
            <br />
            <InputGroup className="mb-3">
                <InputGroup.Text id="inputGroup-sizing-default">
                    Your idole @
                </InputGroup.Text>
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setIdole(e.target.value)}
                    type="text"
                />
            </InputGroup>
            <br />
            <InputGroup className="mb-3">
                <InputGroup.Text id="inputGroup-sizing-default">
                    Your automatic message for a new follow
                </InputGroup.Text>
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setMessage(e.target.value)}
                    type="text"
                />
            </InputGroup>
            <br />
            <InputGroup className="mb-3">
                <InputGroup.Text> Set your automatic label and the board for it </InputGroup.Text>
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setLabelName(e.target.value)}
                    type="text"
                />
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setBoardName(e.target.value)}
                    type="text"
                />
            </InputGroup>

            <br />
            <InputGroup className="mb-3">
                <InputGroup.Text id="inputGroup-sizing-default">
                    Choose your board to check for Trello actions
                </InputGroup.Text>
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setBoardNameTrello(e.target.value)}
                    type="text"
                />
            </InputGroup>

            <br />
            <InputGroup className="mb-3">
                <InputGroup.Text id="inputGroup-sizing-default">
                    Choose your repo to check
                </InputGroup.Text>
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setRepoNameTrello(e.target.value)}
                    type="text"
                />
            </InputGroup>

            <br />
            <InputGroup className="mb-3">
                <InputGroup.Text> Set your repo, the board, and the list to link them</InputGroup.Text>
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setRepoListName(e.target.value)}
                    type="text"
                />
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setListBoardName(e.target.value)}
                    type="text"
                />
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setListName(e.target.value)}
                    type="text"
                />
            </InputGroup>
            <br />
            <InputGroup className="mb-3">
                <InputGroup.Text> Link github repo and trello board </InputGroup.Text>
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setTrelloRepoName(e.target.value)}
                    type="text"
                />
                <Form.Control
                    aria-label="Default"
                    aria-describedby="inputGroup-sizing-default"
                    onChange={e => setTrelloBoardRName(e.target.value)}
                    type="text"
                />
            </InputGroup>

            <Link to="/addArea">
                <Button variant="outline-success" onClick={() => sendTexts()}>
                    Ok
                </Button>
            </Link>
        </div>
    );

}

export default SetTexts
import React from "react";


const AddServices = ({username}) => {

    function otherConnection(service) {
        let url = "http://localhost:8080/login/" + service
        window.open(url, "_self")
    }
    
    return(
        <div className="addServices">
        <h1>Add services</h1>
            <div>
                Add new services for more actions !!!
            </div>
            <br/>
            <br/>
            <br/>
            <br/>
            <br/>
            <div class="d-grid gap-2 col-6 mx-auto">
            <button type="button" class="btn btn-info" onClick={() => otherConnection("twitter")}>Twitter</button>
            <br/>
            <br/>
            <button type="button" class="btn btn-secondary" onClick={() => otherConnection("github")}>Github</button>
            <br/>
            <br/>
            <button type="button" class="btn btn-light" onClick={() => otherConnection("trello")}>Trello</button>
            <br/>
            <br/>
            <button type="button" class="btn btn-success"onClick={() => otherConnection("spotify")}>Spotify</button>
            </div>
        </div>
        );
}

export default AddServices
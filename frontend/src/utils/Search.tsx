import axios from "axios";
import {fetchAuthSession } from "aws-amplify/auth";
import { GetJWT } from "./SendCsv";
const apiBaseUrl = process.env.REACT_APP_API_URL? process.env.REACT_APP_API_URL : '';
async function SearchRegistrationNumber(search: string){
    const JWT = await GetJWT();
    console.log(JWT);
    const searchText = "PC2021320/18010044"
    let results  = {};
    await axios.get(
        `${apiBaseUrl}/search?registrationNumber=${searchText}&latestOnly=Yes&strictMode=No`,
        {
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + JWT,
            },

        }
).then((response) => {
        console.log(response);
        console.log(response.data.Results)
        results = {"data": response.data.Results??[]};
    }).catch((error) => {
        console.log(error);
        results =  {"error": error};
    }
    );
    return results
}



export async function SearchRegAndLicence(search: string): Promise<any>{
    // if search is not digits or letters or / then throw error
    if (!/^[a-zA-Z0-9///]*$/.test(search)) {
        throw new Error("Invalid search input");
    }
    if (search.includes("/")) {
        console.log("Registration number");
        return  SearchRegistrationNumber(search);
        }
    else {
        console.log("Licence number");
    }

}



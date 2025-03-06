import axios from "axios";
import { GetJWT } from "./SendCsv";
const apiBaseUrl = process.env.REACT_APP_API_URL
  ? process.env.REACT_APP_API_URL
  : "";
export async function SearchRegistrationNumber(
  search: string,
  latestOnly: "Yes" | "No" = "Yes",
  strictMode: "Yes" | "No" = "No",
  licenceNumber: string| null  = "",
  routeNumber: string | null= ""
): Promise<any> {
  const JWT = await GetJWT();
  let results = {};
  let requestString = `${apiBaseUrl}/search?registrationNumber=${search}&latestOnly=${latestOnly}&strictMode=${strictMode}`;
  if (licenceNumber) {
    requestString += `&licenceNumber=${licenceNumber}`;
  }
  if (routeNumber) {
    requestString += `&routeNumber=${routeNumber}`;
  }
  console.log(requestString);
  await axios
    .get(
      `${requestString}`,
      {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json",
          Authorization: "Bearer " + JWT,
        },
      }
    )
    .then((response) => {
      results = { data: response.data.Results ?? [] };
    })
    .catch((error) => {
      if (error.message === "Request failed with status code 401") {
        results = { error: { message: "Unauthorised" } };
      }else{
      results = { error: error };
      }
    });
  return results;
}

export async function SearchRegAndLicence(search: string): Promise<any> {
  // if search is not digits or letters or / then throw error
  if (!/^[a-zA-Z0-9///]*$/.test(search)) {
    throw new Error("Invalid search inputs");
  }
  return SearchRegistrationNumber(search);
}

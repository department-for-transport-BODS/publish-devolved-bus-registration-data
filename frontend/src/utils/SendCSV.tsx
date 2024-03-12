import axios, { AxiosError } from "axios";
import { getApiUrl } from "../config";

export const SendCSV = async (formData: FormData, navigate:any) => {
    const apiBaseUrl = getApiUrl();

    try {
        let jwt = "";
        Object.entries(localStorage).forEach(([key, value]) => {
            if (key.includes("accessToken")) {

                jwt = value.toString();
            }
        });
        const response = await axios.post(
            `${apiBaseUrl}/api/v1/uploadfile`,
            formData,
            {
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "multipart/form-data",
                    "Authorization": "Bearer " + jwt,
                },
            }
        );
        navigate("/successfullyuploaded", { state: response?.data, replace: true });
    } catch (error) {
        
        const nowData = {
            message: (error as AxiosError).message,
            code: (error as AxiosError).code,
            data: (error as AxiosError).response?.data,
        };
        navigate("/partlyuploaded", { state: nowData.data, replace: true});
    }
}

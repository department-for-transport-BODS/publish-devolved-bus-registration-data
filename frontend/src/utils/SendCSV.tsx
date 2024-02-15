import axios, { AxiosError } from "axios";
export const SendCSV = async (formData: FormData, navigate:any) => {
    const API_URL = process.env.REACT_APP_API_URL || "";
try {
    const response = await axios.post(
        API_URL,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
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

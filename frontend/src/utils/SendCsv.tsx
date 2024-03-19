import axios, { AxiosError } from "axios";
export const SendCsv = async (formData: FormData, navigate:any) => {
    const apiBaseUrl = process.env.REACT_APP_API_URL? process.env.REACT_APP_API_URL : '';

    try {
        let jwt = "";
        Object.entries(localStorage).forEach(([key, value]) => {
            if (key.includes("accessToken")) {

                jwt = value.toString();
            }
        });
        const response = await axios.post(
            `${apiBaseUrl}/upload-file`,
            formData,
            {
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "multipart/form-data",
                    "Authorization": "Bearer " + jwt,
                },
            }
        );
        navigate("/successfully-uploaded", { state: response?.data, replace: true });
    } catch (error: any) {
        if (error.response.status ===422) {
        const nowData = {
            message: (error as AxiosError).message,
            code: (error as AxiosError).code,
            data: (error as AxiosError).response?.data,
        };
        navigate("/partly-uploaded", { state: nowData.data, replace: true});
    } else {
        navigate("/error", { state: {error: error?.message}, replace: true});
    }
}
}
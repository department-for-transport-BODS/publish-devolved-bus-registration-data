import axios from "axios";
import { fetchAuthSession } from "aws-amplify/auth";

const GetJWT = async () => {
        let jwt = "";
        await fetchAuthSession().then(() => {
            Object.entries(localStorage).forEach(([key, value]) => {
                if (key.includes("accessToken")) {
                    jwt = value.toString();
                }
            });
        });
        return jwt;
    };
const apiBaseUrl = process.env.REACT_APP_API_URL? process.env.REACT_APP_API_URL : '';
const GetReport = async (report_id:string) => {
    const JWT = await GetJWT();
    let count = 0;
    let reportStatus = "";
    let report = null;
    while (count < 4) {
        await new Promise((resolve) => setTimeout(resolve, 30000));
        await axios.get(
            `${apiBaseUrl}/get-report?report_id=${report_id}`,
            {
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + JWT,
                },
            }
        ).then((response) => {
        reportStatus = response?.data?.ReportStatus; 
        report = response?.data?.Report;

        
        
    })
    if (reportStatus === "Completed") {
        return {"ReportStatus": reportStatus, "Report": report}
    }
    count++;
}
}
const ShowResponse = (report:any, navigate:any) =>{
    if (report.invalid_records.length > 0) {
        navigate("/partly-uploaded", { state: {detail: report}, replace: true });
    } else {
        navigate("/successfully-uploaded", { state: report, replace: true });
    }

}

export const SendCsv = async (formData: FormData, navigate:any) => {
    const JWT = await GetJWT();
    try {
        const response = await axios.post(
            `${apiBaseUrl}/upload-file`,
            formData,
            {
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "multipart/form-data",
                    "Authorization": "Bearer " + JWT,
                },
            }
        );
        const report_id = response?.data?.report_id;
        // navigate("/successfully-uploaded", { state: response?.data, replace: true });
        const Report = await GetReport(report_id);
        if (Report !== null && Report !== undefined) {
            ShowResponse(Report.Report, navigate);
        }
    } catch (error: any) {
        navigate("/error", { state: {error: error?.message}, replace: true});
}
}

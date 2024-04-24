import axios from "axios";
import { fetchAuthSession } from "aws-amplify/auth";
import Cookies from 'universal-cookie';

export const GetJWT = async () => {
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
export const GetReport = async (report_id:string,navigate:any) => {
    const JWT = await GetJWT();
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
        const report = response?.data?.Report;
        ShowResponse(report, navigate);

        
        
    })
}
export const getStaged = async () => {
    const JWT = await GetJWT();
    let count = 0;
    let stageStatus = "";
    let stagedRecrods = null;
    while (count < 4) {
        await new Promise((resolve) => setTimeout(resolve, 30000));
        const cookies = new Cookies();
        const staged_id = cookies.get('stage_id');
        if (staged_id !== null || staged_id !== undefined) {
        
        await axios.get(
            `${apiBaseUrl}/get-staged?stage_id=${staged_id}`,
            {
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + JWT,
                },
            }
        ).then((response) => {
        stageStatus = response?.data?.status;
        stagedRecrods = response?.data?.records;

        
        
    })
    }
    if (stageStatus === "Completed") {
        return {"stageStatus": stageStatus, "records": stagedRecrods}
    }
    count++;
}
throw new Error("Staging failed");
}

export const CommitRegistrations = async (stage_id:string) => {
    const JWT = await GetJWT();
    try {
        await axios.post(
            `${apiBaseUrl}/staged-records/commit?stage_id=${stage_id}`,
            {},
            {
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + JWT,
                },
            }
        );
    } catch (error: any) {
        return error;
    }
};

export const DiscardRegistrations = async (stage_id:string) => {
    const JWT = await GetJWT();
    try {
        await axios.post(
            `${apiBaseUrl}/staged-records/discard?stage_id=${stage_id}`,
            {},
            {
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + JWT,
                },
            }
        );
    } catch (error: any) {
        return error;
    }
};


const ShowResponse = async (report:any, navigate:any) =>{
    console.log(report)
    const invalid_records_length = report.invalid_records[0]?.records ? Object.keys(report.invalid_records[0]?.records).length : 0;
    if (report.invalid_records.length === 1 && invalid_records_length === 0) {
        navigate("/successfully-uploaded", { state: report, replace: true });
    } else {
        navigate("/partly-uploaded", { state: {detail: report}, replace: true });
    }

}
const ShowPreValidation = (records:any, navigate:any) =>{
        navigate("/pre-validation", { state: {data: records}, replace: true });
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
        // send report it to cookie:
        console.log(report_id);

        if (report_id !== null && report_id !== undefined){
            const cookies = new Cookies();
            cookies.set('stage_id', report_id, { path: '/' });
            console.log(cookies.get('stage_id')); 
            }
    } catch (error: any) {
        navigate("/error", { state: {error: error?.message}, replace: true});
    }
};
export const handleStagedResults = async (stagedRecords:any, navigate:any) => {
    const cookies = new Cookies();
    const staged_id  = cookies.get('stage_id');
    try {
        if (stagedRecords !== null && stagedRecords !== undefined) {
            const records = stagedRecords.records?? [];
            console.log(records)
            if (records.length === 0) {
                await CommitRegistrations(staged_id);
                await GetReport(staged_id, navigate);
                cookies.remove('stage_id');
                
            }
            else{
                ShowPreValidation(stagedRecords.records, navigate);
            }
        }
        // const Report = await GetReport(report_id);
        // if (Report !== null && Report !== undefined) {
        //     ShowResponse(Report.Report, navigate);
        // }
    } catch (error: any) {
        navigate("/error", { state: {error: error?.message}, replace: true});
}
}


export const CheckStageProcesses = async () => {
    const JWT = await GetJWT();
    try {
      const response = await axios.get(
        `${apiBaseUrl}/get-staged-process`,
        {
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + JWT,
          },
        }
      );
      return response.data;
    }
    catch (error: any) {
      return error;
    }
    };
  
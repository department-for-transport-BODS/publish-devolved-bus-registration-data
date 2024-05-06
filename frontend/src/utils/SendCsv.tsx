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
        })
        return jwt;
    };
const apiBaseUrl = process.env.REACT_APP_API_URL? process.env.REACT_APP_API_URL : '';
export const GetReport = async (report_id:string,navigate:unknown) => {
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
    let count = 0;
    let stageStatus = "";
    let stagedRecrods = null;
    const cookies = new Cookies();
    let break_loop = false;
    while (count < 4) {
        if (break_loop) {
            break;
        }
        await new Promise((resolve) => setTimeout(resolve, 30000));
        const JWT = await GetJWT();
        const staged_id = cookies.get('stage_id');
        if (staged_id !== null || staged_id !== undefined) {
        axios.get(
            `${apiBaseUrl}/stage`,
            {
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + JWT,
                },
                params: {
                    entity: "record",
                    stage_id: staged_id,
                },
            },
        ).then((response) => {
        stageStatus = response?.data?.status;
        stagedRecrods = response?.data?.records;
    }).catch((error) => {
        const res = error.response?? null;
        // if error is 425 then continue
        if (res && error.response.status === 425) {
            count--;
            return;
        }else{
            break_loop = true;
            // throw new Error("Staging failed");
        }
    });
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
    // check if report has attribute invalid_records
    if (report.invalid_file === null || report.invalid_file === undefined) {
    const invalid_records_length = report.invalid_records[0]?.records ? Object.keys(report.invalid_records[0]?.records).length : 0;
    if (report.invalid_records.length === 1 && invalid_records_length === 0) {
        navigate("/successfully-uploaded", { state: report, replace: true });
    } else {
        navigate("/partly-uploaded", { state: {detail: report}, replace: true });
    }
}
else{
    navigate("/error", { state: {error: "This file failed the antivirus check. Please upload a new file."}, replace: true});
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

        if (report_id !== null && report_id !== undefined){
            const cookies = new Cookies();
            cookies.set('stage_id', report_id, { path: '/' });
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
    let res = {}
    try {
      await axios.get(
        `${apiBaseUrl}/stage`,
        {
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + JWT,
          },
            params: {
                entity: "process",
            },
        }
      ).then((response) => {
      res = response.data;
      }).catch((error) => {
        res = error; 
      });
    }
    catch (error: any) {
      return error;
    }
    return res;
    };
  
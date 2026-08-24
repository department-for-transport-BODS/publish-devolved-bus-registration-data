import axios, { AxiosError } from "axios";
import { fetchAuthSession } from "aws-amplify/auth";
import Cookies from "universal-cookie";
import { NavigateFunction } from "react-router-dom";
import {
  ReportData,
  StagedRecordsData,
  Stage,
  StageProcessesResponse,
} from "../interfaces/apiTypes";

export type { Stage, StageProcessesResponse };

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

const apiBaseUrl = process.env.REACT_APP_API_URL
  ? process.env.REACT_APP_API_URL
  : "";

const ShowResponse = async (report: ReportData, navigate: NavigateFunction) => {
  // check if report has attribute invalid_records
  if (report.invalid_file === null || report.invalid_file === undefined) {
    const invalid_records_length = report.invalid_records[0]?.records
      ? Object.keys(report.invalid_records[0]?.records).length
      : 0;
    if (report.invalid_records.length === 1 && invalid_records_length === 0) {
      navigate("/successfully-uploaded", { state: report, replace: true });
    } else {
      navigate("/partly-uploaded", {
        state: { detail: report },
        replace: true,
      });
    }
  } else {
    navigate("/error", {
      state: {
        error:
          "This file failed the antivirus check. Please upload a new file.",
      },
      replace: true,
    });
  }
};

const ShowPreValidation = (records: unknown[], navigate: NavigateFunction) => {
  navigate("/pre-validation", { state: { data: records }, replace: true });
};

export const GetReport = async (report_id: string, navigate: NavigateFunction) => {
  const JWT = await GetJWT();
  await axios
    .get(`${apiBaseUrl}/get-report?report_id=${report_id}`, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
        Authorization: "Bearer " + JWT,
      },
    })
    .then((response) => {
      const report = response?.data?.Report as ReportData;
      ShowResponse(report, navigate);
    });
};

export const getStaged = async (): Promise<StagedRecordsData | AxiosError> => {
  await new Promise((resolve) => setTimeout(resolve, 30000));
  const JWT = await GetJWT();
  try {
    const response = await axios.get(`${apiBaseUrl}/stage`, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
        Authorization: "Bearer " + JWT,
      },
    });
    return response.data;
  } catch (error: unknown) {
    const axiosError = error as AxiosError;
    const res = axiosError.response ?? null;
    // if error is 425 then continue
    if (res && axiosError.response?.status === 425) {
      return getStaged();
    } else {
      return axiosError;
    }
  }
};

export const CommitRegistrations = async (stage_id: string) => {
  const JWT = await GetJWT();
  try {
    await axios.post(
      `${apiBaseUrl}/staged-records/commit?stage_id=${stage_id}`,
      {},
      {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json",
          Authorization: "Bearer " + JWT,
        },
      }
    );
  } catch (error: unknown) {
    return error;
  }
};

export const DiscardRegistrations = async (stage_id: string) => {
  const JWT = await GetJWT();
  try {
    await axios.post(
      `${apiBaseUrl}/staged-records/discard?stage_id=${stage_id}`,
      {},
      {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json",
          Authorization: "Bearer " + JWT,
        },
      }
    );
  } catch (error: unknown) {
    return error;
  }
};

export const SendCsv = async (formData: FormData, navigate: NavigateFunction) => {
  const JWT = await GetJWT();
  try {
    const response = await axios.post(`${apiBaseUrl}/upload-file`, formData, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "multipart/form-data",
        Authorization: "Bearer " + JWT,
      },
      timeout: 3000,
    });

    const report_id = response?.data?.report_id;

    if (report_id !== null && report_id !== undefined) {
      const cookies = new Cookies();
      cookies.set("stage_id", report_id, { path: "/" });
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : undefined;
    if (message !== "timeout of 3000ms exceeded") {
      navigate("/error", { state: { error: message }, replace: true });
    }
  }
};

export const handleStagedResults = async (
  stagedRecords: StagedRecordsData,
  navigate: NavigateFunction
) => {
  console.log(stagedRecords);
  const staged_id = stagedRecords.stage_id;
  const cookies = new Cookies();
  cookies.set("stage_id", staged_id, { path: "/" });
  try {
    const records = stagedRecords.records ?? [];
    if (records.length === 0) {
      await CommitRegistrations(staged_id);
      await GetReport(staged_id, navigate);
      cookies.remove("stage_id");
    } else {
      ShowPreValidation(stagedRecords.records as unknown[], navigate);
    }
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "An unknown error occurred";
    navigate("/error", { state: { error: message }, replace: true });
  }
};

export const CheckStageProcesses = async (): Promise<StageProcessesResponse | AxiosError> => {
  const JWT = await GetJWT();
  let res: StageProcessesResponse | AxiosError = {};
  try {
    await axios
      .get(`${apiBaseUrl}/stage`, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json",
          Authorization: "Bearer " + JWT,
        },
        params: {
          stagedProcessOnly: "Yes",
        },
      })
      .then((response) => {
        res = response.data;
      })
      .catch((error: AxiosError) => {
        res = error;
      });
  } catch (error: unknown) {
    return error as AxiosError;
  }
  return res;
};

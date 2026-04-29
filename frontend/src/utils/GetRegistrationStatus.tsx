import { useEffect, useState } from "react";
import axios, { AxiosError }from "axios";
import { fetchAuthSession } from "aws-amplify/auth";
import { config } from "./Config";

type viewRegistrationsRecord = {
    licence_number: string;
    operator_name: string;
    total_services: number;
    requires_attention: number;
    licence_status: string;
  }
const useRegistrationStatus = () => {
    const [data, setData] = useState<viewRegistrationsRecord[]|null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const apiBaseUrl = config.publicApiUrl;
                let jwt = "";
                fetchAuthSession().then(async () => {
                Object.entries(localStorage).forEach(([key, value]) => {
                    if (key.includes("accessToken")) {
                        jwt = value.toString();
                    }
                });
                axios.get(
                    `${apiBaseUrl}/view-registrations/status`,
                    {
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            "Authorization": "Bearer " + jwt,
                        },
                    }
                ).then((response) => {
                setData(response.data);
                }).catch((error) => {
                    setError(error);
                });
            });
            } catch (error: AxiosError | any) {
                setError(error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    return { data, loading, error };
};

export default useRegistrationStatus;

import { useEffect, useState } from "react";
import axios from "axios";
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
                const apiBaseUrl = process.env.REACT_APP_API_URL || "";
                let jwt = "";
                Object.entries(localStorage).forEach(([key, value]) => {
                    if (key.includes("accessToken")) {
                        jwt = value.toString();
                    }
                });

                const response = await axios.get(
                    `${apiBaseUrl}/view-registrations/status`,
                    {
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            Authorization: "Bearer " + jwt,
                        },
                    }
                );

                setData(response.data);
            } catch (error) {
                setError(error as any);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    return { data, loading, error };
};

export default useRegistrationStatus;

import { useEffect, useState } from "react";
import axios from "axios";

const useGetAllRecords = () => {
    const [data, setData] = useState<null>(null);
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
                    `${apiBaseUrl}all-records`,
                    {
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            Authorization: "Bearer " + jwt,
                        },
                    }
                );

                setData(response.data);
                // download it as csv
                const csv = response.data.map((row: any) => Object.values(row).join(",")).join("\n");
                const blob = new Blob([csv], { type: "text/csv" });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "all-records.csv"; 
                a.click();
                window.URL.revokeObjectURL(url);

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

export default useGetAllRecords;
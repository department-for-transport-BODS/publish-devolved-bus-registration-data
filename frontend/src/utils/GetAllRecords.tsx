import axios from "axios";

const GetAllRecords = async () => {


 
            try {
                const apiBaseUrl = process.env.REACT_APP_API_URL || "";
                let jwt = "";
                Object.entries(localStorage).forEach(([key, value]) => {
                    if (key.includes("accessToken")) {
                        jwt = value.toString();
                    }
                });

                const response = await axios.get(
                    `${apiBaseUrl}/all-records`,
                    {
                        headers: {
                            "Access-Control-Allow-Origin": "*",
                            "Content-Type": "application/json",
                            Authorization: "Bearer " + jwt,
                        },
                    }
                );

                // download it as csv
                const headers = Object.keys(response.data[0]).join(","); // Get the headers from the first row
                // add " to each value that has a comma in it
                response.data.forEach((row: any) => {
                    Object.entries(row).forEach(([key, value]) => {
                        if (typeof value === "string" && value.includes(",")) {
                            row[key] = `"${value}"`;
                        }
                    });
                })
                const csv = [headers, ...response.data.map((row: any) => Object.values(row).join(","))].join("\n"); // Include headers in the CSV
                const blob = new Blob([csv], { type: "text/csv" }); // Set encoding to UTF-8
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "all-records.csv"; 
                a.click();
                window.URL.revokeObjectURL(url);
                } catch (error) {
                     throw new Error("Failed to download CSV");
                    
        }

};

export default GetAllRecords;
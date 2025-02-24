// import { useState } from "react";
// import axios from "axios";

// export default function Home() {
//   const [industry, setIndustry] = useState("");
//   const [compliance, setCompliance] = useState("");
//   const [policy, setPolicy] = useState("");

//   const generatePolicy = async () => {
//     try {
//       const response = await axios.post(
//         "http://127.0.0.1:5000/generate-policy",
//         {
//           industry,
//           compliance,
//         }
//       );
//       setPolicy(response.data.policy);
//     } catch (error) {
//       console.error("Error generating policy:", error);
//     }
//   };

//   return (
//     <div>
//       <h1>AI-Powered Policy Generator</h1>
//       <input
//         type="text"
//         placeholder="Industry"
//         value={industry}
//         onChange={(e) => setIndustry(e.target.value)}
//       />
//       <input
//         type="text"
//         placeholder="Compliance"
//         value={compliance}
//         onChange={(e) => setCompliance(e.target.value)}
//       />
//       <button onClick={generatePolicy}>Generate Policy</button>
//       <pre>{policy}</pre>
//     </div>
//   );
// }


import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [industry, setIndustry] = useState("");
  const [compliance, setCompliance] = useState("");
  const [policy, setPolicy] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Generate Policy
  const generatePolicy = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/generate-policy", {
        industry,
        compliance,
      });
      setPolicy(response.data.policy);
    } catch (error) {
      console.error("Error generating policy:", error);
    }
    setIsLoading(false);
  };

  // Fetch Policy from Database
  const fetchPolicy = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:5000/get-policy", {
        params: { industry, compliance },
      });
      setPolicy(response.data.policy);
    } catch (error) {
      console.error("Error fetching policy:", error);
    }
    setIsLoading(false);
  };

  // Update Policy in Database
  const updatePolicy = async () => {
    setIsLoading(true);
    try {
      await axios.put("http://127.0.0.1:5000/update-policy", {
        industry,
        compliance,
        policy,
      });
      alert("Policy updated successfully!");
      setIsEditing(false);
    } catch (error) {
      console.error("Error updating policy:", error);
    }
    setIsLoading(false);
  };

  return (
    <div>
      <h1>AI-Powered Policy Generator</h1>
      <input
        type="text"
        placeholder="Industry"
        value={industry}
        onChange={(e) => setIndustry(e.target.value)}
      />
      <input
        type="text"
        placeholder="Compliance"
        value={compliance}
        onChange={(e) => setCompliance(e.target.value)}
      />
      <button onClick={generatePolicy} disabled={isLoading}>
        {isLoading ? "Generating..." : "Generate Policy"}
      </button>
      <button onClick={fetchPolicy} disabled={isLoading}>
        {isLoading ? "Fetching..." : "Fetch Policy"}
      </button>

      {policy && (
        <div>
          <textarea
            value={policy}
            onChange={(e) => setPolicy(e.target.value)}
            disabled={!isEditing}
            rows={10}
            cols={50}
          />
          <button onClick={() => setIsEditing(!isEditing)}>
            {isEditing ? "Cancel Edit" : "Edit Policy"}
          </button>
          {isEditing && (
            <button onClick={updatePolicy} disabled={isLoading}>
              {isLoading ? "Updating..." : "Save Changes"}
            </button>
          )}
        </div>
      )}
    </div>
  );
}

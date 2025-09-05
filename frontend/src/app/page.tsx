"use client";
import React, { useState } from "react";

interface CircuitData {
  projectId: string;
  projectName: string;
  [key: string]: any;
}

export default function HomePage() {
  const [circuitData, setCircuitData] = useState<CircuitData | null>(null);
  const [message, setMessage] = useState<string>("");

  const projectId = "proj_1a2b3c4d";
  const apiUrl = `http://127.0.0.1:5000/api/circuit/${projectId}`;

  const handleLoad = async () => {
    try {
      setMessage("正在从后端加载数据...");
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: CircuitData = await response.json();
      setCircuitData(data);
      setMessage("数据加载成功！");
    } catch (error) {
      console.error("加载数据失败:", error);
      setMessage(`加载数据失败: ${error}`);
    }
  };

  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>面包板电路前后端交互演示</h1>

      <div style={{ margin: "2rem 0" }}>
        <button
          onClick={handleLoad}
          style={{ marginRight: "1rem", padding: "0.5rem 1rem" }}
        >
          从后端加载数据
        </button>
      </div>

      {message && <p style={{ color: "blue" }}>状态: {message}</p>}

      <h2>当前前端的电路数据:</h2>
      {circuitData ? (
        <pre
          style={{
            background: "#f0f0f0",
            padding: "1rem",
            borderRadius: "5px",
            whiteSpace: "pre-wrap",
          }}
        >
          {JSON.stringify(circuitData, null, 2)}
        </pre>
      ) : (
        <p>暂无数据。请点击“加载数据”按钮。</p>
      )}
    </main>
  );
}

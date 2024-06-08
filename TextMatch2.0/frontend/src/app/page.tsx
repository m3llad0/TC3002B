"use client";
import React, { useState } from "react";
import axios from "axios";

const api = process.env.REACT_APP_API_URL;

export default function Home() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<{ plgarised_text?: boolean; results: any }>();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const response = await axios.post("http://127.0.0.1:5000/plagarsim", { text });
      setResult(response.data);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <main className="w-full h-svh bg-white">
      <section className="mx-auto py-20 px-20 flex flex-col justify-center items-center gap-y-8">
        <h1 className=" text-gray-900 text-4xl font-bold">Text Match</h1>
        <div className="flex flex-col gap-y-10 items-center">
          <textarea
            onChange={(e) => setText(e.target.value)}
            placeholder="Your paper abstract here ..."
            className="w-[45vw] h-[50vh] mx-10 outline-none focus:outline-none focus:ring-2 text-gray-800 border-2 border-[#06D6A0] rounded-2xl"
          />
        </div>

        <button
          onClick={handleSubmit}
          type="button"
          className="text-white bg-[#EF476F] hover:bg-[#EB1E4E] focus:ring-4 focus:outline-none focus:ring-[#F47C98] font-medium rounded-3xl text-sm px-6 py-2.5 text-center md:mr-0 w-fit"
        >
          Enviar
        </button>

        {loading && <p className="text-gray-900">Loading...</p>}

        {result && !loading && (
          <div>
            {result.plgarised_text ? (
              <div className="flex flex-row items-center">
                <p className="text-gray-900">Plagio detectado</p>
                <p className="text-gray-900">Archivo original</p>
                <ul>
                  {Object.entries(result.results.original_files).map(([fileName, similarity]) => (
                    <li key={fileName} className="text-gray-900">
                      {fileName}: {String(similarity)}
                    </li>
                  ))}
                </ul>
                <p className="text-gray-900">Tipo de plagio: {result.results.plagiarism_type}</p>
              </div>
            ) : (
              <p className="text-gray-900">No hay plagio</p>
            )}
          </div>
        )}
      </section>
    </main>
  );
}

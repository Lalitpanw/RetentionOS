// This is a basic Next.js SaaS-style landing page for RetentionOS
the project uses Tailwind CSS for styling

import Head from "next/head";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <Head>
        <title>RetentionOS – Predict. Segment. Re-engage.</title>
      </Head>

      <header className="bg-white shadow-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">RetentionOS</h1>
          <nav>
            <a href="#features" className="mr-6 hover:text-blue-600">Features</a>
            <a href="#demo" className="hover:text-blue-600">Try Demo</a>
          </nav>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-20">
        <section className="text-center">
          <h2 className="text-4xl font-extrabold mb-4">Predict. Segment. Re-engage.</h2>
          <p className="text-lg text-gray-600 mb-6">
            Upload your user data and get churn risk predictions instantly.
          </p>
          <a
            href="https://your-streamlit-app.streamlit.app"
            target="_blank"
            className="inline-block bg-blue-600 text-white px-6 py-3 rounded-xl shadow hover:bg-blue-700"
          >
            Launch Tool
          </a>
        </section>

        <section id="features" className="mt-20">
          <h3 className="text-2xl font-bold mb-4">Key Features</h3>
          <ul className="space-y-4">
            <li className="bg-white p-4 rounded shadow">
              📊 Churn Risk Prediction based on behavior data
            </li>
            <li className="bg-white p-4 rounded shadow">
              🧠 Smart Segments: High, Medium, Low risk users
            </li>
            <li className="bg-white p-4 rounded shadow">
              💬 Nudge Message Suggestions to retain users
            </li>
          </ul>
        </section>

        <section id="demo" className="mt-20">
          <h3 className="text-2xl font-bold mb-4">Live Demo</h3>
          <iframe
            src="https://your-streamlit-app.streamlit.app"
            className="w-full h-[600px] border rounded shadow"
            title="RetentionOS Live Demo"
          ></iframe>
        </section>
      </main>

      <footer className="text-center text-sm text-gray-500 mt-20 pb-10">
        Built by Lalit · RetentionOS · 2025
      </footer>
    </div>
  );
}

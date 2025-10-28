// page.tsx (Next.js App Router)
'use client';

import { useState, useEffect } from 'react';

interface NgramResult {
  ngram: string;
  count: number;
  probability: number;
}

interface AnalysisResponse {
  results: NgramResult[];
  totalCount: number;
  uniqueCount: number;
  ngramType: string;
}

export default function Home() {
  const [files, setFiles] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>('');
  const [tokenType, setTokenType] = useState<'normal' | 'normalized'>('normal');
  const [ngramType, setNgramType] = useState<'unigram' | 'bigram' | 'trigram'>('unigram');
  const [results, setResults] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const API_URL = 'http://127.0.0.1:5000/api';

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      console.log('fetching');
      
      const response = await fetch(`${API_URL}/files`);
      const data = await response.json();
      setFiles(data.files);
      if (data.files.length > 0) {
        setSelectedFile(data.files[0]);
      }
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert('Please select a file');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          filename: selectedFile,
          tokenType,
          ngramType,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setResults(data);
      } else {
        alert(data.error || 'Analysis failed');
      }
    } catch (error) {
      console.error('Error analyzing:', error);
      alert('Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-purple-600 to-indigo-700 p-6">
      <div className="max-w-7xl mx-auto bg-white rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="bg-linear-to-r from-purple-600 to-indigo-700 text-white p-8 text-center">
          <h1 className="text-4xl font-bold mb-2">📊 N-gram Analyzer</h1>
          <p className="text-lg opacity-90">Analyze unigrams, bigrams, and trigrams from your text files</p>
        </div>

        {/* Controls */}
        <div className="p-8 bg-gray-50 border-b border-gray-200">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Select File
              </label>
              <select
                value={selectedFile}
                onChange={(e) => setSelectedFile(e.target.value)}
                className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-purple-600 focus:outline-none"
              >
                {files.map((file) => (
                  <option key={file} value={file}>
                    {file}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Token Type
              </label>
              <select
                value={tokenType}
                onChange={(e) => setTokenType(e.target.value as 'normal' | 'normalized')}
                className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-purple-600 focus:outline-none"
              >
                <option value="normal">Normal Tokens</option>
                <option value="normalized">Normalized Tokens</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                N-gram Type
              </label>
              <select
                value={ngramType}
                onChange={(e) => setNgramType(e.target.value as 'unigram' | 'bigram' | 'trigram')}
                className="w-full p-3 border-2 border-gray-300 rounded-lg focus:border-purple-600 focus:outline-none"
              >
                <option value="unigram">Unigram</option>
                <option value="bigram">Bigram</option>
                <option value="trigram">Trigram</option>
              </select>
            </div>

            <div className="flex items-end">
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full p-3 bg-linear-to-r from-purple-600 to-indigo-700 text-white rounded-lg font-semibold hover:shadow-lg transition disabled:opacity-50"
              >
                {loading ? 'Analyzing...' : 'Analyze'}
              </button>
            </div>
          </div>
        </div>

        {/* Results */}
        <div className="p-8">
          {results ? (
            <>
              {/* Statistics */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div className="bg-linear-to-r from-purple-600 to-indigo-700 text-white p-6 rounded-xl shadow-lg">
                  <h3 className="text-sm opacity-90 mb-2">Total {results.ngramType}s</h3>
                  <div className="text-4xl font-bold">{results.totalCount.toLocaleString()}</div>
                </div>
                <div className="bg-linear-to-r from-purple-600 to-indigo-700 text-white p-6 rounded-xl shadow-lg">
                  <h3 className="text-sm opacity-90 mb-2">Unique {results.ngramType}s</h3>
                  <div className="text-4xl font-bold">{results.uniqueCount.toLocaleString()}</div>
                </div>
              </div>

              {/* Table */}
              <div className="overflow-x-auto rounded-xl shadow-lg">
                <table className="w-full">
                  <thead className="bg-linear-to-r from-purple-600 to-indigo-700 text-white">
                    <tr>
                      <th className="p-4 text-left">Rank</th>
                      <th className="p-4 text-left">{results.ngramType}</th>
                      <th className="p-4 text-left">Count</th>
                      <th className="p-4 text-left">Probability</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.results.map((result, index) => (
                      <tr
                        key={index}
                        className="border-b border-gray-200 hover:bg-gray-50 transition"
                      >
                        <td className="p-4">{index + 1}</td>
                        <td className="p-4 font-mono text-gray-700">{result.ngram}</td>
                        <td className="p-4">{result.count.toLocaleString()}</td>
                        <td className="p-4">{result.probability.toFixed(6)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          ) : (
            <div className="text-center py-20 text-gray-400">
              <svg
                className="w-24 h-24 mx-auto mb-4 opacity-50"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <h2 className="text-2xl font-semibold mb-2">No Results Yet</h2>
              <p>Upload a file and click &quot;Analyze&quot; to see n-gram statistics</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
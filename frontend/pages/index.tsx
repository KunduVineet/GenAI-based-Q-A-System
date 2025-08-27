import { useState } from 'react'
import Head from 'next/head'
import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface ApiResponse {
  success: boolean
  message: string
  data: any
}

export default function Home() {
  const [activeTab, setActiveTab] = useState('summarize')
  const [inputText, setInputText] = useState('')
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Additional fields for different features
  const [question, setQuestion] = useState('')
  const [targetTone, setTargetTone] = useState('professional')
  const [targetLanguage, setTargetLanguage] = useState('Spanish')
  const [maxLength, setMaxLength] = useState(100)

  const handleSubmit = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text')
      return
    }

    setLoading(true)
    setError('')
    setResult('')

    try {
      let endpoint = ''
      let payload: any = {}

      switch (activeTab) {
        case 'summarize':
          endpoint = '/api/v1/ai/summarize'
          payload = { text: inputText, max_length: maxLength }
          break
        case 'question-answer':
          endpoint = '/api/v1/ai/question-answer'
          payload = { context: inputText, question: question }
          break
        case 'tone-rewrite':
          endpoint = '/api/v1/ai/tone-rewrite'
          payload = { text: inputText, target_tone: targetTone }
          break
        case 'translate':
          endpoint = '/api/v1/ai/translate'
          payload = { text: inputText, target_language: targetLanguage }
          break
      }

      const response = await axios.post(`${API_BASE_URL}${endpoint}`, payload)
      const data: ApiResponse = response.data

      if (data.success) {
        switch (activeTab) {
          case 'summarize':
            setResult(data.data.summary)
            break
          case 'question-answer':
            setResult(data.data.answer)
            break
          case 'tone-rewrite':
            setResult(data.data.rewritten_text)
            break
          case 'translate':
            setResult(data.data.translation)
            break
        }
      } else {
        setError(data.message || 'Something went wrong')
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to connect to AI service')
    } finally {
      setLoading(false)
    }
  }

  const tabs = [
    { id: 'summarize', name: 'Summarize Text', icon: '📝' },
    { id: 'question-answer', name: 'Ask Questions', icon: '❓' },
    { id: 'tone-rewrite', name: 'Change Tone', icon: '✨' },
    { id: 'translate', name: 'Translate', icon: '🌍' }
  ]

  return (
    <>
      <Head>
        <title>AI Text Assistant</title>
        <meta name="description" content="AI-powered text processing tools" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen gradient-bg">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">
              🤖 AI Text Assistant
            </h1>
            <p className="text-xl text-white opacity-90">
              Powerful AI tools to help you with text processing
            </p>
          </div>

          {/* Main Card */}
          <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl overflow-hidden">
            {/* Tabs */}
            <div className="flex flex-wrap border-b">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 min-w-0 px-4 py-4 text-center font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'bg-primary-500 text-white'
                      : 'text-gray-600 hover:text-primary-600 hover:bg-gray-50'
                  }`}
                >
                  <div className="text-2xl mb-1">{tab.icon}</div>
                  <div className="text-sm">{tab.name}</div>
                </button>
              ))}
            </div>

            {/* Content */}
            <div className="p-8">
              {/* Input Section */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {activeTab === 'question-answer' ? 'Context/Text to analyze:' : 'Enter your text:'}
                </label>
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder={
                    activeTab === 'summarize' ? 'Enter the text you want to summarize...' :
                    activeTab === 'question-answer' ? 'Enter the context or article you want to ask about...' :
                    activeTab === 'tone-rewrite' ? 'Enter the text you want to rewrite...' :
                    'Enter the text you want to translate...'
                  }
                  className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                />
              </div>

              {/* Additional Fields */}
              {activeTab === 'question-answer' && (
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Your Question:
                  </label>
                  <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="What do you want to know about the text above?"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              )}

              {activeTab === 'tone-rewrite' && (
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Target Tone:
                  </label>
                  <select
                    value={targetTone}
                    onChange={(e) => setTargetTone(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="professional">Professional</option>
                    <option value="casual">Casual</option>
                    <option value="friendly">Friendly</option>
                    <option value="formal">Formal</option>
                    <option value="enthusiastic">Enthusiastic</option>
                  </select>
                </div>
              )}

              {activeTab === 'translate' && (
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Translate to:
                  </label>
                  <select
                    value={targetLanguage}
                    onChange={(e) => setTargetLanguage(e.target.value)}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="Spanish">Spanish</option>
                    <option value="French">French</option>
                    <option value="German">German</option>
                    <option value="Italian">Italian</option>
                    <option value="Portuguese">Portuguese</option>
                    <option value="Chinese">Chinese</option>
                    <option value="Japanese">Japanese</option>
                    <option value="Korean">Korean</option>
                  </select>
                </div>
              )}

              {activeTab === 'summarize' && (
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Summary Length (words):
                  </label>
                  <input
                    type="number"
                    value={maxLength}
                    onChange={(e) => setMaxLength(parseInt(e.target.value) || 100)}
                    min="20"
                    max="500"
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              )}

              {/* Submit Button */}
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="w-full bg-primary-500 hover:bg-primary-600 disabled:bg-gray-400 text-white font-medium py-4 px-6 rounded-lg transition-colors text-lg"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                    Processing...
                  </div>
                ) : (
                  `${tabs.find(t => t.id === activeTab)?.icon} ${tabs.find(t => t.id === activeTab)?.name}`
                )}
              </button>

              {/* Error */}
              {error && (
                <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-600">❌ {error}</p>
                </div>
              )}

              {/* Result */}
              {result && (
                <div className="mt-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Result:
                  </label>
                  <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                    <p className="text-gray-800 whitespace-pre-wrap">{result}</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Footer */}
          <div className="text-center mt-12">
            <p className="text-white opacity-75">
              Powered by Google Gemini AI • Built with Next.js & FastAPI
            </p>
          </div>
        </div>
      </div>
    </>
  )
}
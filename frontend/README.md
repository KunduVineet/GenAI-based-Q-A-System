# AI Text Assistant Frontend

A beautiful, user-friendly web interface for the AI Backend Service.

## Features

🤖 **AI-Powered Tools:**
- Text Summarization
- Question Answering
- Tone Rewriting
- Translation

✨ **User Experience:**
- Clean, modern interface
- Responsive design
- Real-time processing
- Error handling

## Quick Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
```bash
cp .env.local.example .env.local
# Edit .env.local with your backend URL
```

### 3. Run Development Server
```bash
npm run dev
```

Visit http://localhost:3000

## Deploy to Vercel

### Option 1: Vercel CLI
```bash
npm install -g vercel
vercel
```

### Option 2: GitHub Integration
1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy automatically

### Environment Variables for Production
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

## Project Structure
```
frontend/
├── pages/
│   ├── _app.tsx          # App wrapper
│   └── index.tsx         # Main page
├── styles/
│   └── globals.css       # Global styles
├── package.json          # Dependencies
├── next.config.js        # Next.js config
├── tailwind.config.js    # Tailwind CSS config
└── vercel.json          # Vercel deployment config
```

## Usage

1. **Text Summarization**: Enter long text, get concise summary
2. **Question Answering**: Provide context and ask questions
3. **Tone Rewriting**: Change text tone (professional, casual, etc.)
4. **Translation**: Translate text to different languages

## Technologies Used

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - API calls
- **Vercel** - Deployment platform
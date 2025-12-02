# HFRL Integration Hub

Human Feedback Reinforcement Learning Platform - A comprehensive web application for training and improving AI models through human feedback.

## Overview

HFRL Integration Hub provides an intuitive interface for developers and non-technical users to interact with AI models, provide feedback, and track improvements over time. The platform supports multiple AI providers including OpenAI, Anthropic, Deepseek, and Kimi K2.

## Features

### Core Functionality
- **Multi-Provider Support**: Connect to OpenAI, Anthropic, Deepseek, and Kimi K2
- **Interactive Workspace**: Generate content with customizable parameters
- **Feedback System**: Rate and comment on AI responses
- **Analytics Dashboard**: Track performance metrics and improvements
- **Visual Customization**: Multiple themes and color schemes
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Technical Features
- RESTful API backend with FastAPI
- Real-time feedback integration
- Comprehensive error handling
- Request logging and monitoring
- Input validation and security
- CORS support for cross-origin requests

## Quick Start

### Local Development

See [QUICKSTART.md](QUICKSTART.md) for detailed 5-minute setup guide.

**Quick commands:**
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Frontend (new terminal)
python -m http.server 8080
```

### Deploy to Production

**Recommended: Vercel + Render (Free tier available)**

See [DEPLOY-VERCEL-RENDER.md](DEPLOY-VERCEL-RENDER.md) for complete step-by-step guide.

**Quick deploy:**
1. Push code to GitHub
2. Deploy backend on Render (5 min)
3. Deploy frontend on Vercel (2 min)
4. Update CORS and API URLs (2 min)
5. Done! 🎉

**Other options:**
- [DEPLOYMENT.md](DEPLOYMENT.md) - All deployment options
- [QUICK-DEPLOY-GUIDE.md](QUICK-DEPLOY-GUIDE.md) - 5-minute reference
- [deploy.sh](deploy.sh) - Automated deployment script

## Project Structure

```
hfrl-integration-hub/
├── index.html              # Main workspace page
├── analytics.html          # Analytics dashboard
├── documentation.html      # Documentation page
├── settings.html           # Settings and configuration
├── main.js                 # Frontend JavaScript
├── resources/              # Images and assets
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── routers/       # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── config.py      # Configuration
│   │   ├── schemas.py     # Data models
│   │   └── exceptions.py  # Custom exceptions
│   ├── main.py            # Application entry
│   └── requirements.txt   # Python dependencies
└── README.md              # This file
```

## Usage

### 1. Configure API Keys (One-time setup)

1. Go to **Settings** page
2. Enter your API keys for the providers you want to use:
   - OpenAI API Key ([Get key](https://platform.openai.com/api-keys))
   - Anthropic API Key ([Get key](https://console.anthropic.com/))
   - Deepseek API Key ([Get key](https://platform.deepseek.com/))
   - Kimi K2 API Key ([Get key](https://platform.moonshot.cn/))
3. Click **"Test"** for each provider to verify
4. Click **"Save All API Keys"**

**Note**: API keys are stored securely in your browser's localStorage and never sent to our servers.

### 2. Generate Content

1. Go to **Workspace** (home page)
2. Select a model provider and model
3. Choose a task type (dialogue, code, story, etc.)
4. Enter your prompt
5. Adjust temperature and max tokens
6. Click **"Generate Content"**

### 3. Provide Feedback

1. Rate the response (1-5 stars)
2. Add comments about quality
3. Select learning rate
4. Click **"Apply Feedback"**

### 4. Track Progress

Visit the **Analytics** page to see:
- Average quality scores
- Improvement rates
- Training statistics
- Session history

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Key Endpoints

```
POST /api/models/generate       - Generate AI content
POST /api/models/test-connection - Test API connection
POST /api/feedback              - Submit feedback
GET  /api/analytics             - Get analytics data
GET  /api/settings              - Get settings
PUT  /api/settings              - Update settings
```

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
DEEPSEEK_API_KEY=your_key_here
KIMI_API_KEY=your_key_here

# Application Settings
DEBUG=False
SECRET_KEY=your-secret-key
RATE_LIMIT_PER_MINUTE=60
REQUEST_TIMEOUT=60
```

### CORS Configuration

Edit `backend/app/config.py` to add allowed origins:

```python
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://yourdomain.com"
]
```

## Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Use HTTPS in production** - Encrypt data in transit
3. **Implement rate limiting** - Prevent abuse
4. **Validate all inputs** - Prevent injection attacks
5. **Keep dependencies updated** - Patch security vulnerabilities
6. **Use strong secrets** - Generate secure SECRET_KEY
7. **Enable CORS selectively** - Only allow trusted origins

## Troubleshooting

### Backend Won't Start
- Check Python version (3.8+)
- Verify all dependencies are installed
- Check if port 8000 is available
- Review error logs

### API Connection Fails
- Verify API keys are correct
- Check internet connection
- Ensure backend server is running
- Review CORS settings

### Frontend Not Loading
- Use a local server (not file://)
- Check browser console for errors
- Verify all CDN resources load
- Clear browser cache

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Check the Documentation page
- Review API documentation
- Check browser console for errors
- Review backend logs

## Roadmap

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication and authorization
- [ ] Team collaboration features
- [ ] Model fine-tuning capabilities
- [ ] Advanced analytics and reporting
- [ ] Export/import training data
- [ ] Webhook integrations
- [ ] Mobile app

## Acknowledgments

Built with:
- FastAPI - Modern Python web framework
- Tailwind CSS - Utility-first CSS framework
- ECharts - Powerful charting library
- Anime.js - Animation library
- p5.js - Creative coding library

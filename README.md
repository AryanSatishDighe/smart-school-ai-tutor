# Smart School AI Tutor (Classes 5–10)

A simple Python + Streamlit app that uses the Gemini API to answer school questions.

## Files
- `app.py` — chatbot application
- `requirements.txt` — Python dependencies

## 1. Get a Gemini API key
Create a key at https://aistudio.google.com/app/apikey.
Keep it private. Do not paste it into `app.py` or commit it to GitHub.

## 2. Upload the files to GitHub
Create a new repository, for example `smart-school-ai-tutor`, and upload:
- `app.py`
- `requirements.txt`

Do not upload a file containing your API key.

## 3. Deploy on Streamlit Community Cloud
1. Visit https://share.streamlit.io/
2. Sign in with GitHub.
3. Choose **Create app** and select your repository.
4. Set the main file path to `app.py`.
5. Deploy the app.

## 4. Add the API key as a secret
In your deployed app, open **Settings → Secrets** and add:

```toml
GEMINI_API_KEY = "paste_your_real_key_here"
```

Replace the placeholder with your real key. Do not share screenshots showing the key.

## 5. Test
Select a class and ask a question such as:
- What is photosynthesis?
- Solve 2x + 5 = 17 step by step.
- Explain the water cycle in simple words.

## Troubleshooting
- **API key not found:** Check that the secret is named exactly `GEMINI_API_KEY`.
- **401/403:** Check the key and whether the API is enabled for your project.
- **429:** You may have reached your API quota or rate limit.
- **404/model not found:** The default model in `app.py` (`gemini-2.5-flash`) may not be available for your key. Check the official models list at https://ai.google.dev/gemini-api/docs/models and replace `MODEL_NAME` in `app.py` with a model available to your account.
- **503:** The service may be temporarily busy; wait and try again.

## Cost note
Streamlit, GitHub, and the code are free to start. Gemini API use is subject to the provider's current free-tier eligibility, quotas, and pricing. Free use and uninterrupted availability are not guaranteed.
